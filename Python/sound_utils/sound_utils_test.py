"""
Sound Utilities 测试模块

测试所有声音与音频工具功能。
"""

import unittest
import math
from mod import (
    # 频率转换
    frequency_to_note, note_to_frequency, midi_to_frequency, frequency_to_midi,
    # 波长计算
    speed_of_sound_to_wavelength, wavelength_to_frequency, speed_of_sound_temperature,
    # 分贝计算
    power_ratio_to_decibels, decibels_to_power_ratio,
    amplitude_ratio_to_decibels, decibels_to_amplitude_ratio,
    sound_pressure_to_spl, spl_to_sound_pressure, combine_decibels,
    # BPM 计算
    bpm_to_beat_duration_ms, beat_duration_to_bpm, bpm_to_note_duration,
    bpm_to_measure_duration, calculate_delay_time_ms,
    # 音频采样
    calculate_audio_file_size, calculate_audio_duration, calculate_bit_rate,
    get_audio_info, samples_to_milliseconds, milliseconds_to_samples,
    # 泛音
    generate_harmonics, generate_overtones_series,
    # 音程和弦
    calculate_interval, generate_chord_frequencies, get_scale_notes,
    transpose_frequency, cents_to_frequency_ratio, frequency_ratio_to_cents,
    # 常量和类
    MusicalNote, AudioFileInfo, A4_FREQUENCY, SPEED_OF_SOUND_AIR,
    NOTE_ALIASES, INTERVAL_NAMES, CHORD_FORMULAS,
    COMMON_FREQUENCIES, SAMPLE_RATES, BIT_DEPTHS, SPL_REFERENCE,
)


class TestFrequencyConversion(unittest.TestCase):
    """频率与音符转换测试"""
    
    def test_frequency_to_note_a4(self):
        """测试 A4 频率转换"""
        note = frequency_to_note(440.0)
        self.assertEqual(note.name, "A")
        self.assertEqual(note.octave, 4)
        self.assertEqual(note.midi_note, 69)
        self.assertEqual(note.cents_deviation, 0.0)
    
    def test_frequency_to_note_c4(self):
        """测试中央 C 转换"""
        note = frequency_to_note(261.63)
        self.assertEqual(note.name, "C")
        self.assertEqual(note.octave, 4)
        self.assertEqual(note.midi_note, 60)
    
    def test_frequency_to_note_with_deviation(self):
        """测试有偏差的频率"""
        # 450 Hz 比 A4 (440) 高约 39 音分
        note = frequency_to_note(450.0)
        self.assertEqual(note.name, "A")
        self.assertAlmostEqual(note.cents_deviation, 38.9, places=1)
    
    def test_note_to_frequency_a4(self):
        """测试 A4 频率计算"""
        freq = note_to_frequency("A", 4)
        self.assertEqual(freq, 440.0)
    
    def test_note_to_frequency_c4(self):
        """测试中央 C 频率计算"""
        freq = note_to_frequency("C", 4)
        self.assertAlmostEqual(freq, 261.626, places=2)
    
    def test_note_to_frequency_with_flat_names(self):
        """测试降号音符名称"""
        # Db 应该等于 C#
        freq_db = note_to_frequency("Db", 4)
        freq_csharp = note_to_frequency("C#", 4)
        self.assertEqual(freq_db, freq_csharp)
    
    def test_midi_to_frequency(self):
        """测试 MIDI 音符号转换"""
        self.assertEqual(midi_to_frequency(69), 440.0)  # A4
        self.assertAlmostEqual(midi_to_frequency(60), 261.626, places=2)  # C4
    
    def test_frequency_to_midi(self):
        """测试频率到 MIDI 转换"""
        self.assertEqual(frequency_to_midi(440.0), 69)
        self.assertEqual(frequency_to_midi(261.63), 60)
    
    def test_invalid_frequency(self):
        """测试无效频率"""
        with self.assertRaises(ValueError):
            frequency_to_note(0)
        with self.assertRaises(ValueError):
            frequency_to_note(-100)
    
    def test_invalid_note_name(self):
        """测试无效音符名称"""
        with self.assertRaises(ValueError):
            note_to_frequency("X", 4)
    
    def test_midi_range_limits(self):
        """测试 MIDI 范围限制"""
        # 最低 MIDI
        freq = midi_to_frequency(0)
        self.assertAlmostEqual(freq, 8.176, places=2)
        # 最高 MIDI
        freq = midi_to_frequency(127)
        self.assertAlmostEqual(freq, 12543.85, places=1)


