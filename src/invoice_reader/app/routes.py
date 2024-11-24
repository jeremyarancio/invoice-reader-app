from typing import Annotated

from fastapi import FastAPI, UploadFile, File, Depends, Form, status, Response
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ValidationError
import sqlmodel

from invoice_reader import presenter

# from invoice_reader.app import auth
from invoice_reader.schemas import InvoiceSchema, UserSchema, TokenSchema
from invoice_reader import db
from invoice_reader.utils import logger
from invoice_reader import settings
from invoice_reader.app import auth


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
def add_invoice(
	upload_file: Annotated[UploadFile, File()],
	invoice_data: Annotated[InvoiceSchema | None, Depends(Checker(InvoiceSchema))],
	session: Annotated[sqlmodel.Session, Depends(db.get_session)],
	user: Annotated[UserSchema, Depends(auth.get_user)],
):
	if upload_file.content_type != "application/pdf":
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only PDF files are allowed.")
	try:
		user_id = settings._USER_ID #NOTE: Temporary
		if invoice_data:
			presenter.submit(
				user_id=user_id,
				file=upload_file.file,
				filename=upload_file.filename,
				invoice_data=invoice_data,
				session=session,
			)
			return {
				"message": "The file and its information were successfully stored.",
				"status": 200,
			}
		extracted_metadata = presenter.extract(file=upload_file.file)
		return {
			"message": "File was successfully parsed and metadata were extracted.",
			"invoice_data": extracted_metadata.model_dump_json(indent=2),
			"status": 200,
		}
	except Exception as e:
		LOGGER.error(e)
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/users/register")
def register(
	user: UserSchema,
	session: sqlmodel.Session = Depends(db.get_session)
):
	try:
		presenter.register_user(user=user, session=session)
		return Response(
			content="User has been added to the database.",
			status_code=200
		)
	except Exception as e:
		LOGGER.error(e)
		raise HTTPException(status_code=400, detail=str(e))
	

@app.post("/api/v1/users/login/")
def login(
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
	session:Annotated[sqlmodel.Session, Depends(db.get_session)]
) -> TokenSchema:
	try: 
		user = auth.authenticate_user(username=form_data.username, password=form_data.password, session=session)
		access_token = auth.create_access_token(username=user.username)
	except Exception:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid authentication credentials",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return TokenSchema(access_token=access_token, token_type="bearer")
