"""Core Ecospold module containing parsing and saving functionalities."""

from __future__ import annotations

from typing import IO, TYPE_CHECKING

from lxml import etree

from .config import Defaults
from .lxmlh import (
    parse_directory,
    parse_file,
    parse_zip_file,
    save_file,
    validate_directory,
    validate_file,
    validate_zip_file,
)
from .model_v1 import AdministrativeInformation as AdministrativeInformationV1
from .model_v1 import (
    Allocation,
    Dataset,
    DataSetInformation,
    Exchange,
    MetaInformation,
    Person,
    ProcessInformation,
    ReferenceFunction,
    Source,
    Validation,
)
from .model_v1 import DataEntryBy as DataEntryByV1
from .model_v1 import DataGeneratorAndPublication as DataGeneratorAndPublicationV1
from .model_v1 import EcoSpold as EcoSpoldV1
from .model_v1 import FlowData as FlowDataV1
from .model_v1 import Geography as GeographyV1
from .model_v1 import ModellingAndValidation as ModellingAndValidationV1
from .model_v1 import Representativeness as RepresentativenessV1
from .model_v1 import Technology as TechnologyV1
from .model_v1 import TimePeriod as TimePeriodV1
from .model_v2 import (
    Activity,
    ActivityDataset,
    ActivityDescription,
    Beta,
    Classification,
    Compartment,
    ElementaryExchange,
    FileAttributes,
    Gamma,
    ImpactIndicator,
    IntermediateExchange,
    Lognormal,
    MacroEconomicScenario,
    Normal,
    Parameter,
    PedigreeMatrix,
    Property,
    RequiredContextReference,
    Review,
    TextAndImage,
    TransferCoefficient,
    Triangular,
    Uncertainty,
    Uniform,
)
from .model_v2 import AdministrativeInformation as AdministrativeInformationV2
from .model_v2 import DataEntryBy as DataEntryByV2
from .model_v2 import DataGeneratorAndPublication as DataGeneratorAndPublicationV2
from .model_v2 import EcoSpold as EcoSpoldV2
from .model_v2 import FlowData as FlowDataV2
from .model_v2 import Geography as GeographyV2
from .model_v2 import ModellingAndValidation as ModellingAndValidationV2
from .model_v2 import Representativeness as RepresentativenessV2
from .model_v2 import Technology as TechnologyV2
from .model_v2 import TimePeriod as TimePeriodV2

if TYPE_CHECKING:
    from pathlib import Path


class EcospoldLookupV1(etree.CustomElementClassLookup):
    """Custom XML lookup class for Ecospold V1 files."""

    def lookup(
        self,
        type: str,  # noqa: A002 (lxml's signature)
        doc: object,
        namespace: str | None,
        name: str | None,
    ) -> type[etree.ElementBase] | None:
        """Maps Ecospold XML elements to custom Ecospold classes."""
        lookupmap = {
            "administrativeInformation": AdministrativeInformationV1,
            "allocation": Allocation,
            "dataEntryBy": DataEntryByV1,
            "dataGeneratorAndPublication": DataGeneratorAndPublicationV1,
            "dataset": Dataset,
            "dataSetInformation": DataSetInformation,
            "ecoSpold": EcoSpoldV1,
            "exchange": Exchange,
            "flowData": FlowDataV1,
            "geography": GeographyV1,
            "metaInformation": MetaInformation,
            "modellingAndValidation": ModellingAndValidationV1,
            "person": Person,
            "processInformation": ProcessInformation,
            "referenceFunction": ReferenceFunction,
            "representativeness": RepresentativenessV1,
            "source": Source,
            "technology": TechnologyV1,
            "timePeriod": TimePeriodV1,
            "validation": Validation,
        }
        return lookupmap.get(name or "")


