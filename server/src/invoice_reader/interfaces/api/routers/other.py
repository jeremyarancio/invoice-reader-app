from typing import Annotated

import sqlmodel
from fastapi import APIRouter, Depends, HTTPException

from invoice_reader import db, presenter
from invoice_reader.schemas import Currency

router = APIRouter(
    prefix="/v1",
    tags=["Others"],
)


@router.get("/currencies/")
def get_currencies(
    session: Annotated[sqlmodel.Session, Depends(db.get_session)],
) -> list[Currency]:
    try:
        currencies = presenter.get_currencies(session=session)
        return currencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
