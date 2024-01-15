from typing import Any, Optional


def try_parse_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
