"""
Reasoning tools example: chain-of-thought, ReAct, and structured extraction.

Run: python example/exp5_reasoning.py
"""

from skelet_standard.tools.chain_of_thought import ChainOfThoughtAnswer
from skelet_standard.tools.chain_of_thought import build_system_prompt as cot_prompt
from skelet_standard.tools.extraction import ExtractionResult
from skelet_standard.tools.extraction import build_system_prompt as extraction_prompt
from skelet_standard.tools.react import ReActResult, ReActStep
from skelet_standard.tools.react import build_system_prompt as react_prompt

print("--- chain of thought ---")
print(cot_prompt()[:200], "...\n")
cot = ChainOfThoughtAnswer(
    reasoning_steps=[
        "Original price is $80, discount is 25%",
        "25% of $80 is $20",
        "$80 - $20 = $60",
    ],
    answer="$60",
)
print(cot)

print("\n--- ReAct ---")
print(react_prompt()[:200], "...\n")
react = ReActResult(
    steps=[
        ReActStep(thought="need today's exchange rate", action="lookup_rate", action_input="USD-EUR", observation=None),
        ReActStep(thought="observation came back 0.92, can now convert", observation="0.92"),
    ],
    final_answer="100 USD is about 92 EUR",
)
print(react)

print("\n--- extraction ---")
print(extraction_prompt()[:200], "...\n")
extracted = ExtractionResult(
    fields={"name": "Jane Doe", "email": "jane@example.com"},
    missing_fields=["phone"],
)
print(extracted)
