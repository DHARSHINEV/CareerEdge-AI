"""
CareerEdge AI - Resume Completeness & Quality Scoring Service
Evaluates structural completeness, technical density, measurable impact,
project descriptions, and highlights actionable weaknesses without hallucination.
"""

import re
import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger("careeredge.resume_analyzer")

GENERIC_PHRASES = [
    "hard worker",
    "team player",
    "quick learner",
    "passionate",
    "worked on",
    "responsible for",
    "helped with",
    "assisted in",
    "good communication",
    "detail-oriented",
]


class ResumeQualityAnalyzer:
    """
    Computes a deterministic Resume Completeness Score (0-100) and
    produces explainable critique on weak projects, lack of metrics, and generic text.
    """

    def analyze(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = parsed_resume.get("raw_text", "")
        skills = parsed_resume.get("technical_skills", {})
        projects = parsed_resume.get("projects", [])
        experience = parsed_resume.get("experience", [])
        education = parsed_resume.get("education", [])

        total_skills_count = sum(len(v) for v in skills.values())

        # 1. Structural Completeness (Weight: 25%)
        # Education (5), Contact (5), Skills (5), Projects (5), Experience (5)
        structure_score = 0
        if education:
            structure_score += 5
        if parsed_resume.get("email") or parsed_resume.get("contact"):
            structure_score += 5
        if total_skills_count >= 5:
            structure_score += 5
        if len(projects) >= 2:
            structure_score += 5
        if len(experience) >= 1:
            structure_score += 5

        # 2. Measurable Impact & Quantifiable Results (Weight: 25%)
        metric_pattern = re.compile(
            r"\b(\d+%\b|\$\d+|\b\d+x\b|\b\d+\s*ms\b|\b\d+\s*users\b|\b\d+\s*requests\b|\baccuracy\b|\blatency\b|\bthroughput\b)",
            re.IGNORECASE,
        )
        metric_matches = metric_pattern.findall(raw_text)
        impact_score = min(25, len(metric_matches) * 5)

        # 3. Project Depth & Evidence Quality (Weight: 25%)
        project_score = 0
        for p in projects:
            p_desc = p.get("description", "")
            p_techs = p.get("technologies", [])
            if len(p_techs) >= 2 and len(p_desc.split()) >= 15:
                project_score += 8
        project_score = min(25, project_score)

        # 4. Technical Keyword Density & Ontology Coverage (Weight: 25%)
        keyword_score = min(25, int((total_skills_count / 15.0) * 25))

        completeness_score = int(structure_score + impact_score + project_score + keyword_score)
        completeness_score = max(20, min(100, completeness_score))

        # Actionable Critiques & Weakness Detection
        improvement_areas = []

        # Check measurable metrics
        if len(metric_matches) < 2:
            improvement_areas.append(
                "Missing measurable impact: Resume lacks quantified achievements (e.g. '% latency reduction', 'X requests/sec', 'model accuracy gain')."
            )

        # Check weak project descriptions
        weak_projects = []
        for p in projects:
            desc = p.get("description", "")
            techs = p.get("technologies", [])
            if len(desc.split()) < 15 or len(techs) == 0:
                weak_projects.append(p.get("name", "Project"))
        if weak_projects:
            improvement_areas.append(
                f"Weak project descriptions in: [{', '.join(weak_projects)}]. Detail the specific engineering problem, architecture, and measurable outcome."
            )

        # Check generic phrases
        found_generic = [p for p in GENERIC_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", raw_text.lower())]
        if found_generic:
            improvement_areas.append(
                f"Generic phrasing detected ({', '.join(found_generic[:3])}). Replace passive phrases with active engineering verbs (e.g., 'Engineered', 'Optimized', 'Architected')."
            )

        # Check technical skills evidence correlation
        for cat, cat_skills in skills.items():
            if cat in ["ML/AI", "Cloud", "DevOps"]:
                for s in cat_skills:
                    # check if skill is in projects
                    in_project = any(s.lower() in p.get("description", "").lower() or s in p.get("technologies", []) for p in projects)
                    if not in_project and len(projects) > 0:
                        improvement_areas.append(
                            f"Skill '{s}' is listed in skills inventory but does not appear in any project description. Add a project demonstrating production or experimental use."
                        )
                        break

        if not improvement_areas:
            improvement_areas.append("Strong technical alignment and quantified project outcomes demonstrated.")

        quality_breakdown = {
            "Structural Integrity": int((structure_score / 25.0) * 100),
            "Measurable Impact": int((impact_score / 25.0) * 100),
            "Project Engineering Depth": int((project_score / 25.0) * 100),
            "Technical Vocabulary Density": int((keyword_score / 25.0) * 100),
        }

        return {
            "completeness_score": completeness_score,
            "quality_breakdown": quality_breakdown,
            "improvement_areas": improvement_areas[:5],
            "metric_count": len(metric_matches),
            "total_skills_extracted": total_skills_count,
        }


# Singleton instance
_quality_analyzer: Optional[ResumeQualityAnalyzer] = None


def get_resume_quality_analyzer() -> ResumeQualityAnalyzer:
    global _quality_analyzer
    if _quality_analyzer is None:
        _quality_analyzer = ResumeQualityAnalyzer()
    return _quality_analyzer
