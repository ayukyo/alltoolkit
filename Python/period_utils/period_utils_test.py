#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Period Utilities Tests
===================================
Unit tests for period_utils module.

Run with: python -m pytest period_utils_test.py -v
Or: python period_utils_test.py
"""

import unittest
import sys
import math

# Import the module
from mod import (
    # Constants
    BPM_MIN, BPM_MAX, DEFAULT_SAMPLE_RATE, NOTE_FREQUENCIES, RHYTHM_PATTERNS,
    # Enums
    WaveType, TimeUnit,
    # Data classes
    PeriodConfig, BPMConfig,
    # Conversion functions
    bpm_to_ms, ms_to_bpm, hz_to_period_ms, period_ms_to_hz,
    frequency_to_note_name, note_name_to_frequency,
    samples_to_seconds, seconds_to_samples,
    # Wave generation
    generate_sine_wave, generate_square_wave, generate_sawtooth_wave,
    generate_triangle_wave, generate_pulse_wave, generate_wave,
    # Pattern functions
    generate_periodic_sequence, generate_heartbeat_pattern,
    generate_metronome_pattern, generate_lfo_pattern,
    generate_tremolo_pattern, generate_vibrato_pattern,
    # Rhythm functions
    generate_rhythm_pattern, analyze_rhythm_pattern, create_custom_pattern,
    # Utility functions
    calculate_harmonics, calculate_octave_equivalent, quantize_to_grid,
    calculate_swing_offset, format_time_ms, format_bpm, format_frequency,
    # Generator class
    PeriodGenerator,
)


class TestBPMConversion(unittest.TestCase):
    """Test BPM conversion functions"""
    
    def test_bpm_to_ms_basic(self):
        """Test basic BPM to milliseconds conversion"""
        self.assertAlmostEqual(bpm_to_ms(60), 1000.0, places=1)
        self.assertAlmostEqual(bpm_to_ms(120), 500.0, places=1)
        self.assertAlmostEqual(bpm_to_ms(90), 666.67, places=1)
    
    def test_ms_to_bpm_basic(self):
        """Test basic milliseconds to BPM conversion"""
        self.assertAlmostEqual(ms_to_bpm(1000), 60.0, places=1)
        self.assertAlmostEqual(ms_to_bpm(500), 120.0, places=1)
    
    def test_bpm_ms_roundtrip(self):
        """Test BPM to ms and back"""
        for bpm in [60, 90, 120, 140, 180]:
            ms = bpm_to_ms(bpm)
            result_bpm = ms_to_bpm(ms)
            self.assertAlmostEqual(result_bpm, bpm, places=1)
    
    def test_bpm_to_ms_invalid(self):
        """Test invalid BPM raises error"""
        with self.assertRaises(ValueError):
            bpm_to_ms(0)
        with self.assertRaises(ValueError):
            bpm_to_ms(-10)
    
    def test_ms_to_bpm_invalid(self):
        """Test invalid ms raises error"""
        with self.assertRaises(ValueError):
            ms_to_bpm(0)
        with self.assertRaises(ValueError):
            ms_to_bpm(-10)


class TestFrequencyConversion(unittest.TestCase):
    """Test frequency conversion functions"""
    
    def test_hz_to_period_ms(self):
        """Test Hz to period milliseconds conversion"""
        self.assertAlmostEqual(hz_to_period_ms(1), 1000.0, places=1)
        self.assertAlmostEqual(hz_to_period_ms(2), 500.0, places=1)
        self.assertAlmostEqual(hz_to_period_ms(10), 100.0, places=1)
    
    def test_period_ms_to_hz(self):
        """Test period milliseconds to Hz conversion"""
        self.assertAlmostEqual(period_ms_to_hz(1000), 1.0, places=1)
        self.assertAlmostEqual(period_ms_to_hz(500), 2.0, places=1)
    
    def test_hz_period_roundtrip(self):
        """Test Hz to period and back"""
        for hz in [1, 5, 10, 100, 440]:
            period = hz_to_period_ms(hz)
            result_hz = period_ms_to_hz(period)
            self.assertAlmostEqual(result_hz, hz, places=3)
    
    def test_note_name_to_frequency(self):
        """Test note name to frequency conversion"""
        self.assertAlmostEqual(note_name_to_frequency('A4'), 440.0, places=1)
        self.assertAlmostEqual(note_name_to_frequency('C4'), 261.63, places=1)
        self.assertAlmostEqual(note_name_to_frequency('a4'), 440.0, places=1)  # Case insensitive
    
    def test_note_name_invalid(self):
        """Test invalid note name raises error"""
        with self.assertRaises(ValueError):
            note_name_to_frequency('H4')  # No H note
    
    def test_frequency_to_note_name(self):
        """Test frequency to nearest note name conversion"""
        self.assertEqual(frequency_to_note_name(440), 'A4')
        self.assertEqual(frequency_to_note_name(261.63), 'C4')
        self.assertEqual(frequency_to_note_name(466), 'A#4')  # Close to A#4 (466.16)


class TestSampleConversion(unittest.TestCase):
    """Test sample conversion functions"""
    
    def test_samples_to_seconds(self):
        """Test samples to seconds conversion"""
        self.assertAlmostEqual(samples_to_seconds(44100, 44100), 1.0, places=5)
        self.assertAlmostEqual(samples_to_seconds(22050, 44100), 0.5, places=5)
        self.assertAlmostEqual(samples_to_seconds(88200, 44100), 2.0, places=5)
    
    def test_seconds_to_samples(self):
        """Test seconds to samples conversion"""
        self.assertEqual(seconds_to_samples(1.0, 44100), 44100)
        self.assertEqual(seconds_to_samples(0.5, 44100), 22050)
        self.assertEqual(seconds_to_samples(2.0, 44100), 88200)
    
    def test_samples_seconds_roundtrip(self):
        """Test samples to seconds and back"""
        for seconds in [0.1, 0.5, 1.0, 2.5]:
            samples = seconds_to_samples(seconds, 44100)
            result_seconds = samples_to_seconds(samples, 44100)
            self.assertAlmostEqual(result_seconds, seconds, places=3)


class TestWaveGeneration(unittest.TestCase):
    """Test wave generation functions"""
    
    def test_generate_sine_wave_basic(self):
        """Test basic sine wave generation"""
        wave = generate_sine_wave(44100, 440)
        self.assertEqual(len(wave), 44100)
        # Check amplitude range
        for sample in wave:
            self.assertGreaterEqual(sample, -1.0)
            self.assertLessEqual(sample, 1.0)
    
    def test_generate_sine_wave_amplitude(self):
        """Test sine wave amplitude control"""
        wave_half = generate_sine_wave(44100, 440, amplitude=0.5)
        self.assertTrue(all(-0.5 <= s <= 0.5 for s in wave_half))
        self.assertAlmostEqual(max(wave_half), 0.5, places=2)
    
    def test_generate_square_wave(self):
        """Test square wave generation"""
        wave = generate_square_wave(44100, 440)
        self.assertEqual(len(wave), 44100)
        # Square wave should only have values near 1 or -1
        for sample in wave:
            self.assertTrue(sample > 0.9 or sample < -0.9 or abs(sample) < 0.1)
    
    def test_generate_sawtooth_wave(self):
        """Test sawtooth wave generation"""
        wave = generate_sawtooth_wave(44100, 440)
        self.assertEqual(len(wave), 44100)
        # Check that values are in range
        self.assertTrue(all(-1 <= s <= 1 for s in wave))
    
    def test_generate_triangle_wave(self):
        """Test triangle wave generation"""
        wave = generate_triangle_wave(44100, 440)
        self.assertEqual(len(wave), 44100)
        self.assertTrue(all(-1 <= s <= 1 for s in wave))
    
    def test_generate_pulse_wave(self):
        """Test pulse wave generation"""
        wave = generate_pulse_wave(44100, 440, pulse_width=0.1)
        self.assertEqual(len(wave), 44100)
    
    def test_generate_wave_function(self):
        """Test generic wave generation function"""
        for wave_type in ['sine', 'square', 'triangle', 'sawtooth', 'pulse']:
            wave = generate_wave(wave_type, 44100, 440)
            self.assertEqual(len(wave), 44100, f"Failed for {wave_type}")
    
    def test_generate_wave_enum(self):
        """Test wave generation with enum type"""
        wave = generate_wave(WaveType.SINE, 44100, 440)
        self.assertEqual(len(wave), 44100)
    
    def test_generate_wave_invalid(self):
        """Test invalid wave type raises error"""
        with self.assertRaises(ValueError):
            generate_wave('invalid', 44100, 440)


class TestPatternGeneration(unittest.TestCase):
    """Test pattern generation functions"""
    
    def test_generate_periodic_sequence_basic(self):
        """Test basic periodic sequence generation"""
        pattern = [1, 0, 0.5, 0]
        result = generate_periodic_sequence(pattern, 3)
        expected = [1.0, 0.0, 0.5, 0.0] * 3
        self.assertEqual(result, expected)
    
    def test_generate_periodic_sequence_amplitude(self):
        """Test periodic sequence with amplitude"""
        pattern = [1, 0]
        result = generate_periodic_sequence(pattern, 2, amplitude=0.5)
        expected = [0.5, 0.0, 0.5, 0.0]
        self.assertEqual(result, expected)
    
    def test_generate_heartbeat_pattern(self):
        """Test heartbeat pattern generation"""
        pattern = generate_heartbeat_pattern(72, 5.0)
        self.assertEqual(len(pattern), 5 * 44100)
        # Should have some non-zero values (heartbeats)
        self.assertTrue(any(s > 0 for s in pattern))
    
    def test_generate_metronome_pattern(self):
        """Test metronome pattern generation"""
        pattern = generate_metronome_pattern(120, 5.0)
        self.assertEqual(len(pattern), 5 * 44100)
        # Should have some non-zero values (clicks)
        self.assertTrue(any(s > 0 for s in pattern))
    
    def test_generate_lfo_pattern(self):
        """Test LFO pattern generation"""
        lfo = generate_lfo_pattern(44100, 5.0)
        self.assertEqual(len(lfo), 44100)
        # LFO should be in range 0-1
        self.assertTrue(all(0 <= s <= 1 for s in lfo))
    
    def test_generate_tremolo_pattern(self):
        """Test tremolo pattern generation"""
        tremolo = generate_tremolo_pattern(44100, 5.0, depth=0.5)
        self.assertEqual(len(tremolo), 44100)
        # Tremolo should modulate volume
        self.assertTrue(all(0.5 <= s <= 1.0 for s in tremolo))
    
    def test_generate_vibrato_pattern(self):
        """Test vibrato pattern generation"""
        vibrato = generate_vibrato_pattern(44100, 6.0, semitones=1.0)
        self.assertEqual(len(vibrato), 44100)
        # Vibrato should oscillate around 0
        self.assertTrue(any(s > 0.5 for s in vibrato))
        self.assertTrue(any(s < -0.5 for s in vibrato))


class TestRhythmFunctions(unittest.TestCase):
    """Test rhythm functions"""
    
    def test_generate_rhythm_pattern_valid(self):
        """Test rhythm pattern generation with valid name"""
        pattern = generate_rhythm_pattern('straight_4', 120)
        self.assertIsInstance(pattern, list)
        self.assertTrue(len(pattern) > 0)
        for time_ms, strength in pattern:
            self.assertIsInstance(time_ms, float)
            self.assertIsInstance(strength, float)
    
    def test_generate_rhythm_pattern_invalid(self):
        """Test rhythm pattern with invalid name"""
        with self.assertRaises(ValueError):
            generate_rhythm_pattern('invalid_pattern', 120)
    
    def test_analyze_rhythm_pattern_basic(self):
        """Test basic rhythm analysis"""
        pattern = [1, 0, 1, 0]
        analysis = analyze_rhythm_pattern(pattern)
        self.assertEqual(analysis['total_steps'], 4)
        self.assertEqual(analysis['beat_count'], 2)
        self.assertEqual(analysis['rest_count'], 2)
        self.assertEqual(analysis['density'], 0.5)
    
    def test_analyze_rhythm_pattern_with_floats(self):
        """Test rhythm analysis with float values"""
        pattern = [1, 0, 0.5, 0]
        analysis = analyze_rhythm_pattern(pattern)
        self.assertEqual(analysis['beat_count'], 2)
        self.assertAlmostEqual(analysis['average_intensity'], 0.75, places=2)
    
    def test_create_custom_pattern(self):
        """Test custom pattern creation"""
        pattern = create_custom_pattern([0, 2, 4, 6], 8)
        expected = [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
        self.assertEqual(pattern, expected)
    
    def test_create_custom_pattern_with_strengths(self):
        """Test custom pattern with varying strengths"""
        pattern = create_custom_pattern([0, 4], 8, strengths=[1.0, 0.5])
        expected = [1.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0]
        self.assertEqual(pattern, expected)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_calculate_harmonics(self):
        """Test harmonic calculation"""
        harmonics = calculate_harmonics(440, 4)
        expected = [440.0, 880.0, 1320.0, 1760.0]
        self.assertEqual(harmonics, expected)
    
    def test_calculate_octave_equivalent(self):
        """Test octave equivalent calculation"""
        # A5 (880) to A4 (440)
        result = calculate_octave_equivalent(880, 4)
        self.assertAlmostEqual(result, 440.0, places=1)
        
        # A3 (220) to A4 (440)
        result = calculate_octave_equivalent(220, 4)
        self.assertAlmostEqual(result, 440.0, places=1)
    
    def test_quantize_to_grid_nearest(self):
        """Test quantization to nearest"""
        self.assertEqual(quantize_to_grid(523, 100), 500)
        self.assertEqual(quantize_to_grid(573, 100), 600)
    
    def test_quantize_to_grid_up(self):
        """Test quantization up"""
        self.assertEqual(quantize_to_grid(523, 100, 'up'), 600)
        self.assertEqual(quantize_to_grid(500, 100, 'up'), 500)
    
    def test_quantize_to_grid_down(self):
        """Test quantization down"""
        self.assertEqual(quantize_to_grid(523, 100, 'down'), 500)
        self.assertEqual(quantize_to_grid(600, 100, 'down'), 600)
    
    def test_calculate_swing_offset(self):
        """Test swing offset calculation"""
        # First eighth note - no offset
        offset = calculate_swing_offset(0, 0.6, 8)
        self.assertEqual(offset, 0.0)
        
        # Second eighth note - should have offset
        offset = calculate_swing_offset(1, 0.6, 8)
        self.assertAlmostEqual(offset, 0.1, places=3)  # 0.6 - 0.5
    
    def test_format_time_ms(self):
        """Test time formatting"""
        self.assertEqual(format_time_ms(500), '500.0ms')
        # Use a value that rounds cleanly
        self.assertEqual(format_time_ms(1235.0), '1.235s')
    
    def test_format_bpm(self):
        """Test BPM formatting"""
        self.assertEqual(format_bpm(120), '120 BPM')
        self.assertEqual(format_bpm(128.5), '128.5 BPM')
    
    def test_format_frequency(self):
        """Test frequency formatting"""
        self.assertEqual(format_frequency(440), '440.0 Hz')
        self.assertEqual(format_frequency(1500), '1.50 kHz')


class TestDataClasses(unittest.TestCase):
    """Test data classes"""
    
    def test_period_config(self):
        """Test PeriodConfig dataclass"""
        config = PeriodConfig(frequency_hz=440, amplitude=0.8)
        self.assertEqual(config.frequency_hz, 440)
        self.assertAlmostEqual(config.period_seconds, 1/440, places=5)
        self.assertEqual(config.amplitude, 0.8)
    
    def test_bpm_config(self):
        """Test BPMConfig dataclass"""
        config = BPMConfig(bpm=120)
        self.assertAlmostEqual(config.beat_duration_ms, 500.0, places=1)
        self.assertAlmostEqual(config.beat_duration_seconds, 0.5, places=3)
        self.assertAlmostEqual(config.quarter_note_ms, 500.0, places=1)
        self.assertAlmostEqual(config.eighth_note_ms, 250.0, places=1)
    
    def test_bpm_config_invalid(self):
        """Test BPMConfig with invalid BPM"""
        with self.assertRaises(ValueError):
            BPMConfig(bpm=10)  # Below minimum
        
        with self.assertRaises(ValueError):
            BPMConfig(bpm=400)  # Above maximum


class TestPeriodGenerator(unittest.TestCase):
    """Test PeriodGenerator class"""
    
    def test_generator_basic(self):
        """Test basic generator usage"""
        gen = PeriodGenerator()
        self.assertEqual(gen.num_samples, 0)
        self.assertEqual(gen.duration_seconds, 0.0)
    
    def test_generator_add_wave(self):
        """Test adding wave to generator"""
        gen = PeriodGenerator().add_wave('sine', 440, 1.0)
        self.assertEqual(gen.num_samples, 44100)
        self.assertAlmostEqual(gen.duration_seconds, 1.0, places=2)
    
    def test_generator_normalize(self):
        """Test generator normalization"""
        gen = PeriodGenerator().add_wave('sine', 440, 2.0, amplitude=1.0).normalize()
        samples = gen.get_samples()
        max_val = max(abs(s) for s in samples)
        self.assertAlmostEqual(max_val, 1.0, places=5)
    
    def test_generator_clear(self):
        """Test generator clear"""
        gen = PeriodGenerator().add_wave('sine', 440, 1.0).clear()
        self.assertEqual(gen.num_samples, 0)
    
    def test_generator_info(self):
        """Test generator info"""
        gen = PeriodGenerator().add_wave('sine', 440, 1.0)
        info = gen.info()
        self.assertEqual(info['sample_rate'], 44100)
        self.assertAlmostEqual(info['duration_seconds'], 1.0, places=2)


if __name__ == '__main__':
    unittest.main(verbosity=2)