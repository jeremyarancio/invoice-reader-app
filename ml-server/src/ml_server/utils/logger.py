from loguru import logger

logger.add(
    "app.log",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    enqueue=True,
)


def get_logger():
    """Get the configured logger instance."""
    return logger
