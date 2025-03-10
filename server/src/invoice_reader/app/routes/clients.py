import uuid
from typing import Annotated

import sqlmodel
from fastapi import APIRouter, Depends, Query, Response
from fastapi.exceptions import HTTPException

from invoice_reader import db, presenter, settings
from invoice_reader.app import auth
from invoice_reader.schemas import Client, PagedClientGetResponse, User
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger()

router = APIRouter(
    prefix="/api/v1/clients",
    tags=["Clients"],
)


@router.get("/")
def get_clients(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
    page: int = Query(1, ge=1),
    per_page: int = Query(settings.PER_PAGE, ge=1),
) -> PagedClientGetResponse:
    try:
        paged_client_response = presenter.get_paged_clients(
            user=user,
            session=session,
            page=page,
            per_page=per_page,
        )
        return paged_client_response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e


@router.post("/")
def add_client(
    client: Client,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> Response:
    try:
        LOGGER.info(f"Adding client for user: {user.email}")
        presenter.add_client(user=user, client=client, session=session)
        return Response(
            content="New client added to the database.",
            status_code=201,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{client_id}")
def delete_client(
    client_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> None:
    try:
        presenter.delete_client(
            client_id=client_id, user_id=user.user_id, session=session
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
