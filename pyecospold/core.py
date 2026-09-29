"""Core Ecospold module containing parsing and saving functionalities."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Union

from lxml import etree
from typing_extensions import override

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
    Binomial,
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
    Undefined,
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


class EcospoldLookupV1(etree.CustomElementClassLookup):
    """Custom XML lookup class for Ecospold V1 files."""

    @override
    def lookup(
        self,
        type: str,
        doc: object,
        namespace: Union[str, None],
        name: Union[str, None],
    ) -> Union[type[etree.ElementBase], None]:
        """Return the pyecospold class for an XML element.

        lxml calls this for every element it parses.

        Args:
            type: kind of node (``"element"``, ``"comment"``, ...).
            doc: lxml's internal document object.
            namespace: namespace of the element.
            name: tag name of the element.

        Returns:
            The class for ``name``, or None to let lxml choose.
        """
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

    @override
    def lookup(
        self,
        type: str,
        doc: object,
        namespace: Union[str, None],
        name: Union[str, None],
    ) -> Union[type[etree.ElementBase], None]:
        """Return the pyecospold class for an XML element.

        lxml calls this for every element it parses.

        Args:
            type: kind of node (``"element"``, ``"comment"``, ...).
            doc: lxml's internal document object.
            namespace: namespace of the element.
            name: tag name of the element.

        Returns:
            The class for ``name``, or None to let lxml choose.
        """
        lookupmap = {
            "activity": Activity,
            "activityDataset": ActivityDataset,
            "activityDescription": ActivityDescription,
            "administrativeInformation": AdministrativeInformationV2,
            "allocationComment": TextAndImage,
            "childActivityDataset": ActivityDataset,
            "beta": Beta,
            "binomial": Binomial,
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
            "productionVolumeUncertainty": Uncertainty,
            "parameter": Parameter,
            "pedigreeMatrix": PedigreeMatrix,
            "property": Property,
            "representativeness": RepresentativenessV2,
            "requiredContext": RequiredContextReference,
            "review": Review,
            "technology": TechnologyV2,
            "timePeriod": TimePeriodV2,
            "transferCoefficient": TransferCoefficient,
            "triangular": Triangular,
            "uncertainty": Uncertainty,
            "undefined": Undefined,
            "uniform": Uniform,
        }
        return lookupmap.get(name or "")


def parse_file_v1(file: Union[str, Path, IO[str], IO[bytes]]) -> EcoSpoldV1:
    """Parse an EcoSpold v1 file.

    Args:
        file: path to the EcoSpold file, or an open file object.

    Returns:
        The root ``EcoSpold`` element.
    """
    return parse_file(file, Defaults.SCHEMA_V1_FILE, EcospoldLookupV1())


def parse_file_v2(file: Union[str, Path, IO[str], IO[bytes]]) -> EcoSpoldV2:
    """Parse an EcoSpold v2 file.

    Args:
        file: path to the EcoSpold file, or an open file object.

    Returns:
        The root ``EcoSpold`` element.
    """
    return parse_file(file, Defaults.SCHEMA_V2_FILE, EcospoldLookupV2())


def validate_file_v1(
    file: Union[str, Path, IO[str], IO[bytes]],
) -> Union[etree._ListErrorLog, None]:
    """Validate an EcoSpold v1 file against its schema.

    Args:
        file: path to the EcoSpold file, or an open file object.

    Returns:
        None if the file is valid, otherwise lxml's log of validation errors.
    """
    return validate_file(file, Defaults.SCHEMA_V1_FILE)


def validate_file_v2(
    file: Union[str, Path, IO[str], IO[bytes]],
) -> Union[etree._ListErrorLog, None]:
    """Validate an EcoSpold v2 file against its schema.

    Args:
        file: path to the EcoSpold file, or an open file object.

    Returns:
        None if the file is valid, otherwise lxml's log of validation errors.
    """
    return validate_file(file, Defaults.SCHEMA_V2_FILE)


def parse_directory_v1(
    dir_path: Union[str, Path], valid_suffixes: Union[list[str], None] = None
) -> list[tuple[Path, EcoSpoldV1]]:
    """Parse every EcoSpold v1 file in a directory.

    Args:
        dir_path: directory with EcoSpold v1 files.
        valid_suffixes: file suffixes to parse; defaults to
            ``[".xml", ".spold"]``.

    Returns:
        ``(path, EcoSpold)`` for each parsed file.
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
    dir_path: Union[str, Path], valid_suffixes: Union[list[str], None] = None
) -> list[tuple[Path, EcoSpoldV2]]:
    """Parse every EcoSpold v2 file in a directory.

    Args:
        dir_path: directory with EcoSpold v2 files.
        valid_suffixes: file suffixes to parse; defaults to
            ``[".xml", ".spold"]``.

    Returns:
        ``(path, EcoSpold)`` for each parsed file.
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
    dir_path: Union[str, Path], valid_suffixes: Union[list[str], None] = None
) -> list[tuple[Path, Union[etree._ListErrorLog, None]]]:
    """Validate every EcoSpold v1 file in a directory.

    Args:
        dir_path: directory with EcoSpold v1 files.
        valid_suffixes: file suffixes to validate; defaults to
            ``[".xml", ".spold"]``.

    Returns:
        ``(path, errors)`` for each file; errors is None for a valid file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return validate_directory(
        dir_path, Defaults.SCHEMA_V1_FILE, valid_suffixes=valid_suffixes
    )


