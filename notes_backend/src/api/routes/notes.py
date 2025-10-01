from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.db import crud, models
from src.db.schemas import NoteCreate, NoteUpdate, NoteOut

router = APIRouter(prefix="/notes", tags=["notes"])


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[NoteOut],
    summary="List notes",
    description="Retrieve a paginated list of notes ordered by creation time (newest first).",
    responses={200: {"description": "List of notes returned successfully."}},
)
def list_notes(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
) -> List[NoteOut]:
    """Return a paginated list of all notes."""
    return crud.get_notes(db, skip=skip, limit=limit)


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with the provided title and optional content.",
    responses={
        201: {"description": "Note created successfully."},
        422: {"description": "Validation error"},
    },
)
def create_note(note_in: NoteCreate, db: Session = Depends(get_db)) -> NoteOut:
    """Create and return a new note."""
    note = crud.create_note(db, note_in=note_in)
    return note


# PUBLIC_INTERFACE
@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get a note",
    description="Get a single note by its unique identifier.",
    responses={
        200: {"description": "Note found and returned."},
        404: {"description": "Note not found."},
    },
)
def get_note(
    note_id: int = Path(..., ge=1, description="ID of the note to retrieve"),
    db: Session = Depends(get_db),
) -> NoteOut:
    """Return a single note by ID or 404 if not found."""
    note = crud.get_note(db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note  # type: ignore[return-value]


# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update a note",
    description="Update an existing note by its ID with the provided fields.",
    responses={
        200: {"description": "Note updated successfully."},
        404: {"description": "Note not found."},
        422: {"description": "Validation error"},
    },
)
def update_note(
    note_id: int = Path(..., ge=1, description="ID of the note to update"),
    note_in: NoteUpdate = ...,
    db: Session = Depends(get_db),
) -> NoteOut:
    """Update and return the note, or 404 if it does not exist."""
    note_db: Optional[models.Note] = crud.get_note(db, note_id=note_id)
    if not note_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    updated = crud.update_note(db, note_db=note_db, note_in=note_in)
    return updated


# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its ID.",
    responses={
        204: {"description": "Note deleted successfully."},
        404: {"description": "Note not found."},
    },
)
def delete_note(
    note_id: int = Path(..., ge=1, description="ID of the note to delete"),
    db: Session = Depends(get_db),
) -> None:
    """Delete the note if it exists, else return 404."""
    note_db: Optional[models.Note] = crud.get_note(db, note_id=note_id)
    if not note_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    crud.delete_note(db, note_db=note_db)
    # 204 No Content implied by status_code, returning None
