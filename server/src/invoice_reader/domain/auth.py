from datetime import datetime

from pydantic import BaseModel


class DecodedToken(BaseModel):
    email: str
    exp: datetime
    type: str
