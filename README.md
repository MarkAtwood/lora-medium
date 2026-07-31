# lora-medium

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python library that simulates LoRa radio propagation medium for protocol analysis and testing. It models the physical layer behavior of LoRa networks, enabling developers to test mesh protocols, evaluate network topologies, and stress-test implementations without physical hardware.

## Features

- **Propagation Models**: Free-space path loss (FSPL), log-distance path loss, two-ray ground reflection
- **Collision Detection**: Accurate modeling of packet collisions in shared spectrum
- **Capture Effect**: Realistic handling of stronger signals suppressing weaker concurrent transmissions
- **Chaos Engineering**: Configurable packet loss, latency injection, Gilbert-Elliott burst error model
- **Duty Cycle Tracking**: Per-node airtime accounting for regulatory compliance testing
- **Hardware Quirks**: Model real-world radio behavior (SX1276/SX1262 timing, CAD latency)

## Installation

```bash
pip install lora-medium
```

## Quick Example

```python
from lora_medium import Medium, LogDistancePropagation

# Create a medium with log-distance propagation model
medium = Medium(propagation=LogDistancePropagation(
    pl0=127.41,      # Path loss at reference distance (dB)
    n=2.8,           # Path loss exponent
    d0=1.0,          # Reference distance (m)
    sigma=4.0,       # Shadow fading std dev (dB)
))

# Register nodes with their positions and radio parameters
medium.add_node("node_a", position=(0, 0, 0), tx_power=14)
medium.add_node("node_b", position=(100, 0, 0), tx_power=14)
medium.add_node("node_c", position=(50, 50, 0), tx_power=14)

# Transmit a packet and see who receives it
results = medium.transmit("node_a", payload=b"hello", sf=10, bw=125000)
for rx in results.receivers:
    print(f"{rx.node_id}: rssi={rx.rssi:.1f} dBm, snr={rx.snr:.1f} dB")
```

## License

Apache-2.0
