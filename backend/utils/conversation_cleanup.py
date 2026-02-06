"""
Utility functions for cleaning up conversation resources
"""
from sqlmodel import Session, select
from datetime import datetime, timedelta
from models.conversation import Conversation
from models.message import Message


def cleanup_old_conversations(db_session: Session, days_old: int = 365):
    """
    Clean up conversations that are older than the specified number of days

    Args:
        db_session: Database session
        days_old: Delete conversations older than this many days (default: 365)

    Returns:
        Number of conversations deleted
    """
    cutoff_date = datetime.now() - timedelta(days=days_old)

    # Find conversations to delete
    statement = select(Conversation).where(Conversation.created_at < cutoff_date)
    conversations_to_delete = db_session.exec(statement).all()

    deleted_count = 0
    for conversation in conversations_to_delete:
        # Delete associated messages first (due to foreign key constraint)
        message_statement = select(Message).where(Message.conversation_id == conversation.id)
        messages = db_session.exec(message_statement).all()

        for message in messages:
            db_session.delete(message)

        # Delete the conversation
        db_session.delete(conversation)
        deleted_count += 1

    # Commit the changes
    db_session.commit()

    return deleted_count


def cleanup_empty_conversations(db_session: Session):
    """
    Clean up conversations that have no messages

    Args:
        db_session: Database session

    Returns:
        Number of empty conversations deleted
    """
    # Find conversations that have no associated messages
    # This is a more complex query, so we'll do it in two steps

    all_conversations = db_session.exec(select(Conversation)).all()
    deleted_count = 0

    for conversation in all_conversations:
        message_count_statement = select(Message).where(Message.conversation_id == conversation.id)
        messages = db_session.exec(message_count_statement).all()

        if len(messages) == 0:
            # This conversation has no messages, delete it
            db_session.delete(conversation)
            deleted_count += 1

    # Commit the changes
    db_session.commit()

    return deleted_count


def get_conversation_stats(db_session: Session):
    """
    Get statistics about conversations in the database

    Args:
        db_session: Database session

    Returns:
        Dictionary with conversation statistics
    """
    total_conversations = db_session.exec(select(Conversation)).all()
    total_count = len(total_conversations)

    # Count messages
    total_messages = db_session.exec(select(Message)).all()
    message_count = len(total_messages)

    # Calculate average messages per conversation
    avg_messages_per_conversation = message_count / total_count if total_count > 0 else 0

    # Find oldest conversation
    if total_conversations:
        oldest = min(conversation.created_at for conversation in total_conversations)
        newest = max(conversation.updated_at for conversation in total_conversations)
    else:
        oldest = None
        newest = None

    return {
        "total_conversations": total_count,
        "total_messages": message_count,
        "avg_messages_per_conversation": avg_messages_per_conversation,
        "oldest_conversation": oldest.isoformat() if oldest else None,
        "newest_activity": newest.isoformat() if newest else None
    }