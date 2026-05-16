#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for Acoustic Utilities Module

Comprehensive test suite for acoustic calculation functions.
"""

import math
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from acoustic_utils import (
    # Constants
    SPEED_OF_SOUND_20C,
    REFERENCE_SOUND_PRESSURE,
    REFERENCE_SOUND_INTENSITY,
    REFERENCE_SOUND_POWER,
    
    # Enums
    FrequencyWeighting,
    RoomType,
    
    # Data Classes
    SoundLevel,
    RoomAcoustics,
    
    # Core Decibel Functions
    db_from_power,
    db_from_intensity,
    db_from_pressure,
    power_from_db,
    intensity_from_db,
    pressure_from_db,
    
    # Sound Level Operations
    add_decibels,
    subtract_decibels,
    average_decibels,
    decibel_difference,
    
    # Distance Attenuation
    distance_attenuation,
    sound_level_at_distance,
    distance_from_sound_level,
    
    # Wavelength and Frequency
    wavelength,
    frequency_from_wavelength,
    speed_of_sound,
    
    # Doppler Effect
    doppler_frequency,
    doppler_shift,
    
    # Frequency Weighting
    a_weighting,
    c_weighting,
    apply_weighting,
    
    # Loudness Conversions
    phon_to_sone,
    sone_to_phon,
    db_to_phon,
    
    # Room Acoustics
    sabine_rt60,
    eyring_rt60,
    room_modes,
    critical_distance,
    recommended_rt60,
    
    # Noise Criteria
    noise_criteria,
    
    # Sound Exposure and Dose
    sound_exposure_level,
    equivalent_continuous_level,
    noise_dose,
    time_weighted_average,
    
    # Utility Functions
    db_to_linear,
    linear_to_db,
    db_gain,
    amplitude_ratio_db,
    sound_power_level,
    sound_intensity_level,
    hearing_threshold_shift,
    
    # Main Class
    AcousticUtils,
    
    # Convenience Functions
    calculate_rt60,
    sound_level_summary,
)


class TestDecibelCalculations:
    """Test decibel conversion functions."""
    
    def test_db_from_power(self):
        """Test power to decibel conversion."""
        # Reference power should be 0 dB
        assert db_from_power(1e-12) == 0.0
        
        # 10x power = 10 dB
        assert db_from_power(1e-11) == 10.0
        
        # 100x power = 20 dB
        assert db_from_power(1e-10) == 20.0
        
        # 1 mW = 90 dB
        assert db_from_power(0.001) == 90.0
        
    def test_db_from_intensity(self):
        """Test intensity to decibel conversion."""
        assert db_from_intensity(1e-12) == 0.0
        assert db_from_intensity(1e-6) == 60.0
        assert db_from_intensity(1e-3) == 90.0
        
    def test_db_from_pressure(self):
        """Test pressure to sound pressure level conversion."""
        # Reference pressure should be 0 dB (threshold of hearing)
        assert db_from_pressure(20e-6) == 0.0
        
        # 20 Pa = 60 dB
        assert round(db_from_pressure(0.02)) == 60
        
        # 200 Pa = 80 dB
        assert round(db_from_pressure(0.2)) == 80
        
    def test_power_from_db(self):
        """Test decibel to power conversion."""
        assert power_from_db(0) == 1e-12
        assert power_from_db(90) == 0.001
        
    def test_intensity_from_db(self):
        """Test decibel to intensity conversion."""
        assert intensity_from_db(0) == 1e-12
        assert intensity_from_db(60) == 1e-6
        
    def test_pressure_from_db(self):
        """Test decibel to pressure conversion."""
        assert pressure_from_db(0) == 20e-6
        assert round(pressure_from_db(60), 2) == 0.02
        
    def test_db_roundtrip(self):
        """Test that conversions are reversible."""
        # Power
        p1 = 0.001
        db = db_from_power(p1)
        p2 = power_from_db(db)
        assert abs(p1 - p2) < 1e-10
        
        # Pressure
        pr1 = 0.05
        db = db_from_pressure(pr1)
        pr2 = pressure_from_db(db)
        assert abs(pr1 - pr2) < 1e-10


class TestDecibelOperations:
    """Test decibel arithmetic operations."""
    
    def test_add_decibels(self):
        """Test adding sound levels."""
        # Two equal sources add 3 dB
        assert round(add_decibels(60, 60)) == 63
        
        # Three equal sources add ~4.8 dB
        assert round(add_decibels(60, 60, 60), 1) == 64.8
        
        # Adding to a much louder source
        result = add_decibels(80, 70)
        assert round(result, 1) == 80.4
        
    def test_add_decibels_zero(self):
        """Test adding with zero level."""
        assert add_decibels(60) == 60
        
    def test_subtract_decibels(self):
        """Test subtracting background noise."""
        # Subtract 50 dB background from 60 dB total
        result = subtract_decibels(60, 50)
        assert round(result, 1) == 59.5
        
        # Subtract nearly equal levels
        result = subtract_decibels(60, 59)
        assert result > 50  # Should be significantly lower
        
    def test_average_decibels(self):
        """Test averaging sound levels."""
        result = average_decibels(60, 70, 80)
        # Energy average gives higher result than arithmetic average
        assert 70 < result < 80
        
        # Equal levels should average to same
        assert average_decibels(70, 70, 70) == 70
        
    def test_decibel_difference(self):
        """Test difference between levels."""
        assert decibel_difference(80, 70) == 10
        assert decibel_difference(70, 80) == 10  # Absolute value


class TestDistanceAttenuation:
    """Test sound propagation over distance."""
    
    def test_distance_attenuation(self):
        """Test inverse square law attenuation."""
        # Double distance = 6 dB loss
        assert round(distance_attenuation(2, 1)) == 6
        
        # 10x distance = 20 dB loss
        assert round(distance_attenuation(10, 1)) == 20
        
        # 100x distance = 40 dB loss
        assert round(distance_attenuation(100, 1)) == 40
        
    def test_sound_level_at_distance(self):
        """Test sound level at specific distance."""
        # 100 dB at 1m = 80 dB at 10m
        result = sound_level_at_distance(100, 10, 1)
        assert round(result) == 80
        
        # Same distance = same level
        assert sound_level_at_distance(60, 5, 5) == 60
        
    def test_distance_from_sound_level(self):
        """Test calculating distance from sound levels."""
        # If source is 100 dB at 1m, at what distance is it 80 dB?
        distance = distance_from_sound_level(100, 80, 1)
        assert round(distance) == 10


class TestWavelengthAndFrequency:
    """Test wavelength and frequency conversions."""
    
    def test_wavelength(self):
        """Test frequency to wavelength conversion."""
        # A4 (440 Hz) wavelength
        wl = wavelength(440)
        assert 0.77 < wl < 0.79
        
        # 1000 Hz wavelength
        wl = wavelength(1000)
        assert round(wl, 3) == 0.343
        
    def test_frequency_from_wavelength(self):
        """Test wavelength to frequency conversion."""
        freq = frequency_from_wavelength(0.343)
        assert round(freq) == 1000
        
    def test_wavelength_frequency_roundtrip(self):
        """Test that wavelength and frequency conversions are reversible."""
        f1 = 1000
        wl = wavelength(f1)
        f2 = frequency_from_wavelength(wl)
        assert abs(f1 - f2) < 0.01
        
    def test_speed_of_sound(self):
        """Test speed of sound calculation."""
        # At 20°C
        c = speed_of_sound(20)
        assert 343 < c < 344
        
        # At 0°C
        c = speed_of_sound(0)
        assert 330 < c < 332


class TestDopplerEffect:
    """Test Doppler effect calculations."""
    
    def test_doppler_approaching(self):
        """Test Doppler shift when source approaches."""
        # Source at 440 Hz moving toward observer at 30 m/s
        f_observed = doppler_frequency(440, source_velocity=30, approaching=True)
        assert f_observed > 440  # Higher frequency when approaching
        
    def test_doppler_receding(self):
        """Test Doppler shift when source recedes."""
        f_observed = doppler_frequency(440, source_velocity=30, approaching=False)
        assert f_observed < 440  # Lower frequency when receding
        
    def test_doppler_observer_moving(self):
        """Test Doppler shift when observer moves."""
        # Observer moving toward stationary source
        f_observed = doppler_frequency(440, observer_velocity=30, approaching=True)
        assert f_observed > 440
        
    def test_doppler_shift(self):
        """Test frequency shift calculation."""
        shift = doppler_shift(440, 30)  # Approaching at 30 m/s
        assert shift > 0  # Positive shift when approaching
        
        shift = doppler_shift(440, -30)  # Receding at 30 m/s
        assert shift < 0  # Negative shift when receding


class TestFrequencyWeighting:
    """Test frequency weighting functions."""
    
    def test_a_weighting_1khz(self):
        """Test A-weighting at 1 kHz (reference frequency)."""
        # A-weighting at 1 kHz should be 0 dB
        result = a_weighting(1000)
        assert abs(result) < 0.1
        
    def test_a_weighting_low_frequency(self):
        """Test A-weighting at low frequency."""
        # Low frequencies are heavily attenuated
        result = a_weighting(100)
        assert result < -15  # Significant negative correction
        
    def test_a_weighting_high_frequency(self):
        """Test A-weighting at high frequency."""
        # High frequencies have small correction
        result = a_weighting(10000)
        assert -5 < result < 0
        
    def test_c_weighting(self):
        """Test C-weighting."""
        # C-weighting is flatter
        result = c_weighting(1000)
        assert abs(result) < 0.1
        
        # Less attenuation at low frequencies
        result = c_weighting(100)
        assert -1 < result < 0
        
    def test_apply_weighting(self):
        """Test applying weighting to sound level."""
        # At 1 kHz, no change
        result = apply_weighting(60, 1000, FrequencyWeighting.A)
        assert abs(result - 60) < 0.1
        
        # At 100 Hz, significant attenuation
        result = apply_weighting(60, 100, FrequencyWeighting.A)
        assert result < 45


class TestLoudnessConversions:
    """Test loudness unit conversions."""
    
    def test_phon_to_sone(self):
        """Test phon to sone conversion."""
        # 40 phon = 1 sone (reference)
        assert phon_to_sone(40) == 1.0
        
        # 50 phon = 2 sones (double loudness)
        assert phon_to_sone(50) == 2.0
        
        # 60 phon = 4 sones
        assert phon_to_sone(60) == 4.0
        
    def test_sone_to_phon(self):
        """Test sone to phon conversion."""
        assert sone_to_phon(1) == 40.0
        assert sone_to_phon(2) == 50.0
        assert sone_to_phon(4) == 60.0
        
    def test_loudness_roundtrip(self):
        """Test that conversions are reversible."""
        phon = 55
        sone = phon_to_sone(phon)
        phon_back = sone_to_phon(sone)
        assert abs(phon - phon_back) < 0.01


class TestRoomAcoustics:
    """Test room acoustic calculations."""
    
    def test_room_properties(self):
        """Test room dimension calculations."""
        room = RoomAcoustics(5, 4, 3)
        
        # Volume = 5 * 4 * 3 = 60 m³
        assert room.volume == 60
        
        # Surface area = 2*(lw + wh + lh) = 2*(20 + 12 + 15) = 94 m²
        assert room.surface_area == 94
        
        # Floor area = 5 * 4 = 20 m²
        assert room.floor_area() == 20
        
    def test_sabine_rt60(self):
        """Test Sabine reverberation time calculation."""
        room = RoomAcoustics(5, 4, 3)
        rt60 = sabine_rt60(room, 0.2)
        
        # Typical RT60 for a small room should be < 2 seconds
        assert 0.5 < rt60 < 2
        
    def test_eyring_rt60(self):
        """Test Eyring reverberation calculation."""
        room = RoomAcoustics(5, 4, 3)
        rt60 = eyring_rt60(room, 0.2)
        
        # Eyring gives similar result to Sabine for moderate absorption
        assert 0.3 < rt60 < 2.5
        
    def test_room_modes(self):
        """Test room mode calculation."""
        room = RoomAcoustics(5, 4, 3)
        modes = room_modes(room, 2)
        
        # Should have multiple modes
        assert len(modes) > 0
        
        # All frequencies should be positive
        assert all(m[3] > 0 for m in modes)
        
        # First axial mode should correspond to longest dimension
        axial_modes = [m for m in modes if sum(m[:3]) == 1]
        assert len(axial_modes) == 3
        
    def test_critical_distance(self):
        """Test critical distance calculation."""
        room = RoomAcoustics(5, 4, 3)
        rc = critical_distance(1, room, 0.2)
        
        # Critical distance should be reasonable for room size
        assert 0.1 < rc < 5
        
    def test_recommended_rt60(self):
        """Test recommended RT60 values."""
        # Recording studio should have short RT60
        min_rt, max_rt = recommended_rt60(RoomType.RECORDING_STUDIO)
        assert 0.3 <= min_rt < max_rt <= 0.5
        
        # Church should have long RT60
        min_rt, max_rt = recommended_rt60(RoomType.CHURCH)
        assert min_rt >= 1.5


class TestNoiseCriteria:
    """Test noise criteria calculations."""
    
    def test_noise_criteria_low(self):
        """Test NC rating for quiet spectrum."""
        # Quiet room spectrum
        spectrum = {
            63: 40, 125: 35, 250: 30, 500: 25,
            1000: 22, 2000: 20, 4000: 18, 8000: 16
        }
        nc = noise_criteria(spectrum)
        assert nc <= 25
        
    def test_noise_criteria_high(self):
        """Test NC rating for noisy spectrum."""
        # Noisy room spectrum
        spectrum = {
            63: 70, 125: 65, 250: 60, 500: 55,
            1000: 52, 2000: 50, 4000: 48, 8000: 46
        }
        nc = noise_criteria(spectrum)
        assert nc >= 50


class TestNoiseDose:
    """Test noise exposure calculations."""
    
    def test_noise_dose_85db_8hours(self):
        """Test 100% dose at 85 dB for 8 hours."""
        dose = noise_dose(85, 8)
        assert round(dose) == 100
        
    def test_noise_dose_88db_4hours(self):
        """Test 100% dose at 88 dB for 4 hours (3 dB exchange)."""
        dose = noise_dose(88, 4)
        assert round(dose) == 100
        
    def test_noise_dose_double_exposure(self):
        """Test that double exposure doubles dose."""
        dose1 = noise_dose(85, 4)
        dose2 = noise_dose(85, 8)
        assert dose2 == 2 * dose1
        
    def test_equivalent_continuous_level(self):
        """Test Leq calculation."""
        # Equal levels should average to same
        leq = equivalent_continuous_level((80, 3600), (80, 3600))
        assert leq == 80
        
        # Higher level dominates
        leq = equivalent_continuous_level((80, 3600), (90, 3600))
        assert leq > 85
        assert leq < 90


class TestSoundExposure:
    """Test sound exposure calculations."""
    
    def test_sound_exposure_level(self):
        """Test SEL calculation."""
        # Same duration should return same level
        sel = sound_exposure_level(85, 8 * 3600, 8 * 3600)
        assert sel == 85
        
        # Longer duration increases SEL
        sel = sound_exposure_level(85, 8 * 3600, 1)
        assert sel > 85
        
    def test_time_weighted_average(self):
        """Test TWA calculation."""
        # 85 dB for 8 hours should give 85 dB TWA
        twa = time_weighted_average((85, 8))
        assert round(twa) == 85


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_db_to_linear(self):
        """Test dB to linear conversion."""
        assert db_to_linear(0) == 1
        assert db_to_linear(10) == 10
        assert db_to_linear(20) == 100
        
    def test_linear_to_db(self):
        """Test linear to dB conversion."""
        assert linear_to_db(1) == 0
        assert linear_to_db(10) == 10
        assert linear_to_db(100) == 20
        
    def test_db_gain(self):
        """Test dB gain conversion."""
        # Power gain: 10 dB = 10x power
        assert round(db_gain(10), 1) == 10.0
        
        # 20 dB = 100x power
        assert round(db_gain(20), 1) == 100.0
        
        # -6 dB ≈ 0.25x power
        assert round(db_gain(-6), 2) == 0.25
        
    def test_amplitude_ratio_db(self):
        """Test amplitude ratio to dB."""
        # Amplitude ratio uses 20*log10 formula
        assert round(amplitude_ratio_db(2), 1) == 6.0  # 2x amplitude ≈ 6 dB
        assert amplitude_ratio_db(10) == 20.0  # 10x amplitude = 20 dB
        assert amplitude_ratio_db(100) == 40.0  # 100x amplitude = 40 dB


class TestAcousticUtilsClass:
    """Test the AcousticUtils class."""
    
    def test_class_constants(self):
        """Test class constants are accessible."""
        assert AcousticUtils.SPEED_OF_SOUND > 300
        assert AcousticUtils.REF_PRESSURE > 0
        assert AcousticUtils.REF_INTENSITY > 0
        
    def test_class_methods(self):
        """Test class methods work correctly."""
        # Decibel methods
        assert AcousticUtils.db_from_power(1e-12) == 0
        assert AcousticUtils.db_from_pressure(20e-6) == 0
        
        # Wavelength method
        wl = AcousticUtils.wavelength(440)
        assert 0.77 < wl < 0.79
        
        # Doppler method
        f = AcousticUtils.doppler_frequency(440, 30, approaching=True)
        assert f > 440


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_calculate_rt60(self):
        """Test RT60 calculation convenience function."""
        result = calculate_rt60(5, 4, 3, 0.2)
        
        assert 'volume_m3' in result
        assert 'surface_area_m2' in result
        assert 'sabine_rt60' in result
        assert 'eyring_rt60' in result
        assert 'critical_distance' in result
        assert 'first_three_modes' in result
        
        assert result['volume_m3'] == 60
        assert result['sabine_rt60'] > 0
        
    def test_sound_level_summary(self):
        """Test sound level summary function."""
        summary = sound_level_summary(0.02)  # 60 dB
        
        assert summary['spl_db'] == 60
        assert summary['intensity_w_m2'] > 0
        assert 'perceived_loudness' in summary
        assert 'hearing_damage_risk' in summary


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_zero_power(self):
        """Test handling of zero or negative power."""
        assert db_from_power(0) == float('-inf')
        assert db_from_power(-1) == float('-inf')
        
    def test_zero_pressure(self):
        """Test handling of zero pressure."""
        assert db_from_pressure(0) == float('-inf')
        
    def test_invalid_distance(self):
        """Test handling of invalid distance."""
        with pytest.raises(ValueError):
            distance_attenuation(0, 1)
            
    def test_invalid_absorption(self):
        """Test handling of invalid absorption coefficient."""
        room = RoomAcoustics(5, 4, 3)
        
        with pytest.raises(ValueError):
            sabine_rt60(room, -0.1)
            
        with pytest.raises(ValueError):
            sabine_rt60(room, 1.5)
            
    def test_zero_sone(self):
        """Test handling of zero sone."""
        with pytest.raises(ValueError):
            sone_to_phon(0)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])