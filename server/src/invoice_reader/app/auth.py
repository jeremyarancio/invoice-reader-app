import uuid
from datetime import datetime, timedelta
from typing import Annotated

import jwt
import sqlmodel
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from invoice_reader import db, presenter, settings
from invoice_reader.app.exceptions import (
    CREDENTIALS_EXCEPTION,
    EXISTING_USER_EXCEPTION,
    EXPIRED_TOKEN_EXCEPTION,
    MISSING_ENVIRONMENT_VARIABLE_EXCEPTION,
    NO_REFRESH_TOKEN_EXCEPTION,
    USER_NOT_FOUND_EXCEPTION,
)
from invoice_reader.mappers import UserMapper
from invoice_reader.schemas import User, UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
) -> uuid.UUID:
    try:
        if not settings.JWT_ALGORITHM:
            raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
        payload = jwt.decode(
            token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
        user = presenter.get_user_by_email(email=email, session=session)
        if not user:
            raise USER_NOT_FOUND_EXCEPTION
    except ExpiredSignatureError as e:
        raise EXPIRED_TOKEN_EXCEPTION from e
    except InvalidTokenError as e:
        raise CREDENTIALS_EXCEPTION from e
    if not user.user_id:
        raise HTTPException(detail="User id not found.", status_code=500)
    return user.user_id


def authenticate_user(email: str, password: str, session: sqlmodel.Session) -> User:
    user = presenter.get_user_by_email(email=email, session=session)
    if not user:
        raise USER_NOT_FOUND_EXCEPTION
    if not verify_password(password, user.hashed_password):
        raise CREDENTIALS_EXCEPTION
    return user


def create_access_token(email: str) -> str:
    if not settings.JWT_SECRET_KEY or not settings.JWT_ALGORITHM:
        raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
    to_encode = {"sub": email}
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def register_user(user_create: UserCreate, session: sqlmodel.Session) -> None:
    """Move auth to presenter layer"""
    existing_user = presenter.get_user_by_email(user_create.email, session=session)
    if existing_user:
        raise EXISTING_USER_EXCEPTION
    hashed_password = get_password_hash(user_create.password)
    user = UserMapper.map_user_create_to_user(
        user_create=user_create,
        hashed_password=hashed_password,
        is_disable=False,
    )
    presenter.add_user(user=user, session=session)


def refresh_token(email: str, session: sqlmodel.Session) -> str:
    # TODO: Remove by switching to Pydantic-Config
    if not settings.JWT_ALGORITHM or not settings.JWT_SECRET_KEY:
        raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
    user = presenter.get_user_by_email(email=email, session=session)
    if not user:
        raise USER_NOT_FOUND_EXCEPTION
    refresh_token = presenter.get_refresh_token(user_id=user.user_id, session=session)
    if not refresh_token:
        raise NO_REFRESH_TOKEN_EXCEPTION
    try:
        jwt.decode(
            refresh_token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except ExpiredSignatureError as e:
        raise EXPIRED_TOKEN_EXCEPTION from e
    # If the refresh token is still valid, we can create a new access token
    return create_access_token(email=email)


def get_email_from_expired_token(
    token: str,
) -> str:
    try:
        if not settings.JWT_ALGORITHM:
            raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
        payload: dict = jwt.decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False},
        )
        email = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
        return email
    except InvalidTokenError as e:
        raise CREDENTIALS_EXCEPTION from e
