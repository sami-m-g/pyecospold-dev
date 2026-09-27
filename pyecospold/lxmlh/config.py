"""Type conversions and defaults for XML attribute values."""

import math
from collections.abc import Callable
from datetime import datetime
from typing import Any

TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

TYPE_FUNC_MAP: dict[type, Callable[[Any], Any]] = {
    bool: lambda string: string.lower() == "true",
    datetime: datetime.fromisoformat,
}

TYPE_DEFAULTS: dict[type, Any] = {
    int: 0.0,
    float: math.nan,
    bool: "false",
    str: "",
}
