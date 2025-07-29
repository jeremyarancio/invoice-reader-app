from fastapi import FastAPI, UploadFile

from ml_server.utils import logger
from ml_server.domain.invoice import InvoiceExtraction

logger = logger.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Invoice Reader ML Server",
    description="A FastAPI server for managing Machine Learning and AI features.",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ml-server"}


@app.post("/v1/parse")
async def parse(upload_file: UploadFile) -> InvoiceExtraction:

    file= upload_file.file
    
    return invoice_extraction   

