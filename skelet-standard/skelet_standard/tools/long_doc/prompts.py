"""
Prompt + skill for long-document reading. Framework-agnostic: only builds
text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

LONG_DOC_SKILL = SkillPrompt(
    name="long-document-reading",
    description=(
        "Navigate a document too long to read in one pass by deciding which "
        "chunk to read next or what to search for, instead of needing the "
        "whole document in context at once. Use whenever a file/document "
        "exceeds a comfortable context size."
    ),
    overview=(
        "The document is pre-split into overlapping chunks. You return a "
        "NavigationDecision: 'read_chunk' (with chunk_index) to view a "
        "specific chunk, 'search' (with query) to find which chunks mention "
        "something, or 'done' once you have what you need."
    ),
    when_to_use=[
        "The document is too large to read in full at once",
        "Only specific sections are relevant to the current task",
    ],
    when_not_to_use=[
        "The document already fits comfortably in context — just read it directly",
    ],
    instructions=[
        "Start by searching for the terms most relevant to the task, rather "
        "than reading chunks sequentially from the start",
        "Read a chunk only when you have a specific reason to believe it's relevant",
        "Track what you've already learned across turns instead of re-reading the same chunk",
        "Return 'done' as soon as you have enough information — don't keep reading speculatively",
    ],
    rules=[
        Rule(
            name="JUSTIFY_EVERY_STEP",
            description="`reason` must explain why this specific action helps the task, not just restate the action",
            priority=Priority.HIGH,
        ),
        Rule(
            name="NO_RANDOM_SCAN",
            description="don't read chunks sequentially with no basis — search first, then target the chunks search surfaced",
            priority=Priority.HIGH,
        ),
        Rule(
            name="STOP_WHEN_SUFFICIENT",
            description="return action='done' once the task can be completed; don't keep navigating past that point",
            priority=Priority.CRITICAL,
        ),
    ],
    edge_cases=[
        "search finds no matching chunks — try a different/broader query before giving up",
        "relevant content straddles a chunk boundary — the chunk overlap should cover this; if not, read the adjacent chunk too",
    ],
    output_format="A NavigationDecision object.",
    validation_checklist=[
        "chunk_index is set when action='read_chunk'",
        "query is set when action='search'",
    ],
)


def build_system_prompt() -> str:
    return LONG_DOC_SKILL.render_body()
