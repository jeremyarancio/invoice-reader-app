from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from invoice_reader.mappers.invoices import InvoiceMapper
from invoice_reader.models import CurrencyModel, InvoiceModel, UserModel
from invoice_reader.repository import InvoiceRepository
from invoice_reader.schemas import AuthToken, FileData
from invoice_reader.schemas.invoices import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceUpdate,
    PagedInvoiceResponse,
)
from invoice_reader.schemas.users import User

from ..utils import assert_status_code

PAGE = 1
PER_PAGE = 2


def test_submit_invoice(
    upload_files,
    api_client: TestClient,
    s3_mocker: Mock,
    new_invoice_create: InvoiceCreate,
    auth_token: AuthToken,
    existing_user: User,
    invoice_repository: InvoiceRepository,
):
    data = new_invoice_create.model_dump_json()
    response = api_client.post(
        url="/api/v1/invoices/",
        data={"data": data},
        files=upload_files,
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )

    assert_status_code(response, 201)

    invoice_model = invoice_repository.get_by_invoice_number(
        new_invoice_create.invoice.invoice_number,
        user_id=existing_user.user_id,
    )
    s3_mocker.upload_fileobj.assert_called_once()
    assert invoice_model.invoice_number == new_invoice_create.invoice.invoice_number


def test_submit_exisiting_invoice(
    upload_files,
    api_client: TestClient,
    s3_mocker: Mock,
    existing_invoice_create: InvoiceCreate,
    auth_token: AuthToken,
    test_existing_invoice: InvoiceModel,
):
    data = existing_invoice_create.model_dump_json()
    response = api_client.post(
        url="/api/v1/invoices/",
        data={"data": data},
        files=upload_files,
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert_status_code(response, 409)
    s3_mocker.upload_fileobj.assert_not_called()


@pytest.mark.parametrize(
    "wrong_files",
    [
        ("wrong_filename", "application/json"),
        ("upload_file", "image/jpeg"),
    ],
    indirect=True,
)
def test_submit_invoice_with_wrong_format(
    wrong_files,
    api_client: TestClient,
    s3_mocker: Mock,
    auth_token: AuthToken,
):
    response = api_client.post(
        url="/api/v1/invoices/",
        files=wrong_files,
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert_status_code(response, 422)
    s3_mocker.assert_not_called()


def test_get_invoice(
    file_data: FileData,
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_invoice: InvoiceModel,
    test_existing_currency: CurrencyModel,
):
    response = api_client.get(
        url=f"/api/v1/invoices/{file_data.file_id}",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert_status_code(response, 200)

    payload = InvoiceResponse.model_validate(response.json())
    assert payload.invoice_id == test_existing_invoice.file_id
    assert payload.s3_path == test_existing_invoice.s3_path
    assert payload.data.invoice_number == test_existing_invoice.invoice_number
    assert payload.currency_id == test_existing_currency.id


def test_get_invoices(
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_invoices: list[InvoiceModel],
):
    response = api_client.get(
        url="/api/v1/invoices/",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
        params={"page": PAGE, "per_page": PER_PAGE},
    )
    assert_status_code(response, 200)

    paged_invoices = PagedInvoiceResponse.model_validate(response.json())
    assert len(paged_invoices.data) == PER_PAGE
    assert paged_invoices.total == 3
    assert (
        test_existing_invoices[0].invoice_number
        == paged_invoices.data[0].data.invoice_number
    )


def test_submit_invoice_unauthorized(
    upload_files,
    api_client: TestClient,
    new_invoice_create: InvoiceCreate,
):
    data = new_invoice_create.model_dump_json()
    response = api_client.post(
        url="/api/v1/invoices/",
        data={"data": data},
        files=upload_files,
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert_status_code(response, 401)


def test_delete_invoice(
    api_client: TestClient,
    test_existing_invoice: InvoiceModel,
    auth_token: AuthToken,
    existing_user: User,
    invoice_repository: InvoiceRepository,
    s3_mocker: Mock,
):
    response = api_client.delete(
        url=f"/api/v1/invoices/{test_existing_invoice.file_id}",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert_status_code(response, 204)

    invoice = invoice_repository.get_by_invoice_number(
        invoice_number=test_existing_invoice.invoice_number,
        user_id=existing_user.user_id,
    )
    assert not invoice
    s3_mocker.delete_object.assert_called_once()


def test_update_invoice(
    api_client: TestClient,
    test_existing_invoice: InvoiceModel,
    auth_token: AuthToken,
    invoice_repository: InvoiceRepository,
):
    updated_invoice = InvoiceUpdate.model_validate(
        InvoiceMapper.map_invoice_model_to_invoice(test_existing_invoice).model_dump()
    )
    updated_invoice.invoice_number = "number1234"
    updated_invoice.description = "Updated description"
    updated_invoice.gross_amount = 1234

    response = api_client.put(
        url=f"/api/v1/invoices/{test_existing_invoice.file_id}",
        data=updated_invoice.model_dump_json(),
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )

    assert_status_code(response, 204)

    invoice_model = invoice_repository.get(
        file_id=test_existing_invoice.file_id, user_id=test_existing_invoice.user_id
    )
    assert invoice_model
    assert invoice_model.invoice_number == updated_invoice.invoice_number
    assert invoice_model.amount_excluding_tax == 1234
    assert invoice_model.description == "Updated description"


def test_update_existing_invoice_number(
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_invoices: list[InvoiceModel],
):
    updated_invoice = InvoiceUpdate.model_validate(
        InvoiceMapper.map_invoice_model_to_invoice(
            test_existing_invoices[0]
        ).model_dump()
    )
    updated_invoice.invoice_number = test_existing_invoices[1].invoice_number
    updated_invoice.description = "Updated description"
    updated_invoice.gross_amount = 1234

    response = api_client.put(
        url=f"/api/v1/invoices/{test_existing_invoices[0].file_id}",
        data=updated_invoice.model_dump_json(),
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert_status_code(response, 409)


def test_update_invoice_unchanged(
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_invoices: list[InvoiceModel],
):
    "In case there's no change, we want to avoid conflict."
    updated_invoice = InvoiceUpdate.model_validate(
        InvoiceMapper.map_invoice_model_to_invoice(
            test_existing_invoices[0]
        ).model_dump()
    )

    response = api_client.put(
        url=f"/api/v1/invoices/{test_existing_invoices[0].file_id}",
        data=updated_invoice.model_dump_json(),
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert_status_code(response, 204)


def test_get_invoice_url(
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_invoice: InvoiceModel,
    s3_mocker: Mock,
):
    s3_mocker.generate_presigned_url.return_value = "http://presigned/url"
    response = api_client.get(
        url=f"/api/v1/invoices/{test_existing_invoice.file_id}/url/",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert_status_code(response, 200)
    s3_mocker.generate_presigned_url.assert_called_once()
