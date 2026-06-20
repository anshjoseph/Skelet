"""
Prompt + skill for chain-of-thought answers. Framework-agnostic: only
builds text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

CHAIN_OF_THOUGHT_SKILL = SkillPrompt(
    name="chain-of-thought",
    description=(
        "Reason step by step before answering, returning the steps and the "
        "final answer as separate fields. Use for tasks where the answer is "
        "more reliable when intermediate steps are made explicit (math, "
        "multi-step logic, planning)."
    ),
    overview=(
        "You return a ChainOfThoughtAnswer: `reasoning_steps` (ordered, one "
        "step per item) and `answer` (the final answer alone, usable "
        "without the steps)."
    ),
    when_to_use=[
        "The task has multiple dependent steps where skipping ahead risks an error",
        "The caller wants the reasoning auditable separately from the answer",
    ],
    when_not_to_use=[
        "The task is a direct lookup/restatement with no real reasoning to show",
    ],
    instructions=[
        "Break the task into the smallest steps that are each individually easy to verify",
        "Work through the steps in order; each step may depend on the result of the previous one",
        "Put only the final result in `answer` — it must stand alone without `reasoning_steps`",
    ],
    rules=[
        Rule(
            name="ANSWER_STANDS_ALONE",
            description="`answer` must be understandable and correct on its own, without needing `reasoning_steps` to make sense",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="NO_SKIPPED_STEPS",
            description="don't jump to the answer inside `reasoning_steps` — each step should be a small, checkable increment",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "the task turns out to need no real reasoning — return a single trivial step rather than inventing steps",
    ],
    output_format="A ChainOfThoughtAnswer object: reasoning_steps, answer.",
    validation_checklist=[
        "answer is correct and self-contained",
        "each reasoning step follows from the previous one",
    ],
)


def build_system_prompt() -> str:
    return CHAIN_OF_THOUGHT_SKILL.render_body()
