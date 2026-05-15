"""
Tone Utilities 测试模块

全面测试 tone_utils 模块的所有功能。
"""

import math
import unittest
from mod import (
    note_to_frequency, frequency_to_note, midi_to_frequency, frequency_to_midi,
    note_to_midi, midi_to_note, generate_scale, generate_chord, identify_chord,
    cents_difference, frequency_ratio_to_cents, cents_to_frequency_ratio,
    transpose_note, get_interval, get_harmonics, get_enharmonic_equivalents,
    is_consonant_interval, get_circle_of_fifths, Tone,
    NOTE_NAMES, NOTE_NAMES_FLAT, SCALE_PATTERNS, CHORD_PATTERNS,
    STANDARD_PITCH, MIDI_MIN, MIDI_MAX
)


class TestNoteFrequencyConversion(unittest.TestCase):
    """测试音符与频率转换。"""
    
    def test_note_to_frequency_a4(self):
        """测试 A4 = 440Hz。"""
        self.assertAlmostEqual(note_to_frequency('A', 4), 440.0, places=2)
    
    def test_note_to_frequency_c4(self):
        """测试中央 C (C4)。"""
        self.assertAlmostEqual(note_to_frequency('C', 4), 261.63, places=2)
    
    def test_note_to_frequency_a4_octave(self):
        """测试 A5 应该是 880Hz。"""
        self.assertAlmostEqual(note_to_frequency('A', 5), 880.0, places=2)
    
    def test_note_to_frequency_sharp(self):
        """测试升号音符。"""
        # A#4 应该比 A4 高约 26.16Hz
        a4 = note_to_frequency('A', 4)
        asharp4 = note_to_frequency('A#', 4)
        self.assertGreater(asharp4, a4)
        self.assertAlmostEqual(asharp4, 466.16, places=2)
    
    def test_note_to_frequency_flat(self):
        """测试降号音符。"""
        # Bb4 应该等于 A#4
        self.assertAlmostEqual(note_to_frequency('Bb', 4), note_to_frequency('A#', 4), places=2)
    
    def test_frequency_to_note_a4(self):
        """测试 440Hz 应该识别为 A4。"""
        note, octave, midi = frequency_to_note(440.0)
        self.assertEqual(note, 'A')
        self.assertEqual(octave, 4)
        self.assertEqual(midi, 69)
    
    def test_frequency_to_note_c4(self):
        """测试中央 C 频率识别。"""
        note, octave, midi = frequency_to_note(261.63)
        self.assertEqual(note, 'C')
        self.assertEqual(octave, 4)
        self.assertEqual(midi, 60)
    
    def test_frequency_to_note_flat(self):
        """测试使用降号表示。"""
        note, octave, midi = frequency_to_note(466.16, prefer_flat=True)
        self.assertEqual(note, 'Bb')
    
    def test_note_frequency_roundtrip(self):
        """测试音符到频率再回到音符。"""
        for note in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
            freq = note_to_frequency(note, 4)
            result_note, result_octave, _ = frequency_to_note(freq)
            self.assertEqual(result_note, note)
            self.assertEqual(result_octave, 4)


