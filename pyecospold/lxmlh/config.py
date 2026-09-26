import math
from collections.abc import Callable
from datetime import datetime
from typing import Any

TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

TYPE_FUNC_MAP: dict[type, Callable[[str], Any]] = {
    bool: lambda string: string.lower() == "true",
    datetime: lambda string: datetime.fromisoformat(string),
}

TYPE_DEFAULTS: dict[type, Any] = {
    int: 0.0,
    float: math.nan,
    bool: "false",
    str: "",
}
