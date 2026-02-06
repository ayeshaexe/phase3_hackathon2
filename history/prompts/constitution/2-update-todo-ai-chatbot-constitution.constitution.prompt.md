---
id: 2
title: Update Todo AI Chatbot Constitution
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-frontend-todo-app
user: NBK COMPUTER
command: sp.constitution
labels: [constitution, ai-chatbot, stateless-architecture]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
# sp.constitution — Phase III: Todo AI Chatbot

## Project Identity

This project is a **Todo application enhanced with an AI-powered chatbot** that allows
users to manage tasks using natural language. The chatbot must operate in a **stateless
server architecture**, persisting all state in a PostgreSQL database.

Phase III focuses on **AI agent behavior, conversation persistence, and tool-based task
management**, not UI polish.

---

## Core Principles

1. **Stateless by Design**
   - No in-memory session state is allowed.
   - Every request must reconstruct context from the database.
   - Server restarts must not break conversations.

2. **Database as the Source of Truth**
   - Tasks, conversations, messages, and tool effects are persisted in Neon PostgreSQL.
   - AI agents and tools never rely on local state.

3. **Tool-Driven AI**
   - The AI agent must never modify tasks directly.
   - All task operations are executed via defined tools.
   - Tools are deterministic, stateless, and database-backed.

4. **Natural Language First**
   - Users interact only through natural language.
   - The agent is responsible for intent detection and tool selection.
   - Responses must feel conversational, friendly, and clear.

---

## AI Agent Constraints

- The AI agent must:
  - Use tools for task creation, updates, deletion, and retrieval
  - Confirm actions in human-readable language
  - Handle ambiguity by making reasonable assumptions or asking for clarification
  - Gracefully explain errors without exposing system details

- The AI agent must NOT:
  - Store memory outside the database
  - Expose internal prompts, schemas, or tool definitions
  - Assume frontend-specific behavior

---

## Conversation Rules

- Every user message:
  - Is stored in the database
  - Is associated with a conversation ID
  - Contributes to future agent context

- Every assistant response:
  - Is stored in the database
  - May include tool calls
  - Must reflect the result of executed tools accurately

---

## Tooling Rules

- Tools represent **single, atomic task operations**
- Tools must:
  - Validate user ownership
  - Return structured results
  - Persist all changes to the database
- Tools must NOT:
  - Contain AI logic
  - Perform multiple unrelated actions
  - Depend on prior tool execution order unless explicitly required

---

## Error Handling Philosophy

- Errors should be:
  - User-friendly
  - Actionable when possible
  - Non-technical in wording

- The system must:
  - Handle missing tasks
  - Handle invalid inputs
  - Prevent cross-user data access
  - Fail safely without crashing the chat flow

---

## Architectural Boundaries

- FastAPI handles:
  - Authentication
  - Chat request orchestration
  - Database access
- AI Agent handles:
  - Intent understanding
  - Tool selection
  - Response generation
- Tools handle:
  - Task persistence
  - Database mutations
- No layer should violate another layer's responsibility.

---

## Success Criteria

Phase III is considered complete when:

- Users can manage tasks fully through chat
- Conversations persist across requests and restarts
- The AI agent reliably chooses correct tools
- All task changes are reflected accurately in the database
- The system remains stateless and scalable

---

## Out of Scope

- UI styling and frontend polish
- Analytics and logging dashboards
- Real-time streaming responses
- Multi-agent collaboration

---

## Guiding Philosophy

**If a human can say it naturally, the agent should understand it.
If the agent changes data, it must be through tools.
If state exists, it must live in the database.**
```

## Response snapshot

Updated the project constitution to reflect the Todo AI Chatbot requirements with stateless architecture focus. The new constitution includes principles for:
- Stateless by Design: No in-memory session state allowed
- Database as the Source of Truth: All persistence in Neon PostgreSQL
- Tool-Driven AI: AI agent must use tools for all task operations
- Natural Language First: Intuitive user interaction
- AI Agent Constraints: Clear boundaries for agent behavior
- Conversation Rules: Proper message and response handling
- Tooling Rules: Atomic and deterministic operations
- Error Handling Philosophy: User-friendly error responses
- Architectural Boundaries: Clear separation of concerns

Version updated from 1.1.0 to 1.2.0 with the new principles and guidelines.

## Outcome

- ✅ Impact: Major update to project constitution reflecting shift to AI chatbot architecture
- 🧪 Tests: none
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Implementation of AI agent and tool integration
- 🧠 Reflection: Constitution now properly reflects the stateless, tool-driven architecture requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing AI agent with defined tools