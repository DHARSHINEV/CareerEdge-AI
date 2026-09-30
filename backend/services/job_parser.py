"""
CareerEdge AI - Job Description Parser & Ontology Normalizer
Extracts job title, required skills, preferred qualifications, responsibilities,
and domains with full alias normalization.
"""

import re
import logging
from typing import Dict, Any, List, Set, Optional
from backend.services.skill_ontology import get_skill_ontology

logger = logging.getLogger("careeredge.job_parser")


class JobParser:
    """
    Parses job descriptions, discovers domain, separates required vs preferred skills,
    and maps all extracted technologies to normalized canonical skills.
    """

    def __init__(self):
        self.ontology = get_skill_ontology()

    def parse(self, raw_text: str) -> Dict[str, Any]:
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

        job_title = self._extract_job_title(lines, raw_text)
        domain = self._extract_domain(raw_text, job_title)

        sections = self._split_job_sections(raw_text)

        required_skills = self._extract_skills_from_text(sections.get("required", "") or raw_text)
        preferred_skills = self._extract_skills_from_text(sections.get("preferred", ""))

        # If no explicit preferred section found, separate into required vs preferred by wording
        if not preferred_skills:
            req_list = []
            pref_list = []
            for s in required_skills:
                # If mentioned near 'preferred', 'nice to have', 'bonus', 'plus'
                pattern = re.compile(r"(?:preferred|nice to have|bonus|plus)[^\n.]{0,100}\b" + re.escape(s.lower()), re.IGNORECASE)
                if pattern.search(raw_text.lower()):
                    pref_list.append(s)
                else:
                    req_list.append(s)
            required_skills = req_list or required_skills
            preferred_skills = pref_list

        # Deduplicate: skills in required shouldn't be duplicated in preferred
        preferred_skills = [s for s in preferred_skills if s not in required_skills]

        responsibilities = self._extract_bullets(sections.get("responsibilities", ""))
        education = self._extract_education_requirements(raw_text)
        experience_level = self._extract_experience_level(raw_text)

        all_tools_and_tech = sorted(list(set(required_skills + preferred_skills)))

        return {
            "job_title": job_title,
            "domain": domain,
            "required_skills": required_skills[:12],
            "preferred_skills": preferred_skills[:8],
            "responsibilities": responsibilities[:6],
            "education_requirements": education,
            "experience_level": experience_level,
            "tools_and_tech": all_tools_and_tech,
            "raw_text": raw_text,
        }

    def _extract_job_title(self, lines: List[str], text: str) -> str:
        common_titles = [
            "Machine Learning Engineer",
            "AI Engineer",
            "Edge AI Engineer",
            "Data Scientist",
            "Software Engineer",
            "Full Stack Developer",
            "Backend Engineer",
            "DevOps Engineer",
            "Cloud Solutions Architect",
            "Data Engineer",
            "Computer Vision Engineer",
            "NLP Engineer",
        ]

        # Check in text first
        for title in common_titles:
            if re.search(r"\b" + re.escape(title) + r"\b", text, re.IGNORECASE):
                return title

        # Check first line
        if lines:
            first_line = lines[0].strip(":#- ")
            if len(first_line) < 60:
                return first_line.title()

        return "Machine Learning Engineer"

    def _extract_domain(self, text: str, title: str) -> str:
        text_lower = text.lower() + " " + title.lower()
        if any(k in text_lower for k in ["snapdragon", "npu", "hexagon", "edge ai", "on-device", "embedded ai", "quantization"]):
            return "Edge AI & On-Device Acceleration"
        if any(k in text_lower for k in ["machine learning", "deep learning", "llm", "ai", "model"]):
            return "Machine Learning & AI Engineering"
        if any(k in text_lower for k in ["cloud", "aws", "azure", "kubernetes", "devops"]):
            return "Cloud Infrastructure & DevOps"
        if any(k in text_lower for k in ["data engineer", "etl", "spark", "pipeline", "warehouse"]):
            return "Data Engineering & Analytics"
        if any(k in text_lower for k in ["frontend", "react", "full stack", "web"]):
            return "Full Stack Software Development"
        return "Software Engineering"

    def _split_job_sections(self, text: str) -> Dict[str, str]:
        sections: Dict[str, str] = {}
        headers = {
            "required": [r"\brequirements\b", r"\brequired skills\b", r"\bwhat you will need\b", r"\bqualifications\b", r"\bminimum qualifications\b"],
            "preferred": [r"\bpreferred qualifications\b", r"\bnice to have\b", r"\bbonus points\b", r"\bpreferred skills\b"],
            "responsibilities": [r"\bresponsibilities\b", r"\bwhat you will do\b", r"\bduties\b", r"\brole overview\b"],
        }

        # Divide text
        text_lines = text.splitlines()
        current_sec = "required"
        sec_buffers = {"required": [], "preferred": [], "responsibilities": []}

        for line in text_lines:
            line_clean = line.strip().lower()
            matched_header = False
            for sec_name, pats in headers.items():
                if any(re.search(p, line_clean) for p in pats) and len(line_clean) < 40:
                    current_sec = sec_name
                    matched_header = True
                    break
            if not matched_header:
                sec_buffers[current_sec].append(line)

        return {k: "\n".join(v).strip() for k, v in sec_buffers.items()}

    def _extract_skills_from_text(self, text: str) -> List[str]:
        found: Set[str] = set()
        text_lower = " " + text.lower() + " "

        for canonical, cat in self.ontology.canonical_to_category.items():
            all_terms = [canonical] + [a for a, c in self.ontology.alias_to_canonical.items() if c == canonical]
            for term in all_terms:
                if re.search(r"(?:^|[\s,;/()•|])" + re.escape(term.lower()) + r"(?:[\s,;/()•|]|$)", text_lower):
                    found.add(canonical)
                    break

        return sorted(list(found))

    def _extract_bullets(self, text: str) -> List[str]:
        bullets = []
        for line in text.splitlines():
            line_str = line.strip("• -* \t")
            if len(line_str) > 15:
                bullets.append(line_str)
        return bullets

    def _extract_education_requirements(self, text: str) -> List[str]:
        reqs = []
        if re.search(r"\b(bachelor|b\.s\.|b\.tech|b\.e\.)\b", text, re.IGNORECASE):
            reqs.append("Bachelor's degree in Computer Science, Data Science, or related engineering discipline")
        if re.search(r"\b(master|m\.s\.|phd|advanced degree)\b", text, re.IGNORECASE):
            reqs.append("Master's or Ph.D. degree preferred")
        return reqs or ["Bachelor's degree in Computer Science or equivalent practical experience"]

    def _extract_experience_level(self, text: str) -> str:
        match = re.search(r"\b(\d+)\+?\s*(?:-\s*\d+)?\s*years?\b", text, re.IGNORECASE)
        if match:
            return f"{match.group(0)} experience"
        if re.search(r"\b(senior|lead|staff|principal)\b", text, re.IGNORECASE):
            return "Senior (5+ years)"
        if re.search(r"\b(junior|entry|intern|fresh)\b", text, re.IGNORECASE):
            return "Entry Level / Early Career (0-2 years)"
        return "Mid-Level (2-4 years)"


# Singleton instance
_job_parser: Optional[JobParser] = None


def get_job_parser() -> JobParser:
    global _job_parser
    if _job_parser is None:
        _job_parser = JobParser()
    return _job_parser
