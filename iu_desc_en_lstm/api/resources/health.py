from flask_restful import Resource


class Health(Resource):
    """API for health-check."""

    def get(self) -> str:
        return "ok"
