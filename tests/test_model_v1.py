"""Test cases for the __model_v1__ module."""

from collections.abc import Callable
from datetime import date, datetime, timedelta, timezone
from io import BytesIO, StringIO
from pathlib import Path

import pytest
from lxml import etree
from syrupy.assertion import SnapshotAssertion

from pyecospold.core import parse_file_v1
from pyecospold.model_v1 import (
    TimePeriod,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2023-03-29T18:04:18", datetime(2023, 3, 29, 18, 4, 18)),
        (
            "2023-03-29T18:04:18.534+02:00",
            datetime(2023, 3, 29, 18, 4, 18, 534000, timezone(timedelta(hours=2))),
        ),
    ],
)
def test_parse_file_v1_timestamp(
    fixtures_dir: Path, value: str, expected: datetime
) -> None:
    """It parses ISO 8601 timestamps, including fractions and offsets."""
    xml = (fixtures_dir / "v1" / "v1_1.xml").read_text(encoding="utf-8")
    xml = xml.replace('timestamp="2006-10-31T20:34:59"', f'timestamp="{value}"')

    assert parse_file_v1(BytesIO(xml.encode("utf-8"))).datasets[0].timestamp == expected


def test_parse_file_v1_fail(fixtures_dir: Path) -> None:
    """It fails on schema violation."""
    xml_str = (fixtures_dir / "v1" / "v1_1.xml").read_text(encoding="utf-8")
    xml_str = xml_str.replace('amount="1"', 'amount="abc"')
    xml_str = xml_str.replace("<?xml version='1.0' encoding='UTF-8'?>", "")

    with pytest.raises(etree.XMLSyntaxError):
        parse_file_v1(StringIO(xml_str))


def test_parse_file_v1_time_period_start_year(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startYear>1995</startYear>
        <endYear>1995</endYear>
    </timePeriod>"""
    tp = parse_time_period(xml_text)

    assert tp.startDate == date(1995, 1, 1)
    assert tp.endDate == date(1995, 12, 31)


def test_parse_file_v1_time_period_validity(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startYear>1995</startYear>
        <endYear>1995</endYear>
    </timePeriod>"""
    tp = parse_time_period(xml_text)

    assert tp.dataValidForEntirePeriod
    assert tp.text == "foo bar"

    xml_text = """<timePeriod dataValidForEntirePeriod="false">
        <startYear>1995</startYear>
        <endYear>1995</endYear>
    </timePeriod>"""
    tp = parse_time_period(xml_text)

    assert not tp.dataValidForEntirePeriod
    assert not tp.text


def test_parse_file_v1_time_period_date(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startDate>1995-02-03</startDate>
        <endDate>1995-04-21</endDate>
    </timePeriod>"""
    tp = parse_time_period(xml_text)

    assert tp.startDate == date(1995, 2, 3)
    assert tp.endDate == date(1995, 4, 21)


def test_parse_file_v1_time_period_year_month_january(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startYearMonth>1995-01</startYearMonth>
        <endYearMonth>1995-01</endYearMonth>
    </timePeriod>"""
    tp = parse_time_period(xml_text)

    assert tp.startDate == date(1995, 1, 1)
    assert tp.endDate == date(1995, 1, 31)


def test_parse_file_v1_time_period_year_month_december(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startYearMonth>1995-12</startYearMonth>
        <endYearMonth>1995-12</endYearMonth>
    </timePeriod>"""
    tp = parse_time_period(xml_text)

    assert tp.startDate == date(1995, 12, 1)
    assert tp.endDate == date(1995, 12, 31)


def test_parse_file_v1_time_period_year_month_february(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startYearMonth>1995-02</startYearMonth>
        <endYearMonth>1995-02</endYearMonth>
    </timePeriod>"""
    tp = parse_time_period(xml_text)

    assert tp.startDate == date(1995, 2, 1)
    assert tp.endDate == date(1995, 2, 28)


def test_parse_file_v1_time_period_set_new_values(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startDate>1995-02-03</startDate>
        <endDate>1995-04-05</endDate>
    </timePeriod>"""
    tp = parse_time_period(xml_text)

    tp.startDate = date(1990, 5, 6)
    tp.endDate = date(2012, 1, 2)

    assert tp.startDate == date(1990, 5, 6)
    assert tp._startDate == "1990-05-06"
    assert tp.endDate == date(2012, 1, 2)
    assert tp._endDate == "2012-01-02"


def test_parse_file_v1_time_period_set_new_values_errors(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startDate>1995-02-03</startDate>
        <endDate>1995-04-05</endDate>
    </timePeriod>"""
    tp = parse_time_period(xml_text)
    with pytest.raises(ValueError, match="must be a `datetime"):
        tp.startDate = "1990-05-06"
    with pytest.raises(ValueError, match="is after `timePeriod"):
        tp.startDate = date(2022, 1, 2)
    with pytest.raises(ValueError, match="must be a `datetime"):
        tp.endDate = "2012-01-02"
    with pytest.raises(ValueError, match="is before `timePeriod"):
        tp.endDate = date(1970, 5, 6)


@pytest.mark.parametrize("name", ["v1_1.xml", "v1_2.spold"])
def test_parse_file_v1(
    fixtures_dir: Path,
    name: str,
    as_data: Callable[[object], object],
    snapshot: SnapshotAssertion,
) -> None:
    """It exposes every value of the sample file through the model."""
    assert as_data(parse_file_v1(fixtures_dir / "v1" / name)) == snapshot
