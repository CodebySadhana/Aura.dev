# Aura.dev

Multi-agent task orchestration with a FastAPI/SSE backend and a React, Tailwind and Motion client.

## Run locally

```powershell
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

In another terminal:

```powershell
cmd /c npm install
cmd /c npm run dev
```

The frontend runs on `http://localhost:5173`, and the API runs on `http://localhost:8000`. Local development uses JSON persistence under `backend/data/conversations`; configure `AURA_API_TOKEN` before exposing the API. See [API_CONTRACT.md](API_CONTRACT.md) for integration details.

## GitHub Pages

Pushing `main` deploys the static frontend through `.github/workflows/deploy-pages.yml`. In the GitHub repository, enable **Settings → Pages → Source: GitHub Actions**, then add a repository variable named `VITE_API_URL` containing the public HTTPS URL of the separately deployed FastAPI backend. GitHub Pages cannot host the Python API or SSE service.

## Render backend

The included `render.yaml` deploys the API from this repository. In Render, create a **New → Blueprint** deployment, select this GitHub repository, and accept the `aura-api` service. Copy its public HTTPS URL into the GitHub repository variable `VITE_API_URL`, then rerun the Pages workflow.
