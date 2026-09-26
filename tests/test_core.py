"""Test cases for the __core__ module."""

import re
import shutil
from collections.abc import Callable
from importlib import import_module
from io import StringIO
from pathlib import Path

import pytest

import pyecospold
from pyecospold import parse_file_v1, save_ecospold_file, validate_file_v1
from pyecospold.config import Defaults
from pyecospold.core import EcospoldLookupV1
from pyecospold.lxmlh import parse_directory, validate_directory


@pytest.fixture
def api(version: str) -> Callable[[str], Callable]:
    """Public function for the current version, e.g. ``api("parse_file")``."""
    return lambda name: getattr(pyecospold, f"{name}_{version}")


@pytest.fixture
def root_class(version: str) -> type:
    """Root element class for the current version."""
    return import_module(f"pyecospold.model_{version}").EcoSpold


@pytest.fixture(params=["directory", "zip_file"])
def kind(request: pytest.FixtureRequest) -> str:
    """Source kind; tests using it run for a directory and a zip file."""
    return request.param


@pytest.fixture
def as_source(kind: str, make_zip: Callable[[Path], Path]) -> Callable[[Path], Path]:
    """Passes a directory through as-is or zipped, matching ``kind``."""
    return make_zip if kind == "zip_file" else lambda directory: directory


@pytest.fixture
def files_with_invalid(fixtures_dir: Path, version: str, tmp_path: Path) -> Path:
    """Copy of the version's files plus an invalid copy of the first one."""
    directory = tmp_path / "files"
    shutil.copytree(fixtures_dir / version, directory)
    valid = (directory / f"{version}_1.xml").read_text(encoding="utf-8")
    (directory / "invalid.xml").write_text(
        re.sub(r'amount="[^"]*"', 'amount="abc"', valid, count=1), encoding="utf-8"
    )
    return directory


def test_validate_file_success(fixtures_dir: Path, version: str, api: Callable) -> None:
    """It validates file successfully."""
    assert api("validate_file")(fixtures_dir / version / f"{version}_1.xml") is None


def test_validate_file_v1_fail() -> None:
    """It reports why an invalid file fails validation."""
    xml = StringIO("<ecoSpold></ecoSpold>")
    error_expected = (
        "<string>:1:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_1: Element 'ecoSpold': "
        "No matching global declaration available for the validation root."
    )
    error_actual = validate_file_v1(xml)
    assert error_actual is not None
    assert str(error_actual[0]) == error_expected


def test_parse(
    fixtures_dir: Path,
    version: str,
    kind: str,
    api: Callable,
    as_source: Callable[[Path], Path],
    root_class: type,
) -> None:
    """It reads all files of a directory or zip file."""
    results = sorted(api(f"parse_{kind}")(as_source(fixtures_dir / version)))

    assert [path.name for path, _ in results] == [
        f"{version}_1.xml",
        f"{version}_2.spold",
    ]
    assert all(isinstance(root, root_class) for _, root in results)


@pytest.mark.parametrize("sample", ["1.xml", "2.spold"])
def test_save_file(
    tmp_path: Path,
    fixtures_dir: Path,
    version: str,
    sample: str,
    api: Callable,
    canonical_xml: Callable[[Path], str],
) -> None:
    """It writes back the file it read."""
    input_path = fixtures_dir / version / f"{version}_{sample}"
    output_path = tmp_path / input_path.name
    save_ecospold_file(api("parse_file")(input_path), output_path, fill_defaults=False)

    assert canonical_xml(output_path) == canonical_xml(input_path)


def test_save_file_defaults(
    tmp_path: Path,
    fixtures_dir: Path,
    canonical_xml: Callable[[Path], str],
) -> None:
    """It fills default values when saving."""
    input_path = fixtures_dir / "v1" / "v1_1.xml"
    output_path = tmp_path / "v1_1.xml"
    save_ecospold_file(parse_file_v1(input_path), output_path, fill_defaults=True)

    expected_path = fixtures_dir / "expected" / "v1_1_defaults.xml"
    assert canonical_xml(output_path) == canonical_xml(expected_path)


def test_validate(
    files_with_invalid: Path,
    version: str,
    kind: str,
    api: Callable,
    as_source: Callable[[Path], Path],
) -> None:
    """It reports schema errors of invalid files only."""
    results = {
        path.name: errors
        for path, errors in api(f"validate_{kind}")(as_source(files_with_invalid))
    }

    assert results.keys() == {f"{version}_1.xml", f"{version}_2.spold", "invalid.xml"}
    assert results[f"{version}_1.xml"] is None
    assert results[f"{version}_2.spold"] is None
    assert "'abc'" in str(results["invalid.xml"][0])


def test_save_file_fills_dynamic_defaults(fixtures_dir: Path, tmp_path: Path) -> None:
    """It stamps the generator when it is unset."""
    eco_spold = parse_file_v1(fixtures_dir / "v1" / "v1_1.xml")
    eco_spold.datasets[0].generator = ""
    output_path = tmp_path / "output.xml"
    save_ecospold_file(eco_spold, output_path, fill_defaults=True)

    generator = parse_file_v1(output_path).datasets[0].generator
    assert generator == f"pyecospold.{pyecospold.__version__}"


def test_lxmlh_directory_defaults_to_xml_suffix(fixtures_dir: Path) -> None:
    """Without suffixes, lxmlh only considers .xml files."""
    directory = fixtures_dir / "v1"
    parsed = parse_directory(directory, Defaults.SCHEMA_V1_FILE, EcospoldLookupV1())
    validated = validate_directory(directory, Defaults.SCHEMA_V1_FILE)

    assert [path.name for path, _ in parsed] == ["v1_1.xml"]
    assert validated == [(directory / "v1_1.xml", None)]
