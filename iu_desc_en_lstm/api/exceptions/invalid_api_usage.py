"""API using exceptions."""
from typing import Dict, Union, Tuple

from flask import Response, jsonify

from api.entity.exception_enum import ExceptionEnum


class InvalidAPIUsage(Exception):
    """Class of exception about invalid API usage."""

    def __init__(self, error: ExceptionEnum = ExceptionEnum.INTERNAL_SERVER_ERROR,
                 status_code: int = 500,
                 payload: None = None) -> None:
        """Initialize some attributes of class."""
        super().__init__()
        self.error: str = error.name
        self.message: str = error.value
        self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """Create dict with parameters for answer."""
        answer_parameters: Dict[str, Union[str, int]] = dict(self.payload or ())
        answer_parameters['error'] = self.error
        answer_parameters['message'] = self.message
        return answer_parameters


def invalid_api_usage(exception: InvalidAPIUsage) -> Tuple[Response, int]:
    """Transform an exception to JSON format."""
    return jsonify(exception.to_dict()), exception.status_code
