const API_URL = "http://localhost:8000";

// Tab Switching
function switchTab(tabId) {
    // Buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        // If no event object (programmatic switch), we manually find the target button
        // But for simplicity, we just rely on the click handler if called via UI
    });

    // Set active button
    const targetBtn = document.querySelector(`button[onclick="switchTab('${tabId}')"]`);
    if (targetBtn) targetBtn.classList.add('active');

    // Content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabId}-tab`).classList.add('active');

    // Hide results when switching
    document.getElementById('resultArea').classList.add('hidden');

    if (tabId === 'admin') {
        loadAdminIPs();
    }
}

// File Input
function handleFileSelect(input) {
    if (input.files.length > 0) {
        document.getElementById('fileName').innerText = input.files[0].name;
    }
}

// UI Helpers
function showLoading() {
    const res = document.getElementById('resultArea');
    res.classList.remove('hidden');
    document.getElementById('resultBadge').innerText = "Scanning...";
    document.getElementById('resultBadge').className = "score-badge";
    document.getElementById('scoreValue').innerText = "--";
    document.getElementById('resultDetails').innerText = "Analyzing data...";
}

function showResult(data) {
    const isSafe = data.status === 'safe' || data.status === 'allowed';

    // Badge
    const badge = document.getElementById('resultBadge');
    badge.innerText = data.status.toUpperCase();
    badge.className = isSafe ? "score-badge" : "score-badge danger";

    if (!isSafe) {
        badge.style.background = "rgba(239, 68, 68, 0.2)";
        badge.style.color = "#ef4444";
        document.querySelector('.result-card').style.borderLeftColor = "#ef4444";
        document.querySelector('.score-circle').style.borderColor = "#ef4444";
    } else {
        badge.style.background = "rgba(16, 185, 129, 0.2)";
        badge.style.color = "#10b981";
        document.querySelector('.result-card').style.borderLeftColor = "#10b981";
        document.querySelector('.score-circle').style.borderColor = "#10b981";
    }

    // Score
    document.getElementById('scoreValue').innerText = data.score || 0;

    // Details
    document.getElementById('resultDetails').innerText = data.details || "No threats detected.";
}

// API Calls
async function scanUrl() {
    const url = document.getElementById('urlInput').value;
    if (!url) return; // Silent return for auto-scan

    showLoading();
    try {
        const res = await fetch(`${API_URL}/scan/url`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });
        const data = await res.json();
        showResult(data);
    } catch (e) {
        console.error("Error scanning URL:", e);
        // Don't alert on auto-scan errors to avoid spamming user
    }
}

