"""Test cases for the __core__ module."""

import os
import zipfile
from collections.abc import Callable
from io import StringIO
from pathlib import Path

from lxml import etree

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
from pyecospold.model_v1 import EcoSpold as EcoSpoldV1
from pyecospold.model_v2 import EcoSpold as EcoSpoldV2


def test_validate_file_v1_success() -> None:
    """It validates file successfully."""
    assert validate_file_v1("data/v1/v1_1.xml") is None


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


def test_validate_file_v2_success() -> None:
    """It validates file successfully."""
    assert validate_file_v2("data/v2/v2_1.xml") is None


def test_parse_directory_v1() -> None:
    """It reads all files successfully."""
    dir_path = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v1")
    files = [os.path.join(dir_path, "v1_1.xml"), os.path.join(dir_path, "v1_2.spold")]
    ecospold_list = sorted(parse_directory_v1(dir_path))

    assert len(ecospold_list) == 2
    assert ecospold_list[0][0] == Path(files[0])
    assert ecospold_list[1][0] == Path(files[1])
    assert ecospold_list[0][1].datasets[0].generator == "EcoAdmin 1.1.17.110"
    assert ecospold_list[1][1].datasets[0].generator == "EcoAdmin 1.1.17.110"


def test_parse_directory_v2() -> None:
    """It reads all files successfully."""
    dir_path = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v2")
    files = [os.path.join(dir_path, "v2_1.xml"), os.path.join(dir_path, "v2_2.spold")]
    ecospold_list = sorted(parse_directory_v2(dir_path))
    activity1 = ecospold_list[0][1].activityDataset.activityDescription.activity[0]
    activity2 = ecospold_list[1][1].activityDataset.activityDescription.activity[0]

    assert len(ecospold_list) == 2
    assert ecospold_list[0][0] == Path(files[0])
    assert ecospold_list[1][0] == Path(files[1])
    assert activity1.inheritanceDepth == 0
    assert activity2.inheritanceDepth == 0


def test_save_file(tmpdir) -> None:
    """It saves read file correctly."""
    input_path = "data/v1/v1_1.xml"
    meta_information = parse_file_v1(input_path)
    output_path = os.path.join(tmpdir, os.urandom(24).hex())
    save_ecospold_file(meta_information, output_path, fill_defaults=False)

    with open(input_path, encoding="utf-8") as input_file:
        with open(output_path, encoding="utf-8") as output_file:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            translated_output = output_file.read().translate(mapping)
            translated_input = input_file.read().translate(mapping)
            assert translated_output == translated_input


def test_save_file_defaults(tmpdir, fixtures_dir) -> None:
    """It saves read file correctly."""
    input_path = fixtures_dir / "v1" / "v1_1.xml"
    expected_output_path = fixtures_dir / "v1" / "v1_1_defaults.xml"
    meta_information = parse_file_v1(input_path)
    output_path = os.path.join(tmpdir, os.urandom(24).hex())
    save_ecospold_file(meta_information, output_path, fill_defaults=True)

    with open(expected_output_path, encoding="utf-8") as input_file:
        with open(output_path, encoding="utf-8") as output_file:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            translated_output = output_file.read().translate(mapping)
            translated_input = input_file.read().translate(mapping)
            assert translated_output == translated_input


def _validate_directory(
    dataset_version: int,
    validator: Callable[
        [str | Path, list[str] | None], list[tuple[Path, etree.ElementBase]]
    ],
) -> None:
    """It reads all files successfully."""
    dir_path = os.path.join(Path(__file__).parents[1], "data", f"v{dataset_version}")
    files = [
        os.path.join(dir_path, f"v{dataset_version}_1.xml"),
        os.path.join(dir_path, f"v{dataset_version}_2.spold"),
    ]
    result = sorted(validator(dir_path))

    assert len(result) == len(files)
    for i in range(2):
        assert str(result[i][0]) == str(files[i])
        assert result[i][1] is None


def test_validate_directory_v1() -> None:
    """It validates directory successfully."""
    _validate_directory(1, validate_directory_v1)


def test_validate_directory_v2() -> None:
    """It validates directory successfully."""
    _validate_directory(2, validate_directory_v2)


def __zip_data(tmpdir, data_dir: str, file_name: str = "data.zip") -> str:
    zip_file_path = os.path.join(tmpdir, file_name)
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(data_dir):
            for file in files:
                zip_file.write(os.path.join(root, file), file)
    return zip_file_path


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


def test_parse_zip_file_v1(tmpdir) -> None:
    """It reads zip file successfully."""
    zip_file_path = __zip_data(tmpdir, os.path.join("data", "v1"))
    _parse_zip_file(zip_file_path, parse_zip_file_v1, EcoSpoldV1)


def test_parse_zip_file_v2(tmpdir) -> None:
    """It reads zip file successfully."""
    zip_file_path = __zip_data(tmpdir, os.path.join("data", "v2"))
    _parse_zip_file(zip_file_path, parse_zip_file_v2, EcoSpoldV2)


def test_validate_zip_file_v1(tmpdir) -> None:
    """It validates zip file successfully."""
    zip_file_path = __zip_data(tmpdir, os.path.join("data", "v1"))
    for result in validate_zip_file_v1(zip_file_path):
        assert result[1] is None


def test_validate_zip_file_v2(tmpdir) -> None:
    """It validates zip file successfully."""
    zip_file_path = __zip_data(tmpdir, os.path.join("data", "v2"))
    for result in validate_zip_file_v2(zip_file_path):
        assert result[1] is None
