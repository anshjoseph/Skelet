from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from skelet.core._helpers import clean, nonempty
from skelet.core.prompt import Example, render_examples
from skelet.core.rule import Constraint, Rule, render_constraints, render_rules


class Resource(BaseModel):
    """A bundled file a skill can point to (e.g. a script, reference doc, or
    template living alongside SKILL.md)."""

    path: str
    purpose: str

    @field_validator("path", "purpose")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v


class SkillPrompt(BaseModel):
    """Mirrors the structure of an Anthropic SKILL.md: YAML-style frontmatter
    (name/description) used for discovery/triggering, plus the body content
    Claude reads once the skill is loaded."""

    # --- Frontmatter (used for routing/triggering, kept short) -------------
    name: str
    description: str  # what it does + when to use it; this is what triggers loading

    # --- Body ----------------------------------------------------------------
    overview: Optional[str] = None
    when_to_use: List[str] = Field(default_factory=list)        # trigger conditions
    when_not_to_use: List[str] = Field(default_factory=list)    # anti-triggers
    instructions: List[str] = Field(default_factory=list)       # ordered steps
    rules: List[Rule] = Field(default_factory=list)
    constraints: List[Constraint] = Field(default_factory=list)
    edge_cases: List[str] = Field(default_factory=list)
    examples: List[Example[Any]] = Field(default_factory=list)
    resources: List[Resource] = Field(default_factory=list)     # bundled files
    output_format: Optional[str] = None
    validation_checklist: List[str] = Field(default_factory=list)

    @field_validator("name", "description")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v

    @field_validator("overview", "output_format")
    @classmethod
    def _clean_scalar(cls, v: Optional[str]) -> Optional[str]:
        return clean(v)

    @field_validator(
        "when_to_use", "when_not_to_use", "instructions",
        "edge_cases", "validation_checklist",
    )
    @classmethod
    def _clean_list(cls, v: List[str]) -> List[str]:
        return nonempty(v)

    @model_validator(mode="after")
    def _require_body(self) -> "SkillPrompt":
        if not self.render_body():
            raise ValueError("SkillPrompt body is empty; provide at least one section.")
        return self

    # --- Rendering -----------------------------------------------------------

    def render_frontmatter(self) -> str:
        """Renders the YAML-style frontmatter block, matching SKILL.md conventions."""
        return f"---\nname: {self.name}\ndescription: {self.description}\n---"

    def render_body(self) -> str:
        sections: List[str] = []

        def section(title: str, body: str) -> None:
            body = body.strip()
            if body:
                sections.append(f"# {title}\n{body}")

        if self.overview:
            section("OVERVIEW", self.overview)

        if self.when_to_use:
            section(
                "WHEN TO USE",
                "\n".join(f"- {item}" for item in self.when_to_use),
            )

        if self.when_not_to_use:
            section(
                "WHEN NOT TO USE",
                "\n".join(f"- {item}" for item in self.when_not_to_use),
            )

        if self.instructions:
            section(
                "INSTRUCTIONS",
                "\n".join(f"{i}. {step}" for i, step in enumerate(self.instructions, 1)),
            )

        if self.rules:
            section("RULES", render_rules(self.rules))

        if self.constraints:
            section("CONSTRAINTS", render_constraints(self.constraints))

        if self.edge_cases:
            section("EDGE CASES", "\n".join(f"- {c}" for c in self.edge_cases))

        if self.examples:
            section("EXAMPLES", render_examples(self.examples))

        if self.resources:
            section(
                "RESOURCES",
                "\n".join(f"- {r.path}: {r.purpose}" for r in self.resources),
            )

        if self.output_format:
            section("OUTPUT FORMAT", self.output_format)

        if self.validation_checklist:
            section(
                "VALIDATION CHECKLIST",
                "\n".join(f"[ ] {item}" for item in self.validation_checklist),
            )

        return "\n\n".join(sections)

    def render(self) -> str:
        """Full SKILL.md-style document: frontmatter + body."""
        return f"{self.render_frontmatter()}\n\n{self.render_body()}"

    def __str__(self) -> str:
        return self.render()
