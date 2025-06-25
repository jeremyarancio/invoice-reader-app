import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse

from invoice_reader.app.main import app
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger(__name__)


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
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "msg": root_cause,
                # Include location only for validation errors
                "loc": getattr(exc, "loc", None),
            }
        },
    )
