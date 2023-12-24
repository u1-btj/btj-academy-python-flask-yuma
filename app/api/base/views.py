from flask import Blueprint, jsonify

from .base_schemas import BaseResponse
router = Blueprint("health", __name__, url_prefix='/api/v1/health')

@router.route('/',  methods=['GET'])
def get_health() -> BaseResponse:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return jsonify(BaseResponse(message="OK").__dict__)