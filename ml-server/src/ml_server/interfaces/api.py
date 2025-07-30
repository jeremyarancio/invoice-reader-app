from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, UploadFile

from ml_server.domain.invoice import InvoiceExtraction
from ml_server.interfaces.dependencies.parser import get_parser
from ml_server.services.exceptions import CustomException
from ml_server.services.parser import ParserInteface, ParserService
from ml_server.utils import logger

LOGGER = logger.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Invoice Reader ML Server",
    description="A FastAPI server for managing Machine Learning and AI features.",
    version="0.1.0",
)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    return HTTPException(
        status_code=exc.status_code,
        detail=exc.message,
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ml-server"}


@app.post("/v1/parse")
async def parse(
    upload_file: UploadFile, parser: Annotated[ParserInteface, Depends(get_parser)]
) -> InvoiceExtraction:
    file = upload_file.file
    invoice_extraction = await ParserService.parse(file=file, parser=parser)
    return invoice_extraction
