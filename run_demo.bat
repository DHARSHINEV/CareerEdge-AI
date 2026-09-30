@echo off
TITLE CareerEdge AI - 1-Click Competition Demo
echo ======================================================================
echo   CareerEdge AI - 1-Click Competition Demonstration Launcher
echo   Qualcomm Snapdragon(R) AI Lab Challenge 2026
echo ======================================================================
echo.

cd /d "%~dp0"

echo Starting server and launching browser demo...
start "CareerEdge Backend" cmd /c "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

ping -n 4 127.0.0.1 >nul

start http://127.0.0.1:8000
echo.
echo Application opened in your default browser at http://127.0.0.1:8000
echo Enjoy exploring CareerEdge AI!
