# 🛡️ Phishing Detection System

A comprehensive phishing detection system that uses machine learning to identify and block phishing attempts through URL analysis, email scanning, and real-time threat detection.

## 🚀 Features

- **URL Scanning**: Analyze URLs for phishing indicators using ML-based detection
- **Email Analysis**: Scan email content, subjects, and senders for phishing patterns
- **IP Management**: Automatic blocking of suspicious IP addresses
- **Real-time Detection**: Fast, efficient threat detection powered by machine learning
- **Modern Web Interface**: Clean, responsive frontend for easy interaction
- **REST API**: Full-featured FastAPI backend for integration with other systems

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── ip_data.json         # IP blocking data storage
│   ├── demo_script.py       # Demo/testing script
│   └── services/
│       ├── detector.py      # Core phishing detection logic
│       ├── ip_manager.py    # IP blocking and management
│       └── ml_engine.py     # Machine learning model engine
├── frontend/
│   ├── index.html           # Main web interface
│   ├── script.js            # Frontend JavaScript logic
│   └── style.css            # Styling
└── README.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phishing-detection-system.git
   cd phishing-detection-system
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   - Web Interface: `http://localhost:8000/static/index.html`
   - API Documentation: `http://localhost:8000/docs`

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scan/url` | POST | Scan a URL for phishing |
| `/scan/email` | POST | Analyze email content |
| `/admin/blocked-ips` | GET | View blocked IP addresses |
| `/docs` | GET | Interactive API documentation |

## 🔧 Technologies Used

- **Backend**: FastAPI, Python, Uvicorn
- **ML/AI**: Scikit-learn, NumPy
- **Image Processing**: OpenCV, Pillow
- **Frontend**: HTML5, CSS3, JavaScript

## 📊 How It Works

1. **URL Analysis**: The system extracts features from URLs (domain age, SSL status, suspicious patterns) and runs them through an ML model
2. **Email Scanning**: Analyzes email headers, content, and sender reputation to detect phishing attempts
3. **Threat Scoring**: Each scan returns a threat score and detailed analysis
4. **IP Protection**: Automatically blocks IPs showing suspicious behavior

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and security research purposes. Always verify results and use responsibly.

---

Made with ❤️ for cybersecurity
