from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.core.llm import get_llm

REQUIRED_FIELDS_BY_INTENT = {
    "order_management": ["order_number"],
    "quotation_request": ["product", "quantity"],
    "invoice_query": ["invoice_number"],
    "other_support": ["description"],
}

FOLLOWUP_PROMPT = PromptTemplate.from_template(
    """You are a helpful B2B support assistant. The user wants help with: {intent}.
The following required information is still missing: {missing_fields}.
Ask a natural, friendly follow-up question to collect this information.
Keep it concise."""
)


FIELD_VALIDATORS = {
    "order_number": lambda v: isinstance(v, str) and v.startswith("CA")
}


def get_missing_fields(intent: str, entities: dict) -> list[str]:
    required = REQUIRED_FIELDS_BY_INTENT.get(intent, [])
    missing = []
    for f in required:
        value = entities.get(f)
        validator = FIELD_VALIDATORS.get(f)
        if not value or (validator and not validator(value)):
            missing.append(f)
    return missing


def generate_followup(intent: str, missing_fields: list[str]) -> str:
    chain = FOLLOWUP_PROMPT | get_llm() | StrOutputParser()
    return chain.invoke({
        "intent": intent,
        "missing_fields": ", ".join(missing_fields)
    })
