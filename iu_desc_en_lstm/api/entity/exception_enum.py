"""Enumeration of backend errors."""
from enum import Enum


class ExceptionEnum(Enum):
    """Class with enumeration of backend errors."""

    PATH_NOT_PROVIDED = 'No path provided'
    IMAGE_NOT_FOUND = 'Image not found'
    INTERNAL_SERVER_ERROR = 'The server encountered an unexpected condition which prevented ' \
                            'it from fulfilling the request.'
