from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from typing import Optional
from backend.core.llm import get_llm

ENTITY_PROMPT = PromptTemplate.from_template(
    """Extract the following entities from the customer query. Return a JSON object.
Fields: product, quantity (integer or null), order_number, invoice_number, description.
Use null for missing fields.

Query: {query}

JSON:"""
)


class ExtractedEntities(BaseModel):
    product: Optional[str] = None
    quantity: Optional[int] = None
    order_number: Optional[str] = None
    invoice_number: Optional[str] = None
    description: Optional[str] = None


def extract_entities(query: str) -> ExtractedEntities:
    chain = ENTITY_PROMPT | get_llm() | JsonOutputParser()
    result = chain.invoke({"query": query})
    return ExtractedEntities(**result)
