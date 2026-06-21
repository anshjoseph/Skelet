"""
Structured prompt spec for video-generation models (Sora/Runway/Veo-style).

This skill doesn't generate video itself — it shapes an LLM's output into
a well-formed spec that a downstream video generator consumes. Output is
advisory: nothing here is auto-applied or verified, so this is a skill,
not a tool.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class VideoPromptSpec(BaseModel):
    scene: str = Field(description="what happens in the shot, described concretely")
    style: str = Field(description="visual style, e.g. 'cinematic', 'anime', 'photorealistic'")
    camera_movement: Optional[str] = Field(
        default=None, description="e.g. 'slow dolly in', 'static', 'handheld pan left'"
    )
    duration_seconds: Optional[float] = Field(default=None, description="target clip length")
    aspect_ratio: Optional[str] = Field(default=None, description="e.g. '16:9', '9:16'")
    keyframes: List[str] = Field(
        default_factory=list,
        description="ordered beats describing how the shot evolves, in plain language",
    )
    negative_prompt: Optional[str] = Field(
        default=None, description="things to avoid in the generated video"
    )
