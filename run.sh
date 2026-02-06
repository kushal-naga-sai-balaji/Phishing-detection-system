#!/bin/bash

# PhishGuard - Easy Run Script
# This script sets up and runs the PhishGuard backend server

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║     🛡️  PhishGuard - AI Phishing Detection System  🛡️     ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
echo -e "${YELLOW}[1/4] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Found Python ${PYTHON_VERSION}${NC}"

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
echo -e "\n${YELLOW}[2/4] Checking virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Check and install dependencies
echo -e "\n${YELLOW}[3/4] Checking dependencies...${NC}"
# Use python -m pip to ensure we use the pip from the current python interpreter (venv)
if ! python3 -m pip show fastapi &> /dev/null; then
    echo "📦 Installing dependencies from requirements.txt..."
    python3 -m pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Dependencies are installed${NC}"
fi

# Start the server
echo -e "\n${YELLOW}[4/4] Starting PhishGuard server...${NC}"
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🚀 Server is starting...                                 ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📍 Access points:${NC}"
echo -e "   🌐 Web Interface:  ${GREEN}http://localhost:8000${NC}"
echo -e "   📚 API Docs:       ${GREEN}http://localhost:8000/docs${NC}"
echo -e "   🧩 Extension:      Load from browser-extension/ folder"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo -e "   • Press ${RED}Ctrl+C${NC} to stop the server"
echo -e "   • Check browser-extension/QUICKSTART.md for extension setup"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Run the server
python main.py
