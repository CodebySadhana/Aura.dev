# Aura.dev client contract

All API routes require a bearer token when `AURA_API_TOKEN` is configured; local dev accepts any/missing token and must not be deployed that way.

Start a task with `POST /api/v1/chat/start` and JSON `{ "user_id": "...", "content": "...", "agents": ["Coder"] }`. The immediate result contains `session_id`. Open `GET /api/v1/chat/stream?session_id=...` as SSE and parse each `data:` value as `AutoGenMessage`; a message with `stop_reason` ends the run. Alternatively poll `GET /api/v1/conversations/{user_id}/{session_id}`.

Python, JavaScript, and generic HTTP clients should retry 5xx/timeouts a small bounded number of times. A dropped SSE stream is resumable by reopening it using the same session ID; fetch the conversation endpoint after completion for the authoritative persisted history.
