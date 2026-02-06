# 🚀 PhishGuard - Quick Start Scripts

Three easy ways to run PhishGuard with automatic setup!

## Option 1: Shell Script (macOS/Linux) ⭐ Recommended

```bash
./run.sh
```

**Features:**
- ✅ Colorful terminal output
- ✅ Automatic dependency installation
- ✅ Virtual environment setup
- ✅ Clear status messages

## Option 2: Python Script (Cross-platform)

```bash
python3 run.py
```

**Features:**
- ✅ Works on any platform (Windows/macOS/Linux)
- ✅ Pure Python implementation
- ✅ Same functionality as shell script
- ✅ No need for bash/shell

## Option 3: Batch File (Windows)

```cmd
run.bat
```

**Features:**
- ✅ Native Windows batch script
- ✅ Double-click to run
- ✅ Automatic setup
- ✅ Pause on completion

---

## What These Scripts Do

1. **Check Python Installation** (3.8+ required)
2. **Create Virtual Environment** (if not exists)
3. **Install Dependencies** (from requirements.txt)
4. **Start the Server** (on http://localhost:8000)

## First Time Setup

### macOS/Linux:
```bash
chmod +x run.sh run.py  # Make scripts executable
./run.sh                # Run
```

### Windows:
```cmd
run.bat                 # Just double-click or run in cmd
```

### Python (Any OS):
```bash
python3 run.py          # Works everywhere
```

## What You'll See

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🛡️  PhishGuard - AI Phishing Detection System  🛡️     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

[1/4] Checking Python installation...
✅ Found Python 3.11.0

[2/4] Checking virtual environment...
✅ Virtual environment exists

[3/4] Checking dependencies...
✅ Dependencies are installed

[4/4] Starting PhishGuard server...

╔═══════════════════════════════════════════════════════════╗
║  🚀 Server is starting...                                 ║
╚═══════════════════════════════════════════════════════════╝

📍 Access points:
   🌐 Web Interface:  http://localhost:8000
   📚 API Docs:       http://localhost:8000/docs
   🧩 Extension:      Load from browser-extension/ folder

💡 Tips:
   • Press Ctrl+C to stop the server
   • Check browser-extension/QUICKSTART.md for extension setup
```

## Troubleshooting

### "Permission denied" (macOS/Linux)
```bash
chmod +x run.sh run.py
```

### "Python not found"
Install Python 3.8+ from [python.org](https://www.python.org/)

### "Module not found" errors
The scripts auto-install dependencies. If issues persist:
```bash
cd backend
pip install -r requirements.txt
```

### Port 8000 already in use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9  # macOS/Linux

# Or change port in backend/main.py
```

## Next Steps

After the server starts:

1. ✅ **Web Interface**: Open http://localhost:8000
2. ✅ **API Docs**: Visit http://localhost:8000/docs
3. ✅ **Browser Extension**: See `browser-extension/QUICKSTART.md`

---

**Choose your preferred method and start in seconds!** 🎯
