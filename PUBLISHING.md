# 🚀 Publishing PhishGuard to Extension Stores

You can publish the generated `phishguard-extension-v1.0.0.zip` file directly to browser extension stores.

## 📦 What files do you need?

We have already generated the package for you:
- **File:** `phishguard-extension-v1.0.0.zip` inside the root folder.
- **Contents:** manifest.json, background scripts, content scripts, popup UI, and icons.

---

## 🌐 1. Google Chrome Web Store (Chrome, Brave, Opera)

1. **Go to Developer Dashboard:**
   - Visit [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/dev/dashboard)
   - Sign in with your Google Account.
   - Note: There is a one-time $5 registration fee.

2. **Upload Package:**
   - Click **"New Item"**.
   - Upload the `phishguard-extension-v1.0.0.zip` file.

3. **Fill Listing Information:**
   - **Store Listing:** Description, screenshots (you can take screenshots of the popup).
   - **Privacy:** Detailed below.
   - **Pricing:** Free.

4. **Privacy Practices (Crucial):**
   - **Host Permissions:** Explain that you scan `http://*/*` and `https://*/*` to detect phishing content.
   - **Remote Code:** Confirm you do not use remote code (PhishGuard uses a local API backend, but for the specific store version, you might need to host the backend properly on a server like Heroku/AWS if you want public users to use it without running `run.sh` locally).
   - *Since this version connects to `localhost:8000`, it is intended for "Self-Hosted" or "Developer" distribution. If you want to publish for the public, you must deploy the Backend API to a public URL (e.g., `https://api.your-phishguard.com`) and update `background.js` and `popup.js`.*

---

## 🟦 2. Microsoft Edge Add-ons

1. **Go to Partner Center:**
   - Visit [Microsoft Partner Center](https://partner.microsoft.com/en-us/dashboard/microsoftedge/overview/)
   - Sign in with a Microsoft Account.

2. **Create New Extension:**
   - Click **"Create new extension"**.
   - Upload `phishguard-extension-v1.0.0.zip`.

3. **Details:**
   - Similar to Chrome, fill in description and upload screenshots.

---

## 🦊 3. Mozilla Firefox Add-ons

*Note: Chromium extensions (Manifest V3) need minor adjustments for Firefox.*

1. **Go to Developer Hub:**
   - Visit [Firefox Add-on Developer Hub](https://addons.mozilla.org/en-US/developers/)

2. **Submit a New Add-on:**
   - You might need to adjust `manifest.json` specifically for Firefox (e.g., using `background.scripts` instead of `service_worker` depending on their current V3 support status).

---

## ⚠️ Important Note on Backend

Currently, the extension points to `http://localhost:8000`.

**For Public Release:**
1. Deploy the contents of the `backend/` folder to a public server (AWS, Heroku, DigitalOcean, Render).
2. Update the `API_BASE_URL` in `browser-extension/popup.js` and `browser-extension/background.js` to your new public HTTPS URL.
3. Re-zip the folder before uploading to the store.
