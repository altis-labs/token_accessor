from unittest.mock import MagicMock

from token_accessor.jwt_token import Token
from token_accessor.lock import Lock
from token_accessor.memory_token_accessor import MemoryTokenAccessor
from token_accessor.token_accessor_base import TokenAccessorBase


def test_memory_token_accessor_returns_new_token_when_none_exist():
    mock_lock = MagicMock(Lock)
    mock_token = MagicMock(Token)

    token_accessor = MagicMock(TokenAccessorBase)
    token_accessor.get_token.return_value = mock_token

    accessor = MemoryTokenAccessor(mock_lock, token_accessor, None)
    token = accessor.access_token()

    token_accessor.get_token.assert_called_once()

    assert token == mock_token


def test_memory_token_accessor_returns_new_token_when_invalid():
    mock_lock = MagicMock(Lock)

    mock_invalid_token = MagicMock(Token)
    mock_invalid_token.is_valid.return_value = False

    mock_valid_token = MagicMock(Token)
    mock_valid_token.is_valid.return_value = True

    token_accessor = MagicMock(TokenAccessorBase)
    token_accessor.get_token.return_value = mock_valid_token

    accessor = MemoryTokenAccessor(
        mock_lock, token_accessor, mock_invalid_token
    )
    token = accessor.access_token()

    mock_invalid_token.is_valid.assert_called_once()

    assert token == mock_valid_token


def test_memory_token_accessor_returns_cached_token():
    mock_lock = MagicMock(Lock)

    mock_valid_token = MagicMock(Token)
    mock_valid_token.is_valid.return_value = True

    token_accessor = MagicMock(TokenAccessorBase)

    accessor = MemoryTokenAccessor(mock_lock, token_accessor, mock_valid_token)
    token = accessor.access_token()

    token_accessor.get_token.assert_not_called()
    mock_valid_token.is_valid.assert_called_once()

    assert token == mock_valid_token
