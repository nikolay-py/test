"""Flask app initialization for wsgi."""
from api import create_app

from api.utils.check_artifacts import check_artifacts

check_artifacts()

app = create_app()
