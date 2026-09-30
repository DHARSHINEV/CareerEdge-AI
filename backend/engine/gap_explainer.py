"""
CareerEdge AI - "Why Is My Profile Not Aligned?" Gap Explainer Engine
Provides deep, actionable, explainable breakdowns of missing skills,
detailing why each gap matters, what evidence is missing, what concepts to learn,
and how to demonstrate competence to recruiters.
"""

from typing import Dict, Any, List
from backend.models.schemas import GapAnalysisResponse, GapDetail, MatchAnalysisResponse
from ai.runtime.ai_engine import get_ai_engine
from backend.services.skill_ontology import get_skill_ontology


class GapExplainerEngine:
    """
    Synthesizes actionable gap explanations grounded in resume evidence and target job context.
    """

    def __init__(self):
        self.ai_engine = get_ai_engine()
        self.ontology = get_skill_ontology()

    def explain_gaps(
        self,
        match_result: MatchAnalysisResponse,
        parsed_resume: Dict[str, Any],
        parsed_job: Dict[str, Any],
    ) -> GapAnalysisResponse:
        target_role = match_result.target_role
        alignment = match_result.overall_alignment
        critical_gaps = match_result.top_critical_gaps

        resume_skills_dict = parsed_resume.get("technical_skills", {})
        all_resume_skills = set()
        for cat_skills in resume_skills_dict.values():
            for s in cat_skills:
                all_resume_skills.add(s.lower())

        gap_details: List[GapDetail] = []

        for item in critical_gaps:
            skill = item.requirement
            category = item.category
            is_req = item.is_required

            # Find related skills candidate actually possesses
            related = [
                r for r in self.ontology.get_related(skill)
                if r.lower() in all_resume_skills
            ]

            explanation = self.ai_engine.generation_engine.explain_gap(
                skill=skill,
                category=category,
                target_role=target_role,
                is_required=is_req,
                related_skills=related,
            )

            gap_details.append(
                GapDetail(
                    skill=explanation["skill"],
                    category=explanation["category"],
                    importance=explanation["importance"],
                    why_it_matters=explanation["why_it_matters"],
                    evidence_missing=explanation["evidence_missing"],
                    what_to_learn=explanation["what_to_learn"],
                    recommended_project=explanation["recommended_project"],
                    resume_demonstration_guide=explanation["resume_demonstration_guide"],
                )
            )

        summary = (
            f"Your profile exhibits a {alignment}% alignment with the {target_role} position. "
            f"You demonstrate strong proficiency in foundational skills ({len(match_result.strong_matches)} matched), "
            f"but currently have {len(critical_gaps)} critical qualification gaps that directly impact profile strength."
        )

        return GapAnalysisResponse(
            target_role=target_role,
            alignment_percentage=alignment,
            summary=summary,
            gaps=gap_details,
        )


# Singleton instance
_gap_explainer = None


def get_gap_explainer() -> GapExplainerEngine:
    global _gap_explainer
    if _gap_explainer is None:
        _gap_explainer = GapExplainerEngine()
    return _gap_explainer
