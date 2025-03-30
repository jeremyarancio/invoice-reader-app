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
    headers={"WWW-Authenticate": "Bearer"},
)

EXISTING_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Email already used."
)

EXISTING_INVOICE_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Invoice already exisiting."
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

ROLLBACK = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Something went wrong with ",
)

EXPIRED_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The JWT is expired. Generate a new one.",
)
