"""
Integration tests for complete CareerEdge AI workflow.
Resume -> Job Matching -> Skill Gap Analysis -> 30-Day Roadmap -> PDF Export -> Session Purge.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_complete_integration_pipeline():
    # 1. Health check
    r_health = client.get("/api/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "healthy"

    # 2. Hardware runtime status check
    r_device = client.get("/api/device")
    assert r_device.status_code == 200
    assert "status_label" in r_device.json()

    # 3. Load synthetic demo data
    r_demo = client.get("/api/demo/load")
    assert r_demo.status_code == 200
    demo = r_demo.json()
    assert demo["candidate"] == "Alex Morgan [DEMO DATA]"
    assert 0 <= demo["match"]["overall_alignment"] <= 100
    assert len(demo["gaps"]["gaps"]) >= 1
    assert len(demo["roadmap"]["weeks"]) == 4

    # 4. Generate PDF report
    r_pdf = client.post("/api/export/pdf", json={})
    assert r_pdf.status_code == 200
    assert r_pdf.headers["content-type"] == "application/pdf"
    assert len(r_pdf.content) > 1000

    # 5. Clear session & privacy purge
    r_purge = client.delete("/api/session")
    assert r_purge.status_code == 200
    assert r_purge.json()["zero_retention_guaranteed"] is True
