// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Get current tab URL
async function getCurrentTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab;
}

// Scan URL using the API
async function scanUrl(url) {
    try {
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
        
        return await response.json();
    } catch (error) {
        console.error('Scan error:', error);
        return { 
            status: 'error', 
            score: 0, 
            details: 'Unable to connect to PhishGuard server. Make sure the backend is running on ' + API_BASE_URL 
        };
    }
}

// Display scan result
function displayResult(result, elementId) {
    const element = document.getElementById(elementId);
    
    if (result.status === 'error') {
        element.innerHTML = `
            <div class="result-error">
                <span class="result-icon">⚠️</span>
                <strong>Connection Error</strong>
                <div class="result-details">${result.details}</div>
            </div>
        `;
        element.className = 'scan-result';
        return;
    }
    
    let statusClass, icon, statusText;
    
    if (result.status === 'safe') {
        statusClass = 'result-safe';
        icon = '✅';
        statusText = 'Safe';
    } else if (result.status === 'phishing') {
        statusClass = 'result-phishing';
        icon = '🚨';
        statusText = 'Phishing Detected!';
    } else {
        statusClass = 'result-suspicious';
        icon = '⚠️';
        statusText = 'Suspicious';
    }
    
    element.innerHTML = `
        <span class="result-icon">${icon}</span>
        <strong>${statusText}</strong> (Score: ${result.score}/100)
        <div class="result-details">${result.details || 'No additional details'}</div>
    `;
    element.className = `scan-result ${statusClass}`;
    
    // Update stats
    updateStats(result.status);
}

// Update statistics
function updateStats(status) {
    chrome.storage.local.get(['pagesScanned', 'threatsBlocked'], (data) => {
        const pagesScanned = (data.pagesScanned || 0) + 1;
        const threatsBlocked = data.threatsBlocked || 0;
        const newThreats = status === 'phishing' ? threatsBlocked + 1 : threatsBlocked;
        
        chrome.storage.local.set({ 
            pagesScanned, 
            threatsBlocked: newThreats 
        });
        
        document.getElementById('pagesScanned').textContent = pagesScanned;
        document.getElementById('threatsBlocked').textContent = newThreats;
    });
}

// Load and display statistics
function loadStats() {
    chrome.storage.local.get(['pagesScanned', 'threatsBlocked'], (data) => {
        document.getElementById('pagesScanned').textContent = data.pagesScanned || 0;
        document.getElementById('threatsBlocked').textContent = data.threatsBlocked || 0;
    });
}

// Initialize popup
document.addEventListener('DOMContentLoaded', async () => {
    loadStats();
    
    // Get and display current tab URL
    const tab = await getCurrentTab();
    const urlDisplay = document.getElementById('currentUrl');
    
    if (tab && tab.url) {
        urlDisplay.textContent = tab.url;
        
        // Auto-scan if enabled
        chrome.storage.local.get(['autoScan'], async (data) => {
            if (data.autoScan !== false) {
                const result = await scanUrl(tab.url);
                displayResult(result, 'scanResult');
            } else {
                document.getElementById('scanResult').innerHTML = '<div class="loading">Click "Scan This Page" to analyze</div>';
            }
        });
    } else {
        urlDisplay.textContent = 'Unable to get current page URL';
    }
    
    // Scan current page button
    document.getElementById('scanCurrentPage').addEventListener('click', async () => {
        const tab = await getCurrentTab();
        if (tab && tab.url) {
            document.getElementById('scanResult').innerHTML = '<div class="loading">Analyzing...</div>';
            const result = await scanUrl(tab.url);
            displayResult(result, 'scanResult');
        }
    });
    
    // Manual scan button
    document.getElementById('scanManual').addEventListener('click', async () => {
        const url = document.getElementById('manualUrl').value.trim();
        if (!url) {
            alert('Please enter a URL to scan');
            return;
        }
        
        document.getElementById('manualResult').innerHTML = '<div class="loading">Analyzing...</div>';
        const result = await scanUrl(url);
        displayResult(result, 'manualResult');
    });
    
    // Report phishing button
    document.getElementById('reportPhishing').addEventListener('click', async () => {
        const tab = await getCurrentTab();
        if (tab && tab.url) {
            alert(`Reporting: ${tab.url}\n\nThis feature will be implemented to send reports to the PhishGuard database.`);
        }
    });
    
    // Settings
    document.getElementById('autoScan').addEventListener('change', (e) => {
        chrome.storage.local.set({ autoScan: e.target.checked });
    });
    
    document.getElementById('showNotifications').addEventListener('change', (e) => {
        chrome.storage.local.set({ showNotifications: e.target.checked });
    });
    
    // Load settings
    chrome.storage.local.get(['autoScan', 'showNotifications'], (data) => {
        document.getElementById('autoScan').checked = data.autoScan !== false;
        document.getElementById('showNotifications').checked = data.showNotifications !== false;
    });
});
