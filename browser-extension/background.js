// Background Service Worker for PhishGuard Extension

const API_BASE_URL = 'http://localhost:8000';

// Install event
chrome.runtime.onInstalled.addListener(() => {
    console.log('PhishGuard extension installed');
    
    // Initialize storage
    chrome.storage.local.set({
        pagesScanned: 0,
        threatsBlocked: 0,
        autoScan: true,
        showNotifications: true
    });
    
    // Set badge
    chrome.action.setBadgeText({ text: 'ON' });
    chrome.action.setBadgeBackgroundColor({ color: '#667eea' });
});

// Listen for tab updates (new page loads)
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        // Get settings
        const { autoScan, showNotifications } = await chrome.storage.local.get(['autoScan', 'showNotifications']);
        
        if (autoScan) {
            // Scan the URL
            const result = await scanUrl(tab.url);
            
            // Show notification if threat detected
            if (result.status === 'phishing' && showNotifications) {
                chrome.notifications.create({
                    type: 'basic',
                    iconUrl: 'icons/icon128.png',
                    title: '🚨 PhishGuard Alert',
                    message: `Phishing detected!\nThreat Score: ${result.score}/100\n${result.details}`,
                    priority: 2
                });
                
                // Update badge to warning
                chrome.action.setBadgeText({ text: '⚠️', tabId });
                chrome.action.setBadgeBackgroundColor({ color: '#ef4444', tabId });
            } else {
                // Update badge to safe
                chrome.action.setBadgeText({ text: '✓', tabId });
                chrome.action.setBadgeBackgroundColor({ color: '#22c55e', tabId });
            }
        }
    }
});

// Scan URL function
async function scanUrl(url) {
    try {
        // Skip certain URLs
        if (url.startsWith('chrome://') || 
            url.startsWith('chrome-extension://') || 
            url.startsWith('about:') ||
            url.startsWith('edge://')) {
            return { status: 'safe', score: 0, details: 'Browser internal page' };
        }
        
        const response = await fetch(`${API_BASE_URL}/scan/url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });
        
        if (!response.ok) {
            throw new Error('Scan failed');
        }
        
        const result = await response.json();
        
        // Update statistics
        updateStats(result.status);
        
        return result;
    } catch (error) {
        console.error('Scan error:', error);
        return { status: 'error', score: 0, details: 'Unable to scan' };
    }
}

// Update statistics
async function updateStats(status) {
    const data = await chrome.storage.local.get(['pagesScanned', 'threatsBlocked']);
    const pagesScanned = (data.pagesScanned || 0) + 1;
    const threatsBlocked = status === 'phishing' ? (data.threatsBlocked || 0) + 1 : (data.threatsBlocked || 0);
    
    chrome.storage.local.set({ pagesScanned, threatsBlocked });
}

// Listen for messages from content script or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'scanUrl') {
        scanUrl(request.url).then(result => {
            sendResponse(result);
        });
        return true; // Keep message channel open for async response
    }
    
    if (request.action === 'getStats') {
        chrome.storage.local.get(['pagesScanned', 'threatsBlocked'], (data) => {
            sendResponse(data);
        });
        return true;
    }
});

// Context menu for right-click scanning
chrome.contextMenus.create({
    id: 'scanLink',
    title: 'Scan with PhishGuard',
    contexts: ['link']
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (info.menuItemId === 'scanLink' && info.linkUrl) {
        const result = await scanUrl(info.linkUrl);
        
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon128.png',
            title: result.status === 'phishing' ? '🚨 Phishing Link!' : '✅ Safe Link',
            message: `URL: ${info.linkUrl}\nScore: ${result.score}/100\n${result.details}`,
            priority: result.status === 'phishing' ? 2 : 1
        });
    }
});

// Download Protection: Scan downloads before they complete
if (chrome.downloads) {
    chrome.downloads.onCreated.addListener(async (downloadItem) => {
        // We can check the URL of the download
        const url_result = await scanUrl(downloadItem.url);
        
        if (url_result.status === 'phishing' || url_result.score >= 70) {
            chrome.downloads.cancel(downloadItem.id, () => {
                chrome.notifications.create({
                    type: 'basic',
                    iconUrl: 'icons/icon128.png',
                    title: '🚨 Download Blocked!',
                    message: `PhishGuard blocked a suspicious download from: ${downloadItem.url}\nReason: ${url_result.details}`,
                    priority: 2
                });
            });
        }
    });
}

// Handle scanning image content from background (to avoid CORS in content script)
async function scanRemoteImage(imageUrl) {
    try {
        // Fetch image as blob
        const response = await fetch(imageUrl);
        const blob = await response.blob();
        
        // Prepare form data
        const formData = new FormData();
        formData.append('file', blob, 'image_scan.png');
        
        // Send to backend
        const scanRes = await fetch(`${API_BASE_URL}/scan/file`, {
            method: 'POST',
            body: formData
        });
        
        if (!scanRes.ok) throw new Error('Backend scan failed');
        return await scanRes.json();
        
    } catch (error) {
        console.error('Image scan error:', error);
        return { status: 'error' };
    }
}

// Add message handler for content script requesting image scan
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'scanUrl') {
        scanUrl(request.url).then(result => sendResponse(result));
        return true; 
    }
    
    if (request.action === 'scanImage') {
        scanRemoteImage(request.imageUrl).then(result => sendResponse(result));
        return true;
    }
    
    if (request.action === 'getStats') {
        chrome.storage.local.get(['pagesScanned', 'threatsBlocked'], (data) => {
            sendResponse(data);
        });
        return true;
    }
});

