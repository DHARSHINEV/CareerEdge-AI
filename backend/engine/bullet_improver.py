"""
CareerEdge AI - Resume Bullet Improvement Assistant
Transforms passive, generic resume bullet points into strong, action-oriented,
technically precise engineering statements without hallucinating false metrics.
Uses explicit placeholders like [insert measured latency/speedup] where data is needed.
"""

import re
from typing import List, Dict, Any
from backend.models.schemas import (
    BulletImprovementItem,
    ResumeImprovementResponse,
)

# Common weak verbs and their strong engineering alternatives
ACTION_VERB_MAP = {
    "worked on": ["Architected and implemented", "Engineered", "Developed end-to-end"],
    "helped with": ["Collaborated on engineering", "Contributed core modules to", "Spearheaded the integration of"],
    "responsible for": ["Led development of", "Maintained and optimized", "Orchestrated"],
    "did": ["Implemented", "Executed", "Constructed"],
    "made": ["Designed and deployed", "Authored", "Programmed"],
    "used": ["Leveraged", "Integrated", "Utilized"],
    "handled": ["Administered", "Streamlined", "Resolved"],
}


class ResumeBulletImprover:
    """
    Identifies weak or vague bullet points in resume projects/experience and
    generates structured improvements following the formula:
    [Action Verb] + [Specific Problem/Feature] + [Technologies Used] + [Measurable Outcome Placeholder]
    """

    def improve_bullets(
        self,
        parsed_resume: Dict[str, Any],
        target_role: str = "Machine Learning Engineer",
    ) -> ResumeImprovementResponse:
        projects = parsed_resume.get("projects", [])
        experience = parsed_resume.get("experience", [])

        candidate_bullets: List[str] = []

        # Collect bullet points from projects
        for p in projects:
            desc = p.get("description", "")
            for line in desc.split("."):
                line_clean = line.strip("• -* \t\n")
                if 15 < len(line_clean) < 140:
                    candidate_bullets.append(line_clean)

        # Collect bullet points from experience
        for exp in experience:
            for resp in exp.get("responsibilities", []):
                resp_clean = resp.strip("• -* \t\n")
                if 15 < len(resp_clean) < 140:
                    candidate_bullets.append(resp_clean)

        # Default fallback sample bullets if resume has very short entries
        if not candidate_bullets:
            candidate_bullets = [
                "Worked on machine learning project for classification.",
                "Helped team with building FastAPI backend and testing.",
                "Used Docker for running containers in development.",
            ]

        improvements: List[BulletImprovementItem] = []

        for bullet in candidate_bullets[:5]:
            improved, critique, strength = self._transform_bullet(bullet, target_role)
            improvements.append(
                BulletImprovementItem(
                    original_bullet=bullet,
                    improved_bullet=improved,
                    critique=critique,
                    added_strength=strength,
                )
            )

        return ResumeImprovementResponse(improvements=improvements)

    def _transform_bullet(self, original: str, target_role: str) -> tuple[str, str, str]:
        lower = original.lower()

        # Check if already has a metric
        has_metric = bool(re.search(r"\b(\d+%\b|\$\d+|\b\d+x\b|\b\d+\s*ms\b)", lower))

        # Check weak verb
        matched_weak = None
        for weak in ACTION_VERB_MAP:
            if weak in lower:
                matched_weak = weak
                break

        if matched_weak:
            strong_verb = ACTION_VERB_MAP[matched_weak][0]
            # Replace weak verb
            subbed = re.sub(re.escape(matched_weak), strong_verb, original, flags=re.IGNORECASE, count=1)
            if not has_metric:
                improved = f"{subbed}, achieving [insert measured outcome, e.g., 28% latency reduction or 99.2% test coverage]."
                critique = f"Replaced passive phrase '{matched_weak}' with strong action verb and added outcome placeholder."
                strength = "Converts passive participation into direct engineering leadership and highlights quantifiable value."
            else:
                improved = subbed
                critique = f"Upgraded passive verb '{matched_weak}' to dynamic engineering action verb."
                strength = "Clearer ownership and direct technical impact."
            return improved, critique, strength

        # If lacks metric
        if not has_metric:
            improved = f"{original.rstrip('.')}, optimizing workflow efficiency and resulting in [insert measured speedup or outcome, e.g. 35% faster throughput]."
            critique = "Original bullet described a task without demonstrating business impact or measurable result."
            strength = "Grounds technical execution in an explicit, quantifiable engineering outcome."
            return improved, critique, strength

        # If already quite strong, polish phrasing
        improved = f"Engineered and deployed: {original.rstrip('.')} with automated validation."
        critique = "Enhanced technical clarity and emphasized deployment readiness."
        strength = "Demonstrates production readiness for modern engineering roles."
        return improved, critique, strength


# Singleton instance
_bullet_improver = None


def get_bullet_improver() -> ResumeBulletImprover:
    global _bullet_improver
    if _bullet_improver is None:
        _bullet_improver = ResumeBulletImprover()
    return _bullet_improver
