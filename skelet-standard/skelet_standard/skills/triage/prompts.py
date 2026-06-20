"""
Prompt + skill for triage. Framework-agnostic: only builds text to feed to
whatever model client the caller is using.
"""

from skelet.core import Priority as RulePriority
from skelet.core import Rule, SkillPrompt

TRIAGE_SKILL = SkillPrompt(
    name="triage",
    description=(
        "Classify and prioritize an incoming item (ticket, bug report, "
        "support request) so it can be routed. Use whenever incoming items "
        "need consistent categorization before being handled."
    ),
    overview=(
        "You return a Triage: `category`, `priority`, `rationale`, and "
        "`duplicate_of` if the item is clearly a duplicate of something "
        "referenced in the given context."
    ),
    when_to_use=[
        "An incoming item needs to be categorized and prioritized before routing",
    ],
    when_not_to_use=[
        "The item already has a definitive category/priority from policy — don't re-triage what's already decided",
    ],
    instructions=[
        "Read the item and assign the category that best matches its content, not its phrasing",
        "Set priority based on actual impact/urgency described, not the reporter's tone",
        "Explain the reasoning briefly in `rationale`",
        "Only set `duplicate_of` if there's a clear, specific match in the given context — never guess",
    ],
    rules=[
        Rule(
            name="IMPACT_OVER_TONE",
            description="priority reflects actual described impact/urgency, not how dramatically the reporter wrote it",
            priority=RulePriority.CRITICAL,
        ),
        Rule(
            name="NO_GUESSED_DUPLICATES",
            description="only set duplicate_of when the context actually shows a matching existing item; never guess",
            priority=RulePriority.HIGH,
        ),
        Rule(
            name="CONSISTENT_CATEGORIES",
            description="reuse the same category labels already established in context, rather than inventing new ones for the same kind of issue",
            priority=RulePriority.HIGH,
        ),
    ],
    edge_cases=[
        "item is ambiguous between two categories — pick the more actionable one and say so in `rationale`",
        "item looks like spam/abuse — category should reflect that rather than triaging it as a normal request",
    ],
    output_format="A Triage object: category, priority, rationale, duplicate_of.",
    validation_checklist=[
        "priority matches described impact, not tone",
        "duplicate_of is only set with a real match in context",
    ],
)


def build_system_prompt() -> str:
    return TRIAGE_SKILL.render_body()
