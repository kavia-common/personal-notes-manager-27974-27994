from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Shared properties for Note objects."""

    title: str = Field(..., description="Title of the note")
    content: Optional[str] = Field(None, description="Content/body of the note")


class NoteCreate(NoteBase):
    """Properties required to create a new Note."""
    pass


class NoteUpdate(BaseModel):
    """Properties allowed when updating an existing Note."""
    title: Optional[str] = Field(None, description="Updated title for the note")
    content: Optional[str] = Field(None, description="Updated content for the note")


class NoteOut(NoteBase):
    """Response schema for a Note item with metadata."""

    id: int = Field(..., description="Unique identifier of the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True  # enables orm_mode in Pydantic v2
