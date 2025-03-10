from typing import Annotated

import sqlmodel
from fastapi import APIRouter, Depends, Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from invoice_reader import db, presenter
from invoice_reader.app import auth
from invoice_reader.schemas import AuthToken, User, UserCreate

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post("/signup/")
def signup(
    user: UserCreate, session: Annotated[sqlmodel.Session, Depends(db.get_session)]
):
    auth.register_user(user=user, session=session)
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
    user: Annotated[User, Depends(auth.get_current_user)],
) -> None:
    try:
        presenter.delete_user(user_id=user.user_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
