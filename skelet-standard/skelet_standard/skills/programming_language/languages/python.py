from skelet.core import Priority, Rule, SkillPrompt

PYTHON_SKILL = SkillPrompt(
    name="language-conventions-python",
    description=(
        "Review a Python snippet against PEP 8 and common Pythonic idioms "
        "— not correctness. Use whenever Python code needs a style pass."
    ),
    overview=(
        "You return a LanguageReview with language='python': a list of "
        "`violations` (rule, location, suggestion) and a one-line `summary`."
    ),
    when_to_use=[
        "Python code needs a style/idiom pass distinct from correctness review",
    ],
    when_not_to_use=[
        "Looking for bugs or logic errors — that's correctness review, not this skill",
    ],
    instructions=[
        "Check naming: snake_case for functions/variables, PascalCase for "
        "classes, UPPER_CASE for constants",
        "Check for non-Pythonic patterns: manual index loops instead of "
        "iteration/enumerate, type(x) == y instead of isinstance, "
        "comparing to None/True/False with == instead of is",
        "Check for missing/incorrect use of context managers (with) for "
        "files, locks, connections",
        "Check list/dict/set comprehensions are used instead of manual "
        "build-up loops where it improves clarity",
        "For each violation, quote the exact location and give a concrete fix",
    ],
    rules=[
        Rule(
            name="PEP8_NAMING",
            description="snake_case functions/variables, PascalCase classes, UPPER_CASE constants",
            priority=Priority.HIGH,
        ),
        Rule(
            name="IDIOMATIC_OVER_MANUAL",
            description="prefer comprehensions, enumerate, context managers, isinstance over manual equivalents",
            priority=Priority.HIGH,
        ),
        Rule(
            name="CONVENTIONS_NOT_BUGS",
            description="only report style/idiom issues; never report correctness bugs under this skill",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="ACTIONABLE_SUGGESTION",
            description="every violation must include a concrete suggested replacement, not just a complaint",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "code intentionally targets Python 2 or a constrained environment — "
        "do not flag idioms that wouldn't work there",
        "snippet is already idiomatic — return an empty `violations` list",
    ],
    output_format="A LanguageReview object with language='python'.",
    validation_checklist=[
        "Every violation has a concrete suggestion",
        "No correctness/logic issues reported here",
    ],
)


def build_system_prompt() -> str:
    return PYTHON_SKILL.render_body()
