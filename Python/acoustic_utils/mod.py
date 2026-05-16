#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Acoustic Utilities Module

Comprehensive acoustic and sound calculation utilities with zero external dependencies.
Provides decibel calculations, sound pressure levels, room acoustics, and more.

Features:
- Decibel calculations (power, intensity, pressure)
- Sound level conversions
- Frequency-weighted filters (A, B, C, D weighting)
- Room acoustics (RT60, room modes)
- Sound propagation (distance attenuation)
- Doppler effect calculations
- Wavelength and frequency conversions
- Loudness conversions (phon, sone)
- Noise criteria calculations

Author: AllToolkit
License: MIT
Date: 2026-05-16
"""

import math
from typing import Tuple, List, Optional, Dict, Union
from enum import Enum
from dataclasses import dataclass


# =============================================================================
# Constants
# =============================================================================

# Speed of sound in air at 20°C (m/s)
SPEED_OF_SOUND_20C = 343.0

# Reference sound pressure (Pa) - threshold of human hearing
REFERENCE_SOUND_PRESSURE = 20e-6  # 20 micropascals

# Reference sound intensity (W/m²)
REFERENCE_SOUND_INTENSITY = 1e-12

# Reference sound power (W)
REFERENCE_SOUND_POWER = 1e-12

# Reference distance for sound measurements (meters)
REFERENCE_DISTANCE = 1.0

# A-weighting frequency coefficients
A_WEIGHTING_COEFFICIENTS = [
    (12200.0, 20.6),  # f1, f2 for low-frequency cut
    (12200.0, 107.7),  # f1, f2 for mid-frequency correction
    (737.9, 158.5),  # f1, f2 for high-frequency emphasis
]


# =============================================================================
# Enums
# =============================================================================

class FrequencyWeighting(Enum):
    """Frequency weighting types for sound level measurements."""
    A = 'A'  # A-weighting (most common, approximates human hearing)
    B = 'B'  # B-weighting (obsolete)
    C = 'C'  # C-weighting (flat response)
    D = 'D'  # D-weighting (aircraft noise)
    Z = 'Z'  # Z-weighting (zero/flat, no weighting)
    LIN = 'LIN'  # Linear (same as Z)


class RoomType(Enum):
    """Room types for RT60 estimation."""
    LIVING_ROOM = 'living_room'
    BEDROOM = 'bedroom'
    OFFICE = 'office'
    CLASSROOM = 'classroom'
    LECTURE_HALL = 'lecture_hall'
    CHURCH = 'church'
    CONCERT_HALL = 'concert_hall'
    RECORDING_STUDIO = 'recording_studio'
    GYMNASIUM = 'gymnasium'


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class SoundLevel:
    """Represents a sound level measurement."""
    decibels: float
    weighting: FrequencyWeighting = FrequencyWeighting.A
    
    def __repr__(self):
        return f"{self.decibels:.1f} dB({self.weighting.value})"


@dataclass
class RoomAcoustics:
    """Room acoustic properties."""
    length: float  # meters
    width: float  # meters
    height: float  # meters
    
    @property
    def volume(self) -> float:
        """Calculate room volume in cubic meters."""
        return self.length * self.width * self.height
    
    @property
    def surface_area(self) -> float:
        """Calculate total surface area in square meters."""
        return 2 * (
            self.length * self.width +
            self.width * self.height +
            self.length * self.height
        )
    
    def floor_area(self) -> float:
        """Calculate floor area in square meters."""
        return self.length * self.width


# =============================================================================
# Core Decibel Functions
# =============================================================================

def db_from_power(power: float, reference: float = REFERENCE_SOUND_POWER) -> float:
    """
    Calculate decibels from power ratio.
    
    dB = 10 * log10(P / P_ref)
    
    Args:
        power: Power in watts
        reference: Reference power in watts (default: 10^-12 W)
    
    Returns:
        Decibel value
    
    Examples:
        >>> db_from_power(0.001)
        90.0
        >>> db_from_power(1e-12)
        0.0
    """
    if power <= 0:
        return float('-inf')
    return 10 * math.log10(power / reference)


def db_from_intensity(intensity: float, reference: float = REFERENCE_SOUND_INTENSITY) -> float:
    """
    Calculate decibels from sound intensity.
    
    dB = 10 * log10(I / I_ref)
    
    Args:
        intensity: Sound intensity in W/m²
        reference: Reference intensity in W/m² (default: 10^-12 W/m²)
    
    Returns:
        Decibel value
    
    Examples:
        >>> db_from_intensity(1e-6)
        60.0
    """
    if intensity <= 0:
        return float('-inf')
    return 10 * math.log10(intensity / reference)


def db_from_pressure(pressure: float, reference: float = REFERENCE_SOUND_PRESSURE) -> float:
    """
    Calculate sound pressure level (SPL) in decibels.
    
    dB = 20 * log10(P / P_ref)
    
    Args:
        pressure: Sound pressure in pascals
        reference: Reference pressure in pascals (default: 20 µPa)
    
    Returns:
        Sound pressure level in decibels
    
    Examples:
        >>> db_from_pressure(20e-6)
        0.0
        >>> db_from_pressure(0.02)  # 20 Pa = 60 dB
        60.0
    """
    if pressure <= 0:
        return float('-inf')
    return 20 * math.log10(pressure / reference)


def power_from_db(decibels: float, reference: float = REFERENCE_SOUND_POWER) -> float:
    """
    Convert decibels to power.
    
    P = P_ref * 10^(dB/10)
    
    Args:
        decibels: Decibel value
        reference: Reference power in watts
    
    Returns:
        Power in watts
    
    Examples:
        >>> power_from_db(90)
        0.001
    """
    return reference * (10 ** (decibels / 10))


def intensity_from_db(decibels: float, reference: float = REFERENCE_SOUND_INTENSITY) -> float:
    """
    Convert decibels to sound intensity.
    
    Args:
        decibels: Decibel value
        reference: Reference intensity in W/m²
    
    Returns:
        Sound intensity in W/m²
    
    Examples:
        >>> intensity_from_db(60)
        1e-06
    """
    return reference * (10 ** (decibels / 10))


def pressure_from_db(decibels: float, reference: float = REFERENCE_SOUND_PRESSURE) -> float:
    """
    Convert sound pressure level to pressure in pascals.
    
    P = P_ref * 10^(dB/20)
    
    Args:
        decibels: Sound pressure level in decibels
        reference: Reference pressure in pascals
    
    Returns:
        Sound pressure in pascals
    
    Examples:
        >>> pressure_from_db(60)
        0.02
    """
    return reference * (10 ** (decibels / 20))


# =============================================================================
# Sound Level Operations
# =============================================================================

def add_decibels(*levels: float) -> float:
    """
    Add multiple sound levels in decibels (incoherent addition).
    
    Uses the formula: dB_total = 10 * log10(sum(10^(dB_i/10)))
    
    Args:
        *levels: Sound levels in decibels
    
    Returns:
        Combined sound level in decibels
    
    Examples:
        >>> round(add_decibels(60, 60), 1)
        63.0
        >>> add_decibels(80, 70)
        80.4
    """
    if not levels:
        return float('-inf')
    
    # Sum the intensities
    total_intensity = sum(10 ** (db / 10) for db in levels if db > float('-inf'))
    
    if total_intensity <= 0:
        return float('-inf')
    
    return 10 * math.log10(total_intensity)


def subtract_decibels(total: float, background: float) -> float:
    """
    Subtract background noise from total sound level.
    
    Uses the formula: dB_signal = 10 * log10(10^(dB_total/10) - 10^(dB_background/10))
    
    Args:
        total: Total measured sound level (dB)
        background: Background noise level (dB)
    
    Returns:
        Source sound level in decibels
    
    Examples:
        >>> round(subtract_decibels(60, 50), 1)
        59.5
    """
    total_intensity = 10 ** (total / 10)
    bg_intensity = 10 ** (background / 10)
    
    if total_intensity <= bg_intensity:
        return float('-inf')
    
    return 10 * math.log10(total_intensity - bg_intensity)


def average_decibels(*levels: float) -> float:
    """
    Calculate the energy average of multiple sound levels.
    
    Args:
        *levels: Sound levels in decibels
    
    Returns:
        Average sound level in decibels
    
    Examples:
        >>> round(average_decibels(60, 70, 80), 1)
        72.3
    """
    if not levels:
        return float('-inf')
    
    avg_intensity = sum(10 ** (db / 10) for db in levels if db > float('-inf')) / len(levels)
    
    if avg_intensity <= 0:
        return float('-inf')
    
    return 10 * math.log10(avg_intensity)


def decibel_difference(db1: float, db2: float) -> float:
    """
    Calculate the difference between two sound levels.
    
    Args:
        db1: First sound level (dB)
        db2: Second sound level (dB)
    
    Returns:
        Absolute difference in decibels
    
    Examples:
        >>> decibel_difference(80, 70)
        10.0
    """
    return abs(db1 - db2)


# =============================================================================
# Distance Attenuation
# =============================================================================

def distance_attenuation(distance: float, reference_distance: float = REFERENCE_DISTANCE) -> float:
    """
    Calculate sound level attenuation due to distance (spherical spreading).
    
    Uses inverse square law: attenuation = 20 * log10(d / d_ref)
    
    Args:
        distance: Distance from source in meters
        reference_distance: Reference distance in meters
    
    Returns:
        Attenuation in decibels (negative values indicate reduction)
    
    Examples:
        >>> round(distance_attenuation(2, 1), 1)
        6.0
        >>> round(distance_attenuation(10, 1), 1)
        20.0
    """
    if distance <= 0 or reference_distance <= 0:
        raise ValueError("Distance must be positive")
    
    return 20 * math.log10(distance / reference_distance)


def sound_level_at_distance(
    source_level: float,
    distance: float,
    reference_distance: float = REFERENCE_DISTANCE
) -> float:
    """
    Calculate sound level at a given distance from a point source.
    
    Args:
        source_level: Sound level at reference distance (dB)
        distance: Target distance in meters
        reference_distance: Reference distance in meters
    
    Returns:
        Sound level at the specified distance (dB)
    
    Examples:
        >>> round(sound_level_at_distance(100, 10, 1), 1)
        80.0
    """
    return source_level - distance_attenuation(distance, reference_distance)


def distance_from_sound_level(
    source_level: float,
    measured_level: float,
    reference_distance: float = REFERENCE_DISTANCE
) -> float:
    """
    Calculate distance from source given source level and measured level.
    
    Args:
        source_level: Sound level at reference distance (dB)
        measured_level: Measured sound level (dB)
        reference_distance: Reference distance in meters
    
    Returns:
        Distance from source in meters
    
    Examples:
        >>> round(distance_from_sound_level(100, 80, 1), 1)
        10.0
    """
    attenuation = source_level - measured_level
    
    if attenuation < 0:
        raise ValueError("Measured level cannot be higher than source level")
    
    return reference_distance * (10 ** (attenuation / 20))


# =============================================================================
# Wavelength and Frequency
# =============================================================================

def wavelength(frequency: float, speed_of_sound: float = SPEED_OF_SOUND_20C) -> float:
    """
    Calculate wavelength from frequency.
    
    λ = c / f
    
    Args:
        frequency: Frequency in Hz
        speed_of_sound: Speed of sound in m/s (default: 343 m/s at 20°C)
    
    Returns:
        Wavelength in meters
    
    Examples:
        >>> round(wavelength(440), 3)  # A4 note
        0.78
        >>> round(wavelength(1000), 3)
        0.343
    """
    if frequency <= 0:
        raise ValueError("Frequency must be positive")
    
    return speed_of_sound / frequency


def frequency_from_wavelength(wavelength_m: float, speed_of_sound: float = SPEED_OF_SOUND_20C) -> float:
    """
    Calculate frequency from wavelength.
    
    f = c / λ
    
    Args:
        wavelength_m: Wavelength in meters
        speed_of_sound: Speed of sound in m/s
    
    Returns:
        Frequency in Hz
    
    Examples:
        >>> round(frequency_from_wavelength(0.343), 0)
        1000.0
    """
    if wavelength_m <= 0:
        raise ValueError("Wavelength must be positive")
    
    return speed_of_sound / wavelength_m


def speed_of_sound(temperature: float = 20.0) -> float:
    """
    Calculate speed of sound in air at a given temperature.
    
    c ≈ 331.3 * sqrt(1 + T/273.15) m/s
    
    Args:
        temperature: Temperature in Celsius (default: 20°C)
    
    Returns:
        Speed of sound in m/s
    
    Examples:
        >>> round(speed_of_sound(20), 1)
        343.2
        >>> round(speed_of_sound(0), 1)
        331.3
    """
    return 331.3 * math.sqrt(1 + temperature / 273.15)


# =============================================================================
# Doppler Effect
# =============================================================================

def doppler_frequency(
    source_frequency: float,
    source_velocity: float = 0,
    observer_velocity: float = 0,
    speed_of_sound: float = SPEED_OF_SOUND_20C,
    approaching: bool = True
) -> float:
    """
    Calculate observed frequency due to Doppler effect.
    
    f' = f * (c + v_observer) / (c + v_source)
    
    Args:
        source_frequency: Original frequency in Hz
        source_velocity: Source velocity in m/s (positive if moving)
        observer_velocity: Observer velocity in m/s (positive if moving towards source)
        speed_of_sound: Speed of sound in m/s
        approaching: True if source and observer are approaching
    
    Returns:
        Observed frequency in Hz
    
    Examples:
        >>> doppler_frequency(440, 30, 0)  # Source moving towards observer at 30 m/s
        484.8...
        >>> doppler_frequency(440, 0, 30)  # Observer moving towards source at 30 m/s
        478.8...
    """
    if source_velocity >= speed_of_sound:
        raise ValueError("Source velocity cannot exceed speed of sound")
    
    if approaching:
        # Source moving towards observer or observer moving towards source
        return source_frequency * (speed_of_sound + observer_velocity) / (speed_of_sound - source_velocity)
    else:
        # Moving apart
        return source_frequency * (speed_of_sound - observer_velocity) / (speed_of_sound + source_velocity)


def doppler_shift(
    source_frequency: float,
    relative_velocity: float,
    speed_of_sound: float = SPEED_OF_SOUND_20C
) -> float:
    """
    Calculate frequency shift due to relative motion.
    
    Positive velocity = approaching, negative = receding.
    
    Args:
        source_frequency: Original frequency in Hz
        relative_velocity: Relative velocity in m/s (positive = approaching)
        speed_of_sound: Speed of sound in m/s
    
    Returns:
        Frequency shift in Hz (positive = higher pitch)
    
    Examples:
        >>> round(doppler_shift(440, 30), 1)  # Approaching at 30 m/s
        38.5
    """
    observed = doppler_frequency(source_frequency, relative_velocity, 0, speed_of_sound, True)
    return observed - source_frequency


# =============================================================================
# Frequency Weighting
# =============================================================================

def a_weighting(frequency: float) -> float:
    """
    Calculate A-weighting correction for a frequency.
    
    A-weighting approximates the human ear's frequency response at moderate levels.
    
    Args:
        frequency: Frequency in Hz
    
    Returns:
        A-weighting correction in dB
    
    Examples:
        >>> round(a_weighting(1000), 1)
        0.0
        >>> round(a_weighting(100), 1)
        -19.1
        >>> round(a_weighting(10000), 1)
        -2.5
    """
    if frequency <= 0:
        return float('-inf')
    
    f = frequency
    f2 = f ** 2
    
    # A-weighting formula (IEC 61672-1)
    # C-weighting = A-weighting + D-weighting correction
    ra = (12200 ** 2 * f2 ** 2) / (
        (f2 + 20.6 ** 2) *
        (f2 + 12200 ** 2) *
        math.sqrt((f2 + 107.7 ** 2) * (f2 + 737.9 ** 2))
    )
    
    ra1000 = (12200 ** 2 * 1000 ** 4) / (
        (1000 ** 2 + 20.6 ** 2) *
        (1000 ** 2 + 12200 ** 2) *
        math.sqrt((1000 ** 2 + 107.7 ** 2) * (1000 ** 2 + 737.9 ** 2))
    )
    
    return 20 * math.log10(ra / ra1000)


def c_weighting(frequency: float) -> float:
    """
    Calculate C-weighting correction for a frequency.
    
    C-weighting has a flat response except at very low and high frequencies.
    
    Args:
        frequency: Frequency in Hz
    
    Returns:
        C-weighting correction in dB
    
    Examples:
        >>> round(c_weighting(1000), 1)
        0.0
        >>> round(c_weighting(100), 1)
        -0.2
    """
    if frequency <= 0:
        return float('-inf')
    
    f = frequency
    f2 = f ** 2
    
    rc = (12200 ** 2 * f2) / (
        (f2 + 20.6 ** 2) * (f2 + 12200 ** 2)
    )
    
    rc1000 = (12200 ** 2 * 1000 ** 2) / (
        (1000 ** 2 + 20.6 ** 2) * (1000 ** 2 + 12200 ** 2)
    )
    
    return 20 * math.log10(rc / rc1000)


def apply_weighting(
    decibels: float,
    frequency: float,
    weighting: FrequencyWeighting = FrequencyWeighting.A
) -> float:
    """
    Apply frequency weighting to a sound level.
    
    Args:
        decibels: Unweighted sound level in dB
        frequency: Frequency in Hz
        weighting: Weighting type (A, B, C, D, or Z)
    
    Returns:
        Weighted sound level in dB
    
    Examples:
        >>> round(apply_weighting(60, 100, FrequencyWeighting.A), 1)
        40.9
        >>> round(apply_weighting(60, 1000, FrequencyWeighting.A), 1)
        60.0
    """
    if weighting == FrequencyWeighting.A:
        correction = a_weighting(frequency)
    elif weighting == FrequencyWeighting.C:
        correction = c_weighting(frequency)
    else:
        # Z or LIN weighting = no correction
        correction = 0.0
    
    return decibels + correction


# =============================================================================
# Loudness Conversions
# =============================================================================

def phon_to_sone(phon: float) -> float:
    """
    Convert loudness level (phon) to loudness (sone).
    
    1 sone = loudness of 40 phon
    Relationship: sone = 2^((phon - 40) / 10)
    
    Args:
        phon: Loudness level in phon
    
    Returns:
        Loudness in sone
    
    Examples:
        >>> phon_to_sone(40)
        1.0
        >>> phon_to_sone(50)
        2.0
        >>> round(phon_to_sone(60), 1)
        4.0
    """
    return 2 ** ((phon - 40) / 10)


def sone_to_phon(sone: float) -> float:
    """
    Convert loudness (sone) to loudness level (phon).
    
    phon = 40 + 10 * log2(sone)
    
    Args:
        sone: Loudness in sone
    
    Returns:
        Loudness level in phon
    
    Examples:
        >>> sone_to_phon(1)
        40.0
        >>> sone_to_phon(2)
        50.0
    """
    if sone <= 0:
        raise ValueError("Sone must be positive")
    
    return 40 + 10 * math.log2(sone)


def db_to_phon(db: float, frequency: float = 1000.0) -> float:
    """
    Convert dB to phon using equal-loudness contours.
    
    At 1000 Hz, phon = dB. At other frequencies, corrections apply.
    
    Args:
        db: Sound pressure level in dB
        frequency: Frequency in Hz
    
    Returns:
        Loudness level in phon
    
    Examples:
        >>> db_to_phon(60, 1000)
        60.0
    """
    if frequency == 1000:
        return db
    
    # Simplified approximation using Fletcher-Munson curves
    # This is an approximation; real equal-loudness curves are more complex
    weighting_correction = a_weighting(frequency)
    
    # The phon value is approximately the dB level corrected for equal loudness
    return db + weighting_correction


# =============================================================================
# Room Acoustics
# =============================================================================

def sabine_rt60(room: RoomAcoustics, absorption_coefficient: float) -> float:
    """
    Calculate reverberation time (RT60) using Sabine's formula.
    
    RT60 = 0.161 * V / (S * α)
    
    Args:
        room: Room dimensions
        absorption_coefficient: Average absorption coefficient (0-1)
    
    Returns:
        RT60 in seconds
    
    Examples:
        >>> room = RoomAcoustics(5, 4, 3)
        >>> round(sabine_rt60(room, 0.2), 2)
        0.98
    """
    if not 0 <= absorption_coefficient <= 1:
        raise ValueError("Absorption coefficient must be between 0 and 1")
    
    if absorption_coefficient == 0:
        return float('inf')
    
    # Sabine's formula: RT60 = 0.161 * V / (S * α)
    # where V = volume (m³), S = surface area (m²), α = absorption coefficient
    return 0.161 * room.volume / (room.surface_area * absorption_coefficient)


def eyring_rt60(room: RoomAcoustics, absorption_coefficient: float) -> float:
    """
    Calculate reverberation time using Eyring's formula.
    
    More accurate for highly absorptive rooms.
    RT60 = 0.161 * V / (-S * ln(1 - α))
    
    Args:
        room: Room dimensions
        absorption_coefficient: Average absorption coefficient (0-1)
    
    Returns:
        RT60 in seconds
    
    Examples:
        >>> room = RoomAcoustics(5, 4, 3)
        >>> round(eyring_rt60(room, 0.2), 2)
        1.09
    """
    if not 0 <= absorption_coefficient <= 1:
        raise ValueError("Absorption coefficient must be between 0 and 1")
    
    if absorption_coefficient == 0:
        return float('inf')
    
    if absorption_coefficient == 1:
        return 0
    
    # Eyring's formula: RT60 = 0.161 * V / (-S * ln(1 - α))
    return 0.161 * room.volume / (-room.surface_area * math.log(1 - absorption_coefficient))


def room_modes(room: RoomAcoustics, max_mode: int = 5) -> List[Tuple[int, int, int, float]]:
    """
    Calculate room resonance frequencies (room modes).
    
    Uses the formula: f = (c/2) * sqrt((nx/Lx)² + (ny/Ly)² + (nz/Lz)²)
    
    Args:
        room: Room dimensions
        max_mode: Maximum mode number for each dimension
    
    Returns:
        List of tuples (nx, ny, nz, frequency)
    
    Examples:
        >>> room = RoomAcoustics(5, 4, 3)
        >>> modes = room_modes(room, 2)
        >>> len(modes) > 0
        True
    """
    modes = []
    c = SPEED_OF_SOUND_20C
    
    for nx in range(max_mode + 1):
        for ny in range(max_mode + 1):
            for nz in range(max_mode + 1):
                if nx == 0 and ny == 0 and nz == 0:
                    continue
                
                frequency = (c / 2) * math.sqrt(
                    (nx / room.length) ** 2 +
                    (ny / room.width) ** 2 +
                    (nz / room.height) ** 2
                )
                
                modes.append((nx, ny, nz, frequency))
    
    # Sort by frequency
    modes.sort(key=lambda x: x[3])
    return modes


def critical_distance(
    source_directivity: float,
    room: RoomAcoustics,
    absorption_coefficient: float
) -> float:
    """
    Calculate the critical distance in a room.
    
    The critical distance is where direct and reverberant sound levels are equal.
    
    rc = 0.141 * sqrt(Q * S * α)
    
    Args:
        source_directivity: Directivity factor Q (1 = omnidirectional, 2 = floor, 4 = corner)
        room: Room dimensions
        absorption_coefficient: Average absorption coefficient
    
    Returns:
        Critical distance in meters
    
    Examples:
        >>> room = RoomAcoustics(5, 4, 3)
        >>> round(critical_distance(1, room, 0.2), 2)
        0.77
    """
    if absorption_coefficient <= 0:
        raise ValueError("Absorption coefficient must be positive")
    
    return 0.141 * math.sqrt(source_directivity * room.surface_area * absorption_coefficient)


def recommended_rt60(room_type: RoomType) -> Tuple[float, float]:
    """
    Get recommended RT60 range for a room type.
    
    Args:
        room_type: Type of room
    
    Returns:
        Tuple of (minimum RT60, maximum RT60) in seconds
    
    Examples:
        >>> recommended_rt60(RoomType.RECORDING_STUDIO)
        (0.3, 0.5)
    """
    recommendations = {
        RoomType.LIVING_ROOM: (0.4, 0.6),
        RoomType.BEDROOM: (0.3, 0.5),
        RoomType.OFFICE: (0.4, 0.6),
        RoomType.CLASSROOM: (0.4, 0.6),
        RoomType.LECTURE_HALL: (0.6, 0.9),
        RoomType.CHURCH: (1.5, 3.0),
        RoomType.CONCERT_HALL: (1.5, 2.5),
        RoomType.RECORDING_STUDIO: (0.3, 0.5),
        RoomType.GYMNASIUM: (1.0, 1.5),
    }
    return recommendations.get(room_type, (0.5, 1.0))


# =============================================================================
# Noise Criteria
# =============================================================================

def noise_criteria(spectrum: Dict[int, float]) -> int:
    """
    Estimate Noise Criteria (NC) rating from octave band spectrum.
    
    Args:
        spectrum: Dictionary mapping center frequencies to dB values
                  Common frequencies: 63, 125, 250, 500, 1000, 2000, 4000, 8000
    
    Returns:
        NC rating (approximate)
    
    Examples:
        >>> spectrum = {63: 50, 125: 45, 250: 40, 500: 35, 1000: 32, 2000: 30, 4000: 28, 8000: 26}
        >>> nc = noise_criteria(spectrum)
        >>> 25 <= nc <= 40
        True
    """
    # NC contour values (tangent method approximation)
    # NC contours are defined at 8 octave bands
    nc_contours = {
        15: {63: 47, 125: 36, 250: 29, 500: 22, 1000: 17, 2000: 14, 4000: 12, 8000: 11},
        20: {63: 51, 125: 40, 250: 33, 500: 26, 1000: 22, 2000: 19, 4000: 17, 8000: 16},
        25: {63: 54, 125: 44, 250: 37, 500: 31, 1000: 27, 2000: 24, 4000: 22, 8000: 21},
        30: {63: 57, 125: 48, 250: 41, 500: 35, 1000: 31, 2000: 29, 4000: 28, 8000: 27},
        35: {63: 60, 125: 52, 250: 45, 500: 40, 1000: 36, 2000: 34, 4000: 33, 8000: 32},
        40: {63: 64, 125: 56, 250: 50, 500: 45, 1000: 41, 2000: 39, 4000: 38, 8000: 37},
        45: {63: 67, 125: 60, 250: 54, 500: 49, 1001: 46, 2000: 44, 4000: 43, 8000: 42},
        50: {63: 71, 125: 64, 250: 58, 500: 54, 1000: 51, 2000: 49, 4000: 48, 8000: 47},
        55: {63: 74, 125: 67, 250: 62, 500: 58, 1000: 56, 2000: 54, 4000: 53, 8000: 52},
        60: {63: 77, 125: 71, 250: 67, 500: 63, 1000: 61, 2000: 59, 4000: 58, 8000: 57},
        65: {63: 80, 125: 75, 250: 71, 500: 68, 1000: 66, 2000: 64, 4000: 63, 8000: 62},
        70: {63: 83, 125: 79, 250: 75, 500: 72, 1000: 71, 2000: 69, 4000: 68, 8000: 67},
    }
    
    # Find the lowest NC contour that is exceeded by the measured spectrum
    for nc in sorted(nc_contours.keys()):
        exceeded = False
        for freq, level in spectrum.items():
            if freq in nc_contours[nc] and level > nc_contours[nc][freq]:
                exceeded = True
                break
        if not exceeded:
            return nc
    
    return 70  # Maximum NC rating


# =============================================================================
# Sound Exposure and Dose
# =============================================================================

def sound_exposure_level(level: float, duration: float, reference_duration: float = 1.0) -> float:
    """
    Calculate Sound Exposure Level (SEL/LEQ).
    
    SEL = L + 10 * log10(T / T_ref)
    
    Args:
        level: Sound level in dB
        duration: Exposure duration in seconds
        reference_duration: Reference duration in seconds (default: 1 second for SEL)
    
    Returns:
        Sound exposure level in dB
    
    Examples:
        >>> round(sound_exposure_level(85, 8 * 3600, 8 * 3600), 1)  # 8-hour Leq
        85.0
    """
    return level + 10 * math.log10(duration / reference_duration)


def equivalent_continuous_level(*measurements: Tuple[float, float]) -> float:
    """
    Calculate equivalent continuous sound level (Leq) from time-varying measurements.
    
    Leq = 10 * log10(sum(Ti * 10^(Li/10)) / sum(Ti))
    
    Args:
        *measurements: Tuples of (level in dB, duration in seconds)
    
    Returns:
        Equivalent continuous sound level in dB
    
    Examples:
        >>> round(equivalent_continuous_level((80, 3600), (90, 3600)), 1)
        87.4
    """
    if not measurements:
        return float('-inf')
    
    total_time = sum(t for _, t in measurements)
    total_exposure = sum(t * 10 ** (L / 10) for L, t in measurements)
    
    return 10 * math.log10(total_exposure / total_time)


def noise_dose(level: float, duration: float, criterion: float = 85, exchange_rate: float = 3) -> float:
    """
    Calculate noise dose for occupational exposure.
    
    Dose = (T / T_allowed) * 100%
    
    Args:
        level: Sound level in dB
        duration: Exposure duration in hours
        criterion: Criterion level (default: 85 dB for 8 hours)
        exchange_rate: Exchange rate in dB (default: 3 dB = doubling)
    
    Returns:
        Noise dose as percentage
    
    Examples:
        >>> round(noise_dose(85, 8), 1)
        100.0
        >>> round(noise_dose(88, 4), 1)  # 3 dB higher, half the time
        100.0
    """
    # Calculate allowed duration
    # For 3 dB exchange rate: T_allowed = 8 * 2^((criterion - level) / exchange_rate)
    allowed_duration = 8 * (2 ** ((criterion - level) / exchange_rate))
    
    return (duration / allowed_duration) * 100


def time_weighted_average(*measurements: Tuple[float, float], criterion: float = 85, exchange_rate: float = 3) -> float:
    """
    Calculate Time-Weighted Average (TWA) noise exposure.
    
    Args:
        *measurements: Tuples of (level in dB, duration in hours)
        criterion: Criterion level (default: 85 dB)
        exchange_rate: Exchange rate in dB (default: 3 dB)
    
    Returns:
        TWA in dB
    
    Examples:
        >>> round(time_weighted_average((85, 8)), 0)
        85.0
    """
    if not measurements:
        return 0.0
    
    # Calculate total dose
    total_dose = sum(
        duration * (2 ** ((level - criterion) / exchange_rate))
        for level, duration in measurements
    )
    
    # Calculate TWA
    total_duration = sum(d for _, d in measurements)
    
    if total_duration <= 0:
        return 0.0
    
    # Normalize to 8 hours if total duration is different
    normalized_dose = total_dose * (8 / total_duration) if total_duration > 0 else 0
    
    return criterion + exchange_rate * math.log2(normalized_dose / 8) if normalized_dose > 0 else 0


# =============================================================================
# Utility Functions
# =============================================================================

def db_to_linear(decibels: float) -> float:
    """
    Convert decibels to linear scale.
    
    Args:
        decibels: Value in decibels
    
    Returns:
        Linear value
    
    Examples:
        >>> round(db_to_linear(20), 2)
        10.0
        >>> round(db_to_linear(0), 2)
        1.0
    """
    return 10 ** (decibels / 10)


def linear_to_db(linear: float) -> float:
    """
    Convert linear scale to decibels.
    
    Args:
        linear: Linear value (must be positive)
    
    Returns:
        Value in decibels
    
    Examples:
        >>> linear_to_db(10)
        10.0
        >>> linear_to_db(1)
        0.0
    """
    if linear <= 0:
        return float('-inf')
    
    return 10 * math.log10(linear)


def db_gain(gain_db: float) -> float:
    """
    Calculate linear gain from dB gain.
    
    Args:
        gain_db: Gain in decibels
    
    Returns:
        Linear gain factor
    
    Examples:
        >>> round(db_gain(6), 2)
        2.0
        >>> round(db_gain(-6), 2)
        0.5
    """
    return 10 ** (gain_db / 10)


def amplitude_ratio_db(amplitude: float, reference: float = 1.0) -> float:
    """
    Calculate dB from amplitude ratio.
    
    dB = 20 * log10(A / A_ref)
    
    Args:
        amplitude: Amplitude value
        reference: Reference amplitude
    
    Returns:
        Decibel value
    
    Examples:
        >>> amplitude_ratio_db(2)
        6.0
        >>> amplitude_ratio_db(10)
        20.0
    """
    if amplitude <= 0 or reference <= 0:
        return float('-inf')
    
    return 20 * math.log10(amplitude / reference)


def sound_power_level(power: float, reference: float = REFERENCE_SOUND_POWER) -> float:
    """
    Calculate sound power level (Lw or SWL).
    
    Lw = 10 * log10(W / W_ref)
    
    Args:
        power: Sound power in watts
        reference: Reference power (default: 10^-12 W)
    
    Returns:
        Sound power level in dB
    
    Examples:
        >>> sound_power_level(0.001)  # 1 mW
        90.0
    """
    return db_from_power(power, reference)


def sound_intensity_level(intensity: float, reference: float = REFERENCE_SOUND_INTENSITY) -> float:
    """
    Calculate sound intensity level (Li).
    
    Li = 10 * log10(I / I_ref)
    
    Args:
        intensity: Sound intensity in W/m²
        reference: Reference intensity (default: 10^-12 W/m²)
    
    Returns:
        Sound intensity level in dB
    
    Examples:
        >>> sound_intensity_level(1e-6)
        60.0
    """
    return db_from_intensity(intensity, reference)


def hearing_threshold_shift(exposure_level: float, exposure_hours: float) -> float:
    """
    Estimate temporary threshold shift from noise exposure.
    
    Simplified model based on ISO 1999.
    
    Args:
        exposure_level: A-weighted exposure level in dB
        exposure_hours: Exposure duration in hours
    
    Returns:
        Estimated temporary threshold shift in dB
    
    Examples:
        >>> hearing_threshold_shift(85, 8)
        0.0
        >>> hearing_threshold_shift(100, 8) > 0
        True
    """
    # Simplified TTS model
    # TTS ≈ max(0, (L - 75) * log10(T) / 2)
    if exposure_level <= 75:
        return 0.0
    
    return max(0, (exposure_level - 75) * math.log10(max(1, exposure_hours)) / 2)


# =============================================================================
# Main AcousticUtils Class
# =============================================================================

class AcousticUtils:
    """
    Comprehensive acoustic calculation utilities.
    
    Provides methods for decibel calculations, sound propagation,
    room acoustics, and more.
    """
    
    # Constants
    SPEED_OF_SOUND = SPEED_OF_SOUND_20C
    REF_PRESSURE = REFERENCE_SOUND_PRESSURE
    REF_INTENSITY = REFERENCE_SOUND_INTENSITY
    REF_POWER = REFERENCE_SOUND_POWER
    
    @staticmethod
    def db_from_power(power: float, reference: float = REF_POWER) -> float:
        """Calculate decibels from power."""
        return db_from_power(power, reference)
    
    @staticmethod
    def db_from_pressure(pressure: float, reference: float = REF_PRESSURE) -> float:
        """Calculate sound pressure level in decibels."""
        return db_from_pressure(pressure, reference)
    
    @staticmethod
    def db_from_intensity(intensity: float, reference: float = REF_INTENSITY) -> float:
        """Calculate decibels from sound intensity."""
        return db_from_intensity(intensity, reference)
    
    @staticmethod
    def add_decibels(*levels: float) -> float:
        """Add multiple sound levels in decibels."""
        return add_decibels(*levels)
    
    @staticmethod
    def subtract_decibels(total: float, background: float) -> float:
        """Subtract background noise from total level."""
        return subtract_decibels(total, background)
    
    @staticmethod
    def average_decibels(*levels: float) -> float:
        """Calculate energy average of sound levels."""
        return average_decibels(*levels)
    
    @staticmethod
    def wavelength(frequency: float, speed: float = SPEED_OF_SOUND) -> float:
        """Calculate wavelength from frequency."""
        return wavelength(frequency, speed)
    
    @staticmethod
    def frequency(wavelength_m: float, speed: float = SPEED_OF_SOUND) -> float:
        """Calculate frequency from wavelength."""
        return frequency_from_wavelength(wavelength_m, speed)
    
    @staticmethod
    def speed_of_sound(temperature: float = 20.0) -> float:
        """Calculate speed of sound at given temperature."""
        return speed_of_sound(temperature)
    
    @staticmethod
    def doppler_frequency(
        source_freq: float,
        source_vel: float = 0,
        observer_vel: float = 0,
        speed: float = SPEED_OF_SOUND,
        approaching: bool = True
    ) -> float:
        """Calculate Doppler-shifted frequency."""
        return doppler_frequency(source_freq, source_vel, observer_vel, speed, approaching)
    
    @staticmethod
    def distance_attenuation(distance: float, ref_distance: float = 1.0) -> float:
        """Calculate sound attenuation over distance."""
        return distance_attenuation(distance, ref_distance)
    
    @staticmethod
    def sound_at_distance(source_level: float, distance: float, ref_distance: float = 1.0) -> float:
        """Calculate sound level at a distance."""
        return sound_level_at_distance(source_level, distance, ref_distance)
    
    @staticmethod
    def a_weighting(frequency: float) -> float:
        """Get A-weighting correction for frequency."""
        return a_weighting(frequency)
    
    @staticmethod
    def c_weighting(frequency: float) -> float:
        """Get C-weighting correction for frequency."""
        return c_weighting(frequency)
    
    @staticmethod
    def apply_weighting(db: float, freq: float, weighting: FrequencyWeighting = FrequencyWeighting.A) -> float:
        """Apply frequency weighting to sound level."""
        return apply_weighting(db, freq, weighting)
    
    @staticmethod
    def phon_to_sone(phon: float) -> float:
        """Convert phon to sone."""
        return phon_to_sone(phon)
    
    @staticmethod
    def sone_to_phon(sone: float) -> float:
        """Convert sone to phon."""
        return sone_to_phon(sone)
    
    @staticmethod
    def rt60_sabine(room: RoomAcoustics, absorption: float) -> float:
        """Calculate RT60 using Sabine's formula."""
        return sabine_rt60(room, absorption)
    
    @staticmethod
    def rt60_eyring(room: RoomAcoustics, absorption: float) -> float:
        """Calculate RT60 using Eyring's formula."""
        return eyring_rt60(room, absorption)
    
    @staticmethod
    def room_modes(room: RoomAcoustics, max_mode: int = 5) -> List[Tuple[int, int, int, float]]:
        """Calculate room resonance frequencies."""
        return room_modes(room, max_mode)
    
    @staticmethod
    def critical_distance(q: float, room: RoomAcoustics, absorption: float) -> float:
        """Calculate critical distance in room."""
        return critical_distance(q, room, absorption)
    
    @staticmethod
    def noise_dose(level: float, duration: float, criterion: float = 85, exchange: float = 3) -> float:
        """Calculate noise dose percentage."""
        return noise_dose(level, duration, criterion, exchange)
    
    @staticmethod
    def leq(*measurements: Tuple[float, float]) -> float:
        """Calculate equivalent continuous level."""
        return equivalent_continuous_level(*measurements)


