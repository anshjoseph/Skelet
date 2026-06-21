"""
Build system prompts for the media-generation pack (image, video, 3D
object, sprite sheet), then pretend a model returned each structured spec
following the skill's rules.

Run with both packages installed:
    pip install -e .
    pip install -e skelet-prompt-pack-media
    python example/exp7_media.py
"""

from skelet.core import Prompt
from skelet_prompt_pack_media.skills.image import ImagePromptSpec, build_system_prompt as image_prompt
from skelet_prompt_pack_media.skills.object_3d import Object3DPromptSpec, build_system_prompt as object_3d_prompt
from skelet_prompt_pack_media.skills.sprite_sheet import (
    SpriteSheetPromptSpec,
    build_system_prompt as sprite_sheet_prompt,
)
from skelet_prompt_pack_media.skills.video import VideoPromptSpec, build_system_prompt as video_prompt

base_prompt = Prompt(
    role="you are a generative-media prompting assistant",
    objective="turn a loose creative idea into a precise, structured prompt spec",
)


def show(title: str, system_prompt: str, spec) -> None:
    print(f"=== {title} ===")
    print(f"{base_prompt.render()}\n\n{system_prompt}")
    print("\n--- model's structured output ---")
    print(spec.model_dump_json(indent=2))
    print("\n" + "=" * 80 + "\n")


# 1. Image — "a fox guarding an ancient library, painterly, warm light"
show(
    "image",
    image_prompt(),
    ImagePromptSpec(
        subject="a red fox standing guard at the entrance of an ancient stone library",
        style="painterly, oil-on-canvas",
        composition="medium shot, fox centered, library doorway behind it",
        lighting="warm late-afternoon light through the doorway",
        color_palette="warm ochres and deep browns with cool shadow blues",
        aspect_ratio="3:2",
        details=["dust motes visible in the light beams", "worn stone steps"],
        negative_prompt="no text, no modern objects",
    ),
)

# 2. Video — "a drone shot flying over a coastline at sunrise"
show(
    "video",
    video_prompt(),
    VideoPromptSpec(
        scene="a drone flies low over a rocky coastline as waves crash below",
        style="cinematic, photorealistic",
        camera_movement="slow forward drone push, slight rise at the end",
        duration_seconds=6,
        aspect_ratio="16:9",
        keyframes=[
            "drone low over the water approaching the coastline",
            "rises slightly to reveal the sun breaking over the horizon",
        ],
        negative_prompt="no people, no boats",
    ),
)

# 3. 3D object — "a low-poly treasure chest for a game asset pack"
show(
    "3d object",
    object_3d_prompt(),
    Object3DPromptSpec(
        subject="a wooden treasure chest with iron bands and a latch",
        style="low-poly, hand-painted textures",
        materials=["weathered wood", "rusted iron"],
        polycount_target="low (<3k tris)",
        reference_views=["front", "3/4 view", "top-down"],
        output_format="glb",
    ),
)

# 4. Sprite sheet — "a knight character walk cycle for a 2D platformer"
show(
    "sprite sheet",
    sprite_sheet_prompt(),
    SpriteSheetPromptSpec(
        subject="a knight in plate armor",
        action="walk cycle",
        frame_count=8,
        frame_size="64x64",
        directions=["left", "right"],
        style="16-bit pixel art",
        background="transparent",
    ),
)
