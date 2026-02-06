import requests
import qrcode
import io
import time
import os

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

import json

def unblock_myself():
    try:
        # Read local ip_data.json to find IPs
        if os.path.exists("ip_data.json"):
            with open("ip_data.json", "r") as f:
                data = json.load(f)
                for ip in data.keys():
                    requests.post(f"{BASE_URL}/admin/unblock/{ip}")
    except Exception as e:
        print(f"Failed to unblock: {e}")

def test_url_scan():
    unblock_myself()
    print_section("TESTING URL DETECTION")
    
    # 1. Phishing URL
    phishing_url = "http://verify-account-security.net"
    print(f"Scanning Phishing URL: {phishing_url}")
    try:
        res = requests.post(f"{BASE_URL}/scan/url", json={"url": phishing_url})
        print("Response:", res.json())
    except Exception as e:
        print("Error:", e)
        
    # 2. Safe URL
    safe_url = "https://google.com"
    print(f"\nScanning Safe URL: {safe_url}")
    try:
        res = requests.post(f"{BASE_URL}/scan/url", json={"url": safe_url})
        print("Response:", res.json())
    except Exception as e:
        print("Error:", e)

def test_email_scan():
    print_section("TESTING EMAIL ANALYSIS")
    
    # 1. Phishing Email
    print("Analysing Phishing Email...")
    email_data = {
        "subject": "URGENT: Verify your account",
        "body": "Dear user, click here to login to your bank account immediately or it will be suspended.",
        "sender": "security@fake-bank-alert.com"
    }
    try:
        res = requests.post(f"{BASE_URL}/scan/email", json=email_data)
        print("Response:", json.dumps(res.json(), indent=2))
    except Exception as e:
        print("Error:", e)

def test_file_scan():
    print_section("TESTING FILE DETECTION")
    
    # 1. EICAR Test String (Simulated Malware)
    print("Scanning Malicious File Content (EICAR)...")
    eicar_content = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    files = {'file': ('test_virus.txt', eicar_content, 'text/plain')}
    
    try:
        res = requests.post(f"{BASE_URL}/scan/file", files=files)
        print("Response:", json.dumps(res.json(), indent=2))
    except Exception as e:
        print("Error:", e)

def check_admin_stats():
    print_section("CHECKING ADMIN STATS")
    try:
        res = requests.get(f"{BASE_URL}/admin/ips")
        print("Blocked IPs and History:", json.dumps(res.json(), indent=2))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # Wait for server to start
    print("Waiting for server to be ready...")
    time.sleep(2) 
    
    test_url_scan()
    test_email_scan()
    test_file_scan()
    check_admin_stats()
    print_section("DEMO COMPLETED")
    print_section("TESTING EMAIL DETECTION")
    
    # 1. Phishing Email
    payload = {
        "sender": "alert@paypal-ident-verify.com",
        "subject": "Urgent: Account Suspension",
        "body": "Your account will be suspended if you do not login and verify your banking details immediately."
    }
    print("Scanning Phishing Email:")
    print(payload)
    try:
        res = requests.post(f"{BASE_URL}/scan/email", json=payload)
        print("Response:", res.json())
    except Exception as e:
        print("Error:", e)

def test_file_scan():
    unblock_myself()
    print_section("TESTING FILE/VIRUS DETECTION")
    
    # 1. Test EICAR string (Virus)
    eicar_str = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    print("Scanning EICAR Test File (Virus Content)")
    
    files = {'file': ('eicar.txt', eicar_str)}
    try:
        res = requests.post(f"{BASE_URL}/scan/file", files=files)
        print("Response:", res.json())
    except Exception as e:
        print("Error:", e)
        
    # 2. Test Safe File
    print("\nScanning Safe Text File")
    files = {'file': ('hello.txt', 'Just a harmless text file.')}
    try:
        res = requests.post(f"{BASE_URL}/scan/file", files=files)
        print("Response:", res.json())
    except Exception as e:
        print("Error:", e)

def test_qr_scan():
    unblock_myself()
    print_section("TESTING QR CODE DETECTION")
    
    # 1. Generate QR with Phishing URL
    phishing_link = "http://free-prize-winner.com/claim-now"
    print(f"Generating QR Code containing phishing link: {phishing_link}")
    
    qr = qrcode.QRCode()
    qr.add_data(phishing_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Upload QR
    files = {'file': ('phishing_qr.png', img_byte_arr, 'image/png')}
    
    print("Uploading QR Code...")
    try:
        res = requests.post(f"{BASE_URL}/scan/file", files=files)
        print("Response:", res.json())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # Wait for server to start if running via automation
    print("Waiting for server to be ready...", end="", flush=True)
    for _ in range(10):
        try:
            requests.get(BASE_URL)
            print(" Ready!")
            break
        except:
            time.sleep(1)
            print(".", end="", flush=True)
    else:
        print("\nServer not reachable. Make sure it's running.")
        exit(1)
        
    test_url_scan()
    test_email_scan()
    test_file_scan()
    test_qr_scan()
