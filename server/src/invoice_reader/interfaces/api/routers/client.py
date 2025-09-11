from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response

from invoice_reader.domain.client import ClientBase, ClientID, ClientUpdate
from invoice_reader.domain.user import UserID
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.infrastructure import get_client_repository
from invoice_reader.interfaces.schemas.client import (
    ClientCreate,
    ClientResponse,
    PagedClientResponse,
)
from invoice_reader.services.client import ClientService
from invoice_reader.services.interfaces.repositories import IClientRepository

router = APIRouter(
    prefix="/v1/clients",
    tags=["Clients"],
)


@router.get("/")
def get_clients(
    user_id: Annotated[UserID, Depends(get_current_user_id)],
    client_repository: Annotated[IClientRepository, Depends(get_client_repository)],
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
) -> PagedClientResponse:
    clients = ClientService.get_paged_clients(
        user_id=user_id,
        client_repository=client_repository,
        page=page,
        per_page=per_page,
    )
    return PagedClientResponse(
        total=len(clients),
        page=page,
        per_page=per_page,
        data=[
            ClientResponse(
                client_name=client.client_name,
                city=client.city,
                country=client.country,
                street_address=client.street_address,
                street_number=client.street_number,
                zipcode=client.zipcode,
            )
            for client in clients
        ],
    )


@router.get("/{client_id}", dependencies=[Depends(get_current_user_id)])
def get_client(
    client_id: ClientID,
    client_repository: Annotated[IClientRepository, Depends(get_client_repository)],
) -> ClientResponse:
    client = ClientService.get_client(client_id=client_id, client_repository=client_repository)
    return ClientResponse(
        client_name=client.client_name,
        city=client.city,
        country=client.country,
        street_address=client.street_address,
        street_number=client.street_number,
        zipcode=client.zipcode,
    )


@router.post("/")
def add_client(
    client_create: ClientCreate,
    user_id: Annotated[UserID, Depends(get_current_user_id)],
    client_repository: Annotated[IClientRepository, Depends(get_client_repository)],
) -> Response:
    client_data = ClientBase(
        client_name=client_create.client_name,
        street_number=client_create.street_number,
        street_address=client_create.street_address,
        zipcode=client_create.zipcode,
        city=client_create.city,
        country=client_create.country,
    )
    ClientService.add_client(
        user_id=user_id, client_data=client_data, client_repository=client_repository
    )
    return Response(
        content="New client added to the database.",
        status_code=201,
    )


@router.delete("/{client_id}", dependencies=[Depends(get_current_user_id)])
def delete_client(
    client_id: ClientID,
    client_repository: Annotated[IClientRepository, Depends(get_client_repository)],
) -> Response:
    ClientService.delete_client(client_id=client_id, client_repository=client_repository)
    return Response(status_code=204)


@router.put("/{client_id}")
def update_client(
    client_id: ClientID,
    client_update: ClientUpdate,
    user_id: Annotated[UserID, Depends(get_current_user_id)],
    client_repository: Annotated[IClientRepository, Depends(get_client_repository)],
) -> Response:
    ClientService.update_client(
        user_id=user_id,
        client_id=client_id,
        client_update=client_update,
        client_repository=client_repository,
    )
    return Response(status_code=204)
