from unittest.mock import MagicMock, patch

from gql import Client, gql

from token_accessor.gql_client import GqlClient
from token_accessor.jwt_token import Token
from token_accessor.token_accessor_base import TokenAccessorBase


def mock_execute(self, document, variable_values=None):
    return {"data": {"test": "test"}}


@patch.object(Client, "execute", new=mock_execute)
def test_get_gql_client_execute_constructs_auth_header():
    token = MagicMock(Token)
    token.get_auth_header.return_value = {"auth": "auth"}

    token_accessor = MagicMock(TokenAccessorBase)
    token_accessor.get_token.return_value = token

    client = GqlClient("http://localhost:3000", token_accessor)
    client.execute(gql("query { test }"))

    assert token.get_auth_header.called
