from fastapi import (
    FastAPI,
    Request,
)
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from invoice_reader import settings
from invoice_reader.app.routes import clients, invoices, others, users
from invoice_reader.utils import logger

LOGGER = logger.get_logger(__name__)


app = FastAPI()
app.include_router(users.router)
app.include_router(invoices.router)
app.include_router(clients.router)
app.include_router(others.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONT_END_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Log the status code and error message
    LOGGER.error(f"HTTP Error: {exc.status_code} - {exc.detail}")
    # Return the default HTTPException response
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/")
async def root():
    return {"message": "Welcome to the Invoice Reader API!"}
