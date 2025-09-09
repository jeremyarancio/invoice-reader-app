from fastapi import HTTPException, status

EXISTING_CLIENT_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Client already exisiting. "
)

USER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credentials are not valid.",
)

EXISTING_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Email already used."
)


class ExistingInvoiceException(HTTPException):
    "Custom exception to not rollback if Invoice already existing."


EXISTING_INVOICE_EXCEPTION = ExistingInvoiceException(
    status_code=status.HTTP_409_CONFLICT, detail="Invoice already exisiting."
)


ROLLBACK = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Something went wrong with storing a new invoice.",
)

UNPROCESSABLE_FILE = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="The uploaded file is unprocessable.",
)

MISSING_ENVIRONMENT_VARIABLE_EXCEPTION = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Missing required environment variable",
)

CLIENT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Client was not found."
)

INVOICE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Invoice was not found."
)


EXPIRED_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="The JWT is expired. Generate a new one.",
)


NO_REFRESH_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No refresh token found in cookie.",
)


INVALID_EXTRACTED_DATA_EXCEPTION = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Issue with parsing the document.",
)


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
