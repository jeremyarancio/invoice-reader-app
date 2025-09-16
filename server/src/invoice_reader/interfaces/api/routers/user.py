from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.repository import get_user_repository
from invoice_reader.interfaces.schemas.auth import AuthToken
from invoice_reader.interfaces.schemas.user import UserCreate, UserResponse
from invoice_reader.services.auth import AuthService
from invoice_reader.services.exceptions import AuthenticationException
from invoice_reader.services.interfaces.repositories import IUserRepository
from invoice_reader.services.user import UserService
from invoice_reader.settings import get_settings

settings = get_settings()

router = APIRouter(
    prefix="/v1/users",
    tags=["Users"],
)


@router.post("/signup/")
def signup(
    user_create: UserCreate,
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> Response:
    UserService.register_user(
        email=user_create.email,
        password=user_create.password,
        user_repository=user_repository,
    )
    return Response(content="User has been added to the database.", status_code=201)


@router.post("/signin/")
def signin(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> AuthToken:
    access_token, refresh_token = UserService.authenticate_user(
        email=form_data.username,
        password=form_data.password,
        user_repository=user_repository,
    )
    response.set_cookie(
        value=refresh_token,
        expires=settings.refresh_token_expire,
        key="refresh_token",
        httponly=True,
        secure=settings.protocol == "https",
        samesite="none" if settings.protocol == "https" else "lax",
        domain=settings.domain_name,
    )
    return AuthToken(access_token=access_token, token_type="bearer")


@router.delete("/")
def delete_user(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> Response:
    UserService.delete(user_id=user_id, user_repository=user_repository)
    return Response(content="User successfully deleted.", status_code=204)


@router.post("/refresh/")
def refresh(request: Request, response: Response) -> AuthToken:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise AuthenticationException(message="No refresh token found.")
    access_token, refresh_token = AuthService.refresh_token(token=refresh_token)
    response.set_cookie(
        value=refresh_token,
        expires=settings.refresh_token_expire,
        key="refresh_token",
        httponly=True,
        secure=settings.protocol == "https",
        samesite="none" if settings.protocol == "https" else "lax",
        domain=settings.domain_name,
    )

    return AuthToken(access_token=access_token, token_type="bearer")


@router.post("/signout/")
def signout(response: Response) -> Response:
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=settings.protocol == "https",
        samesite="none" if settings.protocol == "https" else "lax",
        domain=settings.domain_name,
    )
    return Response(content="User successfully signed out.", status_code=204)


@router.get("/me/")
def get_current_user(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> UserResponse:
    user = UserService.get_user(user_id=user_id, user_repository=user_repository)
    return UserResponse.from_user(user)
