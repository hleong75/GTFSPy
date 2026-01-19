#!/usr/bin/env python3
"""
Python-for-Android build hook for GTFSPy

This hook installs libtool before the build starts to fix the libffi compilation error.
The error occurs because libffi's configure.ac requires AC_PROG_LIBTOOL macro
which is provided by libtool package.

Error fixed:
  configure.ac:41: error: possibly undefined macro: AC_PROG_LIBTOOL
  configure:8578: error: possibly undefined macro: AC_PROG_LD
"""

import subprocess
import sys


def prebuild_hook(ctx):
    """
    Hook called before the build starts.
    Installs libtool to fix libffi compilation issues.
    """
    print("=" * 70)
    print("Running GTFSPy prebuild hook...")
    print("=" * 70)
    
    try:
        # Check if libtool is already installed
        result = subprocess.run(
            ['which', 'libtool'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✓ libtool already installed at: {result.stdout.strip()}")
        else:
            print("Installing libtool to fix libffi compilation...")
            
            # Install libtool using apt-get
            subprocess.run(
                ['apt-get', 'update'],
                check=True
            )
            subprocess.run(
                ['apt-get', 'install', '-y', 'libtool', 'libtool-bin'],
                check=True
            )
            
            print("✓ libtool installed successfully")
        
        # Verify installation
        result = subprocess.run(
            ['libtool', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"✓ Libtool version: {result.stdout.split()[3]}")
        print("=" * 70)
        print("Prebuild hook completed successfully")
        print("=" * 70)
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install libtool: {e}", file=sys.stderr)
        print("Attempting to continue build anyway...", file=sys.stderr)
    except Exception as e:
        print(f"WARNING: Prebuild hook encountered an error: {e}", file=sys.stderr)
        print("Attempting to continue build anyway...", file=sys.stderr)


def postbuild_hook(ctx):
    """
    Hook called after the build completes.
    """
    print("=" * 70)
    print("GTFSPy build completed!")
    print("=" * 70)
