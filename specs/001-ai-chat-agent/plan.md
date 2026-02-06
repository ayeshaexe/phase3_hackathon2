# Implementation Plan: AI Chat Agent & Conversation System

**Branch**: `001-ai-chat-agent` | **Date**: 2026-02-06 | **Spec**: [link]
**Input**: Feature specification from `/specs/001-ai-chat-agent/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless AI-driven chat system that integrates with the existing todo application. The system will use FastAPI to handle chat requests, store conversation data in Neon PostgreSQL using SQLModel, and integrate with OpenAI Agents SDK for natural language processing and intent detection. The system will be completely stateless, reconstructing conversation context from the database on each request, and will connect to the frontend UI for seamless chat experience.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenRouter Agents SDK, SQLModel, Better Auth (existing auth system)
**Storage**: Neon Serverless PostgreSQL (existing db infrastructure)
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: web
**Performance Goals**: <200ms p95 response time, 10 concurrent conversations
**Constraints**: <5 seconds response time for AI processing, stateless operation, user data isolation, integrate with existing auth system
**Scale/Scope**: Single-user conversations, persistent history per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Stateless by Design: System will reconstruct context from database on each request, no in-memory session state
- ✅ Database as the Source of Truth: All conversations and messages stored in Neon PostgreSQL
- ✅ Tool-Driven AI: AI agent will use tools for task operations (though actual tools are in Spec 4, the architecture will support this)
- ✅ Natural Language First: Users interact through natural language
- ✅ AI Agent Constraints: Will implement using OpenAI Agents SDK, store no memory outside database
- ✅ Conversation Rules: All user and assistant messages stored in database
- ✅ Error Handling Philosophy: System will return user-friendly error messages
- ✅ Architectural Boundaries: FastAPI handles auth/orchestration, AI agent handles intent/response
- ✅ Security Requirements: Using existing Better Auth/JWT authentication system for consistency
- ✅ Technology Stack: Using Python FastAPI (existing), SQLModel (existing), Neon PostgreSQL (existing), OpenRouter Agents SDK (new)
- ✅ Data Requirements: Storing timestamps in UTC, processing requests independently

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chat-agent/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (integrated with existing structure)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py      # New: Conversation entity
│   │   ├── message.py          # New: Message entity
│   │   └── __init__.py         # Update: Export new models
│   ├── services/
│   │   ├── chat_service.py     # New: Core chat logic
│   │   ├── ai_agent.py         # New: AI agent integration
│   │   ├── conversation_service.py  # New: Conversation management
│   │   └── task_service.py     # Existing: May be referenced for tool integration
│   ├── api/
│   │   └── v1/
│   │       ├── chat.py         # New: Chat API endpoints
│   │       └── __init__.py     # Update: Include chat routes
│   └── main.py                 # Update: Include chat routes
├── requirements.txt            # Update: Add OpenAI SDK
└── tests/
    ├── unit/
    │   ├── test_conversation.py
    │   ├── test_message.py
    │   └── test_chat_service.py
    └── integration/
        └── test_chat_api.py
```

```text
frontend/
├── components/
│   ├── chat/
│   │   ├── ChatWindow.tsx      # New: Main chat UI component
│   │   ├── MessageBubble.tsx   # New: Individual message display
│   │   ├── ChatInput.tsx       # New: Input field with send button
│   │   └── ConversationHistory.tsx  # New: Conversation listing
│   └── ui/
│       └── [existing components]
├── app/
│   ├── chat/                   # New: Chat page route
│   │   └── page.tsx
│   └── tasks/
│       └── page.tsx            # Update: Add chat navigation/link
├── hooks/
│   └── useChat.ts              # New: Chat state management
├── types/
│   └── chat.ts                 # New: Chat-related TypeScript interfaces
└── lib/
    └── api.ts                  # Update: Add chat API functions
```

**Structure Decision**: Integrating with existing project structure, extending the current backend API and adding new frontend components. Following the constraint that no direct task CRUD logic is included in this spec (will be in Spec 4).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

None required - all constitution requirements satisfied.