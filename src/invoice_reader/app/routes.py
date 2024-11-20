from typing import Annotated

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
import sqlmodel

from invoice_reader import presenter

# from invoice_reader.app import auth
from invoice_reader.schemas import InvoiceSchema
from invoice_reader import db
from invoice_reader.utils import logger


LOGGER = logger.get_logger(__name__)

# TEMPORARY
USER_ID = "jeremy1544"


app = FastAPI()


class Checker:
	"""https://shorturl.at/Beaur"""

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
	return {"message": "Hello World"}


@app.post("/api/v1/files/submit/")
def add_invoice(
	upload_file: Annotated[UploadFile, File()],
	invoice_schema: Annotated[InvoiceSchema | None, Depends(Checker(InvoiceSchema))],
	session: sqlmodel.Session = Depends(db.get_session),
):
	if upload_file.content_type != "application/pdf":
		raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
	try:
		# token = auth.get_token()
		# user_id = presenter.get_user_id(token=token)
		user_id = USER_ID
		if invoice_schema:
			presenter.submit(
				user_id=user_id,
				file=upload_file.file,
				filename=upload_file.filename,
				invoice_schema=invoice_schema,
				session=session,
			)
			return {
				"message": "The file and its information were successfully stored.",
				"status": 200,
			}
		extracted_metadata = presenter.extract(file=upload_file.file)
		return {
			"message": "File was successfully parsed and metadata were extracted.",
			"metadata": extracted_metadata.model_dump_json(indent=2),
			"status": 200,
		}
	except Exception as e:
		LOGGER.error(e)
		raise HTTPException(status_code=500, detail=f"File submition failed: {str(e)}")
