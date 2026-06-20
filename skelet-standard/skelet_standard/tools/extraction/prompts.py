"""
Prompt + skill for structured extraction. Framework-agnostic: only builds
text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

EXTRACTION_SKILL = SkillPrompt(
    name="structured-extraction",
    description=(
        "Pull a specific set of fields out of unstructured text into "
        "key/value pairs. Use whenever structured data needs to be lifted "
        "out of free text (forms, emails, documents) instead of read manually."
    ),
    overview=(
        "You return an ExtractionResult: `fields` (only fields actually "
        "found, by name) and `missing_fields` (requested fields that were "
        "not present)."
    ),
    when_to_use=[
        "A known set of fields needs to be pulled from free text into structured form",
    ],
    when_not_to_use=[
        "The fields aren't known in advance — that's open-ended extraction, not this skill",
    ],
    instructions=[
        "Look for each requested field in the source text",
        "Put found values in `fields`, using the exact field name requested as the key",
        "List any requested field not found in `missing_fields` — do not omit it silently and do not guess a value",
    ],
    rules=[
        Rule(
            name="NO_INVENTED_VALUES",
            description="never put a guessed or inferred-beyond-the-text value into `fields` — if it's not actually there, list it in `missing_fields` instead",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="EXPLICIT_MISSING",
            description="every requested field that isn't found must appear in `missing_fields`, not be left out of both",
            priority=Priority.CRITICAL,
        ),
    ],
    edge_cases=[
        "a field appears more than once with conflicting values — use the most authoritative/most recent occurrence and note the conflict if the schema allows it",
        "a field is present but ambiguous — prefer marking it missing over guessing",
    ],
    output_format="An ExtractionResult object: fields, missing_fields.",
    validation_checklist=[
        "No invented values in fields",
        "Every requested-but-absent field is listed in missing_fields",
    ],
)


def build_system_prompt() -> str:
    return EXTRACTION_SKILL.render_body()
