"""Run with: python -m backend.test_api (after installing requirements)."""
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
r = client.post("/api/v1/chat/start", json={"user_id":"test", "content":"hello"})
assert r.status_code == 200 and r.json()["agents"] == ["CEO", "CTO", "Coder", "Executor", "QA Reviewer"]
