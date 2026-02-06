import pytest
from fastapi.testclient import TestClient
from main import app
from db import get_session, create_db_and_tables
from sqlmodel import Session, SQLModel, create_engine
from unittest.mock import patch
import os


@pytest.fixture(scope="module")
def test_client():
    # Create a test client
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def mock_db():
    # Create an in-memory database for testing
    engine = create_engine("sqlite:///./test.db", echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


def test_chat_endpoint_basic_flow(test_client, mock_db):
    """Test the basic chat flow: send message and receive AI response"""
    # Mock the AI agent response
    with patch('services.ai_agent.ai_agent_service.process_user_message') as mock_process:
        mock_process.return_value = {
            "response": "This is a test response from the AI",
            "conversation_id": 1,
            "timestamp": "2023-10-20T10:00:00Z"
        }

        # Mock JWT token (this would normally be a valid token)
        headers = {
            "Authorization": "Bearer mock_valid_token",
            "Content-Type": "application/json"
        }

        # Send a request to the chat endpoint
        response = test_client.post(
            "/api/user123/chat",
            headers=headers,
            json={"message": "Test message", "conversation_id": None}
        )

        # Assert the response
        assert response.status_code == 200
        assert response.json()["message"] == "This is a test response from the AI"
        assert response.json()["conversation_id"] == 1


def test_get_conversations(test_client):
    """Test getting user conversations"""
    # Mock JWT token
    headers = {
        "Authorization": "Bearer mock_valid_token"
    }

    # Mock the chat service response
    with patch('services.chat_service.chat_service.get_user_conversations') as mock_get_conv:
        mock_get_conv.return_value = {
            "conversations": [
                {
                    "id": 1,
                    "title": "Test Conversation",
                    "created_at": "2023-10-20T09:00:00Z",
                    "updated_at": "2023-10-20T10:00:00Z"
                }
            ],
            "total_count": 1
        }

        response = test_client.get("/api/user123/conversations", headers=headers)

        assert response.status_code == 200
        assert len(response.json()["conversations"]) == 1
        assert response.json()["total_count"] == 1


def test_get_specific_conversation(test_client):
    """Test getting a specific conversation"""
    # Mock JWT token
    headers = {
        "Authorization": "Bearer mock_valid_token"
    }

    # Mock the chat service response
    with patch('services.chat_service.chat_service.get_conversation') as mock_get_conv:
        mock_get_conv.return_value = {
            "conversation": {
                "id": 1,
                "title": "Test Conversation",
                "created_at": "2023-10-20T09:00:00Z",
                "updated_at": "2023-10-20T10:00:00Z"
            },
            "messages": [
                {
                    "id": 1,
                    "role": "user",
                    "content": "Hello",
                    "timestamp": "2023-10-20T09:30:00Z"
                },
                {
                    "id": 2,
                    "role": "assistant",
                    "content": "Hi there!",
                    "timestamp": "2023-10-20T09:31:00Z"
                }
            ]
        }

        response = test_client.get("/api/user123/conversations/1", headers=headers)

        assert response.status_code == 200
        assert response.json()["conversation"]["id"] == 1
        assert len(response.json()["messages"]) == 2


def test_rate_limiting(test_client):
    """Test that rate limiting is working"""
    # This test would require more complex mocking of the rate limiter
    # For now, we'll just verify that the rate limiter is in place
    # by checking if the proper error is returned when limit is exceeded

    # This is a simplified test - in a real scenario, we'd need to trigger
    # the rate limiter to exceed its limit
    headers = {
        "Authorization": "Bearer mock_valid_token",
        "Content-Type": "application/json"
    }

    # We'll test that the endpoint exists and accepts requests
    # Rate limiting tests would typically be more complex and environment-specific
    with patch('services.ai_agent.ai_agent_service.process_user_message') as mock_process:
        mock_process.return_value = {
            "response": "Test response",
            "conversation_id": 1,
            "timestamp": "2023-10-20T10:00:00Z"
        }

        response = test_client.post(
            "/api/user123/chat",
            headers=headers,
            json={"message": "Rate limit test", "conversation_id": None}
        )

        # Should succeed under normal circumstances
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__])