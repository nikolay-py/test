import os
import pytest

from dotenv import load_dotenv

load_dotenv()

@pytest.fixture()
def host_name() -> str:
    """Return host."""
    host = os.environ['PYTEST_HOST_PORT']
    return host


@pytest.fixture()
def img_path() -> str:
    """Return image's name."""
    host_image_dir = os.environ.get('HOST_IMAGE_DIR')

    source_file = 'tests_files/image_for_tests.jpg'
    destination_file = os.path.join(host_image_dir, 'image_for_tests.jpg')
    os.popen(f'cp {source_file} {destination_file}')

    return 'image_for_tests.jpg'

