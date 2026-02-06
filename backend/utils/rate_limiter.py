from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)

# Define rate limit for chat endpoints
CHAT_RATE_LIMIT = "100/minute"