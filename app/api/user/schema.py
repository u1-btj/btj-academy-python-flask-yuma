from pydantic import BaseModel, Field, EmailStr
from api.base.base_schemas import BaseResponse, PaginationParams
from utils import REGEX_PASSWORD

class ReadUserResponse(BaseResponse):
    data: dict | None

class ReadAllUserResponse(BaseResponse):
    data: dict | None

class ReadAllUseParamRequest(PaginationParams):
    include_deactivated: bool = False,

class UpdateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=6, max_length=100)
    email: EmailStr


class UpdateUserResponse(BaseResponse):
    data: dict | None


class ActivateDeactivateUserResponse(BaseResponse):
    data: dict | None
