"""Values downstream packages read, pinned by hand.

Snapshots record everything; these state intent, so a snapshot update can't
silently change what bw2io's EcoSpold1 importer and ecoinvent_interface rely on.
"""

from datetime import date, datetime
from pathlib import Path

from pyecospold import parse_file_v1, parse_file_v2

NS_V1 = "{http://www.EcoInvent.org/EcoSpold01}"


def test_bw2io_ecospold1(fixtures_dir: Path) -> None:
    """The typed and lxml-element accesses of bw2io.extractors.ecospold1."""
    dataset = parse_file_v1(fixtures_dir / "v1" / "v1_1.xml").datasets[0]
    meta = dataset.metaInformation
    process = meta.processInformation
    reference = process.referenceFunction
    info = process.dataSetInformation
    admin = meta.administrativeInformation

    assert dataset.tag == f"{NS_V1}dataset"
    assert dataset.get("number") == "1"

    assert reference.name == "compost plant, open"
    assert reference.unit == "unit"
    assert (reference.category, reference.subCategory) == (
        "agricultural means of production",
        "buildings",
    )
    assert (reference.get("category"), reference.get("subCategory")) == (
        "agricultural means of production",
        "buildings",
    )
    assert reference.localName == "Kompostieranlage, offen"
    assert reference.localSubCategory == "Gebäude"
    assert reference.includedProcesses.startswith("Building materials required")
    assert reference.datasetRelatesToProduct is True
    assert reference.infrastructureProcess is True
    assert reference.infrastructureIncluded is True

    assert process.geography.text == "Values refer to the situtation in Switzerland."
    assert process.technology.text == "Refer to open plant composting."
    assert process.timePeriod.dataValidForEntirePeriod is True
    assert process.timePeriod.startDate == date(1999, 1, 1)
    assert process.timePeriod.endDate == date(1999, 12, 31)

    assert info.type == 1
    assert info.impactAssessmentResult is False
    assert (info.version, info.internalVersion) == ("1.3", "53.03")
    assert info.timestamp == datetime(2003, 9, 12, 10, 14, 36)
    assert (info.languageCode, info.localLanguageCode) == ("en", "de")
    assert info.energyValues == 0

    assert [person.number for person in admin.persons] == [309, 291]
    assert admin.persons[0].companyCode == "EMPA-SG"
    assert admin.persons[0].countryCode == "CH"
    assert admin.dataEntryBy.person == 309

    (source,) = meta.modellingAndValidation.sources
    assert source.number == 146
    assert source.sourceTypeStr == "Measurement on site"
    assert source.firstAuthor == "Nemecek, T."
    assert source.year == 2003
    assert source.title == "Life Cycle Inventories of Agricultural Production Systems"
    assert source.volumeNo == 15
    assert source.text == "CD-ROM"

    product, steel = dataset.flowData.exchanges
    assert product.groupsStr == ["ReferenceProduct"]
    assert product.infrastructureProcess is True
    assert steel.groupsStr == ["FromTechnosphere"]
    assert steel.number == 2156
    assert steel.name == "disposal, building, reinforcement steel, to recycling"
    assert (steel.location, steel.unit) == ("CH", "kg")
    assert steel.CASNumber == "007439-89-6"
    assert steel.formula == "Fe"
    assert steel.generalComment == "(2,3,1,1,1,5)"
    assert steel.referenceToSource == 0
    assert (steel.get("category"), steel.get("subCategory")) == (
        "waste management",
        "recycling",
    )
    assert steel.get("uncertaintyType") == "1"
    assert steel.get("meanValue") == "21200"
    assert steel.get("standardDeviation95") == "1.22"

    (allocation,) = dataset.flowData.allocations
    assert allocation.get("referenceToCoProduct") == "1"
    assert allocation.get("fraction") == "97.6"
    assert [(child.tag, child.text) for child in allocation.iterchildren()] == [
        (f"{NS_V1}referenceToInputOutput", "1")
    ]


def test_ecoinvent_interface_mapping(fixtures_dir: Path) -> None:
    """The accesses of ecoinvent_interface.mapping."""
    activity_dataset = parse_file_v2(fixtures_dir / "v2" / "v2_2.spold").activityDataset
    description = activity_dataset.activityDescription
    products = [
        exchange
        for exchange in activity_dataset.flowData.intermediateExchanges
        if exchange.groupStr == "ReferenceProduct" and exchange.amount
    ]

    assert description.activity[0].activityNames[0] == (
        "formic acid production, methyl formate route"
    )
    assert description.geography[0].shortNames[0] == "RER"
    assert [product.names[0] for product in products] == ["formic acid"]
    assert products[0].amount == 1.0
