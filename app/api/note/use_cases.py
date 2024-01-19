import datetime
import math

from werkzeug.exceptions import HTTPException

from sqlalchemy import func, select

from db import get_session
from models.note import Note, NoteSchema
from .schemas import AddNoteRequest

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