def validate_directory_v2(
    dir_path: Union[str, Path], valid_suffixes: Union[list[str], None] = None
) -> list[tuple[Path, Union[etree._ListErrorLog, None]]]:
    """Validate every EcoSpold v2 file in a directory.

    Args:
        dir_path: directory with EcoSpold v2 files.
        valid_suffixes: file suffixes to validate; defaults to
            ``[".xml", ".spold"]``.

    Returns:
        ``(path, errors)`` for each file; errors is None for a valid file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return validate_directory(
        dir_path, Defaults.SCHEMA_V2_FILE, valid_suffixes=valid_suffixes
    )


def parse_zip_file_v1(
    file_path: Union[str, Path], valid_suffixes: Union[list[str], None] = None
) -> list[tuple[Path, EcoSpoldV1]]:
    """Parse every EcoSpold v1 file in a ZIP archive.

    Args:
        file_path: ZIP archive with EcoSpold v1 files.
        valid_suffixes: file suffixes to parse; defaults to
            ``[".xml", ".spold"]``.

    Returns:
        ``(path, EcoSpold)`` for each parsed file.
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
    file_path: Union[str, Path], valid_suffixes: Union[list[str], None] = None
) -> list[tuple[Path, EcoSpoldV2]]:
    """Parse every EcoSpold v2 file in a ZIP archive.

    Args:
        file_path: ZIP archive with EcoSpold v2 files.
        valid_suffixes: file suffixes to parse; defaults to
            ``[".xml", ".spold"]``.

    Returns:
        ``(path, EcoSpold)`` for each parsed file.
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
    file_path: Union[str, Path], valid_suffixes: Union[list[str], None] = None
) -> list[tuple[Path, Union[etree._ListErrorLog, None]]]:
    """Validate every EcoSpold v1 file in a ZIP archive.

    Args:
        file_path: ZIP archive with EcoSpold v1 files.
        valid_suffixes: file suffixes to validate; defaults to
            ``[".xml", ".spold"]``.

    Returns:
        ``(path, errors)`` for each file; errors is None for a valid file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return validate_zip_file(
        file_path, Defaults.SCHEMA_V1_FILE, valid_suffixes=valid_suffixes
    )


def validate_zip_file_v2(
    file_path: Union[str, Path], valid_suffixes: Union[list[str], None] = None
) -> list[tuple[Path, Union[etree._ListErrorLog, None]]]:
    """Validate every EcoSpold v2 file in a ZIP archive.

    Args:
        file_path: ZIP archive with EcoSpold v2 files.
        valid_suffixes: file suffixes to validate; defaults to
            ``[".xml", ".spold"]``.

    Returns:
        ``(path, errors)`` for each file; errors is None for a valid file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml", ".spold"]

    return validate_zip_file(
        file_path, Defaults.SCHEMA_V2_FILE, valid_suffixes=valid_suffixes
    )


def save_ecospold_file(
    root: etree.ElementBase, path: Union[str, Path], fill_defaults: bool = False
) -> None:
    """Save an EcoSpold element tree to an XML file.

    Args:
        root: root ``EcoSpold`` element of the tree to save.
        path: where to write the file.
        fill_defaults: fill empty attributes from ``Defaults`` before saving.
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
