"""
Prompt + skill for customer-care responses. Framework-agnostic: only builds
text to feed to whatever model client the caller is using.
"""

from skelet.core import Priority, Rule, SkillPrompt

CUSTOMER_CARE_SKILL = SkillPrompt(
    name="customer-care-response",
    description=(
        "Draft a reply to a customer support message. Use whenever a "
        "customer message needs a response that should be reviewed/checked "
        "before sending, not auto-sent."
    ),
    overview=(
        "You return a CustomerCareResponse: `reply`, `tone`, whether it "
        "`needs_escalation` (and why), and `referenced_facts` the reply "
        "depends on so they can be verified."
    ),
    when_to_use=[
        "A customer message needs a drafted reply",
    ],
    when_not_to_use=[
        "The message is abusive, a legal threat, or a safety issue — escalate immediately rather than drafting a reply",
    ],
    instructions=[
        "Read the customer's message and identify what they actually need",
        "Draft a reply addressing it directly, in a tone appropriate to the situation",
        "List any account/order/policy facts the reply depends on in `referenced_facts`",
        "If the request requires authority, policy exceptions, or you are not "
        "confident the facts are correct, set `needs_escalation=true` with a reason",
    ],
    rules=[
        Rule(
            name="NO_INVENTED_FACTS",
            description="never state an account/order/policy fact you weren't given — list what you relied on instead of guessing",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="ESCALATE_WHEN_UNSURE",
            description="if confidence is low or the issue needs human judgment/authority, escalate rather than guess",
            priority=Priority.CRITICAL,
        ),
        Rule(
            name="MATCH_TONE_TO_SITUATION",
            description="use an empathetic/apologetic tone for complaints, neutral for routine requests",
            priority=Priority.HIGH,
        ),
    ],
    edge_cases=[
        "customer is angry/abusive — keep the reply calm, still flag for escalation if appropriate",
        "request requires a refund/exception outside given policy facts — escalate",
    ],
    output_format="A CustomerCareResponse object.",
    validation_checklist=[
        "No invented account/order/policy facts",
        "needs_escalation has a reason whenever it is true",
    ],
)


def build_system_prompt() -> str:
    return CUSTOMER_CARE_SKILL.render_body()
