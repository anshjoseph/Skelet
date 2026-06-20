"""
Prompt + skill for compaction. Framework-agnostic: only builds text to feed
to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

COMPACTION_SKILL = SkillPrompt(
    name="compaction",
    description=(
        "Compress long content (conversation history, logs, docs) into a "
        "shorter form while being explicit about what was kept and what was "
        "dropped. Use whenever content needs to fit a smaller budget without "
        "silently losing important facts."
    ),
    overview=(
        "You return a CompactionResult: a `summary` (the compacted text), "
        "`preserved_facts` (what you deliberately kept), and `dropped` (what "
        "you deliberately removed, and why it was safe to remove)."
    ),
    when_to_use=[
        "Content exceeds a target size/token budget and must be shortened",
        "Old context needs to be condensed before continuing a task",
    ],
    when_not_to_use=[
        "The content is already short enough — don't compact for its own sake",
        "Losing any detail would be unacceptable (e.g. legal/contractual text) "
        "— flag that instead of compacting",
    ],
    instructions=[
        "Identify facts, decisions, constraints, and open questions that "
        "matter for future use of this content",
        "Write the shortest summary that preserves all of them",
        "List every fact you kept in `preserved_facts`",
        "List what you removed in `dropped`, with enough detail that the "
        "caller can tell whether the removal was safe",
    ],
    rules=[
        Rule(
            name="NO_SILENT_LOSS",
            description=(
                "every fact dropped from the original must appear in `dropped`. "
                "Never shrink content by silently omitting something — the "
                "caller must be able to see what was lost."
            ),
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="NO_INVENTION",
            description="never add facts, numbers, or claims that were not in the original content",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="PRESERVE_DECISIONS",
            description="decisions and constraints take priority over narrative/explanation when space is limited",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "content has no compactable redundancy — return it close to as-is and "
        "say so, rather than forcing a cut that drops real information",
    ],
    output_format="A CompactionResult object: summary, preserved_facts, dropped.",
    validation_checklist=[
        "Every dropped fact is listed in `dropped`, not silently gone",
        "No invented facts in `summary`",
    ],
)


def build_system_prompt() -> str:
    return COMPACTION_SKILL.render_body()
