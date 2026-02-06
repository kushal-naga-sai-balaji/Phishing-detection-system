import unittest
import os
import sys
import shutil
import tempfile

# Add backend directory to path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import ml_engine, detector, ip_manager

class TestMLEngine(unittest.TestCase):
    def test_training_and_prediction(self):
        # Force training
        ml_engine.train_model()
        
        # Test Safe
        safe_res = ml_engine.predict_text("google.com")
        self.assertEqual(safe_res["label"], "safe")
        
        # Test Phishing
        phish_res = ml_engine.predict_text("secure-login-update.com")
        self.assertEqual(phish_res["label"], "phishing")

class TestDetector(unittest.TestCase):
    def test_url_detection(self):
        # Good URL
        res = detector.detect_url("https://github.com/sangineedikushal/Phishing-detection-system")
        self.assertEqual(res["status"], "safe")
        
        # Bad URL (IP address)
        res = detector.detect_url("http://192.168.1.1/login")
        # IP (+30) + 'login' keyword (+10) + ML detection (likely ~40-50) = ~80+
        self.assertGreater(res["score"], 50) 
        self.assertEqual(res["status"], "phishing")
        
        # Bad URL (Keywords + length if long)
        res = detector.detect_url("http://secure-update-account-verify-login-now-urgent-winner.com")
        self.assertEqual(res["status"], "phishing")

    def test_email_detection(self):
        # Phishing Email
        res = detector.detect_email(
            subject="Urgent: Your account will be suspended",
            body="Click here to verify your banking details immediately",
            sender="admin@secure-bank-verify.com"
        )
        self.assertEqual(res["status"], "phishing")

class TestIPManager(unittest.TestCase):
    def setUp(self):
        # Backup existing ip_data.json if exists
        self.original_data = ip_manager.ip_store
        ip_manager.ip_store = {}
        
    def tearDown(self):
        ip_manager.ip_store = self.original_data
        
    def test_blocking_logic(self):
        test_ip = "1.2.3.4"
        
        # Suspicious activity 1
        ip_manager.record_activity(test_ip, is_suspicious=True)
        self.assertFalse(ip_manager.is_blocked(test_ip))
        
        # Suspicious activity 2
        ip_manager.record_activity(test_ip, is_suspicious=True)
        self.assertFalse(ip_manager.is_blocked(test_ip))
        
        # Suspicious activity 3 (Should Block)
        ip_manager.record_activity(test_ip, is_suspicious=True)
        self.assertTrue(ip_manager.is_blocked(test_ip))
        
        # Unblock
        ip_manager.unblock_ip(test_ip)
        self.assertFalse(ip_manager.is_blocked(test_ip))

if __name__ == '__main__':
    unittest.main()
