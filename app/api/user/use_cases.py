import datetime
import math

from werkzeug.exceptions import HTTPException

from sqlalchemy import func, select

from db import get_session
from api.base.base_schemas import PaginationMetaResponse, PaginationParams
from models.user import User, UserSchema
from .schemas import (
    UpdateUserRequest,
)

class ReadAllUser:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
        self,
        page_params: PaginationParams,
        include_deactivated: bool,
    ) -> (list[dict], PaginationMetaResponse):
        with self.session as session:
            total_item = session.execute(
                select(func.count())
                .select_from(User)
                .where(User.deactivated_at == None)
            )
            total_item = total_item.scalar()

            query = (
                select(User)
                .offset((page_params.page - 1) * page_params.item_per_page)
                .limit(page_params.item_per_page)
            )
            if not include_deactivated:
                query = query.filter(User.deactivated_at == None)

            paginated_query = session.execute(query)
            paginated_query = paginated_query.scalars().all()

            users = [UserSchema.from_orm(p).__dict__ for p in paginated_query]

            meta = PaginationMetaResponse(
                total_item=total_item,
                page=page_params.page,
                item_per_page=page_params.item_per_page,
                total_page=math.ceil(total_item / page_params.item_per_page),
            )

            return users, meta


class ReadUser:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, user_id: int) -> UserSchema:
        with self.session as session:
            user = session.execute(
                select(User).where(
                    (User.user_id == user_id).__and__(User.deactivated_at == None)
                )
            )
            user = user.scalars().first()
            if not user:
                exception = HTTPException(description="user not found")
                exception.code = 404
                raise exception
            return UserSchema.from_orm(user)


class UpdateUser:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(self, user_id: int, request: UpdateUserRequest) -> UserSchema:
        with self.session as session:
            user = session.execute(
                select(User).where(
                    (User.user_id == user_id).__and__(User.deactivated_at == None)
                )
            )
            user = user.scalars().first()
            if not user:
                exception = HTTPException(description="user not found")
                exception.code = 404
                raise exception

            username_is_modified = user.username != request.username
            if username_is_modified:
                u = session.execute(
                    select(User).where(User.username == request.username)
                )
                u = u.scalars().first()
                if u is not None:
                    exception = HTTPException(description=f"username: {request.username} is already taken")
                    exception.code = 400
                    raise exception

            email_is_modified = user.email != request.email
            if email_is_modified:
                u = session.execute(
                    select(User).where(User.email == request.email)
                )
                u = u.scalars().first()
                if u is not None:
                    exception = HTTPException(description=f"email: {request.email} is already taken")
                    exception.code = 400
                    raise exception

            user.name = request.name
            user.username = request.username
            user.email = request.email
            user.updated_at = datetime.datetime.utcnow()
            user.updated_by = user_id

            session.flush()
            return UserSchema.from_orm(user)


class DeactivateUser:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
        self,
        user_id: int,
    ) -> UserSchema:
        with self.session as session:
            user = session.execute(
                select(User).where(
                    (User.user_id == user_id).__and__(User.deactivated_at == None)
                )
            )
            user = user.scalars().first()

            if not user:
                exception = HTTPException(description="user not found")
                exception.code = 404
                raise exception

            user.deactivated_at = datetime.datetime.utcnow()
            user.deactivated_by = user_id

            session.flush()

            return UserSchema.from_orm(user)
