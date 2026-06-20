from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel

Renderable = Union[BaseModel, str]


def clean(text: Optional[str]) -> Optional[str]:
    """Strip surrounding whitespace; treat all-whitespace as empty/None."""
    if text is None:
        return None
    stripped = text.strip()
    return stripped or None


def nonempty(items: List[str]) -> List[str]:
    """Drop blank/whitespace-only entries and strip the rest."""
    return [s.strip() for s in items if s and s.strip()]


def render_value(value: Renderable) -> str:
    """Render an Example input/output that may be a Pydantic model or a string."""
    if isinstance(value, BaseModel):
        # Pretty JSON keeps nested models readable in the prompt.
        return value.model_dump_json(indent=2)
    return str(value).strip()
