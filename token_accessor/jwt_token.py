from datetime import datetime
from typing import Dict


class Token:
    def __init__(self, token: str, expires: datetime):
        self.__token = token
        self.__expires = expires

    @property
    def token(self) -> str:
        return self.__token

    @property
    def expires(self) -> datetime:
        return self.__expires

    def is_valid(self) -> bool:
        return self.expires > datetime.now()

    def get_auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}
