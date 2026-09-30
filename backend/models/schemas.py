"""
CareerEdge AI - Pydantic Data Models & Schemas
Strict type validation for all career intelligence and AI runtime APIs.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


# -------------------------------------------------------------
# Device & Hardware Runtime Models
# -------------------------------------------------------------
class DeviceStatus(BaseModel):
    device_name: str = Field(..., description="Operating system host name or model")
    os_name: str = Field(..., description="Operating system release and build")
    architecture: str = Field(..., description="CPU architecture (ARM64 or AMD64)")
    processor: str = Field(..., description="Processor brand and model string")
    gpu_name: Optional[str] = Field(None, description="Detected GPU controller")
    npu_detected: bool = Field(..., description="Whether a Snapdragon Hexagon NPU is physically detected")
    npu_name: Optional[str] = Field(None, description="NPU hardware identifier if present")
    onnx_runtime_version: str = Field(..., description="Installed ONNX Runtime version")
    available_providers: List[str] = Field(..., description="All available ONNX Runtime execution providers")
    active_provider: str = Field(..., description="Currently active execution provider")
    qnn_available: bool = Field(..., description="Whether Qualcomm QNN Execution Provider is available")
    runtime_mode: str = Field(..., description="NPU_ACTIVE, CPU_FALLBACK, or GPU_ACTIVE")
    status_label: str = Field(..., description="User-facing status string")
    qnn_status_label: str = Field(default="QNN DEPLOYMENT PATH IMPLEMENTED — NOT PHYSICALLY VERIFIED ON CURRENT HOST", description="Honest verification status of QNN on current host")
    privacy_mode: str = Field(default="100% On-Device / Zero Cloud Upload")
    is_offline_verified: bool = Field(default=True)


class RuntimeConfig(BaseModel):
    preferred_device: str = Field("auto", description="auto, npu, or cpu")


# -------------------------------------------------------------
# Skill & Ontology Models
# -------------------------------------------------------------
class SkillItem(BaseModel):
    name: str
    category: str  # Programming, ML/AI, Data, Web, Cloud, DevOps, Soft, Other
    proficiency_estimate: Optional[str] = "Intermediate"
    evidence_snippets: List[str] = []


class ResumeSectionExperience(BaseModel):
    company: str
    role: str
    duration: str
    technologies: List[str] = []
    responsibilities: List[str] = []
    has_quantified_impact: bool = False


class ResumeSectionProject(BaseModel):
    name: str
    technologies: List[str] = []
    description: str
    impact: str = ""
    has_metrics: bool = False


class ResumeSectionEducation(BaseModel):
    degree: str
    institution: str
    graduation_year: Optional[str] = None
    gpa: Optional[str] = None


class ResumeSectionCertification(BaseModel):
    name: str
    issuer: str
    year: Optional[str] = None


# -------------------------------------------------------------
# Resume Intelligence Models
# -------------------------------------------------------------
class ResumeAnalysisRequest(BaseModel):
    resume_text: Optional[str] = None


class ResumeAnalysisResponse(BaseModel):
    candidate_name: str
    email: Optional[str] = None
    contact: Optional[str] = None
    links: List[str] = []
    education: List[ResumeSectionEducation] = []
    technical_skills: Dict[str, List[str]] = {}
    experience: List[ResumeSectionExperience] = []
    projects: List[ResumeSectionProject] = []
    certifications: List[ResumeSectionCertification] = []
    completeness_score: int
    quality_breakdown: Dict[str, int]
    improvement_areas: List[str]
    raw_word_count: int


# -------------------------------------------------------------
# Job Description Models
# -------------------------------------------------------------
class JobAnalysisRequest(BaseModel):
    job_text: str


class JobAnalysisResponse(BaseModel):
    job_title: str
    domain: str
    required_skills: List[str]
    preferred_skills: List[str]
    responsibilities: List[str]
    education_requirements: List[str]
    experience_level: str
    tools_and_tech: List[str]


# -------------------------------------------------------------
# Alignment & Semantic Matching Models
# -------------------------------------------------------------
class SkillMatchDetail(BaseModel):
    requirement: str
    status: str  # Strong Match, Partial Match, Missing
    category: str
    is_required: bool
    resume_evidence: str
    recommendation: str
    semantic_similarity: float


class AlignmentScoreBreakdown(BaseModel):
    technical_skills: int
    projects: int
    experience: int
    education: int
    domain: int


class MatchAnalysisRequest(BaseModel):
    resume_id: Optional[str] = None
    resume_data: Optional[Dict[str, Any]] = None
    job_text: Optional[str] = None
    job_data: Optional[Dict[str, Any]] = None


class MatchAnalysisResponse(BaseModel):
    target_role: str
    overall_alignment: int
    score_breakdown: AlignmentScoreBreakdown
    strong_matches: List[SkillMatchDetail]
    partial_matches: List[SkillMatchDetail]
    missing_skills: List[SkillMatchDetail]
    top_critical_gaps: List[SkillMatchDetail]
    inference_latency_ms: float
    execution_provider: str


# -------------------------------------------------------------
# "Why is my profile not aligned?" Deep Dive
# -------------------------------------------------------------
class GapDetail(BaseModel):
    skill: str
    category: str
    importance: str  # Critical (Required) vs Medium (Preferred)
    why_it_matters: str
    evidence_missing: str
    what_to_learn: List[str]
    recommended_project: str
    resume_demonstration_guide: str


class GapAnalysisResponse(BaseModel):
    target_role: str
    alignment_percentage: int
    summary: str
    gaps: List[GapDetail]


# -------------------------------------------------------------
# Roadmap Models
# -------------------------------------------------------------
class RoadmapDayTask(BaseModel):
    day: int
    title: str
    description: str
    linked_gap: str
    deliverable: str


class RoadmapWeek(BaseModel):
    week_number: int
    theme: str
    objective: str
    tasks: List[RoadmapDayTask]


class RoadmapResponse(BaseModel):
    target_role: str
    weeks: List[RoadmapWeek]
    estimated_weekly_hours: int = 10
    total_duration_days: int = 30


# -------------------------------------------------------------
# Project Recommendation Models
# -------------------------------------------------------------
class RecommendedProject(BaseModel):
    title: str
    target_skills: List[str]
    difficulty: str  # Beginner, Intermediate, Advanced
    estimated_timeline: str
    summary: str
    architecture: str
    deliverables: List[str]
    resume_bullet_sample: str


class ProjectRecommendationResponse(BaseModel):
    projects: List[RecommendedProject]


# -------------------------------------------------------------
# Resume Bullet Improver Models
# -------------------------------------------------------------
class BulletImprovementItem(BaseModel):
    original_bullet: str
    improved_bullet: str
    critique: str
    added_strength: str


class ResumeImprovementResponse(BaseModel):
    improvements: List[BulletImprovementItem]


# -------------------------------------------------------------
# Benchmark Models
# -------------------------------------------------------------
class BenchmarkRunResult(BaseModel):
    model_name: str
    model_size_mb: float
    device: str
    execution_provider: str
    input_shape: str
    warmup_iterations: int
    measured_iterations: int
    load_time_ms: float
    first_inference_latency_ms: float
    avg_latency_ms: float
    median_latency_ms: float
    p95_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    throughput_ips: float
    speedup_vs_cpu: Optional[float] = None
    is_simulated: bool = False
    timestamp: str
    notes: str


# -------------------------------------------------------------
# Privacy & Session Models
# -------------------------------------------------------------
class PrivacyStatus(BaseModel):
    local_only_storage: bool = True
    telemetry_enabled: bool = False
    cloud_ai_api_used: bool = False
    zero_retention_external: bool = True
    session_items_count: int = 0
    active_database: str = "SQLite Local"
