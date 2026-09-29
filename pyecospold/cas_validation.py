"""Validation and normalisation of CAS registry numbers.

All information from
https://www.cas.org/support/documentation/chemical-substances/checkdig

CAS numbers have the form A-B-C, where:

    A has between 2 and 7 integers
    B has 2 integers
    C is a single check digit integer

To calculate the check digit:

Each integer starting from the right, and ignoring hyphens, is given a
weight corresponding to its ordinal position (1-indexed). The check is
calculated from the sum of the weighted values, taking the values in
the ones digit. For example for 107-07-3, the sum would be:

    1 * 7 + 2 * 0 + 3 * 7 + 4 * 0 + 5 * 1 = 33

And the check digit would be 3 (the values in the ones position.
Similarly, for 110-63-4:

    1 * 3 + 2 * 6 + 3 * 0 + 4 * 1 + 5 * 1 = 24

"""

import math
from typing import Union


def validate_cas(cas: Union[str, float]) -> str:
    """Normalise a CAS number: strip, re-hyphenate, zero-pad, check the digit.

    Args:
        cas: CAS number as a string, or as a number without hyphens.

    Returns:
        The CAS number as ``0000000-00-0``.

    Raises:
        ValueError: if it has invalid characters, is empty, or its check digit is
            wrong.
    """
    if isinstance(cas, str):
        cas_str = cas.strip()
    elif isinstance(cas, (int, float)):
        cas_str = _convert_numeric_cas(cas)

    valid_characters = {str(x) for x in range(10)}.union({"-"})
    invalid_characters = {c for c in cas_str if c not in valid_characters}
    if invalid_characters:
        msg = f"CAS number includes invalid characters: {invalid_characters}"
        raise ValueError(msg)

    if not cas_str:
        msg = f"Given CAS is empty: {cas!r}."
        raise ValueError(msg)

    cas_str = _rehyphenate_cas(cas_str)

    _check_digit(cas_str)
    return _zero_pad_cas(cas_str)


def _check_digit(cas_str: str) -> None:
    total = sum(
        (a + 1) * int(b) for a, b in zip(range(9), cas_str.replace("-", "")[-2::-1])
    )
    error = (
        f"CAS Check Digit error: CAS '{cas_str}' has check digit of {cas_str[-1]}, "
        f"but it should be {total % 10}"
    )
    if total % 10 != int(cas_str[-1]):
        msg = f"CAS not valid: {cas_str} ({error})"
        raise ValueError(msg)


def _convert_numeric_cas(cas: float) -> str:
    if math.isnan(cas):
        msg = "Given CAS value is Not-a-Number"
        raise ValueError(msg)
    cas_str = str(int(cas))
    return _rehyphenate_cas(cas_str)


def _rehyphenate_cas(cas_str: str) -> str:
    cas_str = cas_str.replace("-", "")
    return f"{cas_str[-10:-3]}-{cas_str[-3:-1]}-{cas_str[-1]}"


def _zero_pad_cas(cas_str: str) -> str:
    zeros = "0" * (12 - len(cas_str))
    return zeros + cas_str
