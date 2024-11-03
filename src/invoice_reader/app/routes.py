from io import BytesIO

from fastapi import FastAPI, File, UploadFile, HTTPException

from invoice_reader import presenter
from invoice_reader.settings import SRC_DIR
from invoice_reader.core.schemas import InvoiceMetadata

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/upload/")
def upload(
    file: UploadFile,
    metadata: InvoiceMetadata,
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    try:
        extracted_metadata = presenter.upload(file.file, metadata=metadata)
        if extracted_metadata.is_complete():
            return {
                "message": f"Fields are missing: {[key for key, value in extracted_metadata.model_dump().items() if value is None ]}",
                "metadata": extracted_metadata.model_dump()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")