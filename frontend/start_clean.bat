@echo off
chcp 65001 >nul
echo ====================================
echo  DebtCall Automator - Frontend
echo ====================================
echo.

REM Check node_modules
if not exist "node_modules" (
    echo [!] Dependencies not installed!
    echo [*] Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
)

REM Check port 5173
echo [*] Checking port 5173...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173" ^| find "LISTENING"') do (
    echo [!] Port 5173 is busy (PID %%a)
    echo [?] Kill process? (Y/N)
    choice /c YN /n
    if errorlevel 2 goto skip_kill
    taskkill /F /PID %%a
)
:skip_kill

echo.
echo [*] Starting frontend at http://localhost:5173
echo [*] Backend API: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop
echo ====================================
echo.

REM Start dev server
call npm run dev
