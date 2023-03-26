import logging.config

from api.logging.settings import logger_config

from init_config import Config


def initialize_loggers():
    """Initialize all loggers."""

    logging.config.dictConfig(logger_config)

    own_loggers = ['api']

    for name, obj in logging.root.manager.loggerDict.items():
        if name.split('.')[0] in own_loggers and isinstance(obj, logging.Logger):
            obj.setLevel(Config.DEFAULT_LOGGERS_LEVEL)
            obj.handlers.extend(logging.root.getChild('desc_en_logger').handlers)