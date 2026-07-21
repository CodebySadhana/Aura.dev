import asyncio
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from fastapi import Depends, FastAPI, File, HTTPException, Path as ApiPath, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .database import get_store
from .mcp_tools import router as mcp_router
from .orchestrator import AGENTS, CancellationToken, run_task
from .schemas import ChatMessageCreate, StopRequest, Team, TeamCreate
from .search_index import SearchIndex

app = FastAPI(title="Aura.dev")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("AURA_CORS_ORIGINS", "http://localhost:5173").split(","), allow_methods=["*"], allow_headers=["Authorization", "Content-Type"])
app.include_router(mcp_router)
security = HTTPBearer(auto_error=False)
store = get_store()
queues: dict[str, asyncio.Queue] = {}
tokens: dict[str, CancellationToken] = {}

def validate_token(creds: HTTPAuthorizationCredentials | None = Depends(security)):
    expected = os.getenv("AURA_API_TOKEN")
    if expected and (not creds or creds.credentials != expected): raise HTTPException(401, "Invalid bearer token")
    # Dev-only when AURA_API_TOKEN is unset. Set it in every deployed environment.
    return creds.credentials if creds else "local-dev"

async def launch(session_id: str, body: ChatMessageCreate):
    token, queue = tokens[session_id], queues[session_id]
    item = {"session_id": session_id, "user_id": body.user_id, "content": body.content, "agents": body.agents, "start_time": datetime.now(timezone.utc).isoformat(), "messages": []}
    async for message in run_task(session_id, body.user_id, body.content, body.agents, token):
        data = message.model_dump(mode="json"); item["messages"].append(data); store.save_conversation(item); await queue.put(data)
    await queue.put(None)

@app.post("/api/v1/chat/start")
async def start(body: ChatMessageCreate, _: str = Depends(validate_token)):
    session_id = str(uuid.uuid4()); tokens[session_id] = CancellationToken(); queues[session_id] = asyncio.Queue()
    asyncio.create_task(launch(session_id, body))
    return {"session_id": session_id, "start_time": datetime.now(timezone.utc), "agents": body.agents or ["CEO", "CTO", "Coder", "Executor", "QA Reviewer"]}

@app.get("/api/v1/agents")
async def agents(_: str = Depends(validate_token)):
    return {"orchestrator": "CEO", "departments": {"engineering": ["CTO", "Coder", "Executor"], "research": ["Research Lead", "WebSurfer", "FileSurfer", "RAG Agent"], "product": ["Product Lead", "Coder", "RAG Agent"], "security": ["Security Lead", "FileSurfer", "QA Reviewer"]}}

@app.get("/api/v1/chat/stream")
async def stream(session_id: str, _: str = Depends(validate_token)):
    if session_id not in queues: raise HTTPException(404, "Session not found or no longer active")
    async def events():
        while (message := await queues[session_id].get()) is not None:
            yield f"data: {json.dumps(message)}\n\n"
    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.post("/api/v1/chat/stop")
async def stop(body: StopRequest, _: str = Depends(validate_token)):
    token = tokens.get(body.session_id)
    if not token: raise HTTPException(404, "Session not found")
    token.cancel(); return {"status": "cancellation requested", "session_id": body.session_id}

@app.get("/api/v1/conversations")
async def conversations(user_id: str = Query(pattern=r"^[A-Za-z0-9_-]+$"), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), _: str = Depends(validate_token)):
    return store.list_conversations(user_id, page, page_size)

@app.get("/api/v1/conversations/{user_id}/{session_id}")
async def conversation(user_id: str = ApiPath(pattern=r"^[A-Za-z0-9_-]+$"), session_id: str = ApiPath(pattern=r"^[A-Za-z0-9-]+$"), _: str = Depends(validate_token)):
    value = store.get_conversation(user_id, session_id)
    if not value: raise HTTPException(404, "Conversation not found")
    return value

@app.delete("/api/v1/conversations/{user_id}/{session_id}")
async def delete_conversation(user_id: str = ApiPath(pattern=r"^[A-Za-z0-9_-]+$"), session_id: str = ApiPath(pattern=r"^[A-Za-z0-9-]+$"), _: str = Depends(validate_token)):
    if not store.delete_conversation(user_id, session_id): raise HTTPException(404, "Conversation not found")
    return {"deleted": True}

@app.get("/api/v1/teams", response_model=list[Team])
async def list_teams(_: str = Depends(validate_token)): return store.list_teams()
@app.get("/api/v1/teams/{team_id}", response_model=Team)
async def get_team(team_id: str, _: str = Depends(validate_token)):
    team = next((t for t in store.list_teams() if t["id"] == team_id), None)
    if not team: raise HTTPException(404, "Team not found")
    return team
@app.post("/api/v1/teams", response_model=Team)
async def create_team(body: TeamCreate, _: str = Depends(validate_token)):
    team = Team(id=str(uuid.uuid4()), **body.model_dump()); teams = store.list_teams(); teams.append(team.model_dump()); store.save_teams(teams); return team
@app.put("/api/v1/teams/{team_id}", response_model=Team)
async def update_team(team_id: str, body: TeamCreate, _: str = Depends(validate_token)):
    teams = store.list_teams()
    for i, current in enumerate(teams):
        if current["id"] == team_id: teams[i] = Team(id=team_id, **body.model_dump()).model_dump(); store.save_teams(teams); return teams[i]
    raise HTTPException(404, "Team not found")
@app.delete("/api/v1/teams/{team_id}")
async def delete_team(team_id: str, _: str = Depends(validate_token)):
    teams = [t for t in store.list_teams() if t["id"] != team_id]
    store.save_teams(teams); return {"deleted": True}
@app.post("/api/v1/teams/initialize")
async def initialize_teams(_: str = Depends(validate_token)):
    templates = Path("backend/data/teams-definitions"); teams = [json.loads(p.read_text()) for p in templates.glob("*.json")]; store.save_teams(teams); return {"initialized": len(teams)}

@app.post("/api/v1/upload")
async def upload(indexName: str, files: list[UploadFile] = File(...), _: str = Depends(validate_token)):
    if len(files) > 10: raise HTTPException(400, "Maximum 10 files")
    accepted = {"text/plain", "text/markdown", "application/json"}; index = SearchIndex(); results = []
    for file in files:
        if file.content_type not in accepted: raise HTTPException(415, f"Unsupported type: {file.content_type}")
        data = await file.read()
        if len(data) > 2_000_000: raise HTTPException(413, "File exceeds 2 MB")
        results.append(index.ingest(indexName, file.filename or "upload.txt", data))
    return {"indexName": indexName, "files": results}
