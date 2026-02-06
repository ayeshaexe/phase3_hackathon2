# OpenRouter AI Agent Implementation Guide

## Overview
This guide explains how to implement AI agents using OpenRouter instead of OpenAI. OpenRouter provides access to multiple LLMs through a unified API.

## Installation

Install the required dependencies:

```bash
pip install openrouter-python python-dotenv
```

## Configuration

Set up your environment variables:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Basic Agent Implementation

Here's how to implement a basic agent using OpenRouter:

```python
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenRouter
client = openai.OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def create_basic_agent(system_prompt: str):
    """
    Create a basic agent using OpenRouter

    Args:
        system_prompt: The system instructions for the agent

    Returns:
        A function that can be called to process user messages
    """

    def process_message(user_message: str, conversation_history: list = None):
        """
        Process a user message and return the agent's response

        Args:
            user_message: The user's input message
            conversation_history: List of previous messages for context

        Returns:
            The agent's response message
        """

        # Build the message history
        messages = [{"role": "system", "content": system_prompt}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_message})

        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o",  # Or any other model available on OpenRouter
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return "Sorry, I'm having trouble processing your request right now."

    return process_message

# Example usage
if __name__ == "__main__":
    agent = create_basic_agent(
        "You are a helpful assistant for managing todo tasks. "
        "Help users add, update, and manage their tasks using natural language."
    )

    response = agent("Add a new task: Buy groceries")
    print(response)
```

## Agent with Function Tools

Here's how to implement an agent that can call functions/tools:

```python
import json
from typing import Dict, Any

def create_agent_with_tools(system_prompt: str, available_tools: Dict[str, callable]):
    """
    Create an agent that can use tools/functions

    Args:
        system_prompt: The system instructions for the agent
        available_tools: Dictionary mapping tool names to functions

    Returns:
        A function that can be called to process user messages
    """

    def process_message(user_message: str, conversation_history: list = None):
        """
        Process a user message, potentially calling tools

        Args:
            user_message: The user's input message
            conversation_history: List of previous messages for context

        Returns:
            The agent's response message
        """

        messages = [{"role": "system", "content": system_prompt}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_message})

        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o",
                messages=messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": func.__doc__ or f"Function {name}",
                        "parameters": {
                            "type": "object",
                            "properties": {},  # Define based on function signature
                            "required": []     # Define based on function signature
                        }
                    }
                } for name in available_tools.keys()],
                tool_choice="auto"
            )

            # Process the response
            choice = response.choices[0]

            if choice.finish_reason == "tool_calls":
                # Process tool calls
                tool_responses = []

                for tool_call in choice.message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name in available_tools:
                        try:
                            result = available_tools[function_name](**function_args)
                            tool_responses.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps(result)
                            })
                        except Exception as e:
                            tool_responses.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": f"Error: {str(e)}"
                            })

                # Add tool responses to messages and get final response
                messages.append(choice.message)
                messages.extend(tool_responses)

                final_response = client.chat.completions.create(
                    model="openai/gpt-4o",
                    messages=messages,
                    temperature=0.7
                )

                return final_response.choices[0].message.content
            else:
                # No tool calls, return the message content directly
                return choice.message.content

        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return "Sorry, I'm having trouble processing your request right now."

    return process_message

# Example with tools
def add_todo_task(title: str, description: str = None) -> Dict[str, Any]:
    """Add a new todo task to the database"""
    # Implementation would interact with your database
    return {
        "success": True,
        "task_id": 123,
        "message": f"Task '{title}' has been added successfully"
    }

def get_todo_tasks() -> Dict[str, Any]:
    """Get all todo tasks for the current user"""
    # Implementation would fetch from your database
    return {
        "tasks": [
            {"id": 1, "title": "Buy groceries", "completed": False},
            {"id": 2, "title": "Walk the dog", "completed": True}
        ]
    }

# Create an agent with tools
if __name__ == "__main__":
    tools = {
        "add_todo_task": add_todo_task,
        "get_todo_tasks": get_todo_tasks
    }

    agent = create_agent_with_tools(
        "You are a helpful assistant for managing todo tasks. "
        "Use the available tools to add, update, and manage tasks. "
        "Always confirm actions with the user before making changes.",
        tools
    )

    response = agent("Add a new task: Buy groceries")
    print(response)
```

## Session Management for Conversation History

To maintain conversation context (stateless but with database persistence):

```python
from typing import List, Dict
from datetime import datetime

class ConversationService:
    """
    Service to manage conversation history in the database
    """

    def __init__(self, db_session):
        self.db_session = db_session

    def get_conversation_history(self, conversation_id: int) -> List[Dict]:
        """
        Retrieve conversation history from database
        """
        # This would query your Conversation and Message models
        # Return in the format expected by the OpenRouter API
        pass

    def save_message(self, conversation_id: int, role: str, content: str):
        """
        Save a message to the database
        """
        # This would create a new Message record
        pass

def create_stateless_agent(conversation_service: ConversationService, system_prompt: str):
    """
    Create an agent that loads context from database for each request
    """

    def process_message(user_message: str, user_id: str, conversation_id: int = None):
        # If no conversation ID provided, create a new one
        if conversation_id is None:
            # Create new conversation in database
            # Implementation would create a new Conversation record
            pass

        # Load conversation history from database
        history = conversation_service.get_conversation_history(conversation_id)

        # Process the message with context
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o",
                messages=messages,
                temperature=0.7
            )

            assistant_response = response.choices[0].message.content

            # Save both user and assistant messages to database
            conversation_service.save_message(conversation_id, "user", user_message)
            conversation_service.save_message(conversation_id, "assistant", assistant_response)

            return {
                "response": assistant_response,
                "conversation_id": conversation_id
            }

        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return {
                "response": "Sorry, I'm having trouble processing your request right now.",
                "conversation_id": conversation_id
            }

    return process_message
```

## Error Handling and Best Practices

```python
import time
import logging
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """
    Decorator to retry API calls on failure
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:  # Last attempt
                        logging.error(f"API call failed after {max_retries} attempts: {e}")
                        raise
                    logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=1)
def call_openrouter_api(messages, model="openai/gpt-4o", **kwargs):
    """
    Call OpenRouter API with retry logic
    """
    return client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )
```

## Model Selection

OpenRouter supports many different models. You can specify different models based on your needs:

```python
# Fast, cheap models for simple tasks
FAST_MODEL = "google/gemini-flash"
# Powerful models for complex reasoning
POWERFUL_MODEL = "openai/gpt-4o"
# Open-source alternatives
OPEN_SOURCE_MODEL = "mistralai/mistral-7b-instruct"

def select_model_for_task(task_complexity: str) -> str:
    """
    Select the appropriate model based on task complexity
    """
    model_mapping = {
        "simple": FAST_MODEL,
        "complex": POWERFUL_MODEL,
        "custom": OPEN_SOURCE_MODEL
    }

    return model_mapping.get(task_complexity, FAST_MODEL)
```

This implementation maintains the stateless architecture requirement by loading conversation history from the database for each request and saving responses back to the database, while leveraging OpenRouter's API for AI processing.