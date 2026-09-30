# CareerEdge AI — Hardware & Environment Diagnostic Report
**Target Competition:** Snapdragon® AI Lab Build & Present Challenge by Qualcomm  
**Target Platform:** Snapdragon-powered HP Windows PCs (ARM64 Hexagon NPU)  
**Report Generated:** September 29, 2026  
**Status:** Authentic Local Hardware Inspection Completed

---

## 1. System Hardware & Operating System

| Attribute | Detected Value | Verification Method |
| :--- | :--- | :--- |
| **Operating System** | Windows 11 Pro (10.0.26200-SP0) | `platform.platform()` |
| **CPU Model** | Intel64 Family 6 Model 126 Stepping 5, GenuineIntel | `platform.processor()` |
| **Host Architecture** | AMD64 (x86_64) | `platform.machine()` |
| **Primary GPU** | Intel(R) UHD Graphics Family (Driver 31.0.101.2141) | `Win32_VideoController` |
| **Snapdragon NPU** | **Not Present on Host** (Development Machine is Intel x86_64) | `Get-PnpDevice` / Hardware Tree Query |
| **Qualcomm Hexagon NPU** | Not detected on host hardware | Device Manager & WMI Scan |

---

## 2. Software Runtime Environment

| Component | Detected Version | Notes |
| :--- | :--- | :--- |
| **Python** | 3.14.7 AMD64 (Anaconda, Inc.) | Active Python interpreter |
| **Node.js** | v24.18.0 | Active Node runtime |
| **npm** | 11.16.0 | Frontend package manager |
| **Pip** | 26.2.1 | Package installer for Python |
| **ONNX Runtime** | 1.30.0 | High-performance inference engine |
| **NumPy** | 2.5.3 | Numerical computing engine |
| **Scikit-Learn** | 1.9.1 | Embedding and cosine similarity engine |
| **PyPDF** | 6.19.0 | Local PDF document text parser |
| **Python-Docx** | 1.2.0 | Local DOCX document text parser |
| **ReportLab** | 5.0.1 | Client-side/local PDF career report generator |

---

## 3. ONNX Runtime & Qualcomm QNN Inspection

```python
import onnxruntime as ort
print("ONNX Runtime Version:", ort.__version__)
# -> 1.30.0
print("Available Providers:", ort.get_available_providers())
# -> ['AzureExecutionProvider', 'CPUExecutionProvider']
```

### QNN Execution Provider Status:
- **`QNNExecutionProvider` Detected:** `False`
- **Reason:** The development machine is an Intel x64 system. The Qualcomm QNN Execution Provider (`QNNExecutionProvider`) requires Windows on Snapdragon ARM64 hardware (Snapdragon X Elite, Snapdragon X Plus) with Qualcomm Hexagon NPU drivers and Qualcomm Neural Processing SDK binaries (`qnn_onnxruntime.dll` / `QnnHtp.dll`).

---

## 4. Hardware Verification & Anti-Fabrication Declarations

In strict accordance with the Qualcomm competition guidelines:
1. **No False NPU Claims:** The application will **never** claim `NPU ACTIVE` when running on this Intel x64 system. The AI Runtime status will explicitly display:
   ```
   LOCAL AI • CPU FALLBACK ACTIVE (Intel64 Family 6 Model 126)
   ```
2. **Graceful Fallback:** The backend AI runtime abstraction (`engine/qnn_runtime.py`) is designed with a hardware-adaptive provider chain:
   - Priority 1: `QNNExecutionProvider` (Activated automatically when deployed on Snapdragon X Elite/Plus PCs)
   - Priority 2: Deliberate Accelerator (DirectML / GPU if configured)
   - Priority 3: `CPUExecutionProvider` (Active on development machine)
3. **No Fabricated Benchmarks:** All benchmark metrics displayed in the live system represent actual physical timing on the executing machine. Qualcomm AI Hub reference benchmarks for Snapdragon X Elite are kept strictly distinct in dedicated documentation and clearly labeled as **Reference Benchmarks**.

---

## 5. Current Project Structure

```
CareerEdge-AI/
├── frontend/             # React + TypeScript + Vite UI
├── backend/              # FastAPI Local Application Server
│   ├── api/              # REST Endpoints (/health, /device, /resume, /job, /match, /roadmap, /benchmark)
│   ├── engine/           # Career Intelligence, Scoring, Explainability Engine
│   ├── models/           # Pydantic Schemas & DTOs
│   ├── services/         # Resume Parser, Job Parser, Skill Ontology
│   ├── database/         # Local SQLite Session Storage
│   └── utils/            # Document extraction & validation
├── ai/
│   ├── models/           # Local ONNX Embedding Model artifacts
│   ├── runtime/          # Hardware detection, QNN loader, CPU fallback
│   ├── embeddings/       # Local Sentence-level Embedding generator
│   └── preprocessing/    # Text normalization & skill alias ontology
├── demo/                 # Synthetic offline demo datasets (Alex Morgan - ML Engineer)
├── benchmarks/           # Reproducible benchmark harness & latest reports
├── tests/                # Comprehensive unit and integration test suite
└── docs/                 # Competition submission, architecture, model card, pitch, setup
```

---

## 6. Recommended Runtime Mode

- **Development & Local Evaluation Mode:** `CPUExecutionProvider` (High efficiency, 100% offline, zero cloud API dependencies).
- **Target Deployment Mode (Snapdragon PC):** `QNNExecutionProvider` on Qualcomm Hexagon NPU (NPU inference with INT8 / FP16 quantized models for sub-10ms latency and minimal battery impact).
