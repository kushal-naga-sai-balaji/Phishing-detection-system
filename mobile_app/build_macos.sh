#!/bin/bash

# Build script for macOS using PyInstaller

# 1. Install PyInstaller if not present
pip install pyinstaller

# 2. Clean previous builds
rm -rf build dist *.spec

# 3. Create the standalone application
# --name: Name of the app
# --onefile: Bundle everything into one executable (optional, often better without for macOS .app bundles but simpler for CLI)
# --windowed: No terminal window
# --icon: You can add an icon later with --icon=icon.icns
# --add-data: Kivy needs some specific hooks usually, but newer PyInstaller handles Kivy reasonably well.
#             Sometimes need to collect kv files if they are separate. Here we only have main.py python code.

echo "📦 Packaging PhishGuard for macOS..."

pyinstaller --name "PhishGuard" \
            --windowed \
            --noconfirm \
            --clean \
            main.py

echo "✅ Build complete!"
echo "🚀 You can find your app in the 'dist' folder:"
echo "   dist/PhishGuard.app"