# =============================================================================
# Convenience Functions
# =============================================================================

def calculate_rt60(room_length: float, room_width: float, room_height: float, absorption: float) -> dict:
    """
    Calculate room acoustic parameters.
    
    Args:
        room_length: Room length in meters
        room_width: Room width in meters
        room_height: Room height in meters
        absorption: Average absorption coefficient
    
    Returns:
        Dictionary with acoustic parameters
    
    Examples:
        >>> result = calculate_rt60(5, 4, 3, 0.2)
        >>> 'sabine_rt60' in result
        True
    """
    room = RoomAcoustics(room_length, room_width, room_height)
    
    return {
        'volume_m3': room.volume,
        'surface_area_m2': room.surface_area,
        'floor_area_m2': room.floor_area(),
        'sabine_rt60': sabine_rt60(room, absorption),
        'eyring_rt60': eyring_rt60(room, absorption),
        'critical_distance': critical_distance(1, room, absorption),
        'first_three_modes': room_modes(room, 2)[:3],
    }


def sound_level_summary(pressure_pa: float) -> dict:
    """
    Generate comprehensive sound level summary.
    
    Args:
        pressure_pa: Sound pressure in pascals
    
    Returns:
        Dictionary with various sound level metrics
    
    Examples:
        >>> summary = sound_level_summary(0.02)  # 60 dB
        >>> summary['spl_db']
        60.0
    """
    spl = db_from_pressure(pressure_pa)
    
    return {
        'pressure_pa': pressure_pa,
        'spl_db': spl,
        'intensity_w_m2': intensity_from_db(spl),
        'power_w': power_from_db(spl) if spl > 0 else 0,
        'perceived_loudness': 'Silent' if spl < 20 else 'Quiet' if spl < 40 else 'Moderate' if spl < 60 else 'Loud' if spl < 80 else 'Very Loud' if spl < 100 else 'Dangerous',
        'hearing_damage_risk': 'Safe' if spl < 85 else 'Caution' if spl < 100 else 'High Risk' if spl < 120 else 'Immediate Danger',
    }