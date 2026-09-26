"""Test cases for the __core__ module."""

from collections.abc import Callable
from io import StringIO
from pathlib import Path

from lxml import etree

import pyecospold
from pyecospold import (
    parse_directory_v1,
    parse_directory_v2,
    parse_file_v1,
    parse_zip_file_v1,
    parse_zip_file_v2,
    save_ecospold_file,
    validate_directory_v1,
    validate_directory_v2,
    validate_file_v1,
    validate_file_v2,
    validate_zip_file_v1,
    validate_zip_file_v2,
)
from pyecospold.config import Defaults
from pyecospold.core import EcospoldLookupV1
from pyecospold.lxmlh import parse_directory, validate_directory
from pyecospold.model_v1 import EcoSpold as EcoSpoldV1
from pyecospold.model_v2 import EcoSpold as EcoSpoldV2


def test_validate_file_v1_success(fixtures_dir: Path) -> None:
    """It validates file successfully."""
    assert validate_file_v1(fixtures_dir / "v1" / "v1_1.xml") is None


def test_validate_file_v1_fail() -> None:
    """It validates file successfully."""
    xml = StringIO("<ecoSpold></ecoSpold>")
    error_expected = (
        "<string>:1:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_1: Element 'ecoSpold': "
        "No matching global declaration available for the validation root."
    )
    error_actual = validate_file_v1(xml)
    assert error_actual is not None
    assert str(error_actual[0]) == error_expected


def test_validate_file_v2_success(fixtures_dir: Path) -> None:
    """It validates file successfully."""
    assert validate_file_v2(fixtures_dir / "v2" / "v2_1.xml") is None


def test_parse_directory_v1(fixtures_dir: Path) -> None:
    """It reads all files successfully."""
    dir_path = fixtures_dir / "v1"
    files = [dir_path / "v1_1.xml", dir_path / "v1_2.spold"]
    ecospold_list = sorted(parse_directory_v1(dir_path))

    assert len(ecospold_list) == 2
    assert ecospold_list[0][0] == files[0]
    assert ecospold_list[1][0] == files[1]
    assert ecospold_list[0][1].datasets[0].generator == "EcoAdmin 1.1.17.110"
    assert ecospold_list[1][1].datasets[0].generator == "EcoAdmin 1.1.17.110"


def test_parse_directory_v2(fixtures_dir: Path) -> None:
    """It reads all files successfully."""
    dir_path = fixtures_dir / "v2"
    files = [dir_path / "v2_1.xml", dir_path / "v2_2.spold"]
    ecospold_list = sorted(parse_directory_v2(dir_path))
    activity1 = ecospold_list[0][1].activityDataset.activityDescription.activity[0]
    activity2 = ecospold_list[1][1].activityDataset.activityDescription.activity[0]

    assert len(ecospold_list) == 2
    assert ecospold_list[0][0] == files[0]
    assert ecospold_list[1][0] == files[1]
    assert activity1.inheritanceDepth == 0
    assert activity2.inheritanceDepth == 0


def test_save_file(
    tmp_path: Path,
    fixtures_dir: Path,
    compare_files: Callable[[Path, Path], bool],
) -> None:
    """It saves read file correctly."""
    input_path = fixtures_dir / "v1" / "v1_1.xml"
    output_path = tmp_path / "v1_1.xml"
    save_ecospold_file(parse_file_v1(input_path), output_path, fill_defaults=False)

    assert compare_files(input_path, output_path)


def test_save_file_defaults(
    tmp_path: Path,
    fixtures_dir: Path,
    compare_files: Callable[[Path, Path], bool],
) -> None:
    """It saves read file correctly."""
    input_path = fixtures_dir / "v1" / "v1_1.xml"
    output_path = tmp_path / "v1_1.xml"
    save_ecospold_file(parse_file_v1(input_path), output_path, fill_defaults=True)

    assert compare_files(fixtures_dir / "expected" / "v1_1_defaults.xml", output_path)


