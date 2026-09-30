"""
CareerEdge AI - Unified AI Engine Abstraction
Implements strict architectural separation:
  - LocalEmbeddingEngine
  - LocalGenerationEngine
  - NPUInferenceEngine
  - CPUFallbackEngine
Allows the career intelligence pipeline to run seamlessly across Snapdragon NPU and CPU.
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

from ai.embeddings.local_embeddings import get_embedding_engine, LocalEmbeddingEngine
from backend.engine.qnn_runtime import get_runtime_manager, QNNRuntimeManager

logger = logging.getLogger("careeredge.ai_engine")


class NPUInferenceEngine:
    """
    Handles inference routed specifically to the Qualcomm Hexagon NPU
    via ONNX Runtime QNN Execution Provider.
    """

    def __init__(self, runtime_mgr: QNNRuntimeManager):
        self.runtime_mgr = runtime_mgr

    def is_active(self) -> bool:
        return self.runtime_mgr.active_provider == "QNNExecutionProvider"

    def execute(self, inputs: Dict[str, np.ndarray]) -> Tuple[List[np.ndarray], float]:
        if not self.is_active():
            raise RuntimeError("NPUInferenceEngine invoked but QNNExecutionProvider is not active.")
        return self.runtime_mgr.run_inference(inputs)


class CPUFallbackEngine:
    """
    Handles inference on host CPU (x86_64 or ARM64) when NPU/QNN is not present.
    """

    def __init__(self, runtime_mgr: QNNRuntimeManager):
        self.runtime_mgr = runtime_mgr

    def is_active(self) -> bool:
        return self.runtime_mgr.active_provider != "QNNExecutionProvider"

    def execute(self, inputs: Dict[str, np.ndarray]) -> Tuple[List[np.ndarray], float]:
        return self.runtime_mgr.run_inference(inputs)


class LocalGenerationEngine:
    """
    Deterministic & rule-augmented local generation engine for explainable
    career recommendations, gap explanations, roadmaps, and resume improvements.
    Guarantees no hallucinated metrics and 100% offline predictability.
    """

    def __init__(self, embedding_engine: LocalEmbeddingEngine):
        self.embedding_engine = embedding_engine

    def explain_gap(
        self,
        skill: str,
        category: str,
        target_role: str,
        is_required: bool,
        related_skills: List[str],
    ) -> Dict[str, Any]:
        """
        Synthesizes an explainable, fact-grounded gap analysis for a missing or partial skill.
        """
        importance = "Critical (Required Requirement)" if is_required else "Secondary (Preferred Qualification)"
        
        evidence_str = (
            f"No direct evidence or verified projects utilizing {skill} were detected in the resume."
            if not related_skills
            else f"Found related background in ({', '.join(related_skills)}), but direct proficiency in {skill} is not demonstrated."
        )

        why_reasons = {
            "ML/AI": f"In {target_role} roles, {skill} is essential for designing, training, or deploying machine learning pipelines in production.",
            "Programming": f"{skill} is the foundational language used for engineering the core logic, algorithms, and services in this role.",
            "Cloud": f"Modern {target_role} workflows require deploying and scaling architectures on {skill} infrastructure.",
            "DevOps": f"{skill} ensures containerization, continuous integration, and reproducible environments across development and production.",
            "Data": f"Data processing, validation, and feature engineering depend on strong competence with {skill}.",
            "Web": f"Building interfaces, REST APIs, or data visualization relies on {skill}.",
        }
        why_it_matters = why_reasons.get(
            category,
            f"Demonstrating {skill} provides direct alignment with the key responsibilities of a {target_role}."
        )

        learning_topics = {
            "Docker": ["Container lifecycle and Dockerfiles", "Multi-stage builds for Python/C++ apps", "Docker Compose for multi-container services"],
            "PyTorch": ["Tensor operations & autograd", "Custom Dataset & DataLoader pipelines", "Model export to ONNX & quantization"],
            "AWS": ["EC2, S3, and IAM basics", "Lambda serverless functions", "SageMaker model endpoints"],
            "Kubernetes": ["Pods, Deployments, and Services", "ConfigMaps & Secrets", "Helm chart packaging"],
            "SQL": ["Complex JOINs and aggregation", "Window functions & subqueries", "Indexing & query optimization"],
            "FastAPI": ["Async path operations & Pydantic models", "Dependency injection", "OpenAPI docs & testing"],
            "MLOps": ["Model versioning with MLflow/DVC", "Automated training pipelines", "Monitoring data drift"],
        }
        what_to_learn = learning_topics.get(skill, [
            f"Core fundamentals and standard libraries of {skill}",
            f"Best practices and idioms for {skill} in {target_role} stacks",
            f"Production testing and integration patterns with {skill}",
        ])

        project_ideas = {
            "Docker": f"Containerize a local {target_role} inference service with health checks and volume persistence.",
            "PyTorch": "Train a custom transformer or CNN classifier, export to ONNX format, and benchmark inference latency.",
            "AWS": "Deploy a serverless data ingestion or model prediction API with automated CI/CD to AWS ECS/Lambda.",
            "Kubernetes": "Deploy a scalable microservice cluster with horizontal pod autoscaling and ingress controllers.",
            "SQL": "Design an analytics schema with automated query benchmarks and window aggregation for real-world telemetry.",
        }
        rec_project = project_ideas.get(
            skill,
            f"Build an end-to-end portfolio application showcasing {skill} solving a domain problem in {target_role}."
        )

        guide = (
            f"Add a dedicated bullet under Projects or Experience: 'Implemented [Feature] using {skill}, "
            f"achieving [insert measured outcome, e.g., 35% speedup or automated test coverage].'"
        )

        return {
            "skill": skill,
            "category": category,
            "importance": importance,
            "why_it_matters": why_it_matters,
            "evidence_missing": evidence_str,
            "what_to_learn": what_to_learn,
            "recommended_project": rec_project,
            "resume_demonstration_guide": guide,
        }


class AIEngine:
    """
    Unified Top-Level AI Engine.
    Dispatches between NPU and CPU engines and coordinates semantic embeddings.
    """

    def __init__(self):
        self.runtime_mgr = get_runtime_manager()
        self.embedding_engine = get_embedding_engine()
        self.npu_engine = NPUInferenceEngine(self.runtime_mgr)
        self.cpu_engine = CPUFallbackEngine(self.runtime_mgr)
        self.generation_engine = LocalGenerationEngine(self.embedding_engine)

    def get_active_inference_engine(self):
        if self.npu_engine.is_active():
            return self.npu_engine
        return self.cpu_engine

    def encode_texts(self, texts: List[str]) -> Tuple[np.ndarray, float]:
        return self.embedding_engine.encode(texts)

    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        return self.embedding_engine.compute_similarity(vec1, vec2)

    def get_status(self) -> Dict[str, Any]:
        status = self.runtime_mgr.get_runtime_status()
        status["npu_engine_active"] = self.npu_engine.is_active()
        status["cpu_fallback_active"] = self.cpu_engine.is_active()
        return status


# Singleton instance
_ai_engine: Optional[AIEngine] = None


def get_ai_engine() -> AIEngine:
    global _ai_engine
    if _ai_engine is None:
        _ai_engine = AIEngine()
    return _ai_engine
