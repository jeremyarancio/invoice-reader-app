
def test_submit_invoice(
    upload_files,
    client: TestClient,
    s3_mocker: Mock,
    invoice_data: InvoiceCreate,
    session: Session,
    user: User,
    auth_token: AuthToken,
    client_id: str,
):
    data = json.dumps(
        {
            "invoice": json.loads(
                invoice_data.model_dump_json()
            ),  # Workaround because date not JSON serializable
            "client_id": client_id,
        }
    )
    response = client.post(
        url="/api/v1/invoices/submit",
        data={"data": data},
        files=upload_files,
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    invoice_data_from_db = session.exec(
        select(models.InvoiceModel).where(models.InvoiceModel.user_id == user.user_id)
    ).one_or_none()

    assert response.status_code == 200
    assert invoice_data_from_db is not None
    s3_mocker.upload_fileobj.assert_called_once()
    assert (
        invoice_data_from_db.amount_excluding_tax == invoice_data.amount_excluding_tax
    )
    assert invoice_data_from_db.invoice_number == invoice_data.invoice_number
    assert invoice_data_from_db.invoiced_date == invoice_data.invoiced_date
    assert invoice_data_from_db.uploaded_date is not None


def test_submit_invoice_with_wrong_format(
    wrong_files,
    client: TestClient,
    s3_mocker: Mock,
    auth_token: AuthToken,
):
    response = client.post(
        url="/api/v1/invoices/submit",
        files=wrong_files,
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    assert response.status_code == 422
    s3_mocker.assert_not_called()


def test_get_invoice(
    client: TestClient,
    auth_token: AuthToken,
    user: User,
    invoice_models: list[InvoiceModel],
    session: Session,
):
    invoice_model = invoice_models[0]
    response = client.get(
        url=f"/api/v1/invoices/{invoice_model.file_id}",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    payload = InvoiceResponse.model_validate(response.json())
    assert response.status_code == 200
    assert payload.file_id == invoice_model.file_id
    assert payload.s3_path == invoice_model.s3_path
    assert payload.data.invoice_number == invoice_model.invoice_number


def test_get_invoices(
    client: TestClient,
    auth_token: AuthToken,
    user: User,
    invoice_models: list[InvoiceModel],
    session: Session,
):
    PAGE = 1
    PER_PAGE = 2
    response = client.get(
        url="/api/v1/invoices/",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
        params={"page": PAGE, "per_page": PER_PAGE},
    )
    payload = PagedInvoiceResponse.model_validate(response.json())
    assert response.status_code == 200
    assert len(payload.data) == PER_PAGE
    assert payload.total == len(invoice_models)
    assert all(item.data.invoice_number for item in payload.data)
