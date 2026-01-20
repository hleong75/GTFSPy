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

# Android SDK and NDK paths (use environment variables if available)
ANDROID_SDK="${ANDROID_SDK_ROOT:-${ANDROID_HOME}}"
ANDROID_NDK_DIR="${ANDROID_NDK_HOME:-${ANDROID_NDK_ROOT}}"

# Build directory
BUILD_DIR="./.p4a_build"
DIST_DIR="./dist"

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
if [ -n "$ANDROID_SDK" ]; then
    echo "  Android SDK: $ANDROID_SDK"
fi
if [ -n "$ANDROID_NDK_DIR" ]; then
    echo "  Android NDK: $ANDROID_NDK_DIR"
fi
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

# Copy p4a configuration files to temp source
cp -v p4a_hook.py "$TEMP_SOURCE/"
cp -rv p4a_recipes "$TEMP_SOURCE/"

# Build APK with p4a
echo "Building APK with p4a..."
echo "========================================================================"

cd "$TEMP_SOURCE"

# Build p4a command with SDK/NDK paths if available
P4A_CMD="p4a apk \
    --name \"$APP_NAME\" \
    --package \"$PACKAGE_NAME\" \
    --version \"$VERSION\" \
    --requirements \"$REQUIREMENTS\" \
    --permission \"$PERMISSIONS\" \
    --orientation \"$ORIENTATION\" \
    --android-api \"$ANDROID_API\" \
    --ndk-api \"$ANDROID_MIN_API\" \
    --ndk-version \"$ANDROID_NDK\" \
    --arch arm64-v8a \
    --arch armeabi-v7a \
    --bootstrap \"$BOOTSTRAP\" \
    --release \
    --local-recipes \"p4a_recipes\" \
    --hook \"p4a_hook.py\" \
    --private . \
    --storage-dir \"$BUILD_DIR/p4a-storage\""

# Add SDK directory if available
if [ -n "$ANDROID_SDK" ]; then
    P4A_CMD="$P4A_CMD --sdk-dir \"$ANDROID_SDK\""
fi

# Add NDK directory if available
if [ -n "$ANDROID_NDK_DIR" ]; then
    P4A_CMD="$P4A_CMD --ndk-dir \"$ANDROID_NDK_DIR\""
fi

# Execute the p4a command
eval $P4A_CMD

BUILD_EXIT_CODE=$?
cd ../..

# Copy APK to dist directory
echo ""
echo "========================================================================"
if [ $BUILD_EXIT_CODE -ne 0 ]; then
    echo "ERROR: Build failed with exit code $BUILD_EXIT_CODE"
    exit $BUILD_EXIT_CODE
fi

echo "Copying APK to dist directory..."

# Look for APK in known p4a output locations
APK_SOURCE=""
for location in \
    "$BUILD_DIR/source" \
    "$BUILD_DIR/p4a-storage" \
    "$TEMP_SOURCE"; do
    APK_FOUND=$(find "$location" -name "*.apk" 2>/dev/null | head -1)
    if [ -n "$APK_FOUND" ]; then
        APK_SOURCE="$APK_FOUND"
        break
    fi
done

if [ -n "$APK_SOURCE" ] && [ -f "$APK_SOURCE" ]; then
    cp "$APK_SOURCE" "$DIST_DIR/"
    echo "✓ APK copied to: $DIST_DIR/$(basename "$APK_SOURCE")"
else
    echo "ERROR: APK not found in build directories"
    echo "Searched in:"
    echo "  - $BUILD_DIR/source"
    echo "  - $BUILD_DIR/p4a-storage"
    echo "  - $TEMP_SOURCE"
    exit 1
fi

echo ""
echo "========================================================================"
echo "Build complete!"
echo "========================================================================"
# Check if any APK files exist in dist directory
if ls "$DIST_DIR"/*.apk 1> /dev/null 2>&1; then
    echo "✓ APK successfully created:"
    ls -lh "$DIST_DIR"/*.apk
else
    echo "ERROR: Build completed but no APK was created"
    exit 1
fi
