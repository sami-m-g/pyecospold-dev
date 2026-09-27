"""Property factories and accessors for XML attributes and elements."""

import re
from collections.abc import Callable
from typing import Any

from lxml import etree

from .config import TYPE_DEFAULTS, TYPE_FUNC_MAP


def set_attribute(
    element: etree.ElementBase,
    key: str,
    value: Any,
    schema_file: str,
    validator: Callable[[Any], str] | None,
) -> None:
    """Helper method for setting XML attributes.

    Raises DocumentInvalid exception on inappropriate setting according to XSD schema.
    """
    if validator is not None:
        value = validator(value)
    element.set(key, str(value))
    schema = etree.XMLSchema(file=schema_file)
    schema.assertValid(element.getroottree())


def set_attribute_list(
    element: etree.ElementBase, key: str, values: list[Any], schema_file: str
) -> None:
    """Helper method for setting XML list attributes.

    Raises DocumentInvalid exception on inappropriate setting according to XSD schema.
    """
    for old_value in get_element_list(element, key):
        element.remove(old_value)
    elements = []
    name_space = element.nsmap.get(None, "")
    for value in values:
        elements.append(etree.SubElement(element, f"{{{name_space}}}{key}"))
        elements[-1].text = str(value)
    element.extend(elements)
    schema = etree.XMLSchema(file=schema_file)
    schema.assertValid(element.getroottree())


def set_element_text(
    parent: etree.ElementBase, element: str, value: Any, schema_file: str
) -> None:
    """Helper method for setting XML element text.

    Raises DocumentInvalid exception on inappropriate setting according to XSD schema.
    """
    get_element(parent, element).text = str(value)
    schema = etree.XMLSchema(file=schema_file)
    schema.assertValid(parent.getroottree())


def get_element(parent: etree.ElementBase, element: str) -> Any:  # class set by lookup
    """Helper wrapper method for retrieving XML elements as custom XML classes."""
    return parent.find(element, namespaces=parent.nsmap)


def get_element_list(parent: etree.ElementBase, element: str) -> list[Any]:
    """Return the child elements with the given name.

    Helper wrapper method for retrieving XML list elements as a list of custom XML
    classes.
    """
    return parent.findall(element, namespaces=parent.nsmap)


def get_element_text(
    parent: etree.ElementBase, element: str, element_type: type = str
) -> str:
    """Helper wrapper method for retrieving XML element text as a string.

    Returns TYPE_DEFAULTS[str] if no text exists or element is None.
    """
    return TYPE_FUNC_MAP.get(element_type, element_type)(
        getattr(
            get_element(parent, element),
            "text",
            str(TYPE_DEFAULTS[str]),
        )
    )


def get_inner_text_list(parent: etree.ElementBase, element: str) -> list[str]:
    """Return the texts of the last nodes in a chain of XML elements.

    Helper wrapper method for retrieving the list of last nodes in a chain of XML
    elements.
    """
    inner_elements = get_element_list(parent, element)
    return [
        re.sub("[ ]{2,}", "", str(inner_element.text)).replace("\n", " ")
        for inner_element in inner_elements
    ]


def get_attribute(
    parent: etree.ElementBase, attribute: str, attr_type: type = str
) -> Any:
    """Helper wrapper method for retrieving XML attributes.

    Returns TYPE_DEFAULTS[type] if attribute doesn't exist.
    """
    return TYPE_FUNC_MAP.get(attr_type, attr_type)(
        parent.get(attribute, TYPE_DEFAULTS.get(attr_type, None))
    )


def get_attribute_list(
    parent: etree.ElementBase, attribute: str, attr_type: type = str
) -> list[Any]:
    """Helper wrapper method for retrieving XML list attributes.

    Returns empty list if attributes don't exist.
    """
    return [
        TYPE_FUNC_MAP.get(attr_type, attr_type)(
            re.sub("[\n]{1,}", " ", re.sub("[ ]{2,}", "", x.text))
        )
        for x in get_element_list(parent, attribute)
    ]


def create_attribute(
    name: str,
    attr_type: type,
    schema_file: str,
    validator: Callable[[Any], str] | None = None,
) -> Any:
    """Helper wrapper method for creating setters and getters for an attribute."""
    return property(
        fget=lambda self: get_attribute(self, name, attr_type),
        fset=lambda self, value: set_attribute(
            self, name, value, schema_file, validator
        ),
    )


def create_element_text(name: str, element_type: type, schema_file: str) -> Any:
    """Helper wrapper method for creating setters and getters for an element text."""
    return property(
        fget=lambda self: get_element_text(self, name, element_type),
        fset=lambda self, value: set_element_text(self, name, value, schema_file),
    )


def create_attribute_list(name: str, attr_type: type, schema_file: str) -> Any:
    """Helper wrapper method for creating setters and getters for an attribute list."""
    return property(
        fget=lambda self: get_attribute_list(self, name, attr_type),
        fset=lambda self, values: set_attribute_list(self, name, values, schema_file),
    )


def fill_in_defaults(
    node: etree.ElementBase,
    static_defaults: dict[str, dict[str, str]],
    dynamic_defaults: dict[str, dict[str, Callable[[Any], str]]],
) -> None:
    """Helper method for filling in defaults in all tree given any node."""
    root = node.getroottree()
    for child in root.iter():
        for defaults in [static_defaults, dynamic_defaults]:
            for key, value in defaults.get(child.__class__.__name__, {}).items():
                if getattr(child, key, TYPE_DEFAULTS[str]) in TYPE_DEFAULTS.values():
                    if isinstance(value, str):
                        setattr(child, key, value)
                    else:
                        setattr(child, key, value(child))
