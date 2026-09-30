"""
CareerEdge AI - Comprehensive Skill Ontology & Alias Mapping
Normalizes technical synonyms, standardizes naming, maps parent categories,
and defines related skill bridges (e.g. TensorFlow <-> PyTorch).
"""

from typing import Dict, List, Optional, Tuple, Set


# Canonical category definitions
CATEGORIES = [
    "Programming",
    "ML/AI",
    "Data",
    "Web",
    "Cloud",
    "DevOps",
    "Tools",
    "Soft Skills",
]

# Canonical skill database: canonical_name -> (Category, List[Aliases], List[Related/Bridged Skills])
SKILL_ONTOLOGY_DATA = {
    # ------------------ Programming ------------------
    "Python": ("Programming", ["py", "python3", "python 3"], ["FastAPI", "Pandas", "PyTorch", "NumPy"]),
    "C++": ("Programming", ["cpp", "cplusplus", "c/c++"], ["C", "CUDA", "Embedded Systems"]),
    "C": ("Programming", ["c lang", "ansi c"], ["C++", "Embedded Systems"]),
    "Java": ("Programming", ["java 8", "java 17", "java 21", "jvm"], ["Spring", "Kotlin"]),
    "JavaScript": ("Programming", ["js", "es6", "vanilla js"], ["TypeScript", "Node.js", "React"]),
    "TypeScript": ("Programming", ["ts"], ["JavaScript", "React", "Node.js"]),
    "Go": ("Programming", ["golang"], ["Docker", "Kubernetes", "Microservices"]),
    "Rust": ("Programming", ["rustlang"], ["C++", "WebAssembly", "Systems Programming"]),
    "SQL": ("Programming", ["structured query language", "ansi sql"], ["PostgreSQL", "MySQL", "Data Warehousing"]),
    "R": ("Programming", ["r lang"], ["Statistics", "Data Analysis"]),
    "C#": ("Programming", ["csharp", ".net", "dotnet"], ["Azure"]),

    # ------------------ ML / AI ------------------
    "Machine Learning": ("ML/AI", ["ml", "machine-learning"], ["Scikit-learn", "Deep Learning", "Data Science"]),
    "Deep Learning": ("ML/AI", ["dl", "deep-learning", "neural networks", "ann", "cnn", "rnn"], ["PyTorch", "TensorFlow", "Computer Vision"]),
    "PyTorch": ("ML/AI", ["torch", "pytorch2"], ["Deep Learning", "TensorFlow", "ONNX", "Transformers"]),
    "TensorFlow": ("ML/AI", ["tf", "tf2", "keras"], ["Deep Learning", "PyTorch", "TFLite"]),
    "Scikit-learn": ("ML/AI", ["sklearn", "scikit"], ["Machine Learning", "Pandas", "NumPy"]),
    "Natural Language Processing": ("ML/AI", ["nlp", "text processing", "nlu"], ["Transformers", "LLMs", "BERT", "Tokenizers"]),
    "Computer Vision": ("ML/AI", ["cv", "image processing", "vision"], ["OpenCV", "CNN", "YOLO"]),
    "Large Language Models": ("ML/AI", ["llm", "llms", "generative ai", "genai", "prompt engineering"], ["NLP", "Transformers", "LangChain"]),
    "Transformers": ("ML/AI", ["transformer", "huggingface", "hf", "bert", "roberta"], ["NLP", "PyTorch", "LLMs"]),
    "ONNX": ("ML/AI", ["onnx runtime", "ort", "open neural network exchange"], ["PyTorch", "QNN", "Quantization", "TensorRT"]),
    "Qualcomm QNN": ("ML/AI", ["qnn", "qualcomm neural network", "hexagon npu", "qualcomm ai hub"], ["ONNX", "Quantization", "Edge AI", "NPU"]),
    "Edge AI": ("ML/AI", ["on-device ai", "embedded ai", "tinyml", "edge computing"], ["ONNX", "Qualcomm QNN", "Quantization"]),
    "MLOps": ("ML/AI", ["ml ops", "model deployment", "model monitoring", "mlflow", "dvc"], ["Docker", "Kubernetes", "CI/CD"]),
    "Reinforcement Learning": ("ML/AI", ["rl", "q-learning", "ppo"], ["Machine Learning"]),

    # ------------------ Data ------------------
    "Pandas": ("Data", ["pandas dataframe"], ["NumPy", "Python", "Data Analysis"]),
    "NumPy": ("Data", ["numpy arrays"], ["Pandas", "Python", "SciPy"]),
    "PostgreSQL": ("Data", ["postgres", "pgsql"], ["SQL", "Relational Databases"]),
    "MySQL": ("Data", ["mariadb"], ["SQL"]),
    "MongoDB": ("Data", ["mongo", "nosql"], ["Document Databases"]),
    "Redis": ("Data", ["redis cache"], ["In-Memory Data", "Caching"]),
    "Power BI": ("Data", ["powerbi", "power-bi"], ["Tableau", "Data Visualization", "DAX"]),
    "Tableau": ("Data", ["tableau desktop"], ["Power BI", "Data Visualization"]),
    "Apache Spark": ("Data", ["spark", "pyspark"], ["Big Data", "Hadoop"]),
    "Data Warehousing": ("Data", ["dwh", "snowflake", "bigquery", "redshift"], ["SQL", "ETL"]),
    "ETL": ("Data", ["data pipeline", "data ingestion", "airflow"], ["Python", "SQL", "Spark"]),
    "Statistics": ("Data", ["statistical modeling", "hypothesis testing", "probability"], ["Data Science", "Machine Learning"]),

    # ------------------ Web & Backend ------------------
    "FastAPI": ("Web", ["fastapi framework", "fast-api"], ["Python", "REST APIs", "Pydantic", "Uvicorn"]),
    "Flask": ("Web", ["flask app"], ["Python", "REST APIs", "FastAPI"]),
    "Django": ("Web", ["django rest framework", "drf"], ["Python", "Web Development"]),
    "React": ("Web", ["react.js", "reactjs", "react native"], ["JavaScript", "TypeScript", "Frontend"]),
    "Node.js": ("Web", ["nodejs", "node"], ["JavaScript", "TypeScript", "Express"]),
    "Express": ("Web", ["express.js", "expressjs"], ["Node.js", "REST APIs"]),
    "HTML": ("Web", ["html5"], ["CSS", "Web Development"]),
    "CSS": ("Web", ["css3", "sass", "tailwind", "tailwindcss"], ["HTML", "Web Design"]),
    "REST APIs": ("Web", ["restful api", "rest", "api design"], ["FastAPI", "HTTP", "JSON"]),
    "GraphQL": ("Web", ["graphql api"], ["REST APIs", "Apollo"]),

    # ------------------ Cloud ------------------
    "AWS": ("Cloud", ["amazon web services", "ec2", "s3", "lambda", "sagemaker", "ecs", "eks"], ["Cloud", "Docker"]),
    "Google Cloud Platform": ("Cloud", ["gcp", "google cloud", "vertex ai", "gke", "cloud run"], ["Cloud", "Kubernetes"]),
    "Microsoft Azure": ("Cloud", ["azure", "azure ml", "azure devops"], ["Cloud"]),
    "Serverless": ("Cloud", ["aws lambda", "cloud functions"], ["Cloud", "Microservices"]),

    # ------------------ DevOps & System ------------------
    "Docker": ("DevOps", ["docker container", "dockerfile", "containerization", "containers"], ["Kubernetes", "DevOps", "CI/CD"]),
    "Kubernetes": ("DevOps", ["k8s", "k8", "kube"], ["Docker", "DevOps", "Helm"]),
    "Git": ("DevOps", ["git vcs", "version control"], ["GitHub", "GitLab"]),
    "GitHub": ("DevOps", ["github actions", "gh actions"], ["Git", "CI/CD"]),
    "CI/CD": ("DevOps", ["continuous integration", "continuous deployment", "jenkins", "gitlab ci"], ["DevOps", "GitHub", "Docker"]),
    "Linux": ("DevOps", ["ubuntu", "debian", "rhel", "bash", "shell scripting", "posix"], ["DevOps", "Systems Administration"]),

    # ------------------ Soft Skills & Process ------------------
    "Agile": ("Soft Skills", ["scrum", "kanban", "sprints"], ["Project Management"]),
    "Problem Solving": ("Soft Skills", ["analytical skills", "critical thinking"], []),
    "Team Leadership": ("Soft Skills", ["mentorship", "tech lead", "collaboration"], []),
    "Communication": ("Soft Skills", ["technical writing", "presentation"], []),
}


