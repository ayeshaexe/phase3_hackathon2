from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import DateTime, Column
from sqlalchemy.dialects.postgresql import JSONB


class MessageBase(SQLModel):
    conversation_id: int = Field(index=True, foreign_key="conversation.id")
    role: str = Field(regex="^(user|assistant)$")  # Either "user" or "assistant"
    content: str = Field(max_length=5000)


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Set defaults at the database level using SQLModel syntax with timezone-aware datetimes
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime, nullable=False)

    # Optional metadata field for storing additional data like token usage, model info
    metadata_: Optional[dict] = Field(default=None, sa_column=Column(JSONB))


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    timestamp: datetime
    metadata_: Optional[dict] = None