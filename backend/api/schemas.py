from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    session_id: str = Field(..., description="Unique session identifier")


class ChatResponse(BaseModel):
    session_id: str
    response: str
    intent: Optional[str] = None
    ticket_id: Optional[str] = None


class TicketCreate(BaseModel):
    session_id: str
    intent: str
    product: Optional[str] = None
    quantity: Optional[int] = None
    order_id: Optional[str] = None
    invoice_number: Optional[str] = None
    description: Optional[str] = None


class TicketResponse(TicketCreate):
    ticket_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationLogResponse(BaseModel):
    session_id: str
    query: str
    response: str
    timestamp: datetime

    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    session_id: str
    logs: list[ConversationLogResponse]
