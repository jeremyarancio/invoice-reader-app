from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from invoice_reader.domain.auth import EncodedToken
from invoice_reader.domain.user import UserID
from invoice_reader.interfaces.dependencies.infrastructure import get_user_repository
from invoice_reader.services.auth import AuthService
from invoice_reader.services.exceptions import EntityNotFoundException
from invoice_reader.services.interfaces.repositories import IUserRepository
from invoice_reader.settings import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user_id(
    access_token: Annotated[EncodedToken, Depends(oauth2_scheme)],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> UserID:
    payload = AuthService.decode_token(token=access_token)
    user = user_repository.get_by_email(email=payload.email)
    if not user:
        raise EntityNotFoundException(message="User not found.")
    return user.user_id
