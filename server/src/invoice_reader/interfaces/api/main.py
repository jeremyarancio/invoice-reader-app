import traceback

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_fastapi_instrumentator import Instrumentator

from invoice_reader import settings
from invoice_reader.interfaces.api.routers import (
    client_router,
    user_router,
    invoice_router,
)
from invoice_reader.utils import logger

LOGGER = logger.get_logger(__name__)


app = FastAPI()
app.include_router(user_router)
app.include_router(invoice_router)
app.include_router(client_router)

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
def http_exception_handler(request: Request, exc: HTTPException):
    # Log the status code and error message
    LOGGER.error("HTTP Error: %s - %s", exc.status_code, exc.detail)
    # Return the default HTTPException response
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.get("/")
async def root(response: Response):
    return {"message": "Welcome to the Invoice Reader API!"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Get root cause
    root_cause = str(exc)
    traceback_str = "".join(
        traceback.format_exception(type(exc), exc, exc.__traceback__)
    )

    # For production, log the full traceback but don't return it
    LOGGER.error(f"ERROR: {traceback_str}")  # Log to your system

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


# Monitoring
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app)
