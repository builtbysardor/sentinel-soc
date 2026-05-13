@echo off
echo ========================================
echo   SentinelLog v2.0
echo   Real-time Threat Detection System
echo ========================================
echo.

echo [1/3] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo [3/3] Starting SentinelLog server...
echo.
echo ========================================
echo   Server running at:
echo   http://localhost:8000
echo.
echo   Press Ctrl+C to stop
echo ========================================
echo.

python main.py

pause
