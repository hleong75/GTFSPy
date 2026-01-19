from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory
from pythonforandroid.logger import shprint
from os.path import join
import sh


class LibffiRecipe(Recipe):
    """
    Custom libffi recipe that fixes the AC_PROG_LIBTOOL error.
    
    This recipe ensures libtool is installed before building libffi,
    which is required for the autoconf macros to work properly.
    
    Error fixed:
      configure.ac:41: error: possibly undefined macro: AC_PROG_LIBTOOL
      configure:8578: error: possibly undefined macro: AC_PROG_LD
    """
    
    version = '3.4.6'
    url = 'https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz'
    
    patches = []
    
    def should_build(self, arch):
        return not self.has_libs(arch, 'libffi.so')
    
    def prebuild_arch(self, arch):
        """Install libtool before building"""
        super().prebuild_arch(arch)
        
        # Install libtool if not already present
        try:
            sh.which('libtool')
            print("libtool is already installed")
        except sh.ErrorReturnCode:
            print("Installing libtool...")
            try:
                shprint(sh.apt_get, 'update', _tail=10)
                shprint(sh.apt_get, 'install', '-y', 'libtool', 'libtool-bin', 
                       'automake', 'autoconf', _tail=10)
                print("libtool installed successfully")
            except Exception as e:
                print(f"Warning: Could not install libtool automatically: {e}")
                print("Please ensure libtool is installed in your build environment")
    
    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        
        with current_directory(self.get_build_dir(arch.arch)):
            # Configure
            configure = sh.Command('./configure')
            shprint(configure,
                    '--host=' + arch.command_prefix,
                    '--prefix=' + self.ctx.get_python_install_dir(arch.arch),
                    '--disable-builddir',
                    '--enable-shared',
                    _env=env)
            
            # Build
            shprint(sh.make, '-j4', _env=env)
            shprint(sh.make, 'install', _env=env)


recipe = LibffiRecipe()
