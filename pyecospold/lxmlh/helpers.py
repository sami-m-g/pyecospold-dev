"""Property factories and accessors for XML attributes and elements."""

import re
from typing import Any, Callable, Optional, Protocol, TypeVar, cast, overload

from lxml import etree

from .config import TYPE_DEFAULTS, TYPE_FUNC_MAP

T = TypeVar("T")


class XmlProperty(Protocol[T]):
    """Type of the properties built below: reading one on an element gives a ``T``.

    At runtime these are plain ``property`` objects; this protocol only tells
    type checkers what their getter returns.
    """

    @overload
    def __get__(self, obj: None, owner: type) -> "XmlProperty[T]": ...
    @overload
    def __get__(self, obj: object, owner: type) -> T: ...
    def __set__(self, obj: object, value: object) -> None:
        """Write the value to the XML; the schema validates it.

        Args:
            obj: element to write to.
            value: new value.
        """


def set_attribute(
    element: etree.ElementBase,
    key: str,
    value: object,
    schema_file: str,
    validator: Optional[Callable[[Any], str]],
) -> None:
    """Set an XML attribute, then validate the whole tree.

    Raises lxml's ``DocumentInvalid`` if the schema rejects the new value.

    Args:
        element: element to change.
        key: attribute name.
        value: new value, written as text.
        schema_file: XSD to validate against.
        validator: normalises the value before it is written.
    """
    if validator is not None:
        value = validator(value)
    element.set(key, str(value))
    schema = etree.XMLSchema(file=schema_file)
    schema.assertValid(element.getroottree())


