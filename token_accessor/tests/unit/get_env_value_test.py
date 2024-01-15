import os
from unittest import mock

import pytest

from token_accessor.get_env_value import get_env_value


@mock.patch.dict(os.environ, {"KEY": "value"})
def test_returns_value():
    value = get_env_value("KEY")

    assert value == "value"


@mock.patch.dict(os.environ, {"KEY": ""})
def test_returns_default_value_when_env_value_empty():
    value = get_env_value("KEY", "DEFAULT")

    assert value == "DEFAULT"


def test_returns_default_value():
    value = get_env_value("KEY", "value")

    assert value == "value"


def test_throws_when_no_key():
    with pytest.raises(RuntimeError):
        get_env_value("KEY")
