"""
Long-document navigation example: chunk a large document, let the model
decide where to look instead of reading it all at once.

Run: python example/exp4_long_doc.py
"""

from skelet_standard.tools.long_doc import NavigationDecision, build_system_prompt, chunk_document, find_chunks_containing

print(build_system_prompt())
print("\n" + "=" * 80 + "\n")

document = "\n".join(f"line {i}: some log content" if i != 342 else f"line {i}: ERROR disk full" for i in range(1, 600))

chunks = chunk_document(document, chunk_size_lines=200, overlap_lines=20)
print(f"split into {len(chunks)} chunks")

# Turn 1: model decides to search instead of reading sequentially.
decision = NavigationDecision(action="search", query="ERROR", reason="looking for the failure mentioned in the task")
print(decision)

matches = find_chunks_containing(chunks, decision.query)
print(f"chunks containing '{decision.query}': {matches}")

# Turn 2: model reads the chunk that matched.
decision2 = NavigationDecision(
    action="read_chunk",
    chunk_index=matches[0],
    reason="confirm the exact error before answering",
)
target = next(c for c in chunks if c.index == decision2.chunk_index)
print(f"reading chunk {target.index} (lines {target.start_line}-{target.end_line})")
