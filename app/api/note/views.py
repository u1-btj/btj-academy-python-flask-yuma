from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from flask_pydantic import validate
from api.base.base_schemas import BaseResponse
from middlewares.authentication import get_user_id_from_access_token

from .schemas import (
    AddNoteRequest,
    AddNoteResponse
)
from .use_cases import AddNewNote

router = Blueprint("note", __name__, url_prefix='/api/v1/notes')

@router.route("/", methods=["POST"])
@validate()
def create(
    body: AddNoteRequest
) -> AddNoteResponse:
    try:
        token_user_id = get_user_id_from_access_token(request)
        
        resp_data = AddNewNote().execute(request=body, user_id=token_user_id)

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