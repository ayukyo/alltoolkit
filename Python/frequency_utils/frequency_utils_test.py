#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Frequency Utilities Test Suite
============================================

Test cases for the frequency_utils module.
"""

import pytest
import math
import sys
import os

# Ensure the module directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Conversion functions
    convert_frequency,
    frequency_to_all,
    frequency_to_period,
    period_to_frequency,
    angular_frequency,
    angular_to_frequency,
    
    # Wavelength functions
    frequency_to_wavelength,
    wavelength_to_frequency,
    get_wavelength_result,
    
    # Musical note functions
    note_to_frequency,
    frequency_to_note,
    get_midi_frequency,
    get_note_harmonics,
    
    # Cent functions
    calculate_cents,
    cents_to_frequency,
    get_cent_result,
    frequency_ratio_to_cents,
    cents_to_ratio,
    
    # Radio spectrum functions
    get_radio_band,
    get_band_frequencies,
    list_radio_bands,
    
    # Utility functions
    is_audio_frequency,
    is_radio_frequency,
    is_visible_light,
    get_frequency_description,
    format_frequency,
    
    # Scale functions
    generate_chromatic_scale,
    note_to_midi,
    generate_major_scale,
    
    # Constants
    SPEED_OF_LIGHT,
    SPEED_OF_SOUND_AIR_20C,
    STANDARD_A4,
    CENTS_PER_OCTAVE,
    
    # Enums
    FrequencyUnit,
    WaveMedium,
)


class TestFrequencyConversion:
    """频率转换测试"""
    
    def test_hz_to_khz(self):
        assert convert_frequency(1000, 'Hz', 'kHz') == 1.0
    
    def test_khz_to_hz(self):
        assert convert_frequency(1, 'kHz', 'Hz') == 1000.0
    
    def test_hz_to_mhz(self):
        assert convert_frequency(1e6, 'Hz', 'MHz') == 1.0
    
    def test_mhz_to_hz(self):
        assert convert_frequency(1, 'MHz', 'Hz') == 1e6
    
    def test_ghz_to_mhz(self):
        assert convert_frequency(1, 'GHz', 'MHz') == 1000.0
    
    def test_hz_to_thz(self):
        assert convert_frequency(1e12, 'Hz', 'THz') == 1.0
    
    def test_rpm_to_hz(self):
        assert convert_frequency(60, 'rpm', 'Hz') == 1.0
    
    def test_hz_to_rpm(self):
        assert convert_frequency(1, 'Hz', 'rpm') == 60.0
    
    def test_rps_to_hz(self):
        assert convert_frequency(1, 'rps', 'Hz') == 1.0
    
    def test_enum_units(self):
        assert convert_frequency(1000, FrequencyUnit.HZ, FrequencyUnit.KILOHZ) == 1.0
    
    def test_invalid_unit(self):
        with pytest.raises(ValueError):
            convert_frequency(1, 'invalid', 'Hz')
    
    def test_frequency_to_all(self):
        result = frequency_to_all(1, 'MHz')
        assert result.hertz == 1e6
        assert result.kilohertz == 1000
        assert result.megahertz == 1
        assert result.gigahertz == 0.001
        assert result.rpm == 6e7


class TestPeriodFunctions:
    """周期转换测试"""
    
    def test_frequency_to_period(self):
        assert frequency_to_period(50) == 0.02
        assert frequency_to_period(1) == 1.0
        assert frequency_to_period(1000) == 0.001
    
    def test_period_to_frequency(self):
        assert period_to_frequency(0.02) == 50.0
        assert period_to_frequency(1) == 1.0
        assert period_to_frequency(0.001) == 1000.0
    
    def test_frequency_period_inverse(self):
        freq = 440
        period = frequency_to_period(freq)
        assert period_to_frequency(period) == freq
    
    def test_invalid_frequency(self):
        with pytest.raises(ValueError):
            frequency_to_period(0)
        with pytest.raises(ValueError):
            frequency_to_period(-1)
    
    def test_invalid_period(self):
        with pytest.raises(ValueError):
            period_to_frequency(0)
    
    def test_angular_frequency(self):
        assert round(angular_frequency(1), 4) == 6.2832
    
    def test_angular_to_frequency(self):
        assert round(angular_to_frequency(2 * math.pi), 4) == 1.0


class TestWavelengthFunctions:
    """波长计算测试"""
    
    def test_frequency_to_wavelength_light(self):
        # 100 MHz radio wave
        wl = frequency_to_wavelength(100e6, SPEED_OF_LIGHT)
        assert round(wl, 2) == 3.0
    
    def test_frequency_to_wavelength_sound(self):
        # 440 Hz sound in air
        wl = frequency_to_wavelength(440, SPEED_OF_SOUND_AIR_20C)
        assert round(wl, 3) == 0.780
    
    def test_wavelength_to_frequency(self):
        freq = wavelength_to_frequency(3, SPEED_OF_LIGHT)
        assert round(freq) == 99930819
    
    def test_wavelength_frequency_inverse(self):
        freq = 100e6
        wl = frequency_to_wavelength(freq)
        freq2 = wavelength_to_frequency(wl)
        assert abs(freq - freq2) < 1
    
    def test_get_wavelength_result(self):
        result = get_wavelength_result(100e6)
        assert result.frequency_hz == 100e6
        assert round(result.wavelength_m, 2) == 3.0
        assert result.wavelength_cm == result.wavelength_m * 100
        assert result.wavelength_mm == result.wavelength_m * 1000
    
    def test_get_wavelength_result_air(self):
        result = get_wavelength_result(440, WaveMedium.AIR)
        assert round(result.wavelength_m, 2) == 0.78
        assert result.medium == '空气 (20°C)'
    
    def test_invalid_frequency_wavelength(self):
        with pytest.raises(ValueError):
            frequency_to_wavelength(0)
        with pytest.raises(ValueError):
            wavelength_to_frequency(0)


class TestMusicalNotes:
    """音乐音符测试"""
    
    def test_note_to_frequency_a4(self):
        assert round(note_to_frequency('A', 4), 2) == 440.0
    
    def test_note_to_frequency_c4(self):
        assert round(note_to_frequency('C', 4), 2) == 261.63
    
    def test_note_to_frequency_sharp(self):
        assert round(note_to_frequency('A#', 4), 2) == 466.16
    
    def test_note_to_frequency_flat(self):
        # Db should equal C#
        db_freq = note_to_frequency('Db', 4)
        cs_freq = note_to_frequency('C#', 4)
        assert round(db_freq, 2) == round(cs_freq, 2) == 277.18
    
    def test_note_to_frequency_custom_a4(self):
        # Using 442 Hz as A4 (some orchestras)
        freq = note_to_frequency('A', 4, a4_hz=442)
        assert freq == 442
    
    def test_frequency_to_note_a4(self):
        result = frequency_to_note(440)
        assert result.note_name == 'A'
        assert result.octave == 4
        assert result.midi_note == 69
    
    def test_frequency_to_note_c4(self):
        result = frequency_to_note(261.63)
        assert result.note_name == 'C'
        assert result.octave == 4
        assert result.midi_note == 60
    
    def test_get_midi_frequency(self):
        assert round(get_midi_frequency(69), 2) == 440.0  # A4
        assert round(get_midi_frequency(60), 2) == 261.63  # C4
    
    def test_midi_range(self):
        with pytest.raises(ValueError):
            get_midi_frequency(-1)
        with pytest.raises(ValueError):
            get_midi_frequency(128)
    
    def test_note_to_midi(self):
        assert note_to_midi('A', 4) == 69
        assert note_to_midi('C', 4) == 60
    
    def test_harmonics(self):
        result = get_note_harmonics(440, 5)
        assert result.fundamental_hz == 440
        assert len(result.harmonics) == 5
        # 1st harmonic (fundamental)
        assert result.harmonics[0][0] == 1
        assert result.harmonics[0][1] == 440
        # 2nd harmonic (octave)
        assert result.harmonics[1][1] == 880
    
    def test_invalid_note(self):
        with pytest.raises(ValueError):
            note_to_frequency('X', 4)
    
    def test_invalid_frequency_note(self):
        with pytest.raises(ValueError):
            frequency_to_note(0)


class TestCentCalculations:
    """音分计算测试"""
    
    def test_octave_cents(self):
        assert calculate_cents(440, 880) == 1200.0
    
    def test_semitone_cents(self):
        # 466.16 Hz is approximately A#4, slight rounding difference
        cents = calculate_cents(440, 466.16)
        assert abs(cents - 100.0) < 0.1
    
    def test_negative_cents(self):
        assert calculate_cents(880, 440) == -1200.0
    
    def test_cents_to_frequency_octave(self):
        assert round(cents_to_frequency(440, 1200), 2) == 880.0
    
    def test_cents_to_frequency_semitone(self):
        assert round(cents_to_frequency(440, 100), 2) == 466.16
    
    def test_cents_frequency_inverse(self):
        cents = 100
        freq = cents_to_frequency(440, cents)
        cents_back = calculate_cents(440, freq)
        assert round(cents_back) == cents
    
    def test_get_cent_result(self):
        result = get_cent_result(440, 880)
        assert result.cents == 1200
        assert result.semitones == 12
        assert result.octaves == 1
        assert result.ratio == 2
    
    def test_ratio_to_cents(self):
        assert frequency_ratio_to_cents(2) == 1200.0
        # Perfect fifth (3/2)
        assert round(frequency_ratio_to_cents(1.5), 2) == 701.96
    
    def test_cents_to_ratio(self):
        assert cents_to_ratio(1200) == 2.0
        assert round(cents_to_ratio(700), 4) == 1.4983
    
    def test_invalid_cents_frequency(self):
        with pytest.raises(ValueError):
            calculate_cents(0, 440)
        with pytest.raises(ValueError):
            calculate_cents(440, 0)


class TestRadioSpectrum:
    """无线电频谱测试"""
    
    def test_vhf_band(self):
        band = get_radio_band(100e6)
        assert band[0] == 'VHF'
    
    def test_uhf_band(self):
        band = get_radio_band(2.4e9)
        assert band[0] == 'UHF'
    
    def test_hf_band(self):
        band = get_radio_band(10e6)
        assert band[0] == 'HF'
    
    def test_mf_band(self):
        band = get_radio_band(1e6)
        assert band[0] == 'MF'
    
    def test_lf_band(self):
        band = get_radio_band(100e3)
        assert band[0] == 'LF'
    
    def test_shf_band(self):
        band = get_radio_band(10e9)
        assert band[0] == 'SHF'
    
    def test_ehf_band(self):
        band = get_radio_band(100e9)
        assert band[0] == 'EHF'
    
    def test_get_band_frequencies(self):
        min_f, max_f, name = get_band_frequencies('VHF')
        assert min_f == 30e6
        assert max_f == 300e6
        assert name == 'Very High Frequency'
    
    def test_invalid_band(self):
        with pytest.raises(ValueError):
            get_band_frequencies('INVALID')
    
    def test_list_radio_bands(self):
        bands = list_radio_bands()
        assert len(bands) == 12
        assert bands[0][0] == 'ELF'


class TestUtilityFunctions:
    """工具函数测试"""
    
    def test_is_audio_frequency(self):
        assert is_audio_frequency(440) == True
        assert is_audio_frequency(20) == True
        assert is_audio_frequency(20000) == True
        assert is_audio_frequency(10) == False
        assert is_audio_frequency(50000) == False
    
    def test_is_radio_frequency(self):
        assert is_radio_frequency(100e6) == True
        assert is_radio_frequency(3e3) == True
        assert is_radio_frequency(300e9) == True
        assert is_radio_frequency(2000) == False
        assert is_radio_frequency(500e9) == False
    
    def test_is_visible_light(self):
        assert is_visible_light(500e12) == True  # 500 THz
        assert is_visible_light(400e12) == True
        assert is_visible_light(800e12) == True
        assert is_visible_light(100e12) == False
        assert is_visible_light(1000e12) == False
    
    def test_format_frequency_khz(self):
        assert format_frequency(1000) == '1.00 kHz'
    
    def test_format_frequency_mhz(self):
        assert format_frequency(1e6) == '1.00 MHz'
    
    def test_format_frequency_ghz(self):
        assert format_frequency(1e9) == '1.00 GHz'
    
    def test_format_frequency_hz(self):
        assert format_frequency(100) == '100.00 Hz'
    
    def test_format_frequency_thz(self):
        assert format_frequency(1e12) == '1.00 THz'
    
    def test_format_frequency_precision(self):
        assert format_frequency(1234, 4) == '1.2340 kHz'
    
    def test_get_frequency_description_audio(self):
        desc = get_frequency_description(440)
        assert '音频' in desc or 'A' in desc
    
    def test_get_frequency_description_radio(self):
        desc = get_frequency_description(100e6)
        assert 'VHF' in desc


class TestScaleGeneration:
    """音阶生成测试"""
    
    def test_generate_chromatic_scale(self):
        scale = generate_chromatic_scale('C', 4, 12)
        assert len(scale) == 12
        assert scale[0][0] == 'C'
        assert scale[0][1] == 4
    
    def test_generate_chromatic_scale_octave(self):
        scale = generate_chromatic_scale('C', 4, 13)
        assert len(scale) == 13
        # Last note should be C5
        assert scale[-1][0] == 'C'
        assert scale[-1][1] == 5
    
    def test_generate_major_scale(self):
        scale = generate_major_scale('C', 4)
        assert len(scale) == 8
        notes = [n[0] for n in scale]
        assert notes == ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
    
    def test_major_scale_intervals(self):
        scale = generate_major_scale('C', 4)
        freqs = [n[2] for n in scale]
        # Check that intervals are correct
        # C-D should be a whole step (approximately)
        ratio_cd = freqs[1] / freqs[0]
        assert round(frequency_ratio_to_cents(ratio_cd)) == 200  # Whole step
        # C-E should be two whole steps
        ratio_ce = freqs[2] / freqs[0]
        assert round(frequency_ratio_to_cents(ratio_ce)) == 400


class TestEdgeCases:
    """边缘情况测试"""
    
    def test_zero_frequency(self):
        with pytest.raises(ValueError):
            frequency_to_period(0)
        with pytest.raises(ValueError):
            frequency_to_wavelength(0)
        with pytest.raises(ValueError):
            frequency_to_note(0)
    
    def test_negative_frequency(self):
        with pytest.raises(ValueError):
            frequency_to_period(-100)
    
    def test_very_high_frequency(self):
        freq = 1e15
        wl = frequency_to_wavelength(freq)
        assert wl < 1e-6  # Very short wavelength
    
    def test_very_low_frequency(self):
        freq = 0.001
        period = frequency_to_period(freq)
        assert period == 1000  # 1000 seconds
    
    def test_format_very_low_frequency(self):
        formatted = format_frequency(0.001)
        assert 'mHz' in formatted
    
    def test_format_very_high_frequency(self):
        formatted = format_frequency(1e15)
        assert 'PHz' not in formatted  # Should show THz or higher


if __name__ == '__main__':
    pytest.main([__file__, '-v'])