from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class AutoGenMessage(BaseModel):
    time: datetime = Field(default_factory=datetime.utcnow)
    session_id: str
    session_user: str
    source: str
    type: Literal["text", "image", "tool_call", "error", "stop"]
    content: str | None = None
    content_image: str | None = None
    stop_reason: str | None = None


class ChatMessageCreate(BaseModel):
    user_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    content: str = Field(min_length=1, max_length=20_000)
    agents: list[str] = []
    run_mode_locally: bool = False


class StopRequest(BaseModel):
    session_id: str = Field(pattern=r"^[A-Za-z0-9-]+$")
    user_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")


class Team(BaseModel):
    id: str
    name: str = Field(min_length=1, max_length=120)
    agents: list[str]
    description: str = ""


class TeamCreate(BaseModel):
    name: str
    agents: list[str]
    description: str = ""
