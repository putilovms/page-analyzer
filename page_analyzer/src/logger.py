import logging.config
import logging

# CUSTOM_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CUSTOM_TIME_FORMAT = '%H:%M'
LOG_FILENAME = "page_analyzer.log"

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            "datefmt": CUSTOM_TIME_FORMAT,
        },
    },
    "handlers": {
        "logfile": {
            "formatter": "default",
            "level": "DEBUG",
            "filename": LOG_FILENAME,
            "class": "logging.FileHandler",
            "mode": "w",
        },
        "stdout": {
            "formatter": "default",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {},
    "root": {
        "level": "DEBUG",
        "handlers": [
            "logfile",
            "stdout"
        ],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

log = logging.getLogger(__name__)
log.info('Logger is active!')
