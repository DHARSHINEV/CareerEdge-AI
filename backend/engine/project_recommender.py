"""
CareerEdge AI - Project Recommendation Engine
Generates portfolio project blueprints engineered specifically to bridge the candidate's
exact missing skills into verified, resume-ready evidence.
"""

from typing import List, Dict, Any, Set
from backend.models.schemas import RecommendedProject, ProjectRecommendationResponse, SkillMatchDetail


# Curated catalog of engineering projects categorized by tech stack combinations
PROJECT_CATALOG = [
    {
        "title": "On-Device Edge AI Inference Engine & Benchmarking Suite",
        "primary_skills": ["ONNX", "Qualcomm QNN", "PyTorch", "Edge AI"],
        "difficulty": "Intermediate",
        "estimated_timeline": "2-3 weeks",
        "summary": "Train and quantize a compact Transformer or Vision model, export to ONNX format, and run accelerated inference via Qualcomm QNN Execution Provider on Snapdragon NPU with graceful CPU fallback.",
        "architecture": "PyTorch Model Training -> ONNX Graph Export -> INT8 Quantization -> ONNX Runtime Inference Session -> Hexagon NPU / CPU Fallback -> Latency Benchmark Dashboard.",
        "deliverables": [
            "Quantized ONNX model artifact (<30MB)",
            "Automated benchmark script comparing NPU vs CPU latency",
            "FastAPI microservice for local embeddings or classification",
        ],
        "resume_bullet_sample": "Engineered an on-device Edge AI inference pipeline using PyTorch, ONNX Runtime, and Qualcomm QNN, achieving [insert measured latency, e.g. 5.2ms] inference on Snapdragon NPU with CPU fallback.",
    },
    {
        "title": "Containerized ML Microservice with Automated CI/CD",
        "primary_skills": ["Docker", "FastAPI", "CI/CD", "GitHub"],
        "difficulty": "Intermediate",
        "estimated_timeline": "1-2 weeks",
        "summary": "Build and containerize an asynchronous REST API serving machine learning predictions, complete with multi-stage Docker builds, health checks, and GitHub Actions continuous integration.",
        "architecture": "Client Request -> FastAPI Async Router -> Pydantic Validation -> ML Pipeline -> Multi-stage Docker Container -> GitHub Actions Automated Test Suite.",
        "deliverables": [
            "Production Dockerfile with non-root user and minimal image footprint",
            "GitHub Actions workflow running unit tests on every pull request",
            "Interactive Swagger/OpenAPI documentation",
        ],
        "resume_bullet_sample": "Architected and containerized a high-throughput ML inference microservice using FastAPI and Docker, integrating automated GitHub Actions CI/CD to maintain [insert test coverage, e.g. 94%] test coverage.",
    },
    {
        "title": "Scalable Cloud Data Ingestion & Model Serving on AWS",
        "primary_skills": ["AWS", "Python", "SQL", "Docker"],
        "difficulty": "Advanced",
        "estimated_timeline": "3-4 weeks",
        "summary": "Design a serverless or containerized data processing architecture on AWS that ingests raw telemetry, stores structured records in PostgreSQL, and generates real-time predictions.",
        "architecture": "Data Ingestion -> AWS Lambda / API Gateway -> S3 Storage -> PostgreSQL RDS -> Docker Container on AWS ECS / App Runner.",
        "deliverables": [
            "Infrastructure-as-code or deployment scripts for AWS services",
            "PostgreSQL schema with indexing and aggregation queries",
            "Load test report demonstrating handling of concurrent requests",
        ],
        "resume_bullet_sample": "Deployed a cloud-native model serving pipeline on AWS using Docker, S3, and PostgreSQL, processing [insert batch size or requests/sec] with automated data validation.",
    },
    {
        "title": "Distributed Task Orchestration & Microservices on Kubernetes",
        "primary_skills": ["Kubernetes", "Docker", "DevOps", "Go"],
        "difficulty": "Advanced",
        "estimated_timeline": "3 weeks",
        "summary": "Package a multi-service web application into Kubernetes manifests with horizontal pod autoscalers, service discovery, ConfigMaps, and cluster monitoring.",
        "architecture": "Ingress Controller -> Front-end Service Pods -> ClusterIP -> Back-end Worker Deployment -> Horizontal Pod Autoscaler -> Local Minikube / K3s Cluster.",
        "deliverables": [
            "Production Kubernetes manifests (Deployments, Services, Ingress, HPA)",
            "Helm chart for unified one-command cluster deployment",
            "Grafana/Prometheus metrics dashboard monitoring cluster load",
        ],
        "resume_bullet_sample": "Designed and deployed a resilient microservice architecture on Kubernetes with Docker and Helm, configuring horizontal autoscaling to handle [insert traffic increase] spikes without downtime.",
    },
    {
        "title": "End-to-End Deep Learning Classification & PyTorch Pipeline",
        "primary_skills": ["PyTorch", "Deep Learning", "Computer Vision", "Machine Learning"],
        "difficulty": "Intermediate",
        "estimated_timeline": "2 weeks",
        "summary": "Implement a custom convolutional neural network or fine-tune a vision transformer for domain classification, incorporating data augmentation, learning rate scheduling, and model checkpointing.",
        "architecture": "Dataset Pipeline (Torchvision) -> Custom PyTorch Model -> Cross-Entropy Loss with AdamW -> Checkpoint Management -> Evaluation Metrics (Precision/Recall/F1).",
        "deliverables": [
            "Modular PyTorch training and evaluation scripts",
            "Confusion matrix and learning curves visualization",
            "Exported ONNX model ready for deployment",
        ],
        "resume_bullet_sample": "Trained and evaluated a PyTorch deep learning classifier for [insert domain], achieving [insert measured metric, e.g. 92.4% F1-score] with ONNX export for low-latency inference.",
    },
    {
        "title": "High-Performance Analytics Warehouse & Query Engine",
        "primary_skills": ["SQL", "PostgreSQL", "Data Warehousing", "ETL"],
        "difficulty": "Intermediate",
        "estimated_timeline": "2 weeks",
        "summary": "Construct an analytics star-schema data warehouse in PostgreSQL with automated ETL pipelines, window functions, and query optimization for large tabular datasets.",
        "architecture": "Raw CSV/Parquet -> Python ETL Ingestion -> Staging Tables -> Star Schema (Fact & Dimensions) -> Indexed Views -> Analytics Dashboards.",
        "deliverables": [
            "DDL schema with foreign keys, constraints, and indexes",
            "ETL script with idempotency and transaction safety",
            "Benchmark showing execution time reduction for analytical queries",
        ],
        "resume_bullet_sample": "Engineered an analytics data warehouse in PostgreSQL with automated Python ETL pipelines, optimizing query execution times by [insert measured speedup, e.g. 60%] via strategic indexing.",
    },
]


