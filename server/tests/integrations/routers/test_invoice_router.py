from typing import Any

import pytest
from fastapi.testclient import TestClient

from invoice_reader.domain.invoice import Invoice, InvoiceUpdate
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.file import InMemoryFileRepository
from invoice_reader.interfaces.api.main import app
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.infrastructure.parser import TestParser
from invoice_reader.interfaces.schemas.invoice import InvoiceCreate, InvoiceResponse
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.parser import get_parser
from invoice_reader.interfaces.dependencies.repository import (
    get_file_repository,
    get_invoice_repository,
)


def _test_get_invoice_repository():
    return InMemoryInvoiceRepository()


def create_test_get_current_user_id(user: User):
    def _test_get_current_user_id():
        return user.id_

    return _test_get_current_user_id


def _test_get_parser():
    return TestParser()


def _test_get_file_repository():
    return InMemoryFileRepository()


@pytest.fixture
def test_client(user: User):
    client = TestClient(app)
    app.dependency_overrides[get_invoice_repository] = _test_get_invoice_repository
    app.dependency_overrides[get_parser] = _test_get_parser
    app.dependency_overrides[get_current_user_id] = create_test_get_current_user_id(user=user)
    app.dependency_overrides[get_file_repository] = _test_get_file_repository
    yield client
    app.dependency_overrides.clear()


def test_add_invoice(test_client: TestClient, upload_files: Any, invoice_create: InvoiceCreate):
    response = test_client.post(
        "/v1/invoices/",
        files=upload_files,
        data={"data": invoice_create.model_dump_json()},
    )
    assert response.status_code == 201


def test_add_exisiting_invoice(
    test_client: TestClient,
    upload_files: Any,
    invoice_create: InvoiceCreate,
    existing_invoice: Invoice,
):
    response = test_client.post(
        "/v1/invoices/", files=upload_files, data={"data": invoice_create.model_dump_json()}
    )
    assert response.status_code == 409


def test_get_invoice(test_client: TestClient, existing_invoice: Invoice):
    response = test_client.get(f"/v1/invoices/{existing_invoice.id_}")
    invoice_response = InvoiceResponse.model_validate(response.json())
    assert response.status_code == 200
    assert invoice_response.invoice_id == existing_invoice.id_
    assert invoice_response.data.invoice_number == existing_invoice.invoice_number


# TODO: Get invoices


def test_update_invoice(
    test_client: TestClient, invoice_update: InvoiceUpdate, existing_invoice: Invoice
):
    response = test_client.put(
        f"/v1/invoices/{existing_invoice.id_}",
        data=invoice_update.model_dump_json(),  # type: ignore
    )
    assert response.status_code == 204
    updated_invoice = InMemoryInvoiceRepository().get(invoice_id=existing_invoice.id_)
    assert updated_invoice is not None
    assert updated_invoice.gross_amount == invoice_update.gross_amount
    assert updated_invoice.vat == invoice_update.vat
    assert updated_invoice.description == invoice_update.description


def test_update_invoice_with_existing_invoice_number(
    test_client: TestClient, invoice_update: InvoiceUpdate, existing_invoice: Invoice
):
    # TODO: Store several invoices to test update 409
    response = test_client.put(
        f"/v1/invoices/{existing_invoice.id_}",
        data=invoice_update.model_dump_json(),  # type: ignore
    )
    assert response.status_code == 409


def test_delete_invoice(test_client: TestClient, existing_invoice: Invoice):
    response = test_client.delete(f"/v1/invoices/{existing_invoice.id_}")
    assert response.status_code == 204
    deleted_invoice = InMemoryInvoiceRepository().get(invoice_id=existing_invoice.id_)
    assert deleted_invoice is None
