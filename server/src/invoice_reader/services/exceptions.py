class CustomException(Exception):
    """Base exception with status code support"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code


class ExistingEntityException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class RollbackException(CustomException):
    pass


class EntityNotFoundException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class AuthenticationException(CustomException):
    """Could be 401 or 403."""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code=status_code)


class InfrastructureException(CustomException):
    """Exception for external infrastructure errors."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message, status_code=status_code)
