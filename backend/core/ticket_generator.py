import uuid
from backend.api.schemas import TicketCreate
from backend.core.entity_extractor import ExtractedEntities


def generate_ticket(session_id: str, intent: str, entities: ExtractedEntities) -> TicketCreate:
    return TicketCreate(
        session_id=session_id,
        intent=intent,
        product=entities.product,
        quantity=entities.quantity,
        order_id=entities.order_number,
        invoice_number=entities.invoice_number,
        description=entities.description,
    )


def generate_ticket_id() -> str:
    return f"TKT-{uuid.uuid4().hex[:8].upper()}"
