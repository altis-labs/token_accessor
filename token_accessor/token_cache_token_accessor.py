from typing import Optional, Union
from urllib.parse import urljoin, urlparse

import boto3
import requests

from token_accessor.get_aws_auth import get_aws_auth
from token_accessor.get_env_value import get_env_value
from token_accessor.jwt_token import Token
from token_accessor.lock import AsyncLock, ThreadLock
from token_accessor.memory_token_accessor import (
    AsyncMemoryTokenAccessor,
    MemoryTokenAccessor,
)
from token_accessor.token_accessor_base import AsyncTokenAccessorBase, TokenAccessorBase
from token_accessor.token_cache_token import parse_token


def create_token_accessor(
    url_path: str,
    scope: Optional[str] = None,
    token_cache_url: Optional[str] = None,
    session: Optional[boto3.Session] = None,
) -> TokenAccessorBase:
    token_cache_url = token_cache_url or get_env_value("TOKEN_CACHE_URL")
    token_scope = scope or get_env_value("TOKEN_SCOPE")
    token_audience = get_env_value("TOKEN_AUDIENCE", "https://api.altislabs.com")

    if not token_cache_url:
        raise ValueError("TOKEN_CACHE_URL is not defined")

    if not token_scope:
        raise ValueError("TOKEN_SCOPE is not defined")

    if not token_cache_url.endswith("/"):
        token_cache_url += "/"

    url = urljoin(token_cache_url, url_path)

    cache_lock = ThreadLock()

    cache_accessor = TokenCacheTokenAccessor(
        cache_lock, url, token_scope, token_audience, session
    )

    memory_lock = ThreadLock()

    return MemoryTokenAccessor(memory_lock, cache_accessor)


def create_async_token_accessor(
    url_path: str,
    scope: Optional[str] = None,
    token_cache_url: Optional[str] = None,
    session: Optional[boto3.Session] = None,
) -> AsyncTokenAccessorBase:
    token_cache_url = token_cache_url or get_env_value("TOKEN_CACHE_URL")
    token_scope = scope or get_env_value("TOKEN_SCOPE")
    token_audience = get_env_value("TOKEN_AUDIENCE", "https://api.altislabs.com")

    if not token_cache_url:
        raise ValueError("TOKEN_CACHE_URL is not defined")

    if not token_scope:
        raise ValueError("TOKEN_SCOPE is not defined")

    if not token_cache_url.endswith("/"):
        token_cache_url += "/"

    url = urljoin(token_cache_url, url_path)

    cache_lock = AsyncLock()

    cache_accessor = AsyncTokenCacheTokenAccessor(
        cache_lock, url, token_scope, token_audience, session
    )

    memory_lock = AsyncLock()

    return AsyncMemoryTokenAccessor(memory_lock, cache_accessor)


def create_generic_client_token_accessor(
    token_cache_url: Optional[str] = None,
    scope: str = "api",
    session: Optional[boto3.Session] = None,
) -> TokenAccessorBase:
    return create_token_accessor("generic-client", scope, token_cache_url, session)


def create_nota_api_token_accessor(
    token_cache_url: Optional[str] = None,
    scope: str = "api",
    session: Optional[boto3.Session] = None,
) -> TokenAccessorBase:
    return create_token_accessor("nota-api", scope, token_cache_url, session)


def create_dicom_server_token_accessor(
    token_cache_url: Optional[str] = None,
    scope: str = "pacs",
    session: Optional[boto3.Session] = None,
) -> TokenAccessorBase:
    return create_token_accessor("dicom-server", scope, token_cache_url, session)


def create_async_generic_client_token_accessor(
    token_cache_url: Optional[str] = None,
    scope: str = "api",
    session: Optional[boto3.Session] = None,
) -> AsyncTokenAccessorBase:
    return create_async_token_accessor(
        "generic-client", scope, token_cache_url, session
    )


def create_async_nota_api_token_accessor(
    token_cache_url: Optional[str] = None,
    scope: str = "api",
    session: Optional[boto3.Session] = None,
) -> AsyncTokenAccessorBase:
    return create_async_token_accessor("nota-api", scope, token_cache_url, session)


def create_async_dicom_server_token_accessor(
    token_cache_url: Optional[str] = None,
    scope: str = "pacs",
    session: Optional[boto3.Session] = None,
) -> AsyncTokenAccessorBase:
    return create_async_token_accessor("dicom-server", scope, token_cache_url, session)


class TokenCacheTokenAccessor(TokenAccessorBase):
    def __init__(
        self,
        token_lock: ThreadLock,
        token_cache_url: str,
        client_scope: str,
        audience: str,
        session: Optional[boto3.Session] = None,
    ):
        super().__init__(token_lock)

        self.__token_cache_url = token_cache_url
        self.__client_scope = client_scope
        self.__audience = audience
        self.__session = session

    def access_token(self) -> Token:
        headers = {"content-type": "application/json"}
        payload = {
            "scope": self.__client_scope,
            "audience": self.__audience,
            "grant_type": "client_credentials",
        }

        auth = get_aws_auth(self.__token_cache_url, self.__session)

        response = requests.post(
            url=self.__token_cache_url, json=payload, headers=headers, auth=auth
        )
        response.raise_for_status()

        data = response.json()

        return parse_token(data)


class AsyncTokenCacheTokenAccessor(AsyncTokenAccessorBase):
    def __init__(
        self,
        lock: AsyncLock,
        token_cache_url: str,
        client_scope: str,
        audience: str,
        session: Optional[boto3.Session] = None,
    ):
        super().__init__(lock)

        self.__token_cache_url = token_cache_url
        self.__client_scope = client_scope
        self.__audience = audience
        self.__session = session

    async def access_token(self) -> Token:
        headers = {"content-type": "application/json"}
        payload = {
            "scope": self.__client_scope,
            "audience": self.__audience,
            "grant_type": "client_credentials",
        }

        auth = get_aws_auth(self.__token_cache_url, self.__session)

        response = requests.post(
            url=self.__token_cache_url, json=payload, headers=headers, auth=auth
        )
        response.raise_for_status()

        data = response.json()

        return parse_token(data)
