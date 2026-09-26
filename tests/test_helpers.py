"""Test cases for the __helpers__ module."""

from datetime import date
from pathlib import Path

import pytest
from lxml.etree import DocumentInvalid

from pyecospold.core import parse_file_v1, parse_file_v2
from pyecospold.model_v1 import ProcessInformation


@pytest.fixture
def process_information(fixtures_dir: Path) -> ProcessInformation:
    """ProcessInformation of the parsed v1 sample."""
    eco_spold = parse_file_v1(fixtures_dir / "v1" / "v1_1.xml")
    return eco_spold.datasets[0].metaInformation.processInformation


def test_set_attribute_validator(process_information: ProcessInformation) -> None:
    """It runs the attribute validator (CAS normalisation) on set."""
    cas_number_input = "    0000110-63-4\n"
    cas_number_expected = "0000110-63-4"
    process_information.referenceFunction.CASNumber = cas_number_input

    assert process_information.referenceFunction.CASNumber == cas_number_expected


def test_set_attribute_fail(process_information: ProcessInformation) -> None:
    """It rejects a value the schema does not allow."""
    with pytest.raises(DocumentInvalid):
        process_information.referenceFunction.amount = "abc"


def test_set_attribute_success(process_information: ProcessInformation) -> None:
    """It sets an attribute."""
    amount = 2.0
    process_information.referenceFunction.amount = amount

    assert process_information.referenceFunction.amount == amount


def test_set_attribute_list_success(process_information: ProcessInformation) -> None:
    """It sets an attribute list."""
    synonyms = ["0", "1", "2"]
    process_information.referenceFunction.synonyms = synonyms

    assert process_information.referenceFunction.synonyms == synonyms


def test_set_element_text_success(process_information: ProcessInformation) -> None:
    """It sets element text (timePeriod startDate)."""
    start_date = date(1970, 1, 1)
    process_information.timePeriod.startDate = start_date

    assert process_information.timePeriod.startDate == start_date


def test_get_attribute_list_empty_element(fixtures_dir: Path) -> None:
    """An empty list element reads as an empty string instead of crashing."""
    eco_spold = parse_file_v2(fixtures_dir / "v2" / "v2_1.xml")
    exchanges = eco_spold.activityDataset.flowData.elementaryExchanges
    hydrogen_chloride = next(e for e in exchanges if e.names == ["Hydrogen chloride"])

    assert hydrogen_chloride.synonyms == [""]