def set_attribute_list(
    element: etree.ElementBase, key: str, values: list[Any], schema_file: str
) -> None:
    """Replace the child texts named ``key``, then validate the whole tree.

    Raises lxml's ``DocumentInvalid`` if the schema rejects the new values.

    Args:
        element: element to change.
        key: child element name.
        values: new values, written as text.
        schema_file: XSD to validate against.
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
    parent: etree.ElementBase, element: str, value: object, schema_file: str
) -> None:
    """Set a child element's text, then validate the whole tree.

    Raises lxml's ``DocumentInvalid`` if the schema rejects the new value.

    Args:
        parent: element whose child changes.
        element: child element name.
        value: new value, written as text.
        schema_file: XSD to validate against.
    """
    get_element(parent, element).text = str(value)
    schema = etree.XMLSchema(file=schema_file)
    schema.assertValid(parent.getroottree())


def get_element(parent: etree.ElementBase, element: str) -> Any:  # noqa: ANN401 (class set by lookup)
    """Return the first child element with the given name.

    Args:
        parent: element to search in.
        element: child element name.

    Returns:
        The child, as the class the lookup chose, or None if there is none.
    """
    return parent.find(element, namespaces=parent.nsmap)


def get_element_list(parent: etree.ElementBase, element: str) -> list[Any]:
    """Return all child elements with the given name.

    Args:
        parent: element to search in.
        element: child element name.

    Returns:
        The children, as the classes the lookup chose.
    """
    return parent.findall(element, namespaces=parent.nsmap)


def get_element_text(
    parent: etree.ElementBase, element: str, element_type: type = str
) -> str:
    """Return a child element's text, converted to ``element_type``.

    Args:
        parent: element to search in.
        element: child element name.
        element_type: Python type the text is converted to.

    Returns:
        The converted text; an empty string is converted if the child is missing.
    """
    return TYPE_FUNC_MAP.get(element_type, element_type)(
        getattr(
            get_element(parent, element),
            "text",
            str(TYPE_DEFAULTS[str]),
        )
    )


def get_inner_text_list(parent: etree.ElementBase, element: str) -> list[str]:
    """Return the texts of all child elements with the given name.

    Args:
        parent: element to search in.
        element: child element name.

    Returns:
        The texts, with runs of spaces removed and newlines turned into spaces.
    """
    inner_elements = get_element_list(parent, element)
    return [
        re.sub("[ ]{2,}", "", str(inner_element.text)).replace("\n", " ")
        for inner_element in inner_elements
    ]


def get_attribute(
    parent: etree.ElementBase, attribute: str, attr_type: type[T] = str
) -> T:
    """Return an XML attribute, converted to ``attr_type``.

    Args:
        parent: element to read from.
        attribute: attribute name.
        attr_type: Python type the value is converted to.

    Returns:
        The converted value, or the type's default from ``TYPE_DEFAULTS`` if the
        attribute is missing.
    """
    return TYPE_FUNC_MAP.get(attr_type, attr_type)(
        parent.get(attribute, TYPE_DEFAULTS.get(attr_type, None))
    )


def get_attribute_list(
    parent: etree.ElementBase, attribute: str, attr_type: type = str
) -> list[Any]:
    """Return the texts of all child elements with the given name, converted.

    Args:
        parent: element to read from.
        attribute: child element name.
        attr_type: Python type each text is converted to.

    Returns:
        The converted values; empty if there are none.
    """
    return [
        TYPE_FUNC_MAP.get(attr_type, attr_type)(
            re.sub("[\n]{1,}", " ", re.sub("[ ]{2,}", "", x.text))
        )
        for x in get_element_list(parent, attribute)
    ]


def create_attribute(
    name: str,
    attr_type: type[T],
    schema_file: str,
    validator: Optional[Callable[[Any], str]] = None,
) -> XmlProperty[T]:
    """Create a property that reads and writes an XML attribute.

    Args:
        name: attribute name.
        attr_type: Python type the value is read as.
        schema_file: XSD that validates writes.
        validator: normalises a value before it is written.

    Returns:
        The property.
    """
    return cast(  # property satisfies XmlProperty; see the protocol
        "XmlProperty[T]",
        property(
            fget=lambda self: get_attribute(self, name, attr_type),
            fset=lambda self, value: set_attribute(
                self, name, value, schema_file, validator
            ),
        ),
    )


def create_element_text(
    name: str, element_type: type[T], schema_file: str
) -> XmlProperty[T]:
    """Create a property that reads and writes a child element's text.

    Args:
        name: child element name.
        element_type: Python type the text is read as.
        schema_file: XSD that validates writes.

    Returns:
        The property.
    """
    return cast(  # property satisfies XmlProperty; see the protocol
        "XmlProperty[T]",
        property(
            fget=lambda self: get_element_text(self, name, element_type),
            fset=lambda self, value: set_element_text(self, name, value, schema_file),
        ),
    )


def create_attribute_list(
    name: str, attr_type: type[T], schema_file: str
) -> XmlProperty[list[T]]:
    """Create a property that reads and writes a list of child texts.

    Args:
        name: child element name.
        attr_type: Python type each text is read as.
        schema_file: XSD that validates writes.

    Returns:
        The property.
    """
    return cast(
        "XmlProperty[list[T]]",
        property(
            fget=lambda self: get_attribute_list(self, name, attr_type),
            fset=lambda self, values: set_attribute_list(
                self, name, values, schema_file
            ),
        ),
    )


def fill_in_defaults(
    node: etree.ElementBase,
    static_defaults: dict[str, dict[str, str]],
    dynamic_defaults: dict[str, dict[str, Callable[[Any], str]]],
) -> None:
    """Fill empty attributes in the whole tree of ``node`` with defaults.

    Args:
        node: any element of the tree.
        static_defaults: fixed values, per class name and attribute.
        dynamic_defaults: functions computing a value from the element, per class
            name and attribute.
    """
    root = node.getroottree()
    for child in root.iter():
        for defaults in [static_defaults, dynamic_defaults]:
            for key, value in defaults.get(child.__class__.__name__, {}).items():
                if getattr(child, key, TYPE_DEFAULTS[str]) in TYPE_DEFAULTS.values():
                    if isinstance(value, str):
                        setattr(child, key, value)
                    else:
                        setattr(child, key, value(child))
