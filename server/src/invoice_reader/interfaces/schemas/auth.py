from pydantic import BaseModel

from invoice_reader.domain.auth import EncodedToken


class AuthToken(BaseModel):
    access_token: EncodedToken
    token_type: str
