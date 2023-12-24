from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from flask_pydantic import validate
from api.base.base_schemas import BaseResponse
from middlewares.authentication import get_user_id_from_access_token

from .schema import (
    ReadAllUserResponse,
    ReadUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    ReadAllUseParamRequest,
)
from .use_cases import DeactivateUser, ReadAllUser, ReadUser, UpdateUser

router = Blueprint("user", __name__, url_prefix='/api/v1/user')


@router.route("/", methods=["GET"])
@validate()
def read_all(
    query: ReadAllUseParamRequest,
):
    try:
        get_user_id_from_access_token(request),

        read_all = ReadAllUser()

        resp_data = read_all.execute(
            page_params=query, include_deactivated=query.include_deactivated
        )

        return jsonify(ReadAllUserResponse(
            status="success",
            message="success read users",
            data={"records":resp_data[0], "meta":resp_data[1].__dict__},
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(ReadAllUserResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to read users"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(ReadAllUserResponse(
            status="error",
            message=message,
        ).__dict__), 500

@router.route("/<user_id>", methods=["GET"])
@validate()
def read(
    user_id: int
):
    try:
        get_user_id_from_access_token(request)

        read_user = ReadUser()
        resp_data = read_user.execute(user_id=user_id)

        return jsonify(ReadUserResponse(
            status="success",
            message="success read user",
            data=resp_data.__dict__,
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(ReadUserResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to read user"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(ReadUserResponse(
            status="error",
            message=message,
        ).__dict__), 500

@router.route("/", methods=["PUT"])
@validate()
def update(
    body: UpdateUserRequest,
):
    try:
        token_user_id = get_user_id_from_access_token(request)

        update_user = UpdateUser()
        resp_data = update_user.execute(user_id=token_user_id, request=body)

        return jsonify(UpdateUserResponse(
            status="success",
            message="success update user",
            data=resp_data.__dict__,
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(UpdateUserResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message="failed to update user"
        if hasattr(e, 'message'):
            message = e.message
        elif hasattr(e, 'detail'):
            message = e.detail

        return jsonify(UpdateUserResponse(
            status="error",
            message=message,
        ).__dict__), 500

@router.route("/deactivate", methods=["PUT"])
def deactivate():
    try:
        token_user_id = get_user_id_from_access_token(request)
        
        deactivate_user = DeactivateUser()
        deactivate_user.execute(
            user_id=token_user_id,
        )

        return jsonify(BaseResponse(
            status="success",
            message="success deactivate user",
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(BaseResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message = "error deactivate user"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(BaseResponse(
            status="error",
            message=message,
        ).__dict__), 500
