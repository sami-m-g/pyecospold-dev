"""Test cases for the __model_v2__ module."""

from datetime import datetime
from pathlib import Path

import pytest

from pyecospold.core import parse_file_v2
from pyecospold.model_v2 import (
    Activity,
    ActivityDataset,
    ActivityDescription,
    AdministrativeInformation,
    Classification,
    DataEntryBy,
    DataGeneratorAndPublication,
    EcoSpold,
    ElementaryExchange,
    FileAttributes,
    FlowData,
    Geography,
    IntermediateExchange,
    MacroEconomicScenario,
    ModellingAndValidation,
    Parameter,
    Representativeness,
    Technology,
    TextAndImage,
    TimePeriod,
    Uncertainty,
)


@pytest.fixture
def eco_spold(fixtures_dir: Path) -> EcoSpold:
    return parse_file_v2(fixtures_dir / "v2" / "v2_2.spold")


def test_parse_file_v2_eco_spold(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    geography_id = "0723d252-7e2a-11de-9820-0019e336be3a"
    geography_short_name = "RER"
    activity_name = "formic acid production, methyl formate route"
    elementary_exchange_compartment = "water"
    elementary_exchange_sub_compartment = "surface water"
    elementary_exchange_name = "BOD5, Biological Oxygen Demand"
    elementary_exchange_unit_name = "kg"
    intermediate_exchange_name = "water, deionised, from tap water, at user"
    intermediate_exchange_unit_name = "kg"

    assert isinstance(eco_spold, EcoSpold)
    assert isinstance(eco_spold.activityDataset, ActivityDataset)
    assert eco_spold.geography.geographyId == geography_id
    assert eco_spold.geographyShortName == geography_short_name
    assert eco_spold.activityName == activity_name
    assert (
        eco_spold.elementary_exchange_compartment(0, 0)
        == elementary_exchange_compartment
    )
    assert (
        eco_spold.elementary_exchange_sub_compartment(0, 0)
        == elementary_exchange_sub_compartment
    )
    assert eco_spold.elementary_exchange_name(0, 0) == elementary_exchange_name
    assert (
        eco_spold.elementary_exchange_unit_name(0, 0) == elementary_exchange_unit_name
    )
    assert eco_spold.intermediate_exchange_name(0, 0) == intermediate_exchange_name
    assert (
        eco_spold.intermediate_exchange_unit_name(0, 0)
        == intermediate_exchange_unit_name
    )


def test_parse_file_v2_activity_dataset(fixtures_dir: Path) -> None:
    """It parses attributes correctly."""
    eco_spold = parse_file_v2(fixtures_dir / "v2" / "v2_1.xml")
    activity_dataset = eco_spold.activityDataset

    assert isinstance(activity_dataset.activityDescription, ActivityDescription)
    assert isinstance(
        activity_dataset.administrativeInformation, AdministrativeInformation
    )
    assert isinstance(activity_dataset.flowData, FlowData)
    assert isinstance(activity_dataset.modellingAndValidation, ModellingAndValidation)


def test_parse_file_v2_child_activity_dataset(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    activity_dataset = eco_spold.activityDataset

    assert isinstance(activity_dataset.activityDescription, ActivityDescription)
    assert isinstance(
        activity_dataset.administrativeInformation, AdministrativeInformation
    )
    assert isinstance(activity_dataset.flowData, FlowData)
    assert isinstance(activity_dataset.modellingAndValidation, ModellingAndValidation)


def test_parse_file_v2_activity_description(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    activity_description = eco_spold.activityDataset.activityDescription

    assert isinstance(activity_description.activity[0], Activity)
    assert isinstance(activity_description.classification[0], Classification)
    assert isinstance(activity_description.geography[0], Geography)
    assert isinstance(
        activity_description.macroEconomicScenario[0], MacroEconomicScenario
    )
    assert isinstance(activity_description.technology[0], Technology)
    assert isinstance(activity_description.timePeriod[0], TimePeriod)


def test_parse_file_v2_flow_data(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    elementary_exchanges_len = 11
    intermediate_exchanges_len = 41
    parameters_len = 6
    impact_indicators_len = 0
    flow_data = eco_spold.activityDataset.flowData

    assert isinstance(flow_data.elementaryExchanges[0], ElementaryExchange)
    assert isinstance(flow_data.intermediateExchanges[0], IntermediateExchange)
    assert isinstance(flow_data.parameters[0], Parameter)

    assert len(flow_data.elementaryExchanges) == elementary_exchanges_len
    assert len(flow_data.intermediateExchanges) == intermediate_exchanges_len
    assert len(flow_data.parameters) == parameters_len
    assert len(flow_data.impactIndicators) == impact_indicators_len


def test_parse_file_v2_modelling_and_validation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    modelling_and_validation = eco_spold.activityDataset.modellingAndValidation

    assert isinstance(modelling_and_validation.representativeness, Representativeness)
    assert modelling_and_validation.review is None


def test_parse_file_v2_administrative_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    administrative_information = eco_spold.activityDataset.administrativeInformation

    assert isinstance(administrative_information.dataEntryBy, DataEntryBy)
    assert isinstance(
        administrative_information.dataGeneratorAndPublication,
        DataGeneratorAndPublication,
    )
    assert isinstance(administrative_information.fileAttributes, FileAttributes)


def test_parse_file_v2_activity(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    activity_names = ["formic acid production, methyl formate route"]
    general_comment_texts = [
        "This data represents the production of 1 kg of formic acid "
        "from methyl formate. Raw materials and energy consumptions are "
        "modelled with literature data. The emissions are estimated. "
        "Infrastructure is included with a default value.",
        "[This dataset was already contained in the ecoinvent database version 2. "
        "It was not individually updated during the transfer to ecoinvent version 3. "
        "Life Cycle Impact Assessment results may still have changed, as they are "
        "affected by changes in the supply chain, i.e. in other datasets. This "
        "dataset was generated following the ecoinvent quality guidelines for "
        "version 2. It may have been subject to central changes described in the "
        "ecoinvent version 3 change report "
        "(http://www.ecoinvent.org/database/ecoinvent-version-3/reports-of-changes/),"
        " and the results of the central updates were reviewed extensively. The "
        "changes added e.g. consistent water flows and other information throughout "
        "the database. The documentation of this dataset can be found in the "
        "ecoinvent reports of version 2, which are still available via the ecoinvent "
        "website. The change report linked above covers all central changes that were"
        " made during the conversion process.]",
    ]
    general_comment_image_urls = []
    included_activities_ends = [
        "This activity ends with 1 kg of formic acid, 100% af the factory gate. "
        "The dataset includes the input materials, energy uses, "
        "infrastructure and emissions."
    ]
    included_activities_starts = [
        "From the reception of methyl formate at the factory gate."
    ]
    synonyms = ["methanoic acid"]
    tags = ["ConvertedDataset"]
    activity_id = "ffed8e5b-8ecb-4a93-bc79-a1404afd9fcd"
    activity_name_id = "8b542688-aa36-45d5-b2f0-3b15ade03700"
    parent_activity_id = "dca19657-6614-4b1d-98aa-0658dd2ced39"
    inheritance_depth = 0
    inheritance_depth_str = "not a child"
    activity_type = 1
    type_str = "Unit process"
    special_activity_type = 0
    special_activity_type_str = "ordinary transforming activity (default)"
    energy_values = 0
    energy_values_str = "Undefined (default)"
    master_allocation_property_id = ""
    master_allocation_property_id_overwritten_by_child = False
    master_allocation_property_context_id = ""
    dataset_icon = ""
    activity = eco_spold.activityDataset.activityDescription.activity[0]

    assert activity.allocationComment is None
    assert isinstance(activity.generalComment, TextAndImage)
    assert activity.activityNames == activity_names
    assert activity.generalComment.texts == general_comment_texts
    assert activity.generalComment.imageUrls == general_comment_image_urls
    assert activity.includedActivitiesEnds == included_activities_ends
    assert activity.includedActivitiesStarts == included_activities_starts
    assert activity.synonyms == synonyms
    assert activity.tags == tags
    assert activity.id == activity_id
    assert activity.activityNameId == activity_name_id
    assert activity.parentActivityId == parent_activity_id
    assert activity.inheritanceDepth == inheritance_depth
    assert activity.inheritanceDepthStr == inheritance_depth_str
    assert activity.type == activity_type
    assert activity.typeStr == type_str
    assert activity.specialActivityType == special_activity_type
    assert activity.specialActivityTypeStr == special_activity_type_str
    assert activity.energyValues == energy_values
    assert activity.energyValuesStr == energy_values_str
    assert activity.masterAllocationPropertyId == master_allocation_property_id
    assert (
        activity.masterAllocationPropertyIdOverwrittenByChild
        == master_allocation_property_id_overwritten_by_child
    )
    assert (
        activity.masterAllocationPropertyContextId
        == master_allocation_property_context_id
    )
    assert activity.datasetIcon == dataset_icon


def test_parse_file_v2_classification(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    classification_id = "7ac1cbc6-1385-4a68-8647-ed7aa78db201"
    classification_context_id = ""
    classification_system = "EcoSpold01Categories"
    classification_value = "chemicals/organics"
    activity_description = eco_spold.activityDataset.activityDescription
    classification = activity_description.classification[0]

    assert classification.classificationId == classification_id
    assert classification.classificationContextId == classification_context_id
    assert classification.classificationSystem == classification_system
    assert classification.classificationValue == classification_value


def test_parse_file_v2_geography(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    geography_id = "0723d252-7e2a-11de-9820-0019e336be3a"
    geography_context_id = ""
    short_names = ["RER"]
    comments_texts = ["The inventory is modelled for Europe."]
    comments_image_urls = []
    activity_description = eco_spold.activityDataset.activityDescription
    geography = activity_description.geography[0]

    assert geography.geographyId == geography_id
    assert geography.geographyContextId == geography_context_id
    assert geography.shortNames == short_names
    assert geography.comments[0].texts == comments_texts
    assert geography.comments[0].imageUrls == comments_image_urls


def test_parse_file_v2_technology(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    technology_level = 3
    technology_level_str = "Current (default)"
    comments_texts = [
        "To keep undesirable reesterification as low as possible, the time of "
        "direct contact between methanol and formic acid must be as short as "
        "possible, and separation must be carried out at the lowest possible "
        "temperature. Introduction of methyl formate into the lower part of "
        "the column in which lower boiling methyl formate and methanol are "
        "separated from water and formic acid, has also been suggested. This "
        "largely prevents reesterification because of the excess methyl formate "
        "present in the critical region of the column."
    ]
    comments_image_url = (
        "https://db3.ecoinvent.org/images/2ddc19c0-905f-42c3-b14c-e68332befec9"
    )
    activity_description = eco_spold.activityDataset.activityDescription
    technology = activity_description.technology[0]

    assert technology.technologyLevel == technology_level
    assert technology.technologyLevelStr == technology_level_str
    assert technology.comments[0].texts[0] == comments_texts[0]
    assert technology.comments[0].imageUrls[0] == comments_image_url


def test_parse_file_v2_time_period(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    start_date = "1984-01-01"
    end_date = "2014-12-31"
    is_data_valid_for_entire_period = True
    comments_texts = ["Time of publications"]
    image_urls = []
    activity_description = eco_spold.activityDataset.activityDescription
    time_period = activity_description.timePeriod[0]

    assert time_period.startDate == start_date
    assert time_period.endDate == end_date
    assert time_period.isDataValidForEntirePeriod == is_data_valid_for_entire_period
    assert time_period.comments[0].texts == comments_texts
    assert time_period.comments[0].imageUrls == image_urls


def test_parse_file_v2_macro_economic_scenario(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    macro_economic_scenario_id = "d9f57f0a-a01f-42eb-a57b-8f18d6635801"
    macro_economic_scenario_context_id = ""
    names = ["Business-as-Usual"]
    comments = []
    activity_description = eco_spold.activityDataset.activityDescription
    macro_economic_scenario = activity_description.macroEconomicScenario[0]

    assert macro_economic_scenario.macroEconomicScenarioId == macro_economic_scenario_id
    assert (
        macro_economic_scenario.macroEconomicScenarioContextId
        == macro_economic_scenario_context_id
    )
    assert macro_economic_scenario.names == names
    assert macro_economic_scenario.comments == comments


def test_parse_file_v2_intermediate_exchange(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    exchange_id = "336dd4ef-cece-4c49-b412-5fe565ec8b8f"
    unit_id = "980b811e-3905-4797-82a5-173f5568bc7e"
    amount = 0
    production_volume_amount = 0
    names = ["heat, district or industrial, natural gas"]
    unit_names = ["MJ"]
    comments = ["Literature value."]
    intermediate_exchange_id = "1125e767-7b5d-442e-81d6-9b0d3e1919ac"
    group = 5
    group_type = "input"
    group_str = "From Technosphere (unspecified)"
    out_group = 0
    out_group_str = "ReferenceProduct"
    classifications_len = 1
    production_volume_uncertainties_len = 0
    intermediate_exchanges = eco_spold.activityDataset.flowData.intermediateExchanges
    intermediate_exchange = intermediate_exchanges[1]
    intermediate_exchange_out = intermediate_exchanges[6]

    assert intermediate_exchange.id == exchange_id
    assert intermediate_exchange.unitId == unit_id
    assert intermediate_exchange.amount == amount
    assert intermediate_exchange.productionVolumeAmount == production_volume_amount
    assert intermediate_exchange.intermediateExchangeId == intermediate_exchange_id
    assert intermediate_exchange.group == group
    assert intermediate_exchange.groupType == group_type
    assert intermediate_exchange.groupStr == group_str
    assert intermediate_exchange.names == names
    assert intermediate_exchange.unitNames == unit_names
    assert intermediate_exchange.comments == comments

    assert intermediate_exchange_out.group == out_group
    assert intermediate_exchange_out.groupStr == out_group_str

    assert isinstance(intermediate_exchange.uncertainties[0], Uncertainty)
    assert len(intermediate_exchange.classifications) == classifications_len
    assert (
        len(intermediate_exchange.productionVolumeUncertainties)
        == production_volume_uncertainties_len
    )


def test_parse_file_v2_elementary_exchange(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    exchange_id = "719770d0-4b1e-4c44-bd9e-72c4687a6ee0"
    unit_id = "487df68b-4994-4027-8fdc-a4dc298257b7"
    amount = 0.0011
    is_calculated_amount = False
    source_id_overwritten_by_child = False
    specific_allocation_property_id = ""
    specific_allocation_property_id_overwritten_by_child = False
    specific_allocation_property_context_id = ""
    elementary_exchange_id = "70d467b6-115e-43c5-add2-441de9411348"
    names = ["BOD5, Biological Oxygen Demand"]
    unit_names = ["kg"]
    comments = [
        "Calculation. This value was calculated from the amount of methyl formate in "
        "the treated waste water assuming a carbon conversion of 96% for COD. "
        "The worst case scenario, BOD=COD, was used. "
        "It is assumed that the manufacturing plant is located in an "
        "urban/industrial area and consequently the emissions are categorised as "
        "emanating in a high population density area. The emissions into water are "
        "assumed to be emitted into rivers."
    ]
    group = 4
    group_type = "output"
    group_str = "ToEnvironment"
    in_group = 4
    in_group_str = "FromEnvironment"
    synonyms = []
    tags = []
    properties_len = 0
    transfer_coefficients_len = 0
    elementary_exchanges = eco_spold.activityDataset.flowData.elementaryExchanges
    elementary_exchange = elementary_exchanges[0]
    elementary_exchange_in = elementary_exchanges[1]

    assert elementary_exchange.id == exchange_id
    assert elementary_exchange.unitId == unit_id
    assert elementary_exchange.amount == amount
    assert elementary_exchange.isCalculatedAmount == is_calculated_amount
    assert (
        elementary_exchange.sourceIdOverwrittenByChild == source_id_overwritten_by_child
    )
    assert (
        elementary_exchange.specificAllocationPropertyId
        == specific_allocation_property_id
    )
    assert (
        elementary_exchange.specificAllocationPropertyIdOverwrittenByChild
        == specific_allocation_property_id_overwritten_by_child
    )
    assert (
        elementary_exchange.specificAllocationPropertyContextId
        == specific_allocation_property_context_id
    )
    assert elementary_exchange.elementaryExchangeId == elementary_exchange_id
    assert elementary_exchange.names == names
    assert elementary_exchange.unitNames == unit_names
    assert elementary_exchange.comments == comments
    assert elementary_exchange.group == group
    assert elementary_exchange.groupType == group_type
    assert elementary_exchange.groupStr == group_str
    assert elementary_exchange.synonyms == synonyms
    assert elementary_exchange.tags == tags

    assert elementary_exchange_in.group == in_group
    assert elementary_exchange_in.groupStr == in_group_str

    assert isinstance(elementary_exchange.uncertainties[0], Uncertainty)
    assert len(elementary_exchange.properties) == properties_len
    assert len(elementary_exchange.transferCoefficients) == transfer_coefficients_len


def test_parse_file_v2_uncertainty(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    flow_data = eco_spold.activityDataset.flowData
    uncertainty = flow_data.intermediateExchanges[1].uncertainties[0]

    assert uncertainty.triangular is None
    assert uncertainty.uniform is None
    assert uncertainty.beta is None
    assert uncertainty.gamma is None
    assert uncertainty.binomial is None
    assert uncertainty.undefined is None


def test_parse_file_v2_normal(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    mean_value = 0
    variance = 0
    variance_with_pedigree_uncertainty = 0
    flow_data = eco_spold.activityDataset.flowData
    uncertainty = flow_data.intermediateExchanges[1].uncertainties[0]
    normal = uncertainty.normal

    assert normal.meanValue == mean_value
    assert normal.variance == variance
    assert normal.varianceWithPedigreeUncertainty == variance_with_pedigree_uncertainty


def test_parse_file_v2_lognormal(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    mean_value = 0.6
    _mu = -0.51
    variance = 0.03
    variance_with_pedigree_uncertainty = 0.0707
    flow_data = eco_spold.activityDataset.flowData
    uncertainty = flow_data.intermediateExchanges[0].uncertainties[0]
    lognormal = uncertainty.lognormal

    assert lognormal.meanValue == mean_value
    assert lognormal.mu == _mu
    assert lognormal.variance == variance
    assert (
        lognormal.varianceWithPedigreeUncertainty == variance_with_pedigree_uncertainty
    )


def test_parse_file_v2_property(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    property_id = "c74c3729-e577-4081-b572-a283d2561a75"
    amount = 0.4
    is_defining_value = True
    unit_id = "577e242a-461f-44a7-922c-d8e1c3d2bf45"
    names = ["carbon content, fossil"]
    unit_names = ["dimensionless"]
    comments = ["CH2O"]
    uncertainties_len = 0
    flow_data = eco_spold.activityDataset.flowData
    prop = flow_data.intermediateExchanges[6].properties[0]

    assert prop.propertyId == property_id
    assert prop.amount == amount
    assert prop.isDefiningValue == is_defining_value
    assert prop.unitId == unit_id
    assert prop.names == names
    assert prop.unitNames == unit_names
    assert prop.comments == comments
    assert len(prop.uncertainties) == uncertainties_len


def test_parse_file_v2_compartment(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    sub_compartment_id = "963f8022-3e2e-4be9-ad4d-b3b7a2282099"
    compartments = ["water"]
    sub_compartments = ["surface water"]
    flow_data = eco_spold.activityDataset.flowData
    compartment = flow_data.elementaryExchanges[0].compartment

    assert compartment.subCompartmentId == sub_compartment_id
    assert compartment.compartments == compartments
    assert compartment.subCompartments == sub_compartments


def test_parse_file_v2_parameter(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    parameter_id = "e952df4c-1ca5-4710-9f53-be47be9191c1"
    variable_name = "fraction_CW_R_to_air"
    amount = 0.771
    names = ["fraction, cooling water, recirculating system, to air"]
    comments = [
        "Calculated based on literature value (Scown, C.D., 2011, Water Footprint "
        "of U.S. Transportation Fuels and supplying information of the article) "
        "(Vionnet, S., Quantis Water Database - Technical Report, 2012). "
    ]
    mean_value = 0.771
    _mu = -0.26
    variance = 0.04
    variance_with_pedigree_uncertainty = 0.0413
    flow_data = eco_spold.activityDataset.flowData
    parameter = flow_data.parameters[0]
    lognormal = parameter.uncertainties[0].lognormal

    assert parameter.parameterId == parameter_id
    assert parameter.variableName == variable_name
    assert parameter.amount == amount
    assert parameter.names == names
    assert parameter.comments == comments

    assert lognormal.meanValue == mean_value
    assert lognormal.mu == _mu
    assert lognormal.variance == variance
    assert (
        lognormal.varianceWithPedigreeUncertainty == variance_with_pedigree_uncertainty
    )


def test_parse_file_v2_representativeness(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    percent = 100
    system_model_id = "06590a66-662a-4885-8494-ad0cf410f956"
    system_model_names = ["Allocation, ecoinvent default"]
    sampling_procedures = ["Literature data"]
    extrapolations = [
        "This dataset has been extrapolated from year 2006 to the year of the "
        "calculation (2014). The uncertainty has been adjusted accordingly."
    ]
    modelling_and_validation = eco_spold.activityDataset.modellingAndValidation
    representativeness = modelling_and_validation.representativeness

    assert representativeness.percent == percent
    assert representativeness.systemModelId == system_model_id
    assert representativeness.systemModelNames == system_model_names
    assert representativeness.samplingProcedures == sampling_procedures
    assert representativeness.extrapolations == extrapolations


def test_parse_file_v2_data_entry_by(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    person_id = "4e412379-4901-477d-bbc1-3e2797ab9350"
    is_active_author = False
    person_name = "personName"
    person_email = "personEmail@domain.com"
    administrative_information = eco_spold.activityDataset.administrativeInformation
    data_entry_by = administrative_information.dataEntryBy

    assert data_entry_by.personId == person_id
    assert data_entry_by.isActiveAuthor == is_active_author
    assert data_entry_by.personName == person_name
    assert data_entry_by.personEmail == person_email


def test_parse_file_v2_data_generator_and_publication(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    person_id = "4e412379-4901-477d-bbc1-3e2797ab9350"
    person_name = "personName"
    person_email = "personEmail@domain.com"
    data_published_in = 2
    data_published_in_str = (
        "Data has been published entirely in 'referenceToPublishedSource'."
    )
    published_source_id = "71272329-1b17-415b-9f9b-299ebfbce109"
    published_source_year = "2007"
    published_source_first_author = "Sutter, J."
    is_copyright_protected = True
    page_numbers = "solvents"
    access_restricted_to = 1
    access_restricted_to_str = "Licensees"
    administrative_information = eco_spold.activityDataset.administrativeInformation
    data_generator_and_publication = (
        administrative_information.dataGeneratorAndPublication
    )

    assert data_generator_and_publication.personId == person_id
    assert data_generator_and_publication.personName == person_name
    assert data_generator_and_publication.personEmail == person_email
    assert data_generator_and_publication.dataPublishedIn == data_published_in
    assert data_generator_and_publication.dataPublishedInStr == data_published_in_str
    assert data_generator_and_publication.publishedSourceId == published_source_id
    assert data_generator_and_publication.publishedSourceYear == published_source_year
    assert (
        data_generator_and_publication.publishedSourceFirstAuthor
        == published_source_first_author
    )
    assert data_generator_and_publication.isCopyrightProtected == is_copyright_protected
    assert data_generator_and_publication.pageNumbers == page_numbers
    assert data_generator_and_publication.accessRestrictedTo == access_restricted_to
    assert (
        data_generator_and_publication.accessRestrictedToStr == access_restricted_to_str
    )


def test_parse_file_v2_file_attributes(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    major_release = 3
    minor_release = 0
    major_revision = 37
    minor_revision = 0
    internal_schema_version = "2.0.10"
    default_language = "en"
    creation_timestamp = datetime(2010, 7, 28, 18, 41, 6)
    last_edit_timestamp = datetime(2011, 9, 22, 18, 30, 49)
    file_generator = "EcoEditor 2.0.43.6348"
    file_timestamp = datetime(2011, 9, 22, 18, 30, 49)
    context_id = "de659012-50c4-4e96-b54a-fc781bf987ab"
    context_names = ["ecoinvent"]
    required_contexts_len = 0
    administrative_information = eco_spold.activityDataset.administrativeInformation
    file_attributes = administrative_information.fileAttributes

    assert file_attributes.majorRelease == major_release
    assert file_attributes.minorRelease == minor_release
    assert file_attributes.majorRevision == major_revision
    assert file_attributes.minorRevision == minor_revision
    assert file_attributes.internalSchemaVersion == internal_schema_version
    assert file_attributes.defaultLanguage == default_language
    assert file_attributes.creationTimestamp == creation_timestamp
    assert file_attributes.lastEditTimestamp == last_edit_timestamp
    assert file_attributes.fileGenerator == file_generator
    assert file_attributes.fileTimestamp == file_timestamp
    assert file_attributes.contextId == context_id
    assert file_attributes.contextNames == context_names
    assert len(file_attributes.requiredContexts) == required_contexts_len


def test_parse_file_v2_pedigree_matrix(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    reliability = 2
    reliability_str = (
        "Verified data partly based on assumptions OR nonverified data based on "
        "measurements"
    )
    completeness = 3
    completeness_str = (
        "Representative data from only some sites (<<50%) relevant for the market "
        "considered OR >50% of sites but from shorter periods"
    )
    temporal_correlation = 1
    temporal_correlation_str = (
        "Less than 3 years of difference to the time period of the dataset "
        "(fields 600-610)"
    )
    geographical_correlation = 3
    geographical_correlation_str = "Data from area with similar production conditions"
    further_technology_correlation = 1
    further_technology_correlation_str = (
        "Data from enterprises, processes and materials under study"
    )
    flow_data = eco_spold.activityDataset.flowData
    parameter = flow_data.parameters[0]
    pedigree_matrix = parameter.uncertainties[0].pedigreeMatrices[0]

    assert pedigree_matrix.reliability == reliability
    assert pedigree_matrix.reliabilityStr == reliability_str
    assert pedigree_matrix.completeness == completeness
    assert pedigree_matrix.completenessStr == completeness_str
    assert pedigree_matrix.temporalCorrelation == temporal_correlation
    assert pedigree_matrix.temporalCorrelationStr == temporal_correlation_str
    assert pedigree_matrix.geographicalCorrelation == geographical_correlation
    assert pedigree_matrix.geographicalCorrelationStr == geographical_correlation_str
    assert (
        pedigree_matrix.furtherTechnologyCorrelation == further_technology_correlation
    )
    assert (
        pedigree_matrix.furtherTechnologyCorrelationStr
        == further_technology_correlation_str
    )
