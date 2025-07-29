from loguru import logger, Logger

def get_logger() -> Logger:
    """Get the configured logger instance."""
    return logger