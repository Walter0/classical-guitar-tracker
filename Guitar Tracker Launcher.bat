@echo off
echo 🎸 Starting Classical Guitar Learning Tracker...
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo Installing/checking Streamlit...
pip install streamlit >nul 2>&1

echo 🚀 Launching Guitar Tracker...
echo.
echo 💡 Your browser will open automatically
echo 💡 Close this window to stop the app
echo.

python launch.py
pause