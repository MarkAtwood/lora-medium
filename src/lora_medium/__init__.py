"""LoRa radio medium simulator.

Simulates RF propagation, collisions, capture effect, and chaos conditions
for LoRa protocol testing and analysis.
"""

__version__ = "0.1.0"

from .chaos import (
    ChaosEngine,
    ChaosRule,
    DegradeRule,
    DropRule,
    GilbertElliottRule,
    JammerRule,
    LatencyRule,
    LossRule,
    PartitionRule,
    TxJitterRule,
)
from .duty_cycle import DutyCycleTracker
from .medium import Medium, RxCandidate
from .propagation import FSPL, LogDistancePL, PropagationModel, TwoRayGround
from .quirks import PRESETS as QUIRK_PRESETS
from .quirks import QuirkProfile
from .transmission import Transmission, airtime_us

__all__ = [
    # Core
    "Medium",
    "RxCandidate",
    "Transmission",
    "airtime_us",
    # Propagation models
    "PropagationModel",
    "FSPL",
    "LogDistancePL",
    "TwoRayGround",
    # Chaos injection
    "ChaosEngine",
    "ChaosRule",
    "DropRule",
    "LatencyRule",
    "LossRule",
    "JammerRule",
    "DegradeRule",
    "PartitionRule",
    "GilbertElliottRule",
    "TxJitterRule",
    # Duty cycle
    "DutyCycleTracker",
    # Hardware quirks
    "QuirkProfile",
    "QUIRK_PRESETS",
]
