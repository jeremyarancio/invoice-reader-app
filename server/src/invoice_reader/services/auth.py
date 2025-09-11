from datetime import datetime, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from invoice_reader.domain.auth import DecodedToken, EncodedToken
from invoice_reader.services.exceptions import AuthenticationException
from invoice_reader.settings import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def decode_token(token: EncodedToken) -> DecodedToken:
        try:
            payload = jwt.decode(  # type: ignore
                jwt=token,
                key=settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            return DecodedToken(**payload)
        except ExpiredSignatureError as e:
            raise AuthenticationException(
                message="Refresh token has expired. Please sign in again.",
                status_code=401,
            ) from e
        except InvalidTokenError as e:
            raise AuthenticationException(
                message="Invalid refresh token. Please sign in again.",
                status_code=401,
            ) from e

    @classmethod
    def refresh_token(cls, token: EncodedToken) -> tuple[EncodedToken, EncodedToken]:
        payload = cls.decode_token(token=token)
        if email := payload.email:
            access_token = cls.create_token(
                email=email,
                expire=settings.access_token_expire,
                token_type="access",
            )
            # We also re-update the refresh token to extend the login session
            refresh_token = cls.create_token(
                email=email,
                expire=settings.refresh_token_expire,
                token_type="refresh",
            )
            return access_token, refresh_token
        else:
            raise AuthenticationException(status_code=401, message="Email not found in token.")

    @staticmethod
    def create_token(email: str, expire: int, token_type: str) -> EncodedToken:
        exp = datetime.now() + timedelta(seconds=expire)
        payload = DecodedToken(
            email=email,
            exp=exp,
            type=token_type,
        )
        encoded_jwt = jwt.encode(  # type: ignore
            payload=payload.model_dump(),
            key=settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )
        return EncodedToken.convert_str(encoded_jwt)
