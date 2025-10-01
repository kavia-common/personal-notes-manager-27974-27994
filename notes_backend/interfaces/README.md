# Interfaces

This folder contains the generated OpenAPI specification for the Notes backend.

- openapi.json: Generated OpenAPI schema for the FastAPI application, including the /notes CRUD endpoints and health check.

Regeneration
- Ensure the backend app exposes the OpenAPI at /openapi.json (FastAPI default).
- A small helper script (e.g., scripts/generate_openapi.py) can fetch from the running service and write to this path:
  personal-notes-manager-27974-27994/notes_backend/interfaces/openapi.json

CORS
- The backend should enable CORSMiddleware to allow the frontend origin:
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
- Ensure database tables are created on startup (e.g., in a FastAPI startup event) so the app is ready to serve requests without manual migrations for this simple demo.
- Example:
  @app.on_event("startup")
  async def on_startup():
      # SQLAlchemy example:
      # Base.metadata.create_all(bind=engine)
      pass