class TestWavelengthCalculation(unittest.TestCase):
    """波长计算测试"""
    
    def test_speed_of_sound_to_wavelength(self):
        """测试波长计算"""
        wavelength = speed_of_sound_to_wavelength(343, 440)
        self.assertAlmostEqual(wavelength, 0.7795, places=3)
    
    def test_wavelength_to_frequency(self):
        """测试频率计算"""
        freq = wavelength_to_frequency(343, 0.78)
        self.assertAlmostEqual(freq, 439.74, places=1)
    
    def test_speed_of_sound_temperature(self):
        """测试温度对声速的影响"""
        # 20°C
        speed_20 = speed_of_sound_temperature(20)
        self.assertAlmostEqual(speed_20, 343.42, places=1)
        # 0°C
        speed_0 = speed_of_sound_temperature(0)
        self.assertAlmostEqual(speed_0, 331.3, places=1)
    
    def test_invalid_wavelength(self):
        """测试无效波长"""
        with self.assertRaises(ValueError):
            speed_of_sound_to_wavelength(343, 0)
        with self.assertRaises(ValueError):
            wavelength_to_frequency(343, 0)


class TestDecibelCalculation(unittest.TestCase):
    """分贝计算测试"""
    
    def test_power_ratio_to_decibels(self):
        """测试功率比分贝转换"""
        # 10x 功率 = 10 dB
        self.assertEqual(power_ratio_to_decibels(10), 10.0)
        # 2x 功率 ≈ 3 dB
        self.assertAlmostEqual(power_ratio_to_decibels(2), 3.01, places=2)
    
    def test_decibels_to_power_ratio(self):
        """测试分贝到功率比转换"""
        self.assertEqual(decibels_to_power_ratio(10), 10.0)
        self.assertAlmostEqual(decibels_to_power_ratio(3), 2.0, places=2)
    
    def test_amplitude_ratio_to_decibels(self):
        """测试振幅比分贝转换"""
        # 10x 振幅 = 20 dB
        self.assertEqual(amplitude_ratio_to_decibels(10), 20.0)
        # 2x 振幅 ≈ 6 dB
        self.assertAlmostEqual(amplitude_ratio_to_decibels(2), 6.02, places=2)
    
    def test_decibels_to_amplitude_ratio(self):
        """测试分贝到振幅比转换"""
        self.assertEqual(decibels_to_amplitude_ratio(20), 10.0)
        self.assertAlmostEqual(decibels_to_amplitude_ratio(6), 2.0, places=2)
    
    def test_sound_pressure_to_spl(self):
        """测试声压级转换"""
        # 参考声压 = 0 dB
        self.assertEqual(sound_pressure_to_spl(20e-6), 0.0)
        # 1 Pa ≈ 94 dB
        self.assertAlmostEqual(sound_pressure_to_spl(1), 94.0, places=1)
    
    def test_spl_to_sound_pressure(self):
        """测试声压转换"""
        # 0 dB = 参考声压
        self.assertEqual(spl_to_sound_pressure(0), 20e-6)
        # 94 dB ≈ 1 Pa
        self.assertAlmostEqual(spl_to_sound_pressure(94), 1.0, places=2)
    
    def test_combine_decibels(self):
        """测试分贝合并"""
        # 两个相同声源叠加增加约 3 dB
        combined = combine_decibels([60, 60])
        self.assertAlmostEqual(combined, 63.01, places=2)
        # 三个声源叠加增加约 4.8 dB
        combined = combine_decibels([60, 60, 60])
        self.assertAlmostEqual(combined, 64.77, places=2)
    
    def test_invalid_power_ratio(self):
        """测试无效功率比"""
        with self.assertRaises(ValueError):
            power_ratio_to_decibels(0)
        with self.assertRaises(ValueError):
            power_ratio_to_decibels(-1)


