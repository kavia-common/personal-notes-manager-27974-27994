# personal-notes-manager-27974-27994

Backend (FastAPI) runs on port 3001 by default and exposes CRUD endpoints for notes.
Frontend (React) should call the backend at http://localhost:3001 (configurable via REACT_APP_API_BASE_URL).

Quick start:
- Backend:
  uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
- Frontend:
  Set REACT_APP_API_BASE_URL=http://localhost:3001 (or use .env) and start the dev server.

CORS: Configured to allow http://localhost:3000.
DB: SQLite file (notes.db) is created automatically on startup via init_db().

OpenAPI:
- To regenerate from a running backend:
  python scripts/generate_openapi.py --base-url http://localhost:3001 --out interfaces/openapi.json
- Or generate from the app:
  python -m src.api.generate_openapi
