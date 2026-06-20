"""
Skills example: advisory output that nothing auto-applies — triage,
customer care, and per-language code review.

Run: python example/exp6_skills.py
"""

from skelet_standard.skills.customer_care import CustomerCareResponse
from skelet_standard.skills.programming_language import REGISTRY, build_system_prompt_for
from skelet_standard.skills.triage import Triage

print("--- triage ---")
ticket = Triage(
    category="bug",
    priority="urgent",
    rationale="reported data loss affecting all users on the latest deploy",
)
print(ticket)

print("\n--- customer care ---")
reply = CustomerCareResponse(
    reply="I'm sorry about the trouble — I've issued a refund to your original payment method; it should appear within 5-7 business days.",
    tone="apologetic",
    needs_escalation=False,
    referenced_facts=["refund policy: 5-7 business days to original payment method"],
)
print(reply)

print("\n--- programming language conventions ---")
print("registered presets:", list(REGISTRY.keys()))
print(build_system_prompt_for("python")[:200], "...")
print(build_system_prompt_for("rust")[:200], "...  (falls back to generic, no preset for rust)")
