from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class ConversationBase(SQLModel):
    user_id: str = Field(index=True)  # User ID from JWT
    title: str = Field(max_length=200)


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Set defaults at the database level using SQLModel syntax with timezone-aware datetimes
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime, nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime, nullable=False)


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime