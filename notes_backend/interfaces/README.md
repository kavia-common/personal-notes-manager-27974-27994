# Interfaces

This folder contains the generated OpenAPI specification for the Notes backend.

- openapi.json: Generated OpenAPI schema for the FastAPI application, including the /notes CRUD endpoints and health check.

Regeneration
- Ensure the backend app exposes the OpenAPI at /openapi.json (FastAPI default).
- Option 1: Run the backend locally (uvicorn on http://localhost:3001) and then:
  python scripts/generate_openapi.py --base-url http://localhost:3001 --out interfaces/openapi.json
- Option 2: Run the in-app generator:
  python -m src.api.generate_openapi
  (writes to interfaces/openapi.json)

CORS
- The backend enables CORSMiddleware to allow the frontend origin explicitly:
  http://localhost:3000
- Example (FastAPI):
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

Database initialization
- Database tables are created on startup so the app is ready to serve requests without manual migrations in this demo.
- Implemented via FastAPI startup event calling init_db().
