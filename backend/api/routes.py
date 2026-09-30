"""
CareerEdge AI - REST API Endpoints & Request Handlers
Provides verified on-device inference, resume parsing, job alignment matching,
explainable gap analysis, 30-day roadmap synthesis, benchmarking, and PDF export.
"""

import os
import uuid
import pathlib
from typing import Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import Response

from backend.models.schemas import (
    DeviceStatus,
    ResumeAnalysisRequest,
    ResumeAnalysisResponse,
    JobAnalysisRequest,
    JobAnalysisResponse,
    MatchAnalysisRequest,
    MatchAnalysisResponse,
    GapAnalysisResponse,
    RoadmapResponse,
    ProjectRecommendationResponse,
    ResumeImprovementResponse,
    PrivacyStatus,
)
from backend.utils.document_reader import DocumentReader
from backend.services.resume_parser import get_resume_parser
from backend.services.resume_analyzer import get_resume_quality_analyzer
from backend.services.job_parser import get_job_parser
from backend.engine.matcher import get_job_matcher
from backend.engine.gap_explainer import get_gap_explainer
from backend.engine.roadmap_generator import get_roadmap_generator
from backend.engine.project_recommender import get_project_recommender
from backend.engine.bullet_improver import get_bullet_improver
from backend.engine.qnn_runtime import get_runtime_manager
from ai.runtime.ai_engine import get_ai_engine
from backend.database.database import get_local_db
from backend.services.report_exporter import get_report_exporter
from benchmark import run_benchmark

router = APIRouter(prefix="/api")

DEMO_DIR = pathlib.Path(__file__).parent.parent.parent / "demo"


# -------------------------------------------------------------
# System & Hardware Runtime Endpoints
# -------------------------------------------------------------
@router.get("/health")
def get_health():
    return {
        "status": "healthy",
        "service": "CareerEdge AI",
        "version": "1.0.0",
        "competition": "Snapdragon® AI Lab Build & Present Challenge by Qualcomm",
        "local_ai_active": True,
    }


@router.get("/device", response_model=DeviceStatus)
@router.get("/runtime", response_model=DeviceStatus)
def get_device_info():
    runtime_mgr = get_runtime_manager()
    status = runtime_mgr.get_runtime_status()
    return DeviceStatus(**status)


