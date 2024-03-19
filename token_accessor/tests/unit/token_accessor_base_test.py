from unittest.mock import MagicMock, patch

import pytest

from token_accessor.lock import ThreadLock
from token_accessor.token_accessor_base import TokenAccessorBase


@patch.object(TokenAccessorBase, "__abstractmethods__", set())
def test_token_accessor_base_locks_on_get_token():
    mock_lock = MagicMock(ThreadLock)

    accessor = TokenAccessorBase(mock_lock)
    accessor.get_token()

    mock_lock.acquire.assert_called_once()
    mock_lock.release.assert_called_once()


@patch.object(TokenAccessorBase, "__abstractmethods__", set())
@patch.object(TokenAccessorBase, "access_token", side_effect=Exception())
def test_token_accessor_base_releases_when_access_token_raises(
    _mock_access_token,
):
    mock_lock = MagicMock(ThreadLock)

    accessor = TokenAccessorBase(mock_lock)

    with pytest.raises(Exception):
        accessor.get_token()

    mock_lock.release.assert_called_once()
