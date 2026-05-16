#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Acoustic Utilities Examples

Practical examples demonstrating acoustic calculations.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    db_from_pressure,
    db_from_power,
    db_from_intensity,
    add_decibels,
    subtract_decibels,
    distance_attenuation,
    sound_level_at_distance,
    wavelength,
    frequency_from_wavelength,
    speed_of_sound,
    doppler_frequency,
    a_weighting,
    c_weighting,
    apply_weighting,
    FrequencyWeighting,
    phon_to_sone,
    sone_to_phon,
    RoomAcoustics,
    sabine_rt60,
    eyring_rt60,
    room_modes,
    critical_distance,
    recommended_rt60,
    RoomType,
    noise_criteria,
    noise_dose,
    equivalent_continuous_level,
    AcousticUtils,
    calculate_rt60,
    sound_level_summary,
)


def example_basic_decibels():
    """Example: Basic decibel calculations."""
    print("\n" + "="*60)
    print("Example 1: Basic Decibel Calculations")
    print("="*60)
    
    # Sound pressure to SPL
    pressure = 0.02  # 20 Pa
    spl = db_from_pressure(pressure)
    print(f"\nSound pressure {pressure} Pa -> SPL: {spl:.1f} dB")
    
    # Sound power to dB
    power = 0.001  # 1 mW
    power_db = db_from_power(power)
    print(f"Sound power {power} W -> Level: {power_db:.1f} dB")
    
    # Sound intensity to dB
    intensity = 1e-6  # 1 µW/m²
    intensity_db = db_from_intensity(intensity)
    print(f"Sound intensity {intensity} W/m² -> Level: {intensity_db:.1f} dB")


def example_decibel_operations():
    """Example: Adding and subtracting sound levels."""
    print("\n" + "="*60)
    print("Example 2: Sound Level Operations")
    print("="*60)
    
    # Adding sound levels (incoherent sources)
    print("\nAdding sound levels:")
    print(f"60 dB + 60 dB = {add_decibels(60, 60):.1f} dB (+3 dB)")
    print(f"60 dB + 60 dB + 60 dB = {add_decibels(60, 60, 60):.1f} dB")
    print(f"80 dB + 70 dB = {add_decibels(80, 70):.1f} dB")
    
    # Subtracting background noise
    print("\nSubtracting background noise:")
    print(f"60 dB total - 50 dB background = {subtract_decibels(60, 50):.1f} dB")


def example_distance_attenuation():
    """Example: Sound propagation over distance."""
    print("\n" + "="*60)
    print("Example 3: Distance Attenuation")
    print("="*60)
    
    # Point source at 100 dB at 1 meter
    source_level = 100
    reference_distance = 1
    
    print(f"\nSource: {source_level} dB at {reference_distance} m")
    print("\nSound levels at various distances:")
    
    distances = [2, 5, 10, 20, 50, 100]
    for d in distances:
        level = sound_level_at_distance(source_level, d, reference_distance)
        attenuation = distance_attenuation(d, reference_distance)
        print(f"  {d} m: {level:.1f} dB (attenuation: {attenuation:.1f} dB)")


def example_wavelength():
    """Example: Wavelength and frequency calculations."""
    print("\n" + "="*60)
    print("Example 4: Wavelength and Frequency")
    print("="*60)
    
    # Common frequencies
    frequencies = [20, 100, 440, 1000, 4000, 20000]
    
    print("\nFrequency -> Wavelength (at 20°C):")
    for f in frequencies:
        wl = wavelength(f)
        print(f"  {f} Hz -> {wl:.4f} m ({wl*100:.1f} cm)")
    
    # Speed of sound at different temperatures
    print("\nSpeed of sound at different temperatures:")
    temps = [0, 10, 20, 30, 40]
    for t in temps:
        c = speed_of_sound(t)
        print(f"  {t}°C: {c:.1f} m/s")


