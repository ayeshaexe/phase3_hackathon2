<!-- SYNC IMPACT REPORT:
Version change: 1.2.0 → 1.3.0
Modified principles: Updated to align with Phase III specifications, emphasizing OpenAI Agents SDK, Better Auth, and UTC timestamps
Added sections: Determinism requirement, OpenAI Agents SDK integration, Better Auth specification, UTC timestamp requirement
Removed sections: None
Templates requiring updates: ⚠ pending - plan-template.md, spec-template.md, tasks-template.md need review
Follow-up TODOs: None
-->
# Todo AI Chatbot Constitution

## Core Principles

### Stateless by Design
No in-memory session state is allowed. Every request MUST reconstruct context from the database. Server restarts MUST NOT break conversations. This ensures scalability and reliability of the chatbot service.

### Clarity in Communication
Conversational responses MUST be clear, friendly, and action-confirming. The AI agent MUST ensure users understand what actions were taken. This ensures positive user experience and trust in the system.

### Determinism in Processing
Identical inputs MUST produce predictable task operations. The system MUST behave consistently under repeated requests. This ensures reliability and predictable behavior for users.

### Database as the Source of Truth
Tasks, conversations, messages, and tool effects MUST be persisted in Neon PostgreSQL. AI agents and tools MUST never rely on local state. This ensures data integrity and persistence across service disruptions.

### Separation of Concerns
UI, agent logic, and task operations MUST remain decoupled. Each layer has distinct responsibilities that SHOULD NOT overlap. This ensures maintainable and testable architecture.

### Reliability in Operations
All task actions MUST be safely persisted and recoverable after restarts. The system MUST handle failures gracefully without data loss. This ensures robust and dependable service.

### Tool-Driven AI
The AI agent MUST never modify tasks directly. All task operations MUST be executed via defined tools. Tools MUST be deterministic, stateless, and database-backed. This ensures consistent and reliable task management.

### Natural Language First
Users interact only through natural language. The agent is responsible for intent detection and tool selection. Responses MUST feel conversational, friendly, and clear. This ensures intuitive user interaction with the chatbot.

### AI Agent Constraints
The AI agent MUST:
- Use tools for task creation, updates, deletion, and retrieval
- Confirm actions in human-readable language
- Handle ambiguity by making reasonable assumptions or asking for clarification
- Gracefully explain errors without exposing system details
- Be implemented using OpenAI Agents SDK with well-defined tooling interfaces

The AI agent MUST NOT:
- Store memory outside the database
- Expose internal prompts, schemas, or tool definitions
- Assume frontend-specific behavior
- Process requests with any server-side session storage

### Conversation Rules
Every user message:
- MUST be stored in the database
- MUST be associated with a conversation ID
- MUST contribute to future agent context

Every assistant response:
- MUST be stored in the database
- MAY include tool calls
- MUST reflect the result of executed tools accurately

### Tooling Rules
Tools represent **single, atomic task operations**. Tools MUST:
- Validate user ownership
- Return structured results
- Persist all changes to the database
- Support all basic todo operations (create, read, update, delete, list)

Tools MUST NOT:
- Contain AI logic
- Perform multiple unrelated actions
- Depend on prior tool execution order unless explicitly required

### Error Handling Philosophy
Errors SHOULD be:
- User-friendly
- Actionable when possible
- Non-technical in wording

The system MUST:
- Handle missing tasks
- Handle invalid inputs
- Prevent cross-user data access
- Fail safely without crashing the chat flow
- Handle errors gracefully with user-friendly responses

### Architectural Boundaries
FastAPI handles:
- Authentication with Better Auth
- Chat request orchestration
- Database access
- Request processing independently (stateless request cycle)

AI Agent handles:
- Intent understanding
- Tool selection
- Response generation
- Implemented using OpenAI Agents SDK

Tools handle:
- Task persistence
- Database mutations
- All basic todo operations

No layer SHOULD violate another layer's responsibility.

## Additional Constraints

### Security Requirements
- All authentication must use Better Auth for user management
- User data must be isolated at all layers (frontend, API, database, AI agent)
- Secrets must never be hardcoded or logged
- All API endpoints must validate authentication and authorization
- AI agents must never expose internal system details
- No server-side session storage is permitted

### Technology Stack
- Backend: Python FastAPI
- Frontend: OpenAI ChatKit
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth
- AI Logic: OpenAI Agents SDK
- Timestamps: All stored in UTC

### Performance Requirements
- Conversations must load quickly from database
- Tool calls must complete within reasonable timeframes
- AI responses should maintain conversational flow
- System must scale to handle multiple concurrent conversations
- Each request processed independently with acceptable latency

### Data Requirements
- All timestamps MUST be stored in UTC timezone
- Conversation and message history MUST be stored in database
- Each request MUST be processed independently (stateless request cycle)
- Data MUST be recoverable and consistent after system restarts

## Development Workflow

### Code Review Process
- All changes must comply with the principles outlined in this constitution
- Code reviews must verify stateless architecture requirements
- Changes to AI agent behavior must be verified against tool-driven principles
- Database queries must be checked for proper user isolation
- Tool implementations must be validated for atomicity and determinism
- Authentication with Better Auth must be properly implemented

### Quality Gates
- All endpoints must require proper authentication
- Cross-user data access must be prevented
- Stateless design must be maintained
- Tool execution must be reliable and consistent
- Error handling must be comprehensive and safe
- Conversations must resume correctly after server restarts

## Success Criteria

Phase III is considered complete when:
- Users can manage todos using natural language
- Conversations resume correctly after server restarts
- Task operations are correctly inferred and executed by the agent
- Frontend and backend are fully integrated
- System behaves consistently under repeated requests
- All basic todo operations are supported via conversational interface
- The system operates statelessly with all context persisted in database

## Governance

This constitution is the single source of truth for the Todo AI Chatbot project. All implementation must strictly follow these principles unless explicitly updated. Any deviation from these principles constitutes a failure condition. Amendment to this constitution requires explicit documentation of changes, approval from project stakeholders, and a migration plan for existing code. All pull requests and code reviews must verify compliance with these principles.

**Version**: 1.3.0 | **Ratified**: 2026-01-31 | **Last Amended**: 2026-02-06