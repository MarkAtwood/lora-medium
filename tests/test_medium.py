# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: The contributors to the LICHEN project
"""Basic tests for lora_medium.Medium."""

from lora_medium import Medium, FSPL


def test_medium_transmission_received():
    """Test that a transmission from one node is received by another."""
    # Create medium with free-space path loss (deterministic, no fading)
    medium = Medium(propagation=FSPL())

    # Define node positions: node1 at origin, node2 at 100m away
    pos1 = (0.0, 0.0, 0.0)
    pos2 = (100.0, 0.0, 0.0)

    # Node1 transmits
    payload = b"hello"
    tx_power_dbm = 14
    start_time_us = 0

    tx = medium.start_tx(
        node_id="node1",
        payload=payload,
        tx_power_dbm=tx_power_dbm,
        position=pos1,
        time_us=start_time_us,
    )
    assert tx is not None, "Transmission should succeed"

    # Node2 receives during transmission
    mid_time_us = (tx.start_time_us + tx.end_time_us) // 2
    candidates = medium.get_rx_candidates(
        rx_node_id="node2",
        rx_position=pos2,
        time_us=mid_time_us,
    )

    assert len(candidates) == 1, f"Expected 1 candidate, got {len(candidates)}"
    assert candidates[0].transmission.payload == payload

    # Resolve reception (single candidate = success)
    result = medium.resolve_reception(candidates)
    assert result is not None, "Reception should succeed"
    assert result.payload == payload


def test_medium_no_self_reception():
    """Test that a node does not receive its own transmission."""
    medium = Medium(propagation=FSPL())
    pos = (0.0, 0.0, 0.0)

    tx = medium.start_tx(
        node_id="node1",
        payload=b"test",
        tx_power_dbm=14,
        position=pos,
        time_us=0,
    )
    assert tx is not None

    # Node1 should not receive its own transmission
    mid_time_us = (tx.start_time_us + tx.end_time_us) // 2
    candidates = medium.get_rx_candidates(
        rx_node_id="node1",
        rx_position=pos,
        time_us=mid_time_us,
    )

    assert len(candidates) == 0, "Node should not receive its own transmission"
