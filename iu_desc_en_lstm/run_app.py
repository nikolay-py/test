from api import create_app
from api.utils.check_artifacts import check_artifacts

check_artifacts()

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
