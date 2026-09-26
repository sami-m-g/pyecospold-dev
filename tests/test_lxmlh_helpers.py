"""Test cases for the __helpers__ module."""

from lxml import etree

from pyecospold.lxmlh import fill_in_defaults


def test_create_attribute(ship_order: etree.ElementTree) -> None:
    """It creates an attribute that user can get and set properly."""
    assert ship_order.order_id == "889923"

    new_order_id = "1234"
    ship_order.order_id = new_order_id
    assert ship_order.order_id == new_order_id


def test_create_element_text(ship_order: etree.ElementTree) -> None:
    """It creates an element text that user can get and set properly."""
    assert ship_order.order_person == "John Smith"

    new_order_person = "John Doe"
    ship_order.order_person = new_order_person
    assert ship_order.order_person == new_order_person


def test_create_attribute_list(ship_order: etree.ElementTree) -> None:
    """It creates an attribute list that user can get and set properly."""
    assert ship_order.discounts == [1, 2]

    new_discounts = [3]
    ship_order.discounts = new_discounts
    assert ship_order.discounts == new_discounts


def test_fill_in_defaults(ship_order: etree.ElementTree) -> None:
    "It fills defaults properly."
    static_defaults = {"ShipOrder": {"order_status": "wip"}}

    def _get_order_time(element: etree.ElementBase) -> str:
        return element.order_id

    dynamic_defaults = {"ShipOrder": {"order_time": _get_order_time}}

    fill_in_defaults(ship_order, static_defaults, dynamic_defaults)
    assert ship_order.order_status == static_defaults["ShipOrder"]["order_status"]
    assert ship_order.order_time == ship_order.order_id


def test_get_element(ship_order: etree.ElementTree) -> None:
    """It gets an element properly."""
    ship_to = ship_order.ship_to
    assert ship_to.name == "Ola Nordmann"


def test_get_element_list(ship_order: etree.ElementTree) -> None:
    """It gets an element list properly."""
    items = ship_order.items_list
    assert len(items) == 2


def test_get_inner_text_list(ship_order: etree.ElementTree) -> None:
    """It gets an inner text list properly."""
    items = ship_order.items_list
    assert items[0].notes == ["Item1", "Item1.1"]
