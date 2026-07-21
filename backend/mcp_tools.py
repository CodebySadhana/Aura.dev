from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/mcp", tags=["mcp"])

class NotifyRequest(BaseModel):
    message: str

@router.post("/notify")
async def notify(body: NotifyRequest):
    """A small MCP-style HTTP tool endpoint agents can invoke."""
    return {"ok": True, "delivered": body.message}
