"""Fixtures for pyecospold."""

import re
import shutil
from collections.abc import Callable
from io import BytesIO
from pathlib import Path
from xml.etree.ElementTree import canonicalize

import pytest

from pyecospold.core import parse_file_v1
from pyecospold.model_v1 import EcoSpold, TimePeriod


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Directory with the EcoSpold test files."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def eco_spold(fixtures_dir: Path) -> EcoSpold:
    """Parsed EcoSpold v1 sample file."""
    return parse_file_v1(fixtures_dir / "v1" / "v1_1.xml")


@pytest.fixture
def parse_time_period(fixtures_dir: Path) -> Callable[[str], TimePeriod]:
    """Factory parsing a v1 file whose `timePeriod` section is the given XML."""
    template = (fixtures_dir / "v1" / "v1_1.xml").read_text(encoding="utf-8")

    def parse(time_period_xml: str) -> TimePeriod:
        xml = re.sub(
            r"<timePeriod\b.*?</timePeriod>", time_period_xml, template, flags=re.DOTALL
        ).encode("utf-8")
        return (
            parse_file_v1(BytesIO(xml))
            .datasets[0]
            .metaInformation.processInformation.timePeriod
        )

    return parse


@pytest.fixture
def make_zip(tmp_path: Path) -> Callable[[Path], Path]:
    """Factory zipping a directory's files into an archive in tmp_path."""

    def make(directory: Path) -> Path:
        return Path(
            shutil.make_archive(str(tmp_path / directory.name), "zip", directory)
        )

    return make


@pytest.fixture(scope="session")
def canonical_xml() -> Callable[[Path], str]:
    """Canonical form (C14N 2.0) of an XML file, ignoring formatting whitespace."""
    return lambda path: canonicalize(from_file=path, strip_text=True)
