// Content Script - Runs on all web pages

// Inject warning banner if page is flagged as phishing
function showPhishingWarning(score, details) {
    // Check if warning already exists
    if (document.getElementById('phishguard-warning')) {
        return;
    }
    
    const warning = document.createElement('div');
    warning.id = 'phishguard-warning';
    warning.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 15px 20px;
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        animation: slideDown 0.3s ease-out;
    `;
    
    warning.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 24px;">🚨</span>
            <div>
                <div style="font-weight: 600; font-size: 16px; margin-bottom: 4px;">
                    PhishGuard Alert: Potential Phishing Site Detected!
                </div>
                <div style="font-size: 13px; opacity: 0.9;">
                    Threat Score: ${score}/100 - ${details}
                </div>
            </div>
        </div>
        <button id="phishguard-close" style="
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            transition: background 0.2s;
        ">
            Dismiss
        </button>
    `;
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideDown {
            from {
                transform: translateY(-100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.insertBefore(warning, document.body.firstChild);
    
    // Add close button functionality
    document.getElementById('phishguard-close').addEventListener('click', () => {
        warning.style.animation = 'slideDown 0.3s ease-out reverse';
        setTimeout(() => warning.remove(), 300);
    });
    
    // Adjust page content to not be hidden behind warning
    const originalMargin = document.body.style.marginTop;
    document.body.style.marginTop = '80px';
    document.body.style.transition = 'margin-top 0.3s ease-out';
}

// Monitor for suspicious forms
function monitorForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Check if form already monitored
        if (form.dataset.phishguardMonitored) {
            return;
        }
        
        form.dataset.phishguardMonitored = 'true';
        
        form.addEventListener('submit', (e) => {
            // Check for password or credit card fields
            const hasPasswordField = form.querySelector('input[type="password"]');
            const hasCreditCardField = form.querySelector('input[name*="card"], input[name*="credit"]');
            
            if (hasPasswordField || hasCreditCardField) {
                const currentUrl = window.location.href;
                
                // Send URL to background for scanning
                chrome.runtime.sendMessage({
                    action: 'scanUrl',
                    url: currentUrl
                }, (result) => {
                    if (result && result.status === 'phishing') {
                        e.preventDefault();
                        
                        const confirmed = confirm(
                            `⚠️ PhishGuard Warning!\n\n` +
                            `This site has been flagged as potentially dangerous (Threat Score: ${result.score}/100).\n\n` +
                            `${result.details}\n\n` +
                            `Are you sure you want to submit this form?`
                        );
                        
                        if (confirmed) {
                            form.submit();
                        }
                    }
                });
            }
        });
    });
}

// Scan links on hover
function setupLinkScanning() {
    document.addEventListener('mouseover', (e) => {
        if (e.target.tagName === 'A' && e.target.href) {
            // Check for suspiciously long URLs or IPs immediately
            const url = e.target.href;
            if (url.length > 100 || /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/.test(url)) {
                 chrome.runtime.sendMessage({ action: 'scanUrl', url: url }, (result) => {
                     if (result && result.status === 'phishing') {
                         e.target.style.border = '2px solid red';
                         e.target.style.backgroundColor = 'rgba(255,0,0,0.1)';
                         e.target.title = `⚠️ PHISHING: ${result.details}`;
                     }
                 });
            }
        }
    });
}

// Auto-scan images for QR codes or malware
function autoScanImages() {
    // Only scan images that are large enough to be content (ignore icons)
    const images = Array.from(document.querySelectorAll('img')).filter(img => {
        return img.width > 100 && img.height > 100 && img.src.startsWith('http');
    });

    // Limit to first 5 large images to prevent server overload
    images.slice(0, 5).forEach(img => {
        if (img.dataset.pgScanned) return;
        img.dataset.pgScanned = 'true';
        
        chrome.runtime.sendMessage({ action: 'scanImage', imageUrl: img.src }, (result) => {
            if (result && (result.status === 'malicious' || result.status === 'phishing')) {
                // Highlight malicious image
                img.style.border = '5px solid red';
                img.style.filter = 'blur(5px)'; // Obfuscate
                
                // Add overlay warning
                const warning = document.createElement('div');
                warning.style.cssText = `
                    position: absolute;
                    background: red;
                    color: white;
                    padding: 4px;
                    font-size: 12px;
                    z-index: 1000;
                    pointer-events: none;
                `;
                warning.textContent = "⚠️ THREAT DETECTED";
                
                // Position warning relative to parent if possible, or just skip sophisticated positioning for now
                img.parentNode.insertBefore(warning, img);
            }
        });
    });
}

// Initialize content script
(function init() {
    // Check if page should be scanned automatically
    chrome.storage.local.get(['autoScan'], (data) => {
        if (data.autoScan !== false) {
            const currentUrl = window.location.href;
            
            // Request scan from background script
            chrome.runtime.sendMessage({
                action: 'scanUrl',
                url: currentUrl
            }, (result) => {
                if (result && result.status === 'phishing' && result.score >= 70) {
                    showPhishingWarning(result.score, result.details);
                }
            });
            
            // Trigger auto-scan for page content
            setTimeout(autoScanImages, 2000); // Wait for page load
        }
    });
    
    // Monitor forms
    monitorForms();
    
    // Re-monitor forms if page content changes dynamically
    const observer = new MutationObserver(() => {
        monitorForms();
        // Debounce image scanning
        // autoScanImages(); // Uncomment if you want aggressive scanning on scroll/dynamic load
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Setup link scanning
    setupLinkScanning();
})();
