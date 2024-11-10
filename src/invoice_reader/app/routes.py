from fastapi import FastAPI, UploadFile, HTTPException

from invoice_reader import presenter
from invoice_reader.app import auth
from invoice_reader.schemas import InvoiceMetadata


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/submit/")
def submit(
    file: UploadFile,
    metadata: InvoiceMetadata | None,
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    try:
        user_id = presenter.get_user_id()
        if metadata:
            presenter.submit(
                user_id=user_id, 
                file=file.file,
                filename=file.filename, 
                metadata=metadata
            )
            return {
                "message": "The file and its information were successfully stored.",
                "status": 200,
            }
        extracted_metadata = presenter.extract(file=file.file)
        return {
            "message": "File was successfully parsed and metadata were extracted.",
            "metadata": extracted_metadata.model_dump_json(),
            "status": 200, 
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"File submition failed: {str(e)}"
        ) from e
