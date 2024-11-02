from io import BytesIO

from fastapi import FastAPI, File, UploadFile, HTTPException

from invoice_reader.settings import SRC_DIR
from invoice_reader.presenter import (
    upload as _upload,
)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/upload/")
def upload(file: UploadFile):
    # if file.content_type != "application/pdf":
    #     raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    try:
        file_path = _upload(file.file)
        return {"file_path": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")