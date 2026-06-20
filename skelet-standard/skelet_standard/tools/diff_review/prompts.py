"""
Prompt + skill for diff review. Framework-agnostic: only builds text to
feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

DIFF_REVIEW_SKILL = SkillPrompt(
    name="diff-review",
    description=(
        "Review a code diff and produce structured comments tied to exact "
        "quoted locations, with a severity per comment. Use whenever a diff "
        "needs review before merging."
    ),
    overview=(
        "You return a DiffReview: `summary` plus a list of `comments`, each "
        "with a `location` (exact quoted snippet), `severity`, `comment`, "
        "and an optional `suggestion`."
    ),
    when_to_use=[
        "A diff/PR needs review feedback before merging",
    ],
    when_not_to_use=[
        "Reviewing a whole file with no diff context — review the change, not the unrelated surrounding code",
    ],
    instructions=[
        "Focus only on lines actually changed by the diff, not pre-existing code left untouched",
        "For each issue, quote the exact changed snippet into `location`",
        "Assign severity honestly: 'blocking' only for things that must be fixed before merge, "
        "'info' for optional notes",
        "Give a concrete `suggestion` whenever the fix is clear",
    ],
    rules=[
        Rule(
            name="DIFF_SCOPE_ONLY",
            description="only comment on lines the diff actually changes, not pre-existing unrelated code",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="HONEST_SEVERITY",
            description="don't inflate severity to 'blocking' for stylistic nitpicks, and don't downplay real correctness/security issues as 'info'",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="EXACT_LOCATION",
            description="`location` must be an exact quoted snippet from the diff, not a paraphrase or a line number",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "the diff is correct and idiomatic — return an empty `comments` list rather than inventing nitpicks",
        "an issue affects code the diff didn't touch but the diff depends on — note it as 'info', not 'blocking', since it's outside the diff's scope",
    ],
    output_format="A DiffReview object: summary, comments.",
    validation_checklist=[
        "Every comment's location is an exact snippet from the diff",
        "No comment targets code outside the diff's changed lines",
    ],
)


def build_system_prompt() -> str:
    return DIFF_REVIEW_SKILL.render_body()
