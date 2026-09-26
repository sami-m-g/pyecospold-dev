"""Helpers for mapping XML elements to Python classes with lxml."""

from .config import TYPE_DEFAULTS, TYPE_FUNC_MAP
from .helpers import (
    create_attribute,
    create_attribute_list,
    create_element_text,
    fill_in_defaults,
    get_element,
    get_element_list,
    get_inner_text_list,
)
from .parsers import (
    parse_directory,
    parse_file,
    parse_zip_file,
    save_file,
    validate_directory,
    validate_file,
    validate_zip_file,
)

__all__ = (
    "TYPE_DEFAULTS",
    "TYPE_FUNC_MAP",
    "__version__",
    "create_attribute",
    "create_attribute_list",
    "create_element_text",
    "fill_in_defaults",
    "get_element",
    "get_element_list",
    "get_inner_text_list",
    "parse_directory",
    "parse_file",
    "parse_zip_file",
    "save_file",
    "validate_directory",
    "validate_file",
    "validate_zip_file",
)
