from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from langgraph.graph import END
from backend.core.intent_classifier import classify_intent
from backend.core.entity_extractor import extract_entities, ExtractedEntities
from backend.core.conversation_manager import get_missing_fields, generate_followup
from backend.core.ticket_generator import generate_ticket, generate_ticket_id
from backend.api.schemas import TicketCreate


class ChatState(TypedDict):
    session_id: str
    query: str
    intent: Optional[str]
    entities: Optional[dict]
    missing_fields: list[str]
    followup_question: Optional[str]
    ticket: Optional[TicketCreate]
    ticket_id: Optional[str]
    response: str


def classify_node(state: ChatState) -> ChatState:
    state["intent"] = classify_intent(state["query"])
    return state


def extract_node(state: ChatState) -> ChatState:
    entities: ExtractedEntities = extract_entities(state["query"])
    new_entities = {k: v for k, v in entities.model_dump().items() if v is not None}
    existing = state.get("entities") or {}
    state["entities"] = {**existing, **new_entities}
    return state


def check_missing_node(state: ChatState) -> ChatState:
    state["missing_fields"] = get_missing_fields(state["intent"], state["entities"])
    return state


def followup_node(state: ChatState) -> ChatState:
    state["followup_question"] = generate_followup(state["intent"], state["missing_fields"])
    state["response"] = state["followup_question"]
    return state


def generate_ticket_node(state: ChatState) -> ChatState:
    entities = ExtractedEntities(**state["entities"])
    ticket = generate_ticket(state["session_id"], state["intent"], entities)
    ticket_id = generate_ticket_id()
    state["ticket"] = ticket
    state["ticket_id"] = ticket_id
    state["response"] = (
        f"Your support ticket has been created successfully! "
        f"Ticket ID: **{ticket_id}** | Intent: {state['intent']}. "
        f"Our team will get back to you shortly."
    )
    return state


def route_after_check(state: ChatState) -> str:
    return "followup" if state["missing_fields"] else "generate_ticket"


def build_chatbot_graph() -> StateGraph:
    graph = StateGraph(ChatState)
    graph.add_node("classify", classify_node)
    graph.add_node("extract", extract_node)
    graph.add_node("check_missing", check_missing_node)
    graph.add_node("followup", followup_node)
    graph.add_node("generate_ticket", generate_ticket_node)

    graph.set_entry_point("classify")
    graph.add_edge("classify", "extract")
    graph.add_edge("extract", "check_missing")
    graph.add_conditional_edges("check_missing", route_after_check, {
        "followup": "followup",
        "generate_ticket": "generate_ticket",
    })
    graph.add_edge("followup", END)
    graph.add_edge("generate_ticket", END)

    return graph.compile()


chatbot_graph = build_chatbot_graph()
