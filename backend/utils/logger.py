import logging
from datetime import datetime
import json

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat_interactions.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_chat_interaction(user_id: str, conversation_id: int, user_message: str, ai_response: str):
    """
    Log chat interactions for monitoring and debugging
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "conversation_id": conversation_id,
        "user_message": user_message,
        "ai_response": ai_response,
        "interaction_type": "chat"
    }

    logger.info(json.dumps(log_entry))

def log_error(error_message: str, user_id: str = None, conversation_id: int = None):
    """
    Log errors with context
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "conversation_id": conversation_id,
        "error_message": error_message,
        "interaction_type": "error"
    }

    logger.error(json.dumps(log_entry))