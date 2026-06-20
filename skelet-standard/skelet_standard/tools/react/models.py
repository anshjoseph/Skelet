"""
ReAct (reason + act) template — framework-agnostic.

Each turn pairs a thought with an action and its input, so a calling loop
can execute the action and feed back an observation before the next turn.
This module only shapes that structure; it does not execute any action.
"""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ReActStep(BaseModel):
    thought: str = Field(description="reasoning about what to do next and why")
    action: Optional[str] = Field(default=None, description="name of the tool/action to invoke, omitted if no action is needed this step")
    action_input: Optional[Any] = Field(default=None, description="input to pass to `action`, required if `action` is set")
    observation: Optional[str] = Field(
        default=None,
        description="result of the action from a previous turn, filled in by the caller before the next turn — not produced by the model",
    )


class ReActResult(BaseModel):
    steps: List[ReActStep] = Field(description="the thought/action/observation sequence so far")
    final_answer: Optional[str] = Field(
        default=None,
        description="set once enough actions/observations have accumulated to answer; omitted while still acting",
    )
