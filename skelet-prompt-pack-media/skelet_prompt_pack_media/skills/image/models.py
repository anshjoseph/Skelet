"""
Structured prompt spec for image-generation models (Midjourney/DALL-E/
Stable Diffusion-style). Advisory output only — nothing here is
auto-applied or verified.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ImagePromptSpec(BaseModel):
    subject: str = Field(description="what the image depicts, described concretely")
    style: str = Field(description="e.g. 'photorealistic', 'oil painting', 'flat vector art'")
    composition: Optional[str] = Field(
        default=None, description="e.g. 'close-up portrait', 'wide establishing shot', 'centered'"
    )
    lighting: Optional[str] = Field(default=None, description="e.g. 'golden hour', 'studio softbox'")
    color_palette: Optional[str] = Field(default=None, description="e.g. 'muted earth tones'")
    aspect_ratio: Optional[str] = Field(default=None, description="e.g. '1:1', '16:9'")
    details: List[str] = Field(
        default_factory=list, description="specific elements that must appear in the image"
    )
    negative_prompt: Optional[str] = Field(
        default=None, description="things to avoid in the generated image"
    )
