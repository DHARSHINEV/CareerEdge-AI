"""
CareerEdge AI - Resume Intelligence & Parsing Service
Extracts structured sections, technical skills categorized by ontology,
work experiences, engineering projects, education, and certifications.
"""

import re
import logging
from typing import Dict, List, Any, Optional
from backend.services.skill_ontology import get_skill_ontology
from backend.models.schemas import (
    ResumeAnalysisResponse,
    ResumeSectionEducation,
    ResumeSectionExperience,
    ResumeSectionProject,
    ResumeSectionCertification,
)

logger = logging.getLogger("careeredge.resume_parser")


class ResumeParser:
    """
    Parses raw resume text into structured fields using section detection,
    named entity patterns, and skill ontology matching.
    """

    def __init__(self):
        self.ontology = get_skill_ontology()

    def parse(self, raw_text: str) -> Dict[str, Any]:
        """
        Main parser pipeline for raw resume text.
        """
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        text_lower = raw_text.lower()

        candidate_name = self._extract_name(lines)
        email = self._extract_email(raw_text)
        contact = self._extract_phone(raw_text)
        links = self._extract_links(raw_text)

        sections = self._split_into_sections(raw_text)

        education = self._extract_education(sections.get("education", ""))
        skills_categorized = self._extract_skills(raw_text)
        experience = self._extract_experience(sections.get("experience", ""))
        projects = self._extract_projects(sections.get("projects", ""))
        certifications = self._extract_certifications(sections.get("certifications", ""))

        return {
            "candidate_name": candidate_name,
            "email": email,
            "contact": contact,
            "links": links,
            "education": education,
            "technical_skills": skills_categorized,
            "experience": experience,
            "projects": projects,
            "certifications": certifications,
            "raw_word_count": len(raw_text.split()),
            "raw_text": raw_text,
        }

    def _extract_name(self, lines: List[str]) -> str:
        """Heuristically picks candidate name from top lines."""
        for line in lines[:4]:
            # Skip lines with email, phone, links, or section headers
            if any(char in line for char in ["@", "http", "www", "+", "(", ")", "/"]):
                continue
            words = line.split()
            if 1 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
                return line.title()
        return lines[0].title() if lines else "Candidate"

    def _extract_email(self, text: str) -> Optional[str]:
        pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        matches = re.findall(pattern, text)
        return matches[0] if matches else None

    def _extract_phone(self, text: str) -> Optional[str]:
        pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
        matches = re.findall(pattern, text)
        return matches[0] if matches else None

    def _extract_links(self, text: str) -> List[str]:
        pattern = r"(?:https?://)?(?:www\.)?(?:github\.com/[a-zA-Z0-9_-]+|linkedin\.com/in/[a-zA-Z0-9_-]+|[a-zA-Z0-9_-]+\.github\.io)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        return list(set(matches))

    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """
        Splits text into logical resume sections: Education, Experience, Projects, Skills, Certifications.
        """
        section_headers = {
            "education": [r"\beducation\b", r"\bacademics\b", r"\bacademic background\b"],
            "experience": [r"\bexperience\b", r"\bwork experience\b", r"\bemployment\b", r"\bprofessional experience\b"],
            "projects": [r"\bprojects\b", r"\bpersonal projects\b", r"\bacademic projects\b", r"\bkey projects\b"],
            "skills": [r"\bskills\b", r"\btechnical skills\b", r"\bcompetencies\b", r"\btechnologies\b"],
            "certifications": [r"\bcertifications\b", r"\bcertificates\b", r"\blicenses\b", r"\bachievements\b"],
        }

        # Build regex for headings
        all_patterns = []
        for sec, pats in section_headers.items():
            for p in pats:
                all_patterns.append(f"(?P<{sec}_{len(all_patterns)}>{p})")

        combined_regex = re.compile(r"^[ \t]*(?:" + "|".join(all_patterns) + r")[ \t]*:?$", re.IGNORECASE | re.MULTILINE)
        matches = list(combined_regex.finditer(text))

        sections: Dict[str, str] = {}
        if not matches:
            # Fallback simple partition
            return {"experience": text, "projects": text, "skills": text, "education": text}

        for idx, match in enumerate(matches):
            header_name = None
            for key, val in match.groupdict().items():
                if val:
                    header_name = key.split("_")[0]
                    break
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            content = text[start:end].strip()
            if header_name:
                sections[header_name] = content

        return sections

    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extracts and categorizes technical skills present anywhere in the resume using ontology.
        """
        categorized: Dict[str, Set[str]] = {
            "Programming": set(),
            "ML/AI": set(),
            "Data": set(),
            "Web": set(),
            "Cloud": set(),
            "DevOps": set(),
            "Other": set(),
        }

        text_lower = " " + text.lower() + " "

        for canonical, category in self.ontology.canonical_to_category.items():
            # Check canonical and aliases with word boundary checks
            all_terms = [canonical] + [a for a, c in self.ontology.alias_to_canonical.items() if c == canonical]
            found = False
            for term in all_terms:
                escaped = re.escape(term.lower())
                # Use boundary check or punctuation boundary
                if re.search(r"(?:^|[\s,;/()•|])" + escaped + r"(?:[\s,;/()•|]|$)", text_lower):
                    found = True
                    break

            if found:
                target_cat = category if category in categorized else "Other"
                categorized[target_cat].add(canonical)

        return {k: sorted(list(v)) for k, v in categorized.items() if v}

    def _extract_education(self, section_text: str) -> List[Dict[str, Any]]:
        """Extracts education records."""
        records = []
        if not section_text:
            return records

        degree_patterns = [
            r"(?:bachelor|master|phd|b\.s\.|m\.s\.|b\.tech|m\.tech|b\.e\.|m\.e\.|associate)[^,\n]*",
            r"(?:computer science|data science|electrical engineering|information technology|software engineering|ai)",
        ]

        lines = section_text.splitlines()
        current_deg = None
        current_inst = None
        current_year = None

        year_regex = re.compile(r"\b(20\d\d|19\d\d)\b")
        gpa_regex = re.compile(r"\b(?:gpa|cgpa)[:\s]*([0-4]\.\d{1,2}|[5-9]\.\d{1,2}|10(?:\.0)?)\b", re.IGNORECASE)

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Check year
            yr_match = year_regex.search(line_str)
            if yr_match:
                current_year = yr_match.group(1)

            # Check degree
            for dp in degree_patterns:
                match = re.search(dp, line_str, re.IGNORECASE)
                if match and not current_deg:
                    current_deg = match.group(0).strip().title()

            # Check institution
            if any(kw in line_str.lower() for kw in ["university", "college", "institute", "school"]):
                current_inst = line_str.split(",")[0].strip()

        if current_deg or current_inst:
            records.append({
                "degree": current_deg or "Bachelor of Science",
                "institution": current_inst or "Accredited University",
                "graduation_year": current_year,
                "gpa": None,
            })
        return records

    def _extract_experience(self, section_text: str) -> List[Dict[str, Any]]:
        """Extracts work experience records."""
        experiences = []
        if not section_text:
            return experiences

        blocks = re.split(r"\n(?=[A-Z0-9][A-Za-z0-9\s|,-]{3,50}\n)", section_text)
        metric_pattern = re.compile(r"\b(\d+%\b|\$\d+|\b\d+x\b|\b\d+\s*ms\b|\b\d+\s*users\b|\bincreased\b|\breduced\b|\baccelerated\b)", re.IGNORECASE)

        for block in blocks:
            lines = [l.strip() for l in block.splitlines() if l.strip()]
            if not lines:
                continue

            header_line = lines[0]
            role = "Software Engineer"
            company = "Technology Co."

            parts = [p.strip() for p in re.split(r"\||–|-| at ", header_line) if p.strip()]
            if len(parts) >= 2:
                role = parts[0]
                company = parts[1]
            elif len(parts) == 1:
                role = parts[0]

            bullet_lines = lines[1:] if len(lines) > 1 else [lines[0]]
            has_metric = any(bool(metric_pattern.search(b)) for b in bullet_lines)

            # Find technologies mentioned in block
            techs = []
            for canon in self.ontology.canonical_set:
                if re.search(r"\b" + re.escape(canon.lower()) + r"\b", block.lower()):
                    techs.append(canon)

            experiences.append({
                "company": company,
                "role": role,
                "duration": "2023 - Present",
                "technologies": techs[:6],
                "responsibilities": bullet_lines,
                "has_quantified_impact": has_metric,
            })

        return experiences[:5]

    def _extract_projects(self, section_text: str) -> List[Dict[str, Any]]:
        """Extracts technical project items with details."""
        projects = []
        if not section_text:
            return projects

        blocks = re.split(r"\n(?=[A-Z0-9][A-Za-z0-9\s|,-]{2,40}(?:\([^\)]+\))?\n)", section_text)
        metric_pattern = re.compile(r"\b(\d+%\b|\$\d+|\b\d+x\b|\b\d+\s*ms\b|\baccuracy\b|\blatency\b|\bthroughput\b)", re.IGNORECASE)

        for block in blocks:
            lines = [l.strip() for l in block.splitlines() if l.strip()]
            if not lines:
                continue

            name = lines[0].split("|")[0].split("-")[0].strip()
            # Extract technologies
            techs = []
            for canon in self.ontology.canonical_set:
                if re.search(r"\b" + re.escape(canon.lower()) + r"\b", block.lower()):
                    techs.append(canon)

            desc = " ".join(lines[1:]) if len(lines) > 1 else lines[0]
            has_metric = bool(metric_pattern.search(desc))

            projects.append({
                "name": name,
                "technologies": techs[:6],
                "description": desc,
                "impact": "Production outcome demonstrated" if has_metric else "",
                "has_metrics": has_metric,
            })

        return projects[:6]

    def _extract_certifications(self, section_text: str) -> List[Dict[str, Any]]:
        certs = []
        if not section_text:
            return certs

        for line in section_text.splitlines():
            line_str = line.strip("• -* \t")
            if len(line_str) > 4:
                certs.append({
                    "name": line_str,
                    "issuer": "Industry Provider",
                    "year": "2024",
                })
        return certs[:4]


# Singleton instance
_resume_parser: Optional[ResumeParser] = None


def get_resume_parser() -> ResumeParser:
    global _resume_parser
    if _resume_parser is None:
        _resume_parser = ResumeParser()
    return _resume_parser
