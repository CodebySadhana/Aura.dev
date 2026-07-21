import json
from pathlib import Path
from typing import Any


class JsonStore:
    """Zero-infra persistence. Atomic replace prevents partial conversation files."""
    def __init__(self, root: str = "backend/data/conversations"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.teams = self.root.parent / "teams.json"

    def _path(self, user_id: str, session_id: str) -> Path:
        return self.root / user_id / f"{session_id}.json"

    def save_conversation(self, value: dict[str, Any]) -> None:
        path = self._path(value["user_id"], value["session_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(value, default=str), encoding="utf-8")
        temp.replace(path)

    def get_conversation(self, user_id: str, session_id: str) -> dict[str, Any] | None:
        path = self._path(user_id, session_id)
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def list_conversations(self, user_id: str, page: int, page_size: int) -> list[dict[str, Any]]:
        folder = self.root / user_id
        items = [json.loads(p.read_text(encoding="utf-8")) for p in folder.glob("*.json")] if folder.exists() else []
        items.sort(key=lambda x: x.get("start_time", ""), reverse=True)
        return items[(page - 1) * page_size: page * page_size]

    def delete_conversation(self, user_id: str, session_id: str) -> bool:
        path = self._path(user_id, session_id)
        if path.exists():
            path.unlink()
            return True
        return False

    def list_teams(self) -> list[dict[str, Any]]:
        return json.loads(self.teams.read_text()) if self.teams.exists() else []

    def save_teams(self, teams: list[dict[str, Any]]) -> None:
        self.teams.write_text(json.dumps(teams, indent=2), encoding="utf-8")
