"""
Search/replace patch data model — framework- and language-agnostic.

A patch quotes the EXACT existing text to replace ("search") and what to
replace it with ("replace"), instead of addressing by line number. Patches
are verified deterministically before being applied:
    * search text must be found in the current content
    * search text must be unique (or the caller must specify which
      occurrence it means)
If a patch is ambiguous or not found, nothing is guessed — the error is
raised so the caller (whatever framework/language is driving generation)
can decide how to recover.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class PatchError(Exception):
    """Base class for all patch-application failures."""


class PatchNotFound(PatchError):
    def __init__(self, explain: str, search: str):
        self.explain = explain
        self.search = search
        super().__init__(f"Search block not found for patch: {explain}")


class PatchAmbiguous(PatchError):
    def __init__(self, explain: str, search: str, count: int):
        self.explain = explain
        self.search = search
        self.count = count
        super().__init__(f"Search block matched {count} times (not unique) for patch: {explain}")


class PatchOccurrenceOutOfRange(PatchError):
    def __init__(self, explain: str, occurrence: int, count: int):
        super().__init__(
            f"Patch '{explain}' requested occurrence {occurrence} but only {count} matches exist"
        )


class Patch(BaseModel):
    explain: str = Field(description="explanation of what this patch does and why it helps")
    search: str = Field(
        description=(
            "exact existing block of text to find and replace, copied verbatim "
            "including whitespace/indentation. Must be unique in the file — prefer "
            "including a distinctive line (comment, unique identifier, signature) "
            "rather than generic lines like bare loop headers or blank lines, "
            "which often repeat elsewhere in the file."
        )
    )
    replace: str = Field(description="new block of text to put in place of `search`")
    occurrence: int = Field(
        default=1,
        description=(
            "1-based index of which match of `search` to replace, only relevant if "
            "search text legitimately appears more than once and cannot be made "
            "unique with more context. Defaults to 1 (first match)."
        ),
    )


class Patchs(BaseModel):
    summary: str = Field(description="summary of what this set of patches accomplishes")
    patchs: List[Patch]


def _find_nth_occurrence(haystack: str, needle: str, n: int) -> int:
    """Return the start index of the n-th (1-based) occurrence of needle in haystack, or -1."""
    idx = -1
    for _ in range(n):
        idx = haystack.find(needle, idx + 1)
        if idx == -1:
            return -1
    return idx


def apply_single_patch(content: str, patch: Patch) -> str:
    """
    Apply one patch to `content`. Raises PatchNotFound / PatchAmbiguous /
    PatchOccurrenceOutOfRange if the search block can't be unambiguously
    located. Never guesses.
    """
    count = content.count(patch.search)

    if count == 0:
        raise PatchNotFound(patch.explain, patch.search)

    if patch.occurrence > count:
        raise PatchOccurrenceOutOfRange(patch.explain, patch.occurrence, count)

    if count > 1 and patch.occurrence == 1:
        # Ambiguous: more than one match and caller didn't disambiguate.
        raise PatchAmbiguous(patch.explain, patch.search, count)

    start = _find_nth_occurrence(content, patch.search, patch.occurrence)
    end = start + len(patch.search)
    return content[:start] + patch.replace + content[end:]


def apply_patches(patchs: Patchs, content: str) -> str:
    """
    Apply all patches in order. Each patch is applied to the *result* of the
    previous one (since matching is content-based, not position-based,
    order generally doesn't matter unless two patches target overlapping
    text).
    """
    for patch in patchs.patchs:
        content = apply_single_patch(content, patch)
    return content


def add_line_numbers(content: str) -> str:
    """Add line numbers for the model's *reading* context only. These numbers
    are never fed back into patch application — only exact text is matched."""
    lines = content.splitlines()
    width = len(str(len(lines))) if lines else 1
    return "\n".join(f"{str(i + 1).rjust(width)}| {line}" for i, line in enumerate(lines))