class TestMIDIConversion(unittest.TestCase):
    """测试 MIDI 转换功能。"""
    
    def test_midi_to_frequency_a4(self):
        """测试 MIDI 69 = A4 = 440Hz。"""
        self.assertAlmostEqual(midi_to_frequency(69), 440.0, places=2)
    
    def test_midi_to_frequency_c4(self):
        """测试 MIDI 60 = C4。"""
        self.assertAlmostEqual(midi_to_frequency(60), 261.63, places=2)
    
    def test_midi_to_frequency_extremes(self):
        """测试 MIDI 范围边界。"""
        # 最低音
        self.assertGreater(midi_to_frequency(0), 0)
        # 最高音
        self.assertGreater(midi_to_frequency(127), midi_to_frequency(0))
    
    def test_frequency_to_midi_a4(self):
        """测试 440Hz 应该是 MIDI 69。"""
        self.assertEqual(frequency_to_midi(440.0), 69)
    
    def test_frequency_to_midi_c4(self):
        """测试 C4 应该是 MIDI 60。"""
        self.assertEqual(frequency_to_midi(261.63), 60)
    
    def test_midi_frequency_roundtrip(self):
        """测试 MIDI 到频率再回到 MIDI。"""
        for midi in range(21, 109):  # 钢琴键范围 A0-C8
            freq = midi_to_frequency(midi)
            result_midi = frequency_to_midi(freq)
            self.assertEqual(result_midi, midi)
    
    def test_note_to_midi(self):
        """测试音符到 MIDI 转换。"""
        self.assertEqual(note_to_midi('A', 4), 69)
        self.assertEqual(note_to_midi('C', 4), 60)
        self.assertEqual(note_to_midi('C', 0), 12)  # C0 = MIDI 12
    
    def test_midi_to_note(self):
        """测试 MIDI 到音符转换。"""
        note, octave = midi_to_note(69)
        self.assertEqual(note, 'A')
        self.assertEqual(octave, 4)
        
        note, octave = midi_to_note(60)
        self.assertEqual(note, 'C')
        self.assertEqual(octave, 4)
    
    def test_midi_to_note_flat(self):
        """测试 MIDI 到音符（降号）。"""
        note, octave = midi_to_note(70, prefer_flat=True)  # A#4 = Bb4
        self.assertEqual(note, 'Bb')
        self.assertEqual(octave, 4)


