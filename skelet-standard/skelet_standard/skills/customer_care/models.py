"""
Customer-care response data model — framework-agnostic.

Given a customer message, produce a reply plus the reasoning a human
reviewer would want to see (tone, whether escalation is needed) — not just
raw text, so the caller can apply policy checks before sending anything.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class CustomerCareResponse(BaseModel):
    reply: str = Field(description="the response to send to the customer")
    tone: str = Field(description="the tone used, e.g. 'empathetic', 'neutral', 'apologetic'")
    needs_escalation: bool = Field(
        default=False,
        description="true if this should be handed to a human agent instead of sent as-is",
    )
    escalation_reason: Optional[str] = Field(
        default=None,
        description="why escalation is needed, required if needs_escalation is true",
    )
    referenced_facts: List[str] = Field(
        default_factory=list,
        description="account/order/policy facts the reply relies on, so they can be verified before sending",
    )
