import logging
from typing import Optional

from token_accessor.jwt_token import Token
from token_accessor.lock import AsyncLock, ThreadLock
from token_accessor.token_accessor_base import AsyncTokenAccessorBase, TokenAccessorBase

log = logging.getLogger("token_accessor")


class MemoryTokenAccessor(TokenAccessorBase):
    def __init__(
        self,
        token_lock: ThreadLock,
        token_accessor: TokenAccessorBase,
        cached_token: Optional[Token] = None,
    ):
        super().__init__(token_lock)

        self.__cached_token = cached_token
        self.__token_accessor = token_accessor

    def access_token(self) -> Token:
        if self.__cached_token is None or not self.__cached_token.is_valid():
            log.info("Token not found/expired in memory cache. Getting new token...")
            self.__cached_token = self.__token_accessor.get_token()

        return self.__cached_token


class AsyncMemoryTokenAccessor(AsyncTokenAccessorBase):
    def __init__(
        self,
        lock: AsyncLock,
        token_accessor: AsyncTokenAccessorBase,
        cached_token: Optional[Token] = None,
    ):
        super().__init__(lock)

        self.__cached_token = cached_token
        self.__token_accessor = token_accessor

    async def access_token(self) -> Token:
        if self.__cached_token is None or not self.__cached_token.is_valid():
            log.info("Token not found/expired in memory cache. Getting new token...")
            self.__cached_token = await self.__token_accessor.get_token()

        return self.__cached_token