def _validate_directory(
    fixtures_dir: Path,
    dataset_version: int,
    validator: Callable[
        [str | Path, list[str] | None], list[tuple[Path, etree.ElementBase]]
    ],
) -> None:
    """It reads all files successfully."""
    dir_path = fixtures_dir / f"v{dataset_version}"
    files = [
        dir_path / f"v{dataset_version}_1.xml",
        dir_path / f"v{dataset_version}_2.spold",
    ]
    result = sorted(validator(dir_path))

    assert len(result) == len(files)
    for i in range(2):
        assert result[i][0] == files[i]
        assert result[i][1] is None


def test_validate_directory_v1(fixtures_dir: Path) -> None:
    """It validates directory successfully."""
    _validate_directory(fixtures_dir, 1, validate_directory_v1)


def test_validate_directory_v2(fixtures_dir: Path) -> None:
    """It validates directory successfully."""
    _validate_directory(fixtures_dir, 2, validate_directory_v2)


def _parse_zip_file(
    file_path: str,
    parser: Callable[
        [str | Path, list[str] | None], list[tuple[Path, etree.ElementBase]]
    ],
    root_class: etree.ElementBase,
) -> None:
    """It reads zip file successfully."""
    results = parser(file_path)

    for result in results:
        assert isinstance(result[1], root_class)


def test_parse_zip_file_v1(
    fixtures_dir: Path, make_zip: Callable[[Path], Path]
) -> None:
    """It reads zip file successfully."""
    zip_file_path = make_zip(fixtures_dir / "v1")
    _parse_zip_file(zip_file_path, parse_zip_file_v1, EcoSpoldV1)


def test_parse_zip_file_v2(
    fixtures_dir: Path, make_zip: Callable[[Path], Path]
) -> None:
    """It reads zip file successfully."""
    zip_file_path = make_zip(fixtures_dir / "v2")
    _parse_zip_file(zip_file_path, parse_zip_file_v2, EcoSpoldV2)


def test_validate_zip_file_v1(
    fixtures_dir: Path, make_zip: Callable[[Path], Path]
) -> None:
    """It validates zip file successfully."""
    zip_file_path = make_zip(fixtures_dir / "v1")
    for result in validate_zip_file_v1(zip_file_path):
        assert result[1] is None


def test_validate_zip_file_v2(
    fixtures_dir: Path, make_zip: Callable[[Path], Path]
) -> None:
    """It validates zip file successfully."""
    zip_file_path = make_zip(fixtures_dir / "v2")
    for result in validate_zip_file_v2(zip_file_path):
        assert result[1] is None


def _with_invalid_file(fixtures_dir: Path, directory: Path) -> Path:
    """Directory holding a valid v1 file and a copy with an invalid amount."""
    directory.mkdir()
    valid = (fixtures_dir / "v1" / "v1_1.xml").read_text(encoding="utf-8")
    (directory / "valid.xml").write_text(valid, encoding="utf-8")
    (directory / "invalid.xml").write_text(
        valid.replace('amount="1"', 'amount="abc"'), encoding="utf-8"
    )
    return directory


def test_validate_directory_reports_invalid_file(
    fixtures_dir: Path, tmp_path: Path
) -> None:
    """It reports the schema error of the invalid file only."""
    directory = _with_invalid_file(fixtures_dir, tmp_path / "files")
    results = dict(validate_directory_v1(directory))

    assert results[directory / "valid.xml"] is None
    assert "'abc'" in str(results[directory / "invalid.xml"][0])


def test_validate_zip_file_reports_invalid_file(
    fixtures_dir: Path, tmp_path: Path, make_zip: Callable[[Path], Path]
) -> None:
    """It reports the schema error of the invalid archived file only."""
    zip_path = make_zip(_with_invalid_file(fixtures_dir, tmp_path / "files"))
    results = {path.name: errors for path, errors in validate_zip_file_v1(zip_path)}

    assert results["valid.xml"] is None
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
