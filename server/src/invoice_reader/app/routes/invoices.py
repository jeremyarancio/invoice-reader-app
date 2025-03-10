import uuid
from typing import Annotated

import sqlmodel
from fastapi import APIRouter, Depends, File, Form, Query, Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ValidationError

from invoice_reader import db, presenter, settings
from invoice_reader.app import auth
from invoice_reader.schemas import invoice_schema, user_schema

router = APIRouter(
    prefix="/api/v1/invoices",
    tags=["Invoices"],
)


class Checker:
    """When POST File & Payload, HTTP sends a Form request.
    However, HTTP protocole doesn't allow file & body.
    Therefore, we send data as Form as `{"data": json_dumps(invoice_data)}
    along with the file.

    More information here:
    https://shorturl.at/Beaur
    """

    def __init__(self, model: "BaseModel"):
        self.model = model

    def __call__(self, data: str = Form(None)):
        if data:
            try:
                return self.model.model_validate_json(data)
            except ValidationError as e:
                raise HTTPException(
                    detail=jsonable_encoder(e.errors()),
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                ) from e


@router.post("/")
def add_invoice(
    upload_file: Annotated[UploadFile, File()],
    data: Annotated[
        invoice_schema.InvoiceCreate | None,
        Depends(Checker(invoice_schema.InvoiceCreate)),
    ],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[user_schema.User, Depends(auth.get_current_user)],
):
    if upload_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only PDF files are allowed for now.",
        )
    try:
        if data:
            presenter.submit_invoice(
                user_id=user.user_id,
                file=upload_file.file,
                filename=upload_file.filename,
                invoice_data=data,
                session=session,
            )
            return Response(
                content="The file and its information were successfully stored.",
                status_code=201,
            )
        # extracted_metadata = presenter.extract(file=upload_file.file)
        # return Response(
        #     content={"data": extracted_metadata},
        #     status_code=201,
        # )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{file_id}")
def get_invoice(
    file_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[user_schema.User, Depends(auth.get_current_user)],
) -> invoice_schema.InvoiceGetResponse:
    try:
        invoice = presenter.get_invoice(user=user, file_id=file_id, session=session)
        return invoice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Uncaught exception {str(e)}"
        ) from e


@router.get("/")
def get_invoices(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[user_schema.User, Depends(auth.get_current_user)],
    page: int = Query(1, ge=1),
    per_page: int = Query(settings.PER_PAGE, ge=1),
) -> invoice_schema.PagedInvoiceGetResponse:
    try:
        paged_invoices = presenter.get_paged_invoices(
            user=user, session=session, page=page, per_page=per_page
        )
        return paged_invoices
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{file_id}")
def delete_invoice(
    file_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[user_schema.User, Depends(auth.get_current_user)],
) -> None:
    try:
        presenter.delete_invoice(file_id=file_id, user_id=user.user_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/{invoice_id}")
def update_invoice(
    invoice_id: uuid.UUID,
    invoice: invoice_schema.Invoice,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[user_schema.User, Depends(auth.get_current_user)],
) -> None:
    try:
        presenter.update_invoice(
            invoice_id=invoice_id, invoice=invoice, session=session
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{invoice_id}/url/")
def get_invoice_url(
    invoice_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[user_schema.User, Depends(auth.get_current_user)],
) -> str:
    try:
        url = presenter.get_invoice_url(
            invoice_id=invoice_id,
            user_id=user.user_id,
            session=session,
        )
        return url
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
