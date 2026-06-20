from __future__ import annotations

from typing import Any, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field, field_validator, model_validator

from skelet.core._helpers import Renderable, clean, nonempty, render_value
from skelet.core.rule import Constraint, Rule, render_constraints, render_rules

# Example input/output may be any Pydantic model, or a plain string.
T = TypeVar("T", bound=BaseModel)


class Example(BaseModel, Generic[T]):
    # input/output may be any Pydantic model (T) or a plain string.
    input: Union[T, str]
    output: Union[T, str]
    note: Optional[str] = None  # optional explanation of why this example matters

    @field_validator("input", "output")
    @classmethod
    def _not_blank(cls, v: Renderable) -> Renderable:
        # Only string values can be "blank"; models are always valid here.
        if isinstance(v, str) and not v.strip():
            raise ValueError("example input/output must not be blank")
        return v


def render_examples(examples: List[Example[Any]]) -> str:
    blocks = []
    for i, ex in enumerate(examples, 1):
        parts = [f"Example {i}"]
        if ex.note:
            parts.append(f"({ex.note})")
        parts.append(f"Input:\n{render_value(ex.input)}")
        parts.append(f"Output:\n{render_value(ex.output)}")
        blocks.append("\n".join(parts))
    return "\n\n".join(blocks)


class Prompt(BaseModel):
    role: Optional[str] = None
    objective: Optional[str] = None
    context: List[str] = Field(default_factory=list)
    tasks: List[str] = Field(default_factory=list)
    rules: List[Rule] = Field(default_factory=list)
    constraints: List[Constraint] = Field(default_factory=list)
    edge_cases: List[str] = Field(default_factory=list)
    examples: List[Example[Any]] = Field(default_factory=list)
    output_format: Optional[str] = None
    validation_checklist: List[str] = Field(default_factory=list)

    # Normalize free-text scalar fields.
    @field_validator("role", "objective", "output_format")
    @classmethod
    def _clean_scalar(cls, v: Optional[str]) -> Optional[str]:
        return clean(v)

    # Normalize list-of-string fields.
    @field_validator("context", "tasks", "edge_cases", "validation_checklist")
    @classmethod
    def _clean_list(cls, v: List[str]) -> List[str]:
        return nonempty(v)

    @model_validator(mode="after")
    def _require_something(self) -> "Prompt":
        if not self.render():
            raise ValueError("Prompt is empty; provide at least one section.")
        return self

    # --- Rendering ---------------------------------------------------------

    def render(self) -> str:
        sections: List[str] = []

        def section(title: str, body: str) -> None:
            body = body.strip()
            if body:
                sections.append(f"# {title}\n{body}")

        if self.role:
            section("ROLE", self.role)

        if self.objective:
            section("OBJECTIVE", self.objective)

        if self.context:
            section("CONTEXT", "\n".join(f"- {item}" for item in self.context))

        if self.tasks:
            section(
                "TASKS",
                "\n".join(f"{i}. {t}" for i, t in enumerate(self.tasks, 1)),
            )

        if self.rules:
            section("RULES", render_rules(self.rules))

        if self.constraints:
            section("CONSTRAINTS", render_constraints(self.constraints))

        if self.edge_cases:
            section("EDGE CASES", "\n".join(f"- {c}" for c in self.edge_cases))

        if self.examples:
            section("EXAMPLES", render_examples(self.examples))

        if self.output_format:
            section("OUTPUT FORMAT", self.output_format)

        if self.validation_checklist:
            section(
                "VALIDATION CHECKLIST",
                "\n".join(f"[ ] {item}" for item in self.validation_checklist),
            )

        return "\n\n".join(sections)

    def __str__(self) -> str:
        return self.render()
