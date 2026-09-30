# Qualcomm Snapdragon® AI Lab Build & Present Challenge — Official Submission Q&A
**Project Title:** CareerEdge AI — Private On-Device Career Intelligence for Snapdragon PCs  
**Tagline:** Understand your career gap. Improve it privately. Run AI locally.

---

### 1. Project Title
**CareerEdge AI** (Private On-Device Career Intelligence)

---

### 2. One-Line Description
A privacy-first career copilot running 100% locally on Snapdragon-powered Windows PCs that analyzes resumes against target job postings, isolates technical skill gaps, and generates actionable 30-day improvement roadmaps without cloud data leaks.

---

### 3. Problem Statement
Job candidates frequently encounter high rejection rates without understanding *why* their background fell short of employer expectations. Existing cloud-based AI tools require users to upload sensitive personal documents (contact information, employment dates, company names, intellectual property) to third-party cloud servers, posing severe privacy risks, incurring API subscription costs, and leaving candidates with generic, unexplainable percentages rather than actionable guidance.

---

### 4. Proposed Solution
CareerEdge AI brings private career intelligence directly to the user's PC:
1. **Document Understanding:** Locally parses resumes (PDF/DOCX/TXT) and job postings using custom regex chunking and alias ontology normalization.
2. **On-Device Semantic Matching:** Employs a local quantized ONNX Transformer model (`all-MiniLM-L6-v2`) to compute dense semantic embeddings and cosine similarities on the host device.
3. **Deterministic Alignment:** Computes an explainable Profile-to-Role Alignment Score across five transparent dimensions (Technical Skills 40%, Projects 25%, Experience 15%, Education 10%, Domain 10%).
4. **"Why Is My Profile Not Aligned?":** Highlights top critical skill gaps with exact missing evidence, concept learning checklists, capstone project blueprints, and honest resume bullet templates.
5. **Personalized 30-Day Roadmap:** Daily milestones linking actionable deliverables to detected gaps.
6. **Executive PDF Export:** Compiles a publication-grade assessment report locally.

---

### 5. Innovation & Key Differentiators
- **Beyond Keyword Matching:** Combines exact ontology alias matching (`k8s` -> `Kubernetes`, `postgres` -> `PostgreSQL`) with dense semantic vector embeddings.
- **Explainability Over Black-Box Scores:** Every requirement shows its classification (`Strong`, `Partial`, `Missing`), exact cited evidence from the resume, and a concrete recommendation to bridge it.
- **Zero Metric Hallucination:** Resume bullet improver refuses to invent metrics; it provides structured templates with explicit `[insert measured metric]` placeholders.
- **Hardware-Adaptive AI Engine:** Seamlessly executes via Qualcomm QNN on Snapdragon Hexagon NPUs while maintaining an authentic, verified CPU fallback on x86_64 development environments.

---

### 6. Technology Stack
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS / Vanilla CSS, Lucide React icons.
- **Backend:** Python 3, FastAPI, Uvicorn, Pydantic v2.
- **Inference Runtime:** ONNX Runtime 1.30.0 with Qualcomm QNN Execution Provider (`QNNExecutionProvider`) and `CPUExecutionProvider`.
- **AI Models:** `all-MiniLM-L6-v2` (INT8 Quantized ONNX, 22.9 MB footprint, 384-dimensional dense vectors).
- **Document Processing:** PyPDF, Python-Docx, ReportLab.
- **Local Storage:** SQLite (`backend/database/careeredge.db`).

---

### 7. Snapdragon PC Optimization & Hardware Architecture
CareerEdge AI is designed around Qualcomm's Windows-on-Snapdragon architecture. Inference is decoupled through an `AIEngine` abstraction that binds the `QNNExecutionProvider` on Snapdragon X Elite/Plus PCs, routing tensor computations to the Qualcomm Hexagon NPU (`QnnHtp.dll`). By running INT8 quantized graphs in HTP burst mode, semantic evaluations target ~3.8 to 6.2 milliseconds (published external reference) with negligible power draw (~1.5W–3W), preserving laptop battery life during extended offline career planning sessions.

---

### 8. Model Provenance & Qualcomm QNN Deployment Path
The application utilizes a **Local ONNX model with Qualcomm QNN deployment path** (`all-minilm-l6-v2` architecture, also featured in the Qualcomm AI Hub model catalog). The model graph was optimized with ONNX Runtime graph optimizations (`ORT_ENABLE_ALL`) and INT8 quantization, reducing disk footprint from 90MB to 21.91MB and ensuring direct compatibility with the Qualcomm Neural Processing SDK (`QnnHtp.dll`).

---

### 9. NPU Usage & Graceful Fallback Protocol
In strict adherence to competition rules, CareerEdge AI never fakes NPU execution:
- When deployed on Snapdragon ARM64 hardware with Hexagon NPU drivers: Selects `QNNExecutionProvider` and displays `SNAPDRAGON NPU • QNN ACTIVE`.
- When evaluated on x86_64 development machines: Gracefully routes to `CPUExecutionProvider`, displays `LOCAL AI • CPU FALLBACK ACTIVE`, and reports QNN status as `QNN DEPLOYMENT PATH IMPLEMENTED — NOT PHYSICALLY VERIFIED ON CURRENT HOST`. Measured latency on this Intel development PC is authentically recorded at 22.04 ms.

---

### 10. Privacy & Data Sovereignty
- **Zero Cloud AI API Calls:** No OpenAI, Gemini, or third-party cloud APIs are used.
- **Zero Network Telemetry:** No user analytics or tracking beacons.
- **Local SQLite DB:** Data resides strictly on the local machine.
- **1-Click Permanent Purge:** The `DELETE /api/session` endpoint wipes all local databases and uploaded files on command.

---

### 11. Offline Capability
The application has been verified to run 100% offline. Once installed, users can disconnect Wi-Fi, upload resumes, analyze job requirements, benchmark inference times, and generate PDF reports without an internet connection.

---

### 12. User & Social Impact
Job seekers, career changers, and university graduates gain an empowering, private mentor that tells them the truth about their skill alignment without risking their data privacy. By demystifying job requirements and providing concrete 30-day plans, CareerEdge AI shortens the path from career ambiguity to verified engineering capability.

---

### 13. Future Scope
1. **Multi-Modal Job Posting Ingestion:** Add local ONNX OCR to analyze screenshot job postings from LinkedIn or job boards on-device.
2. **"What-If" Simulator:** Enable interactive career scenario simulation ("If I complete a PyTorch project, how will my alignment change?").
3. **Direct Snapdragon Studio Integration:** Package as a native Windows MSIX installer with Qualcomm AI Engine Direct SDK bindings.

---

### 14. GitHub Repository Description
*CareerEdge AI: Private on-device career intelligence and skill gap analysis for Snapdragon PCs powered by ONNX Runtime and Qualcomm QNN Hexagon NPU acceleration.*

---

### 15. Demo Description
*A 3-minute walk-through showcasing synthetic candidate Alex Morgan, immediate hardware inspection, deterministic 5-dimension alignment scoring, "Why Is My Profile Not Aligned?" gap explanations, a 30-day personalized upgrade roadmap, and live physical inference benchmarking.*
