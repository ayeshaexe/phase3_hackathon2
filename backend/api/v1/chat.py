from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from sqlmodel import Session
from typing import Optional
import sys
import os

# Add the backend directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db import get_session
from utils.jwt import get_current_user
from services.chat_service import chat_service
from utils.response import success_response, error_response
from utils.rate_limiter import limiter, CHAT_RATE_LIMIT
from schemas.chat import SendMessageRequest, SendMessageResponse, GetConversationsResponse, GetConversationResponse


router = APIRouter()


@router.post("/{user_id}/chat", response_model=SendMessageResponse)
@limiter.limit(CHAT_RATE_LIMIT)
def send_chat_message(
    request: Request,
    user_id: str,
    chat_request: SendMessageRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Send a message to the AI chat agent
    """
    try:
        # Verify that the user_id in the path matches the authenticated user
        authenticated_user_id = current_user.get("userId") or current_user.get("sub")

        if not authenticated_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        if authenticated_user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_response("ACCESS_DENIED", "Access denied: user ID mismatch")
            )

        # Process the message using the chat service
        result = chat_service.send_message(
            db_session=db,
            user_id=user_id,
            message=chat_request.message,
            conversation_id=chat_request.conversation_id
        )

        # Return the AI response
        return SendMessageResponse(
            message=result["response"],
            conversation_id=result["conversation_id"],
            timestamp=result["timestamp"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("CHAT_ERROR", f"Error processing chat message: {str(e)}")
        )


@router.get("/{user_id}/conversations", response_model=GetConversationsResponse)
async def get_user_conversations(
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get all conversations for a user
    """
    try:
        # Verify that the user_id in the path matches the authenticated user
        authenticated_user_id = current_user.get("userId") or current_user.get("sub")

        if not authenticated_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        if authenticated_user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_response("ACCESS_DENIED", "Access denied: user ID mismatch")
            )

        # Get user conversations using the chat service
        result = chat_service.get_user_conversations(
            db_session=db,
            user_id=user_id,
            limit=limit,
            offset=offset
        )

        return GetConversationsResponse(
            conversations=result["conversations"],
            total_count=result["total_count"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("FETCH_CONVERSATIONS_ERROR", f"Error fetching conversations: {str(e)}")
        )


@router.get("/{user_id}/conversations/{conversation_id}", response_model=GetConversationResponse)
async def get_conversation(
    user_id: str,
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get a specific conversation and its message history
    """
    try:
        # Verify that the user_id in the path matches the authenticated user
        authenticated_user_id = current_user.get("userId") or current_user.get("sub")

        if not authenticated_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        if authenticated_user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_response("ACCESS_DENIED", "Access denied: user ID mismatch")
            )

        # Get conversation using the chat service
        result = chat_service.get_conversation(
            db_session=db,
            conversation_id=conversation_id,
            user_id=user_id
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("CONVERSATION_NOT_FOUND", "Conversation not found or access denied")
            )

        return GetConversationResponse(
            conversation=result["conversation"],
            messages=result["messages"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("FETCH_CONVERSATION_ERROR", f"Error fetching conversation: {str(e)}")
        )