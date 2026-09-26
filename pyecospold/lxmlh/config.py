import math
from datetime import datetime
from typing import Any, Callable, Dict

TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

TYPE_FUNC_MAP: Dict[type, Callable[[str], Any]] = {
    bool: lambda string: string.lower() == "true",
    datetime: lambda string: datetime.fromisoformat(string),
}

TYPE_DEFAULTS: Dict[type, Any] = {
    int: 0.0,
    float: math.nan,
    bool: "false",
    str: "",
}
