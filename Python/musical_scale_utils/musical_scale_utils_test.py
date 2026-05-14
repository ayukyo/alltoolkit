"""
Musical Scale Utils 测试套件

测试音乐音阶与和弦理论工具的所有功能
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Note, Scale, Chord,
    NoteName, ScaleType, ChordType, Interval,
    midi_to_note, midi_to_frequency, frequency_to_midi,
    generate_scale, generate_chord, get_interval, get_interval_name,
    get_interval_consonance, transpose_note, get_chord_tones,
    analyze_chord_quality, get_relative_keys, get_key_signature,
    get_scale_degrees, get_chord_progression_degrees,
    calculate_tempo, calculate_duration, get_beat_durations,
    analyze_rhythm_pattern, suggest_harmony_for_melody,
    compare_scales, get_all_modes_of_scale, invert_chord,
    get_chord_inversion_name, analyze_key_from_notes,
    generate_arpeggio, get_interval_matrix,
    create_chord_from_intervals, get_note_enharmonic,
    get_all_scale_types_info, get_all_chord_types_info,
    generate_circle_of_fifths,
    INTERVAL_SEMITONES, INTERVAL_NAMES_CN, INTERVAL_CONSONANCE,
    SCALE_INTERVALS, CHORD_INTERVALS,
)


class TestNote(unittest.TestCase):
    """测试音符类"""
    
    def test_note_creation(self):
        """测试音符创建"""
        note = Note('C', 4, '')
        self.assertEqual(note.name, 'C')
        self.assertEqual(note.octave, 4)
        self.assertEqual(note.accidental, '')
    
    def test_note_octave_clamping(self):
        """测试八度范围限制"""
        note = Note('C', -1, '')
        self.assertEqual(note.octave, 0)
        
        note = Note('C', 15, '')
        self.assertEqual(note.octave, 9)
    
    def test_note_full_name(self):
        """测试完整音符名称"""
        self.assertEqual(Note('C', 4, '').get_full_name(), 'C')
        self.assertEqual(Note('C', 4, '#').get_full_name(), 'C#')
        self.assertEqual(Note('D', 4, 'b').get_full_name(), 'Db')
    
    def test_midi_number(self):
        """测试 MIDI 音符编号"""
        # C4 = 60 (MIDI)
        self.assertEqual(Note('C', 4, '').get_midi_number(), 60)
        # A4 = 69 (MIDI)
        self.assertEqual(Note('A', 4, '').get_midi_number(), 69)
        # C0 = 12 (最低 MIDI C)
        self.assertEqual(Note('C', 0, '').get_midi_number(), 12)
    
    def test_frequency(self):
        """测试频率计算"""
        # A4 应该是 440Hz
        a4 = Note('A', 4, '')
        self.assertAlmostEqual(a4.get_frequency(), 440.0, places=1)
        
        # C4 应该约为 261.63Hz
        c4 = Note('C', 4, '')
        self.assertAlmostEqual(c4.get_frequency(), 261.63, places=1)
        
        # 使用不同的 A4 参考频率
        a4_442 = Note('A', 4, '').get_frequency(442.0)
        self.assertAlmostEqual(a4_442, 442.0, places=1)


class TestMidiConversion(unittest.TestCase):
    """测试 MIDI 转换"""
    
    def test_midi_to_note(self):
        """测试 MIDI 转 Note"""
        # C4 (MIDI 60)
        note = midi_to_note(60)
        self.assertEqual(note.name, 'C')
        self.assertEqual(note.octave, 4)
        
        # A4 (MIDI 69)
        note = midi_to_note(69)
        self.assertEqual(note.name, 'A')
        self.assertEqual(note.octave, 4)
        
        # C0 (MIDI 12)
        note = midi_to_note(12)
        self.assertEqual(note.name, 'C')
        self.assertEqual(note.octave, 0)
    
    def test_midi_to_frequency(self):
        """测试 MIDI 转频率"""
        # A4 = 440Hz
        self.assertAlmostEqual(midi_to_frequency(69), 440.0, places=1)
        
        # C4 ≈ 261.63Hz
        self.assertAlmostEqual(midi_to_frequency(60), 261.63, places=1)
    
    def test_frequency_to_midi(self):
        """测试频率转 MIDI"""
        # 440Hz -> A4 (MIDI 69)
        self.assertEqual(frequency_to_midi(440.0), 69)
        
        # 261.63Hz -> C4 (MIDI 60)
        self.assertEqual(frequency_to_midi(261.63), 60)
    
    def test_midi_boundary(self):
        """测试 MIDI 边界值"""
        # 超出范围的 MIDI 编号会被裁剪到 0-127
        note = midi_to_note(-1)
        self.assertEqual(note.get_midi_number(), 12)  # 最低有效 MIDI 音 C0
        
        note = midi_to_note(200)
        self.assertEqual(note.get_midi_number(), 127)


class TestScaleGeneration(unittest.TestCase):
    """测试音阶生成"""
    
    def test_major_scale(self):
        """测试大调音阶"""
        scale = generate_scale('C', ScaleType.MAJOR)
        self.assertEqual(scale.root, 'C')
        self.assertEqual(len(scale.notes), 7)
        
        # C 大调应该是 C D E F G A B
        expected = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        actual = [n.get_full_name() for n in scale.notes]
        self.assertEqual(actual, expected)
    
    def test_natural_minor_scale(self):
        """测试自然小调音阶"""
        scale = generate_scale('A', ScaleType.MINOR_NATURAL)
        self.assertEqual(len(scale.notes), 7)
        
        # A 小调应该是 A B C D E F G
        expected = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        actual = [n.get_full_name() for n in scale.notes]
        self.assertEqual(actual, expected)
    
    def test_harmonic_minor_scale(self):
        """测试和声小调音阶"""
        scale = generate_scale('A', ScaleType.MINOR_HARMONIC)
        self.assertEqual(len(scale.notes), 7)
        
        # A 和声小调: A B C D E F G#
        expected = ['A', 'B', 'C', 'D', 'E', 'F', 'G#']
        actual = [n.get_full_name() for n in scale.notes]
        self.assertEqual(actual, expected)
    
    def test_pentatonic_major(self):
        """测试大调五声音阶"""
        scale = generate_scale('C', ScaleType.PENTATONIC_MAJOR)
        self.assertEqual(len(scale.notes), 5)
        
        # C 大调五声: C D E G A
        expected = ['C', 'D', 'E', 'G', 'A']
        actual = [n.get_full_name() for n in scale.notes]
        self.assertEqual(actual, expected)
    
    def test_pentatonic_minor(self):
        """测试小调五声音阶"""
        scale = generate_scale('A', ScaleType.PENTATONIC_MINOR)
        self.assertEqual(len(scale.notes), 5)
        
        # A 小调五声: A C D E G
        expected = ['A', 'C', 'D', 'E', 'G']
        actual = [n.get_full_name() for n in scale.notes]
        self.assertEqual(actual, expected)
    
    def test_blues_scale(self):
        """测试蓝调音阶"""
        scale = generate_scale('A', ScaleType.PENTATONIC_BLUES)
        self.assertEqual(len(scale.notes), 6)
        
        # A 蓝调: A C D D# E G
        self.assertEqual(scale.notes[0].get_full_name(), 'A')
    
    def test_dorian_mode(self):
        """测试多利亚调式"""
        scale = generate_scale('D', ScaleType.DORIAN)
        self.assertEqual(len(scale.notes), 7)
        
        # D 多利亚: D E F G A B C
        expected = ['D', 'E', 'F', 'G', 'A', 'B', 'C']
        actual = [n.get_full_name() for n in scale.notes]
        self.assertEqual(actual, expected)
    
    def test_chromatic_scale(self):
        """测试半音阶"""
        scale = generate_scale('C', ScaleType.CHROMATIC)
        self.assertEqual(len(scale.notes), 12)
    
    def test_whole_tone_scale(self):
        """测试全音阶"""
        scale = generate_scale('C', ScaleType.WHOLE_TONE)
        self.assertEqual(len(scale.notes), 6)
    
    def test_g_major_scale(self):
        """测试 G 大调音阶"""
        scale = generate_scale('G', ScaleType.MAJOR)
        # G 大调: G A B C D E F#
        expected = ['G', 'A', 'B', 'C', 'D', 'E', 'F#']
        actual = [n.get_full_name() for n in scale.notes]
        self.assertEqual(actual, expected)
    
    def test_f_major_scale(self):
        """测试 F 大调音阶"""
        scale = generate_scale('F', ScaleType.MAJOR)
        # F 大调: F G A Bb C D E
        self.assertEqual(scale.notes[0].get_full_name(), 'F')


class TestChordGeneration(unittest.TestCase):
    """测试和弦生成"""
    
    def test_major_triad(self):
        """测试大三和弦"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        self.assertEqual(chord.root, 'C')
        self.assertEqual(len(chord.notes), 3)
        
        # C 大三和弦: C E G
        expected = ['C', 'E', 'G']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_minor_triad(self):
        """测试小三和弦"""
        chord = generate_chord('A', ChordType.MINOR_TRIAD)
        # Am: A C E
        expected = ['A', 'C', 'E']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_diminished_triad(self):
        """测试减三和弦"""
        chord = generate_chord('B', ChordType.DIMINISHED_TRIAD)
        # Bdim: B D F
        expected = ['B', 'D', 'F']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_augmented_triad(self):
        """测试增三和弦"""
        chord = generate_chord('C', ChordType.AUGMENTED_TRIAD)
        # Caug: C E G#
        expected = ['C', 'E', 'G#']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_major_7(self):
        """测试大七和弦"""
        chord = generate_chord('C', ChordType.MAJOR_7)
        # Cmaj7: C E G B
        expected = ['C', 'E', 'G', 'B']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_minor_7(self):
        """测试小七和弦"""
        chord = generate_chord('A', ChordType.MINOR_7)
        # Am7: A C E G
        expected = ['A', 'C', 'E', 'G']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_dominant_7(self):
        """测试属七和弦"""
        chord = generate_chord('G', ChordType.DOMINANT_7)
        # G7: G B D F
        expected = ['G', 'B', 'D', 'F']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_diminished_7(self):
        """测试减七和弦"""
        chord = generate_chord('C', ChordType.DIMINISHED_7)
        # Cdim7: C Eb Gb A (或 Bbb)
        self.assertEqual(len(chord.notes), 4)
    
    def test_sus2_chord(self):
        """测试挂二和弦"""
        chord = generate_chord('C', ChordType.SUS_2)
        # Csus2: C D G
        expected = ['C', 'D', 'G']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_sus4_chord(self):
        """测试挂四和弦"""
        chord = generate_chord('C', ChordType.SUS_4)
        # Csus4: C F G
        expected = ['C', 'F', 'G']
        actual = [n.get_full_name() for n in chord.notes]
        self.assertEqual(actual, expected)
    
    def test_add9_chord(self):
        """测试加九和弦"""
        chord = generate_chord('C', ChordType.ADD_9)
        # Cadd9: C E G D
        self.assertEqual(len(chord.notes), 4)


