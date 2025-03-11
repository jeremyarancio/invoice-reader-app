from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from invoice_reader.models import InvoiceModel, UserModel
from invoice_reader.repository import InvoiceRepository
from invoice_reader.schemas import (
    AuthToken,
    FileData,
    invoice_schema,
)

PAGE = 1
PER_PAGE = 2


def test_submit_invoice(
    upload_files,
    api_client: TestClient,
    s3_mocker: Mock,
    new_invoice_create: invoice_schema.InvoiceCreate,
    auth_token: AuthToken,
    invoice_repository: InvoiceRepository,
):
    data = new_invoice_create.model_dump_json()
    response = api_client.post(
        url="/api/v1/invoices/",
        data={"data": data},
        files=upload_files,
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )

    invoice = invoice_repository.get_by_invoice_number(
        new_invoice_create.invoice.invoice_number
    )

    assert response.status_code == 201
    s3_mocker.upload_fileobj.assert_called_once()
    assert invoice.invoice_number == new_invoice_create.invoice.invoice_number


def test_submit_exisiting_invoice(
    upload_files,
    api_client: TestClient,
    s3_mocker: Mock,
    existing_invoice_create: invoice_schema.InvoiceCreate,
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
    assert response.status_code == 409
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
    assert response.status_code == 422
    s3_mocker.assert_not_called()


def test_get_invoice(
    file_data: FileData,
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_invoice: InvoiceModel,
):
    response = api_client.get(
        url=f"/api/v1/invoices/{file_data.file_id}",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    payload = invoice_schema.InvoiceResponse.model_validate(response.json())
    assert response.status_code == 200
    assert payload.invoice_id == test_existing_invoice.file_id
    assert payload.s3_path == test_existing_invoice.s3_path
    assert payload.data.invoice_number == test_existing_invoice.invoice_number


def test_get_invoices(
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_invoices: list[InvoiceModel],
    test_existing_user: UserModel,
):
    response = api_client.get(
        url="/api/v1/invoices/",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
        params={"page": PAGE, "per_page": PER_PAGE},
    )
    paged_invoices = invoice_schema.PagedInvoiceResponse.model_validate(response.json())

    assert response.status_code == 200
    assert len(paged_invoices.data) == PER_PAGE
    assert paged_invoices.total == 3
    assert (
        test_existing_invoices[0].invoice_number
        == paged_invoices.data[0].data.invoice_number
    )


def test_submit_invoice_unauthorized(
    upload_files,
    api_client: TestClient,
    new_invoice_create: invoice_schema.InvoiceCreate,
):
    data = new_invoice_create.model_dump_json()
    response = api_client.post(
        url="/api/v1/invoices/",
        data={"data": data},
        files=upload_files,
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401


def test_delete_invoice(
    api_client: TestClient,
    test_existing_invoice: InvoiceModel,
    auth_token: AuthToken,
    invoice_repository: InvoiceRepository,
    s3_mocker: Mock,
):
    response = api_client.delete(
        url=f"/api/v1/invoices/{test_existing_invoice.file_id}",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    invoice = invoice_repository.get_by_invoice_number(
        invoice_number=test_existing_invoice.invoice_number
    )
    assert response.status_code == 204
    assert not invoice
    s3_mocker.delete_object.assert_called_once()


def test_update_invoice(
    api_client: TestClient,
    test_existing_user: UserModel,
    test_existing_invoice: InvoiceModel,
    auth_token: AuthToken,
    invoice_repository: InvoiceRepository,
):
    updated_invoice = invoice_schema.InvoiceUpdate.model_validate(
        test_existing_invoice.model_dump()
    )
    updated_invoice.invoice_number = "number1234"
    updated_invoice.amount_excluding_tax = 1234

    response = api_client.put(
        url=f"/api/v1/invoices/{test_existing_invoice.file_id}",
        data=updated_invoice.model_dump_json(),
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )

    invoice_model = invoice_repository.get(
        file_id=test_existing_invoice.file_id, user_id=test_existing_user.user_id
    )
    assert invoice_model
    assert response.status_code == 200
    assert invoice_model.invoice_number == updated_invoice.invoice_number
    assert invoice_model.amount_excluding_tax == 1234


# Add exception no change update


def test_get_invoice_url(
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_invoice: InvoiceModel,
    s3_mocker: Mock,
):
    s3_mocker.generate_presigned_url.return_value = "http://presigned/url"
    response = api_client.get(
        url=f"/api/v1/invoices/{test_existing_invoice.file_id}/url/",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    assert response.status_code == 200
    s3_mocker.generate_presigned_url.assert_called_once()
