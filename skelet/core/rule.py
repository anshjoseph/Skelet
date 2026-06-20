from __future__ import annotations

from enum import IntEnum
from typing import List

from pydantic import BaseModel, field_validator


class Priority(IntEnum):
    """Convenience labels; any int still works for `priority`."""
    LOW = 10
    NORMAL = 100
    HIGH = 500
    CRITICAL = 1000


class Rule(BaseModel):
    name: str
    description: str
    priority: int = Priority.NORMAL

    @field_validator("name", "description")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v


class Constraint(BaseModel):
    description: str

    @field_validator("description")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("constraint description must not be blank")
        return v


def render_rules(rules: List[Rule]) -> str:
    """Render rules sorted by priority desc, preserving original order on ties."""
    ordered = sorted(enumerate(rules), key=lambda pair: (-pair[1].priority, pair[0]))
    return "\n".join(f"- [{r.priority}] {r.name}: {r.description}" for _, r in ordered)


def render_constraints(constraints: List[Constraint]) -> str:
    return "\n".join(f"- {c.description}" for c in constraints)
