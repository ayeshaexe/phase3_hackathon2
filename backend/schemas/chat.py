from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class SendMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class SendMessageResponse(BaseModel):
    message: str
    conversation_id: int
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


class MessageSchema(BaseModel):
    id: int
    role: str
    content: str
    timestamp: str


class ConversationSummary(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str


class GetConversationsResponse(BaseModel):
    conversations: List[ConversationSummary]
    total_count: int


class GetConversationResponse(BaseModel):
    conversation: ConversationSummary
    messages: List[MessageSchema]