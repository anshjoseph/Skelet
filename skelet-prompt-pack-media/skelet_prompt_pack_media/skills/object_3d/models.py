"""
Structured prompt spec for 3D-object-generation models (Meshy/Tripo-style).

Advisory output only — nothing here is auto-applied or verified.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Object3DPromptSpec(BaseModel):
    subject: str = Field(description="what the object is, described concretely")
    style: str = Field(description="e.g. 'low-poly', 'photoreal', 'voxel', 'hand-painted'")
    materials: List[str] = Field(
        default_factory=list, description="surface materials/textures expected on the model"
    )
    polycount_target: Optional[str] = Field(
        default=None, description="e.g. 'low (<5k tris)', 'high-detail'"
    )
    reference_views: List[str] = Field(
        default_factory=list,
        description="angles the model should be consistent from, e.g. 'front', '3/4 view', 'top-down'",
    )
    output_format: Optional[str] = Field(default=None, description="e.g. 'glb', 'obj', 'fbx'")
