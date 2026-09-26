"""Test cases for the __config__ module."""

import os
from pathlib import Path

from pyecospold.config import Defaults


def test_config_defaults() -> None:
    """It overrides defaults variables."""
    root_dir = Path(__file__).parent.parent.resolve()

    config_file_dir = os.path.join(root_dir, "out", "tests")
    config_file_path = os.path.join(config_file_dir, "config.ini")
    os.makedirs(config_file_dir, exist_ok=True)

    schema_dir = os.path.join(root_dir, "pyecospold", "schemas")
    schema_v1_file = os.path.join(schema_dir, "v1", "EcoSpold01Dataset.xsd")
    schema_v2_file = os.path.join(schema_dir, "v2", "EcoSpold02.xsd")
    valid_company_codes = "CompanyCodes.xml"

    with open(config_file_path, "w", encoding="utf-8") as config_file:
        config_file.write("[parameters]\n")
        config_file.write(f"SCHEMA_V1_FILE={schema_v1_file}\n")
        config_file.write(f"SCHEMA_V2_FILE={schema_v2_file}\n\n")
        config_file.write(f"[Dataset]\nvalidCompanyCodes={valid_company_codes}\n")

    Defaults.config_defaults(config_file_path)

    assert (
        Defaults.STATIC_DEFAULTS["Dataset"]["validCompanyCodes"] == valid_company_codes
    )

    Defaults.config_defaults("config.init")
