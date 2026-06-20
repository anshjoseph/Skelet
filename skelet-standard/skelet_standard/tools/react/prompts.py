"""
Prompt + skill for ReAct (reason + act). Framework-agnostic: only builds
text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

REACT_SKILL = SkillPrompt(
    name="react",
    description=(
        "Interleave reasoning with tool actions: think, act, observe the "
        "result, and repeat until the task can be answered. Use whenever "
        "a task needs external information or actions gathered "
        "incrementally rather than answered in one shot."
    ),
    overview=(
        "You return a ReActResult: `steps` (each a thought, optionally an "
        "action + action_input) and `final_answer` once you have enough to "
        "answer. The caller executes `action` and supplies `observation` on "
        "the next turn — you never fabricate an observation yourself."
    ),
    when_to_use=[
        "The task requires looking something up or calling a tool before it can be answered",
        "Information needs to be gathered incrementally based on what previous actions returned",
    ],
    when_not_to_use=[
        "The task can be answered directly with no external lookup/action — just answer it",
    ],
    instructions=[
        "Add a step with a `thought` explaining what to find out or do next",
        "If an action is needed, set `action` and `action_input`; leave `observation` empty — the caller fills it in",
        "On your next turn, read the `observation` the caller filled in before deciding the next thought",
        "Once you can answer, set `final_answer` and stop adding action steps",
    ],
    rules=[
        Rule(
            name="NO_FABRICATED_OBSERVATIONS",
            description="never fill in `observation` yourself — it is only ever written by the caller after executing `action`",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="ACTION_INPUT_REQUIRED",
            description="`action_input` must be set whenever `action` is set",
            priority=Priority.HIGH,
        ),
        Rule(
            name="STOP_WHEN_ANSERABLE",
            description="set `final_answer` as soon as the accumulated observations are sufficient; don't keep acting past that point",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "an action's observation indicates failure — add a new thought addressing the failure rather than repeating the same action unchanged",
        "no action is available that helps — set `final_answer` explaining the limitation instead of looping",
    ],
    output_format="A ReActResult object: steps, final_answer.",
    validation_checklist=[
        "No step has a fabricated observation",
        "final_answer is only set when the task can actually be answered",
    ],
)


def build_system_prompt() -> str:
    return REACT_SKILL.render_body()
