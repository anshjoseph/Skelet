"""
Prompt + skill for the search/replace patch tool. Framework-agnostic: this
only builds text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

PATCH_SKILL = SkillPrompt(
    name="search-replace-patching",
    description=(
        "Generate edits as search/replace blocks instead of line-number "
        "diffs. Use whenever you need to propose changes to existing "
        "content without being able to reliably count lines."
    ),
    overview=(
        "You give a `search` block (the EXACT existing text, copied verbatim) "
        "and a `replace` block (the new text). The system finds `search` in "
        "the content and swaps it for `replace`."
    ),
    when_to_use=[
        "Proposing edits to existing content via the Patchs structured output",
    ],
    when_not_to_use=[
        "Creating brand new content from scratch (just write it directly)",
    ],
    instructions=[
        "Read the content shown below (line numbers are for your reference "
        "only — never feed them back into a patch, only exact text)",
        "For each change, copy the exact existing snippet into `search`",
        "Write the replacement snippet into `replace`",
        "If the same snippet appears more than once, expand `search` with "
        "extra surrounding lines (e.g. a nearby comment) so it matches only "
        "once, rather than setting `occurrence` unless truly unavoidable",
    ],
    rules=[
        Rule(
            name="EXACT_MATCH",
            description=(
                "the `search` block must be copied character-for-character "
                "from the source, including whitespace/indentation, or it "
                "will not be found."
            ),
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="UNIQUE_SEARCH",
            description=(
                "the `search` block must match exactly once in the content. "
                "Avoid generic snippets (bare loop headers, blank lines) "
                "that might repeat elsewhere — include enough context to "
                "make the match unique."
            ),
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="NO_DUPLICATE_PATCHES",
            description=(
                "do not propose two patches whose `search` blocks overlap "
                "or target the same change twice."
            ),
            priority=Priority.CRITICAL,
        ),
    ],
    edge_cases=[
        "search text legitimately repeats and cannot be made unique with "
        "more context — set `occurrence` to the 1-based match index",
    ],
    output_format="A Patchs object: a summary plus a list of Patch objects.",
    validation_checklist=[
        "Every search block is unique (or has an explicit occurrence)",
        "No two patches target overlapping text",
    ],
)


def build_system_prompt() -> str:
    return PATCH_SKILL.render_body()
