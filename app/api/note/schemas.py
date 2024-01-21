from pydantic import BaseModel, Field, EmailStr
from api.base.base_schemas import BaseResponse, PaginationParams

class AddNoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1, max_length=500)

class AddNoteResponse(BaseResponse):
    data: dict | None

class UpdateNoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1, max_length=500)

class UpdateNoteResponse(BaseResponse):
    data: dict | None

class GetNoteResponse(BaseResponse):
    data: dict | None

class GetAllNotesResponse(BaseResponse):
    data: dict | None

class GetAllNotesRequest(PaginationParams):
    filter_by_user_id: bool = True
    include_deleted_note: bool = False