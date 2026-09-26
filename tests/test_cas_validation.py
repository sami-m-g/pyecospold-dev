"""Test cases for the __cas_validation__ module."""

import math

import pytest

from pyecospold.cas_validation import validate_cas


def test_nan():
    """It raises ValueError."""
    with pytest.raises(ValueError):
        validate_cas(math.nan)


def test_valid_int():
    """It validates int CAS."""
    cas = 110634
    assert validate_cas(cas) == "0000110-63-4"


def test_valid_float():
    """It validates float CAS."""
    cas = 110634.0
    assert validate_cas(cas) == "0000110-63-4"


def test_extra_whitespace():
    """It validates CAS with extra whitespaces."""
    cas_pre = "  0000110-63-4"
    cas_post = "0000110-63-4  "
    cas_new_line = "0000110-63-4\n"

    assert validate_cas(cas_pre) == "0000110-63-4"
    assert validate_cas(cas_post) == "0000110-63-4"
    assert validate_cas(cas_new_line) == "0000110-63-4"


def test_invalid_characters():
    """It validates CAS with invalid characters."""
    with pytest.raises(ValueError):
        validate_cas("0000110-63-4a")

    with pytest.raises(ValueError):
        validate_cas("ε0000110-63-4")


def test_empty_cas():
    """It validates empty CAS."""
    with pytest.raises(ValueError):
        validate_cas("")


def test_hyphenation():
    """It validates CAS with hyphens."""
    cas_no_hyphen = "0000110634"
    cas_four_hyphens = "0-00011-063-4"
    # Two hyphens but in wrong place
    cas_two_hyphens = "0-00011063-4"

    assert validate_cas(cas_no_hyphen) == "0000110-63-4"
    assert validate_cas(cas_four_hyphens) == "0000110-63-4"
    assert validate_cas(cas_two_hyphens) == "0000110-63-4"


def test_check_digit():
    """It validates CAS digits."""
    cas_valid = "0000110634"
    cas_invalid1 = "0000120634"
    cas_invalid12 = "0000110635"

    assert validate_cas(cas_valid)
    with pytest.raises(ValueError):
        validate_cas(cas_invalid1)
    with pytest.raises(ValueError):
        validate_cas(cas_invalid12)


def test_zero_padding():
    """It validates zero padding."""
    cas_no_padding = "110-63-4"
    cas_extra_padding = "00000000000000110-63-4"

    assert validate_cas(cas_no_padding) == "0000110-63-4"
    assert validate_cas(cas_extra_padding) == "0000110-63-4"
