"""
Unit tests for deterministic Profile Alignment Scoring Engine.
"""

from backend.engine.scoring import calculate_alignment_score, DEFAULT_WEIGHTS


def test_scoring_weights_sum_to_one():
    total_weight = sum(DEFAULT_WEIGHTS.values())
    assert abs(total_weight - 1.0) < 1e-6


def test_scoring_perfect_alignment():
    res = calculate_alignment_score(100, 100, 100, 100, 100)
    assert res["overall_alignment"] == 100
    assert res["score_breakdown"].technical_skills == 100
    assert res["score_breakdown"].projects == 100
    assert res["score_breakdown"].experience == 100
    assert res["score_breakdown"].education == 100
    assert res["score_breakdown"].domain == 100


def test_scoring_zero_alignment():
    res = calculate_alignment_score(0, 0, 0, 0, 0)
    assert res["overall_alignment"] == 0


def test_scoring_boundary_clamping():
    # Negative inputs should clamp to 0, excessive inputs should clamp to 100
    res = calculate_alignment_score(-50, 150, 50, 50, 50)
    assert 0 <= res["overall_alignment"] <= 100
    assert res["score_breakdown"].technical_skills == 0
    assert res["score_breakdown"].projects == 100


def test_scoring_formula_exact_value():
    # 40% tech, 25% proj, 15% exp, 10% edu, 10% dom
    # 80*0.4 + 70*0.25 + 60*0.15 + 100*0.10 + 50*0.10
    # = 32 + 17.5 + 9.0 + 10 + 5.0 = 73.5 -> 74
    res = calculate_alignment_score(
        skills_score=80,
        projects_score=70,
        experience_score=60,
        education_score=100,
        domain_score=50,
    )
    assert res["overall_alignment"] == 74
