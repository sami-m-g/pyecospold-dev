"""Test cases for the __cas_validation__ module."""

import math
from typing import Union

import pytest

from pyecospold.cas_validation import validate_cas


@pytest.mark.parametrize(
    "cas",
    [
        110634,
        110634.0,
        "  0000110-63-4",
        "0000110-63-4  ",
        "0000110-63-4\n",
        "0000110634",
        "0-00011-063-4",
        "0-00011063-4",
        "110-63-4",
        "00000000000000110-63-4",
    ],
)
def test_valid(cas: Union[str, float]) -> None:
    """It normalises whitespace, hyphens, padding and numbers."""
    assert validate_cas(cas) == "0000110-63-4"


@pytest.mark.parametrize(
    ("cas", "match"),
    [
        (math.nan, "Not-a-Number"),
        ("0000110-63-4a", "invalid characters"),
        ("ε0000110-63-4", "invalid characters"),
        ("", "CAS is empty: ''"),
        ("   ", "CAS is empty: '   '"),
        ("0000120634", "Check Digit error"),
        ("0000110635", "Check Digit error"),
    ],
)
def test_invalid(cas: Union[str, float], match: str) -> None:
    """It rejects values that are not CAS numbers."""
    with pytest.raises(ValueError, match=match):
        validate_cas(cas)
