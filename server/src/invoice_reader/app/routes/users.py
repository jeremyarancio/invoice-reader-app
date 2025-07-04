import uuid
from typing import Annotated

import sqlmodel
from fastapi import APIRouter, Depends, Request, Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from invoice_reader import db, presenter, settings
from invoice_reader.app import auth
from invoice_reader.app.exceptions import NO_REFRESH_TOKEN_EXCEPTION
from invoice_reader.schemas import AuthToken, UserCreate, UserResponse

COOKIE_CONFIG = {
    "key": "refresh_token",
    "httponly": True,
    "secure": settings.PROTOCOL == "https",
    "samesite": "none" if settings.PROTOCOL == "https" else "lax",
    "domain": settings.DOMAIN_NAME,
}


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post("/signup/")
def signup(
    user_create: UserCreate,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
):
    auth.register_user(user_create=user_create, session=session)
    return Response(content="User has been added to the database.", status_code=201)


@router.post("/signin/")
def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    response: Response,
) -> AuthToken:
    try:
        user = auth.authenticate_user(
            email=form_data.username, password=form_data.password, session=session
        )
        access_token = auth.create_token(
            email=user.email,
            expire=settings.ACCESS_TOKEN_EXPIRE,
            token_type="access",
        )
        refresh_token = auth.create_token(
            email=user.email,
            expire=settings.REFRESH_TOKEN_EXPIRE,
            token_type="refresh",
        )
        response.set_cookie(
            value=refresh_token,
            expires=settings.REFRESH_TOKEN_EXPIRE,
            key="refresh_token",
            httponly=True,
            secure=settings.PROTOCOL == "https",
            samesite="none" if settings.PROTOCOL == "https" else "lax",
            domain=settings.DOMAIN_NAME,
        )
        return AuthToken(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/")
def delete_user(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user_id: Annotated[uuid.UUID, Depends(auth.get_current_user_id)],
) -> Response:
    try:
        presenter.delete_user(user_id=user_id, session=session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return Response(content="User successfully deleted.", status_code=204)


@router.post("/refresh/")
def refresh(request: Request, response: Response) -> AuthToken:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise NO_REFRESH_TOKEN_EXCEPTION
    try:
        access_token, refresh_token = auth.refresh_token(token=refresh_token)
        response.set_cookie(
            value=refresh_token,
            expires=settings.REFRESH_TOKEN_EXPIRE,
            key="refresh_token",
            httponly=True,
            secure=settings.PROTOCOL == "https",
            samesite="none" if settings.PROTOCOL == "https" else "lax",
            domain=settings.DOMAIN_NAME,
        )

        return AuthToken(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/signout/")
def signout(response: Response):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=settings.PROTOCOL == "https",
        samesite="none" if settings.PROTOCOL == "https" else "lax",
        domain=settings.DOMAIN_NAME,
    )
    return {"message": "User successfully signed out."}


@router.get("/me/")
def get_current_user(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user_id: Annotated[uuid.UUID, Depends(auth.get_current_user_id)],
) -> UserResponse:
    try:
        user = presenter.get_user(user_id=user_id, session=session)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
