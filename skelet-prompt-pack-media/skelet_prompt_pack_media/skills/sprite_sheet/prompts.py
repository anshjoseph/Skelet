"""
Prompt + skill for the sprite-sheet-generation spec. Framework-agnostic:
this only builds text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

SPRITE_SHEET_SKILL = SkillPrompt(
    name="sprite-sheet-generation-prompting",
    description=(
        "Turn a loose animation idea into a structured SpriteSheetPromptSpec "
        "ready for a 2D/pixel-art sprite generator. Use whenever the goal "
        "is generating game-ready animation frames."
    ),
    overview=(
        "You produce a SpriteSheetPromptSpec: subject, action, frame count, "
        "frame size, facing directions, style, and background treatment — "
        "concrete enough for a downstream sprite generator to act on "
        "without guessing."
    ),
    when_to_use=[
        "The user wants a prompt for a sprite-sheet/2D-animation generator",
    ],
    when_not_to_use=[
        "Generating a single static image (use a plain image-generation prompt instead)",
    ],
    instructions=[
        "Name the subject concretely",
        "Name exactly one action per spec — don't combine multiple animations",
        "Pick a frame_count appropriate to the action (don't pad or guess low)",
        "List only the directions actually needed by the target game/engine",
        "Default background to 'transparent' unless the user says otherwise",
    ],
    rules=[
        Rule(
            name="ONE_ACTION_PER_SPEC",
            description="each SpriteSheetPromptSpec covers exactly one animation/action, not several.",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="CONSISTENT_STYLE",
            description="style must stay consistent across all frames/directions described by one spec.",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "user asks for the same action in multiple directions — list them in `directions`, not as separate specs",
        "user asks for multiple distinct actions — produce one SpriteSheetPromptSpec per action",
    ],
    output_format="A SpriteSheetPromptSpec object.",
    validation_checklist=[
        "action names exactly one animation",
        "frame_count is appropriate for the action, not arbitrary",
        "directions list has no duplicates",
    ],
)


def build_system_prompt() -> str:
    return SPRITE_SHEET_SKILL.render_body()
