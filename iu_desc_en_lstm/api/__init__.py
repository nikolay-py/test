"""Flask app initialization."""
import os

from flask import Flask

from flask_restful import Api

from flask_log_request_id import RequestID


def create_app() -> Flask:
    """Create and configure Flask app."""
    try:
        app = Flask(__name__)

        app.config.from_object(os.environ['APP_SETTINGS'])

        RequestID(app).init_app(app)

        with app.app_context():
            from api.exceptions.invalid_api_usage import InvalidAPIUsage, invalid_api_usage
            from api.exceptions.app_general_exception_handler import app_general_exception_handler
            from api.logging.loggers import initialize_loggers
            from api.routes.routes import initialize_routes

            app.register_error_handler(InvalidAPIUsage, invalid_api_usage)
            app.register_error_handler(Exception, app_general_exception_handler)

            api = Api(app)
            initialize_routes(api)

            initialize_loggers()

    except Exception as err:
        print(f"Unexpected error during flask app init {err=}, {type(err)=}")
        raise

    return app
