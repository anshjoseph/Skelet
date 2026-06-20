"""
Minimal end-to-end example: build a system prompt from skelet core +
skelet-standard, then apply a model's structured output deterministically.

Run with both packages installed:
    pip install -e .
    pip install -e skelet-standard
    python example/exp1.py
"""

from skelet.core import Priority, Prompt, Rule
from skelet_standard.tools.patch import Patch, Patchs, apply_patches, build_system_prompt as patch_prompt

# 1. A project-specific Prompt (role/objective/context) composed with a
#    skill's system prompt (the patch tool's instructions).
base_prompt = Prompt(
    role="you are a senior code reviewer",
    objective="propose small, safe improvements to the given snippet",
)
system_prompt = f"{base_prompt.render()}\n\n{patch_prompt()}"
print(system_prompt)
print("\n" + "=" * 80 + "\n")

# 2. Pretend this Patchs object is the model's structured output, returned
#    after it read the snippet below and followed the patch skill's rules.
snippet = "def add(a,b):\n    return a+b\n"

patches = Patchs(
    summary="add spacing around operators per PEP 8",
    patchs=[
        Patch(
            explain="space arguments and operator for readability",
            search="def add(a,b):\n    return a+b",
            replace="def add(a, b):\n    return a + b",
        ),
    ],
)

# 3. Apply deterministically — no guessing, raises if the search block isn't
#    found/unique.
result = apply_patches(patches, snippet)
print(result)
