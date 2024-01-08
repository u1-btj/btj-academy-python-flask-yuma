from pydantic import BaseModel, Field, EmailStr
from api.base.base_schemas import BaseResponse
from utils import REGEX_PASSWORD

from models.user import UserSchema


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=6, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20, regex=REGEX_PASSWORD)


class RegisterResponse(BaseResponse):
    data: dict | None


class UserTokenSchema(UserSchema):
    access_token: str | None
    refresh_token: str | None


class RefreshTokenResponse(BaseResponse):
    data: dict | None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseResponse):
    data: dict | None


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=6, max_length=20, regex=REGEX_PASSWORD)
    new_password: str = Field(min_length=6, max_length=20, regex=REGEX_PASSWORD)
