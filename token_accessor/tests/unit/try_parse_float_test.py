from token_accessor.try_parse_float import try_parse_float


def test_try_parse_float_returns_float_with_decimal():
    result = try_parse_float("1.234")
    assert result == 1.234


def test_try_parse_float_returns_float_from_int():
    result = try_parse_float("1")
    assert result == 1


def test_try_parse_float_returns_none_for_none():
    result = try_parse_float(None)
    assert result is None


def test_try_parse_float_returns_none_for_invalid():
    result = try_parse_float("a")
    assert result is None
