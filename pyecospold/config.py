"""Defaults configuration."""

import configparser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, ClassVar, Union

from lxml import etree

from . import __version__, lxmlh


@dataclass
class Defaults:
    """Default values that pyecospold fills in when an attribute has none.

    Override them, fully or partially, with ``config_defaults``.

    Attributes:
        SCHEMA_DIR: directory with the bundled XSD schemas.
        SCHEMA_V1_FILE: XSD that EcoSpold v1 files are validated against.
        SCHEMA_V2_FILE: XSD that EcoSpold v2 files are validated against.
        TYPE_DEFAULTS: value read for a missing attribute, per Python type.
        DYNAMIC_DEFAULTS: functions computing default values, per class and
            attribute.
        STATIC_DEFAULTS: fixed default values, per class and attribute.
    """

    SCHEMA_DIR: ClassVar[str] = str(Path(__file__).parent.resolve() / "schemas")
    SCHEMA_V1_FILE: ClassVar[str] = str(Path(SCHEMA_DIR, "v1", "EcoSpold01Dataset.xsd"))
    SCHEMA_V2_FILE: ClassVar[str] = str(Path(SCHEMA_DIR, "v2", "EcoSpold02.xsd"))

    TYPE_DEFAULTS: ClassVar[dict[type, Any]] = lxmlh.TYPE_DEFAULTS

    DYNAMIC_DEFAULTS: ClassVar[
        dict[str, dict[str, Callable[[etree.ElementBase], str]]]
    ] = {
        "Dataset": {
            "generator": lambda _: f"pyecospold.{__version__}",
        },
    }
    STATIC_DEFAULTS: ClassVar[dict[str, dict[str, str]]] = {
        "Allocation": {
            "allocationMethod": "-1",
        },
        "DataEntryBy": {
            "qualityNetwork": "1",
        },
        "DataGeneratorAndPublication": {
            "dataPublishedIn": "0",
        },
        "Dataset": {
            "validCompanyCodes": "CompanyCodes.xml",
            "validRegionalCodes": "RegionalCodes.xml",
            "validCategories": "Categories.xml",
            "validUnits": "Units.xml",
        },
        "DataSetInformation": {
            "impactAssessmentResult": "false",
            "internalVersion": "1.0",
            "version": "1.0",
        },
        "Exchange": {
            "uncertaintyType": "1",
        },
        "FileAttributes": {
            "defaultLanguage": "en",
        },
        "PedigreeMatrix": {
            "reliability": "5",
        },
        "ReferenceFunction": {
            "infrastructureProcess": "true",
        },
    }

    @classmethod
    def config_defaults(cls, config_file: Union[str, Path]) -> None:
        """Override the defaults, fully or partially, from a config file.

        Args:
            config_file: path to the INI config file.
        """
        config = configparser.ConfigParser()
        config.optionxform = lambda optionstr: optionstr
        config.read(config_file)

        if config.has_section("parameters"):
            for key, value in dict(config["parameters"]).items():
                setattr(cls, key, value)

        static_defaults = {
            name: dict(section)
            for name, section in config.items()
            if name != "parameters"
        }
        cls.static_defaults = static_defaults
