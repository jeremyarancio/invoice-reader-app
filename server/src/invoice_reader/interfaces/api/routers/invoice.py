from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ValidationError

from invoice_reader.domain.invoice import InvoiceData
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.exchange_rates_service import get_exchange_rates_service
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
from invoice_reader.services.interfaces.exchange_rates import IExchangeRatesService
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


@router.post("")
def add_invoice(
    upload_file: Annotated[UploadFile, File()],
    data: Annotated[
        InvoiceCreate,
        Depends(Checker(InvoiceCreate)),
    ],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    file_repository: Annotated[IFileRepository, Depends(get_file_repository)],
    invoice_repository: Annotated[IInvoiceRepository, Depends(get_invoice_repository)],
    exchange_rate_service: Annotated[IExchangeRatesService, Depends(get_exchange_rates_service)],
):
    invoice_data = InvoiceData(
        invoice_number=data.data.invoice_number,
        vat=data.data.vat,
        description=data.data.description,
        issued_date=data.data.issued_date,
        paid_date=data.data.paid_date,
    )
    InvoiceService.add_invoice(
        user_id=user_id,
        client_id=data.client_id,
        file_bin=upload_file.file,
        filename=upload_file.filename if upload_file.filename else "",
        gross_amount=data.data.gross_amount,
        currency=data.data.currency,
        invoice_data=invoice_data,
        file_repository=file_repository,
        invoice_repository=invoice_repository,
        exchange_rate_service=exchange_rate_service,
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


@router.get("")
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
    exchange_rate_service: Annotated[IExchangeRatesService, Depends(get_exchange_rates_service)],
) -> Response:
    InvoiceService.update_invoice(
        user_id=user_id,
        invoice_id=invoice_id,
        update_client_id=invoice_update.client_id,
        update_invoice_data=invoice_update.data,
        updated_currency=invoice_update.data.currency,
        updated_gross_amount=invoice_update.data.gross_amount,
        invoice_repository=invoice_repository,
        exchange_rate_service=exchange_rate_service,
    )
    return Response(status_code=204)


@router.get("/{invoice_id}/url", dependencies=[Depends(get_current_user_id)])
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