class TestBPMCalculation(unittest.TestCase):
    """BPM 与时间计算测试"""
    
    def test_bpm_to_beat_duration_ms(self):
        """测试 BPM 到拍时长转换"""
        self.assertEqual(bpm_to_beat_duration_ms(120), 500.0)
        self.assertEqual(bpm_to_beat_duration_ms(60), 1000.0)
    
    def test_beat_duration_to_bpm(self):
        """测试拍时长到 BPM 转换"""
        self.assertEqual(beat_duration_to_bpm(500), 120.0)
        self.assertEqual(beat_duration_to_bpm(1000), 60.0)
    
    def test_bpm_to_note_duration(self):
        """测试音符时长计算"""
        # 四分音符
        self.assertEqual(bpm_to_note_duration(120, "quarter"), 500.0)
        # 八分音符
        self.assertEqual(bpm_to_note_duration(120, "eighth"), 250.0)
        # 二分音符
        self.assertEqual(bpm_to_note_duration(120, "half"), 1000.0)
        # 全音符
        self.assertEqual(bpm_to_note_duration(120, "whole"), 2000.0)
    
    def test_bpm_to_note_duration_chinese(self):
        """测试中文音符名称"""
        self.assertEqual(bpm_to_note_duration(120, "四分"), 500.0)
        self.assertEqual(bpm_to_note_duration(120, "八分"), 250.0)
    
    def test_bpm_to_measure_duration(self):
        """测试小节时长计算"""
        # 4/4 拍
        self.assertEqual(bpm_to_measure_duration(120, "4/4"), 2000.0)
        # 3/4 拍
        self.assertEqual(bpm_to_measure_duration(120, "3/4"), 1500.0)
        # 6/8 拍
        self.assertEqual(bpm_to_measure_duration(120, "6/8"), 1500.0)
    
    def test_calculate_delay_time_ms(self):
        """测试延迟时间计算"""
        # 四分音符延迟
        self.assertEqual(calculate_delay_time_ms(120, "quarter"), 500.0)
        # 八分音符延迟
        self.assertEqual(calculate_delay_time_ms(120, "eighth"), 250.0)
        # 附点八分音符延迟
        self.assertEqual(calculate_delay_time_ms(120, "dotted_eighth"), 375.0)
    
    def test_invalid_bpm(self):
        """测试无效 BPM"""
        with self.assertRaises(ValueError):
            bpm_to_beat_duration_ms(0)
        with self.assertRaises(ValueError):
            bpm_to_beat_duration_ms(-120)
    
    def test_invalid_time_signature(self):
        """测试无效拍号"""
        with self.assertRaises(ValueError):
            bpm_to_measure_duration(120, "invalid")


class TestAudioSampling(unittest.TestCase):
    """音频采样计算测试"""
    
    def test_calculate_audio_file_size(self):
        """测试文件大小计算"""
        # CD 质量 1 分钟
        size = calculate_audio_file_size(60, 44100, 16, 2)
        self.assertEqual(size, 10584000)  # 约 10 MB
        
        # 48kHz 24bit 立体声 1 分钟
        size = calculate_audio_file_size(60, 48000, 24, 2)
        self.assertEqual(size, 17280000)  # 约 17 MB
    
    def test_calculate_audio_duration(self):
        """测试时长计算"""
        duration = calculate_audio_duration(10584000, 44100, 16, 2)
        self.assertEqual(duration, 60.0)
    
    def test_calculate_bit_rate(self):
        """测试比特率计算"""
        # CD 质量
        bitrate = calculate_bit_rate(44100, 16, 2)
        self.assertEqual(bitrate, 1411200)
        
        # 专业音频
        bitrate = calculate_bit_rate(48000, 24, 2)
        self.assertEqual(bitrate, 2304000)
    
    def test_get_audio_info(self):
        """测试获取音频信息"""
        info = get_audio_info(60, 44100, 16, 2)
        self.assertEqual(info.sample_rate, 44100)
        self.assertEqual(info.bit_depth, 16)
        self.assertEqual(info.channels, 2)
        self.assertEqual(info.duration_seconds, 60)
        self.assertEqual(info.file_size_bytes, 10584000)
        self.assertEqual(info.bit_rate, 1411200)
    
    def test_samples_to_milliseconds(self):
        """测试采样到毫秒转换"""
        ms = samples_to_milliseconds(44100, 44100)
        self.assertEqual(ms, 1000.0)
        
        ms = samples_to_milliseconds(512, 44100)
        self.assertAlmostEqual(ms, 11.61, places=2)
    
    def test_milliseconds_to_samples(self):
        """测试毫秒到采样转换"""
        samples = milliseconds_to_samples(1000, 44100)
        self.assertEqual(samples, 44100)
        
        samples = milliseconds_to_samples(500, 48000)
        self.assertEqual(samples, 24000)


