from typing import Optional
from urllib.parse import urljoin, urlparse

import requests

from token_accessor.get_aws_auth import get_aws_auth
from token_accessor.get_env_value import get_env_value
from token_accessor.jwt_token import Token
from token_accessor.lock import ThreadLock
from token_accessor.token_accessor_base import TokenAccessorBase
from token_accessor.token_cache_token import parse_token


def create_token_accessor(
    url_path: str, scope: Optional[str] = None, token_cache_url: Optional[str] = None
) -> TokenAccessorBase:
    token_cache_url = token_cache_url or get_env_value("TOKEN_CACHE_URL")
    token_scope = scope or get_env_value("TOKEN_SCOPE")
    token_audience = get_env_value("TOKEN_AUDIENCE", "https://api.altislabs.com")

    if not token_cache_url:
        raise ValueError("TOKEN_CACHE_URL is not defined")

    if not token_scope:
        raise ValueError("TOKEN_SCOPE is not defined")

    url = urljoin(token_cache_url, url_path)

    parsed_url = urlparse(url)
    parts = parsed_url.netloc.split(".")
    if len(parts) < 3:
        raise ValueError(f"TOKEN_CACHE_URL ({token_cache_url}) is not valid")

    aws_region = parts[2]

    token_lock = ThreadLock()

    return TokenCacheTokenAccessor(
        token_lock, url, aws_region, token_scope, token_audience
    )


def create_generic_client_token_accessor(
    token_cache_url: Optional[str] = None, scope: str = "api"
) -> TokenAccessorBase:
    return create_token_accessor("generic-client", scope, token_cache_url)


def create_nota_api_token_accessor(
    token_cache_url: Optional[str] = None, scope: str = "api"
) -> TokenAccessorBase:
    return create_token_accessor("nota-api", scope, token_cache_url)


def create_dicom_server_token_accessor(
    token_cache_url: Optional[str] = None, scope: str = "pacs"
) -> TokenAccessorBase:
    return create_token_accessor("dicom-server", scope, token_cache_url)


class TokenCacheTokenAccessor(TokenAccessorBase):
    def __init__(
        self,
        token_lock: ThreadLock,
        token_cache_url: str,
        token_cache_region: str,
        client_scope: str,
        audience: str,
    ):
        super().__init__(token_lock)

        self.__token_cache_url = token_cache_url
        self.__token_cache_region = token_cache_region
        self.__client_scope = client_scope
        self.__audience = audience

    def access_token(self) -> Token:
        headers = {"content-type": "application/json"}
        payload = {
            "scope": self.__client_scope,
            "audience": self.__audience,
            "grant_type": "client_credentials",
        }

        auth = get_aws_auth(self.__token_cache_url, self.__token_cache_region)

        response = requests.post(
            url=self.__token_cache_url, json=payload, headers=headers, auth=auth
        )
        response.raise_for_status()

        data = response.json()

        return parse_token(data)