# -------------------------------------------------------------
# Resume Intelligence Endpoints
# -------------------------------------------------------------
@router.post("/resume/upload", response_model=ResumeAnalysisResponse)
async def upload_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        extracted_text, doc_type = DocumentReader.extract_text(content, file.filename or "resume.pdf")

        parser = get_resume_parser()
        parsed = parser.parse(extracted_text)

        analyzer = get_resume_quality_analyzer()
        quality = analyzer.analyze(parsed)

        resume_id = str(uuid.uuid4())
        db = get_local_db()
        db.save_resume(
            resume_id=resume_id,
            filename=file.filename or "uploaded_resume",
            candidate_name=parsed["candidate_name"],
            parsed_data={**parsed, **quality, "resume_id": resume_id},
        )

        return ResumeAnalysisResponse(
            candidate_name=parsed["candidate_name"],
            email=parsed["email"],
            contact=parsed["contact"],
            links=parsed["links"],
            education=parsed["education"],
            technical_skills=parsed["technical_skills"],
            experience=parsed["experience"],
            projects=parsed["projects"],
            certifications=parsed["certifications"],
            completeness_score=quality["completeness_score"],
            quality_breakdown=quality["quality_breakdown"],
            improvement_areas=quality["improvement_areas"],
            raw_word_count=parsed["raw_word_count"],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/resume/analyze", response_model=ResumeAnalysisResponse)
def analyze_resume_text(req: ResumeAnalysisRequest):
    if not req.resume_text or not req.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty.")

    parser = get_resume_parser()
    parsed = parser.parse(req.resume_text)

    analyzer = get_resume_quality_analyzer()
    quality = analyzer.analyze(parsed)

    resume_id = str(uuid.uuid4())
    db = get_local_db()
    db.save_resume(
        resume_id=resume_id,
        filename="pasted_resume.txt",
        candidate_name=parsed["candidate_name"],
        parsed_data={**parsed, **quality, "resume_id": resume_id},
    )

    return ResumeAnalysisResponse(
        candidate_name=parsed["candidate_name"],
        email=parsed["email"],
        contact=parsed["contact"],
        links=parsed["links"],
        education=parsed["education"],
        technical_skills=parsed["technical_skills"],
        experience=parsed["experience"],
        projects=parsed["projects"],
        certifications=parsed["certifications"],
        completeness_score=quality["completeness_score"],
        quality_breakdown=quality["quality_breakdown"],
        improvement_areas=quality["improvement_areas"],
        raw_word_count=parsed["raw_word_count"],
    )


# -------------------------------------------------------------
# Job Description Endpoints
# -------------------------------------------------------------
@router.post("/job/analyze", response_model=JobAnalysisResponse)
def analyze_job(req: JobAnalysisRequest):
    if not req.job_text or not req.job_text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")

    parser = get_job_parser()
    parsed = parser.parse(req.job_text)

    job_id = str(uuid.uuid4())
    db = get_local_db()
    db.save_job(
        job_id=job_id,
        job_title=parsed["job_title"],
        parsed_data={**parsed, "job_id": job_id},
    )

    return JobAnalysisResponse(**parsed)


# -------------------------------------------------------------
# Alignment & Semantic Matching
# -------------------------------------------------------------
@router.post("/match", response_model=MatchAnalysisResponse)
def analyze_match(req: MatchAnalysisRequest):
    db = get_local_db()

    resume_data = req.resume_data
    if not resume_data:
        latest_res = db.get_latest_resume()
        if latest_res:
            resume_data = latest_res["parsed_data"]
        else:
            raise HTTPException(status_code=400, detail="No resume provided or found in session.")

    job_data = req.job_data
    if not job_data:
        if req.job_text:
            parser = get_job_parser()
            job_data = parser.parse(req.job_text)
        else:
            latest_job = db.get_latest_job()
            if latest_job:
                job_data = latest_job["parsed_data"]
            else:
                raise HTTPException(status_code=400, detail="No job description provided or found in session.")

    matcher = get_job_matcher()
    match_result = matcher.evaluate_match(resume_data, job_data)
    return match_result


# -------------------------------------------------------------
# "Why is my profile not aligned?" Deep Dive
# -------------------------------------------------------------
@router.post("/gap-analysis", response_model=GapAnalysisResponse)
def analyze_gaps(req: MatchAnalysisRequest):
    db = get_local_db()
    resume_data = req.resume_data or (db.get_latest_resume() or {}).get("parsed_data")
    job_data = req.job_data or (db.get_latest_job() or {}).get("parsed_data")

    if not resume_data or not job_data:
        raise HTTPException(status_code=400, detail="Both resume and job data required for gap analysis.")

    matcher = get_job_matcher()
    match_result = matcher.evaluate_match(resume_data, job_data)

    explainer = get_gap_explainer()
    gap_result = explainer.explain_gaps(match_result, resume_data, job_data)
    return gap_result


# -------------------------------------------------------------
# 30-Day Personalized Roadmap
# -------------------------------------------------------------
@router.post("/roadmap", response_model=RoadmapResponse)
def generate_roadmap(req: MatchAnalysisRequest):
    db = get_local_db()
    resume_data = req.resume_data or (db.get_latest_resume() or {}).get("parsed_data")
    job_data = req.job_data or (db.get_latest_job() or {}).get("parsed_data")

    if not resume_data or not job_data:
        raise HTTPException(status_code=400, detail="Both resume and job data required for roadmap generation.")

    matcher = get_job_matcher()
    match_result = matcher.evaluate_match(resume_data, job_data)

    generator = get_roadmap_generator()
    roadmap = generator.generate_roadmap(
        target_role=match_result.target_role,
        critical_gaps=match_result.top_critical_gaps,
    )
    return roadmap


# -------------------------------------------------------------
# Project Recommendations
# -------------------------------------------------------------
@router.post("/project/recommend", response_model=ProjectRecommendationResponse)
def recommend_projects(req: MatchAnalysisRequest):
    db = get_local_db()
    resume_data = req.resume_data or (db.get_latest_resume() or {}).get("parsed_data")
    job_data = req.job_data or (db.get_latest_job() or {}).get("parsed_data")

    matcher = get_job_matcher()
    match_result = matcher.evaluate_match(resume_data or {}, job_data or {})

    recommender = get_project_recommender()
    return recommender.recommend(
        critical_gaps=match_result.top_critical_gaps,
        target_role=match_result.target_role,
    )


# -------------------------------------------------------------
# Resume Improvement Assistant
# -------------------------------------------------------------
@router.post("/resume/improve", response_model=ResumeImprovementResponse)
def improve_resume_bullets(req: MatchAnalysisRequest):
    db = get_local_db()
    resume_data = req.resume_data or (db.get_latest_resume() or {}).get("parsed_data", {})
    job_data = req.job_data or (db.get_latest_job() or {}).get("parsed_data", {})

    target_role = job_data.get("job_title", "Machine Learning Engineer") if job_data else "Machine Learning Engineer"

    improver = get_bullet_improver()
    return improver.improve_bullets(parsed_resume=resume_data, target_role=target_role)


# -------------------------------------------------------------
# Benchmark Endpoints
# -------------------------------------------------------------
@router.get("/benchmark")
def get_latest_benchmark():
    db = get_local_db()
    recent = db.get_recent_benchmarks(limit=1)
    if recent:
        return recent[0]

    # If no benchmark run yet, run one
    result = run_benchmark(warmup_count=5, iterations=20)
    return result


@router.post("/benchmark/run")
def trigger_benchmark(warmup: int = 10, iterations: int = 50):
    result = run_benchmark(warmup_count=warmup, iterations=iterations)
    return result


# -------------------------------------------------------------
# Synthetic Demo 1-Click Loader
# -------------------------------------------------------------
@router.get("/demo/load")
def load_demo_data():
    txt_resume_path = DEMO_DIR / "sample_resume.txt"
    txt_job_path = DEMO_DIR / "sample_job.txt"

    if not txt_resume_path.exists() or not txt_job_path.exists():
        raise HTTPException(status_code=404, detail="Synthetic demo files not found.")

    with open(txt_resume_path, "r", encoding="utf-8") as f:
        resume_text = f.read()

    with open(txt_job_path, "r", encoding="utf-8") as f:
        job_text = f.read()

    # Parse resume
    r_parser = get_resume_parser()
    parsed_resume = r_parser.parse(resume_text)
    r_analyzer = get_resume_quality_analyzer()
    quality = r_analyzer.analyze(parsed_resume)

    # Parse job
    j_parser = get_job_parser()
    parsed_job = j_parser.parse(job_text)

    # Save to local SQLite
    db = get_local_db()
    resume_id = "demo-alex-morgan"
    job_id = "demo-mle-snapdragon"
    db.save_resume(resume_id, "sample_resume.pdf", "Alex Morgan [DEMO DATA]", {**parsed_resume, **quality})
    db.save_job(job_id, parsed_job["job_title"], parsed_job)

    # Evaluate match
    matcher = get_job_matcher()
    match_result = matcher.evaluate_match(parsed_resume, parsed_job)

    # Explain gaps
    explainer = get_gap_explainer()
    gap_result = explainer.explain_gaps(match_result, parsed_resume, parsed_job)

    # Roadmap
    roadmap_gen = get_roadmap_generator()
    roadmap = roadmap_gen.generate_roadmap(match_result.target_role, match_result.top_critical_gaps)

    # Projects
    proj_rec = get_project_recommender()
    projects = proj_rec.recommend(match_result.top_critical_gaps, match_result.target_role)

    # Bullet improvements
    improver = get_bullet_improver()
    improvements = improver.improve_bullets(parsed_resume, match_result.target_role)

    return {
        "status": "Demo data loaded successfully",
        "candidate": "Alex Morgan [DEMO DATA]",
        "target_role": parsed_job["job_title"],
        "resume": {**parsed_resume, **quality},
        "job": parsed_job,
        "match": match_result,
        "gaps": gap_result,
        "roadmap": roadmap,
        "recommended_projects": projects,
        "bullet_improvements": improvements,
    }


# -------------------------------------------------------------
# Export Career Report PDF
# -------------------------------------------------------------
@router.post("/export/pdf")
def export_pdf_report(req: MatchAnalysisRequest):
    db = get_local_db()
    resume_data = req.resume_data or (db.get_latest_resume() or {}).get("parsed_data", {})
    job_data = req.job_data or (db.get_latest_job() or {}).get("parsed_data", {})

    matcher = get_job_matcher()
    match_result = matcher.evaluate_match(resume_data, job_data)

    explainer = get_gap_explainer()
    gap_result = explainer.explain_gaps(match_result, resume_data, job_data)

    roadmap_gen = get_roadmap_generator()
    roadmap = roadmap_gen.generate_roadmap(match_result.target_role, match_result.top_critical_gaps)

    proj_rec = get_project_recommender()
    projects = proj_rec.recommend(match_result.top_critical_gaps, match_result.target_role)

    runtime_mgr = get_runtime_manager()
    runtime_status = runtime_mgr.get_runtime_status()

    exporter = get_report_exporter()
    pdf_bytes = exporter.generate_pdf(
        match_data=match_result.model_dump(),
        gap_data=gap_result.model_dump(),
        roadmap_data=roadmap.model_dump(),
        project_data=projects.model_dump(),
        runtime_status=runtime_status,
    )

    filename = f"CareerEdge_Report_{match_result.target_role.replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# -------------------------------------------------------------
# Privacy & Session Purge
# -------------------------------------------------------------
@router.delete("/session")
def clear_session():
    db = get_local_db()
    cleared = db.clear_all_session_data()
    return {
        "status": "All session data, uploaded resumes, and local analyses have been permanently purged.",
        "cleared_records": cleared,
        "zero_retention_guaranteed": True,
    }
