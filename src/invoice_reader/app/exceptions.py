from fastapi import HTTPException, status

EXISTING_CLIENT_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Client already exisiting. "
)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

EXISTING_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Email already used."
)