class TestHarmonics(unittest.TestCase):
    """泛音系列测试"""
    
    def test_generate_harmonics(self):
        """测试泛音生成"""
        harmonics = generate_harmonics(440, 5)
        
        self.assertEqual(len(harmonics), 5)
        self.assertEqual(harmonics[0][0], 1)  # 第1次泛音
        self.assertEqual(harmonics[0][1], 440.0)  # 基频
        
        # 第2次泛音是八度
        self.assertEqual(harmonics[1][1], 880.0)
    
    def test_generate_harmonics_note_names(self):
        """测试泛音音符名称"""
        harmonics = generate_harmonics(440, 10)
        
        # 第1次泛音是 A4
        self.assertEqual(harmonics[0][2], "A4")
        # 第2次泛音是 A5
        self.assertEqual(harmonics[1][2], "A5")
    
    def test_generate_overtones_series_harmonic(self):
        """测试谐波系列"""
        series = generate_overtones_series(100, "harmonic")
        self.assertEqual(series[:5], [100.0, 200.0, 300.0, 400.0, 500.0])
    
    def test_generate_overtones_series_odd(self):
        """测试奇次谐波"""
        series = generate_overtones_series(100, "odd")
        self.assertEqual(series[:5], [100.0, 300.0, 500.0, 700.0, 900.0])
    
    def test_generate_overtones_series_even(self):
        """测试偶次谐波"""
        series = generate_overtones_series(100, "even")
        self.assertEqual(series[:5], [200.0, 400.0, 600.0, 800.0, 1000.0])
    
    def test_invalid_harmonic_input(self):
        """测试无效泛音输入"""
        with self.assertRaises(ValueError):
            generate_harmonics(0, 5)
        with self.assertRaises(ValueError):
            generate_overtones_series(0, "harmonic")


class TestIntervalsAndChords(unittest.TestCase):
    """音程与和弦测试"""
    
    def test_calculate_interval(self):
        """测试音程计算"""
        # C4 到 E4 = 大三度
        semitones, name, ratio = calculate_interval(261.63, 329.63)
        self.assertEqual(semitones, 4)
        self.assertIn("大三度", name)
        
        # C4 到 C5 = 纯八度
        semitones, name, ratio = calculate_interval(261.63, 523.25)
        # 由于归一化到八度内，纯八度会显示为纯一度
        self.assertEqual(semitones % 12, 0)
    
    def test_generate_chord_frequencies_major(self):
        """测试大三和弦"""
        chord = generate_chord_frequencies("C", 4, "major")
        
        self.assertIn("C4", chord)
        self.assertIn("E4", chord)
        self.assertIn("G4", chord)
        
        self.assertEqual(len(chord), 3)
    
    def test_generate_chord_frequencies_minor(self):
        """测试小三和弦"""
        chord = generate_chord_frequencies("A", 4, "minor")
        
        self.assertIn("A4", chord)
        self.assertIn("C5", chord)  # 小三度 = 大六度转位
        self.assertIn("E5", chord)
    
    def test_generate_chord_frequencies_sevenths(self):
        """测试七和弦"""
        chord = generate_chord_frequencies("C", 4, "major7")
        self.assertEqual(len(chord), 4)
        
        chord = generate_chord_frequencies("G", 4, "dominant7")
        self.assertEqual(len(chord), 4)
    
    def test_generate_chord_frequencies_power(self):
        """测试强力和弦"""
        chord = generate_chord_frequencies("E", 4, "power")
        
        self.assertIn("E4", chord)
        self.assertIn("B4", chord)  # 纯五度
        self.assertEqual(len(chord), 2)
    
    def test_invalid_chord_type(self):
        """测试无效和弦类型"""
        with self.assertRaises(ValueError):
            generate_chord_frequencies("C", 4, "unknown")
    
    def test_get_scale_notes_major(self):
        """测试大调音阶"""
        scale = get_scale_notes("C", "major")
        self.assertEqual(scale, ["C", "D", "E", "F", "G", "A", "B"])
    
    def test_get_scale_notes_minor(self):
        """测试小调音阶"""
        scale = get_scale_notes("A", "minor")
        self.assertEqual(scale, ["A", "B", "C", "D", "E", "F", "G"])
    
    def test_get_scale_notes_pentatonic(self):
        """测试五声音阶"""
        scale = get_scale_notes("C", "pentatonic_major")
        self.assertEqual(len(scale), 5)
    
    def test_get_scale_notes_blues(self):
        """测试蓝调音阶"""
        scale = get_scale_notes("A", "blues")
        self.assertEqual(len(scale), 6)
    
    def test_get_scale_notes_chinese(self):
        """测试中文音阶名称"""
        scale = get_scale_notes("C", "大调")
        self.assertEqual(scale, ["C", "D", "E", "F", "G", "A", "B"])


