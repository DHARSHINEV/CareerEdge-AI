# CareerEdge AI — Responsible AI & Ethics Framework
**Application:** CareerEdge AI (Private On-Device Career Intelligence)  
**Standard:** Ethical AI Guidelines for Snapdragon® AI Lab Challenge 2026

---

## 1. System Mission & Core Purpose
CareerEdge AI is designed exclusively as an **educational self-diagnostic tool for career candidates and students**. Its sole objective is to help individuals:
1. Privately inspect how their declared skills match against a job description.
2. Identify concrete skill gaps they can proactively improve.
3. Generate a structured 30-day self-directed learning plan.

---

## 2. Explicit Non-Goals & System Boundaries

CareerEdge AI explicitly **DOES NOT**:
- **Predict hiring outcomes:** It does NOT estimate the probability of receiving an interview, offer, or job.
- **Act as an Applicant Tracking System (ATS):** It does NOT rank or filter candidates for employers or recruiters.
- **Make automated decisions:** It is NOT an automated employment decision tool (AEDT).
- **Infer protected characteristics:** It does NOT detect, extract, or evaluate race, gender, ethnicity, disability, age, sexual orientation, religion, or nationality.
- **Guarantee employment:** Completing the recommended 30-day roadmap or projects does NOT guarantee job placement.

---

## 3. Critical Limitations & Risk Mitigations

### A. Limitations of Resume Parsing & Document Understanding
- **Incomplete or Non-Standard Resumes:** Resumes with unconventional layouts, multi-column designs, or graphical text may have missed or misidentified sections.
- **Mitigation:** The application includes a manual raw-text editor allowing users to review and modify extracted text directly.

### B. False Positives & False Negatives in Semantic Matching
- **Polysemy & Tech Terminology:** Keywords like "Go", "C", or "React" can be ambiguous in natural language.
- **Mitigation:** The `SkillOntology` uses strict word boundary checks, case-sensitive context rules, and alias normalization to prevent false matches.

### C. Bias Risks & Semantic Drift
- **Pretrained Embedding Biases:** Language models can exhibit subtle biases inherited from web training corpora.
- **Mitigation:** Matching uses deterministic ontological rules for skill presence combined with cosine similarity strictly on technical descriptions. Demographics and personal identifiers are completely excluded from the matching vector space.

### D. Prohibition on Metric Fabrication
- **No Hallucinated Experience:** When optimizing resume bullet points, CareerEdge AI **never** invents numbers, percentages, or achievements. It provides explicit placeholders (`[insert measured latency/speedup]`) requiring the candidate to supply truthful, verified metrics.

---

## 4. Human Decision Responsibility
All career decisions, resume edits, and job applications remain the full responsibility of the human user. CareerEdge AI acts as an explainable, on-device assistant to empower candidates with transparent feedback.
