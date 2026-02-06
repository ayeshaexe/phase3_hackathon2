"""
Conversation Service for Todo Chatbot
Handles all conversation-related database operations
"""
from typing import List, Optional
from sqlmodel import Session, select, asc, desc
from datetime import datetime

from models.conversation import Conversation
from models.message import Message


class ConversationService:
    """
    Service class for handling conversation operations
    """

    def get_user_conversations(
        self,
        db_session: Session,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Conversation], int]:
        """
        Get all conversations for a user with pagination

        Args:
            db_session: Database session
            user_id: ID of the user
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip

        Returns:
            Tuple of (list of conversations, total count)
        """
        # Count total conversations for the user
        count_statement = select(Conversation).where(Conversation.user_id == user_id)
        total_count = len(db_session.exec(count_statement).all())

        # Get paginated conversations
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.updated_at))
            .offset(offset)
            .limit(limit)
        )

        conversations = db_session.exec(statement).all()

        return conversations, total_count

    def get_conversation_by_id(
        self,
        db_session: Session,
        conversation_id: int,
        user_id: str
    ) -> Optional[Conversation]:
        """
        Get a specific conversation by ID and user

        Args:
            db_session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            Conversation object if found, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )

        return db_session.exec(statement).first()

    def get_conversation_messages(
        self,
        db_session: Session,
        conversation_id: int,
        user_id: str
    ) -> List[Message]:
        """
        Get all messages for a specific conversation

        Args:
            db_session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            List of Message objects
        """
        # First verify the conversation belongs to the user
        conversation_stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(conversation_stmt).first()

        if not conversation:
            return []

        # Get messages for the conversation
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(asc(Message.timestamp))
        )

        return db_session.exec(statement).all()

    def create_conversation(
        self,
        db_session: Session,
        user_id: str,
        title: str
    ) -> Conversation:
        """
        Create a new conversation

        Args:
            db_session: Database session
            user_id: ID of the user
            title: Title of the conversation

        Returns:
            Created Conversation object
        """
        conversation = Conversation(
            user_id=user_id,
            title=title
        )

        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)

        return conversation

    def update_conversation_title(
        self,
        db_session: Session,
        conversation_id: int,
        user_id: str,
        title: str
    ) -> Optional[Conversation]:
        """
        Update the title of a conversation

        Args:
            db_session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user
            title: New title for the conversation

        Returns:
            Updated Conversation object if successful, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(statement).first()

        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.now()

            db_session.add(conversation)
            db_session.commit()
            db_session.refresh(conversation)

            return conversation

        return None

    def delete_conversation(
        self,
        db_session: Session,
        conversation_id: int,
        user_id: str
    ) -> bool:
        """
        Delete a conversation (cascades to messages)

        Args:
            db_session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            True if successful, False otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(statement).first()

        if conversation:
            db_session.delete(conversation)
            db_session.commit()
            return True

        return False


# Global instance
conversation_service = ConversationService()