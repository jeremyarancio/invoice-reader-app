from datetime import datetime

from pydantic import BaseModel


class EncodedToken(str):
    @classmethod
    def convert_str(cls, token: str) -> "EncodedToken":
        return cls(token)


class DecodedToken(BaseModel):
    email: str
    exp: datetime
    type: str
