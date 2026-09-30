"""
CareerEdge AI - Deterministic Profile Alignment Scoring Engine
Implements the transparent, explainable formula documented in docs/scoring_methodology.md.
Never hallucinates arbitrary scores; calculated mathematically from weights and evidence.
"""

from typing import Dict, List, Any
from backend.models.schemas import AlignmentScoreBreakdown

# Documented transparent weights:
# Technical Skills: 40%
# Projects:         25%
# Experience:       15%
# Education:        10%
# Domain:           10%
DEFAULT_WEIGHTS = {
    "technical_skills": 0.40,
    "projects": 0.25,
    "experience": 0.15,
    "education": 0.10,
    "domain": 0.10,
}


def calculate_alignment_score(
    skills_score: float,
    projects_score: float,
    experience_score: float,
    education_score: float,
    domain_score: float,
    weights: Dict[str, float] = DEFAULT_WEIGHTS,
) -> Dict[str, Any]:
    """
    Computes the deterministic Overall Alignment score (0-100) and component breakdown.
    Each component is clamped strictly between 0 and 100.
    """
    s_clamped = max(0.0, min(100.0, float(skills_score)))
    p_clamped = max(0.0, min(100.0, float(projects_score)))
    exp_clamped = max(0.0, min(100.0, float(experience_score)))
    edu_clamped = max(0.0, min(100.0, float(education_score)))
    dom_clamped = max(0.0, min(100.0, float(domain_score)))

    overall = (
        s_clamped * weights["technical_skills"]
        + p_clamped * weights["projects"]
        + exp_clamped * weights["experience"]
        + edu_clamped * weights["education"]
        + dom_clamped * weights["domain"]
    )

    breakdown = AlignmentScoreBreakdown(
        technical_skills=int(round(s_clamped)),
        projects=int(round(p_clamped)),
        experience=int(round(exp_clamped)),
        education=int(round(edu_clamped)),
        domain=int(round(dom_clamped)),
    )

    return {
        "overall_alignment": int(round(overall)),
        "score_breakdown": breakdown,
        "weights_used": weights,
    }
