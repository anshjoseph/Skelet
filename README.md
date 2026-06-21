# skelet

A library for building structured, predictable LLM prompts as pydantic
models instead of hand-written strings — so prompts can be composed,
versioned, validated, and reused like any other code.

## Packages

- **`skelet`** (this repo, `pyproject.toml`) — core primitives only:
  `Prompt`, `Rule`, `Constraint`, `Example`, `SkillPrompt`, `Resource`,
  `Priority`. No opinionated content, no LLM-framework dependency.
- **`skelet-standard`** (`skelet-standard/`) — a curated, maintainer-reviewed
  pack of common tools/skills built on `skelet`. Depends on `skelet`.
- **third-party packs** — anyone can publish their own
  `skelet-prompt-pack-<name>` depending on `skelet` (or `skelet-standard`).
  See [CONTRIBUTING.md](CONTRIBUTING.md).

## Install

Not on PyPI yet — install directly from git:

```bash
pip install git+https://github.com/anshjoseph/Skelet.git                                    # core primitives only
pip install "git+https://github.com/anshjoseph/Skelet.git#subdirectory=skelet-standard"       # + standard tools/skills
pip install "git+https://github.com/anshjoseph/Skelet.git#subdirectory=skelet-prompt-pack-media"  # + generative-media prompts
```

Each is independent — install only the package(s) you need (`skelet-standard`
and `skelet-prompt-pack-media` both depend on `skelet` and will pull it in).

Working on the library itself instead? Clone and install editable:

```bash
git clone https://github.com/anshjoseph/Skelet.git
cd Skelet
pip install -e .
pip install -e skelet-standard
pip install -e skelet-prompt-pack-media
```

## Core primitives (`skelet.core`)

```python
from skelet.core import Prompt, Rule, Priority, SkillPrompt

prompt = Prompt(
    role="senior code reviewer",
    objective="find bugs and suggest fixes",
    rules=[Rule(name="Safety", description="never break the build", priority=Priority.CRITICAL)],
)
print(prompt.render())
```

`SkillPrompt` mirrors an Anthropic-style `SKILL.md`: frontmatter
(`name`/`description`) plus a structured body (`when_to_use`,
`instructions`, `rules`, `edge_cases`, `output_format`, ...).

## `skelet-standard`: tools vs. skills

```
skelet_standard/
  tools/    output is meant to be applied/verified deterministically
            (patch, citation, diff_review, compaction, long_doc,
             chain_of_thought, react, extraction)
  skills/   output is advisory/informational, nothing gets auto-applied
            (programming_language conventions, customer_care, triage)
```

Every entry is `models.py` (pydantic input/output schema + any pure
verification logic) + `prompts.py` (a `SkillPrompt` built from
`skelet.core`) + `__init__.py` (re-exports). Example:

```python
from skelet_standard.tools.patch import Patch, Patchs, apply_patches, build_system_prompt

system_prompt = build_system_prompt()
# ... send system_prompt + content to your model, get back a Patchs ...
patched = apply_patches(patches, original_content)  # deterministic, verified
```

See [docs/STANDARD.md](docs/STANDARD.md) for a full catalog of every tool
and skill currently in `skelet-standard` — schema, what it's for, and a
usage snippet for each.

Runnable examples:
- [example/exp1.py](example/exp1.py) — compose a project `Prompt` with the
  patch skill, then apply the model's structured output.
- [example/exp2_citation.py](example/exp2_citation.py) — verify a model's
  cited answer against source text, including a rejected hallucinated quote.
- [example/exp3_diff_review.py](example/exp3_diff_review.py) — structured,
  severity-tagged diff comments and a merge-blocking check.
- [example/exp4_long_doc.py](example/exp4_long_doc.py) — chunk a large
  document and navigate it via search instead of reading it all at once.
- [example/exp5_reasoning.py](example/exp5_reasoning.py) — chain-of-thought,
  ReAct, and structured extraction outputs.
- [example/exp6_skills.py](example/exp6_skills.py) — triage, customer care,
  and per-language convention review (with registry fallback).
- [example/exp7_media.py](example/exp7_media.py) — generative-media prompt
  specs (image, video, 3D object, sprite sheet) from `skelet-prompt-pack-media`.

## Adding your own tools/skills

See [CONTRIBUTING.md](CONTRIBUTING.md) for the convention to follow, and
when something belongs in core, `skelet-standard`, or your own pack.
