# 🧩 PhishGuard Browser Extension - Quick Start

## What You Get

The PhishGuard browser extension provides **real-time phishing protection** while you browse:

### ✨ Key Features

1. **🔍 Auto-Scan Pages**
   - Automatically analyzes every website you visit
   - Instant threat detection in the background

2. **🚨 Visual Warnings**
   - Red warning banner for high-risk sites
   - Prevents accidental form submissions on phishing sites

3. **📊 Statistics Dashboard**
   - Track pages scanned
   - Count threats blocked
   - View your protection history

4. **🖱️ Right-Click Scanning**
   - Right-click any link
   - Select "Scan with PhishGuard"
   - Get instant threat analysis

5. **🔔 Desktop Notifications**
   - Real-time alerts for phishing threats
   - Configurable notification settings

6. **🛡️ Form Protection**
   - Warns before submitting forms on suspicious sites
   - Protects passwords and payment info

## 🚀 Quick Setup (5 Minutes)

### Step 1: Start the Backend
```bash
cd backend
python main.py
```
**Wait for:** "Uvicorn running on http://0.0.0.0:8000"

### Step 2: Load the Extension

#### Chrome:
1. Open `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the `browser-extension` folder
5. Done! 🎉

#### Edge:
1. Open `edge://extensions/`
2. Enable "Developer mode" (left sidebar)
3. Click "Load unpacked"
4. Select the `browser-extension` folder
5. Done! 🎉

### Step 3: Pin the Extension
- Click the puzzle icon 🧩 in your toolbar
- Find "PhishGuard - AI Phishing Detector"
- Click the pin 📌 to keep it visible

## 💡 How to Use

### Automatic Protection
Just browse normally! The extension automatically:
- Scans every new page
- Shows warnings for phishing sites
- Blocks forms on dangerous sites

### Manual Scanning
1. **Current Page:** Click the extension icon → "Scan This Page"
2. **Any URL:** Enter URL in popup → Click "Scan"
3. **Links:** Right-click any link → "Scan with PhishGuard"

### View Results
Open the extension popup to see:
- Current page threat score
- Detailed analysis
- Protection statistics

## ⚙️ Settings

Click the extension icon and toggle:
- **Auto-scan new pages** - Automatic protection (recommended ✅)
- **Show threat notifications** - Desktop alerts for threats

## 🎯 Example Use Cases

### Scenario 1: Email Link Protection
1. Receive suspicious email with link
2. **Don't click immediately!**
3. Copy the URL
4. Open PhishGuard extension
5. Paste in "Manual URL Scan"
6. Check the threat score before visiting

### Scenario 2: Social Media Links
1. See a link on Twitter/Facebook
2. Right-click the link
3. Select "Scan with PhishGuard"
4. Get instant threat analysis
5. Decide whether to click

### Scenario 3: Login Form Warning
1. Browse to a site
2. Start filling in login form
3. If phishing detected: **Warning appears!**
4. Extension blocks submission
5. Your credentials are safe

## 🔧 Troubleshooting

### "Unable to connect to server"
- ✅ Make sure backend is running: `python main.py`
- ✅ Check URL is `http://localhost:8000`
- ✅ Try visiting http://localhost:8000/docs

### Extension not working
- ✅ Reload the extension page
- ✅ Check "Developer mode" is enabled
- ✅ Look for errors in extension console

### No scan results
- ✅ Enable "Auto-scan new pages" in settings
- ✅ Click "Scan This Page" manually
- ✅ Make sure URL is not chrome:// or internal page

## 🎨 Understanding Threat Scores

| Score | Badge | Status | Action |
|-------|-------|--------|--------|
| 0-39 | ✅ | Safe | Proceed normally |
| 40-69 | ⚠️ | Suspicious | Be cautious |
| 70-100 | 🚨 | Phishing | **Avoid this site!** |

## 🔐 Privacy & Security

- ✅ All scanning happens via your **local backend**
- ✅ No data sent to third parties
- ✅ URLs are only sent to your own API
- ✅ Statistics stored locally in browser

## 📱 Browser Support

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome | ✅ Supported | Manifest V3 |
| Edge | ✅ Supported | Manifest V3 |
| Brave | ✅ Supported | Chrome-based |
| Firefox | ⏳ Coming Soon | Needs manifest conversion |
| Safari | ⏳ Future | Different extension format |

## 🚀 Next Steps

1. ✅ Install and test the extension
2. 🔍 Try scanning some known phishing sites
3. ⚙️ Customize your settings
4. 📊 Watch your protection stats grow!

---

**Need Help?** Check the main [README.md](../README.md) or open an issue on GitHub.

**Stay Safe!** 🛡️
