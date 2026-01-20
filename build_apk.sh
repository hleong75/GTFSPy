#!/bin/bash
# Build script for GTFSPy using python-for-android directly
# This replaces the need for buildozer

set -e

echo "========================================================================"
echo "Building GTFSPy APK with python-for-android (p4a)"
echo "========================================================================"

# Configuration
APP_NAME="GTFSPy"
PACKAGE_NAME="org.gtfspy.gtfspy"
VERSION="1.0.0"
REQUIREMENTS="python3,kivy,kivymd,mapview,requests,pillow"
PERMISSIONS="INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE"
ORIENTATION="portrait"
ANDROID_API=33
ANDROID_MIN_API=21
ANDROID_NDK="25b"
ARCHS="arm64-v8a armeabi-v7a"
BOOTSTRAP="sdl2"
P4A_BRANCH="develop"

# Build directory
BUILD_DIR="./.p4a_build"
DIST_DIR="./dist"

# Excluded patterns (files not to include in APK)
EXCLUDE_PATTERNS="Log *.md test_core.py create_sample_data.py buildozer.spec"

echo ""
echo "Checking python-for-android installation..."
if ! python3 -m pip show python-for-android > /dev/null 2>&1; then
    echo "Installing python-for-android..."
    python3 -m pip install python-for-android
fi

echo ""
echo "Configuration:"
echo "  App Name: $APP_NAME"
echo "  Package: $PACKAGE_NAME"
echo "  Version: $VERSION"
echo "  Requirements: $REQUIREMENTS"
echo "  Android API: $ANDROID_API (min: $ANDROID_MIN_API)"
echo "  NDK: $ANDROID_NDK"
echo "  Architectures: $ARCHS"
echo "  Bootstrap: $BOOTSTRAP"
echo "  p4a Branch: $P4A_BRANCH"
echo "  Excluded files: $EXCLUDE_PATTERNS"
echo ""

# Create build directory
mkdir -p "$BUILD_DIR"
mkdir -p "$DIST_DIR"

# Copy source files (excluding patterns)
echo "Preparing source files..."
TEMP_SOURCE="$BUILD_DIR/source"
rm -rf "$TEMP_SOURCE"
mkdir -p "$TEMP_SOURCE"

# Copy all Python files and required resources
rsync -av \
    --exclude='.git' \
    --exclude='.buildozer' \
    --exclude='*.md' \
    --exclude='Log' \
    --exclude='test_core.py' \
    --exclude='create_sample_data.py' \
    --exclude='buildozer.spec' \
    --exclude='.p4a_build' \
    --exclude='dist' \
    --exclude='bin' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    ./ "$TEMP_SOURCE/"

echo "Source files prepared in $TEMP_SOURCE"
echo ""

# Build APK with p4a
echo "Building APK with p4a..."
echo "========================================================================"

cd "$TEMP_SOURCE"

p4a apk \
    --name "$APP_NAME" \
    --package "$PACKAGE_NAME" \
    --version "$VERSION" \
    --requirements "$REQUIREMENTS" \
    --permission "$PERMISSIONS" \
    --orientation "$ORIENTATION" \
    --android-api "$ANDROID_API" \
    --ndk-api "$ANDROID_MIN_API" \
    --ndk-version "$ANDROID_NDK" \
    --arch arm64-v8a \
    --arch armeabi-v7a \
    --bootstrap "$BOOTSTRAP" \
    --release \
    --local-recipes "p4a_recipes" \
    --hook "p4a_hook.py" \
    --private . \
    --storage-dir "$BUILD_DIR/p4a-storage"

cd ../..

# Copy APK to dist directory
echo ""
echo "========================================================================"
echo "Copying APK to dist directory..."
APK_SOURCE=$(find "$BUILD_DIR" -name "*.apk" | head -1)
if [ -n "$APK_SOURCE" ]; then
    cp "$APK_SOURCE" "$DIST_DIR/"
    echo "APK copied to: $DIST_DIR/$(basename $APK_SOURCE)"
else
    echo "Warning: APK not found in build directory"
fi

echo ""
echo "========================================================================"
echo "Build complete!"
echo "========================================================================"
echo "APK location: $DIST_DIR/"
ls -lh "$DIST_DIR"/*.apk 2>/dev/null || echo "No APK found"