class TestInterval(unittest.TestCase):
    """测试音程"""
    
    def test_get_interval(self):
        """测试音程计算"""
        # C 到 E 是大三度
        c4 = Note('C', 4, '')
        e4 = Note('E', 4, '')
        interval = get_interval(c4, e4)
        self.assertEqual(interval, Interval.MAJOR_THIRD)
        
        # C 到 G 是纯五度
        g4 = Note('G', 4, '')
        interval = get_interval(c4, g4)
        self.assertEqual(interval, Interval.PERFECT_FIFTH)
        
        # C 到 C# 是小二度
        c_sharp = Note('C', 4, '#')
        interval = get_interval(c4, c_sharp)
        self.assertEqual(interval, Interval.MINOR_SECOND)
    
    def test_interval_name(self):
        """测试音程名称"""
        self.assertEqual(get_interval_name(Interval.MAJOR_THIRD), "大三度")
        self.assertEqual(get_interval_name(Interval.PERFECT_FIFTH), "纯五度")
        self.assertEqual(get_interval_name(Interval.MAJOR_THIRD, 'en'), "M3")
    
    def test_interval_consonance(self):
        """测试音程协和性"""
        self.assertEqual(get_interval_consonance(Interval.PERFECT_FIFTH), "完全协和")
        self.assertEqual(get_interval_consonance(Interval.MAJOR_THIRD), "不完全协和")
        self.assertEqual(get_interval_consonance(Interval.MINOR_SECOND), "极不协和")
    
    def test_interval_semitones(self):
        """测试音程半音数"""
        self.assertEqual(INTERVAL_SEMITONES[Interval.MAJOR_THIRD], 4)
        self.assertEqual(INTERVAL_SEMITONES[Interval.PERFECT_FIFTH], 7)
        self.assertEqual(INTERVAL_SEMITONES[Interval.MAJOR_SEVENTH], 11)


