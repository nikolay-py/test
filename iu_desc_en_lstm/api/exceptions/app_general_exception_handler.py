"""General exception for Flask app."""
from typing import Any, Tuple

from flask import Response, jsonify, current_app

from api.entity.exception_enum import ExceptionEnum

from werkzeug.exceptions import HTTPException, InternalServerError
from werkzeug.http import HTTP_STATUS_CODES


def app_general_exception_handler(e) -> Tuple[Response, Any]:
    """General exception handler."""
    response = dict()

    if isinstance(e, HTTPException) and not isinstance(e, InternalServerError):
        response['error'] = HTTP_STATUS_CODES[e.code]
        response['message'] = e.description
        return jsonify(response), e.code

    if current_app.config['DEBUG']:
        raise e

    response['error'] = ExceptionEnum.INTERNAL_SERVER_ERROR.name
    response['message'] = ExceptionEnum.INTERNAL_SERVER_ERROR.value
    return jsonify(response), 500
