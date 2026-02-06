# Browser Extension Installation Guide

## Creating Extension Icons

Since we need icon files, you can either:

### Option 1: Use online icon generator
1. Go to https://www.favicon-generator.org/ or similar
2. Upload a shield emoji or create a custom shield logo
3. Generate sizes: 16x16, 32x32, 48x48, 128x128
4. Save them in the `icons/` folder

### Option 2: Use emoji as temporary icons
Create simple PNG files with the 🛡️ emoji in different sizes and save them as:
- icon16.png
- icon32.png
- icon48.png
- icon128.png

## Installation Steps

### Chrome / Edge / Brave

1. **Open Extensions Page**
   - Chrome: Navigate to `chrome://extensions/`
   - Edge: Navigate to `edge://extensions/`
   - Brave: Navigate to `brave://extensions/`

2. **Enable Developer Mode**
   - Toggle the "Developer mode" switch in the top right corner

3. **Load Extension**
   - Click "Load unpacked"
   - Select the `browser-extension` folder
   - The extension will appear in your toolbar

4. **Pin the Extension**
   - Click the puzzle icon in the toolbar
   - Find "PhishGuard - AI Phishing Detector"
   - Click the pin icon to keep it visible

### Firefox (requires manifest v2 conversion)

For Firefox, you'll need to modify the manifest.json slightly. Let me know if you need Firefox support.

## Usage

1. **Make sure the backend is running** at http://localhost:8000
2. Click the PhishGuard icon in your toolbar
3. The extension will automatically scan the current page
4. View threat scores and details in the popup

## Features

- ✅ Auto-scan pages as you browse
- ✅ Manual URL scanning
- ✅ Right-click context menu to scan links
- ✅ Warning banners for high-risk sites
- ✅ Form submission protection
- ✅ Statistics tracking
- ✅ Desktop notifications for threats