class TestTranspose(unittest.TestCase):
    """测试移调"""
    
    def test_transpose_up(self):
        """测试向上移调"""
        c4 = Note('C', 4, '')
        e4 = transpose_note(c4, 4)  # 大三度
        self.assertEqual(e4.get_full_name(), 'E')
    
    def test_transpose_down(self):
        """测试向下移调"""
        c4 = Note('C', 4, '')
        g3 = transpose_note(c4, -5)  # 下移纯四度
        self.assertEqual(g3.name, 'G')
        self.assertEqual(g3.octave, 3)
    
    def test_transpose_octave(self):
        """测试跨八度移调"""
        c4 = Note('C', 4, '')
        c5 = transpose_note(c4, 12)  # 上移一个八度
        self.assertEqual(c5.name, 'C')
        self.assertEqual(c5.octave, 5)


class TestChordAnalysis(unittest.TestCase):
    """测试和弦分析"""
    
    def test_chord_tones(self):
        """测试和弦音功能"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        tones = get_chord_tones(chord)
        
        self.assertEqual(tones['root'], 'C')
        self.assertEqual(tones['third'], 'E')
        self.assertEqual(tones['fifth'], 'G')
    
    def test_chord_quality(self):
        """测试和弦性质分析"""
        chord = generate_chord('C', ChordType.MAJOR_7)
        analysis = analyze_chord_quality(chord)
        
        self.assertEqual(analysis['symbol'], 'Cmaj7')
        self.assertEqual(analysis['notes'], ['C', 'E', 'G', 'B'])
        self.assertEqual(len(analysis['intervals_from_root']), 4)
    
    def test_chord_symbol(self):
        """测试和弦符号"""
        self.assertEqual(generate_chord('C', ChordType.MAJOR_TRIAD).get_symbol(), 'C')
        self.assertEqual(generate_chord('A', ChordType.MINOR_TRIAD).get_symbol(), 'Am')
        self.assertEqual(generate_chord('G', ChordType.DOMINANT_7).get_symbol(), 'G7')


class TestKeyRelations(unittest.TestCase):
    """测试调性关系"""
    
    def test_relative_keys_major(self):
        """测试大调近关系调"""
        relatives = get_relative_keys('C major')
        
        # C 大调的关系小调是 A minor
        self.assertIn('A minor', relatives['relative'])
        # 同主音小调是 C minor
        self.assertIn('C minor', relatives['parallel'])
    
    def test_relative_keys_minor(self):
        """测试小调近关系调"""
        relatives = get_relative_keys('A minor')
        
        # A 小调的关系大调是 C major
        self.assertIn('C major', relatives['relative'])
        # 同主音大调是 A major
        self.assertIn('A major', relatives['parallel'])
    
    def test_key_signature(self):
        """测试调号"""
        # C 大调没有升降记号
        sig = get_key_signature('C major')
        self.assertEqual(sig['accidentals'], 0)
        
        # G 大调有一个升号（F#）
        sig = get_key_signature('G major')
        self.assertEqual(sig['accidentals'], 1)
        self.assertEqual(sig['accidental_type'], 'sharps')
        
        # F 大调有一个降号（Bb）
        sig = get_key_signature('F major')
        self.assertEqual(sig['accidentals'], -1)
        self.assertEqual(sig['accidental_type'], 'flats')


class TestScaleDegrees(unittest.TestCase):
    """测试音阶级数"""
    
    def test_scale_degrees(self):
        """测试音阶级数"""
        scale = generate_scale('C', ScaleType.MAJOR)
        degrees = get_scale_degrees(scale)
        
        self.assertEqual(len(degrees), 7)
        self.assertEqual(degrees[0]['degree'], 'I')
        self.assertEqual(degrees[0]['note'], 'C')
        self.assertEqual(degrees[4]['degree'], 'V')
        self.assertEqual(degrees[4]['note'], 'G')
    
    def test_chord_progression_degrees(self):
        """测试调内和弦"""
        scale = generate_scale('C', ScaleType.MAJOR)
        progression = get_chord_progression_degrees(scale)
        
        self.assertEqual(len(progression), 7)
        self.assertEqual(progression[0]['chord'], 'C')
        self.assertEqual(progression[1]['chord'], 'Dm')
        self.assertEqual(progression[4]['chord'], 'G')
        self.assertEqual(progression[6]['chord'], 'Bdim')


class TestTempoAndRhythm(unittest.TestCase):
    """测试节拍与节奏"""
    
    def test_tempo_calculation(self):
        """测试速度计算"""
        bpm = calculate_tempo(60.0, 120)  # 60秒内120拍
        self.assertEqual(bpm, 120.0)
        
        bpm = calculate_tempo(30.0, 60)  # 30秒内60拍
        self.assertEqual(bpm, 120.0)
    
    def test_duration_calculation(self):
        """测试时长计算"""
        duration = calculate_duration(120, 60)  # 120 BPM，60拍
        self.assertEqual(duration, 30.0)
    
    def test_beat_durations(self):
        """测试节拍时长"""
        durations = get_beat_durations(120)
        
        # 120 BPM 时，四分音符 = 0.5秒
        self.assertAlmostEqual(durations['quarter_note'], 0.5, places=2)
        
        # 八分音符 = 0.25秒
        self.assertAlmostEqual(durations['eighth_note'], 0.25, places=2)
        
        # 全音符 = 2秒
        self.assertAlmostEqual(durations['whole_note'], 2.0, places=2)
    
    def test_rhythm_pattern_analysis(self):
        """测试节奏模式分析"""
        pattern = [4, 4, 4, 4]  # 四个四分音符
        analysis = analyze_rhythm_pattern(pattern, 120)
        
        self.assertEqual(analysis['total_beats'], 4)
        self.assertEqual(analysis['bpm'], 120)


class TestHarmonySuggestion(unittest.TestCase):
    """测试和声建议"""
    
    def test_harmony_for_melody(self):
        """测试旋律和声建议"""
        melody = ['C', 'E', 'G']
        suggestions = suggest_harmony_for_melody(melody, 'C major')
        
        self.assertEqual(len(suggestions), 3)
        # C 应该匹配 I 和弦
        self.assertEqual(suggestions[0]['melody_note'], 'C')


class TestScaleComparison(unittest.TestCase):
    """测试音阶比较"""
    
    def test_compare_scales(self):
        """测试音阶比较"""
        c_major = generate_scale('C', ScaleType.MAJOR)
        d_major = generate_scale('D', ScaleType.MAJOR)
        
        comparison = compare_scales(c_major, d_major)
        
        self.assertIn('common_notes', comparison)
        self.assertIn('similarity', comparison)
    
    def test_compare_major_minor(self):
        """测试大调小调比较"""
        c_major = generate_scale('C', ScaleType.MAJOR)
        c_minor = generate_scale('C', ScaleType.MINOR_NATURAL)
        
        comparison = compare_scales(c_major, c_minor)
        
        # C 大调和小调有共同的音
        self.assertGreater(len(comparison['common_notes']), 0)


class TestModes(unittest.TestCase):
    """测试调式"""
    
    def test_all_modes(self):
        """测试所有调式"""
        modes = get_all_modes_of_scale('C')
        
        self.assertEqual(len(modes), 7)
        self.assertIn('Ionian (Major)', modes)
        self.assertIn('Dorian', modes)
        self.assertIn('Locrian', modes)


class TestChordInversion(unittest.TestCase):
    """测试和弦转位"""
    
    def test_first_inversion(self):
        """测试第一转位"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        inverted = invert_chord(chord, 1)
        
        # 第一转位: E G C (低音变成 E)
        self.assertEqual(inverted.notes[0].get_full_name(), 'E')
        self.assertEqual(inverted.notes[1].get_full_name(), 'G')
        # 顶部音符升高一个八度
        self.assertEqual(inverted.notes[2].name, 'C')
        self.assertEqual(inverted.notes[2].octave, 5)
    
    def test_second_inversion(self):
        """测试第二转位"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        inverted = invert_chord(chord, 2)
        
        # 第二转位: G C E
        self.assertEqual(inverted.notes[0].get_full_name(), 'G')
    
    def test_inversion_name(self):
        """测试转位名称"""
        self.assertEqual(get_chord_inversion_name(ChordType.MAJOR_TRIAD, 0), "原位")
        self.assertEqual(get_chord_inversion_name(ChordType.MAJOR_TRIAD, 1), "第一转位（六和弦）")
        self.assertEqual(get_chord_inversion_name(ChordType.MAJOR_7, 1), "第一转位（五六和弦）")


class TestKeyAnalysis(unittest.TestCase):
    """测试调性分析"""
    
    def test_analyze_key(self):
        """测试调性分析"""
        # C 大调的音符
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        analysis = analyze_key_from_notes(notes)
        
        self.assertEqual(analysis['best_match']['key'], 'C major')
        self.assertEqual(analysis['best_match']['confidence'], 1.0)
    
    def test_analyze_key_partial(self):
        """测试部分音符的调性分析"""
        notes = ['C', 'E', 'G']  # C 大三和弦的音符
        analysis = analyze_key_from_notes(notes)
        
        self.assertGreater(analysis['best_match']['confidence'], 0)


class TestArpeggio(unittest.TestCase):
    """测试琶音"""
    
    def test_arpeggio_up(self):
        """测试上行琶音"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        arpeggio = generate_arpeggio(chord, 'up', 1)
        
        # 上行琶音: C E G
        self.assertEqual(len(arpeggio), 3)
        self.assertEqual(arpeggio[0].get_full_name(), 'C')
    
    def test_arpeggio_down(self):
        """测试下行琶音"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        arpeggio = generate_arpeggio(chord, 'down', 1)
        
        # 下行琶音: G E C
        self.assertEqual(len(arpeggio), 3)
        self.assertEqual(arpeggio[0].get_full_name(), 'G')
    
    def test_arpeggio_up_down(self):
        """测试上下行琶音"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        arpeggio = generate_arpeggio(chord, 'up_down', 1)
        
        # 上下行琶音: C E G E C
        self.assertEqual(len(arpeggio), 5)
    
    def test_arpeggio_multi_octave(self):
        """测试多八度琶音"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        arpeggio = generate_arpeggio(chord, 'up', 2)
        
        # 两八度上行: C E G C E G
        self.assertEqual(len(arpeggio), 6)


class TestIntervalMatrix(unittest.TestCase):
    """测试音程矩阵"""
    
    def test_interval_matrix(self):
        """测试音程矩阵"""
        matrix = get_interval_matrix('C')
        
        self.assertEqual(len(matrix), 12)
        self.assertEqual(matrix['C']['interval'], 'P1')
        self.assertEqual(matrix['E']['interval'], 'M3')
        self.assertEqual(matrix['G']['interval'], 'P5')


class TestChordFromIntervals(unittest.TestCase):
    """测试从音程创建和弦"""
    
    def test_create_chord(self):
        """测试从音程创建和弦"""
        intervals = [Interval.MAJOR_THIRD, Interval.PERFECT_FIFTH]
        chord = create_chord_from_intervals('C', intervals)
        
        self.assertEqual(len(chord.notes), 3)  # 根音 + 两个音程
        self.assertEqual(chord.notes[0].get_full_name(), 'C')
        self.assertEqual(chord.notes[1].get_full_name(), 'E')


class TestEnharmonic(unittest.TestCase):
    """测试等音"""
    
    def test_enharmonic(self):
        """测试等音"""
        result = get_note_enharmonic('C#')
        self.assertEqual(result['enharmonic'], 'Db')
        
        result = get_note_enharmonic('Gb')
        self.assertEqual(result['enharmonic'], 'F#')
    
    def test_enharmonic_natural(self):
        """测试自然音等音"""
        result = get_note_enharmonic('C')
        self.assertEqual(result['enharmonic'], 'N/A')


class TestInfoFunctions(unittest.TestCase):
    """测试信息获取函数"""
    
    def test_scale_types_info(self):
        """测试音阶类型信息"""
        info = get_all_scale_types_info()
        
        self.assertGreater(len(info), 10)
        # 应包含大调音阶
        major_info = next(i for i in info if i['name'] == 'major')
        self.assertEqual(major_info['notes_count'], 7)
    
    def test_chord_types_info(self):
        """测试和弦类型信息"""
        info = get_all_chord_types_info()
        
        self.assertGreater(len(info), 10)
    
    def test_circle_of_fifths(self):
        """测试五度圈"""
        circle = generate_circle_of_fifths()
        
        self.assertEqual(len(circle), 14)
        self.assertEqual(circle[0]['major_key'], 'C')
        self.assertEqual(circle[0]['accidentals'], 0)
        self.assertEqual(circle[1]['major_key'], 'G')
        self.assertEqual(circle[1]['accidentals'], 1)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_extreme_octave(self):
        """测试极端八度"""
        note = Note('C', 0, '')
        self.assertEqual(note.octave, 0)
        
        note = Note('C', 10, '')
        self.assertEqual(note.octave, 9)
    
    def test_zero_bpm(self):
        """测试零 BPM"""
        self.assertEqual(calculate_duration(0, 60), 0)
        self.assertEqual(calculate_tempo(60, 0), 0)
    
    def test_empty_pattern(self):
        """测试空节奏模式"""
        analysis = analyze_rhythm_pattern([], 120)
        self.assertEqual(analysis['total_beats'], 0)
    
    def test_chord_inversion_out_of_range(self):
        """测试超出范围的转位"""
        chord = generate_chord('C', ChordType.MAJOR_TRIAD)
        # 三和弦只有 3 个音，最多 2 次转位
        inverted = invert_chord(chord, 5)
        self.assertEqual(inverted.notes[0].get_full_name(), 'C')


class TestJapaneseScales(unittest.TestCase):
    """测试日本音阶"""
    
    def test_yo_scale(self):
        """测试阳音阶"""
        scale = generate_scale('C', ScaleType.JAPANESE_YO)
        self.assertEqual(len(scale.notes), 5)
    
    def test_in_scale(self):
        """测试阴音阶"""
        scale = generate_scale('C', ScaleType.JAPANESE_IN)
        self.assertEqual(len(scale.notes), 5)


class TestExtensions(unittest.TestCase):
    """测试扩展和弦"""
    
    def test_major_9(self):
        """测试大九和弦"""
        chord = generate_chord('C', ChordType.MAJOR_9)
        self.assertEqual(len(chord.notes), 5)
    
    def test_major_13(self):
        """测试大十三和弦"""
        chord = generate_chord('C', ChordType.MAJOR_13)
        self.assertEqual(len(chord.notes), 7)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestNote))
    suite.addTests(loader.loadTestsFromTestCase(TestMidiConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestScaleGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestChordGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestInterval))
    suite.addTests(loader.loadTestsFromTestCase(TestTranspose))
    suite.addTests(loader.loadTestsFromTestCase(TestChordAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestKeyRelations))
    suite.addTests(loader.loadTestsFromTestCase(TestScaleDegrees))
    suite.addTests(loader.loadTestsFromTestCase(TestTempoAndRhythm))
    suite.addTests(loader.loadTestsFromTestCase(TestHarmonySuggestion))
    suite.addTests(loader.loadTestsFromTestCase(TestScaleComparison))
    suite.addTests(loader.loadTestsFromTestCase(TestModes))
    suite.addTests(loader.loadTestsFromTestCase(TestChordInversion))
    suite.addTests(loader.loadTestsFromTestCase(TestKeyAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestArpeggio))
    suite.addTests(loader.loadTestsFromTestCase(TestIntervalMatrix))
    suite.addTests(loader.loadTestsFromTestCase(TestChordFromIntervals))
    suite.addTests(loader.loadTestsFromTestCase(TestEnharmonic))
    suite.addTests(loader.loadTestsFromTestCase(TestInfoFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestJapaneseScales))
    suite.addTests(loader.loadTestsFromTestCase(TestExtensions))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_tests()