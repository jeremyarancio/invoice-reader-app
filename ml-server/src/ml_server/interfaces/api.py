import sys
import traceback
from typing import Annotated

from fastapi import Depends, FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse

from ml_server.domain.invoice import InvoiceExtraction
from ml_server.interfaces.dependencies.parser import get_parser
from ml_server.services.exceptions import CustomException
from ml_server.services.parser import ParserInteface, ParserService
from ml_server.utils.logger import get_logger

logger = get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Invoice Reader ML Server",
    description="A FastAPI server for managing Machine Learning and AI features.",
    version="0.1.0",
)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    logger.error(f"Custom exception occurred: {exc.__class__.__name__} - {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.middleware("http")
async def http_exception(request: Request, call_next):
    "Handle uncaught exceptions."
    try:
        return await call_next(request)
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        # Log the error with traceback
        logger.error(
            f"Uncaught exception: {str(exc)}\nRequest URL: {request.url}\nTraceback:\n{tb_str}"
        )

        # Return user-friendly response
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": "Something went wrong. Please try again later.",
            },
        )


@app.get("/")
async def home():
    return {"message": "Welcome to the Invoice ML Server"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ml-server"}


@app.post("/v1/parse")
async def parse(
    upload_file: UploadFile, parser: Annotated[ParserInteface, Depends(get_parser)]
) -> InvoiceExtraction:
    file = upload_file.file
    content_type = upload_file.content_type if upload_file.content_type else "not specified"
    invoice_extraction = await ParserService.parse(
        file=file, content_type=content_type, parser=parser
    )
    return invoice_extraction
