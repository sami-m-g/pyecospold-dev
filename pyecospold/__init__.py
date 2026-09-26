"""Read, validate and write EcoSpold v1 and v2 XML files."""

__all__ = (
    "Defaults",
    "__version__",
    "parse_directory_v1",
    "parse_directory_v2",
    "parse_file_v1",
    "parse_file_v2",
    "parse_zip_file_v1",
    "parse_zip_file_v2",
    "save_ecospold_file",
    "validate_directory_v1",
    "validate_directory_v2",
    "validate_file_v1",
    "validate_file_v2",
    "validate_zip_file_v1",
    "validate_zip_file_v2",
)

from importlib.metadata import version as _version

__version__ = _version("pyecospold")

from .config import Defaults
from .core import (
    parse_directory_v1,
    parse_directory_v2,
    parse_file_v1,
    parse_file_v2,
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
