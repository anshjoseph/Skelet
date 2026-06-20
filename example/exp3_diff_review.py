"""
Diff review example: structured, severity-tagged comments tied to exact
quoted locations in a diff.

Run: python example/exp3_diff_review.py
"""

from skelet_standard.tools.diff_review import DiffReview, ReviewComment, build_system_prompt, has_blocking_comments

print(build_system_prompt())
print("\n" + "=" * 80 + "\n")

# Pretend this is the model's structured output after reviewing a diff that
# added an unguarded dict access.
review = DiffReview(
    summary="one correctness risk, otherwise fine",
    comments=[
        ReviewComment(
            location='config["timeout"]',
            severity="blocking",
            comment="KeyError if 'timeout' is missing from config",
            suggestion='config.get("timeout", DEFAULT_TIMEOUT)',
        ),
        ReviewComment(
            location="def run(x,y):",
            severity="minor",
            comment="missing space after comma",
            suggestion="def run(x, y):",
        ),
    ],
)

print(review.summary)
for c in review.comments:
    print(f"[{c.severity}] {c.location}: {c.comment} -> {c.suggestion}")

if has_blocking_comments(review):
    print("\nBLOCKED: fix blocking comments before merge")
