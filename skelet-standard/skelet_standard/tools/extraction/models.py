"""
Structured extraction template — framework-agnostic.

Pulls fields out of unstructured text into a flat key/value result, while
being explicit about what couldn't be found rather than guessing or
omitting it silently.
"""

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ExtractionResult(BaseModel):
    fields: Dict[str, Any] = Field(description="extracted field name -> value pairs")
    missing_fields: List[str] = Field(
        default_factory=list,
        description="requested fields that could not be found in the source text",
    )
