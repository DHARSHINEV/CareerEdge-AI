# CareerEdge AI — Architecture Specification
**Target Platform:** Snapdragon-Powered Windows PCs (Qualcomm Hexagon NPU) with CPU Fallback  
**Framework:** React + TypeScript (Vite) + FastAPI + ONNX Runtime (QNN Execution Provider)  
**Privacy Class:** 100% On-Device / Zero Cloud Telemetry

---

## 1. High-Level Architecture Overview

CareerEdge AI is structured as a privacy-first, on-device career intelligence copilot. All document extraction, semantic embedding generation, skill ontology mapping, and roadmap synthesis occur strictly within the user's local operating system.

```
+-----------------------------------------------------------------------------------+
|                                 USER INTERFACE                                    |
|              React 18 + TypeScript + Vite + High-Tech Snapdragon Dark UI          |
|                                                                                   |
|  - Real-time Hardware Diagnostic Pill (NPU vs CPU Fallback Status)               |
|  - Profile Alignment Score Breakdown (40% Tech / 25% Proj / 15% Exp / 10% Edu)    |
|  - "Why Is My Profile Not Aligned?" Deep Dive Explainer                           |
|  - 30-Day Personalized Career Upgrade Roadmap (Days 1–30 with Deliverables)       |
|  - Project Recommendation Engine (Portfolio Blueprints)                           |
|  - Resume Bullet Improver (Honest metrics with [insert metric] placeholders)      |
|  - Live Hardware Benchmark Suite & Snapdragon Reference Comparison               |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST (Localhost)
                                           v
+-----------------------------------------------------------------------------------+
|                             BACKEND APPLICATION SERVER                           |
|                       FastAPI + Pydantic v2 + SQLite Local Storage                |
|                                                                                   |
|  [REST API Handlers]                                                              |
|   /api/health            /api/device         /api/resume/upload                   |
|   /api/job/analyze       /api/match          /api/gap-analysis                    |
|   /api/roadmap           /api/project        /api/export/pdf                      |
|                                                                                   |
|  [Services & Business Logic]                                                      |
|   - DocumentReader: Safe PDF, DOCX, TXT byte parsing                              |
|   - ResumeParser & ResumeQualityAnalyzer: Structural audit & metric extraction   |
|   - JobParser & SkillOntology: Technical normalization & alias resolution         |
|   - SemanticJobMatcher & Deterministic Scoring: Explainable alignment scoring   |
|   - GapExplainer & RoadmapGenerator: Milestone & daily task synthesis             |
|   - LocalDatabase: SQLite session & benchmark history with 1-click privacy wipe   |
|   - CareerReportExporter: ReportLab client-side PDF document compiler            |
+------------------------------------------+----------------------------------------+
                                           | In-Process AI Abstraction
                                           v
+-----------------------------------------------------------------------------------+
|                             LOCAL AI INFERENCE ENGINE                             |
|                        AIEngine Unified Abstraction Layer                         |
|                                                                                   |
|           +------------------------------------------------------------+          |
|           | LocalEmbeddingEngine (all-MiniLM-L6-v2 Quantized ONNX)    |          |
|           | WordPiece Tokenizer -> Mean Pooling -> L2 Normalization   |          |
|           +-----------------------------+------------------------------+          |
|                                         |                                         |
|                     +-------------------+-------------------+                     |
|                     v                                       v                     |
|        [Mode A: Snapdragon PC]                    [Mode B: CPU Fallback]          |
|         QNNExecutionProvider                       CPUExecutionProvider           |
|        Qualcomm Hexagon NPU (HTP)                 Host CPU Multi-threading        |
|        ~3.8 - 6.2 ms Latency                      ~75 ms Latency                  |
|        Ultra-low ~2W NPU Envelope                 Standard x86 TDP                |
+-----------------------------------------------------------------------------------+
```

---

## 2. The AI Inference & Embedding Pipeline

1. **Document Understanding:**
   - User inputs resume via PDF, DOCX, or raw text.
   - Text is cleaned, segmented into sections (Education, Experience, Projects, Skills), and matched against the `SkillOntology` graph.

2. **Semantic Representation:**
   - Raw requirement strings and resume experience contexts are tokenized via local HuggingFace `Tokenizer` (`tokenizer.json`).
   - The tokenized IDs are fed into the quantized `all-MiniLM-L6-v2` ONNX model.

3. **Hardware Dispatch:**
   - `QNNRuntimeManager` inspects available providers via `ort.get_available_providers()`.
   - On Snapdragon X Elite/Plus PCs: Configures `QNNExecutionProvider` with HTP performance mode set to `burst` and FP16/INT8 precision.
   - On x86_64 Development PCs: Binds `CPUExecutionProvider` with graph optimization `ORT_ENABLE_ALL` and 4 intra-op threads.

4. **Vector Pooling & Cosine Similarity:**
   - Token vectors undergo attention-masked mean pooling and unit L2 normalization:
     $$\vec{v} = \frac{\sum_{i} m_i \vec{h}_i}{\|\sum_{i} m_i \vec{h}_i\|_2}$$
   - Cosine similarity between requirements and candidate evidence is computed via dot-product:
     $$\text{sim}(\vec{r}, \vec{c}) = \frac{\vec{r} \cdot \vec{c} + 1.0}{2.0}$$

---

## 3. Explainability & Transparent Formula

CareerEdge AI guarantees that **no hiring probability or arbitrary ATS score is hallucinated**.
Alignment is calculated deterministically:

$$S_{\text{overall}} = 0.40 \cdot S_{\text{tech}} + 0.25 \cdot S_{\text{proj}} + 0.15 \cdot S_{\text{exp}} + 0.10 \cdot S_{\text{edu}} + 0.10 \cdot S_{\text{dom}}$$

Every requirement is individually audited and presented in the UI with:
- **Requirement Name & Category**
- **Match Status:** `Strong Match`, `Partial Match`, or `Missing`
- **Resume Evidence:** Exact verified quote or note explaining why evidence was incomplete
- **Semantic Similarity Percentage**
- **Actionable Recommendation:** Concrete step to close the gap

---

## 4. Privacy & Zero-Retention Security Architecture

- **Local File Processing:** Documents are processed in-memory.
- **Local SQLite DB:** Database is located at `backend/database/careeredge.db`.
- **1-Click Privacy Wipe:** `DELETE /api/session` permanently deletes all resumes, jobs, match analyses, and roadmaps from disk.
- **Offline Capable:** Verified offline operation with zero external network calls.
