"""Image en description API."""
import logging
import os
import time

from flask import request
from flask_restful import Resource

from api.entity.exception_enum import ExceptionEnum
from api.exceptions.invalid_api_usage import InvalidAPIUsage

from init_config import Config

from ml_iu_desc_en_lstm.init_model import init_model, get_description

LOGGER = logging.getLogger(__name__)


class ImageDesc(Resource):
    """API for image description."""
    transform, device, encoder, decoder, vocab = init_model()

    def post(self) -> dict:
        """Image processing and return description."""
        LOGGER.debug('POST-request received')

        path = request.get_json().get('path')

        if not path:
            LOGGER.error(f'InvalidAPIUsage: {ExceptionEnum.PATH_NOT_PROVIDED.value}')
            raise InvalidAPIUsage(ExceptionEnum.PATH_NOT_PROVIDED, status_code=400)

        image_path = os.path.join(Config.SHARED_FILES_DIR, path)

        if not os.path.isfile(image_path):
            LOGGER.error(f'InvalidAPIUsage: Image does not exist:\nimage_path={image_path}')
            raise InvalidAPIUsage(ExceptionEnum.IMAGE_NOT_FOUND)

        try:
            LOGGER.debug('Image processing starting')
            start_proc_time = time.perf_counter()

            response = get_description(
                self.device, self.transform, self.encoder, self.decoder, self.vocab, image_path
            )

            img_proc_time = time.perf_counter() - start_proc_time
            LOGGER.info(f'Image processing time is {img_proc_time}')
            LOGGER.debug('Image processing completed')
        except FileNotFoundError:
            LOGGER.exception(f'Internal Server Error while image processing')
            raise InvalidAPIUsage(ExceptionEnum.INTERNAL_SERVER_ERROR)

        return response
