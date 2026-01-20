# Building GTFSPy with p4a

This document explains how to build the GTFSPy Android APK using python-for-android (p4a) directly, without buildozer.

## Prerequisites

Install python-for-android:
```bash
pip install python-for-android
```

Install Android SDK and NDK (if not already installed):
```bash
# Install Android SDK
# Follow instructions at: https://developer.android.com/studio

# Set environment variables
export ANDROID_SDK_ROOT=/path/to/android-sdk
export ANDROID_NDK_HOME=/path/to/android-ndk
```

Install system dependencies (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y \
    git zip unzip openjdk-17-jdk \
    libtool libtool-bin automake autoconf \
    zlib1g-dev libffi-dev libssl-dev cmake \
    python3-pip python3-setuptools
```

## Building the APK

The build script automatically uses the `ANDROID_SDK_ROOT` and `ANDROID_NDK_HOME` environment variables if they are set. If not set, you need to set them:

```bash
export ANDROID_SDK_ROOT=/path/to/android-sdk
export ANDROID_NDK_HOME=/path/to/android-ndk
```

### Method 1: Using the build script (recommended)

Simply run:
```bash
./build_apk.sh
```

The script will automatically:
- Detect Android SDK and NDK paths from environment variables
- Pass the paths to p4a using `--sdk-dir` and `--ndk-dir` options
- Create the APK in the `dist/` directory.

### Method 2: Using p4a directly

Run p4a with the following command (make sure SDK and NDK paths are set):
```bash
p4a apk \
    --name GTFSPy \
    --package org.gtfspy.gtfspy \
    --version 1.0.0 \
    --requirements python3,kivy,kivymd,mapview,requests,pillow \
    --permission INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE \
    --orientation portrait \
    --android-api 33 \
    --ndk-api 21 \
    --ndk-version 25b \
    --arch arm64-v8a \
    --arch armeabi-v7a \
    --bootstrap sdl2 \
    --local-recipes p4a_recipes \
    --hook p4a_hook.py \
    --private . \
    --sdk-dir "$ANDROID_SDK_ROOT" \
    --ndk-dir "$ANDROID_NDK_HOME" \
    --release
```

## File Exclusions

The build process automatically excludes the following files from the APK:
- All `.md` files (documentation)
- `Log` file (build logs)
- `test_core.py` (test file)
- `create_sample_data.py` (test data generator)
- `buildozer.spec` (buildozer configuration, not needed for p4a)
- `.git` directory
- `.buildozer` directory

Only the essential Python application files are included in the APK.

## Configuration

Configuration is stored in `.p4a` file and can be modified as needed.

## Troubleshooting

### libffi build errors

The project includes a custom p4a hook (`p4a_hook.py`) and recipe (`p4a_recipes/libffi/`) that automatically fix libffi compilation issues by installing libtool.

### Missing dependencies

If you encounter missing dependency errors, ensure all system dependencies are installed:
```bash
sudo apt-get install -y libtool libtool-bin automake autoconf
```

## Comparison with buildozer

- **buildozer**: Higher-level tool that wraps p4a, simpler but less control
- **p4a**: Lower-level tool with more control and flexibility

By using p4a directly, you have more control over the build process and can fine-tune settings.
