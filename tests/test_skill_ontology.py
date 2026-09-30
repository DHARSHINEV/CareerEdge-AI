"""
Unit tests for Skill Ontology, Alias Normalization, and Category Mapping.
"""

from backend.services.skill_ontology import get_skill_ontology


def test_ontology_alias_normalization():
    ontology = get_skill_ontology()
    assert ontology.normalize("ml") == "Machine Learning"
    assert ontology.normalize("pytorch") == "PyTorch"
    assert ontology.normalize("torch") == "PyTorch"
    assert ontology.normalize("postgres") == "PostgreSQL"
    assert ontology.normalize("k8s") == "Kubernetes"
    assert ontology.normalize("docker") == "Docker"
    assert ontology.normalize("nlp") == "Natural Language Processing"
    assert ontology.normalize("cv") == "Computer Vision"
    assert ontology.normalize("gcp") == "Google Cloud Platform"
    assert ontology.normalize("aws") == "AWS"


def test_ontology_categories():
    ontology = get_skill_ontology()
    assert ontology.get_category("Python") == "Programming"
    assert ontology.get_category("Machine Learning") == "ML/AI"
    assert ontology.get_category("PyTorch") == "ML/AI"
    assert ontology.get_category("Docker") == "DevOps"
    assert ontology.get_category("PostgreSQL") == "Data"
    assert ontology.get_category("FastAPI") == "Web"
    assert ontology.get_category("AWS") == "Cloud"


def test_ontology_related_skills():
    ontology = get_skill_ontology()
    assert ontology.are_skills_related("PyTorch", "TensorFlow") is True
    assert ontology.are_skills_related("Machine Learning", "Scikit-learn") is True
    assert ontology.are_skills_related("Docker", "Kubernetes") is True
