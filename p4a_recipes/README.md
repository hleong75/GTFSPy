# Python-for-Android Custom Recipes

This directory contains custom recipes for python-for-android (p4a) used by buildozer when compiling the GTFSPy Android application.

## What are P4A Recipes?

Python-for-android recipes are build instructions for compiling Python packages and their native dependencies for Android. They handle:
- Downloading source code
- Applying patches
- Running configure scripts
- Compiling native code
- Installing libraries

## Custom Recipes in this Directory

### libffi

**Purpose**: Fixes the libffi compilation error that occurs due to missing libtool macros.

**Error Fixed**:
```
configure.ac:41: error: possibly undefined macro: AC_PROG_LIBTOOL
configure:8578: error: possibly undefined macro: AC_PROG_LD
```

**Solution**: 
- Uses libffi version 3.4.6 (stable and tested)
- Automatically installs libtool before building
- Configures libffi with appropriate Android settings

**File**: `libffi/__init__.py`

## How These Recipes are Used

The custom recipes in this directory are activated through the `buildozer.spec` file:

```ini
p4a.local_recipes = p4a_recipes
```

When buildozer runs, it will:
1. Check this directory for custom recipes
2. Use custom recipes instead of default p4a recipes when available
3. Fall back to default recipes for packages not found here

## Adding More Custom Recipes

To add a new custom recipe:

1. Create a new directory: `mkdir p4a_recipes/<package_name>/`
2. Create `__init__.py` with the recipe class
3. Inherit from `pythonforandroid.recipe.Recipe`
4. Override necessary methods (e.g., `build_arch`, `prebuild_arch`)

Example structure:
```
p4a_recipes/
├── README.md (this file)
├── libffi/
│   └── __init__.py
└── your_package/
    └── __init__.py
```

## References

- [Python-for-Android Recipes Documentation](https://python-for-android.readthedocs.io/en/latest/recipes/)
- [Writing Custom Recipes](https://python-for-android.readthedocs.io/en/latest/recipes/#writing-recipes)
- [P4A Recipe Examples](https://github.com/kivy/python-for-android/tree/develop/pythonforandroid/recipes)
