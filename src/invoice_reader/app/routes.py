import uuid
from typing import Annotated

import sqlmodel
from fastapi import Depends, FastAPI, File, Form, Query, Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ValidationError

from invoice_reader import db, presenter, settings
from invoice_reader.app import auth
from invoice_reader.schemas import (
    AuthToken,
    InvoiceData,
    InvoiceResponse,
    PagedInvoiceResponse,
    User,
    UserCreate,
)
from invoice_reader.utils import logger

LOGGER = logger.get_logger(__name__)


app = FastAPI()


class Checker:
    """When POST File & Payload, HTTP sends a Form request.
    However, HTTP protocole doesn't allow file & body.
    Therefore, we send data as Form as `{"data": json_dumps(invoice_data)} along with the file.

    More information here:
    https://shorturl.at/Beaur
    """

    def __init__(self, model: BaseModel):
        self.model = model

    def __call__(self, data: str = Form(None)):
        if data:
            try:
                return self.model.model_validate_json(data)
            except ValidationError as e:
                raise HTTPException(
                    detail=jsonable_encoder(e.errors()),
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )


@app.get("/")
async def root():
    return {"message": "Welcome to the Invoice Reader API!"}


@app.post("/api/v1/files/submit")
def submit(
    upload_file: Annotated[UploadFile, File()],
    invoice_data: Annotated[InvoiceData | None, Depends(Checker(InvoiceData))],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
):
    if upload_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only PDF files are allowed.",
        )
    try:
        if invoice_data:
            presenter.submit(
                user_id=user.user_id,
                file=upload_file.file,
                filename=upload_file.filename,
                invoice_data=invoice_data,
                session=session,
            )
            return Response(
                content="The file and its information were successfully stored.",
                status_code=200,
            )
        extracted_metadata = presenter.extract(file=upload_file.file)
        return Response(
            content={"data": extracted_metadata},
            status_code=200,
        )
    except Exception as e:
        LOGGER.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/files/{file_id}")
def get_file(
    file_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> InvoiceResponse:
    try:
        invoice = presenter.get_invoice(user=user, file_id=file_id, session=session)
        return invoice
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


@app.get("/api/v1/files/")
def get_files(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
    page: int = Query(1, ge=1),
    per_page: int = Query(settings.PER_PAGE, ge=1),
) -> PagedInvoiceResponse:
    try:
        paged_invoices = presenter.get_paged_invoices(
            user=user, session=session, page=page, per_page=per_page
        )
        return paged_invoices
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


@app.post("/api/v1/users/register/")
def register(user: UserCreate, session: sqlmodel.Session = Depends(db.get_session)):
    auth.register_user(user=user, session=session)
    return Response(content="User has been added to the database.", status_code=200)


@app.post("/api/v1/users/login/")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
) -> AuthToken:
    try:
        user = auth.authenticate_user(
            username=form_data.username, password=form_data.password, session=session
        )
        access_token = auth.create_access_token(username=user.username)
    except Exception as e:
        LOGGER.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthToken(access_token=access_token, token_type="bearer")
