class CustomException(Exception):
    """Base exception with status code support"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code


class ParserException(CustomException):
    pass
