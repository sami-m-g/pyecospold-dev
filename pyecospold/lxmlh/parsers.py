"""Parse, validate and save XML files, directories and zip archives."""

import tempfile
import zipfile
from pathlib import Path
from typing import IO, Any, Callable, Union

from lxml import etree, objectify

from .helpers import fill_in_defaults


def parse_file(
    file: Union[str, Path, IO[str], IO[bytes]],
    schema_path: str,
    lookup: etree.CustomElementClassLookup,
) -> Any:  # noqa: ANN401 (class set by lookup)
    """Parse an XML file into the custom classes chosen by ``lookup``.

    Args:
        file: path to the XML file, or an open file object.
        schema_path: path to the XSD schema the file is validated against.
        lookup: maps XML elements to Python classes.

    Returns:
        The root element of the file, as the class the lookup chose.
    """
    schema = etree.XMLSchema(file=schema_path)
    parser = objectify.makeparser(schema=schema)
    parser.set_element_class_lookup(lookup)
    return objectify.parse(file, parser).getroot()


def validate_file(
    file: Union[str, Path, IO[str], IO[bytes]],
    schema_path: str,
) -> Union[etree._ListErrorLog, None]:
    """Validate an XML file against a schema.

    Needed because the default parser doesn't provide any usable error context.

    Args:
        file: path to the XML file, or an open file object.
        schema_path: path to the XSD schema.

    Returns:
        None if the file is valid, otherwise lxml's log of validation errors.
    """
    schema = etree.XMLSchema(file=schema_path)
    doc = etree.parse(file)
    if not schema.validate(doc):
        return schema.error_log
    return None


def parse_directory(
    dir_path: Union[str, Path],
    schema_path: str,
    lookup: etree.CustomElementClassLookup,
    valid_suffixes: Union[list[str], None] = None,
) -> list[tuple[Path, Any]]:
    """Parse every XML file in a directory.

    Args:
        dir_path: directory with files of a single schema version.
        schema_path: path to the XSD schema the files are validated against.
        lookup: maps XML elements to Python classes.
        valid_suffixes: file suffixes to parse; defaults to ``[".xml"]``.

    Returns:
        ``(path, root element)`` for each parsed file.
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
    dir_path: Union[str, Path],
    schema_path: str,
    valid_suffixes: Union[list[str], None] = None,
) -> list[tuple[Path, Union[etree._ListErrorLog, None]]]:
    """Validate every XML file in a directory against a schema.

    Args:
        dir_path: directory with files of a single schema version.
        schema_path: path to the XSD schema.
        valid_suffixes: file suffixes to validate; defaults to ``[".xml"]``.

    Returns:
        ``(path, errors)`` for each file; errors is None for a valid file.
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
    file_path: Union[str, Path],
    schema_path: str,
    lookup: etree.CustomElementClassLookup,
    valid_suffixes: Union[list[str], None] = None,
) -> list[tuple[Path, Any]]:
    """Parse every XML file in a ZIP archive.

    Args:
        file_path: ZIP archive with files of a single schema version.
        schema_path: path to the XSD schema the files are validated against.
        lookup: maps XML elements to Python classes.
        valid_suffixes: file suffixes to parse; defaults to ``[".xml"]``.

    Returns:
        ``(path, root element)`` for each parsed file.
    """
    with (
        tempfile.TemporaryDirectory() as unzip_dir,
        zipfile.ZipFile(file_path, "r") as zip_file,
    ):
        zip_file.extractall(unzip_dir)
        return parse_directory(unzip_dir, schema_path, lookup, valid_suffixes)


def validate_zip_file(
    file_path: Union[str, Path],
    schema_path: str,
    valid_suffixes: Union[list[str], None] = None,
) -> list[tuple[Path, Union[etree._ListErrorLog, None]]]:
    """Validate every XML file in a ZIP archive against a schema.

    Args:
        file_path: ZIP archive with files of a single schema version.
        schema_path: path to the XSD schema.
        valid_suffixes: file suffixes to validate; defaults to ``[".xml"]``.

    Returns:
        ``(path, errors)`` for each file; errors is None for a valid file.
    """
    with (
        tempfile.TemporaryDirectory() as unzip_dir,
        zipfile.ZipFile(file_path, "r") as zip_file,
    ):
        zip_file.extractall(unzip_dir)
        return validate_directory(unzip_dir, schema_path, valid_suffixes)


def save_file(
    root: etree.ElementBase,
    path: Union[str, Path],
    pretty_print: bool = True,
    xml_declaration: bool = True,
    encoding: str = "UTF-8",
    static_defaults: Union[dict[str, dict[str, str]], None] = None,
    dynamic_defaults: Union[
        dict[str, dict[str, Callable[[etree.ElementBase], str]]], None
    ] = None,
) -> None:
    """Save an element tree to an XML file.

    Defaults are filled in only when both ``static_defaults`` and
    ``dynamic_defaults`` are given.

    Args:
        root: root element of the tree to save.
        path: where to write the file.
        pretty_print: indent the output.
        xml_declaration: write the ``<?xml ...?>`` declaration.
        encoding: output encoding.
        static_defaults: fixed values to fill in, per class and attribute.
        dynamic_defaults: functions computing values to fill in, per class and
            attribute.
    """
    if static_defaults is None:
        static_defaults = {}
    if dynamic_defaults is None:
        dynamic_defaults = {}

    if len(static_defaults) != 0 and len(dynamic_defaults) != 0:
        fill_in_defaults(root, static_defaults, dynamic_defaults)

    tree = etree.ElementTree(root)
    tree.write(
        path,
        pretty_print=pretty_print,
        xml_declaration=xml_declaration,
        encoding=encoding,
    )