def example_doppler():
    """Example: Doppler effect calculations."""
    print("\n" + "="*60)
    print("Example 5: Doppler Effect")
    print("="*60)
    
    # Car horn example
    horn_freq = 440  # Hz
    car_speed = 30  # m/s (≈ 108 km/h)
    
    print(f"\nCar horn: {horn_freq} Hz")
    print(f"Car speed: {car_speed} m/s ({car_speed * 3.6:.0f} km/h)")
    
    # Approaching
    approaching_freq = doppler_frequency(horn_freq, source_velocity=car_speed, approaching=True)
    print(f"\nApproaching: {approaching_freq:.1f} Hz (↑{approaching_freq - horn_freq:.1f} Hz)")
    
    # Receding
    receding_freq = doppler_frequency(horn_freq, source_velocity=car_speed, approaching=False)
    print(f"Receding: {receding_freq:.1f} Hz (↓{horn_freq - receding_freq:.1f} Hz)")


def example_weighting():
    """Example: Frequency weighting."""
    print("\n" + "="*60)
    print("Example 6: Frequency Weighting (A and C)")
    print("="*60)
    
    # Frequencies to test
    frequencies = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
    
    print("\nWeighting corrections:")
    print(f"{'Frequency':<12} {'A-weighting':<12} {'C-weighting':<12}")
    print("-" * 36)
    
    for f in frequencies:
        a_cor = a_weighting(f)
        c_cor = c_weighting(f)
        print(f"{f} Hz{'':<8} {a_cor:>6.1f} dB{'':<5} {c_cor:>6.1f} dB")


def example_loudness():
    """Example: Loudness conversions."""
    print("\n" + "="*60)
    print("Example 7: Loudness Conversions (Phon and Sone)")
    print("="*60)
    
    print("\nPhon -> Sone conversions:")
    print(f"{'Phon':<10} {'Sone':<10} {'Description':<20}")
    print("-" * 40)
    
    phon_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]
    descriptions = ['Very quiet', 'Quiet', 'Reference', 'Moderate', 'Loud', 
                    'Very loud', 'Extremely loud', 'Dangerous', 'Painful']
    
    for phon, desc in zip(phon_values, descriptions):
        sone = phon_to_sone(phon)
        print(f"{phon:<10} {sone:>6.2f}{'':<3} {desc}")
    
    print("\nKey relationships:")
    print("  40 phon = 1 sone (reference loudness)")
    print("  Every +10 phon = ×2 sone (doubling loudness)")


def example_room_acoustics():
    """Example: Room acoustics calculations."""
    print("\n" + "="*60)
    print("Example 8: Room Acoustics")
    print("="*60)
    
    # Living room example
    room = RoomAcoustics(length=5, width=4, height=3)
    
    print(f"\nRoom dimensions:")
    print(f"  Length: {room.length} m")
    print(f"  Width: {room.width} m")
    print(f"  Height: {room.height} m")
    print(f"  Volume: {room.volume} m³")
    print(f"  Surface area: {room.surface_area} m²")
    
    # RT60 for different absorption coefficients
    print("\nReverberation time (RT60):")
    absorption_values = [0.1, 0.2, 0.3, 0.5]
    print(f"{'Absorption':<12} {'Sabine RT60':<15} {'Eyring RT60':<15}")
    print("-" * 42)
    
    for alpha in absorption_values:
        sabine = sabine_rt60(room, alpha)
        eyring = eyring_rt60(room, alpha)
        print(f"{alpha:<12} {sabine:>6.2f} s{'':<7} {eyring:>6.2f} s")
    
    # Room modes
    print("\nFirst 5 room modes:")
    modes = room_modes(room, 2)
    for nx, ny, nz, freq in modes[:5]:
        mode_type = "Axial" if sum([nx, ny, nz]) == 1 else "Tangential" if sum([nx, ny, nz]) == 2 else "Oblique"
        print(f"  ({nx},{ny},{nz}): {freq:.1f} Hz [{mode_type}]")
    
    # Recommended RT60 for different room types
    print("\nRecommended RT60 for different room types:")
    room_types = [RoomType.RECORDING_STUDIO, RoomType.LIVING_ROOM, RoomType.CONCERT_HALL, RoomType.CHURCH]
    for rt in room_types:
        min_rt, max_rt = recommended_rt60(rt)
        print(f"  {rt.value}: {min_rt}-{max_rt} s")


