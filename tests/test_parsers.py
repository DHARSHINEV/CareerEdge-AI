"""
Unit tests for Resume Parser, Quality Analyzer, and Job Description Parser.
"""

from backend.services.resume_parser import get_resume_parser
from backend.services.resume_analyzer import get_resume_quality_analyzer
from backend.services.job_parser import get_job_parser


def test_resume_parser_extraction():
    sample_text = """
    Jane Doe
    jane.doe@example.com | (555) 123-4567 | github.com/janedoe
    
    EDUCATION
    University of Washington
    Bachelor of Science in Computer Science, 2024
    
    TECHNICAL SKILLS
    Python, C++, PyTorch, Docker, SQL, FastAPI, Git, Linux
    
    WORK EXPERIENCE
    Software Engineer | Tech Corp
    • Built scalable REST APIs using FastAPI and Python, handling 15,000 requests/sec.
    • Optimized database queries in PostgreSQL, achieving a 45% latency reduction.
    
    KEY PROJECTS
    Edge Vision Classifier | PyTorch, ONNX, Docker
    • Developed an on-device computer vision classifier in PyTorch and exported to ONNX.
    • Evaluated inference performance with 98.2% test accuracy.
    """

    parser = get_resume_parser()
    parsed = parser.parse(sample_text)

    assert parsed["candidate_name"] == "Jane Doe"
    assert parsed["email"] == "jane.doe@example.com"
    assert "github.com/janedoe" in parsed["links"]
    assert len(parsed["education"]) >= 1
    assert "Python" in parsed["technical_skills"].get("Programming", [])
    assert "PyTorch" in parsed["technical_skills"].get("ML/AI", [])
    assert "Docker" in parsed["technical_skills"].get("DevOps", [])
    assert len(parsed["experience"]) >= 1
    assert len(parsed["projects"]) >= 1


def test_resume_quality_scoring():
    parser = get_resume_parser()
    analyzer = get_resume_quality_analyzer()

    text = """
    Alex Smith
    alex@test.com
    EDUCATION: BS Computer Science 2023
    SKILLS: Python, SQL, Git, Linux, Docker
    PROJECTS:
    Classifier App: Built an image classification API in Python and Docker with 35% speedup across 10,000 requests.
    """
    parsed = parser.parse(text)
    quality = analyzer.analyze(parsed)

    assert 0 <= quality["completeness_score"] <= 100
    assert "Structural Integrity" in quality["quality_breakdown"]
    assert "Measurable Impact" in quality["quality_breakdown"]
    assert len(quality["improvement_areas"]) >= 1


def test_job_parser_extraction():
    job_text = """
    Position: Machine Learning Engineer
    Company: Snapdragon AI Labs
    
    Minimum Qualifications:
    • Strong proficiency in Python and C++.
    • Deep experience with PyTorch and ONNX Runtime.
    • Experience with Docker containerization.
    
    Preferred Qualifications:
    • Hands-on with Qualcomm QNN or Hexagon NPU.
    • AWS cloud deployment experience.
    
    Responsibilities:
    • Deploy models to on-device hardware.
    • Optimize inference latency and throughput.
    """

    parser = get_job_parser()
    parsed = parser.parse(job_text)

    assert parsed["job_title"] == "Machine Learning Engineer"
    assert "Python" in parsed["required_skills"]
    assert "PyTorch" in parsed["required_skills"]
    assert "Docker" in parsed["required_skills"]
    assert len(parsed["responsibilities"]) >= 1
