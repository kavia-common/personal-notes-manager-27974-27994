from typing import List, Optional

from sqlalchemy.orm import Session

from src.db import models
from src.db.schemas import NoteCreate, NoteUpdate


# PUBLIC_INTERFACE
def get_notes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Note]:
    """Return a paginated list of notes."""
    return (
        db.query(models.Note)
        .order_by(models.Note.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# PUBLIC_INTERFACE
def get_note(db: Session, note_id: int) -> Optional[models.Note]:
    """Return a single note by ID, or None if not found."""
    return db.query(models.Note).filter(models.Note.id == note_id).first()


# PUBLIC_INTERFACE
def create_note(db: Session, note_in: NoteCreate) -> models.Note:
    """Create and persist a new note."""
    note = models.Note(title=note_in.title, content=note_in.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
def update_note(db: Session, note_db: models.Note, note_in: NoteUpdate) -> models.Note:
    """Update an existing note with provided fields."""
    if note_in.title is not None:
        note_db.title = note_in.title
    if note_in.content is not None:
        note_db.content = note_in.content

    db.add(note_db)
    db.commit()
    db.refresh(note_db)
    return note_db


# PUBLIC_INTERFACE
def delete_note(db: Session, note_db: models.Note) -> None:
    """Delete an existing note."""
    db.delete(note_db)
    db.commit()
