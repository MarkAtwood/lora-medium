# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: The contributors to the LICHEN project
"""Hardware quirks model for realistic radio imperfections.

Models real radio hardware imperfections for simulation fidelity:
- TX/RX mode switching delay (warm-up time)
- PLL lock failures requiring retry
- Crystal drift affecting frequency accuracy
- RSSI measurement noise
- CAD (Channel Activity Detection) error rates
- RX deaf time after TX (turnaround)

Quirks are optional and disabled by default for deterministic tests.
The Medium assigns quirks per node (option B from design notes).
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class QuirkProfile:
    """Hardware quirk parameters for a simulated radio.

    All quirk effects are optional. A profile with all zeros is "ideal"
    (no hardware imperfections). Profiles are immutable to prevent
    accidental mid-simulation changes.

    Attributes:
        warmup_ms: TX/RX mode switch delay in milliseconds (1-5 typical).
            Packets during transition are lost.
        pll_fail_rate: Probability of PLL lock failure per TX attempt (0.0-1.0).
            Typical: 0.001-0.01 (0.1%-1%).
        crystal_ppm: Frequency offset in parts per million (±10-30 typical).
            Affects capture effect and collision detection.
        rssi_noise_db: RSSI measurement noise standard deviation in dB.
            Real hardware has ±3 dB typical.
        cad_false_positive_rate: CAD reports activity when none present (0.0-1.0).
            Typical: 0.01-0.05 (1%-5%).
        cad_false_negative_rate: CAD misses real activity (0.0-1.0).
            Typical: 0.01-0.05 (1%-5%).
        rx_deaf_us: RX deaf time after TX in microseconds.
            TX/RX turnaround time, typically ~100 us.
    """

    warmup_ms: float = 0.0
    pll_fail_rate: float = 0.0
    crystal_ppm: float = 0.0
    rssi_noise_db: float = 0.0
    cad_false_positive_rate: float = 0.0
    cad_false_negative_rate: float = 0.0
    rx_deaf_us: int = 0

    def __post_init__(self) -> None:
        """Validate quirk parameters are in valid ranges."""
        if self.warmup_ms < 0:
            raise ValueError(f"warmup_ms must be >= 0, got {self.warmup_ms}")
        if not 0.0 <= self.pll_fail_rate <= 1.0:
            raise ValueError(f"pll_fail_rate must be 0.0-1.0, got {self.pll_fail_rate}")
        if self.rssi_noise_db < 0:
            raise ValueError(f"rssi_noise_db must be >= 0, got {self.rssi_noise_db}")
        if not 0.0 <= self.cad_false_positive_rate <= 1.0:
            raise ValueError(
                f"cad_false_positive_rate must be 0.0-1.0, got {self.cad_false_positive_rate}"
            )
        if not 0.0 <= self.cad_false_negative_rate <= 1.0:
            raise ValueError(
                f"cad_false_negative_rate must be 0.0-1.0, got {self.cad_false_negative_rate}"
            )
        if self.rx_deaf_us < 0:
            raise ValueError(f"rx_deaf_us must be >= 0, got {self.rx_deaf_us}")

    def with_overrides(self, **kwargs: float | int) -> QuirkProfile:
        """Return a new profile with specified fields overridden."""
        return replace(self, **kwargs)


# Named presets for common hardware configurations
PRESETS: dict[str, QuirkProfile] = {
    # Ideal: no quirks (deterministic tests)
    "ideal": QuirkProfile(),
    # Moderate: typical real-world conditions
    "moderate": QuirkProfile(
        warmup_ms=2.0,
        pll_fail_rate=0.005,
        crystal_ppm=15.0,
        rssi_noise_db=2.0,
        cad_false_positive_rate=0.02,
        cad_false_negative_rate=0.02,
        rx_deaf_us=100,
    ),
    # SX1276: Semtech SX1276 chip characteristics
    "sx1276": QuirkProfile(
        warmup_ms=1.5,
        pll_fail_rate=0.001,
        crystal_ppm=10.0,
        rssi_noise_db=1.5,
        cad_false_positive_rate=0.01,
        cad_false_negative_rate=0.03,
        rx_deaf_us=80,
    ),
    # SX1262: Semtech SX1262 chip (improved over SX1276)
    "sx1262": QuirkProfile(
        warmup_ms=1.0,
        pll_fail_rate=0.0005,
        crystal_ppm=8.0,
        rssi_noise_db=1.0,
        cad_false_positive_rate=0.005,
        cad_false_negative_rate=0.015,
        rx_deaf_us=50,
    ),
    # Garbage: stress testing / worst-case hardware
    "garbage": QuirkProfile(
        warmup_ms=5.0,
        pll_fail_rate=0.05,
        crystal_ppm=30.0,
        rssi_noise_db=5.0,
        cad_false_positive_rate=0.10,
        cad_false_negative_rate=0.10,
        rx_deaf_us=200,
    ),
}


def pll_lock_fails(profile: QuirkProfile) -> bool:
    """Roll for PLL lock failure based on profile's fail rate.

    Args:
        profile: QuirkProfile with pll_fail_rate.

    Returns:
        True if PLL lock failed this attempt, False if successful.
    """
    if profile.pll_fail_rate <= 0:
        return False
    if profile.pll_fail_rate >= 1.0:
        return True
    # Use secrets for cryptographic randomness
    return secrets.randbelow(1_000_000) < int(profile.pll_fail_rate * 1_000_000)


def apply_rssi_noise(rssi_dbm: float, profile: QuirkProfile) -> float:
    """Apply RSSI measurement noise based on profile.

    Uses triangular approximation to Gaussian for simplicity.

    Args:
        rssi_dbm: True RSSI value in dBm.
        profile: QuirkProfile with rssi_noise_db.

    Returns:
        Noisy RSSI value.
    """
    if profile.rssi_noise_db <= 0:
        return rssi_dbm
    # Triangular approximation: sum of two uniform [-1,1] gives [-2,2] with peak at 0
    u1 = (secrets.randbelow(2_000_000) - 1_000_000) / 1_000_000
    u2 = (secrets.randbelow(2_000_000) - 1_000_000) / 1_000_000
    noise = (u1 + u2) / 2.0 * profile.rssi_noise_db
    return rssi_dbm + noise


def cad_with_quirks(
    actual_activity: bool,
    profile: QuirkProfile,
) -> bool:
    """Apply CAD false positive/negative rates to actual channel state.

    Args:
        actual_activity: True if channel actually has activity.
        profile: QuirkProfile with CAD error rates.

    Returns:
        What CAD reports (may differ from actual_activity).
    """
    if actual_activity:
        # Chance of false negative (missing real activity)
        threshold = int(profile.cad_false_negative_rate * 1_000_000)
        # Return False if under threshold (false negative), else True
        return not (threshold > 0 and secrets.randbelow(1_000_000) < threshold)
    # Chance of false positive (seeing phantom activity)
    threshold = int(profile.cad_false_positive_rate * 1_000_000)
    # Return True if under threshold (false positive), else False
    return threshold > 0 and secrets.randbelow(1_000_000) < threshold


def frequency_offset_hz(profile: QuirkProfile, nominal_hz: int) -> int:
    """Calculate frequency offset due to crystal drift.

    Args:
        profile: QuirkProfile with crystal_ppm.
        nominal_hz: Nominal frequency in Hz.

    Returns:
        Actual frequency with drift applied (Hz).
    """
    if profile.crystal_ppm <= 0:
        return nominal_hz
    # Random offset within ±crystal_ppm
    ppm_offset = (secrets.randbelow(2_000_000) - 1_000_000) / 1_000_000 * profile.crystal_ppm
    offset_hz = int(nominal_hz * ppm_offset / 1_000_000)
    return nominal_hz + offset_hz
