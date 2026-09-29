"""Internal helper classes."""

from typing import Any, Callable, Optional

from .config import Defaults
from .lxmlh import create_attribute, create_attribute_list, create_element_text
from .lxmlh.helpers import T, XmlProperty


def create_attribute_v1(
    name: str, attr_type: type[T], validator: Optional[Callable[[Any], str]] = None
) -> XmlProperty[T]:
    """Create a property for an attribute of an EcoSpold v1 element.

    Args:
        name: XML attribute name.
        attr_type: Python type the value is read as.
        validator: normalises a value before it is written.

    Returns:
        The property.
    """
    return create_attribute(name, attr_type, Defaults.SCHEMA_V1_FILE, validator)


def create_attribute_v2(
    name: str, attr_type: type[T], validator: Optional[Callable[[Any], str]] = None
) -> XmlProperty[T]:
    """Create a property for an attribute of an EcoSpold v2 element.

    Args:
        name: XML attribute name.
        attr_type: Python type the value is read as.
        validator: normalises a value before it is written.

    Returns:
        The property.
    """
    return create_attribute(name, attr_type, Defaults.SCHEMA_V2_FILE, validator)


def create_attribute_list_v1(name: str, attr_type: type[T]) -> XmlProperty[list[T]]:
    """Create a property for a list of child texts of an EcoSpold v1 element.

    Args:
        name: XML child element name.
        attr_type: Python type each value is read as.

    Returns:
        The property.
    """
    return create_attribute_list(name, attr_type, Defaults.SCHEMA_V1_FILE)


def create_attribute_list_v2(name: str, attr_type: type[T]) -> XmlProperty[list[T]]:
    """Create a property for a list of child texts of an EcoSpold v2 element.

    Args:
        name: XML child element name.
        attr_type: Python type each value is read as.

    Returns:
        The property.
    """
    return create_attribute_list(name, attr_type, Defaults.SCHEMA_V2_FILE)


def create_element_text_v1(name: str, element_type: type[T]) -> XmlProperty[T]:
    """Create a property for a child's text in an EcoSpold v1 element.

    Args:
        name: XML child element name.
        element_type: Python type the text is read as.

    Returns:
        The property.
    """
    return create_element_text(name, element_type, Defaults.SCHEMA_V1_FILE)


def create_element_text_v2(name: str, element_type: type[T]) -> XmlProperty[T]:
    """Create a property for a child's text in an EcoSpold v2 element.

    Args:
        name: XML child element name.
        element_type: Python type the text is read as.

    Returns:
        The property.
    """
    return create_element_text(name, element_type, Defaults.SCHEMA_V2_FILE)
