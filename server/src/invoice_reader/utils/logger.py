from functools import lru_cache

from loguru import logger


@lru_cache
def get_logger():
    return logger
