import os
from typing import Optional


def get_env_value(key: str, default_value: Optional[str] = None) -> str:
    value = os.environ.get(key, default_value)

    if not value and default_value is not None:
        value = default_value

    if value is None or not value:
        raise RuntimeError(f"Environment value '{key}' is not set")

    return value