class TestTransposition(unittest.TestCase):
    """移调测试"""
    
    def test_transpose_frequency_octave_up(self):
        """测试升高八度"""
        freq = transpose_frequency(440.0, 12)
        self.assertAlmostEqual(freq, 880.0, places=2)
    
    def test_transpose_frequency_octave_down(self):
        """测试降低八度"""
        freq = transpose_frequency(440.0, -12)
        self.assertAlmostEqual(freq, 220.0, places=2)
    
    def test_transpose_frequency_fifth(self):
        """测试纯五度"""
        freq = transpose_frequency(440.0, 7)
        self.assertAlmostEqual(freq, 659.255, places=2)
    
    def test_cents_to_frequency_ratio(self):
        """测试音分到频率比"""
        # 1200 音分 = 一个八度
        ratio = cents_to_frequency_ratio(1200)
        self.assertEqual(ratio, 2.0)
        
        # 100 音分 = 一个半音
        ratio = cents_to_frequency_ratio(100)
        self.assertAlmostEqual(ratio, 1.0595, places=3)
    
    def test_frequency_ratio_to_cents(self):
        """测试频率比到音分"""
        # 一个八度 = 1200 音分
        cents = frequency_ratio_to_cents(2.0)
        self.assertEqual(cents, 1200.0)
        
        # 纯五度 ≈ 702 音分
        cents = frequency_ratio_to_cents(1.5)
        self.assertAlmostEqual(cents, 702.0, places=1)


class TestConstants(unittest.TestCase):
    """常量测试"""
    
    def test_common_frequencies(self):
        """测试常见频率"""
        self.assertEqual(COMMON_FREQUENCIES["A4"], 440.0)
        self.assertEqual(COMMON_FREQUENCIES["C4"], 261.63)
    
    def test_sample_rates(self):
        """测试采样率"""
        self.assertEqual(SAMPLE_RATES["cd_quality"], 44100)
        self.assertEqual(SAMPLE_RATES["studio_quality"], 96000)
    
    def test_bit_depths(self):
        """测试位深度"""
        self.assertEqual(BIT_DEPTHS["16bit"], 16)
        self.assertEqual(BIT_DEPTHS["24bit"], 24)
    
    def test_spl_reference(self):
        """测试声压级参考"""
        self.assertEqual(SPL_REFERENCE["threshold_of_hearing"], 0.0)
        self.assertEqual(SPL_REFERENCE["normal_conversation"], 60.0)
        self.assertEqual(SPL_REFERENCE["threshold_of_pain"], 130.0)


class TestMusicalNoteDataClass(unittest.TestCase):
    """MusicalNote 数据类测试"""
    
    def test_musical_note_creation(self):
        """测试音符对象创建"""
        note = MusicalNote(
            name="A",
            octave=4,
            frequency=440.0,
            midi_note=69,
            wavelength=0.7795
        )
        
        self.assertEqual(note.name, "A")
        self.assertEqual(note.octave, 4)
        self.assertEqual(note.frequency, 440.0)
        self.assertEqual(note.midi_note, 69)
    
    def test_musical_note_from_frequency(self):
        """测试从频率创建音符对象"""
        note = frequency_to_note(440.0)
        
        self.assertIsInstance(note, MusicalNote)
        self.assertEqual(note.name, "A")


class TestAudioFileInfoDataClass(unittest.TestCase):
    """AudioFileInfo 数据类测试"""
    
    def test_audio_file_info_creation(self):
        """测试音频信息对象创建"""
        info = get_audio_info(60, 44100, 16, 2)
        
        self.assertIsInstance(info, AudioFileInfo)
        self.assertEqual(info.duration_seconds, 60)
        self.assertEqual(info.bit_rate, 1411200)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_extreme_midi_values(self):
        """测试极端 MIDI 值"""
        # 最低 MIDI 音符号
        freq = midi_to_frequency(0)
        self.assertTrue(freq > 0)
        
        # 最高 MIDI 音符号
        freq = midi_to_frequency(127)
        self.assertTrue(freq > 0)
    
    def test_frequency_to_midi_edge_cases(self):
        """测试频率到 MIDI 边界"""
        # 超低频率（会被限制到 0）
        midi = frequency_to_midi(1.0)  # Very low frequency
        self.assertTrue(midi >= 0)
        
        # 超高频率（会被限制到 127）
        midi = frequency_to_midi(25000.0)  # Very high frequency
        self.assertTrue(midi <= 127)
    
    def test_combine_decibels_empty_list(self):
        """测试空分贝列表"""
        result = combine_decibels([])
        self.assertEqual(result, 0.0)
    
    def test_combine_decibels_single_value(self):
        """测试单个分贝值"""
        result = combine_decibels([60])
        self.assertEqual(result, 60.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)