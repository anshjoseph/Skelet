# Contributing to skelet

There are three tiers. Know which one your change belongs in before
writing anything.

| Tier | Package | Contains | Review |
|---|---|---|---|
| Core | `skelet` | Bare primitives only: `Prompt`, `Rule`, `Constraint`, `Example`, `SkillPrompt`, `Resource`, `Priority` | Full code review, kept deliberately small |
| Standard | `skelet-standard` | Maintainer-reviewed, regularly-useful tools/skills built on core | Full code review |
| Pack | `skelet-prompt-pack-<name>` | Anyone's project-specific or experimental tools/skills | Only the index-listing entry is reviewed, not the pack's code |

If you're not sure where something goes: if it's a genuinely general
pattern most projects would reuse (like `patch` or `citation`), propose it
for `skelet-standard`. If it's specific to your project/domain, publish
your own pack instead.

## `tools/` vs `skills/`

Inside `skelet-standard` (and any pack), every addition is either a tool or
a skill:

- **`tools/`** — the model's structured output is applied or verified by
  deterministic code afterward (e.g. `patch` applies search/replace blocks,
  `citation` verifies quotes against sources). If your addition has a pure
  "apply"/"verify" function, it's a tool.
- **`skills/`** — the output is advisory/informational; nothing gets
  auto-applied (e.g. `programming_language` review, `customer_care` reply
  drafts, `triage` classification).

## Layout for every tool/skill

```
<tools|skills>/<name>/
    __init__.py   # re-exports the public names from models.py + prompts.py
    models.py     # pydantic input/output schema, plus any pure apply/verify logic
    prompts.py    # a SkillPrompt (from skelet.core) + build_system_prompt()
```

See `skelet_standard/tools/patch/` as the reference implementation.

### `models.py`

- Define the schema the model must return as pydantic `BaseModel`s. Field
  `description`s are instructions to the model, not just type hints — write
  them accordingly.
- No framework imports (no LangChain/OpenAI SDK/etc), no env vars, no file
  or network IO. Pure data and text in, pure data and text out.
- If output needs to be applied or verified, put that logic here with
  explicit exceptions for every failure mode (see `patch`'s
  `PatchNotFound`/`PatchAmbiguous`, `citation`'s `CitationNotFound`) — never
  fail silently or guess.

### `prompts.py`

- Build a `SkillPrompt` from `skelet.core`: `name`, `description`,
  `overview`, `when_to_use`/`when_not_to_use`, `instructions`, `rules`
  (reuse `skelet.core.Rule`/`Priority`, don't redefine), `edge_cases`,
  `output_format`, `validation_checklist`.
- Expose `build_system_prompt() -> str`. Keep it standalone and composable —
  combining it with a project-specific `Prompt` (role/objective/context) is
  the calling project's job, not this file's.

### `__init__.py`

Re-export the public classes/exceptions/functions from `models.py` and
`prompts.py`. Don't export internals (anything prefixed `_`).

## Publishing your own pack

Name it `skelet-prompt-pack-<name>` (any unique name, not necessarily your
username), depending on `skelet` (or `skelet-standard` if you build on its
tools/skills). Follow the same `tools/`/`skills/` + `models.py`/`prompts.py`
layout. To get listed in this repo's index so others can find and
`pip install` it, open a PR adding an entry (name, package URL, one-line
description) — maintainers review that entry, not your pack's source.

## Rules for every contribution (core, standard, or pack)

- No duplicate primitives: reuse `skelet.core` (`Rule`, `Constraint`,
  `Example`, `SkillPrompt`, `Resource`, `Priority`) instead of redefining
  equivalents.
- No framework lock-in: `models.py`/`prompts.py` never import a specific
  LLM client library.
- No environment/IO assumptions in `models.py`/`prompts.py`: no secrets,
  files, or network calls.
- Keep schemas serializable: plain pydantic `BaseModel`s with
  JSON-serializable fields, so every schema is ready to be stored,
  versioned, or shared later without rework.
