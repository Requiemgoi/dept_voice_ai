@echo off
chcp 65001 >nul
echo ====================================
echo  DebtCall Automator - Backend Server
echo ====================================
echo.

REM Check virtual environment in parent directory
if not exist "..\\.venv" (
    echo [ERROR] Virtual environment not found!
    echo Please create it: python -m venv .venv
    echo Run this command from the project root directory
    pause
    exit /b 1
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call ..\\.venv\\Scripts\\activate.bat

REM Check dependencies
echo [*] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [!] Dependencies not installed. Installing...
    pip install -r requirements.txt
)

REM Create necessary directories
echo [*] Creating directories...
if not exist "data\\db" mkdir data\\db
if not exist "data\\audio" mkdir data\\audio
if not exist "data\\uploads" mkdir data\\uploads
if not exist "data\\exports" mkdir data\\exports

REM Check and clear port 8000 if needed
echo [*] Checking port 8000...
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul
if not errorlevel 1 (
    echo [!] Port 8000 is already in use
    echo [*] Attempting to free the port...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
        echo [*] Killing process PID: %%a
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 >nul
)

echo.
echo [*] Starting server at http://127.0.0.1:8000
echo [*] API docs: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop
echo ====================================
echo.

REM Start server
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
