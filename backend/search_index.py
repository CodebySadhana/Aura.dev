import json
import re
from pathlib import Path


class SearchIndex:
    def __init__(self, root: str = "backend/data/search-index"):
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)

    def ingest(self, index: str, filename: str, content: bytes) -> dict:
        text = content.decode("utf-8", errors="replace")
        path = self.root / f"{index}.jsonl"
        with path.open("a", encoding="utf-8") as out:
            out.write(json.dumps({"file": filename, "text": text[:200_000]}) + "\n")
        return {"file": filename, "characters": len(text)}

    def search(self, query: str, index: str = "default", limit: int = 3) -> list[dict]:
        path = self.root / f"{index}.jsonl"
        if not path.exists(): return []
        terms = set(re.findall(r"\w+", query.lower()))
        docs = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        ranked = sorted(docs, key=lambda d: sum(t in d["text"].lower() for t in terms), reverse=True)
        return [{"file": d["file"], "excerpt": d["text"][:800]} for d in ranked[:limit] if d]
