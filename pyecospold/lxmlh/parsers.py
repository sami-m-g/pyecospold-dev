"""Parse, validate and save XML files, directories and zip archives."""

import tempfile
import zipfile
from collections.abc import Callable
from io import StringIO
from pathlib import Path

from lxml import etree, objectify

from .helpers import fill_in_defaults


def parse_file(
    file: str | Path | StringIO,
    schema_path: str,
    lookup: etree.CustomElementClassLookup,
) -> etree.ElementBase:
    """Parses an XML file to custom classes.

    Parameters: file: the str|Path path to the XML file or its StringIO representation.
    schema_path: the path to the XSD schema file. lookup: the lookup class for mapping
    XML elements to python classes. Returns a custom ElementBase class representing the
    root of the XML file.
    """
    schema = etree.XMLSchema(file=schema_path)
    parser = objectify.makeparser(schema=schema)
    parser.set_element_class_lookup(lookup)
    return objectify.parse(file, parser).getroot()


def validate_file(
    file: str | Path | StringIO,
    schema_path: str,
) -> None | list[str]:
    """Validate a file against a given schema.

    Needed because the default parser doesn't provide any usable error context.
    Parameters: file: the str|Path path to the XML file or its StringIO representation.
    schema_path: the path to the XSD schema file. Returns ``None`` if the file
    validates, or a list of errors as strings.
    """
    schema = etree.XMLSchema(file=schema_path)
    doc = etree.parse(file)
    if not schema.validate(doc):
        return schema.error_log
    return None


def parse_directory(
    dir_path: str | Path,
    schema_path: str,
    lookup: etree.CustomElementClassLookup,
    valid_suffixes: list[str] | None = None,
) -> list[tuple[Path, etree.ElementBase]]:
    """Parses a directory of XML files to a list of custom Python classes.

    Parameters: dir_path: the directory path, should contain files of only the
    schema_path version. schema_path: the path to the XSD schema file. lookup: the
    lookup class for mapping XML elements to custom Python classes. valid_suffixes: a
    list of valid file suffixes which will only be considered for parsing. If None,
    defaults to [".xml"]. Returns a list of tuples of file paths and corresponding
    custom Python classes representing the root of the XML file.
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml"]

    dir_path = Path(dir_path).resolve()
    return [
        (
            file_path,
            parse_file(file=file_path, schema_path=schema_path, lookup=lookup),
        )
        for file_path in dir_path.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in valid_suffixes
    ]


def validate_directory(
    dir_path: str | Path,
    schema_path: str,
    valid_suffixes: list[str] | None = None,
) -> list[tuple[Path, None | list[str]]]:
    """Validates a directory of XML files against a given schema.

    Parameters: dir_path: the directory path, should contain files of only the
    schema_path version. schema_path: the path to the XSD schema file. valid_suffixes: a
    list of valid file suffixes which will only be considered for validating. If None,
    defaults to [".xml"].
    """
    if valid_suffixes is None:
        valid_suffixes = [".xml"]

    dir_path = Path(dir_path).resolve()
    return [
        (file_path, validate_file(file=file_path, schema_path=schema_path))
        for file_path in dir_path.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in valid_suffixes
    ]


def parse_zip_file(
    file_path: str | Path,
    schema_path: str,
    lookup: etree.CustomElementClassLookup,
    valid_suffixes: list[str] | None = None,
) -> list[tuple[Path, etree.ElementBase]]:
    """Parses a ZIP file of XML files to a list of custom Python classes.

    Parameters: file_path: the ZIP file path, should contain files of only the
    schema_path version. schema_path: the path to the XSD schema file. lookup: the
    lookup class for mapping XML elements to custom Python classes. valid_suffixes: a
    list of valid file suffixes which will only be considered for parsing. If None,
    defaults to [".xml"]. Returns a list of tuples of file paths and corresponding
    custom Python classes representing the root of the XML file.
    """
    with tempfile.TemporaryDirectory() as unzip_dir:
        with zipfile.ZipFile(file_path, "r") as zip_file:
            zip_file.extractall(unzip_dir)
            return parse_directory(unzip_dir, schema_path, lookup, valid_suffixes)


def validate_zip_file(
    file_path: str | Path,
    schema_path: str,
    valid_suffixes: list[str] | None = None,
) -> None:
    """Validates a ZIP file of XML files against a given schema.

    Parameters: dir_path: the ZIP file path, should contain files of only the
    schema_path version. schema_path: the path to the XSD schema file. valid_suffixes: a
    list of valid file suffixes which will only be considered for validating. If None,
    defaults to [".xml"].
    """
    with tempfile.TemporaryDirectory() as unzip_dir:
        with zipfile.ZipFile(file_path, "r") as zip_file:
            zip_file.extractall(unzip_dir)
            return validate_directory(unzip_dir, schema_path, valid_suffixes)


def save_file(
    root: etree.ElementBase,
    path: str,
    pretty_print: bool = True,
    xml_declaration: bool = True,
    encoding: str = "UTF-8",
    static_defaults: dict[str, dict[str, str]] = None,
    dynamic_defaults: dict[str, dict[str, Callable[[etree.ElementBase], str]]] = None,
) -> None:
    """Saves a custom class to an XML file.

    Parameters: root: the custom class representing the root of the XML file. path: the
    path to save the XML file.
    """
    if static_defaults is None:
        static_defaults = {}
    if dynamic_defaults is None:
        dynamic_defaults = {}

    if len(static_defaults) != 0 and len(dynamic_defaults) != 0:
        fill_in_defaults(root, static_defaults, dynamic_defaults)

    root = etree.ElementTree(root)
    root.write(
        path,
        pretty_print=pretty_print,
        xml_declaration=xml_declaration,
        encoding=encoding,
    )
