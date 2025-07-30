from loguru import Logger, logger


def get_logger() -> Logger:
    """Get the configured logger instance."""
    logger.add(
        "app.log",
        rotation="10 MB",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        enqueue=True,
    )
    return logger
