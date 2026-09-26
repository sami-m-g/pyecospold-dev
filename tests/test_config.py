"""Test cases for the __config__ module."""

import copy
from pathlib import Path

import pytest

from pyecospold.config import Defaults


def test_config_defaults(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """It overrides defaults variables."""
    for name in ("SCHEMA_V1_FILE", "SCHEMA_V2_FILE", "STATIC_DEFAULTS"):
        monkeypatch.setattr(Defaults, name, copy.deepcopy(getattr(Defaults, name)))
    monkeypatch.setattr(Defaults, "static_defaults", None, raising=False)

    schema_dir = Path(Defaults.SCHEMA_DIR)
    valid_company_codes = "CompanyCodes.xml"
    config_file = tmp_path / "config.ini"
    config_file.write_text(
        "[parameters]\n"
        f"SCHEMA_V1_FILE={schema_dir / 'v1' / 'EcoSpold01Dataset.xsd'}\n"
        f"SCHEMA_V2_FILE={schema_dir / 'v2' / 'EcoSpold02.xsd'}\n\n"
        f"[Dataset]\nvalidCompanyCodes={valid_company_codes}\n",
        encoding="utf-8",
    )

    Defaults.config_defaults(config_file)

    assert (
        Defaults.STATIC_DEFAULTS["Dataset"]["validCompanyCodes"] == valid_company_codes
    )
