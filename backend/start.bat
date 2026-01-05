@echo off
chcp 65001 >nul
cls
echo ====================================
echo  DebtCall Automator - Backend
echo ====================================
echo.

REM Activate virtual environment from parent directory
if exist "..\.venv\Scripts\activate.bat" (
    call "..\.venv\Scripts\activate.bat"
) else (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Create data directories if needed
REM Check dependencies
echo [*] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [!] Installing dependencies...
    pip install -r requirements.txt
)

REM Create data directories
if not exist "data\db" mkdir "data\db"
if not exist "data\audio" mkdir "data\audio"
if not exist "data\uploads" mkdir "data\uploads"
if not exist "data\exports" mkdir "data\exports"

echo [*] Starting Backend Server...
echo [*] URL: http://127.0.0.1:8000
echo [*] Docs: http://127.0.0.1:8000/docs
echo.

uvicorn main:app --reload --host 127.0.0.1 --port 8000
