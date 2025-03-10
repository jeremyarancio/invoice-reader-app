from datetime import datetime, timedelta
from typing import Annotated

import jwt
import sqlmodel
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from invoice_reader import db, presenter, settings
from invoice_reader.app.exceptions import (
    CREDENTIALS_EXCEPTION,
    EXISTING_USER_EXCEPTION,
    MISSING_ENVIRONMENT_VARIABLE_EXCEPTION,
    USER_NOT_FOUND_EXCEPTION,
)
from invoice_reader.schemas import user_schema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
) -> user_schema.User:
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
            raise CREDENTIALS_EXCEPTION
    except InvalidTokenError as e:
        raise CREDENTIALS_EXCEPTION from e
    except HTTPException:
        raise
    return user


def authenticate_user(
    email: str, password: str, session: sqlmodel.Session
) -> user_schema.User:
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


def register_user(user: user_schema.UserCreate, session: sqlmodel.Session) -> None:
    existing_user = presenter.get_user_by_email(user.email, session=session)
    if existing_user:
        raise EXISTING_USER_EXCEPTION
    hashed_password = get_password_hash(user.password)
    new_user = user_schema.User(
        hashed_password=hashed_password, email=user.email, is_disabled=False
    )
    presenter.add_user(user=new_user, session=session)
