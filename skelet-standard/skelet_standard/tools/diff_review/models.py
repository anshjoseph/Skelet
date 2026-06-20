"""
Diff review data model — framework-agnostic.

Review comments are tied to an exact quoted location in the diff, not a
line number, so they stay valid even if the caller doesn't track line
numbers precisely (same reasoning as the patch tool's search/replace).
"""

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

Severity = Literal["info", "minor", "major", "blocking"]


class ReviewComment(BaseModel):
    location: str = Field(description="exact snippet from the diff this comment refers to, copied verbatim")
    severity: Severity = Field(description="'info' (note only) through 'blocking' (must fix before merge)")
    comment: str = Field(description="what's wrong and why it matters")
    suggestion: str = Field(default="", description="concrete fix, if there is one; empty if the comment is informational only")


class DiffReview(BaseModel):
    summary: str = Field(description="one-line overall assessment of the diff")
    comments: List[ReviewComment] = Field(default_factory=list)


def has_blocking_comments(review: DiffReview) -> bool:
    return any(c.severity == "blocking" for c in review.comments)
