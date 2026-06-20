"""
Chain-of-thought template — framework-agnostic.

Separates reasoning from the final answer so the caller can show/hide/audit
the reasoning independently, instead of parsing it out of free text.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class ChainOfThoughtAnswer(BaseModel):
    reasoning_steps: List[str] = Field(
        description="ordered intermediate reasoning steps that lead to the answer"
    )
    answer: str = Field(description="the final answer, standalone and usable without the reasoning steps")
