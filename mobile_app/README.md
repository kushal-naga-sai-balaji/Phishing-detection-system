# PhishGuard Mobile (Python/Kivy)

This is a **Python-based** mobile application for the Phishing Detection System, using the [Kivy](https://kivy.org/) framework. It works on Windows, macOS, Linux, Android, and iOS without requiring Node.js or npm.

## Prerequisites

- Python 3.8+
- The backend server running locally

## Installation

1. Navigate to the `mobile_app` directory:
   ```bash
   cd mobile_app
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Open `main.py` and modify the `API_URL` variable if needed.
- **Local Desktop Testing**: `http://127.0.0.1:8000/scan/url`
- **Android Emulator**: `http://10.0.2.2:8000/scan/url`

## Running Locally

To run the app on your computer (simulating the mobile interface):

```bash
python main.py
```

## Building for Android

To package this as an APK for Android, you use `buildozer`.

1. Install Buildozer:
   ```bash
   pip install buildozer
   ```
2. Initialize and build (requires Linux/macOS):
   ```bash
   buildozer init
   buildozer -v android debug
   ```

## Building for macOS

To package this as a standalone macOS application (`.app`):

1. **Run the build script**:
   ```bash
   ./build_macos.sh
   ```
   
   *This uses `PyInstaller` to bundle the Python environment and the app together.*

2. **Locate the App**:
   The application will be generated in `dist/PhishGuard.app`. You can double-click it to run it without needing a terminal.
