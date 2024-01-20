import datetime
import math

from werkzeug.exceptions import HTTPException

from sqlalchemy import func, select

from db import get_session
from models.note import Note, NoteSchema
from .schemas import AddNoteRequest, UpdateNoteRequest, GetAllNotesRequest
from api.base.base_schemas import PaginationMetaResponse, PaginationParams

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

            if note.created_by != user_id:
                exception = HTTPException(description="not valid credentials")
                exception.code = 401
                raise exception

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

            if note.created_by != user_id:
                exception = HTTPException(description="not valid credentials")
                exception.code = 401
                raise exception

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
        
class GetNote:
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

            if note.created_by != user_id:
                exception = HTTPException(description="not valid credentials")
                exception.code = 401
                raise exception

            if not note:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception

            return NoteSchema.from_orm(note)
        
class GetAllNotes:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
        self,
        page_params: GetAllNotesRequest,
        user_id: int
    ) -> (list[dict], PaginationMetaResponse):
        with self.session as session:
            page_query = (
                select(Note)
                .offset((page_params.page - 1) * page_params.item_per_page)
                .limit(page_params.item_per_page)
            )

            total_query = (
                select(func.count())
                .select_from(Note)
            )

            if page_params.filter_by_user_id:
                page_query = page_query.filter(Note.created_by == user_id)
                total_query = total_query.filter(Note.created_by == user_id)
            
            if not page_params.include_deleted_note:
                page_query = page_query.filter(Note.deleted_at == None)
                total_query = total_query.filter(Note.deleted_at == None)

            paginated_query = session.execute(page_query)
            paginated_query = paginated_query.scalars().all()
            
            total_item = session.execute(total_query)
            total_item = total_item.scalar()

            notes = [NoteSchema.from_orm(p).__dict__ for p in paginated_query]

            meta = PaginationMetaResponse(
                total_item=total_item,
                page=page_params.page,
                item_per_page=page_params.item_per_page,
                total_page=math.ceil(total_item / page_params.item_per_page),
            )

            return notes, meta
