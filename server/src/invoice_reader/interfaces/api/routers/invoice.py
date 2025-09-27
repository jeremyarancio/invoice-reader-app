from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ValidationError

from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.parser import get_parser
from invoice_reader.interfaces.dependencies.repository import (
    get_client_repository,
    get_file_repository,
    get_invoice_repository,
)
from invoice_reader.interfaces.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceUpdate,
    PagedInvoiceResponse,
)
from invoice_reader.interfaces.schemas.parser import ParserResponse
from invoice_reader.services.interfaces.parser import IParser
from invoice_reader.services.interfaces.repositories import (
    IFileRepository,
    IInvoiceRepository,
)
from invoice_reader.services.interfaces.repositories.client import IClientRepository
from invoice_reader.services.invoice import InvoiceService

router = APIRouter(
    prefix="/v1/invoices",
    tags=["Invoices"],
)


class Checker[T: BaseModel]:
    """When POST File & Payload, HTTP sends a Form request.
    However, HTTP protocol doesn't allow file & body.
    Therefore, we send data as Form as `{"data": json_dumps(invoice_data)}
    along with the file.
    """

    def __init__(self, model: type[T]):
        self.model = model

    def __call__(self, data: str = Form(None)) -> T:
        if data:
            try:
                return self.model.model_validate_json(data)
            except ValidationError as e:
                raise HTTPException(
                    detail=jsonable_encoder(e.errors()),
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                ) from e
        raise HTTPException(
            detail="Data payload is required.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.post("/")
def add_invoice(
    upload_file: Annotated[UploadFile, File()],
    data: Annotated[
        InvoiceCreate,
        Depends(Checker(InvoiceCreate)),
    ],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    file_repository: Annotated[IFileRepository, Depends(get_file_repository)],
    invoice_repository: Annotated[IInvoiceRepository, Depends(get_invoice_repository)],
):
    InvoiceService.add_invoice(
        user_id=user_id,
        client_id=data.client_id,
        invoice_data=data.data,
        file_bin=upload_file.file,
        filename=upload_file.filename if upload_file.filename else "",
        file_repository=file_repository,
        invoice_repository=invoice_repository,
    )
    return Response(
        content="The file and its information were successfully stored.",
        status_code=201,
    )


@router.post("/parse")
def parse_invoice(
    upload_file: Annotated[UploadFile, File()],
    parser: Annotated[IParser, Depends(get_parser)],
    client_repository: Annotated[IClientRepository, Depends(get_client_repository)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> ParserResponse:
    invoice_data, client = InvoiceService.parse_invoice(
        file=upload_file.file,
        parser=parser,
        client_repository=client_repository,
        user_id=user_id,
    )
    return ParserResponse(invoice=invoice_data, client_id=client.id_ if client else None)


@router.get("/{invoice_id}", dependencies=[Depends(get_current_user_id)])
def get_invoice(
    invoice_id: UUID,
    invoice_repository: Annotated[IInvoiceRepository, Depends(get_invoice_repository)],
) -> InvoiceResponse:
    invoice = InvoiceService.get_invoice(
        invoice_id=invoice_id, invoice_repository=invoice_repository
    )
    return InvoiceResponse.from_invoice(invoice)


@router.get("/")
def get_invoices(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    invoice_repository: Annotated[IInvoiceRepository, Depends(get_invoice_repository)],
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1),
) -> PagedInvoiceResponse:
    paged_invoices = InvoiceService.get_paged_invoices(
        user_id=user_id,
        invoice_repository=invoice_repository,
        page=page,
        per_page=per_page,
    )
    return PagedInvoiceResponse(
        page=page,
        per_page=per_page,
        total=len(paged_invoices),
        invoices=[InvoiceResponse.from_invoice(invoice) for invoice in paged_invoices],
    )


@router.delete("/{invoice_id}", dependencies=[Depends(get_current_user_id)])
def delete_invoice(
    invoice_id: UUID,
    invoice_repository: Annotated[IInvoiceRepository, Depends(get_invoice_repository)],
    file_repository: Annotated[IFileRepository, Depends(get_file_repository)],
) -> Response:
    InvoiceService.delete_invoice(
        invoice_id=invoice_id,
        invoice_repository=invoice_repository,
        file_repository=file_repository,
    )
    return Response(status_code=204)


@router.put("/{invoice_id}")
def update_invoice(
    invoice_id: UUID,
    invoice_update: InvoiceUpdate,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    invoice_repository: Annotated[IInvoiceRepository, Depends(get_invoice_repository)],
) -> Response:
    InvoiceService.update_invoice(
        user_id=user_id,
        invoice_id=invoice_id,
        update_client_id=invoice_update.client_id,
        update_invoice_data=invoice_update.data,
        invoice_repository=invoice_repository,
    )
    return Response(status_code=204)


@router.get("/{invoice_id}/url/", dependencies=[Depends(get_current_user_id)])
def get_invoice_url(
    invoice_id: UUID,
    file_repository: Annotated[IFileRepository, Depends(get_file_repository)],
    invoice_repository: Annotated[IInvoiceRepository, Depends(get_invoice_repository)],
) -> str:
    url = InvoiceService.get_invoice_url(
        invoice_id=invoice_id,
        file_repository=file_repository,
        invoice_repository=invoice_repository,
    )
    return url
