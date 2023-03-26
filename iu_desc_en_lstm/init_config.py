"""Flask application initialization."""
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base initialization config."""

    DEBUG = False
    PROPAGATE_EXCEPTIONS = True

    MODEL_DEVICE = str(os.environ.get('MODEL_DEVICE'))
    NUM_LAYERS = 1
    HIDDEN_SIZE = 512
    EMBED_SIZE = 256

    BASE_DIR = os.getcwd()
    VOCAB_PATH = os.path.join(BASE_DIR, 'ml_iu_desc_en_lstm', 'tokenizer', 'vocab.pkl')

    WEIGHTS_VERSION = str(os.environ.get('WEIGHTS_VERSION'))
    PREDTRAINED_VERSION = str(os.environ.get('PRETRAINED_FASTERRCNN_VERSION'))
    WEIGHTS_DIR = str(os.path.join(BASE_DIR, 'artifacts', 'weights', WEIGHTS_VERSION))
    PREDTRAINED_DIR = str(os.path.join(BASE_DIR, 'artifacts', 'predtrained', PREDTRAINED_VERSION))
    ENCODER_WEIGHTS_FILENAME = str(os.environ.get('ENCODER_WEIGHTS_FILENAME'))
    DECODER_WEIGHTS_FILENAME = str(os.environ.get('DECODER_WEIGHTS_FILENAME'))
    PREDTRAINED_FILENAME = str(os.environ.get('PREDTRAINED_FILENAME'))
    ENCODER_WEIGHTS_FILE_PATH = str(os.path.join(WEIGHTS_DIR, ENCODER_WEIGHTS_FILENAME))
    DECODER_WEIGHTS_FILE_PATH = str(os.path.join(WEIGHTS_DIR, DECODER_WEIGHTS_FILENAME))
    PREDTRAINED_FILE_PATH = str(os.path.join(PREDTRAINED_DIR, PREDTRAINED_FILENAME))

    SHARED_FILES_DIR = str(os.environ.get('CONTAINER_IMAGE_DIR'))

    """Logging."""

    # available log-levels:
    # https://docs.python.org/3/library/logging.html#levels
    DEFAULT_LOGGERS_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production config."""

    ENV = 'production'
    DEBUG = False
    CONSOLE_LOG_LEVEL = 'INFO'


class DevelopmentConfig(Config):
    """Development config."""

    ENV = 'development'
    DEBUG = True
    CONSOLE_LOG_LEVEL = 'DEBUG'
