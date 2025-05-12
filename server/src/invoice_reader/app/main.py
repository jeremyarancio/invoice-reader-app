from fastapi import (
    FastAPI,
    Request,
)
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_fastapi_instrumentator import Instrumentator

from invoice_reader import settings
from invoice_reader.app.routes import clients, invoices, others, users
from invoice_reader.utils import logger

LOGGER = logger.get_logger()


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


@app.get("/home")
def home(response: Response):
    response.set_cookie(key="foo", value="bar", secure=False, samesite="lax")
    return {"foo": "bar"}

# Monitoring
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app)
