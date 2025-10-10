class CustomException(Exception):
    """Base exception with status code support"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code


class InvalidFileFormatException(CustomException):
    """Exception for invalid file format."""

    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)


class AmountsCurrencyMismatchException(CustomException):
    """Exception for mismatched currencies in Amount operations."""

    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)
