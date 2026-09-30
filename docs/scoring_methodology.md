# CareerEdge AI — Profile-to-Role Alignment Scoring Methodology
**Document Version:** 1.0.0  
**Target Competition:** Snapdragon® AI Lab Build & Present Challenge by Qualcomm  
**Standard:** 100% Deterministic, Explainable, Non-Arbitrary

---

## 1. Ethical & Responsible AI Scope
CareerEdge AI computes a **Profile-to-Role Skill Alignment Score**, which quantifies how closely a candidate's uploaded resume matches the stated requirements of a target job description.

> **CRITICAL DISCLAIMER:**  
> The Alignment Score is **NOT** a hiring probability, interview selection prediction, or applicant tracking system (ATS) pass/fail gate. It is an educational and diagnostic tool designed to help the user identify concrete skill gaps and guide their 30-day self-improvement roadmap.

---

## 2. Core Scoring Formula

The overall alignment score $S_{\text{overall}}$ is a deterministic, bounded value in the interval $[0, 100]$, computed as a weighted sum of five orthogonal dimensions:

$$S_{\text{overall}} = w_{\text{tech}} \cdot S_{\text{tech}} + w_{\text{proj}} \cdot S_{\text{proj}} + w_{\text{exp}} \cdot S_{\text{exp}} + w_{\text{edu}} \cdot S_{\text{edu}} + w_{\text{dom}} \cdot S_{\text{dom}}$$

Where the standard component weights are:

| Component | Symbol | Default Weight | Description |
| :--- | :---: | :---: | :--- |
| **Technical Skills** | $w_{\text{tech}}$ | **40%** ($0.40$) | Direct, normalized, and semantically bridged skill match |
| **Projects Evidence** | $w_{\text{proj}}$ | **25%** ($0.25$) | Verified application of target technologies in project portfolios |
| **Work Experience** | $w_{\text{exp}}$ | **15%** ($0.15$) | Professional roles, tenure, and responsibility alignment |
| **Education** | $w_{\text{edu}}$ | **10%** ($0.10$) | Degree level and engineering discipline relevance |
| **Domain Centrality** | $w_{\text{dom}}$ | **10%** ($0.10$) | High-level domain match (e.g. Edge AI, MLOps, Data Engineering) |
| **Total** | $\sum w$ | **100%** ($1.00$) | Strictly normalized |

---

## 3. Component Score Formulations

### A. Technical Skills Alignment ($S_{\text{tech}}$)
Each requirement $r_i \in R$ extracted from the job description is classified into one of three distinct match categories:
1. **Strong Match ($M_{\text{strong}} = 1.0$):**
   - Exact canonical skill match found in resume AND verified evidence in project or experience sections.
2. **Partial Match ($M_{\text{partial}} = 0.5$):**
   - Skill listed in resume skills section but lacking deep project evidence, OR
   - High semantic embedding similarity ($\ge 0.72$ via ONNX embedding model) with a related skill (e.g., candidate has TensorFlow, job requires PyTorch).
3. **Missing ($M_{\text{missing}} = 0.0$):**
   - No lexical, alias, or related semantic evidence detected in resume.

Requirements are partitioned into **Required** ($R_{\text{req}}$, weight $2.0$) and **Preferred** ($R_{\text{pref}}$, weight $1.0$):

$$S_{\text{tech}} = \frac{\sum_{r \in R_{\text{req}}} 2.0 \cdot M(r) + \sum_{r \in R_{\text{pref}}} 1.0 \cdot M(r)}{2.0 \cdot |R_{\text{req}}| + 1.0 \cdot |R_{\text{pref}}|} \times 100$$

### B. Project Portfolio Evidence ($S_{\text{proj}}$)
Evaluates whether required skills are actively implemented in tangible projects:
- Percentage of top required skills with explicit project evidence.
- Baseline bonus if projects demonstrate measurable engineering metrics (e.g., latency, throughput, accuracy).

### C. Experience Alignment ($S_{\text{exp}}$)
Compares stated target seniority (e.g., Junior, Mid, Senior, 3+ years) against detected candidate experience roles and duration.

### D. Education Alignment ($S_{\text{edu}}$)
Compares candidate degree level (Bachelor's, Master's, Ph.D.) and discipline (Computer Science, Data Science, Electrical Engineering) with job education criteria.

### E. Domain Centrality ($S_{\text{dom}}$)
Computes cosine similarity between candidate resume summary embeddings and target job domain profile embeddings using the local ONNX embedding engine.

---

## 4. Transparency & Reproducibility Guarantee
- **No Hidden Arbitrary Points:** The score is calculated strictly by the code in [`backend/engine/scoring.py`](file:///C:/Users/evara/.gemini/antigravity-ide/scratch/CareerEdge-AI/backend/engine/scoring.py).
- **Auditability:** Every skill requirement in the output displays its exact status (`Strong`, `Partial`, or `Missing`), the exact resume text evidence found, and why that classification was assigned.
