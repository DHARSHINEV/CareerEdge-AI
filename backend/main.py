"""
CareerEdge AI - Main FastAPI Application Server
Private On-Device Career Intelligence for Snapdragon PCs.
"""

import os
import sys
import logging
import pathlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add root directory to sys.path
BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from backend.api.routes import router as api_router
from backend.engine.qnn_runtime import get_runtime_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("careeredge.main")

app = FastAPI(
    title="CareerEdge AI — Private On-Device Career Intelligence",
    description="Privacy-first AI Career Copilot designed for Snapdragon-powered Windows PCs.",
    version="1.0.0",
)

# Enable CORS for local Vite development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router)

# Mount frontend production build if available
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")
    logger.info(f"Mounted production frontend from {FRONTEND_DIST}")


@app.on_event("startup")
async def startup_event():
    logger.info("=" * 65)
    logger.info("  Starting CareerEdge AI Application Server")
    logger.info("  Qualcomm Snapdragon® AI Lab Challenge 2026")
    logger.info("=" * 65)

    # Trigger runtime manager initialization
    try:
        runtime_mgr = get_runtime_manager()
        status = runtime_mgr.get_runtime_status()
        logger.info(f"Hardware Host: {status['device_name']} ({status['architecture']})")
        logger.info(f"Processor: {status['processor']}")
        logger.info(f"Active Provider: {status['active_provider']}")
        logger.info(f"Status Label: {status['status_label']}")
        logger.info(f"QNN NPU Available: {status['qnn_available']}")
    except Exception as e:
        logger.error(f"Error during runtime initialization: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
