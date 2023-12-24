import datetime
import bcrypt

from sqlalchemy import select
from werkzeug.exceptions import HTTPException

from db import get_session
from middlewares.authentication import generate_access_token, generate_refresh_token
from models.user import User, UserSchema
from .schema import (
    RegisterRequest,
    LoginRequest,
    UserTokenSchema,
    ChangePasswordRequest,
)

class Register:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, request: RegisterRequest) -> UserSchema:
        with self.session as session:
            usr = session.execute(
                select(User).where(User.username == request.username)
            )
            usr = usr.scalars().first()
            if usr is not None:
                exception = HTTPException(description=f"username: {request.username} is already taken")
                exception.code = 400
                raise exception

            usr = session.execute(select(User).where(User.email == request.email))
            usr = usr.scalars().first()
            if usr is not None:
                exception = HTTPException(description=f"email: {request.email} is already taken")
                exception.code = 400
                raise exception

            pw_bytes = request.password.encode()
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(
                password=pw_bytes,
                salt=salt,
            )

            user = User()
            user.name = request.name
            user.email = request.email
            user.username = request.username
            user.password = hashed_pw.decode()
            user.created_at = datetime.datetime.utcnow()
            user.updated_at = datetime.datetime.utcnow()

            session.add(user)
            session.flush()

            return UserSchema.from_orm(user)


class LoginUser:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
        self,
        data: LoginRequest,
    ) -> UserTokenSchema:
        with self.session as session:
            user = session.execute(
                select(User).where(
                    (
                        (User.username == data.username).__or__(
                            User.email == data.username
                        )
                    ).__and__(User.deactivated_at == None)
                )
            )
            user = user.scalars().first()
            if user is None:
                exception = HTTPException(description="login failed, make sure your credential are correct and try again")
                exception.code = 404
                raise exception
            
            password_matched = bcrypt.checkpw(
                password=data.password.encode(),
                hashed_password=user.password.encode(),
            )
            if not password_matched:
                exception = HTTPException(description="login failed, make sure your credential are correct and try again")
                exception.code = 401
                raise exception

            resp_data = UserTokenSchema.from_orm(user)
            resp_data.access_token = generate_access_token(user.user_id)
            resp_data.refresh_token = generate_refresh_token(user.user_id)

            return resp_data


class ChangePassword:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
        self,
        data: ChangePasswordRequest,
        user_id: int,
    ) -> None:
        with self.session as session:
            user = session.execute(
                select(User).where(
                    (User.user_id == user_id).__and__(User.deactivated_at == None)
                )
            )
            user = user.scalars().first()
            if user is None:
                exception = HTTPException(description=f"user with id: {user_id} does not exist")
                exception.code = 404
                raise exception

            password_matched = bcrypt.checkpw(
                password=data.old_password.encode(),
                hashed_password=user.password.encode(),
            )
            if not password_matched:
                exception = HTTPException(description="incorrect password")
                exception.code = 400
                raise exception

            pw_bytes = data.new_password.encode()
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(
                password=pw_bytes,
                salt=salt,
            )

            user.password = hashed_pw.decode()
            user.updated_at = datetime.datetime.utcnow()
            user.updated_by = user_id

            session.flush()
