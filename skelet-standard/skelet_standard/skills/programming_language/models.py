"""
Language-convention data model — framework-agnostic.

Given a snippet and the language it's written in, produce a review of
where it violates that language's idioms/conventions (not correctness bugs
— that's a different skill). Works for any language; the model supplies
the language-specific knowledge, this just shapes the output.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ConventionViolation(BaseModel):
    rule: str = Field(description="the convention being violated, named concisely (e.g. 'PEP 8 naming')")
    location: str = Field(description="where in the snippet this occurs — a quoted line or identifier, not a line number")
    suggestion: str = Field(description="the idiomatic replacement or fix")


class LanguageReview(BaseModel):
    language: str = Field(description="the programming language the snippet is written in")
    violations: List[ConventionViolation] = Field(default_factory=list)
    summary: Optional[str] = Field(
        default=None,
        description="one-line overall assessment, e.g. 'idiomatic aside from naming'",
    )
