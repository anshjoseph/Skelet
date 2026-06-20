"""
Long-document reading data model — framework-agnostic.

For content too long to put in context at once, the model doesn't read the
whole thing — it gets handed chunks and decides where to go next. The
chunking/lookup logic here is pure and deterministic; only the navigation
*decision* (what to read next) comes from the model.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    index: int
    start_line: int
    end_line: int
    content: str


def chunk_document(content: str, chunk_size_lines: int = 200, overlap_lines: int = 20) -> List[DocumentChunk]:
    """Split content into overlapping line-based chunks. Overlap avoids losing
    context that straddles a chunk boundary."""
    if chunk_size_lines <= overlap_lines:
        raise ValueError("chunk_size_lines must be greater than overlap_lines")

    lines = content.splitlines()
    if not lines:
        return [DocumentChunk(index=0, start_line=1, end_line=0, content="")]

    chunks: List[DocumentChunk] = []
    step = chunk_size_lines - overlap_lines
    start = 0
    index = 0
    while start < len(lines):
        end = min(start + chunk_size_lines, len(lines))
        chunks.append(
            DocumentChunk(
                index=index,
                start_line=start + 1,
                end_line=end,
                content="\n".join(lines[start:end]),
            )
        )
        if end == len(lines):
            break
        start += step
        index += 1
    return chunks


def find_chunks_containing(chunks: List[DocumentChunk], query: str) -> List[int]:
    """Return indexes of chunks whose content contains `query` (case-insensitive)."""
    q = query.lower()
    return [c.index for c in chunks if q in c.content.lower()]


class NavigationDecision(BaseModel):
    action: Literal["read_chunk", "search", "done"] = Field(
        description="'read_chunk' to view a specific chunk by index, 'search' to "
        "look for a keyword/phrase across chunks, 'done' once enough has been read"
    )
    chunk_index: Optional[int] = Field(default=None, description="required when action='read_chunk'")
    query: Optional[str] = Field(default=None, description="required when action='search'")
    reason: str = Field(description="why this action moves the task forward")