class ProjectRecommenderEngine:
    """
    Selects and tailors project recommendations based on detected skill gaps.
    """

    def recommend(
        self,
        critical_gaps: List[SkillMatchDetail],
        target_role: str,
    ) -> ProjectRecommendationResponse:
        gap_skills_set = set(g.requirement.lower() for g in critical_gaps)
        if not gap_skills_set:
            gap_skills_set = {"docker", "pytorch", "aws"}

        # Score catalog projects by how many missing skills they bridge
        scored_projects = []
        for proj in PROJECT_CATALOG:
            overlap = 0
            matched_skills = []
            for s in proj["primary_skills"]:
                if s.lower() in gap_skills_set:
                    overlap += 2
                    matched_skills.append(s)
                else:
                    matched_skills.append(s)

            scored_projects.append((overlap, matched_skills, proj))

        # Sort descending by overlap score
        scored_projects.sort(key=lambda x: x[0], reverse=True)

        recommendations: List[RecommendedProject] = []
        for score, matched, proj in scored_projects[:3]:
            recommendations.append(
                RecommendedProject(
                    title=proj["title"],
                    target_skills=proj["primary_skills"],
                    difficulty=proj["difficulty"],
                    estimated_timeline=proj["estimated_timeline"],
                    summary=proj["summary"],
                    architecture=proj["architecture"],
                    deliverables=proj["deliverables"],
                    resume_bullet_sample=proj["resume_bullet_sample"],
                )
            )

        return ProjectRecommendationResponse(projects=recommendations)


# Singleton instance
_project_recommender = None


def get_project_recommender() -> ProjectRecommenderEngine:
    global _project_recommender
    if _project_recommender is None:
        _project_recommender = ProjectRecommenderEngine()
    return _project_recommender
