"""
Prompt + skill for the video-generation spec. Framework-agnostic: this only
builds text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

VIDEO_SKILL = SkillPrompt(
    name="video-generation-prompting",
    description=(
        "Turn a loose video idea into a structured VideoPromptSpec ready "
        "for a text-to-video model. Use whenever the goal is generating a "
        "video clip rather than describing one in prose."
    ),
    overview=(
        "You produce a VideoPromptSpec: scene, style, camera movement, "
        "duration, aspect ratio, ordered keyframes, and an optional "
        "negative prompt — concrete enough for a downstream video "
        "generator to act on without guessing."
    ),
    when_to_use=[
        "The user wants a prompt for a text-to-video model (Sora, Runway, Veo, etc.)",
    ],
    when_not_to_use=[
        "Describing a video that already exists (use a different skill for that)",
    ],
    instructions=[
        "Restate the scene concretely: subjects, action, setting — avoid vague nouns",
        "Pick one consistent visual style and state it explicitly",
        "Describe camera movement only if it matters to the shot",
        "Break multi-beat scenes into ordered keyframes instead of one run-on sentence",
        "Add a negative prompt only for failure modes that are actually likely",
    ],
    rules=[
        Rule(
            name="ONE_SHOT_ONE_SPEC",
            description="each VideoPromptSpec describes a single continuous shot, not a multi-cut sequence.",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="CONCRETE_SCENE",
            description="the scene must name concrete subjects and actions, not abstract moods alone.",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "user gives a multi-shot sequence — produce one VideoPromptSpec per shot, in order",
    ],
    output_format="A VideoPromptSpec object.",
    validation_checklist=[
        "scene names concrete subjects/actions",
        "style is a single, unambiguous descriptor",
        "keyframes (if any) are ordered and non-redundant",
    ],
)


def build_system_prompt() -> str:
    return VIDEO_SKILL.render_body()
