@echo off
REM Quick Start Setup Script for Google Gemini API Integration (Windows)
REM This script helps you set up Google Gemini API in minutes

setlocal enabledelayedexpansion

cls
echo ==================================================
echo   Google Gemini API - Quick Start Setup (Windows)
echo ==================================================
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo * Python version: %PYTHON_VERSION%

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo.
    echo Creating virtual environment...
    python -m venv .venv
    echo * Virtual environment created
) else (
    echo * Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Installing pip...
python -m pip install --upgrade pip -q

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q
echo * Dependencies installed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Setting up environment configuration...
    (
        echo # Google Gemini API Configuration
        echo # Get your API key from: https://aistudio.google.com/app/apikeys
        echo.
        echo GOOGLE_API_KEY=YOUR_API_KEY_HERE
        echo GOOGLE_MODEL=gemini-1.5-flash
        echo GOOGLE_TEMPERATURE=0.7
    ) > .env
    echo * Created .env file (update with your API key)
) else (
    echo * .env file already exists
)

cls
echo ==================================================
echo   Setup Complete!
echo ==================================================
echo.
echo Next Steps:
echo.
echo 1. Get your Google API key:
echo    --^> https://aistudio.google.com/app/apikeys
echo.
echo 2. Update .env file with your API key:
echo    --^> Open .env with your editor and replace YOUR_API_KEY_HERE
echo.
echo 3. Run the application:
echo    python main.py
echo.
echo Documentation: See GEMINI_SETUP.md
echo.
pause
