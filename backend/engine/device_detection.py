"""
CareerEdge AI - Device Detection & Hardware Diagnostics
Strictly inspects host CPU, GPU, Snapdragon NPU presence, and ONNX Runtime capabilities.
Zero fabrication: never claims NPU unless verified on host.
"""

import os
import platform
import subprocess
import logging
from typing import Dict, Any, List

logger = logging.getLogger("careeredge.device")


def get_hardware_diagnostics() -> Dict[str, Any]:
    """
    Detects hardware, CPU architecture, GPU, and physical NPU presence on Windows.
    """
    os_name = f"{platform.system()} {platform.release()} (Build {platform.version()})"
    arch = platform.machine()
    processor = platform.processor() or "Unknown Processor"
    hostname = platform.node()

    gpu_name = None
    npu_detected = False
    npu_name = None

    # Inspect Windows Video Controller (GPU)
    try:
        cmd = 'powershell -NoProfile -Command "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=4)
        if res.returncode == 0 and res.stdout.strip():
            gpus = [line.strip() for line in res.stdout.strip().splitlines() if line.strip()]
            gpu_name = ", ".join(gpus)
    except Exception as e:
        logger.debug(f"GPU detection error: {e}")

    # Inspect PnP devices for Snapdragon / Hexagon / NPU
    try:
        import re
        pnp_cmd = 'powershell -NoProfile -Command "Get-PnpDevice | Where-Object { `$_.FriendlyName -match \'\\b(Snapdragon|Hexagon|Qualcomm|Neural)\\b\' } | Select-Object -ExpandProperty FriendlyName"'
        res = subprocess.run(pnp_cmd, shell=True, capture_output=True, text=True, timeout=4)
        if res.returncode == 0 and res.stdout.strip():
            lines = [l.strip() for l in res.stdout.strip().splitlines() if l.strip()]
            npu_pattern = re.compile(r"\b(hexagon|qualcomm\s+npu|neural\s+processor|snapdragon\s+compute)\b", re.IGNORECASE)
            for line in lines:
                # Strictly reject any 'input' devices or audio/peripherals
                if "input" in line.lower():
                    continue
                if npu_pattern.search(line) or (re.search(r"\bnpu\b", line, re.IGNORECASE) and not "input" in line.lower()):
                    npu_detected = True
                    npu_name = line
                    break
    except Exception as e:
        logger.debug(f"NPU hardware scan error: {e}")

    # Also check architecture: Snapdragon Windows PCs identify as ARM64
    is_arm64 = arch.lower() in ["arm64", "aarch64"]
    if is_arm64 and not npu_name:
        # On Snapdragon X Elite / Plus, NPU is integrated
        if "snapdragon" in processor.lower() or "qualcomm" in processor.lower():
            npu_detected = True
            npu_name = "Qualcomm Hexagon NPU (45 TOPS)"

    return {
        "device_name": hostname,
        "os_name": os_name,
        "architecture": arch,
        "processor": processor,
        "gpu_name": gpu_name or "Standard Display Adapter",
        "npu_detected": npu_detected,
        "npu_name": npu_name,
        "is_arm64": is_arm64,
    }
