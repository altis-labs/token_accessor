from abc import ABC, abstractmethod

from token_accessor.jwt_token import Token
from token_accessor.lock import AsyncLock, ThreadLock


class TokenAccessorBase(ABC):
    def __init__(self, lock: ThreadLock):
        self.__token_lock = lock

    def get_token(self) -> Token:
        self.__token_lock.acquire()

        try:
            token = self.access_token()
        except Exception as err:
            self.__token_lock.release()
            raise err

        self.__token_lock.release()

        return token

    @abstractmethod
    def access_token(self) -> Token:
        pass


class AsyncTokenAccessorBase(ABC):
    def __init__(self, lock: AsyncLock):
        self.__token_lock = lock

    async def get_token(self) -> Token:
        await self.__token_lock.acquire()

        try:
            token = await self.access_token()
        except Exception as err:
            self.__token_lock.release()
            raise err

        self.__token_lock.release()

        return token

    @abstractmethod
    async def access_token(self) -> Token:
        pass
