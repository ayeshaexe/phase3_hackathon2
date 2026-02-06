"""
Chat Service for Todo Chatbot
Handles chat-specific operations combining AI agent and conversation management
"""
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from datetime import datetime

from models.conversation import Conversation, ConversationCreate
from models.message import Message, MessageCreate
from services.ai_agent import ai_agent_service


class ChatService:
    """
    Service class for handling chat operations
    """

    def send_message(
        self,
        db_session: Session,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return AI response

        Args:
            db_session: Database session
            user_id: ID of the user
            message: The message from the user
            conversation_id: Optional conversation ID (creates new if None)

        Returns:
            Dictionary with response and conversation info
        """
        return ai_agent_service.process_user_message(
            db_session=db_session,
            user_id=user_id,
            user_message=message,
            conversation_id=conversation_id
        )

    def get_conversation(
        self,
        db_session: Session,
        conversation_id: int,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a conversation and its messages

        Args:
            db_session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            Dictionary with conversation and messages, or None if not found
        """
        # Verify conversation belongs to user
        conversation_statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(conversation_statement).first()

        if not conversation:
            return None

        # Get messages for the conversation
        messages_statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp)
        messages = db_session.exec(messages_statement).all()

        return {
            "conversation": {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat()
            },
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        }

    def get_user_conversations(
        self,
        db_session: Session,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get all conversations for a user

        Args:
            db_session: Database session
            user_id: ID of the user
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip

        Returns:
            Dictionary with conversations and total count
        """
        # Count total conversations for the user
        count_statement = select(Conversation).where(Conversation.user_id == user_id)
        all_conversations = db_session.exec(count_statement).all()
        total_count = len(all_conversations)

        # Get paginated conversations
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )

        conversations = db_session.exec(statement).all()

        return {
            "conversations": [
                {
                    "id": conv.id,
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ],
            "total_count": total_count
        }


# Global instance
chat_service = ChatService()