class TestScaleGeneration(unittest.TestCase):
    """测试音阶生成。"""
    
    def test_major_scale_c(self):
        """测试 C 大调音阶。"""
        scale = generate_scale('C', 'major', 4)
        self.assertEqual(len(scale), 7)
        
        # 检查音符名称
        notes = [note.replace('4', '') for note, _ in scale]
        self.assertEqual(notes, ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
    
    def test_major_scale_frequencies(self):
        """测试大调音阶频率关系。"""
        scale = generate_scale('C', 'major', 4)
        
        # 相邻音程检查
        for i in range(len(scale) - 1):
            freq1 = scale[i][1]
            freq2 = scale[i + 1][1]
            # 应该是大二度或小二度
            cents = cents_difference(freq1, freq2)
            self.assertIn(round(cents), [100, 200])  # 半音或全音
    
    def test_minor_scale_a(self):
        """测试 A 小调音阶。"""
        scale = generate_scale('A', 'minor', 4)
        self.assertEqual(len(scale), 7)
    
    def test_pentatonic_scale(self):
        """测试五声音阶。"""
        scale = generate_scale('C', 'pentatonic_major', 4)
        self.assertEqual(len(scale), 5)
    
    def test_blues_scale(self):
        """测试布鲁斯音阶。"""
        scale = generate_scale('A', 'blues', 4)
        self.assertEqual(len(scale), 6)
    
    def test_chromatic_scale(self):
        """测试半音阶。"""
        scale = generate_scale('C', 'chromatic', 4)
        self.assertEqual(len(scale), 12)
    
    def test_invalid_scale_type(self):
        """测试无效音阶类型。"""
        with self.assertRaises(ValueError):
            generate_scale('C', 'invalid_scale', 4)


class TestChordGeneration(unittest.TestCase):
    """测试和弦生成。"""
    
    def test_major_chord(self):
        """测试大三和弦。"""
        chord = generate_chord('C', 'major', 4)
        self.assertEqual(len(chord), 3)
        
        notes = [note.replace('4', '') for note, _ in chord]
        self.assertEqual(notes, ['C', 'E', 'G'])
    
    def test_minor_chord(self):
        """测试小三和弦。"""
        chord = generate_chord('A', 'minor', 4)
        self.assertEqual(len(chord), 3)
        
        # 移除八度数字后检查音符名称
        notes = [note.rstrip('45') for note, _ in chord]
        self.assertEqual(notes, ['A', 'C', 'E'])
    
    def test_diminished_chord(self):
        """测试减三和弦。"""
        chord = generate_chord('B', 'dim', 4)
        self.assertEqual(len(chord), 3)
    
    def test_seventh_chords(self):
        """测试七和弦。"""
        for chord_type in ['maj7', 'min7', 'dom7', 'dim7']:
            chord = generate_chord('C', chord_type, 4)
            self.assertEqual(len(chord), 4, f"{chord_type} should have 4 notes")
    
    def test_sus_chords(self):
        """测试挂留和弦。"""
        sus2 = generate_chord('D', 'sus2', 4)
        self.assertEqual(len(sus2), 3)
        
        sus4 = generate_chord('D', 'sus4', 4)
        self.assertEqual(len(sus4), 3)
    
    def test_invalid_chord_type(self):
        """测试无效和弦类型。"""
        with self.assertRaises(ValueError):
            generate_chord('C', 'invalid_chord', 4)


class TestChordIdentification(unittest.TestCase):
    """测试和弦识别。"""
    
    def test_identify_major_chord(self):
        """测试识别大三和弦。"""
        chords = identify_chord(['C', 'E', 'G'])
        self.assertTrue(len(chords) > 0)
        self.assertIn(('C', 'major'), chords)
    
    def test_identify_minor_chord(self):
        """测试识别小三和弦。"""
        chords = identify_chord(['A', 'C', 'E'])
        self.assertTrue(len(chords) > 0)
        self.assertIn(('A', 'minor'), chords)
    
    def test_identify_diminished_chord(self):
        """测试识别减三和弦。"""
        chords = identify_chord(['B', 'D', 'F'])
        self.assertTrue(len(chords) > 0)
    
    def test_identify_insufficient_notes(self):
        """测试音符不足的情况。"""
        chords = identify_chord(['C', 'E'])
        self.assertEqual(len(chords), 0)
    
    def test_identify_empty(self):
        """测试空列表。"""
        chords = identify_chord([])
        self.assertEqual(len(chords), 0)


class TestCentsAndIntervals(unittest.TestCase):
    """测试音分和音程计算。"""
    
    def test_cents_difference_octave(self):
        """测试八度的音分差。"""
        cents = cents_difference(440, 880)
        self.assertAlmostEqual(cents, 1200, places=2)
    
    def test_cents_difference_semitone(self):
        """测试半音的音分差。"""
        cents = cents_difference(440, 466.16)
        self.assertAlmostEqual(cents, 100, places=1)
    
    def test_cents_difference_negative(self):
        """测试反向音分差。"""
        cents = cents_difference(880, 440)
        self.assertAlmostEqual(cents, -1200, places=2)
    
    def test_frequency_ratio_to_cents_octave(self):
        """测试八度比例转音分。"""
        cents = frequency_ratio_to_cents(2)
        self.assertAlmostEqual(cents, 1200, places=2)
    
    def test_frequency_ratio_to_cents_fifth(self):
        """测试纯五度比例转音分。"""
        cents = frequency_ratio_to_cents(1.5)
        self.assertAlmostEqual(cents, 701.96, places=1)
    
    def test_cents_to_frequency_ratio_octave(self):
        """测试音分转八度比例。"""
        ratio = cents_to_frequency_ratio(1200)
        self.assertAlmostEqual(ratio, 2.0, places=2)
    
    def test_cents_roundtrip(self):
        """测试音分转换往返。"""
        for cents in [100, 200, 500, 701.96, 1200]:
            ratio = cents_to_frequency_ratio(cents)
            result_cents = frequency_ratio_to_cents(ratio)
            self.assertAlmostEqual(cents, result_cents, places=2)
    
    def test_get_interval_perfect_fifth(self):
        """测试纯五度音程。"""
        semitones, name = get_interval('C', 4, 'G', 4)
        self.assertEqual(semitones, 7)
        self.assertEqual(name, 'perfect_fifth')
    
    def test_get_interval_major_third(self):
        """测试大三度音程。"""
        semitones, name = get_interval('C', 4, 'E', 4)
        self.assertEqual(semitones, 4)
        self.assertEqual(name, 'major_third')
    
    def test_get_interval_octave(self):
        """测试八度音程。"""
        semitones, name = get_interval('C', 4, 'C', 5)
        self.assertEqual(semitones, 12)
        self.assertEqual(name, 'octave')


class TestTranspose(unittest.TestCase):
    """测试移调功能。"""
    
    def test_transpose_up(self):
        """测试向上移调。"""
        note, octave = transpose_note('C', 4, 2)
        self.assertEqual(note, 'D')
        self.assertEqual(octave, 4)
    
    def test_transpose_down(self):
        """测试向下移调。"""
        note, octave = transpose_note('D', 4, -2)
        self.assertEqual(note, 'C')
        self.assertEqual(octave, 4)
    
    def test_transpose_across_octave(self):
        """测试跨八度移调。"""
        note, octave = transpose_note('A', 4, 3)
        self.assertEqual(note, 'C')
        self.assertEqual(octave, 5)
    
    def test_transpose_octave(self):
        """测试八度移调。"""
        note, octave = transpose_note('C', 4, 12)
        self.assertEqual(note, 'C')
        self.assertEqual(octave, 5)


class TestHarmonics(unittest.TestCase):
    """测试泛音系列。"""
    
    def test_harmonics_count(self):
        """测试泛音数量。"""
        harmonics = get_harmonics(440, 8)
        self.assertEqual(len(harmonics), 8)
    
    def test_harmonics_fundamental(self):
        """测试基频。"""
        harmonics = get_harmonics(440, 5)
        self.assertEqual(harmonics[0][0], 1)  # 第一个泛音序号
        self.assertEqual(harmonics[0][1], 440)  # 频率
    
    def test_harmonics_octave(self):
        """测试第二泛音是八度。"""
        harmonics = get_harmonics(440, 8)
        self.assertEqual(harmonics[1][1], 880)  # 第二泛音是八度
    
    def test_harmonics_fifth(self):
        """测试第三泛音是纯五度。"""
        harmonics = get_harmonics(440, 8)
        # 第三泛音是 3 * 440 = 1320 Hz
        self.assertEqual(harmonics[2][1], 1320)
    
    def test_harmonics_invalid_frequency(self):
        """测试无效频率。"""
        with self.assertRaises(ValueError):
            get_harmonics(0, 8)
        with self.assertRaises(ValueError):
            get_harmonics(-100, 8)


class TestEnharmonicEquivalents(unittest.TestCase):
    """测试等音功能。"""
    
    def test_enharmonic_sharp(self):
        """测试升号等音。"""
        equivalents = get_enharmonic_equivalents('C#')
        self.assertIn('C#', equivalents)
        self.assertIn('Db', equivalents)
    
    def test_enharmonic_flat(self):
        """测试降号等音。"""
        equivalents = get_enharmonic_equivalents('Eb')
        self.assertIn('D#', equivalents)
        self.assertIn('Eb', equivalents)
    
    def test_enharmonic_natural(self):
        """测试自然音等音（自身）。"""
        equivalents = get_enharmonic_equivalents('D')
        self.assertEqual(len(equivalents), 2)
        self.assertEqual(equivalents[0], equivalents[1])  # D 的等音就是 D


class TestConsonance(unittest.TestCase):
    """测试协和度判断。"""
    
    def test_consonant_intervals(self):
        """测试协和音程。"""
        consonant = [0, 3, 4, 5, 7, 8, 9, 12]  # 纯一度、大小三度、纯四五度、大小六度、八度
        for interval in consonant:
            self.assertTrue(is_consonant_interval(interval), 
                          f"Interval {interval} should be consonant")
    
    def test_dissonant_intervals(self):
        """测试不协和音程。"""
        dissonant = [1, 2, 6, 10, 11]  # 大小二度、三全音、大小七度
        for interval in dissonant:
            self.assertFalse(is_consonant_interval(interval),
                           f"Interval {interval} should be dissonant")


class TestCircleOfFifths(unittest.TestCase):
    """测试五度圈。"""
    
    def test_circle_length(self):
        """测试五度圈长度。"""
        circle = get_circle_of_fifths()
        self.assertEqual(len(circle), 12)
    
    def test_circle_starts_with_c(self):
        """测试五度圈从 C 开始。"""
        circle = get_circle_of_fifths()
        self.assertEqual(circle[0][0], 'C')
    
    def test_circle_progression(self):
        """测试五度圈进程。"""
        circle = get_circle_of_fifths()
        for i in range(len(circle) - 1):
            # 相邻调应该是五度关系
            current = circle[i][0]
            next_key = circle[i + 1][0]
            
            current_midi = note_to_midi(current, 4)
            next_midi = note_to_midi(next_key, 4)
            
            interval = (next_midi - current_midi) % 12
            self.assertEqual(interval, 7, f"Expected fifth between {current} and {next_key}")
    
    def test_circle_relative_minor(self):
        """测试关系小调。"""
        circle = get_circle_of_fifths()
        
        # C 大调的关系小调是 A 小调
        self.assertEqual(circle[0][1], 'A')
        
        # G 大调的关系小调是 E 小调
        self.assertEqual(circle[1][1], 'E')


class TestToneClass(unittest.TestCase):
    """测试 Tone 类。"""
    
    def test_tone_creation(self):
        """测试创建音符。"""
        tone = Tone('A', 4)
        self.assertEqual(tone.note, 'A')
        self.assertEqual(tone.octave, 4)
    
    def test_tone_frequency(self):
        """测试音符频率。"""
        tone = Tone('A', 4)
        self.assertAlmostEqual(tone.frequency, 440.0, places=2)
    
    def test_tone_midi(self):
        """测试音符 MIDI。"""
        tone = Tone('A', 4)
        self.assertEqual(tone.midi_note, 69)
        
        tone_c = Tone('C', 4)
        self.assertEqual(tone_c.midi_note, 60)
    
    def test_tone_transpose(self):
        """测试音符移调。"""
        tone = Tone('C', 4)
        transposed = tone.transpose(2)
        self.assertEqual(transposed.note, 'D')
        self.assertEqual(transposed.octave, 4)
    
    def test_tone_transpose_octave(self):
        """测试跨八度移调。"""
        tone = Tone('A', 4)
        transposed = tone.transpose(3)
        self.assertEqual(transposed.note, 'C')
        self.assertEqual(transposed.octave, 5)
    
    def test_tone_comparison(self):
        """测试音符比较。"""
        tone_a = Tone('A', 4)
        tone_c = Tone('C', 4)
        tone_a_high = Tone('A', 5)
        
        self.assertTrue(tone_c < tone_a)
        self.assertTrue(tone_a < tone_a_high)
        self.assertEqual(tone_a, tone_a)
    
    def test_tone_subtraction(self):
        """测试音符相减（半音差）。"""
        tone_c = Tone('C', 4)
        tone_e = Tone('E', 4)
        tone_g = Tone('G', 4)
        
        self.assertEqual(tone_e - tone_c, 4)  # 大三度
        self.assertEqual(tone_g - tone_c, 7)  # 纯五度
    
    def test_tone_addition(self):
        """测试音符加法。"""
        tone_c = Tone('C', 4)
        tone_e = tone_c + 4  # 大三度
        
        self.assertEqual(tone_e.note, 'E')
        self.assertEqual(tone_e.octave, 4)
    
    def test_tone_interval(self):
        """测试音符间音程计算。"""
        tone_c = Tone('C', 4)
        tone_g = Tone('G', 4)
        
        semitones, name = tone_c.interval_to(tone_g)
        self.assertEqual(semitones, 7)
        self.assertEqual(name, 'perfect_fifth')
    
    def test_tone_repr(self):
        """测试音符字符串表示。"""
        tone = Tone('A', 4)
        repr_str = repr(tone)
        self.assertIn('A4', repr_str)
        self.assertIn('440', repr_str)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况。"""
    
    def test_invalid_note(self):
        """测试无效音符。"""
        with self.assertRaises(ValueError):
            note_to_frequency('H', 4)  # H 不是有效音符
    
    def test_invalid_frequency(self):
        """测试无效频率。"""
        with self.assertRaises(ValueError):
            frequency_to_note(0)
        with self.assertRaises(ValueError):
            frequency_to_note(-100)
    
    def test_midi_boundaries(self):
        """测试 MIDI 边界。"""
        # 有效边界
        self.assertEqual(midi_to_note(0)[0], 'C')
        self.assertEqual(midi_to_note(127)[0], 'G')
        
        # 无效边界
        with self.assertRaises(ValueError):
            midi_to_note(-1)
        with self.assertRaises(ValueError):
            midi_to_note(128)
    
    def test_very_low_frequency(self):
        """测试极低频率。"""
        note, octave, midi = frequency_to_note(20)  # 极低音
        self.assertEqual(octave, 0)  # C0 附近
    
    def test_very_high_frequency(self):
        """测试极高频率。"""
        note, octave, midi = frequency_to_note(10000)
        self.assertGreaterEqual(octave, 8)


if __name__ == '__main__':
    unittest.main(verbosity=2)