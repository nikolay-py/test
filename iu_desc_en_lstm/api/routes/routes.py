"""Routes and functionality."""
from flask_restful import Api

from api.resources.health import Health
from api.resources.image_desc import ImageDesc


def initialize_routes(api: Api) -> None:
    """Initialize all routes."""
    api.add_resource(ImageDesc, '/api/image_desc_en')
    api.add_resource(Health, '/health')
