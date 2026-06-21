"""
Structured prompt spec for sprite-sheet-generation models (pixel-art /
2D-animation generators). Advisory output only — nothing here is
auto-applied or verified.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class SpriteSheetPromptSpec(BaseModel):
    subject: str = Field(description="the character/object being animated")
    action: str = Field(description="the animation, e.g. 'walk cycle', 'idle', 'attack swing'")
    frame_count: int = Field(description="number of frames in the animation")
    frame_size: Optional[str] = Field(default=None, description="e.g. '64x64', '32x32'")
    directions: List[str] = Field(
        default_factory=list,
        description="facing directions needed, e.g. ['left', 'right', 'up', 'down']",
    )
    style: str = Field(description="e.g. 'pixel art', '16-bit', 'hand-drawn'")
    background: Optional[str] = Field(
        default="transparent", description="background treatment, e.g. 'transparent', 'solid color'"
    )
