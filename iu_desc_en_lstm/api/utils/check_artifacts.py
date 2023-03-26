"""Checking weights files existing."""
import os

from init_config import Config


def check_artifacts():
    if not os.path.exists(Config.ENCODER_WEIGHTS_FILE_PATH):
        raise FileNotFoundError(f'Weights file with {Config.WEIGHTS_VERSION} version was not found')
    if not os.path.exists(Config.DECODER_WEIGHTS_FILE_PATH):
        raise FileNotFoundError(f'Weights file with {Config.WEIGHTS_VERSION} version was not found')
