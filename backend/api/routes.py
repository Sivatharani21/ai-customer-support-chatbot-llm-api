from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.api.schemas import ChatRequest, ChatResponse, HistoryResponse, ConversationLogResponse, TicketResponse
from backend.core.chatbot import chatbot_graph
from backend.db.database import get_db
from backend.db.models import Ticket, ConversationLog
from backend.core.ticket_generator import generate_ticket_id

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    state = chatbot_graph.invoke({
        "session_id": request.session_id,
        "query": request.message,
        "intent": None,
        "entities": {},
        "missing_fields": [],
        "followup_question": None,
        "ticket": None,
        "ticket_id": None,
        "response": "",
    })

    log = ConversationLog(
        session_id=request.session_id,
        query=request.message,
        response=state["response"],
    )
    db.add(log)

    ticket_id = None
    if state.get("ticket") and state.get("ticket_id"):
        ticket_data = state["ticket"]
        ticket_id = state["ticket_id"]
        ticket = Ticket(
            ticket_id=ticket_id,
            session_id=ticket_data.session_id,
            intent=ticket_data.intent,
            product=ticket_data.product,
            quantity=ticket_data.quantity,
            order_id=ticket_data.order_id,
            invoice_number=ticket_data.invoice_number,
            description=ticket_data.description,
        )
        db.add(ticket)

    db.commit()

    return ChatResponse(
        session_id=request.session_id,
        response=state["response"],
        intent=state.get("intent"),
        ticket_id=ticket_id,
    )


@router.get("/tickets", response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    return [TicketResponse.model_validate(t) for t in tickets]


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketResponse.model_validate(ticket)


@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    rows = (
        db.query(ConversationLog.session_id, func.max(ConversationLog.timestamp).label("last_active"))
        .group_by(ConversationLog.session_id)
        .order_by(func.max(ConversationLog.timestamp).desc())
        .all()
    )
    return [{"session_id": r.session_id, "last_active": r.last_active.strftime("%Y-%m-%d %H:%M")} for r in rows]


@router.get("/history", response_model=HistoryResponse)
def get_history(session_id: str, db: Session = Depends(get_db)):
    logs = db.query(ConversationLog).filter(
        ConversationLog.session_id == session_id
    ).order_by(ConversationLog.timestamp).all()

    return HistoryResponse(
        session_id=session_id,
        logs=[ConversationLogResponse.model_validate(log) for log in logs],
    )
