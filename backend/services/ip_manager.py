import time
import json
import os

# Use absolute path for data file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "ip_data.json")

BLOCK_THRESHOLD = 3
BLOCK_DURATION = 300

ip_store = {}

def load_from_disk():
    global ip_store
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                ip_store = json.load(f)
            print(f"Loaded {len(ip_store)} IPs from disk.")
        except Exception as e:
            print(f"Error loading IP data: {e}")
            ip_store = {}

def save_to_disk():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(ip_store, f, indent=4)
    except Exception as e:
        print(f"Error saving IP data: {e}")

# Load data on module import
load_from_disk()

def get_ip_data(ip: str):
    return ip_store.get(ip, {"attempts": 0, "blocked_until": 0, "last_seen": 0})

def is_blocked(ip: str) -> bool:
    data = get_ip_data(ip)
    if data["blocked_until"] > time.time():
        return True
    return False

def record_activity(ip: str, is_suspicious: bool):
    data = get_ip_data(ip)
    
    # Reset attempts if it's been a while (e.g., 1 hour)
    if time.time() - data.get("last_seen", 0) > 3600:
        data["attempts"] = 0
    
    data["last_seen"] = time.time()
    
    if is_suspicious:
        data["attempts"] = data.get("attempts", 0) + 1
        if data["attempts"] >= BLOCK_THRESHOLD:
            data["blocked_until"] = time.time() + BLOCK_DURATION
            print(f"BLOCKING IP: {ip}")
    
    ip_store[ip] = data
    save_to_disk()

def unblock_ip(ip: str):
    if ip in ip_store:
        ip_store[ip]["blocked_until"] = 0
        ip_store[ip]["attempts"] = 0
        save_to_disk()

def get_all_ips():
    return ip_store
