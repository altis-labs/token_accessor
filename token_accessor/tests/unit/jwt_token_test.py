from datetime import datetime, timedelta

from token_accessor.jwt_token import Token


def test_token_is_valid_returns_true():
    expires = datetime.now() + timedelta(1)
    token = Token("token", expires)
    assert token.is_valid()


def test_token_is_valid_returns_false():
    expires = datetime.now() - timedelta(1)
    token = Token("token", expires)
    assert not token.is_valid()


def test_token_auth_header_returns_header():
    token = Token("token", expires=datetime.now())
    header = token.get_auth_header()

    assert "Authorization" in header
    assert header["Authorization"].startswith("Bearer ")