async function scanEmail() {
    const sender = document.getElementById('emailSender').value || "";
    const subject = document.getElementById('emailSubject').value || "";
    const body = document.getElementById('emailBody').value || "";

    // For auto-scan, we might run with partial data, but backend handles it.
    // However, if everything is empty, don't scan.
    if (!sender && !body) return;

    showLoading();
    try {
        const res = await fetch(`${API_URL}/scan/email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender, subject, body })
        });
        const data = await res.json();
        showResult(data);
    } catch (e) {
        console.error("Error scanning email:", e);
    }
}

async function scanFile() {
    const input = document.getElementById('fileInput');
    if (input.files.length === 0) return alert("Please select a file");

    const formData = new FormData();
    formData.append('file', input.files[0]);

    showLoading();
    try {
        const res = await fetch(`${API_URL}/scan/file`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        showResult(data);
    } catch (e) {
        alert("Error scanning file");
    }
}

async function loadAdminIPs() {
    const list = document.getElementById('ipList');
    list.innerHTML = '<div class="loading">Loading...</div>';

    try {
        const res = await fetch(`${API_URL}/admin/ips`);
        const data = await res.json();

        list.innerHTML = '';
        if (Object.keys(data).length === 0) {
            list.innerHTML = '<div class="ip-item">No IPs recorded yet.</div>';
            return;
        }

        for (const [ip, info] of Object.entries(data)) {
            const isBlocked = info.blocked_until > Date.now() / 1000;
            const item = document.createElement('div');
            item.className = 'ip-item';
            item.innerHTML = `
                <div>
                    <strong>${ip}</strong> 
                    <span style="color: ${isBlocked ? '#ef4444' : '#10b981'}">
                        ${isBlocked ? '[BLOCKED]' : '[Active]'}
                    </span>
                    <br>
                    <small>Attempts: ${info.attempts}</small>
                </div>
                ${isBlocked ? `<button class="unblock-btn" onclick="unblockIp('${ip}')">Unblock</button>` : ''}
            `;
            list.appendChild(item);
        }
    } catch (e) {
        list.innerHTML = 'Error loading IPs';
    }
}

// Debounce Utility to prevent too many API calls
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

// Auto-scan handlers (Debounced)
const autoScanUrl = debounce(() => {
    const url = document.getElementById('urlInput').value.trim();
    if (url) {
        scanUrl();
    } else {
        document.getElementById('resultArea').classList.add('hidden');
    }
}, 500);

const autoScanEmail = debounce(() => {
    const body = document.getElementById('emailBody').value.trim();
    const sender = document.getElementById('emailSender').value.trim();
    if (body || sender) {
        scanEmail();
    } else {
        document.getElementById('resultArea').classList.add('hidden');
    }
}, 800); // Slightly longer delay for email to allow typing

// Initialize Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // URL Input
    const urlInput = document.getElementById('urlInput');
    if (urlInput) {
        urlInput.addEventListener('input', autoScanUrl);
        urlInput.addEventListener('paste', autoScanUrl);
    }

    // Email Inputs
    const emailBody = document.getElementById('emailBody');
    const emailSender = document.getElementById('emailSender');
    const emailSubject = document.getElementById('emailSubject');

    if (emailBody) emailBody.addEventListener('input', autoScanEmail);
    if (emailSender) emailSender.addEventListener('input', autoScanEmail);
    if (emailSubject) emailSubject.addEventListener('input', autoScanEmail);

    // Initial Load
    loadAdminIPs();
    checkQueryParams();

    // Global Paste Listener
    document.addEventListener('paste', handleGlobalPaste);

    // Global Drop Listener
    document.addEventListener('dragover', (e) => e.preventDefault());
    document.addEventListener('drop', handleGlobalDrop);
});

// ZERO-INTERACTION HANDLERS

function checkQueryParams() {
    const params = new URLSearchParams(window.location.search);
    const url = params.get('url') || params.get('q');

    if (url) {
        console.log("Auto-scanning URL from query param:", url);
        switchTab('url');
        document.getElementById('urlInput').value = url;
        scanUrl();
        // Clear param to avoid re-scan on refresh
        window.history.replaceState({}, document.title, "/");
    }
}

function handleGlobalPaste(e) {
    // If user is already focused on an input, let default behavior happen
    if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

    e.preventDefault();
    const items = (e.clipboardData || e.originalEvent.clipboardData).items;

    for (const item of items) {
        if (item.kind === 'file') {
            const file = item.getAsFile();
            switchTab('file');
            // Manually trigger file input handling
            const container = new DataTransfer();
            container.items.add(file);
            document.getElementById('fileInput').files = container.files;
            document.getElementById('fileName').innerText = file.name;
            scanFile();
            return;
        } else if (item.kind === 'string' && item.type === 'text/plain') {
            item.getAsString((text) => {
                analyzePastedText(text);
            });
        }
    }
}

function handleGlobalDrop(e) {
    e.preventDefault();
    const files = e.dataTransfer.files;

    if (files.length > 0) {
        switchTab('file');
        const container = new DataTransfer();
        container.items.add(files[0]);
        document.getElementById('fileInput').files = container.files;
        document.getElementById('fileName').innerText = files[0].name;
        scanFile();
    }
}

function analyzePastedText(text) {
    text = text.trim();

    // Simple Heuristic to detect Type
    const isUrl = /^(http|www\.|[a-zA-Z0-9-]+\.[a-zA-Z]{2,})/.test(text) && !text.includes('\n') && text.length < 256;
    const isEmail = text.includes('Subject:') || text.includes('From:') || (text.includes('@') && text.length > 20 && text.includes(' '));

    if (isUrl) {
        switchTab('url');
        document.getElementById('urlInput').value = text;
        scanUrl();
        showToast("Auto-detected URL: Scanning...");
    } else if (isEmail) {
        switchTab('email');
        document.getElementById('emailBody').value = text;
        scanEmail();
        showToast("Auto-detected Email Content: Scanning...");
    } else {
        // Default to URL if short, or Email if long
        if (text.length < 150) {
            switchTab('url');
            document.getElementById('urlInput').value = text;
            scanUrl();
        } else {
            switchTab('email');
            document.getElementById('emailBody').value = text;
            scanEmail();
        }
    }
}

function showToast(msg) {
    // Re-purpose the system status or create a temporary toast
    const status = document.getElementById('systemStatus');
    const originalText = status.innerHTML;

    status.innerHTML = `<span class="dot" style="background:cyan; box-shadow:0 0 10px cyan"></span> ${msg}`;
    setTimeout(() => {
        status.innerHTML = originalText;
    }, 3000);
}

async function unblockIp(ip) {
    if (!confirm(`Unblock IP ${ip}?`)) return;
    await fetch(`${API_URL}/admin/unblock/${ip}`, { method: 'POST' });
    loadAdminIPs();
}
