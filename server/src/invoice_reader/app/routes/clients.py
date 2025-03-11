import uuid
from typing import Annotated

import sqlmodel
from fastapi import APIRouter, Depends, Query, Response
from fastapi.exceptions import HTTPException

from invoice_reader import db, presenter, settings
from invoice_reader.app import auth
from invoice_reader.schemas import client_schema
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger()

router = APIRouter(
    prefix="/api/v1/clients",
    tags=["Clients"],
)


@router.get("/")
def get_clients(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user_id: Annotated[uuid.UUID, Depends(auth.get_current_user_id)],
    page: int = Query(1, ge=1),
    per_page: int = Query(settings.PER_PAGE, ge=1),
) -> client_schema.PagedClientResponse:
    try:
        paged_client_response = presenter.get_paged_clients(
            user_id=user_id,
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


@router.get("/{client_id}")
def get_client(
    client_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user_id: Annotated[uuid.UUID, Depends(auth.get_current_user_id)],
) -> client_schema.ClientResponse:
    try:
        client = presenter.get_client(
            user_id=user_id, client_id=client_id, session=session
        )
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Uncaught exception {str(e)}"
        ) from e


@router.post("/")
def add_client(
    client_create: client_schema.ClientCreate,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user_id: Annotated[uuid.UUID, Depends(auth.get_current_user_id)],
) -> Response:
    try:
        presenter.add_client(
            user_id=user_id, client_create=client_create, session=session
        )
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
    user_id: Annotated[uuid.UUID, Depends(auth.get_current_user_id)],
) -> Response:
    try:
        presenter.delete_client(client_id=client_id, user_id=user_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return Response(content="Client successfully deleted.", status_code=204)
