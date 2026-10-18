@echo off
title CareerBridge Web Application
cd /d "%~dp0"

echo ===================================================================
echo                     CareerBridge Platform
echo ===================================================================
echo.
echo [1/3] Checking dependencies...
python -c "import flask, werkzeug, pymupdf, docx; print('All core packages verified.')" 2>nul
if errorlevel 1 (
    echo Installing missing packages from requirements.txt...
    pip install -r requirements.txt
)

echo [2/3] Checking and initializing database...
python database\init_db.py

echo [3/3] Launching CareerBridge Server on http://127.0.0.1:5000 ...
echo Opening browser window...
start http://127.0.0.1:5000

echo.
echo Server is LIVE. Press Ctrl+C in this command window to stop.
echo.
python app.py
pause
