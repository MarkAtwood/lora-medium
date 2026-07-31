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
from .medium import (
    ChannelLoad,
    Medium,
    RendezvousInfo,
    RendezvousMechanism,
    RxCandidate,
    TDMASlot,
    TDMAVector,
)
from .propagation import (
    CAPTURE_THRESHOLD_DB,
    FSPL,
    PATH_LOSS_FREE_SPACE,
    PATH_LOSS_INDOOR,
    PATH_LOSS_URBAN,
    SENSITIVITY_DEFAULT,
    SENSITIVITY_LR_FHSS,
    SENSITIVITY_SF7,
    SENSITIVITY_SF8,
    SENSITIVITY_SF9,
    SENSITIVITY_SF10,
    SENSITIVITY_SF11,
    SENSITIVITY_SF12,
    LogDistancePL,
    PropagationModel,
    TwoRayGround,
    link_budget,
)
from .quirks import PRESETS
from .quirks import PRESETS as QUIRK_PRESETS
from .quirks import (
    QuirkProfile,
    apply_rssi_noise,
    cad_with_quirks,
    frequency_offset_hz,
    pll_lock_fails,
)
from .transmission import Transmission, airtime_us, lr_fhss_airtime_us

__all__ = [
    # Core
    "Medium",
    "RxCandidate",
    "ChannelLoad",
    "RendezvousInfo",
    "RendezvousMechanism",
    "TDMASlot",
    "TDMAVector",
    "Transmission",
    "airtime_us",
    "lr_fhss_airtime_us",
    # Propagation models
    "PropagationModel",
    "FSPL",
    "LogDistancePL",
    "TwoRayGround",
    "link_budget",
    # Propagation constants
    "CAPTURE_THRESHOLD_DB",
    "PATH_LOSS_FREE_SPACE",
    "PATH_LOSS_INDOOR",
    "PATH_LOSS_URBAN",
    "SENSITIVITY_DEFAULT",
    "SENSITIVITY_LR_FHSS",
    "SENSITIVITY_SF7",
    "SENSITIVITY_SF8",
    "SENSITIVITY_SF9",
    "SENSITIVITY_SF10",
    "SENSITIVITY_SF11",
    "SENSITIVITY_SF12",
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
    "PRESETS",
    "apply_rssi_noise",
    "cad_with_quirks",
    "frequency_offset_hz",
    "pll_lock_fails",
]
