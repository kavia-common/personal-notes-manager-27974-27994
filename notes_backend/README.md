# Notes Backend

- Framework: FastAPI
- Port: 3001 (recommended for local dev)
- CORS: Allows http://localhost:3000
- DB: SQLite (DATABASE_URL defaults to sqlite:///./notes.db)

Run locally:
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

Environment:
- DATABASE_URL=sqlite:///./notes.db

OpenAPI:
- python scripts/generate_openapi.py --base-url http://localhost:3001 --out interfaces/openapi.json
- or: python -m src.api.generate_openAPI
