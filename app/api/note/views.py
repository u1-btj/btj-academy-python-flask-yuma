from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from flask_pydantic import validate
from api.base.base_schemas import BaseResponse
from middlewares.authentication import get_user_id_from_access_token

from .schemas import (
    AddNoteRequest,
    AddNoteResponse,
    UpdateNoteRequest,
    UpdateNoteResponse
)
from .use_cases import (
    AddNewNote,
    DeleteNote,
    UpdateNote
)

router = Blueprint("note", __name__, url_prefix='/api/v1/notes')

@router.route("/", methods=["POST"])
@validate()
def create(
    body: AddNoteRequest
) -> AddNoteResponse:
    try:
        user_id = get_user_id_from_access_token(request)
        
        resp_data = AddNewNote().execute(request=body, user_id=user_id)

        return jsonify(AddNoteResponse(
            status="success",
            message="success add new note",
            data=resp_data.dict(),
        ).__dict__), 200
    
    except HTTPException as ex:
        return jsonify(AddNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to add new note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(AddNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500
    
@router.route("/<note_id>", methods=["DELETE"])
@validate()
def delete(
    note_id: int
) -> BaseResponse:
    try:
        user_id = get_user_id_from_access_token(request)

        DeleteNote().execute(user_id=user_id, note_id=note_id)

        return jsonify(BaseResponse(
            status="success",
            message="success delete note",
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(BaseResponse(
            status="error",
            message=ex.description,
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to delete note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(BaseResponse(
            status="error",
            message=message,
        ).__dict__), 500

@router.route("/<note_id>", methods=["PUT"])
@validate()
def update(
    body: UpdateNoteRequest,
    note_id: int
) -> UpdateNoteResponse:
    try:
        user_id = get_user_id_from_access_token(request)

        resp_data = UpdateNote().execute(request=body, user_id=user_id, note_id=note_id)

        return jsonify(UpdateNoteResponse(
            status="success",
            message="success update note",
            data=resp_data.dict(),
        ).__dict__), 200
    except HTTPException as ex:
        return jsonify(UpdateNoteResponse(
            status="error",
            message=ex.description,
            data=None,
        ).__dict__), ex.code
    except Exception as e:
        message = "failed to update note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(UpdateNoteResponse(
            status="error",
            message=message,
            data=None,
        ).__dict__), 500