from datetime import datetime, timedelta

from pydantic import BaseModel

from token_accessor.jwt_token import Token


class TokenCacheToken(BaseModel):
    access_token: str
    expires_in: int


def parse_token(data: any) -> Token:
    parsed: TokenCacheToken = TokenCacheToken.parse_obj(data)
    token = parsed.access_token
    expires = datetime.now() + timedelta(seconds=parsed.expires_in)

    return Token(token, expires)
