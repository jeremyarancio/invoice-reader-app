from fastapi import FastAPI, UploadFile, HTTPException, Depends
import sqlmodel

from invoice_reader import presenter
# from invoice_reader.app import auth
from invoice_reader.schemas import (
	InvoiceSchema,
)
from invoice_reader import db


#TEMPORARY
USER_ID = "jeremy1544"


app = FastAPI()


@app.get("/")
async def root():
	return {"message": "Hello World"}


@app.post("/api/v1/add/")
def add_invoice(
	file: UploadFile,
	invoice_schema: InvoiceSchema | None,
	session: sqlmodel.Session = Depends(db.get_session),
):
	if file.content_type != "application/pdf":
		raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
	try:
		# token = auth.get_token()
		# user_id = presenter.get_user_id(token=token)
		user_id = USER_ID
		if invoice_schema:
			presenter.submit(
				user_id=user_id,
				file=file.file,
				filename=file.filename,
				invoice_schema=invoice_schema,
				session=session,
			)
			return {
				"message": "The file and its information were successfully stored.",
				"status": 200,
			}
		extracted_metadata = presenter.extract(file=file.file)
		return {
			"message": "File was successfully parsed and metadata were extracted.",
			"metadata": extracted_metadata.model_dump_json(indent=2),
			"status": 200,
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"File submition failed: {str(e)}") from e
