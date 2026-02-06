# Quickstart Guide: AI Chat Agent & Conversation System

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL database (Neon or local)
- OpenAI API key
- Existing todo app backend running

## Setup Backend

### 1. Install Dependencies

Add the following to your `backend/requirements.txt`:

```txt
openrouter-python==1.0.0
tiktoken==0.5.2
```

Then install:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Variables

Add to your `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Database Models

Create the new models as specified in the data-model.md:

- `backend/models/conversation.py`
- `backend/models/message.py`

### 4. Database Migration

The system will automatically create the necessary tables on startup through the existing `db.py` mechanism.

### 5. Create Services

Create the following service files:

- `backend/services/chat_service.py`
- `backend/services/ai_agent.py`
- `backend/services/conversation_service.py`

### 6. Create API Routes

Create `backend/api/v1/chat.py` with the endpoints defined in the API contract.

Update `backend/main.py` to include the new chat routes.

## Frontend Integration

### 1. Install Dependencies

```bash
cd frontend
npm install @types/react
```

### 2. Create Components

Create the following components:

- `frontend/components/chat/ChatWindow.tsx`
- `frontend/components/chat/MessageBubble.tsx`
- `frontend/components/chat/ChatInput.tsx`
- `frontend/components/chat/ConversationHistory.tsx`

### 3. Create Hooks and Types

- `frontend/hooks/useChat.ts`
- `frontend/types/chat.ts`

### 4. Add Pages

Create `frontend/app/chat/page.tsx` for the chat interface.

## Running the System

### Backend

```bash
cd backend
uvicorn main:app --reload
```

The chat API will be available at:
- POST `/api/{user_id}/chat` - Send messages to the AI
- GET `/api/{user_id}/conversations` - Get user's conversations
- GET `/api/{user_id}/conversations/{id}` - Get specific conversation

### Frontend

```bash
cd frontend
npm run dev
```

The chat interface will be available at `/chat`.

## API Usage Examples

### Sending a Message

```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a new task to buy groceries"
  }'
```

### Starting a New Conversation

```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi, I want to create a new task",
    "conversation_id": null
  }'
```

### Getting Conversation History

```bash
curl -X GET http://localhost:8000/api/user123/conversations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Testing

Unit tests for the new components will be located in:
- `backend/tests/unit/test_conversation.py`
- `backend/tests/unit/test_message.py`
- `backend/tests/unit/test_chat_service.py`

Integration tests will be in:
- `backend/tests/integration/test_chat_api.py`

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**: Verify your API key is correct in environment variables
2. **Authentication Errors**: Ensure JWT tokens are properly formatted and not expired
3. **Database Connection**: Verify PostgreSQL connection settings in the environment
4. **CORS Issues**: Check CORS configuration in main.py matches your frontend origin

### Logging

Check `backend/backend.log` for server-side logs related to chat functionality.