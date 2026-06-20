"""
Prompt + skill for cited answers. Framework-agnostic: only builds text to
feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

CITATION_SKILL = SkillPrompt(
    name="citation",
    description=(
        "Answer a question while backing every claim with a verbatim quote "
        "from a given source. Use whenever an answer must be traceable back "
        "to source documents instead of taken on the model's word."
    ),
    overview=(
        "You return a CitedAnswer: `answer` plus a list of `citations`, each "
        "with a `source` id and a `quote` copied verbatim from that source. "
        "Quotes are verified by exact substring match against the source — "
        "they are not taken on trust."
    ),
    when_to_use=[
        "An answer is derived from provided source documents and needs to be auditable",
    ],
    when_not_to_use=[
        "There are no source documents to cite against — this skill can't verify claims with nothing to check them against",
    ],
    instructions=[
        "Identify every factual claim in your answer that comes from a source",
        "For each one, copy the exact supporting text into `quote`, character-for-character",
        "Set `source` to the id of the document the quote came from",
        "If a claim can't be backed by an exact quote, rewrite the claim or drop it — don't cite a paraphrase",
    ],
    rules=[
        Rule(
            name="VERBATIM_QUOTE",
            description="`quote` must be copied character-for-character from the source; paraphrasing will fail verification",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="NO_UNCITED_CLAIMS",
            description="every claim in `answer` that depends on a source must have a matching citation",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="CORRECT_SOURCE_ID",
            description="`source` must match the id of the document the quote actually came from, not a guess",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "the same claim is supported by multiple sources — cite all of them, not just one",
        "no source supports a needed claim — say so in `answer` instead of citing something unrelated",
    ],
    output_format="A CitedAnswer object: answer, citations.",
    validation_checklist=[
        "Every citation quote is an exact substring of its source",
        "Every source-dependent claim in `answer` has a citation",
    ],
)


def build_system_prompt() -> str:
    return CITATION_SKILL.render_body()
