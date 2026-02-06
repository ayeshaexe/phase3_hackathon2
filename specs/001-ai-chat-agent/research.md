# Research: AI Chat Agent & Conversation System

## Overview
Research for implementing a stateless AI-driven chat system that integrates with the existing todo application.

## Decision: OpenRouter Agents SDK Integration
**Rationale**: Need to integrate OpenRouter's agent system to handle natural language processing for todo operations. The OpenRouter Agents API provides advanced reasoning capabilities and tool calling functionality that fits our requirements.
**Alternatives considered**:
- Building custom NLP pipeline with transformers
- Using LangChain agents
- Using Anthropic Claude with tool calling

## Decision: Conversation Storage Model
**Rationale**: Need to store conversation history in the database to maintain statelessness. Using SQLModel with Neon PostgreSQL to maintain consistency with existing data models.
**Alternatives considered**:
- Separate document database for conversations
- File-based storage
- In-memory cache with database backup

## Decision: Authentication Integration
**Rationale**: Leverage existing JWT authentication system to ensure user isolation and security consistency across the application.
**Alternatives considered**:
- Separate authentication for chat endpoints
- Anonymous chat with task association later

## Decision: Frontend Chat Component Architecture
**Rationale**: Build reusable chat components that can integrate with the existing Next.js application structure and follow the same patterns as the current UI.
**Alternatives considered**:
- Separate chat application
- iframe integration
- Direct API calls from existing task page

## Decision: Message Streaming vs. Sync Responses
**Rationale**: Implement synchronous request/response initially to maintain consistency with existing API patterns and simplify error handling. Real-time streaming can be added later if needed.
**Alternatives considered**:
- WebSocket-based streaming
- Server-Sent Events (SSE)
- Long polling

## Decision: AI Agent Prompt Engineering
**Rationale**: Design prompts that specifically instruct the agent to use tools for task operations without performing direct database manipulation. This maintains the architectural boundary between AI and data persistence.
**Alternatives considered**:
- Allowing direct database access from agent
- Hard-coded response patterns
- Template-based responses

## Technical Unknowns Resolved

1. **OpenRouter API Keys**: Will need to add OPENROUTER_API_KEY to environment variables
2. **Rate Limiting**: Need to implement proper error handling for API limits
3. **Token Usage**: Monitor costs and implement limits for conversation length
4. **CORS Configuration**: Ensure frontend can access both task and chat APIs
5. **Database Indexing**: Optimize for conversation history queries