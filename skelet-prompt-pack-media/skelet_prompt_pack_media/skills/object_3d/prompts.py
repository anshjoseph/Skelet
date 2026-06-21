"""
Prompt + skill for the 3D-object-generation spec. Framework-agnostic: this
only builds text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

OBJECT_3D_SKILL = SkillPrompt(
    name="3d-object-generation-prompting",
    description=(
        "Turn a loose object idea into a structured Object3DPromptSpec "
        "ready for a text-to-3D model. Use whenever the goal is generating "
        "a 3D asset rather than describing one in prose."
    ),
    overview=(
        "You produce an Object3DPromptSpec: subject, style, materials, "
        "polycount target, reference views, and output format — concrete "
        "enough for a downstream 3D generator to act on without guessing."
    ),
    when_to_use=[
        "The user wants a prompt for a text-to-3D model (Meshy, Tripo, etc.)",
    ],
    when_not_to_use=[
        "Describing an existing 3D model rather than generating a new one",
    ],
    instructions=[
        "Name the subject concretely (what it is, not just a vibe)",
        "Pick one consistent style and state it explicitly",
        "List materials only if they matter for the result (skip if generic)",
        "State reference views the model must stay consistent across, if any",
        "State the output format only if the downstream pipeline requires a specific one",
    ],
    rules=[
        Rule(
            name="SINGLE_OBJECT",
            description="each Object3DPromptSpec describes exactly one object, not a scene or set.",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="CONCRETE_SUBJECT",
            description="the subject must be a concrete noun phrase, not an abstract description.",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "user asks for a set of related objects — produce one Object3DPromptSpec per object",
    ],
    output_format="An Object3DPromptSpec object.",
    validation_checklist=[
        "subject is a concrete noun phrase",
        "style is a single, unambiguous descriptor",
        "reference_views (if any) are non-redundant",
    ],
)


def build_system_prompt() -> str:
    return OBJECT_3D_SKILL.render_body()
