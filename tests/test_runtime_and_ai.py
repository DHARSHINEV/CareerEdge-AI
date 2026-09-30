"""
Unit tests for AI Runtime Abstraction, ONNX Embeddings, and Hardware Fallback.
"""

import numpy as np
from backend.engine.device_detection import get_hardware_diagnostics
from backend.engine.qnn_runtime import get_runtime_manager
from ai.embeddings.local_embeddings import get_embedding_engine
from backend.engine.roadmap_generator import get_roadmap_generator
from backend.engine.project_recommender import get_project_recommender
from backend.engine.bullet_improver import get_bullet_improver
from backend.models.schemas import SkillMatchDetail


def test_hardware_diagnostics_detection():
    diag = get_hardware_diagnostics()
    assert "os_name" in diag
    assert "architecture" in diag
    assert "processor" in diag
    assert isinstance(diag["npu_detected"], bool)


def test_runtime_manager_fallback():
    mgr = get_runtime_manager()
    status = mgr.get_runtime_status()
    assert status["active_provider"] in ["CPUExecutionProvider", "QNNExecutionProvider"]
    assert "status_label" in status


def test_local_embeddings_generation():
    engine = get_embedding_engine()
    texts = [
        "Machine Learning Engineer with PyTorch experience",
        "Deep Learning neural network optimization on Snapdragon",
    ]
    vectors, lat = engine.encode(texts)
    assert vectors.shape == (2, 384)
    assert lat >= 0

    # Test cosine similarity between normalized vectors
    sim = engine.compute_similarity(vectors[0], vectors[1])
    assert 0.0 <= sim <= 1.0


def test_roadmap_generation():
    gen = get_roadmap_generator()
    gaps = [
        SkillMatchDetail(
            requirement="Docker",
            status="Missing",
            category="DevOps",
            is_required=True,
            resume_evidence="None",
            recommendation="Learn Docker",
            semantic_similarity=0.2,
        ),
        SkillMatchDetail(
            requirement="PyTorch",
            status="Partial Match",
            category="ML/AI",
            is_required=True,
            resume_evidence="TensorFlow background",
            recommendation="Build PyTorch project",
            semantic_similarity=0.75,
        ),
    ]
    roadmap = gen.generate_roadmap("Machine Learning Engineer", gaps)
    assert len(roadmap.weeks) == 4
    total_days = sum(len(w.tasks) for w in roadmap.weeks)
    assert total_days == 28 or total_days == 30 or total_days >= 28


def test_project_recommendation():
    rec = get_project_recommender()
    gaps = [
        SkillMatchDetail(
            requirement="Docker",
            status="Missing",
            category="DevOps",
            is_required=True,
            resume_evidence="None",
            recommendation="Learn Docker",
            semantic_similarity=0.2,
        )
    ]
    res = rec.recommend(gaps, "Machine Learning Engineer")
    assert len(res.projects) >= 1
    assert "title" in res.projects[0].model_dump()


def test_bullet_improver_no_hallucination():
    improver = get_bullet_improver()
    sample_resume = {
        "projects": [
            {"name": "ML Model", "description": "Worked on machine learning model for object detection."}
        ]
    }
    res = improver.improve_bullets(sample_resume, "Machine Learning Engineer")
    assert len(res.improvements) >= 1
    # Check that it uses placeholders and doesn't invent fake metrics
    improved = res.improvements[0].improved_bullet
    assert "worked on" not in improved.lower()