class EcospoldLookupV2(etree.CustomElementClassLookup):
    """Custom XML lookup class for Ecospold V2 files."""

    def lookup(
        self,
        type: str,  # noqa: A002 (lxml's signature)
        doc: object,
        namespace: str | None,
        name: str | None,
    ) -> type[etree.ElementBase] | None:
        """Maps Ecospold XML elements to custom Ecospold classes."""
        lookupmap = {
            "activity": Activity,
            "activityDataset": ActivityDataset,
            "activityDescription": ActivityDescription,
            "administrativeInformation": AdministrativeInformationV2,
            "allocationComment": TextAndImage,
            "childActivityDataset": ActivityDataset,
            "beta": Beta,
            "classification": Classification,
            "comment": TextAndImage,
            "compartment": Compartment,
            "dataEntryBy": DataEntryByV2,
            "dataGeneratorAndPublication": DataGeneratorAndPublicationV2,
            "ecoSpold": EcoSpoldV2,
            "elementaryExchange": ElementaryExchange,
            "fileAttributes": FileAttributes,
            "flowData": FlowDataV2,
            "generalComment": TextAndImage,
            "gamma": Gamma,
            "geography": GeographyV2,
            "impactIndicator": ImpactIndicator,
            "intermediateExchange": IntermediateExchange,
            "lognormal": Lognormal,
            "macroEconomicScenario": MacroEconomicScenario,
            "modellingAndValidation": ModellingAndValidationV2,
            "normal": Normal,
            "parameter": Parameter,
            "pedigreeMatrix": PedigreeMatrix,
            "property": Property,
            "representativeness": RepresentativenessV2,
            "requiredContexts": RequiredContextReference,
            "review": Review,
            "technology": TechnologyV2,
            "timePeriod": TimePeriodV2,
            "transferCoefficient": TransferCoefficient,
            "triangular": Triangular,
            "uncertainty": Uncertainty,
            "uniform": Uniform,
        }
        return lookupmap.get(name or "")


def parse_file_v1(file: str | Path | IO[str] | IO[bytes]) -> EcoSpoldV1:
    """Parses an Ecospold V1 XML file to custom Ecospold classes.

    Parameters:
    file: the str|Path path to the Ecospold XML file or an open file object.

    Returns an EcoSpold class representing the root of the XML file.
    """
    return parse_file(file, Defaults.SCHEMA_V1_FILE, EcospoldLookupV1())


def parse_file_v2(file: str | Path | IO[str] | IO[bytes]) -> EcoSpoldV2:
    """Parses an Ecospold V2 XML file to custom Ecospold classes.

    Parameters:
    file: the str|Path path to the Ecospold XML file or an open file object.

    Returns an EcoSpold class representing the root of the XML file.
    """
    return parse_file(file, Defaults.SCHEMA_V2_FILE, EcospoldLookupV2())


def validate_file_v1(
    file: str | Path | IO[str] | IO[bytes],
) -> etree._ListErrorLog | None:
    """Validates an Ecospold V1 XML file to custom Ecospold classes.

    Parameters:
    file: the str|Path path to the Ecospold XML file or an open file object.

    Returns ``None`` if valid or a list of error strings.
    """
    return validate_file(file, Defaults.SCHEMA_V1_FILE)


def validate_file_v2(
    file: str | Path | IO[str] | IO[bytes],
) -> etree._ListErrorLog | None:
    """Parses an Ecospold V2 XML file to custom Ecospold classes.

    Parameters:
    file: the str|Path path to the Ecospold XML file or an open file object.

    Returns ``None`` if valid or a list of error strings.
    """
    return validate_file(file, Defaults.SCHEMA_V2_FILE)


def parse_directory_v1(
    dir_path: str | Path, valid_suffixes: list[str] | None = None
) -> list[tuple[Path, EcoSpoldV1]]:
    """Parses a directory of Ecospold XML files to a list of custom Ecospold classes.

    Parameters:
    dir_path: the directory path, should contain files of version 1 of EcoSpold.
    valid_suffixes: a list of valid file suffixes which will only be considered for
    parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding EcoSpold classes
    representing the root of the XML file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return parse_directory(
        dir_path=dir_path,
        schema_path=Defaults.SCHEMA_V1_FILE,
        lookup=EcospoldLookupV1(),
        valid_suffixes=valid_suffixes,
    )


def parse_directory_v2(
    dir_path: str | Path, valid_suffixes: list[str] | None = None
) -> list[tuple[Path, EcoSpoldV2]]:
    """Parses a directory of Ecospold XML files to a list of custom Ecospold classes.

    Parameters:
    dir_path: the directory path, should contain files of version 2 of EcoSpold.
    valid_suffixes: a list of valid file suffixes which will only be considered for
    parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding EcoSpold classes
    representing the root of the XML file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return parse_directory(
        dir_path=dir_path,
        schema_path=Defaults.SCHEMA_V2_FILE,
        lookup=EcospoldLookupV2(),
        valid_suffixes=valid_suffixes,
    )


