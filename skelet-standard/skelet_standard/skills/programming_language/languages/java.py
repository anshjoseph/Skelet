from skelet.core import Priority, Rule, SkillPrompt

JAVA_SKILL = SkillPrompt(
    name="language-conventions-java",
    description=(
        "Review a Java snippet against standard Java naming/style "
        "conventions and common idioms — not correctness. Use whenever "
        "Java code needs a style pass."
    ),
    overview=(
        "You return a LanguageReview with language='java': a list of "
        "`violations` (rule, location, suggestion) and a one-line `summary`."
    ),
    when_to_use=[
        "Java code needs a style/idiom pass distinct from correctness review",
    ],
    when_not_to_use=[
        "Looking for bugs or logic errors — that's correctness review, not this skill",
    ],
    instructions=[
        "Check naming: camelCase for methods/variables, PascalCase for "
        "classes/interfaces, UPPER_SNAKE_CASE for static final constants",
        "Check for missing use of try-with-resources for Closeable/AutoCloseable",
        "Check for use of == on boxed types (Integer, Long, etc) instead of .equals()",
        "Check for raw types instead of generics, and missing @Override annotations",
        "Check visibility: fields should generally be private with accessors, "
        "not exposed public",
        "For each violation, quote the exact location and give a concrete fix",
    ],
    rules=[
        Rule(
            name="JAVA_NAMING",
            description="camelCase methods/variables, PascalCase classes/interfaces, UPPER_SNAKE_CASE static finals",
            priority=Priority.HIGH,
        ),
        Rule(
            name="RESOURCE_SAFETY",
            description="Closeable/AutoCloseable resources should use try-with-resources, not manual close()",
            priority=Priority.HIGH,
        ),
        Rule(
            name="BOXED_EQUALITY",
            description="boxed types (Integer, Long, etc) must be compared with .equals(), not ==",
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
        "code targets a constrained/older JDK that lacks a suggested feature "
        "— note the constraint instead of flagging it as a violation",
        "snippet is already idiomatic — return an empty `violations` list",
    ],
    output_format="A LanguageReview object with language='java'.",
    validation_checklist=[
        "Every violation has a concrete suggestion",
        "No correctness/logic issues reported here",
    ],
)


def build_system_prompt() -> str:
    return JAVA_SKILL.render_body()
