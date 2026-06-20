"""
Compaction data model — framework-agnostic.

Compaction means compressing long content (a conversation, logs, docs) into
a shorter form while being explicit about what was kept and what was
dropped, so the caller can decide whether anything important was lost.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class CompactionResult(BaseModel):
    summary: str = Field(description="the compacted/compressed version of the content")
    preserved_facts: List[str] = Field(
        default_factory=list,
        description="key facts, decisions, or constraints from the original content that were kept",
    )
    dropped: List[str] = Field(
        default_factory=list,
        description=(
            "things explicitly removed because they were redundant, stale, or "
            "low-value — listed so the caller can see what was lost, not just "
            "what was kept"
        ),
    )


def compression_ratio(original: str, result: CompactionResult) -> float:
    """Rough size reduction ratio (0..1, higher = more compacted). Length-based,
    not token-based — good enough as a sanity check, not a precise budget."""
    if not original:
        return 0.0
    return 1 - (len(result.summary) / len(original))
