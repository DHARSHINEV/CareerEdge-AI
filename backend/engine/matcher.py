"""
CareerEdge AI - Semantic Job Matcher & Requirement Evaluator
Performs hybrid lexical, ontological, and dense embedding matching.
Classifies requirements into Strong, Partial, and Missing with explainable evidence.
"""

import time
import logging
from typing import Dict, Any, List, Tuple
import numpy as np

from backend.services.skill_ontology import get_skill_ontology
from ai.runtime.ai_engine import get_ai_engine
from backend.engine.scoring import calculate_alignment_score
from backend.models.schemas import SkillMatchDetail, MatchAnalysisResponse

logger = logging.getLogger("careeredge.matcher")


class SemanticJobMatcher:
    """
    Evaluates candidate alignment against job requirements using local ONNX embeddings
    and transparent ontology-based classification.
    """

    def __init__(self):
        self.ontology = get_skill_ontology()
        self.ai_engine = get_ai_engine()

    def evaluate_match(
        self, parsed_resume: Dict[str, Any], parsed_job: Dict[str, Any]
    ) -> MatchAnalysisResponse:
        t0 = time.perf_counter()

        resume_skills_dict = parsed_resume.get("technical_skills", {})
        all_resume_skills = []
        for cat_skills in resume_skills_dict.values():
            all_resume_skills.extend(cat_skills)
        resume_skills_set = set(s.lower() for s in all_resume_skills)

        projects = parsed_resume.get("projects", [])
        experience = parsed_resume.get("experience", [])
        education = parsed_resume.get("education", [])
        raw_resume_text = parsed_resume.get("raw_text", "").lower()

        required_skills = parsed_job.get("required_skills", [])
        preferred_skills = parsed_job.get("preferred_skills", [])

        # Ensure we have at least some requirements
        if not required_skills and not preferred_skills:
            required_skills = ["Python", "Machine Learning", "Git"]

        # Collect text snippets for project evidence
        project_texts = [
            f"{p.get('name', '')} {p.get('description', '')} {' '.join(p.get('technologies', []))}".lower()
            for p in projects
        ]

        strong_matches: List[SkillMatchDetail] = []
        partial_matches: List[SkillMatchDetail] = []
        missing_skills: List[SkillMatchDetail] = []

        all_reqs = [(s, True) for s in required_skills] + [(s, False) for s in preferred_skills]

        # Pre-compute embeddings for semantic comparison if needed
        req_texts = [f"Technical proficiency and engineering experience with {s}" for s, _ in all_reqs]
        cand_texts = (
            [f"Demonstrated project experience with {s}" for s in all_resume_skills]
            if all_resume_skills
            else ["General software engineering experience"]
        )

        req_vecs, _ = self.ai_engine.encode_texts(req_texts)
        cand_vecs, enc_lat = self.ai_engine.encode_texts(cand_texts)

        for idx, (skill, is_required) in enumerate(all_reqs):
            skill_lower = skill.lower()
            category = self.ontology.get_category(skill)

            # Check exact presence in resume skills inventory
            exact_in_skills = skill_lower in resume_skills_set

            # Check project evidence
            in_projects = []
            for p in projects:
                p_text = f"{p.get('name', '')} {p.get('description', '')} {' '.join(p.get('technologies', []))}".lower()
                if skill_lower in p_text or skill in p.get("technologies", []):
                    in_projects.append(p.get("name", "Project"))

            # Check experience evidence
            in_exp = []
            for exp in experience:
                e_text = f"{exp.get('company', '')} {exp.get('role', '')} {' '.join(exp.get('responsibilities', []))}".lower()
                if skill_lower in e_text or skill in exp.get("technologies", []):
                    in_exp.append(exp.get("company", "Company"))

            # Semantic similarity to candidate profile
            req_vec = req_vecs[idx] if idx < len(req_vecs) else np.zeros(384)
            sim_scores = [
                self.ai_engine.compute_similarity(req_vec, c_vec)
                for c_vec in cand_vecs
            ]
            max_sim = max(sim_scores) if sim_scores else 0.0

            # Find related skills in resume
            related_in_resume = []
            for r_s in self.ontology.get_related(skill):
                if r_s.lower() in resume_skills_set:
                    related_in_resume.append(r_s)

            # Classification logic
            if exact_in_skills and (in_projects or in_exp):
                status = "Strong Match"
                evidence_items = []
                if in_projects:
                    evidence_items.append(f"Demonstrated in project '{in_projects[0]}'")
                if in_exp:
                    evidence_items.append(f"Applied at '{in_exp[0]}'")
                evidence = "; ".join(evidence_items)
                recommendation = f"Maintain strong evidence and highlight production metrics for {skill}."
                detail = SkillMatchDetail(
                    requirement=skill,
                    status=status,
                    category=category,
                    is_required=is_required,
                    resume_evidence=evidence,
                    recommendation=recommendation,
                    semantic_similarity=round(float(max(0.85, max_sim)), 2),
                )
                strong_matches.append(detail)

            elif exact_in_skills or related_in_resume or max_sim >= 0.70:
                status = "Partial Match"
                if exact_in_skills:
                    evidence = f"Listed in skills inventory, but lacks dedicated project or production experience."
                    rec = f"Build a focused project implementing {skill} to substantiate this skill."
                elif related_in_resume:
                    evidence = f"Resume demonstrates related proficiency in [{', '.join(related_in_resume)}], but direct {skill} evidence is missing."
                    rec = f"Leverage your background in {related_in_resume[0]} to quickly implement a {skill} module or integration."
                else:
                    evidence = f"Semantic alignment detected from related domain experience ({int(max_sim*100)}% similarity)."
                    rec = f"Explicitly document hands-on use of {skill} in your project portfolio."

                detail = SkillMatchDetail(
                    requirement=skill,
                    status=status,
                    category=category,
                    is_required=is_required,
                    resume_evidence=evidence,
                    recommendation=rec,
                    semantic_similarity=round(float(max_sim), 2),
                )
                partial_matches.append(detail)

            else:
                status = "Missing"
                evidence = f"No direct evidence or related technical experience for {skill} detected in resume."
                rec = f"Prioritize learning {skill} fundamentals and build a starter project."
                detail = SkillMatchDetail(
                    requirement=skill,
                    status=status,
                    category=category,
                    is_required=is_required,
                    resume_evidence=evidence,
                    recommendation=rec,
                    semantic_similarity=round(float(max_sim), 2),
                )
                missing_skills.append(detail)

        # ---------------- Compute Component Scores ----------------
        # 1. Technical skills score:
        # Required weight: 2.0, Preferred weight: 1.0
        total_req_points = 0.0
        earned_req_points = 0.0
        for m in strong_matches + partial_matches + missing_skills:
            weight = 2.0 if m.is_required else 1.0
            mult = 1.0 if m.status == "Strong Match" else (0.5 if m.status == "Partial Match" else 0.0)
            earned_req_points += weight * mult
            total_req_points += weight

        skills_score = (earned_req_points / total_req_points * 100.0) if total_req_points > 0 else 50.0

        # 2. Projects score:
        # Based on project count, tech breadth, and metric presence
        p_count = len(projects)
        p_with_metrics = sum(1 for p in projects if p.get("has_metrics", False))
        projects_score = min(100.0, (min(3, p_count) / 3.0) * 70.0 + (min(2, p_with_metrics) / 2.0) * 30.0)

        # 3. Experience score:
        exp_score = min(100.0, len(experience) * 45.0) if experience else 40.0

        # 4. Education score:
        has_deg = len(education) > 0
        education_score = 95.0 if has_deg else 60.0

        # 5. Domain score:
        domain_str = parsed_job.get("domain", "")
        domain_match = any(w in raw_resume_text for w in domain_str.lower().split() if len(w) > 3)
        domain_score = 85.0 if domain_match else 65.0

        # Compute deterministic overall score
        score_result = calculate_alignment_score(
            skills_score=skills_score,
            projects_score=projects_score,
            experience_score=exp_score,
            education_score=education_score,
            domain_score=domain_score,
        )

        # Top critical gaps: prioritize required missing skills first, then required partials
        critical_gaps = [m for m in missing_skills if m.is_required]
        if len(critical_gaps) < 3:
            critical_gaps.extend([m for m in partial_matches if m.is_required])
        if len(critical_gaps) < 3:
            critical_gaps.extend([m for m in missing_skills if not m.is_required])

        total_latency = (time.perf_counter() - t0) * 1000.0
        runtime_status = self.ai_engine.get_status()

        return MatchAnalysisResponse(
            target_role=parsed_job.get("job_title", "Target Role"),
            overall_alignment=score_result["overall_alignment"],
            score_breakdown=score_result["score_breakdown"],
            strong_matches=strong_matches,
            partial_matches=partial_matches,
            missing_skills=missing_skills,
            top_critical_gaps=critical_gaps[:5],
            inference_latency_ms=round(total_latency, 2),
            execution_provider=runtime_status["active_provider"],
        )


# Singleton instance
_matcher: Optional[SemanticJobMatcher] = None


def get_job_matcher() -> SemanticJobMatcher:
    global _matcher
    if _matcher is None:
        _matcher = SemanticJobMatcher()
    return _matcher
