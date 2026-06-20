from skelet_standard.skills.programming_language.languages.java import JAVA_SKILL
from skelet_standard.skills.programming_language.languages.python import PYTHON_SKILL

REGISTRY = {
    "python": PYTHON_SKILL,
    "java": JAVA_SKILL,
}

__all__ = ["JAVA_SKILL", "PYTHON_SKILL", "REGISTRY"]
