@echo off
TITLE CareerEdge AI - Snapdragon On-Device Career Intelligence
echo ======================================================================
echo   CareerEdge AI - Private On-Device Career Intelligence
echo   Qualcomm Snapdragon(R) AI Lab Build ^& Present Challenge 2026
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/3] Verifying Python and ONNX Runtime environment...
python -c "import onnxruntime, fastapi, uvicorn; print('ONNX Runtime:', onnxruntime.__version__, '| Providers:', onnxruntime.get_available_providers())"
if %ERRORLEVEL% NEQ 0 (
    echo Error: Missing Python dependencies. Running pip install...
    python -m pip install -r requirements.txt
)

echo.
echo [2/3] Starting CareerEdge AI Backend Server on port 8000...
start "CareerEdge Backend" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

ping -n 4 127.0.0.1 >nul

echo.
echo [3/3] Launching CareerEdge AI Frontend on port 5173...
cd /d "%~dp0frontend"
start "CareerEdge Frontend" cmd /k "node node_modules\vite\bin\vite.js --port 5173 --host"

ping -n 4 127.0.0.1 >nul

echo.
echo Opening browser to http://localhost:5173 ...
start http://localhost:5173

echo.
echo ======================================================================
echo   CareerEdge AI is now LIVE!
echo   Frontend: http://localhost:5173
echo   Backend ^& API Docs: http://127.0.0.1:8000/docs
echo   Privacy: 100%% On-Device / Zero Cloud Upload
echo ======================================================================
