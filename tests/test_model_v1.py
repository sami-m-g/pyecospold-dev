"""Test cases for the __model_v1__ module."""

import math
from collections.abc import Callable
from datetime import date, datetime, timedelta, timezone
from io import BytesIO, StringIO
from pathlib import Path

import pytest
from lxml import etree

from pyecospold.core import parse_file_v1
from pyecospold.model_v1 import (
    AdministrativeInformation,
    Allocation,
    DataEntryBy,
    DataGeneratorAndPublication,
    Dataset,
    DataSetInformation,
    EcoSpold,
    Exchange,
    FlowData,
    Geography,
    MetaInformation,
    ModellingAndValidation,
    Person,
    ProcessInformation,
    ReferenceFunction,
    Representativeness,
    Source,
    Technology,
    TimePeriod,
    Validation,
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


def test_parse_file_v1_eco_spold(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    validation_id = 0
    validation_status = "validationStatus"

    assert isinstance(eco_spold, EcoSpold)
    assert isinstance(eco_spold.datasets[0], Dataset)
    assert eco_spold.validationId == validation_id
    assert eco_spold.validationStatus == validation_status


def test_parse_file_v1_dataset(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    valid_company_codes = "CompanyCodes.xml"
    valid_regional_codes = "RegionalCodes.xml"
    valid_categories = "Categories.xml"
    valid_units = "Units.xml"
    number = 1
    timestamp = datetime(2006, 10, 31, 20, 34, 59)
    generator = "EcoAdmin 1.1.17.110"
    internal_schema_version = "1.0"
    dataset = eco_spold.datasets[0]

    assert isinstance(dataset.metaInformation, MetaInformation)
    assert isinstance(dataset.flowData, FlowData)
    assert dataset.validCompanyCodes == valid_company_codes
    assert dataset.validRegionalCodes == valid_regional_codes
    assert dataset.validCategories == valid_categories
    assert dataset.validUnits == valid_units
    assert dataset.number == number
    assert dataset.timestamp == timestamp
    assert dataset.generator == generator
    assert dataset.internalSchemaVersion == internal_schema_version


def test_parse_file_v1_meta_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    meta_information = eco_spold.datasets[0].metaInformation

    assert isinstance(meta_information.processInformation, ProcessInformation)
    assert isinstance(meta_information.modellingAndValidation, ModellingAndValidation)
    assert isinstance(
        meta_information.administrativeInformation, AdministrativeInformation
    )


def test_parse_file_v1_flow_data(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    flow_data = eco_spold.datasets[0].flowData

    assert isinstance(flow_data.exchanges[0], Exchange)
    assert isinstance(flow_data.allocations[0], Allocation)


def test_parse_file_v1_process_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    process_information = eco_spold.datasets[0].metaInformation.processInformation

    assert isinstance(process_information.referenceFunction, ReferenceFunction)
    assert isinstance(process_information.geography, Geography)
    assert isinstance(process_information.technology, Technology)
    assert isinstance(process_information.dataSetInformation, DataSetInformation)
    assert isinstance(process_information.timePeriod, TimePeriod)


def test_parse_file_v1_modelling_and_validation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    dataset = eco_spold.datasets[0]
    modelling_and_validation = dataset.metaInformation.modellingAndValidation

    assert isinstance(modelling_and_validation.representativeness, Representativeness)
    assert isinstance(modelling_and_validation.sources[0], Source)
    assert isinstance(modelling_and_validation.validation, Validation)


def test_parse_file_v1_administrative_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    meta_information = eco_spold.datasets[0].metaInformation
    administrative_information = meta_information.administrativeInformation

    assert isinstance(administrative_information.dataEntryBy, DataEntryBy)
    assert isinstance(
        administrative_information.dataGeneratorAndPublication,
        DataGeneratorAndPublication,
    )
    assert isinstance(administrative_information.persons[0], Person)


def test_parse_file_v1_exchange(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    number = 2156
    category = "waste management"
    sub_category = "recycling"
    local_category = "Entsorgungssysteme"
    local_sub_category = "Recycling"
    cas_number = "007439-89-6"
    name = "disposal, building, reinforcement steel, to recycling"
    location = "CH"
    unit = "kg"
    uncertainty_type = 1
    uncertainty_type_str = "lognormal"
    mean_value = 21200
    standard_deviation95 = 1.22
    formula = "Fe"
    reference_to_source = 0
    page_numbers = ""
    general_comment = "(2,3,1,1,1,5)"
    local_name = "Entsorgung, Gebäude, Armierungseisen, ins Recycling"
    infrastructure_process = False
    min_value = math.nan
    max_value = math.nan
    most_likely_value = math.nan
    input_groups = [5]
    input_groups_str = ["FromTechnosphere"]
    output_groups = [0]
    output_groups_str = ["ReferenceProduct"]
    exchange = eco_spold.datasets[0].flowData.exchanges[1]
    output_exchange = eco_spold.datasets[0].flowData.exchanges[0]

    assert exchange.number == number
    assert exchange.category == category
    assert exchange.subCategory == sub_category
    assert exchange.localCategory == local_category
    assert exchange.localSubCategory == local_sub_category
    assert exchange.CASNumber == cas_number
    assert exchange.name == name
    assert exchange.location == location
    assert exchange.unit == unit
    assert exchange.uncertaintyType == uncertainty_type
    assert exchange.uncertaintyTypeStr == uncertainty_type_str
    assert exchange.meanValue == mean_value
    assert exchange.standardDeviation95 == standard_deviation95
    assert exchange.formula == formula
    assert exchange.referenceToSource == reference_to_source
    assert exchange.pageNumbers == page_numbers
    assert exchange.generalComment == general_comment
    assert exchange.localName == local_name
    assert exchange.infrastructureProcess == infrastructure_process
    assert exchange.minValue is min_value
    assert exchange.maxValue is max_value
    assert exchange.mostLikelyValue is most_likely_value
    assert exchange.groups == input_groups
    assert exchange.groupsStr == input_groups_str
    assert output_exchange.groups == output_groups
    assert output_exchange.groupsStr == output_groups_str


def test_parse_file_v1_allocation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    reference_to_co_product = 1
    allocation_method = -1
    allocation_method_str = "Undefined"
    fraction = 97.6
    reference_to_input_outputs = [1]
    explanations = ""
    allocation = eco_spold.datasets[0].flowData.allocations[0]

    assert allocation.referenceToCoProduct == reference_to_co_product
    assert allocation.allocationMethod == allocation_method
    assert allocation.allocationMethodStr == allocation_method_str
    assert allocation.fraction == fraction
    assert allocation.referenceToInputOutputs == reference_to_input_outputs
    assert allocation.explanations == explanations


def test_parse_file_v1_reference_function(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    name = "compost plant, open"
    local_name = "Kompostieranlage, offen"
    unit = "unit"
    category = "agricultural means of production"
    sub_category = "buildings"
    local_category = "Landwirtschaftliche Produktionsmittel"
    local_sub_category = "Gebäude"
    amount = 1
    included_processes = (
        "Building materials required for a compost plant and its "
        "construction as well as the disposal of these materials "
        "were included. Land use during construction and use is "
        "considered. The lifetime of the plant was assumed as 25 "
        "years. Transport of the building materials to the "
        "construction site were included."
    )
    general_comment = (
        "The inventory refers to a compost plant over the lifetime of "
        "25 years. The compost plant is constructed for a treating "
        "capactiy of 10‘000 tons biogenic waste per year. The total "
        "turnover of the plant over the entire lifetime of 25 years "
        "amounts thus 250‘000 tons biogenic waste."
    )
    formula = "0"
    infrastructure_included = True
    cas_number = ""
    statistical_classification = 0
    dataset_relates_to_product = True
    synonyms = ["0"]
    process_information = eco_spold.datasets[0].metaInformation.processInformation
    reference_function = process_information.referenceFunction

    assert reference_function.name == name
    assert reference_function.localName == local_name
    assert reference_function.infrastructureProcess
    assert reference_function.unit == unit
    assert reference_function.category == category
    assert reference_function.subCategory == sub_category
    assert reference_function.localCategory == local_category
    assert reference_function.localSubCategory == local_sub_category
    assert reference_function.amount == amount
    assert reference_function.includedProcesses == included_processes
    assert reference_function.generalComment == general_comment
    assert reference_function.formula == formula
    assert reference_function.infrastructureIncluded == infrastructure_included
    assert reference_function.CASNumber == cas_number
    assert reference_function.statisticalClassification == statistical_classification
    assert reference_function.datasetRelatesToProduct == dataset_relates_to_product
    assert reference_function.synonyms == synonyms


def test_parse_file_v1_geography(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    location = "CH"
    text = "Values refer to the situtation in Switzerland."
    process_information = eco_spold.datasets[0].metaInformation.processInformation
    geography = process_information.geography

    assert geography.location == location
    assert geography.text == text


def test_parse_file_v1_technology(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    text = "Refer to open plant composting."
    process_information = eco_spold.datasets[0].metaInformation.processInformation
    technology = process_information.technology

    assert technology.text == text


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
    assert tp.findtext("{*}startDate") == "1990-05-06"
    assert tp.endDate == date(2012, 1, 2)
    assert tp.findtext("{*}endDate") == "2012-01-02"


def test_parse_file_v1_time_period_set_new_values_errors(
    parse_time_period: Callable[[str], TimePeriod],
) -> None:
    xml_text = """<timePeriod dataValidForEntirePeriod="true" text="foo bar">
        <startDate>1995-02-03</startDate>
        <endDate>1995-04-05</endDate>
    </timePeriod>"""
    tp = parse_time_period(xml_text)
    with pytest.raises(TypeError, match="must be a `datetime"):
        tp.startDate = "1990-05-06"  # pyrefly: ignore[bad-argument-type]  # wrong type on purpose
    with pytest.raises(ValueError, match="is after `timePeriod"):
        tp.startDate = date(2022, 1, 2)
    with pytest.raises(TypeError, match="must be a `datetime"):
        tp.endDate = "2012-01-02"  # pyrefly: ignore[bad-argument-type]  # wrong type on purpose
    with pytest.raises(ValueError, match="is before `timePeriod"):
        tp.endDate = date(1970, 5, 6)


def test_parse_file_v1_dataset_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    _type = 1
    type_str = "Unit process"
    timestamp = datetime(2003, 9, 12, 10, 14, 36)
    version = "1.3"
    internal_version = "53.03"
    energy_values = 0
    energy_values_str = "Undefined"
    language_code = "en"
    local_language_code = "de"
    process_information = eco_spold.datasets[0].metaInformation.processInformation
    data_set_information = process_information.dataSetInformation

    assert data_set_information.type == _type
    assert data_set_information.typeStr == type_str
    assert not data_set_information.impactAssessmentResult
    assert data_set_information.timestamp == timestamp
    assert data_set_information.version == version
    assert data_set_information.internalVersion == internal_version
    assert data_set_information.energyValues == energy_values
    assert data_set_information.energyValuesStr == energy_values_str
    assert data_set_information.languageCode == language_code
    assert data_set_information.localLanguageCode == local_language_code


def test_parse_file_v1_representativeness(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    percent = math.nan
    production_volume = ""
    sampling_procedure = "Data come from one compost plant in Switzerland."
    extrapolations = "none"
    uncertainty_adjustments = "none"
    modelling_and_validation = eco_spold.datasets[
        0
    ].metaInformation.modellingAndValidation
    representativeness = modelling_and_validation.representativeness

    assert representativeness.percent is percent
    assert representativeness.productionVolume == production_volume
    assert representativeness.samplingProcedure == sampling_procedure
    assert representativeness.extrapolations == extrapolations
    assert representativeness.uncertaintyAdjustments == uncertainty_adjustments


def test_parse_file_v1_source(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    number = 146
    source_type = 4
    source_type_str = "Measurement on site"
    first_author = "Nemecek, T."
    additional_authors = (
        "Heil A., Huguenin, O., Meier, S., Erzinger S., "
        "Blaser S., Dux. D., Zimmermann A.,"
    )
    year = 2003
    title = "Life Cycle Inventories of Agricultural Production Systems"
    page_numbers = ""
    name_of_editors = ""
    title_of_anthology = "Final report ecoinvent 2000"
    place_of_publications = "Dübendorf, CH"
    publisher = "Swiss Centre for LCI, FAL & FAT"
    journal = ""
    volume_no = 15
    issue_no = ""
    text = "CD-ROM"
    modelling_and_validation = eco_spold.datasets[
        0
    ].metaInformation.modellingAndValidation
    source = modelling_and_validation.sources[0]

    assert source.number == number
    assert source.sourceType == source_type
    assert source.sourceTypeStr == source_type_str
    assert source.firstAuthor == first_author
    assert source.additionalAuthors == additional_authors
    assert source.year == year
    assert source.title == title
    assert source.pageNumbers == page_numbers
    assert source.nameOfEditors == name_of_editors
    assert source.titleOfAnthology == title_of_anthology
    assert source.placeOfPublications == place_of_publications
    assert source.publisher == publisher
    assert source.journal == journal
    assert source.volumeNo == volume_no
    assert source.issueNo == issue_no
    assert source.text == text


def test_parse_file_v1_validation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    proof_reading_details = "Passed."
    proof_reading_validator = 291
    other_details = ""
    modelling_and_validation = eco_spold.datasets[
        0
    ].metaInformation.modellingAndValidation
    validation = modelling_and_validation.validation

    assert validation.proofReadingDetails == proof_reading_details
    assert validation.proofReadingValidator == proof_reading_validator
    assert validation.otherDetails == other_details


def test_parse_file_v1_data_entry_by(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    person = 309
    quality_network = 1
    meta_information = eco_spold.datasets[0].metaInformation
    data_entry_by = meta_information.administrativeInformation.dataEntryBy

    assert data_entry_by.person == person
    assert data_entry_by.qualityNetwork == quality_network


def test_parse_file_v1_data_generator_and_publication(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    person = 309
    data_published_in = 2
    data_published_in_str = (
        "Data has been published entirely in 'referenceToPublishedSource'"
    )
    reference_to_published_source = 146
    access_restricted_to = 0
    access_restricted_to_str = "Public"
    company_code = ""
    country_code = ""
    page_numbers = ""
    meta_information = eco_spold.datasets[0].metaInformation
    administrative_information = meta_information.administrativeInformation
    data_generator_and_publication = (
        administrative_information.dataGeneratorAndPublication
    )

    assert data_generator_and_publication.person == person
    assert data_generator_and_publication.dataPublishedIn == data_published_in
    assert data_generator_and_publication.dataPublishedInStr == data_published_in_str
    assert (
        data_generator_and_publication.referenceToPublishedSource
        == reference_to_published_source
    )
    assert data_generator_and_publication.copyright
    assert data_generator_and_publication.accessRestrictedTo == access_restricted_to
    assert (
        data_generator_and_publication.accessRestrictedToStr == access_restricted_to_str
    )
    assert data_generator_and_publication.companyCode == company_code
    assert data_generator_and_publication.countryCode == country_code
    assert data_generator_and_publication.pageNumbers == page_numbers


def test_parse_file_v1_person(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    number = 309
    name = "name"
    address = "address"
    telephone = "telephone"
    telefax = "telefax"
    email = "email@domain.com"
    company_code = "EMPA-SG"
    country_code = "CH"
    meta_information = eco_spold.datasets[0].metaInformation
    administrative_information = meta_information.administrativeInformation
    person = administrative_information.persons[0]

    assert person.number == number
    assert person.name == name
    assert person.address == address
    assert person.telephone == telephone
    assert person.telefax == telefax
    assert person.email == email
    assert person.companyCode == company_code
    assert person.countryCode == country_code
