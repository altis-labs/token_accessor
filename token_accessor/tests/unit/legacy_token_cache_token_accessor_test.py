import json
import os
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from freezegun import freeze_time
from httmock import HTTMock, urlmatch, response
from pydantic import ValidationError
from requests import HTTPError

from token_accessor.legacy_token_cache_token_accessor import (
    LegacyTokenCacheTokenAccessor,
    get_aws_auth,
)


@pytest.fixture
def accessor() -> LegacyTokenCacheTokenAccessor:

    mock_lock = MagicMock()
    return LegacyTokenCacheTokenAccessor(
        mock_lock,
        "http://localhost:3000",
        "url",
        "client_id",
        "client_secret",
        "client_scope",
        "audience",
        "grant_type",
    )


@urlmatch(netloc=r"^localhost:3000", method="POST")
def mock_get_token_cache_token_success_response(_url, _request):
    return json.dumps({"access_token": "token", "expires_in": 1})


@urlmatch(netloc=r"^localhost:3000", method="POST")
def mock_get_token_cache_token_bad_token_response(_url, _request):
    return json.dumps({"invalid": "invalid"})


@urlmatch(netloc=r"^localhost:3000", method="POST")
def mock_get_token_cache_token_failure_response(_url, _request):
    return response(status_code=404)


@freeze_time("2012-01-14 12:00:00")
@patch("token_accessor.legacy_token_cache_token_accessor.get_aws_auth")
def test_legacy_token_cache_token_accessor_returns_token(mock_get_aws_auth, accessor):
    mock_get_aws_auth.return_value = MagicMock()

    with HTTMock(mock_get_token_cache_token_success_response):
        token = accessor.access_token()

    assert token.token == "token"
    # compare against fake datetime to ensure timing is not broken in test
    assert token.expires == datetime(2012, 1, 14, 12, 0, 1)


@patch("token_accessor.legacy_token_cache_token_accessor.get_aws_auth")
def test_legacy_token_cache_token_accessor_raises_on_failed_request(
    mock_get_aws_auth, accessor
):
    mock_get_aws_auth.return_value = MagicMock()

    with HTTMock(mock_get_token_cache_token_failure_response):
        with pytest.raises(HTTPError):
            accessor.access_token()


@patch("token_accessor.legacy_token_cache_token_accessor.get_aws_auth")
def test_legacy_token_cache_token_accessor_raises_on_failed_token_parsing(
    mock_get_aws_auth,
    accessor,
):
    mock_get_aws_auth.return_value = MagicMock()

    with HTTMock(mock_get_token_cache_token_bad_token_response):
        with pytest.raises(ValidationError):
            accessor.access_token()


@patch.dict(
    os.environ,
    {
        "AWS_ACCESS_KEY_ID": "",
        "AWS_SECRET_ACCESS_KEY": "",
        "AWS_SESSION_TOKEN": "",
        "AWS_SHARED_CREDENTIALS_FILE": "nofile",
    },
)
def test_get_auth_throws_when_no_credentials():
    with pytest.raises(AttributeError):
        get_aws_auth("http://localhost:3000")
