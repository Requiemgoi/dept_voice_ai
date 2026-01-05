@echo off
chcp 65001 >nul
cls
echo ====================================
echo  DebtCall Automator - Frontend  
echo ====================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo [*] Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [*] Starting Frontend Server...
echo [*] URL: http://localhost:5173
echo.

npm run dev
