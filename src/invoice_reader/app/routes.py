import uuid
from typing import Annotated

import sqlmodel
from fastapi import Depends, FastAPI, File, Form, Query, Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ValidationError

from invoice_reader import db, presenter, settings
from invoice_reader.app import auth
from invoice_reader.schemas import (
    AuthToken,
    Client,
    Invoice,
    InvoiceCreate,
    InvoiceGetResponse,
    PagedClientGetResponse,
    PagedInvoiceGetResponse,
    User,
    UserCreate,
)
from invoice_reader.utils import logger

LOGGER = logger.get_logger(__name__)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONT_END_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
                ) from e


@app.get("/")
async def root():
    return {"message": "Welcome to the Invoice Reader API!"}


@app.post("/api/v1/invoices/submit")
def submit(
    upload_file: Annotated[UploadFile, File()],
    data: Annotated[Invoice | None, Depends(Checker(InvoiceCreate))],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
):
    if upload_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only PDF files are allowed.",
        )
    try:
        if data:
            presenter.submit(
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
        extracted_metadata = presenter.extract(file=upload_file.file)
        return Response(
            content={"data": extracted_metadata},
            status_code=201,
        )
    except HTTPException as e:
        LOGGER.error(e)
        raise e
    except Exception as e:
        LOGGER.error(e)
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/v1/invoices/{file_id}")
def get_invoice(
    file_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> InvoiceGetResponse:
    try:
        invoice = presenter.get_invoice(user=user, file_id=file_id, session=session)
        return invoice
    except HTTPException as e:
        LOGGER.error(e)
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e


@app.get("/api/v1/invoices/")
def get_invoices(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
    page: int = Query(1, ge=1),
    per_page: int = Query(settings.PER_PAGE, ge=1),
) -> PagedInvoiceGetResponse:
    try:
        paged_invoices = presenter.get_paged_invoices(
            user=user, session=session, page=page, per_page=per_page
        )
        return paged_invoices
    except HTTPException as e:
        LOGGER.error(e)
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=e) from e


@app.delete("/api/v1/invoices/{file_id}")
def delete_invoice(
    file_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> Response:
    try:
        presenter.delete_invoice(file_id=file_id, user_id=user.user_id, session=session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e


@app.post("/api/v1/users/register/")
def register(
    user: UserCreate, session: Annotated[sqlmodel.Session, Depends(db.get_session)]
):
    auth.register_user(user=user, session=session)
    return Response(content="User has been added to the database.", status_code=201)


@app.post("/api/v1/users/login/")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
) -> AuthToken:
    try:
        user = auth.authenticate_user(
            email=form_data.username, password=form_data.password, session=session
        )
        access_token = auth.create_access_token(email=user.email)
    except Exception as e:
        LOGGER.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    return AuthToken(access_token=access_token, token_type="bearer")


@app.delete("/api/v1/users/")
def delete_user(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> Response:
    try:
        presenter.delete_user(user_id=user.user_id, session=session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e


@app.get("/api/v1/clients/")
def get_clients(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
    page: int = Query(1, ge=1),
    per_page: int = Query(settings.PER_PAGE, ge=1),
) -> PagedClientGetResponse:
    try:
        paged_client_response = presenter.get_paged_clients(
            user=user,
            session=session,
            page=page,
            per_page=per_page,
        )
        return paged_client_response
    except HTTPException as e:
        LOGGER.error(e)
        raise e
    except Exception as e:
        LOGGER.error(e)
        raise HTTPException(
            status_code=400,
            detail=e,
        ) from e


@app.post("/api/v1/clients/add/")
def add_client(
    client: Client,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> Response:
    try:
        LOGGER.info(f"Adding client for user: {user.email}")
        presenter.add_client(user=user, client=client, session=session)
        return Response(
            content="New client added to the database.",
            status_code=201,
        )
    except HTTPException as e:
        LOGGER.error(e)
        raise e
    except Exception as e:
        LOGGER.error(e)
        raise HTTPException(status_code=400, detail=e) from e


@app.delete("/api/v1/clients/{client_id}")
def delete_client(
    client_id: uuid.UUID,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> Response:
    try:
        presenter.delete_client(
            client_id=client_id, user_id=user.user_id, session=session
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e


@app.put("/api/v1/invoices/{invoice_id}")
def update_invoice(
    invoice_id: uuid.UUID,
    invoice: Invoice,
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
    user: Annotated[User, Depends(auth.get_current_user)],
) -> Response:
    try:
        presenter.update_invoice(
            invoice_id=invoice_id, invoice=invoice, session=session
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
