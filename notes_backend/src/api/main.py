from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.session import init_db
from src.api.routes.notes import router as notes_router

app = FastAPI(
    title="Personal Notes API",
    description="Backend API for a personal notes manager. Provides CRUD endpoints for notes.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Service health and diagnostics"},
        {"name": "notes", "description": "Operations for managing notes"},
    ],
)

# Configure CORS to allow the frontend origin explicitly
# This is required so the React app running on http://localhost:3000 can call the API on http://localhost:3001
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """
    Create database tables on application startup.

    This ensures the SQLite file (notes.db) and all required tables exist before
    serving any request, enabling seamless local development without migrations.
    """
    init_db()


# Health route preserved
@app.get("/", tags=["health"], summary="Health Check")
def health_check():
    """Simple health check endpoint."""
    return {"message": "Healthy"}


# Include notes routes without an extra prefix so endpoints are at /notes
app.include_router(notes_router)
