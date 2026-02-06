@echo off
REM PhishGuard - Easy Run Script for Windows
REM This script sets up and runs the PhishGuard backend server

title PhishGuard - AI Phishing Detection System

echo.
echo ===============================================================
echo.
echo      PhishGuard - AI Phishing Detection System
echo.
echo ===============================================================
echo.

REM Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%

REM Navigate to backend directory
cd /d "%~dp0\backend"

REM Check if virtual environment exists
echo.
echo [2/4] Checking virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check and install dependencies
echo.
echo [3/4] Checking dependencies...
python -m pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies are installed
)

REM Start the server
echo.
echo [4/4] Starting PhishGuard server...
echo.
echo ===============================================================
echo   Server is starting...
echo ===============================================================
echo.
echo Access points:
echo   Web Interface:  http://localhost:8000
echo   API Docs:       http://localhost:8000/docs
echo   Extension:      Load from browser-extension\ folder
echo.
echo Tips:
echo   * Press Ctrl+C to stop the server
echo   * Check browser-extension\QUICKSTART.md for extension setup
echo.
echo ===============================================================
echo.

REM Run the server
python main.py

pause
