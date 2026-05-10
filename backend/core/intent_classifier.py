from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.core.llm import get_llm

INTENT_PROMPT = PromptTemplate.from_template(
    """Classify the following customer support query into one of these intents:
- order_management
- quotation_request
- invoice_query
- other_support

Query: {query}

Respond with only the intent label."""
)


def classify_intent(query: str) -> str:
    chain = INTENT_PROMPT | get_llm() | StrOutputParser()
    return chain.invoke({"query": query}).strip().lower()
