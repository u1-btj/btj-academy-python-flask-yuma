from datetime import datetime, timedelta
from enum import Enum

import jwt
from werkzeug.exceptions import HTTPException
from flask import Request

from settings import settings

algorithm = "HS256"


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def generate_access_token(user_id: int) -> str:
    return jwt.encode(
        payload={
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "user_id": user_id,
            "token_type": TokenType.ACCESS.value,
        },
        key=settings.SECRET_KEY,
        algorithm=algorithm,
    )


def generate_refresh_token(user_id: int) -> str:
    return jwt.encode(
        payload={
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            "user_id": user_id,
            "token_type": TokenType.REFRESH.value,
        },
        key=settings.SECRET_KEY,
        algorithm=algorithm,
    )


def verify_token_type(payload: dict, token_type: TokenType) -> bool:
    str_token_type = payload.get("token_type")
    if str_token_type is None:
        return False

    actual_token_type = TokenType(str_token_type)
    if actual_token_type is not token_type:
        return False

    return True


def get_user_id_from_access_token(
    request: Request
) -> int:
    credentials_exception = HTTPException(
        description="could not validate credentials",
    )
    credentials_exception.code = 401
    
    token = None
    if "Authorization" in request.headers:
        header_values = request.headers["Authorization"].split(" ")
        if header_values[0] != "Bearer":
            credentials_exception.description = "invalid header"
            raise credentials_exception
        
        token = header_values[1]

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[algorithm]
        )
    except jwt.ExpiredSignatureError as e:
        credentials_exception.description = e.__str__()
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    token_type_matched = verify_token_type(
        payload=payload,
        token_type=TokenType.ACCESS,
    )
    if not token_type_matched:
        credentials_exception.description = (
            f"mismatched token type, expecting token with type {TokenType.ACCESS.value}"
        )
        raise credentials_exception

    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    return user_id


def refresh_access_token(
    request: Request
) -> tuple[str, str]:
    credentials_exception = HTTPException(
        description="could not validate credentials",
    )
    credentials_exception.code = 401

    token = None
    if "Authorization" in request.headers:
        header_values = request.headers["Authorization"].split(" ")
        if header_values[0] != "Bearer":
            credentials_exception.description = "invalid header"
            raise credentials_exception
        
        token = header_values[1]

    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[algorithm]
        )
    except jwt.ExpiredSignatureError as e:
        credentials_exception.description = e.__str__()
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    token_type_matched = verify_token_type(
        payload=payload,
        token_type=TokenType.REFRESH,
    )
    if not token_type_matched:
        credentials_exception.description = f"mismatched token type, expecting token with type {TokenType.REFRESH.value}"
        raise credentials_exception

    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    response = [generate_access_token(user_id=user_id), generate_refresh_token(user_id=user_id)]

    return response
