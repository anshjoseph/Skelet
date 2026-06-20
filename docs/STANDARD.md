# skelet-standard catalog

Everything currently available in `skelet-standard`, what it's for, its
schema, and a minimal usage snippet. All of these import from
`skelet.core` for `Rule`/`Priority`/`SkillPrompt` — see [README.md](../README.md)
for the core primitives themselves.

Every entry exposes `build_system_prompt() -> str`. Send that (optionally
combined with your own `skelet.core.Prompt`) as the system prompt, and have
your model client return the named output model as structured output.

## tools/ — output is applied or verified deterministically

### `tools.patch`
Propose edits as exact search/replace blocks instead of line-number diffs.

- Output: `Patchs(summary: str, patchs: List[Patch])`, `Patch(explain, search, replace, occurrence=1)`
- Apply: `apply_patches(patchs, content) -> str` / `apply_single_patch(content, patch)`
- Raises: `PatchNotFound`, `PatchAmbiguous`, `PatchOccurrenceOutOfRange`

```python
from skelet_standard.tools.patch import Patch, Patchs, apply_patches, build_system_prompt
```

### `tools.citation`
Answer a question while backing every claim with a verbatim quote from a
given source; quotes are verified by exact substring match, not trusted.

- Output: `CitedAnswer(answer: str, citations: List[Citation])`, `Citation(source, quote, note=None)`
- Verify: `verify_citations(cited, sources: dict[str, str])` (raises) or
  `find_unverifiable_citations(cited, sources)` (returns the bad ones)
- Raises: `CitationNotFound`, `UnknownSource`

```python
from skelet_standard.tools.citation import CitedAnswer, Citation, verify_citations, build_system_prompt
```

### `tools.diff_review`
Review a code diff into structured, severity-tagged comments tied to exact
quoted locations.

- Output: `DiffReview(summary: str, comments: List[ReviewComment])`,
  `ReviewComment(location, severity: "info"|"minor"|"major"|"blocking", comment, suggestion="")`
- Helper: `has_blocking_comments(review) -> bool`

```python
from skelet_standard.tools.diff_review import DiffReview, has_blocking_comments, build_system_prompt
```

### `tools.compaction`
Compress long content while being explicit about what was kept vs. dropped.

- Output: `CompactionResult(summary: str, preserved_facts: List[str], dropped: List[str])`
- Helper: `compression_ratio(original, result) -> float`

```python
from skelet_standard.tools.compaction import CompactionResult, compression_ratio, build_system_prompt
```

### `tools.long_doc`
Navigate a document too large for context by deciding which chunk to read
or what to search for, instead of reading it all at once.

- Pure chunking: `chunk_document(content, chunk_size_lines=200, overlap_lines=20) -> List[DocumentChunk]`,
  `find_chunks_containing(chunks, query) -> List[int]`
- Output: `NavigationDecision(action: "read_chunk"|"search"|"done", chunk_index=None, query=None, reason)`

```python
from skelet_standard.tools.long_doc import chunk_document, NavigationDecision, build_system_prompt
```

### `tools.chain_of_thought`
Reason step by step, with the final answer kept separate and self-contained.

- Output: `ChainOfThoughtAnswer(reasoning_steps: List[str], answer: str)`

```python
from skelet_standard.tools.chain_of_thought import ChainOfThoughtAnswer, build_system_prompt
```

### `tools.react`
Interleave reasoning with tool actions: thought → action → observation,
repeated until answerable. The caller executes `action` and fills in
`observation` — the model never fabricates one.

- Output: `ReActResult(steps: List[ReActStep], final_answer=None)`,
  `ReActStep(thought, action=None, action_input=None, observation=None)`

```python
from skelet_standard.tools.react import ReActResult, ReActStep, build_system_prompt
```

### `tools.extraction`
Pull a known set of fields out of free text, with missing fields listed
explicitly rather than guessed or silently omitted.

- Output: `ExtractionResult(fields: Dict[str, Any], missing_fields: List[str])`

```python
from skelet_standard.tools.extraction import ExtractionResult, build_system_prompt
```

## skills/ — output is advisory; nothing is auto-applied

### `skills.programming_language`
Review a code snippet against the idioms/conventions of the language it's
written in (style, not correctness). Has language-specific presets
(`python`, `java` so far) and a generic fallback for anything else.

- Output: `LanguageReview(language: str, violations: List[ConventionViolation], summary=None)`,
  `ConventionViolation(rule, location, suggestion)`
- `build_system_prompt_for(language: str) -> str` picks the specific preset
  if registered (see `REGISTRY`), else falls back to the generic skill.

```python
from skelet_standard.skills.programming_language import build_system_prompt_for, REGISTRY
```

### `skills.customer_care`
Draft a reply to a customer support message, flagged for escalation when
appropriate rather than auto-sent.

- Output: `CustomerCareResponse(reply, tone, needs_escalation=False, escalation_reason=None, referenced_facts: List[str])`

```python
from skelet_standard.skills.customer_care import CustomerCareResponse, build_system_prompt
```

### `skills.triage`
Classify and prioritize an incoming item (ticket, bug, support request) so
it can be routed.

- Output: `Triage(category: str, priority: "low"|"normal"|"high"|"urgent", rationale, duplicate_of=None)`

```python
from skelet_standard.skills.triage import Triage, build_system_prompt
```

## Adding to this catalog

New tools/skills follow the layout in [CONTRIBUTING.md](../CONTRIBUTING.md).
Add a section here in the same PR that adds the tool/skill.
