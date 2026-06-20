"""
Triage data model — framework-agnostic.

Classifies and prioritizes an incoming item (ticket, bug report, support
request) so it can be routed, without the model deciding what happens to
it next — routing/action is the caller's job.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

Priority = Literal["low", "normal", "high", "urgent"]


class Triage(BaseModel):
    category: str = Field(description="short category label, e.g. 'bug', 'feature-request', 'billing', 'spam'")
    priority: Priority = Field(description="urgency of handling this item")
    rationale: str = Field(description="why this category/priority was chosen")
    duplicate_of: Optional[str] = Field(
        default=None,
        description="id/reference of an existing item this duplicates, if given context makes that clear",
    )
