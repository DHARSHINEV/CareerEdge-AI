"""
CareerEdge AI - Robustness, Edge Case, and Input Validation Tests
Verifies error handling for empty resumes, malformed documents, unsupported file formats,
empty jobs, long inputs, and privacy purge mechanics.
"""

from fastapi.testclient import TestClient
from backend.main import app
from backend.database.database import get_local_db

client = TestClient(app)


def test_empty_resume_text():
    res = client.post("/api/resume/analyze", json={"resume_text": ""})
    assert res.status_code == 400
    assert "cannot be empty" in res.json()["detail"].lower()


def test_whitespace_only_resume():
    res = client.post("/api/resume/analyze", json={"resume_text": "   \n\t  "})
    assert res.status_code == 400
    assert "cannot be empty" in res.json()["detail"].lower()


def test_empty_job_text():
    res = client.post("/api/job/analyze", json={"job_text": ""})
    assert res.status_code == 400
    assert "cannot be empty" in res.json()["detail"].lower()


def test_unsupported_file_upload():
    fake_exe = b"MZ\x90\x00\x03\x00\x00\x00"
    res = client.post(
        "/api/resume/upload",
        files={"file": ("malicious.exe", fake_exe, "application/octet-stream")},
    )
    assert res.status_code == 400
    assert "unsupported file format" in res.json()["detail"].lower()


def test_corrupted_pdf_upload():
    corrupted_bytes = b"%PDF-1.4\ncorrupted random bytes that do not form a valid pdf object"
    res = client.post(
        "/api/resume/upload",
        files={"file": ("broken.pdf", corrupted_bytes, "application/pdf")},
    )
    assert res.status_code == 400
    assert "failed to extract text" in res.json()["detail"].lower() or "no selectable text" in res.json()["detail"].lower()


def test_very_long_input_handling():
    # 50,000 words of technical text
    long_text = "Python PyTorch Machine Learning Docker AWS SQL " * 10000
    res = client.post("/api/resume/analyze", json={"resume_text": long_text})
    assert res.status_code == 200
    data = res.json()
    assert data["completeness_score"] > 0
    assert "Python" in data["technical_skills"].get("Programming", [])


def test_privacy_purge_verifiability():
    # 1. Load demo data into database
    client.get("/api/demo/load")
    db = get_local_db()
    assert db.get_latest_resume() is not None
    assert db.get_latest_job() is not None

    # 2. Trigger privacy wipe
    res = client.delete("/api/session")
    assert res.status_code == 200
    assert res.json()["zero_retention_guaranteed"] is True

    # 3. Verify SQLite tables are completely empty
    assert db.get_latest_resume() is None
    assert db.get_latest_job() is None
