"""Test cases for the __model_v2__ module."""

from collections.abc import Callable
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from pyecospold.core import parse_file_v2


@pytest.mark.parametrize("name", ["v2_1.xml", "v2_2.spold"])
def test_parse_file_v2(
    fixtures_dir: Path,
    name: str,
    as_data: Callable[[object], object],
    snapshot: SnapshotAssertion,
) -> None:
    """It exposes every value of the sample file through the model."""
    assert as_data(parse_file_v2(fixtures_dir / "v2" / name)) == snapshot


def test_eco_spold_shortcuts(fixtures_dir: Path) -> None:
    """Shortcut methods return the values of the paths they abbreviate."""
    eco_spold = parse_file_v2(fixtures_dir / "v2" / "v2_2.spold")
    flow_data = eco_spold.activityDataset.flowData
    elementary = flow_data.elementaryExchanges[0]
    intermediate = flow_data.intermediateExchanges[0]

    assert eco_spold.elementary_exchange(0) is not None
    assert eco_spold.elementary_exchange_name(0, 0) == elementary.names[0]
    assert eco_spold.elementary_exchange_unit_name(0, 0) == elementary.unitNames[0]
    assert (
        eco_spold.elementary_exchange_compartment(0, 0)
        == elementary.compartment.compartments[0]
    )
    assert (
        eco_spold.elementary_exchange_sub_compartment(0, 0)
        == elementary.compartment.subCompartments[0]
    )
    assert eco_spold.intermediate_exchange(0) is not None
    assert eco_spold.intermediate_exchange_name(0, 0) == intermediate.names[0]
    assert eco_spold.intermediate_exchange_unit_name(0, 0) == intermediate.unitNames[0]
