from flask import Blueprint, jsonify, request

from api.base.base_schemas import BaseResponse
from middlewares.authentication import (
    refresh_access_token,
    get_user_id_from_access_token,
)
from werkzeug.exceptions import HTTPException
from flask_pydantic import validate
from .schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginResponse,
    LoginRequest,
    RefreshTokenResponse,
    ChangePasswordRequest,
)
from .use_cases import LoginUser, Register, ChangePassword

router = Blueprint("auth", __name__, url_prefix='/api/v1/auth')

@router.route("/register", methods=['POST'])
@validate()
def create(
    body: RegisterRequest,
) -> RegisterResponse:
    try:
        resp_data = Register().execute(
            request=body,
        )

        return jsonify(RegisterResponse(
            status="success",
            message="success register new user",
            data=resp_data,
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(RegisterResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to register new user"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(RegisterResponse(
            status="error",
            message=message,
        ).__dict__), 500

@router.route("/login", methods=['POST'])
@validate()
def login(
    body: LoginRequest,
):
    try:
        resp_data = LoginUser().execute(
            data=body,
        )
        return jsonify(LoginResponse(
            status="success",
            message=f"success login for username: {body.username}",
            data=resp_data.__dict__,
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(LoginResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to login"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail
        return jsonify(LoginResponse(
            status="error",
            message=message,
        ).__dict__), 500

@router.route("/refresh-token", methods=['GET'])
def refresh_token():
    try:
        new_token: list[str] = refresh_access_token(request)

        return jsonify(RefreshTokenResponse(
            status="success",
            message="success refreshing access token",
            data={
                "access_token":str(new_token[0]), "refresh_token":str(new_token[1])
            },
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(RefreshTokenResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message = "failed refresh token"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail
        return jsonify(RefreshTokenResponse(
            status="error",
            message=message,
        ).__dict__), 500

@router.route("/change-password", methods=['PUT'])
@validate()
def change_password(
    body: ChangePasswordRequest,
) -> BaseResponse:
    try:
        token_user_id: int = get_user_id_from_access_token(request),
        
        ChangePassword().execute(user_id=token_user_id, data=body)

        return jsonify(BaseResponse(
            status="success",
            message="success change password user",
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(BaseResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message = "error change password user"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(BaseResponse(
            status="error",
            message=message,
        ).__dict__), 500