class SkillOntology:
    """
    Handles skill normalization, synonym resolution, category discovery,
    and related-skill graph analysis.
    """

    def __init__(self):
        self.alias_to_canonical: Dict[str, str] = {}
        self.canonical_to_category: Dict[str, str] = {}
        self.canonical_to_related: Dict[str, List[str]] = {}
        self.canonical_set: Set[str] = set()

        for canonical, (category, aliases, related) in SKILL_ONTOLOGY_DATA.items():
            self.canonical_set.add(canonical)
            self.canonical_to_category[canonical] = category
            self.canonical_to_related[canonical] = related

            # Map canonical itself (lowercase)
            self.alias_to_canonical[canonical.lower()] = canonical

            # Map all declared aliases (lowercase)
            for alias in aliases:
                self.alias_to_canonical[alias.lower()] = canonical

    def normalize(self, term: str) -> Optional[str]:
        """
        Normalizes any input string to its canonical skill name if recognized.
        e.g., 'pytorch' -> 'PyTorch', 'k8s' -> 'Kubernetes', 'tf' -> 'TensorFlow'.
        """
        cleaned = term.strip().lower()
        if not cleaned:
            return None
        return self.alias_to_canonical.get(cleaned, None)

    def get_category(self, canonical_skill: str) -> str:
        """
        Returns the category for a canonical skill, defaulting to 'Other'.
        """
        return self.canonical_to_category.get(canonical_skill, "Other")

    def get_related(self, canonical_skill: str) -> List[str]:
        """
        Returns known related/bridged skills for a canonical skill.
        e.g. PyTorch -> ['Deep Learning', 'TensorFlow', 'ONNX', 'Transformers']
        """
        return self.canonical_to_related.get(canonical_skill, [])

    def are_skills_related(self, skill_a: str, skill_b: str) -> bool:
        """
        Returns True if skill_a and skill_b are recognized related skills or in the same cluster.
        """
        if skill_a.lower() == skill_b.lower():
            return True
        related_a = self.get_related(skill_a)
        related_b = self.get_related(skill_b)
        return skill_b in related_a or skill_a in related_b


# Singleton instance
_ontology: Optional[SkillOntology] = None


def get_skill_ontology() -> SkillOntology:
    global _ontology
    if _ontology is None:
        _ontology = SkillOntology()
    return _ontology
