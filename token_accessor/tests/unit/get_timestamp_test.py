from freezegun import freeze_time

from token_accessor.get_timestamp import get_timestamp


@freeze_time("2012-01-14 12:00:00")
def test_get_timestamp():
    timestamp = get_timestamp()

    assert timestamp == 1326542400