def validate_directory_v1(
    dir_path: str | Path, valid_suffixes: list[str] | None = None
) -> list[tuple[Path, etree._ListErrorLog | None]]:
    """Validates an Ecospold V1 XML file to custom Ecospold classes.

    Parameters:
        dir_path: the directory path, should contain files of version 1 of EcoSpold.
        valid_suffixes: a list of valid file suffixes which will only be considered for
        parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding list of errors, which
    is ``None`` if no errors.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return validate_directory(
        dir_path, Defaults.SCHEMA_V1_FILE, valid_suffixes=valid_suffixes
    )


def validate_directory_v2(
    dir_path: str | Path, valid_suffixes: list[str] | None = None
) -> list[tuple[Path, etree._ListErrorLog | None]]:
    """Validates an Ecospold V1 XML file to custom Ecospold classes.

    Parameters:
        dir_path: the directory path, should contain files of version 2 of EcoSpold.
        valid_suffixes: a list of valid file suffixes which will only be considered for
        parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding list of errors, which
    is ``None`` if no errors.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return validate_directory(
        dir_path, Defaults.SCHEMA_V2_FILE, valid_suffixes=valid_suffixes
    )


def parse_zip_file_v1(
    file_path: str | Path, valid_suffixes: list[str] | None = None
) -> list[tuple[Path, EcoSpoldV1]]:
    """Parses a directory of Ecospold XML files to a list of custom Ecospold classes.

    Parameters:
    file_path: the ZIP file path, should contain files of version 1 of EcoSpold.
    valid_suffixes: a list of valid file suffixes which will only be considered for
    parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding EcoSpold classes
    representing the root of the XML file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return parse_zip_file(
        file_path=file_path,
        schema_path=Defaults.SCHEMA_V1_FILE,
        lookup=EcospoldLookupV1(),
        valid_suffixes=valid_suffixes,
    )


def parse_zip_file_v2(
    file_path: str | Path, valid_suffixes: list[str] | None = None
) -> list[tuple[Path, EcoSpoldV2]]:
    """Parses a directory of Ecospold XML files to a list of custom Ecospold classes.

    Parameters:
    file_path: the ZIP file path, should contain files of version 2 of EcoSpold.
    valid_suffixes: a list of valid file suffixes which will only be considered for
    parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding EcoSpold classes
    representing the root of the XML file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return parse_zip_file(
        file_path=file_path,
        schema_path=Defaults.SCHEMA_V2_FILE,
        lookup=EcospoldLookupV2(),
        valid_suffixes=valid_suffixes,
    )


def validate_zip_file_v1(
    file_path: str | Path, valid_suffixes: list[str] | None = None
) -> list[tuple[Path, etree._ListErrorLog | None]]:
    """Validates an Ecospold V1 XML file to custom Ecospold classes.

    Parameters:
        file_path: the ZIP file path, should contain files of version 1 of EcoSpold.
        valid_suffixes: a list of valid file suffixes which will only be considered for
        parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding list of errors, which
    is ``None`` if no errors.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return validate_zip_file(
        file_path, Defaults.SCHEMA_V1_FILE, valid_suffixes=valid_suffixes
    )


def validate_zip_file_v2(
    file_path: str | Path, valid_suffixes: list[str] | None = None
) -> list[tuple[Path, etree._ListErrorLog | None]]:
    """Validates an Ecospold V2 XML file to custom Ecospold classes.

    Parameters:
        file_path: the ZIP file path, should contain files of version 2 of EcoSpold.
        valid_suffixes: a list of valid file suffixes which will only be considered for
        parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding list of errors, which
    is ``None`` if no errors.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return validate_zip_file(
        file_path, Defaults.SCHEMA_V2_FILE, valid_suffixes=valid_suffixes
    )


def save_ecospold_file(
    root: etree.ElementBase, path: str | Path, *, fill_defaults: bool = False
) -> None:
    """Saves an Ecospold class to an XML file.

    Parameters:
    root: the EcoSpold class representing the root of the XML file.
    path: the path to save the Ecospold XML file.
    fill_defaults: whether to fill defaults values for attributes or not.
    """
    if not fill_defaults:
        static_defaults = None
        dynamic_defaults = None
    else:
        static_defaults = Defaults.STATIC_DEFAULTS
        dynamic_defaults = Defaults.DYNAMIC_DEFAULTS

    save_file(
        root, path, static_defaults=static_defaults, dynamic_defaults=dynamic_defaults
    )
