"""Settings for logging."""
from flask import current_app

from flask_log_request_id import RequestIDLogFilter

logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(request_id)s %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': current_app.config['CONSOLE_LOG_LEVEL'],
            'formatter': 'json',
            'filters': ['request_id_filter'],
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'desc_en_logger': {
            'handlers': ['console']
        },
    },
    'filters': {
        'request_id_filter': {
            '()': RequestIDLogFilter,
        },
    },
}
