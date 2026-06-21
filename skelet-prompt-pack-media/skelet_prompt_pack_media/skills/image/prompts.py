"""
Prompt + skill for the image-generation spec. Framework-agnostic: this only
builds text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

IMAGE_SKILL = SkillPrompt(
    name="image-generation-prompting",
    description=(
        "Turn a loose image idea into a structured ImagePromptSpec ready "
        "for a text-to-image model. Use whenever the goal is generating a "
        "still image rather than describing one in prose."
    ),
    overview=(
        "You produce an ImagePromptSpec: subject, style, composition, "
        "lighting, color palette, aspect ratio, required details, and an "
        "optional negative prompt — concrete enough for a downstream image "
        "generator to act on without guessing."
    ),
    when_to_use=[
        "The user wants a prompt for a text-to-image model (Midjourney, DALL-E, Stable Diffusion, etc.)",
    ],
    when_not_to_use=[
        "Describing an existing image rather than generating a new one",
        "Generating an animation/video (use the video-generation skill instead)",
    ],
    instructions=[
        "Name the subject concretely: who/what, doing what, where",
        "Pick one consistent style and state it explicitly",
        "Describe composition/lighting/palette only if they matter to the result",
        "List required details as discrete items, not buried in one long sentence",
        "Add a negative prompt only for failure modes that are actually likely",
    ],
    rules=[
        Rule(
            name="SINGLE_IMAGE",
            description="each ImagePromptSpec describes exactly one still image, not a sequence or set.",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="CONCRETE_SUBJECT",
            description="the subject must name concrete elements, not abstract moods alone.",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "user asks for a set of variations — produce one ImagePromptSpec per variation",
    ],
    output_format="An ImagePromptSpec object.",
    validation_checklist=[
        "subject names concrete elements",
        "style is a single, unambiguous descriptor",
        "details list has no duplicates",
    ],
)


def build_system_prompt() -> str:
    return IMAGE_SKILL.render_body()
