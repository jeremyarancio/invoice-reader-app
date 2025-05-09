import uuid
from typing import Annotated

import sqlmodel
from fastapi import APIRouter, Depends, Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from invoice_reader import db, presenter
from invoice_reader.app import auth
from invoice_reader.schemas import AuthToken, UserCreate

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
) -> AuthToken:
    try:
        user = auth.authenticate_user(
            email=form_data.username, password=form_data.password, session=session
        )
        access_token = auth.create_access_token(email=user.email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return AuthToken(access_token=access_token, token_type="bearer")


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


@router.get("/refresh/")
def refresh_token(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    token: Annotated[str, Depends(auth.oauth2_scheme)],
) -> AuthToken:
    try:
        email = auth.get_email_from_expired_token(token=token)
        access_token = auth.refresh_token(email=email, session=session)
        return AuthToken(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
