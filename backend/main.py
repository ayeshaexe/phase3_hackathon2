from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import sys
import os
# Add the current directory to the path so we can import from the config and routes folders
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from routes import tasks
from routes import auth
from api.v1 import chat
from db import create_db_and_tables

app = FastAPI(
    title="Todo API",
    description="A secure, production-ready API for managing todo tasks",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://todo-part2.vercel.app","http://localhost:3000"
    ],
    #allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Additional security: expose only necessary headers
    # expose_headers=["Access-Control-Allow-Origin"]
)

# Configure rate limiting middleware
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}