def example_noise_exposure():
    """Example: Occupational noise exposure."""
    print("\n" + "="*60)
    print("Example 9: Occupational Noise Exposure")
    print("="*60)
    
    print("\nNoise dose for 85 dB criterion, 3 dB exchange rate:")
    print(f"{'Level':<10} {'Duration':<12} {'Dose':<10}")
    print("-" * 32)
    
    exposures = [
        (85, 8, "Full shift"),
        (88, 4, "Half shift"),
        (91, 2, "Quarter shift"),
        (80, 8, "Below criterion"),
        (100, 0.5, "Very loud"),
    ]
    
    for level, duration, note in exposures:
        dose = noise_dose(level, duration)
        print(f"{level} dB{'':<5} {duration} h{'':<6} {dose:.1f}%")
    
    # Leq calculation
    print("\nEquivalent continuous level (Leq) example:")
    measurements = [(80, 3600), (85, 3600), (90, 3600)]
    leq = equivalent_continuous_level(*measurements)
    print(f"  Measurements: 80 dB (1h), 85 dB (1h), 90 dB (1h)")
    print(f"  Leq: {leq:.1f} dB")


def example_sound_level_summary():
    """Example: Sound level summary."""
    print("\n" + "="*60)
    print("Example 10: Sound Level Summary")
    print("="*60)
    
    pressures = [2e-5, 2e-4, 2e-3, 2e-2, 0.2, 2]
    
    print("\nSound level analysis for various pressures:")
    for p in pressures:
        summary = sound_level_summary(p)
        print(f"\n{p} Pa:")
        print(f"  SPL: {summary['spl_db']:.1f} dB")
        print(f"  Loudness: {summary['perceived_loudness']}")
        print(f"  Risk: {summary['hearing_damage_risk']}")


def example_acoustic_utils_class():
    """Example: Using AcousticUtils class."""
    print("\n" + "="*60)
    print("Example 11: AcousticUtils Class")
    print("="*60)
    
    # All methods available through the class
    utils = AcousticUtils
    
    print("\nAvailable constants:")
    print(f"  Speed of sound (20°C): {utils.SPEED_OF_SOUND} m/s")
    print(f"  Reference pressure: {utils.REF_PRESSURE} Pa")
    
    print("\nSample calculations:")
    print(f"  dB from pressure (0.02 Pa): {utils.db_from_pressure(0.02):.1f} dB")
    print(f"  Wavelength (440 Hz): {utils.wavelength(440):.3f} m")
    print(f"  Add decibels (60+60): {utils.add_decibels(60, 60):.1f} dB")


def example_calculate_rt60():
    """Example: Comprehensive RT60 calculation."""
    print("\n" + "="*60)
    print("Example 12: Comprehensive Room Acoustics Report")
    print("="*60)
    
    result = calculate_rt60(6, 5, 3.5, 0.25)
    
    print(f"\nRoom acoustic analysis:")
    print(f"  Volume: {result['volume_m3']} m³")
    print(f"  Surface area: {result['surface_area_m2']} m²")
    print(f"  Floor area: {result['floor_area_m2']} m²")
    print(f"  Sabine RT60: {result['sabine_rt60']:.2f} s")
    print(f"  Eyring RT60: {result['eyring_rt60']:.2f} s")
    print(f"  Critical distance: {result['critical_distance']:.2f} m")
    
    print("\nFirst room modes:")
    for mode in result['first_three_modes']:
        nx, ny, nz, freq = mode
        print(f"  ({nx},{ny},{nz}): {freq:.1f} Hz")


if __name__ == '__main__':
    # Run all examples
    example_basic_decibels()
    example_decibel_operations()
    example_distance_attenuation()
    example_wavelength()
    example_doppler()
    example_weighting()
    example_loudness()
    example_room_acoustics()
    example_noise_exposure()
    example_sound_level_summary()
    example_acoustic_utils_class()
    example_calculate_rt60()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)