#!/usr/bin/env python3


"""
PhishGuard Quick Start Script
Run this script to start the PhishGuard backend server with automatic setup
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

# Colors for terminal output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color
    
    @staticmethod
    def disable():
        Colors.BLUE = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.NC = ''

# Disable colors on Windows
if platform.system() == 'Windows':
    Colors.disable()

def print_header():
    print(f"{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║     🛡️  PhishGuard - AI Phishing Detection System  🛡️     ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.NC}\n")

def check_python():
    print(f"{Colors.YELLOW}[1/4] Checking Python installation...{Colors.NC}")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"{Colors.RED}❌ Python 3.8+ required. You have {version.major}.{version.minor}{Colors.NC}")
        sys.exit(1)
    print(f"{Colors.GREEN}✅ Python {version.major}.{version.minor}.{version.micro} found{Colors.NC}")

def setup_venv():
    print(f"\n{Colors.YELLOW}[2/4] Setting up virtual environment...{Colors.NC}")
    backend_dir = Path(__file__).parent / "backend"
    venv_dir = backend_dir / "venv"
    
    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        print(f"{Colors.GREEN}✅ Virtual environment created{Colors.NC}")
    else:
        print(f"{Colors.GREEN}✅ Virtual environment exists{Colors.NC}")
    
    return venv_dir

def get_python_path(venv_dir):
    if platform.system() == 'Windows':
        return venv_dir / "Scripts" / "python.exe"
    else:
        return venv_dir / "bin" / "python"

def install_dependencies(venv_dir):
    print(f"\n{Colors.YELLOW}[3/4] Installing dependencies...{Colors.NC}")
    backend_dir = Path(__file__).parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    python_path = get_python_path(venv_dir)
    
    # Check if fastapi is installed
    try:
        subprocess.run(
            [str(python_path), "-m", "pip", "show", "fastapi"],
            capture_output=True,
            check=True
        )
        print(f"{Colors.GREEN}✅ Dependencies already installed{Colors.NC}")
    except subprocess.CalledProcessError:
        print("📦 Installing from requirements.txt...")
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "-r", str(requirements_file)],
            check=True
        )
        print(f"{Colors.GREEN}✅ Dependencies installed{Colors.NC}")

def start_server(venv_dir):
    print(f"\n{Colors.YELLOW}[4/4] Starting PhishGuard server...{Colors.NC}\n")
    print(f"{Colors.GREEN}╔═══════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.GREEN}║  🚀 Server is starting...                                 ║{Colors.NC}")
    print(f"{Colors.GREEN}╚═══════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.BLUE}📍 Access points:{Colors.NC}")
    print(f"   🌐 Web Interface:  {Colors.GREEN}http://localhost:8000{Colors.NC}")
    print(f"   📚 API Docs:       {Colors.GREEN}http://localhost:8000/docs{Colors.NC}")
    print(f"   🧩 Extension:      Load from browser-extension/ folder\n")
    
    print(f"{Colors.YELLOW}💡 Tips:{Colors.NC}")
    print(f"   • Press {Colors.RED}Ctrl+C{Colors.NC} to stop the server")
    print(f"   • Check browser-extension/QUICKSTART.md for extension setup\n")
    
    print(f"{Colors.BLUE}════════════════════════════════════════════════════════════{Colors.NC}\n")
    
    backend_dir = Path(__file__).parent / "backend"
    python_path = get_python_path(venv_dir)
    main_file = backend_dir / "main.py"
    
    try:
        subprocess.run(
            [str(python_path), str(main_file)],
            cwd=str(backend_dir),
            check=True
        )
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}👋 PhishGuard server stopped{Colors.NC}")
        sys.exit(0)

def main():
    try:
        print_header()
        check_python()
        venv_dir = setup_venv()
        install_dependencies(venv_dir)
        start_server(venv_dir)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}👋 Setup cancelled{Colors.NC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
