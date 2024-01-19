import datetime
import math

from werkzeug.exceptions import HTTPException

from sqlalchemy import func, select

from db import get_session
from models.note import Note, NoteSchema
from .schemas import AddNoteRequest, UpdateNoteRequest

class AddNewNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, request: AddNoteRequest, user_id: int) -> NoteSchema:
        with self.session as session:
            note = Note()
            note.title = request.title
            note.content = request.content
            note.created_by = user_id
            note.updated_by = user_id
            note.created_at = datetime.datetime.utcnow()
            note.updated_at = datetime.datetime.utcnow()

            session.add(note)
            session.flush()

            return NoteSchema.from_orm(note)
        
class DeleteNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, user_id: int, note_id: int) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note).where(
                    (Note.note_id == note_id).__and__(Note.deleted_at == None)
                )
            )
            note = note.scalars().first()

            if not note:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception

            note.deleted_at = datetime.datetime.utcnow()
            note.deleted_by = user_id

            session.flush()

            return NoteSchema.from_orm(note)
        
class UpdateNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, request: UpdateNoteRequest, user_id: int, note_id: int) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note).where(
                    (Note.note_id == note_id).__and__(Note.deleted_at == None)
                )
            )
            note = note.scalars().first()

            if not note:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception

            note.title = request.title
            note.content = request.content
            note.updated_at = datetime.datetime.utcnow()
            note.updated_by = user_id

            session.flush()

            return NoteSchema.from_orm(note)