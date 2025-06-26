import logging
import logging.config
from typing import Optional, TypedDict


class LogConfig(TypedDict):
    version: int
    disable_existing_loggers: bool
    formatters: dict
    handlers: dict
    root: dict


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance. If name is not provided,
    uses the caller's module name.
    """
    if name is None:
        name = __name__

    # Configure logging once at module level
    if not logging.getLogger().hasHandlers():
        config: LogConfig = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                }
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO",
            },
        }
        logging.config.dictConfig(config)

    return logging.getLogger(name)
