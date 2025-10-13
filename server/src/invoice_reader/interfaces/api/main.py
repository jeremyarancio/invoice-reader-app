import traceback
from contextlib import asynccontextmanager
from importlib.metadata import version

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_fastapi_instrumentator import Instrumentator

from invoice_reader.interfaces.api.routers import (
    client_router,
    invoice_router,
    user_router,
)
from invoice_reader.domain.exceptions import CustomException
from invoice_reader.settings import get_settings
from invoice_reader.utils.logger import get_logger

settings = get_settings()

logger = get_logger()

# Get version from package metadata
try:
    APP_VERSION = version("invoice-reader")
except Exception:
    APP_VERSION = "unknown"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, title="Invoice Reader API", version=APP_VERSION)
app.include_router(user_router)
app.include_router(invoice_router)
app.include_router(client_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CustomException)
def http_exception_handler(request: Request, exc: CustomException):
    # Log the status code and error message
    logger.error("Error: {} - {}", exc.status_code, exc.message)
    # Return the default HTTPException response
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Get root cause
    root_cause = str(exc)
    traceback_str = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    # For production, log the full traceback but don't return it
    logger.error("Error: {}", traceback_str)  # Log to your system

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "msg": root_cause,
                # Include location only for validation errors
                "loc": getattr(exc, "loc", None),
            }
        },
    )


@app.get("/")
async def root(response: Response):
    return {"message": "Welcome to the Invoice Reader API!"}


@app.get("/health")
async def health():
    """Health check endpoint with version information."""
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "service": "invoice-reader-api",
    }


# Monitoring
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app)
