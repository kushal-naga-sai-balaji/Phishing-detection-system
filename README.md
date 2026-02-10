<div align="center">

# 🛡️ PhishGuard - AI-Powered Phishing Detection System

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A comprehensive, real-time phishing detection system powered by Machine Learning that protects users from malicious URLs, phishing emails, suspicious files, and QR code attacks.**

[Features](#-features) • [Demo](#-quick-demo) • [Installation](#-installation) • [API Reference](#-api-reference) • [Architecture](#-architecture)

</div>

---

## 🎯 What is PhishGuard?

PhishGuard is an intelligent cybersecurity tool that combines **heuristic analysis** with **machine learning** to detect phishing threats in real-time. It analyzes URLs, emails, and files to identify potential security risks before they can harm users.

### Why PhishGuard?

- 🚀 **Real-time Detection** - Instant threat analysis with sub-second response times
- 🤖 **AI-Powered** - Uses Naive Bayes classifier with TF-IDF vectorization for accurate predictions
- 🔒 **Multi-Layer Protection** - Combines ML predictions with rule-based heuristics for robust detection
- 🌐 **Modern Web Interface** - Beautiful, responsive UI with drag-and-drop support
- 🛡️ **IP Protection** - Automatic blocking of suspicious IP addresses
- 🧩 **Browser Extension** - Chrome/Edge extension for real-time browsing protection
- 📱 **Mobile Application** - React Native app for on-the-go protection

---

## ✨ Features

### 🔗 URL Scanner
Analyzes URLs for phishing indicators:
- Raw IP address detection
- Suspicious keyword identification (`login`, `verify`, `banking`, etc.)
- URL length analysis
- ML-based pattern recognition

### 📧 Email Analyzer
Scans email content for social engineering attacks:
- Sender address analysis
- Subject line scanning
- Body content evaluation
- Combined threat scoring

### 📁 File & QR Code Scanner
Detects malicious files and QR codes:
- File hash verification against known malware signatures
- Executable file detection (`.exe`, `.bat`, `.sh`, `.vbs`)
- QR code extraction and URL analysis
- Image-based threat detection using OpenCV

### 🔐 IP Management & Admin Panel
Built-in security and administration:
- Automatic IP blocking for suspicious activity
- Activity logging and monitoring
- Admin dashboard for IP management
- Real-time status monitoring

### 🧩 Browser Extension
Chrome/Edge extension for seamless protection:
- Auto-scan pages as you browse
- Real-time phishing warnings
- Right-click context menu to scan links
- Form submission protection
- Desktop notifications for threats
- Statistics tracking

---

## 🚀 Quick Demo

<div align="center">

| URL Scanning | Email Analysis | Browser Extension |
|:---:|:---:|:---:|
| Paste any URL to check | Analyze email headers & body | Real-time browsing protection |

</div>

---

## 📦 Installation

### Quick Start (Recommended) ⚡

The easiest way to run PhishGuard:

```bash
# 1. Clone the repository
git clone https://github.com/kushal-naga-sai-balaji/Phishing-detection-system.git
cd Phishing-detection-system

# 2. Run the startup script (auto-installs dependencies)
# On macOS/Linux:
./run.sh

# On Windows:
run.bat

# Or use Python script (cross-platform):
python3 run.py
```

That's it! The script will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start the server automatically

### Manual Setup (Alternative)

If you prefer manual setup:

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- **Git** for cloning the repository

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/kushal-naga-sai-balaji/Phishing-detection-system.git
cd Phishing-detection-system

# 2. Navigate to the backend directory
cd backend

# 3. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python main.py
```

### Browser Extension Setup

Install the PhishGuard browser extension for real-time protection:

1. **Make sure the backend is running** (see steps above)

### Mobile Application Setup

Run the PhishGuard mobile app (Python/Kivy based):

1. **Navigate to the mobile app directory**:
   ```bash
   cd mobile_app
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the app**:
   ```bash
   python main.py
   ```

See [mobile_app/README.md](mobile_app/README.md) for Android packaging instructions via Buildozer.
2. **Open Chrome/Edge Extensions Page**
   - Chrome: `chrome://extensions/`
   - Edge: `edge://extensions/`
3. **Enable Developer Mode** (toggle in top right)
4. **Load Extension**
   - Click "Load unpacked"
   - Select the `browser-extension` folder
5. **Pin the Extension** to your toolbar

📖 Detailed instructions: See [browser-extension/INSTALLATION.md](browser-extension/INSTALLATION.md)

### Access the Application

Once running, open your browser and navigate to:

| Interface | URL |
|-----------|-----|
| 🌐 **Web App** | [http://localhost:8000](http://localhost:8000) |
| 📚 **API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 🔧 **ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| 🧩 **Extension** | Click PhishGuard icon in toolbar |

---

## 📡 API Reference

### Scan URL for Phishing

```http
POST /scan/url
Content-Type: application/json

{
  "url": "http://suspicious-login-verify.com"
}
```

**Response:**
```json
{
  "status": "phishing",
  "score": 75,
  "details": "URL contains suspicious keywords; AI detected phishing patterns (85% confidence)"
}
```

### Analyze Email

```http
POST /scan/email
Content-Type: application/json

{
  "subject": "Urgent: Verify Your Account",
  "body": "Click here to update your banking details immediately",
  "sender": "security@fake-bank.com"
}
```

### Scan File

```http
POST /scan/file
Content-Type: multipart/form-data

file: <your-file>
```

### All Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve main web interface |
| `/scan/url` | POST | Scan URL for phishing indicators |
| `/scan/email` | POST | Analyze email for phishing content |
| `/scan/file` | POST | Upload and scan file for threats |
| `/ip/status` | GET | Get current IP status and history |
| `/admin/ips` | GET | View all tracked IPs (Admin) |
| `/admin/unblock/{ip}` | POST | Unblock a specific IP (Admin) |
| `/docs` | GET | Interactive Swagger documentation |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          PhishGuard System                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────┐    ┌──────────────┐    ┌──────────────────┐        │
│  │   Frontend    │───▶│   FastAPI    │───▶│   ML Engine      │        │
│  │  (HTML/JS/CSS)│    │   Backend    │    │  (Naive Bayes)   │        │
│  └───────────────┘    └──────────────┘    └──────────────────┘        │
│         │                    │                      │                   │
│         │                    ▼                      │                   │
│  ┌───────────────┐    ┌──────────────┐             │                   │
│  │   Browser     │───▶│   Detector   │◀────────────┘                   │
│  │   Extension   │    │   Service    │                                 │
│  └───────────────┘    └──────────────┘                                 │
│         │                    │                                          │
│         │                    ▼                                          │
│         │             ┌──────────────┐                                  │
│         └────────────▶│ IP Manager   │                                  │
│                       │  & Blocker   │                                  │
│                       └──────────────┘                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Project Structure

```
📁 Phishing-detection-system/
├── 📁 backend/
│   ├── 📄 main.py              # FastAPI app & routes
│   ├── 📄 requirements.txt     # Python dependencies
│   ├── 📄 ip_data.json         # IP tracking data
│   ├── 📄 demo_script.py       # Testing script
│   └── 📁 services/
│       ├── 📄 detector.py      # Core detection logic
│       ├── 📄 ip_manager.py    # IP blocking system
│       └── 📄 ml_engine.py     # ML model (TF-IDF + Naive Bayes)
├── 📁 browser-extension/
│   ├── 📄 manifest.json        # Extension configuration
│   ├── 📄 popup.html           # Extension popup UI
│   ├── 📄 popup.css            # Popup styling
│   ├── 📄 popup.js             # Popup logic
│   ├── 📄 background.js        # Background service worker
│   ├── 📄 content.js           # Content script (page injection)
│   ├── 📄 INSTALLATION.md      # Extension setup guide
│   └── 📁 icons/               # Extension icons
├── 📁 frontend/
│   ├── 📄 index.html           # Main web interface
│   ├── 📄 script.js            # Frontend logic
│   └── 📄 style.css            # Styling (Glass morphism design)
├── 📄 .gitignore
└── 📄 README.md
```

---

## 🧠 How the ML Model Works

PhishGuard uses a **Naive Bayes classifier** with **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization:

1. **Text Vectorization**: Converts URLs/email text into numerical features using TF-IDF
2. **Classification**: Naive Bayes classifier predicts `phishing` or `safe`
3. **Confidence Scoring**: Returns probability score for the prediction
4. **Hybrid Approach**: Combines ML predictions with rule-based heuristics for final score

### Scoring System

| Score Range | Status | Description |
|-------------|--------|-------------|
| 0-39 | ✅ Safe | Low risk, likely legitimate |
| 40-69 | ⚠️ Suspicious | Medium risk, proceed with caution |
| 70-100 | 🚨 Phishing | High risk, likely malicious |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python, FastAPI, Uvicorn |
| **ML/AI** | Scikit-learn, TF-IDF, Naive Bayes |
| **Image Processing** | OpenCV, Pillow, NumPy |
| **QR Detection** | OpenCV, qrcode library |
| **Frontend** | HTML5, CSS3, JavaScript |
| **UI Design** | Glass morphism, Space Grotesk font |

---

## 🔮 Future Enhancements

- [ ] Deep learning models (LSTM/BERT) for better accuracy
- [ ] Browser extension for real-time protection
- [ ] Email integration (IMAP/POP3 scanning)
- [ ] Threat intelligence API integration
- [ ] User authentication and role management
- [ ] Detailed analytics dashboard

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

> This tool is developed for **educational and security research purposes only**. Always verify detection results independently. The developers are not responsible for any misuse of this software.

---

<div align="center">

### Made with ❤️ by [Kushal Naga Sai Balaji](https://github.com/kushal-naga-sai-balaji)

**⭐ Star this repo if you find it helpful!**

</div>
