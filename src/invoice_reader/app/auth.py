from datetime import datetime, timedelta
from typing import Annotated

import jwt
import sqlmodel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from invoice_reader import db, presenter, settings
from invoice_reader.schemas import TokenDataSchema, UserCreateSchema, UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

EXISTING_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email already used."
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)]
) -> UserSchema | None:
    try:
        payload: dict = jwt.decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenDataSchema(username=username)
    except InvalidTokenError:
        raise CREDENTIALS_EXCEPTION
    user = presenter.get_user_by_username(username=token_data.username, session=session)
    return user


def authenticate_user(username: str, password: str, session: sqlmodel.Session) -> UserSchema | None:
    user = presenter.get_user_by_username(username=username, session=session)
    if verify_password(password, user.hashed_password):
        return user


def create_access_token(username: str) -> str:
    to_encode = {"sub": username}
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode, 
        key=settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def register_user(user: UserCreateSchema, session: sqlmodel.Session) -> None:
    existing_user = presenter.get_user_by_email(user.email, session=session)
    if existing_user:
        raise EXISTING_USER_EXCEPTION
    hashed_password = get_password_hash(user.password)
    user = UserSchema(hashed_password=hashed_password, **user.model_dump())
    presenter.add_user(user=user, session=session)
