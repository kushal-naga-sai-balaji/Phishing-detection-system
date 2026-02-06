import re
import hashlib
import cv2
import numpy as np
import services.ml_engine as ml_engine

SUSPICIOUS_KEYWORDS = ["login", "verify", "update", "account", "secure", "banking", "urgent", "winner", "prize"]

# Mock "VirusTotal" database of known bad file hashes
KNOWN_BAD_HASHES = {
    "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*": "EICAR Test File",
    # Add more hashes of known malware here
}

def calculate_heuristic_score(text: str) -> float:
    score = 0
    text_lower = text.lower()
    
    for word in SUSPICIOUS_KEYWORDS:
        if word in text_lower:
            score += 10
            
    return min(score, 50) # Cap heuristic score contribution

def detect_url(url: str) -> dict:
    score = 0
    details = []
    
    # 1. Heuristics
    if len(url) > 75:
        score += 10
        details.append("URL is suspiciously long")
        
    if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url):
        score += 30
        details.append("URL contains raw IP address")
        
    heuristic_score = calculate_heuristic_score(url)
    if heuristic_score > 0:
        score += heuristic_score
        details.append("URL contains suspicious keywords")

    # 2. ML Prediction
    ml_result = ml_engine.predict_text(url)
    if ml_result["label"] == "phishing":
        confidence = ml_result["confidence"]
        ml_score = confidence * 60 # Max 60 points from ML
        score += ml_score
        details.append(f"AI detected phishing patterns ({int(confidence*100)}% confidence)")
        
    status = "phishing" if score >= 50 else "safe"
    return {"status": status, "score": int(score), "details": "; ".join(details)}

def detect_email(subject: str, body: str, sender: str) -> dict:
    score = 0
    details = []
    
    # 1. Heuristics
    if "no-reply" not in sender and calculate_heuristic_score(sender) > 0:
         score += 10
         details.append("Suspicious sender address")

    # 2. ML Prediction (on combined text)
    full_text = f"{subject} {body} {sender}"
    ml_result = ml_engine.predict_text(full_text)
    
    if ml_result["label"] == "phishing":
        confidence = ml_result["confidence"]
        score += confidence * 80 # Email content is strong signal
        details.append(f"AI detected phishing content ({int(confidence*100)}% confidence)")
        
    status = "phishing" if score >= 40 else "safe"
    return {"status": status, "score": int(score), "details": "; ".join(details)}

def detect_file(filename: str, content: bytes) -> dict:
    score = 0
    details = []
    
    # 1. Extension Check
    if filename.endswith(('.exe', '.bat', '.sh', '.vbs', '.scr')):
        score += 30
        details.append("High risk file extension")
        
    # 2. Hash Check (Signature Matching)
    file_hash = hashlib.sha256(content).hexdigest()
    
    # Check if hash is in known bad hashes
    if file_hash in KNOWN_BAD_HASHES:
         score = 100
         details.append(f"Known Malware Detected (Hash Match): {KNOWN_BAD_HASHES[file_hash]}")
    
    # For EICAR specifically, let's check the content directly as it's a standard string
    try:
        content_str = content.decode('utf-8', errors='ignore').strip()
        if content_str in KNOWN_BAD_HASHES:
             score = 100
             details.append(f"Known Malware Detected (content match): {KNOWN_BAD_HASHES[content_str]}")
    except:
        pass

    # 3. QR Code Detection (if image)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(content, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is not None:
                detector = cv2.QRCodeDetector()
                data, bbox, _ = detector.detectAndDecode(img)
                
                if data:
                    details.append(f"QR Code detected containing: {data}")
                    
                    # Recursively scan the URL found in QR code
                    # If it looks like a URL, scan it
                    if data.startswith("http") or "www." in data:
                        url_result = detect_url(data)
                        score += url_result["score"]
                        details.append(f"QR Link Analysis: {url_result['details']}")
                        # If the link is phishing, guarantee phishing status
                        if url_result["status"] == "phishing":
                            score = max(score, 60)
        except Exception as e:
            # print(f"Error processing image for QR: {e}")
            pass

    status = "malicious" if score >= 50 else "safe"
    # If it's phishing from QR, we might want to say "phishing" or keep "malicious".
    # Since the unified status is what the frontend expects, "malicious" covers it for files.
    if "QR Link Analysis" in "".join(details) and score >= 50:
         status = "phishing" 

    return {"status": status, "score": score, "details": "; ".join(details)}
