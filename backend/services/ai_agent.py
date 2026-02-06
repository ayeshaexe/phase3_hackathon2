"""
OpenAI Agents SDK Service for Todo Chatbot
Implements AI agent functionality using OpenAI Agents SDK with OpenRouter
"""
import os
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv
import openai
from agents.agent import Agent
from agents.run import Runner
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents import function_tool
from utils.logger import log_chat_interaction, log_error
from utils.performance_monitor import performance_monitor

from models.conversation import Conversation
from models.message import Message
from sqlmodel import Session, select
from openai import OpenAI, AsyncOpenAI  # Use both clients as per user specification

# Import task services
from services.task_service import create_task, get_tasks_by_user, update_task_by_id, delete_task_by_id
from models.task import TaskCreate

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

# Configure OpenAI client to use OpenRouter (synchronous for API calls)
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# Create model configuration for OpenRouter (using AsyncOpenAI for the model)
async_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# Define the model for OpenRouter - using correct parameter names
model = OpenAIChatCompletionsModel(
    openai_client=async_client,
    model="openrouter/auto",  # Auto-selects best available model including free ones
)

class AIAgentService:
    """
    Service class for handling AI agent interactions using OpenAI Agents SDK with OpenRouter
    """

    def __init__(self):
        # Create the main AI agent with instructions
        self.agent = Agent(
            name="Todo Assistant",
            instructions=(
                "You are a helpful assistant for managing todo tasks. "
                "Help users add, update, and manage their tasks using natural language. "
                "Be concise but friendly in your responses. Always confirm important actions. "
                "Use the available tools to interact with the todo system. "
                "When a user wants to add a task, use the create_task_tool. "
                "When a user wants to see their tasks, use the get_tasks_tool. "
                "When a user wants to update a task, use the update_task_tool. "
                "When a user wants to delete a task, use the delete_task_tool."
            ),
            model=model
        )

    def process_user_message(
        self,
        db_session: Session,
        user_id: str,
        user_message: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return AI response using OpenAI Agents SDK

        Args:
            db_session: Database session
            user_id: ID of the user
            user_message: The message from the user
            conversation_id: Optional conversation ID (creates new if None)

        Returns:
            Dictionary with response and conversation info
        """

        # Get or create conversation
        if conversation_id is None:
            conversation = Conversation(
                user_id=user_id,
                title=user_message[:100] + "..." if len(user_message) > 100 else user_message
            )
            db_session.add(conversation)
            db_session.commit()
            db_session.refresh(conversation)
            conversation_id = conversation.id
        else:
            # Verify conversation belongs to user
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conversation = db_session.exec(statement).first()
            if not conversation:
                raise ValueError("Conversation not found or access denied")

        try:
            # Measure performance of the AI response
            import time
            start_time = time.time()

            # Dynamically create tools with the specific context
            @function_tool
            def create_task_tool_local(title: str, description: Optional[str] = None, completed: bool = False) -> Dict[str, Any]:
                """Create a new task for the user. Use this when the user wants to add a new task."""
                try:
                    # Prepare task data for creation
                    task_data = TaskCreate(
                        title=title,
                        description=description,
                        completed=completed
                    )

                    # Create task using service
                    db_task = create_task(db_session, task_data, user_id)

                    return {
                        "success": True,
                        "task_id": db_task.id,
                        "title": db_task.title,
                        "description": db_task.description,
                        "completed": db_task.completed,
                        "message": f"Task '{db_task.title}' has been created successfully."
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "message": f"Failed to create task: {str(e)}"
                    }

            @function_tool
            def get_tasks_tool_local(status_filter: Optional[str] = None) -> Dict[str, Any]:
                """Get all tasks for the user. Use this when the user wants to see their tasks."""
                try:
                    # Get tasks using service
                    tasks = get_tasks_by_user(db_session, user_id, status_filter)

                    task_list = []
                    for task in tasks:
                        task_list.append({
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "completed": task.completed,
                            "created_at": task.created_at.isoformat() if task.created_at else None
                        })

                    return {
                        "success": True,
                        "tasks": task_list,
                        "count": len(task_list),
                        "message": f"Retrieved {len(task_list)} tasks."
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "message": f"Failed to get tasks: {str(e)}"
                    }

            @function_tool
            def update_task_tool_local(task_id: int, title: Optional[str] = None,
                                     description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
                """Update an existing task for the user. Use this when the user wants to update a task."""
                try:
                    # Update task using service
                    updated_task = update_task_by_id(db_session, task_id, user_id, title, description, completed)

                    if updated_task:
                        return {
                            "success": True,
                            "task_id": updated_task.id,
                            "title": updated_task.title,
                            "description": updated_task.description,
                            "completed": updated_task.completed,
                            "message": f"Task '{updated_task.title}' has been updated successfully."
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Task not found or access denied",
                            "message": "Task not found or access denied"
                        }
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "message": f"Failed to update task: {str(e)}"
                    }

            @function_tool
            def delete_task_tool_local(task_id: int) -> Dict[str, Any]:
                """Delete a task for the user. Use this when the user wants to delete a task."""
                try:
                    # Delete task using service
                    deleted = delete_task_by_id(db_session, task_id, user_id)

                    if deleted:
                        return {
                            "success": True,
                            "task_id": task_id,
                            "message": "Task has been deleted successfully."
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Task not found or access denied",
                            "message": "Task not found or access denied"
                        }
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "message": f"Failed to delete task: {str(e)}"
                    }

            # Create a new agent instance with the contextualized tools
            agent_with_tools = Agent(
                name="Todo Assistant",
                instructions=(
                    "You are a helpful assistant for managing todo tasks. "
                    "Help users add, update, and manage their tasks using natural language. "
                    "Be concise but friendly in your responses. Always confirm important actions. "
                    "Use the available tools to interact with the todo system. "
                    "When a user wants to add a task, use the create_task_tool. "
                    "When a user wants to see their tasks, use the get_tasks_tool. "
                    "When a user wants to update a task, use the update_task_tool. "
                    "When a user wants to delete a task, use the delete_task_tool."
                ),
                model=model,
                tools=[create_task_tool_local, get_tasks_tool_local, update_task_tool_local, delete_task_tool_local]
            )

            # Run the agent with the bound functions
            result = Runner.run_sync(
                agent_with_tools,
                user_message
            )

            ai_response = result.final_output

            # Calculate response time
            end_time = time.time()
            response_time = end_time - start_time

            # Save both user and AI messages to database
            user_msg = Message(
                conversation_id=conversation_id,
                role="user",
                content=user_message
            )
            ai_msg = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=ai_response
            )

            db_session.add(user_msg)
            db_session.add(ai_msg)
            db_session.commit()

            # Update conversation timestamp
            conversation.updated_at = datetime.now()
            db_session.add(conversation)
            db_session.commit()

            # Log the chat interaction
            log_chat_interaction(user_id, conversation_id, user_message, ai_response)

            # Log the performance metric
            performance_monitor.log_ai_response_time(user_id, conversation_id, response_time)

            return {
                "response": ai_response,
                "conversation_id": conversation_id,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error calling OpenAI Agents SDK with OpenRouter: {e}")

            # Log the error
            log_error(f"Error calling OpenAI Agents SDK with OpenRouter: {str(e)}", user_id, conversation_id)

            # Still save the user message even if AI fails
            user_msg = Message(
                conversation_id=conversation_id,
                role="user",
                content=user_message
            )
            db_session.add(user_msg)
            db_session.commit()

            # Check if the error is related to timeouts or API issues
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ['timeout', 'connection', 'api', 'rate limit']):
                if 'timeout' in error_str:
                    error_response = "I'm taking longer than expected to respond. Please try again in a moment."
                elif 'rate limit' in error_str:
                    error_response = "I've reached my usage limit. Please try again later."
                elif 'connection' in error_str:
                    error_response = "I'm having trouble connecting. Please try again in a moment."
                else:
                    error_response = "I'm experiencing issues connecting to the AI service. Please try again."
            else:
                error_response = "Sorry, I'm having trouble processing your request right now. Please try again."

            # Save error response to database
            error_msg = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=error_response
            )
            db_session.add(error_msg)
            db_session.commit()

            return {
                "response": error_response,
                "conversation_id": conversation_id,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }


# Global instance
ai_agent_service = AIAgentService()