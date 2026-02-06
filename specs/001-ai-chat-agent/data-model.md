# Data Model: AI Chat Agent & Conversation System

## Entities

### Conversation
Represents a single conversation thread between a user and the AI agent.

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key reference to user, indexed)
- `title`: String (Generated from first message or user-provided, max 200 chars)
- `created_at`: DateTime (UTC timezone, default now)
- `updated_at`: DateTime (UTC timezone, default now, updated on changes)

**Relationships**:
- One-to-many with Message (one conversation has many messages)

**Validation Rules**:
- user_id must exist in users table
- created_at and updated_at must be in UTC
- title must not exceed 200 characters

### Message
Represents an individual message in a conversation, either from user or assistant.

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `conversation_id`: Integer (Foreign Key reference to Conversation, indexed)
- `role`: String (Either "user" or "assistant", constrained)
- `content`: String (The message content, max 5000 chars)
- `timestamp`: DateTime (UTC timezone, default now)
- `metadata`: JSON (Optional, for storing additional data like token usage, model info)

**Relationships**:
- Many-to-one with Conversation (many messages belong to one conversation)

**Validation Rules**:
- conversation_id must exist in conversations table
- role must be either "user" or "assistant"
- timestamp must be in UTC
- content must not exceed 5000 characters
- metadata must be valid JSON if provided

### User (Existing)
Reference to existing user model for authentication and data isolation.

**Fields**:
- `id`: String (Primary Key, from JWT token)
- `email`: String (Unique, validated)
- `created_at`: DateTime (UTC timezone)

**Note**: This model already exists in the system and will be referenced by user_id foreign keys in Conversation model.

## State Transitions

### Conversation
- Created when user initiates first chat
- Updated when new messages are added
- Potentially soft-deleted (marked as inactive) when user deletes conversation

### Message
- Created when user sends message or assistant responds
- Immutable once created (no updates allowed)
- Deleted when parent conversation is deleted

## Relationships and Constraints

1. **Referential Integrity**: Messages must belong to existing conversations
2. **User Isolation**: Users can only access their own conversations and messages
3. **Timestamp Consistency**: All timestamps stored in UTC timezone
4. **Data Size Limits**: Content and metadata fields have size constraints to prevent abuse
5. **Indexing Strategy**: Index on user_id (conversations) and conversation_id (messages) for efficient querying

## Database Schema

```sql
-- conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- indexes for efficient querying
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
```

## Migration Strategy

1. Add conversations table with user_id, title, and timestamps
2. Add messages table with conversation_id, role, content, and timestamp
3. Update existing auth middleware to verify user access to conversations
4. Add database session management for new models