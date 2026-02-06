---
id: 3
title: Update Todo AI Chatbot Constitution
stage: constitution
date: 2026-02-06
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 001-frontend-todo-app
user: exe_ayeshhh
command: /sp.constitution
labels: [constitution, todo-ai-chatbot, phase-iii, stateless-architecture]
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

/sp.constitution

Project: Todo AI Chatbot (Phase III)

Objective:
Design and implement an AI-powered chatbot that manages todo tasks via natural language, using a stateless backend architecture with persistent conversation history.

Core principles:
- Statelessness: Backend holds no in-memory session state; all context is persisted in the database
- Clarity: Conversational responses must be clear, friendly, and action-confirming
- Determinism: Identical inputs should produce predictable task operations
- Separation of concerns: UI, agent logic, and task operations must remain decoupled
- Reliability: All task actions must be safely persisted and recoverable after restarts

Key standards:
- Conversational interface supports all basic todo operations
- AI logic implemented using OpenAI Agents SDK
- Task operations exposed via well-defined tooling interfaces
- Conversation and message history stored in database
- Each request processed independently (stateless request cycle)
- Errors handled gracefully with user-friendly responses

Constraints:
- Backend: Python FastAPI
- Frontend: OpenAI ChatKit
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth
- No server-side session storage
- All timestamps stored in UTC

Success criteria:
- Users can manage todos using natural language
- Conversations resume correctly after server restarts
- Task operations are correctly inferred and executed by the agent
- Frontend and backend are fully integrated
- System behaves consistently under repeated requests

## Response snapshot

Updated the project constitution to align with Todo AI Chatbot Phase III requirements, focusing on stateless architecture, OpenAI Agents SDK integration, Better Auth implementation, and UTC timestamp handling. The constitution now includes:

- Enhanced core principles including Clarity in Communication, Determinism in Processing, Separation of Concerns, and Reliability in Operations
- Updated technology stack specifications with specific mentions of Python FastAPI, OpenAI ChatKit, SQLModel, Neon Serverless PostgreSQL, Better Auth, and OpenAI Agents SDK
- Clear constraints on server-side session storage prohibition
- Explicit requirement for UTC timestamp storage
- Detailed success criteria for Phase III completion
- Improved error handling philosophy aligned with user-friendly responses

Version was incremented from 1.2.0 to 1.3.0 to reflect the minor enhancements and additions to the principles.

## Outcome

- ✅ Impact: Updated constitution to reflect Phase III specifications with enhanced principles
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Implement AI agent with OpenAI Agents SDK and defined tools
- 🧠 Reflection: Constitution now comprehensively covers all specified requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Begin implementation of AI agent tools