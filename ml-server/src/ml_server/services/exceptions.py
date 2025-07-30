class CustomException(Exception):
    """Base exception with status code support"""

    status_code: int = 500  # Default to internal server error

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(message)


class ParserException(CustomException):
    status_code = 422
