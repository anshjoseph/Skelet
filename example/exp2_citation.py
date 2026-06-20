"""
Citation tool example: a model's CitedAnswer is only trusted after every
quote is verified against the actual source text.

Run with both packages installed:
    pip install -e .
    pip install -e skelet-standard
    python example/exp2_citation.py
"""

from skelet_standard.tools.citation import (
    Citation,
    CitedAnswer,
    CitationNotFound,
    build_system_prompt,
    verify_citations,
)

print(build_system_prompt())
print("\n" + "=" * 80 + "\n")

sources = {
    "policy.md": "Refunds are issued within 14 days of the original purchase.",
}

# A correct, verifiable answer from the model.
good = CitedAnswer(
    answer="Refunds are issued within 14 days of purchase.",
    citations=[
        Citation(
            source="policy.md",
            quote="Refunds are issued within 14 days of the original purchase.",
        )
    ],
)
verify_citations(good, sources)
print("good answer: citation verified")

# A hallucinated citation — quote doesn't actually appear in the source.
bad = CitedAnswer(
    answer="Refunds are issued within 30 days.",
    citations=[Citation(source="policy.md", quote="Refunds are issued within 30 days.")],
)
try:
    verify_citations(bad, sources)
except CitationNotFound as e:
    print(f"bad answer rejected: {e}")
