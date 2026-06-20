from skelet_standard.skills.programming_language.languages import JAVA_SKILL, PYTHON_SKILL, REGISTRY
from skelet_standard.skills.programming_language.models import ConventionViolation, LanguageReview
from skelet_standard.skills.programming_language.prompts import LANGUAGE_SKILL, build_system_prompt


def build_system_prompt_for(language: str) -> str:
    """Use the language-specific skill if one is registered, otherwise fall
    back to the generic LANGUAGE_SKILL."""
    skill = REGISTRY.get(language.lower())
    return skill.render_body() if skill else build_system_prompt()


__all__ = [
    "ConventionViolation",
    "LanguageReview",
    "LANGUAGE_SKILL",
    "PYTHON_SKILL",
    "JAVA_SKILL",
    "REGISTRY",
    "build_system_prompt",
    "build_system_prompt_for",
]
