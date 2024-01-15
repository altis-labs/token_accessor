import requests

from token_accessor.get_aws_auth import get_aws_auth
from token_accessor.jwt_token import Token
from token_accessor.lock import Lock
from token_accessor.token_accessor_base import TokenAccessorBase
from token_accessor.token_cache_token import parse_token


class LegacyTokenCacheTokenAccessor(TokenAccessorBase):
    def __init__(
        self,
        token_lock: Lock,
        token_cache_url: str,
        token_cache_region: str,
        url: str,
        client_id: str,
        client_secret: str,
        client_scope: str,
        audience: str,
        grant_type: str = "client_credentials",
    ):
        super().__init__(token_lock)

        self.__token_cache_url = token_cache_url
        self.__token_cache_region = token_cache_region
        self.__url = url
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__client_scope = client_scope
        self.__audience = audience
        self.__grant_type = grant_type

    def access_token(self) -> Token:
        headers = {"content-type": "application/json"}
        payload = {
            "url": self.__url,
            "client_id": self.__client_id,
            "client_secret": self.__client_secret,
            "scope": self.__client_scope,
            "audience": self.__audience,
            "grant_type": self.__grant_type,
        }

        auth = get_aws_auth(self.__token_cache_url, self.__token_cache_region)

        response = requests.post(
            url=self.__token_cache_url, json=payload, headers=headers, auth=auth
        )
        response.raise_for_status()

        data = response.json()

        return parse_token(data)
