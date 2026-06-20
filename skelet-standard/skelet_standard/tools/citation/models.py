"""
Citation data model — framework-agnostic.

An answer that cites sources is only trustworthy if every citation can be
verified to actually appear in the cited source. The model produces quotes
and source ids; verification (does the quote really appear there) is pure
deterministic logic, not left to the model's word.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CitationError(Exception):
    """Base class for all citation-verification failures."""


class CitationNotFound(CitationError):
    def __init__(self, source: str, quote: str):
        self.source = source
        self.quote = quote
        super().__init__(f"Quote not found in source '{source}': {quote!r}")


class UnknownSource(CitationError):
    def __init__(self, source: str):
        self.source = source
        super().__init__(f"Citation references unknown source: {source!r}")


class Citation(BaseModel):
    source: str = Field(description="id/name of the source document this citation refers to")
    quote: str = Field(description="the exact text from the source that supports the claim, copied verbatim")
    note: Optional[str] = Field(default=None, description="optional explanation of how this quote supports the claim")


class CitedAnswer(BaseModel):
    answer: str = Field(description="the answer to the question/task")
    citations: List[Citation] = Field(default_factory=list, description="every citation backing a claim in `answer`")


def verify_citations(cited: CitedAnswer, sources: Dict[str, str]) -> None:
    """
    Raise CitationNotFound / UnknownSource for the first citation that can't
    be verified against `sources` (source id -> full source text). Never
    silently accepts an unverifiable citation.
    """
    for citation in cited.citations:
        if citation.source not in sources:
            raise UnknownSource(citation.source)
        if citation.quote not in sources[citation.source]:
            raise CitationNotFound(citation.source, citation.quote)


def find_unverifiable_citations(cited: CitedAnswer, sources: Dict[str, str]) -> List[Citation]:
    """Non-raising variant: return every citation that fails verification instead of stopping at the first one."""
    bad: List[Citation] = []
    for citation in cited.citations:
        if citation.source not in sources or citation.quote not in sources[citation.source]:
            bad.append(citation)
    return bad
