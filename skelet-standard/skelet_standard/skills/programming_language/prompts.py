"""
Prompt + skill for language-convention review. Framework-agnostic: only
builds text to feed to whatever model client the caller is using.

LANGUAGE_SKILL is a generic fallback that asks the model to apply whatever
conventions are established for the given language. For languages with a
well-known, widely-agreed style guide, a specific skill (e.g. PYTHON_SKILL,
JAVA_SKILL) bakes those conventions in directly instead of relying on the
model to recall them — more reliable, and lets a project pin its own rules.
"""

from skelet.core import Priority, Rule, SkillPrompt

LANGUAGE_SKILL = SkillPrompt(
    name="language-conventions",
    description=(
        "Review a code snippet against the idioms/conventions of the "
        "language it's written in (naming, formatting, idiomatic patterns) "
        "— not correctness. Use whenever code needs to be checked for style "
        "rather than bugs, and no language-specific skill is available."
    ),
    overview=(
        "You return a LanguageReview: the detected/given `language`, a list "
        "of `violations` (rule, location, suggestion), and a one-line "
        "`summary`."
    ),
    when_to_use=[
        "Code needs a style/idiom pass distinct from correctness review",
        "Enforcing a language's established conventions (PEP 8, gofmt idioms, etc)",
    ],
    when_not_to_use=[
        "Looking for bugs or logic errors — that's correctness review, not this skill",
        "The language has no snippet-visible conventions to check (e.g. plain config/data files)",
    ],
    instructions=[
        "Identify the language if not given explicitly",
        "Compare the snippet against that language's established conventions "
        "(official style guide if one exists, otherwise widely-accepted idioms)",
        "For each violation, quote the exact location and give a concrete fix",
        "Do not flag stylistic preferences that aren't an established convention",
    ],
    rules=[
        Rule(
            name="CONVENTIONS_NOT_BUGS",
            description="only report style/idiom issues; never report correctness bugs under this skill",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="ESTABLISHED_ONLY",
            description="only flag conventions that are widely established for the language, not personal preference",
            priority=Priority.HIGH,
        ),
        Rule(
            name="ACTIONABLE_SUGGESTION",
            description="every violation must include a concrete suggested replacement, not just a complaint",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "snippet mixes languages (e.g. SQL embedded in Python) — review each part against its own conventions",
        "snippet is already idiomatic — return an empty `violations` list, not invented nitpicks",
    ],
    output_format="A LanguageReview object: language, violations, summary.",
    validation_checklist=[
        "Every violation has a concrete suggestion",
        "No correctness/logic issues reported here",
    ],
)


def build_system_prompt() -> str:
    return LANGUAGE_SKILL.render_body()
