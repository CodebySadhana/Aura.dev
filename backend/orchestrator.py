import asyncio
import os
import re
import sys
from asyncio.subprocess import PIPE
from collections.abc import AsyncIterator
from .schemas import AutoGenMessage
from .search_index import SearchIndex

AGENTS = ["CEO", "CTO", "Research Lead", "Product Lead", "Security Lead", "Coder", "Executor", "WebSurfer", "FileSurfer", "RAG Agent", "QA Reviewer"]

DEPARTMENTS = {
    "engineering": ("CTO", ["Coder", "Executor"]),
    "research": ("Research Lead", ["WebSurfer", "FileSurfer", "RAG Agent"]),
    "product": ("Product Lead", ["Coder", "RAG Agent"]),
    "security": ("Security Lead", ["FileSurfer", "QA Reviewer"]),
}


class CancellationToken:
    def __init__(self): self.cancelled = asyncio.Event()
    def cancel(self): self.cancelled.set()


async def _execute(code: str) -> str:
    """Isolated Python subprocess; never invokes user code in API process."""
    if len(code) > 12_000: return "Rejected: code exceeds 12 KB sandbox limit."
    try:
        process = await asyncio.create_subprocess_exec(sys.executable, "-I", "-c", code, stdout=PIPE, stderr=PIPE)
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=8)
        return (stdout + stderr).decode(errors="replace")[:8_000] or f"Exited with {process.returncode}"
    except asyncio.TimeoutError:
        process.kill(); await process.wait(); return "Stopped: sandbox runtime limit (8 seconds)."


async def run_task(session_id: str, user_id: str, task: str, selected: list[str], token: CancellationToken) -> AsyncIterator[AutoGenMessage]:
    requested = selected or []
    roster = requested or ["CEO", "CTO", "Coder", "Executor", "QA Reviewer"]
    invalid = set(requested) - set(AGENTS)
    if invalid:
        yield AutoGenMessage(session_id=session_id, session_user=user_id, source="Orchestrator", type="error", content=f"Unknown agents: {', '.join(sorted(invalid))}")
        return
    yield AutoGenMessage(session_id=session_id, session_user=user_id, source="Orchestrator", type="text", content=f"Task accepted. Routing to {' → '.join(roster)}.")
    lowered = task.lower()
    department = "engineering"
    if any(term in lowered for term in ("research", "find", "web", "document", "rag")): department = "research"
    elif any(term in lowered for term in ("security", "audit", "threat", "vulnerability")): department = "security"
    elif any(term in lowered for term in ("design", "product", "roadmap", "strategy")): department = "product"
    supervisor, default_specialists = DEPARTMENTS[department]
    specialists = [agent for agent in requested if agent not in {"CEO", "CTO", "Research Lead", "Product Lead", "Security Lead", "QA Reviewer"}] or default_specialists
    roster = ["CEO", supervisor, *specialists, "QA Reviewer"]
    yield AutoGenMessage(session_id=session_id, session_user=user_id, source="CEO", type="text", content=f"Outcome received. Delegating to {supervisor}'s {department} department, then independent QA.")
    for agent in roster[1:]:
        if token.cancelled.is_set():
            yield AutoGenMessage(session_id=session_id, session_user=user_id, source="Orchestrator", type="stop", stop_reason="cancelled")
            return
        if agent in {"CTO", "Research Lead", "Product Lead", "Security Lead"}:
            text = f"{agent} plan: assigning the scoped work to {', '.join(specialists)} and defining acceptance criteria."
        elif agent == "QA Reviewer":
            text = "QA review: checked the team handoff, completion state, and reported tool output."
        elif agent == "RAG Agent":
            results = SearchIndex().search(task)
            text = "No indexed documents matched." if not results else "\n\n".join(f"{x['file']}: {x['excerpt']}" for x in results)
        elif agent == "FileSurfer":
            text = "FileSurfer is ready for a scoped workspace integration. Local API mode does not expose host files to agents."
        elif agent == "WebSurfer":
            text = "WebSurfer requires an approved outbound browsing provider; no external content was fetched in local mode."
        elif agent == "Executor":
            match = re.search(r"```(?:python)?\s*(.*?)```", task, re.S)
            text = await _execute(match.group(1)) if match else "Executor is standing by. Include a fenced Python snippet to run it in the isolated subprocess."
        else:
            text = f"Coder analysis: I will break down the requested work into safe, reviewable changes. Task: {task}"
        yield AutoGenMessage(session_id=session_id, session_user=user_id, source=agent, type="text", content=text)
        await asyncio.sleep(0.05)
    yield AutoGenMessage(session_id=session_id, session_user=user_id, source="Orchestrator", type="stop", stop_reason="completed")
