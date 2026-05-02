"""
Music Utils 测试套件

测试乐理工具库的所有核心功能
"""

import unittest
import math
from music_utils import (
    Note, NoteName, Interval, Scale, ScaleType, Chord, ChordType, ChordVoicing,
    NoteValue, parse_note, parse_chord, circle_of_fifths, circle_of_fourths,
    relative_minor, relative_major, key_signature, bpm_to_milliseconds,
    bpm_to_seconds, harmonic_series, equal_temperament_frequency,
    guitar_standard_tuning, bass_standard_tuning, ukulele_standard_tuning,
    piano_key_to_note, note_to_piano_key, get_tempo_marking,
    JUST_INTERVALS, TEMPO_MARKINGS,
)


class TestNote(unittest.TestCase):
    """测试音符类"""
    
    def test_note_creation(self):
        """测试音符创建"""
        note = Note(NoteName.C, 4)
        self.assertEqual(note.name, NoteName.C)
        self.assertEqual(note.octave, 4)
    
    def test_note_string(self):
        """测试音符字符串表示"""
        self.assertEqual(str(Note(NoteName.C, 4)), "C4")
        self.assertEqual(str(Note(NoteName.A_SHARP, 5)), "A#5")
    
    def test_note_sharp_flat_names(self):
        """测试升号和降号显示"""
        note = Note(NoteName.C_SHARP, 4)
        self.assertEqual(note.sharp_name, "C#")
        self.assertEqual(note.flat_name, "Db")
    
    def test_midi_conversion(self):
        """测试 MIDI 转换"""
        # A4 = 69 (标准)
        self.assertEqual(Note(NoteName.A, 4).midi(), 69)
        # C4 = 60
        self.assertEqual(Note(NoteName.C, 4).midi(), 60)
        # C0 = 12 (最低)
        self.assertEqual(Note(NoteName.C, 0).midi(), 12)
    
    def test_frequency_calculation(self):
        """测试频率计算"""
        # A4 = 440 Hz
        a4 = Note(NoteName.A, 4)
        self.assertAlmostEqual(a4.frequency(), 440.0, places=1)
        # C4 = 约 261.63 Hz
        c4 = Note(NoteName.C, 4)
        self.assertAlmostEqual(c4.frequency(), 261.63, places=1)
    
    def test_note_from_frequency(self):
        """测试从频率获取音符"""
        note = Note.from_frequency(440.0)
        self.assertEqual(note.name, NoteName.A)
        self.assertEqual(note.octave, 4)
    
    def test_semitones_from(self):
        """测试半音距离计算"""
        c4 = Note(NoteName.C, 4)
        d4 = Note(NoteName.D, 4)
        self.assertEqual(d4.semitones_from(c4), 2)
        
        a4 = Note(NoteName.A, 4)
        c5 = Note(NoteName.C, 5)
        self.assertEqual(c5.semitones_from(a4), 3)
    
    def test_transpose(self):
        """测试移调"""
        c4 = Note(NoteName.C, 4)
        # 移高大二度
        d4 = c4.transpose(2)
        self.assertEqual(d4.name, NoteName.D)
        self.assertEqual(d4.octave, 4)
        # 移高八度
        c5 = c4.transpose(12)
        self.assertEqual(c5.name, NoteName.C)
        self.assertEqual(c5.octave, 5)
    
    def test_note_comparison(self):
        """测试音符比较"""
        c4 = Note(NoteName.C, 4)
        d4 = Note(NoteName.D, 4)
        self.assertTrue(c4 < d4)
        self.assertTrue(d4 > c4)
    
    def test_midi_to_note(self):
        """测试 MIDI 到音符转换"""
        note = Note.midi_to_note(69)
        self.assertEqual(note.name, NoteName.A)
        self.assertEqual(note.octave, 4)


class TestParseNote(unittest.TestCase):
    """测试音符解析"""
    
    def test_parse_basic_notes(self):
        """测试解析基本音符"""
        self.assertEqual(parse_note("C4"), Note(NoteName.C, 4))
        self.assertEqual(parse_note("A4"), Note(NoteName.A, 4))
        self.assertEqual(parse_note("G5"), Note(NoteName.G, 5))
    
    def test_parse_sharp_notes(self):
        """测试解析升号音符"""
        self.assertEqual(parse_note("C#4"), Note(NoteName.C_SHARP, 4))
        self.assertEqual(parse_note("F#5"), Note(NoteName.F_SHARP, 5))
    
    def test_parse_flat_notes(self):
        """测试解析降号音符"""
        self.assertEqual(parse_note("Db4"), Note(NoteName.C_SHARP, 4))
        self.assertEqual(parse_note("Eb5"), Note(NoteName.D_SHARP, 5))
    
    def test_parse_without_octave(self):
        """测试解析无八度音符（默认为4）"""
        self.assertEqual(parse_note("C"), Note(NoteName.C, 4))


class TestInterval(unittest.TestCase):
    """测试音程类"""
    
    def test_interval_semitones(self):
        """测试音程半音数"""
        self.assertEqual(Interval.UNISON, 0)
        self.assertEqual(Interval.MINOR_SECOND, 1)
        self.assertEqual(Interval.MAJOR_SECOND, 2)
        self.assertEqual(Interval.MINOR_THIRD, 3)
        self.assertEqual(Interval.MAJOR_THIRD, 4)
        self.assertEqual(Interval.PERFECT_FIFTH, 7)
        self.assertEqual(Interval.OCTAVE, 12)
    
    def test_interval_from_semitones(self):
        """测试从半音数获取音程"""
        self.assertEqual(Interval.from_semitones(0), Interval.UNISON)
        self.assertEqual(Interval.from_semitones(4), Interval.MAJOR_THIRD)
        self.assertEqual(Interval.from_semitones(7), Interval.PERFECT_FIFTH)
    
    def test_interval_chinese_names(self):
        """测试音程中文名称"""
        self.assertEqual(Interval.MAJOR_THIRD.name_zh(), "大三度")
        self.assertEqual(Interval.PERFECT_FIFTH.name_zh(), "纯五度")


class TestScale(unittest.TestCase):
    """测试音阶类"""
    
    def test_major_scale_notes(self):
        """测试大调音阶音符"""
        scale = Scale(NoteName.C, ScaleType.MAJOR)
        notes = scale.notes()
        expected = [NoteName.C, NoteName.D, NoteName.E, NoteName.F,
                    NoteName.G, NoteName.A, NoteName.B]
        self.assertEqual(notes, expected)
    
    def test_minor_scale_notes(self):
        """测试自然小调音阶音符"""
        scale = Scale(NoteName.A, ScaleType.MINOR)
        notes = scale.notes()
        expected = [NoteName.A, NoteName.B, NoteName.C,
                    NoteName.D, NoteName.E, NoteName.F, NoteName.G]
        self.assertEqual(notes, expected)
    
    def test_blues_scale_notes(self):
        """测试布鲁斯音阶音符"""
        scale = Scale(NoteName.A, ScaleType.BLUES)
        notes = scale.notes()
        # A blues: A, C, D, D#, E, G
        expected = [NoteName.A, NoteName.C, NoteName.D,
                    NoteName.D_SHARP, NoteName.E, NoteName.G]
        self.assertEqual(notes, expected)
    
    def test_pentatonic_scale_notes(self):
        """测试五声音阶音符"""
        # 大调五声 C: C, D, E, G, A
        scale = Scale(NoteName.C, ScaleType.PENTATONIC_MAJOR)
        notes = scale.notes()
        expected = [NoteName.C, NoteName.D, NoteName.E, NoteName.G, NoteName.A]
        self.assertEqual(notes, expected)
    
    def test_scale_contains_note(self):
        """测试音阶包含音符"""
        scale = Scale(NoteName.C, ScaleType.MAJOR)
        self.assertTrue(scale.contains_note(NoteName.C))
        self.assertTrue(scale.contains_note(NoteName.E))
        self.assertFalse(scale.contains_note(NoteName.C_SHARP))
    
    def test_scale_notes_with_octave(self):
        """测试音阶音符带八度"""
        scale = Scale(NoteName.C, ScaleType.MAJOR)
        notes = scale.notes_with_octave(4, 1)
        self.assertEqual(len(notes), 7)
        self.assertEqual(notes[0], Note(NoteName.C, 4))
        self.assertEqual(notes[-1], Note(NoteName.B, 4))
    
    def test_scale_frequencies(self):
        """测试音阶频率"""
        scale = Scale(NoteName.C, ScaleType.MAJOR)
        freqs = scale.frequencies(4, 1)
        self.assertEqual(len(freqs), 7)
        # C4 = 约 261.63 Hz
        self.assertAlmostEqual(freqs[0], 261.63, places=1)
    
    def test_scale_degree(self):
        """测试音阶级别"""
        scale = Scale(NoteName.C, ScaleType.MAJOR)
        self.assertEqual(scale.degree(1), NoteName.C)
        self.assertEqual(scale.degree(3), NoteName.E)
        self.assertEqual(scale.degree(5), NoteName.G)
    
    def test_scale_triad(self):
        """测试音阶三和弦"""
        scale = Scale(NoteName.C, ScaleType.MAJOR)
        # I级和弦 = C大三
        triad = scale.triad(1)
        self.assertEqual(triad.root, NoteName.C)
        self.assertEqual(triad.chord_type, ChordType.MAJOR)
        # ii级和弦 = D小三
        triad2 = scale.triad(2)
        self.assertEqual(triad2.root, NoteName.D)
        self.assertEqual(triad2.chord_type, ChordType.MINOR)
    
    def test_scale_factory_methods(self):
        """测试音阶工厂方法"""
        c_major = Scale.major(NoteName.C)
        self.assertEqual(c_major.scale_type, ScaleType.MAJOR)
        
        a_minor = Scale.minor(NoteName.A)
        self.assertEqual(a_minor.scale_type, ScaleType.MINOR)


class TestChord(unittest.TestCase):
    """测试和弦类"""
    
    def test_major_chord_notes(self):
        """测试大三和弦音符"""
        chord = Chord(NoteName.C, ChordType.MAJOR)
        notes = chord.notes()
        expected = [NoteName.C, NoteName.E, NoteName.G]
        self.assertEqual(notes, expected)
    
    def test_minor_chord_notes(self):
        """测试小三和弦音符"""
        chord = Chord(NoteName.A, ChordType.MINOR)
        notes = chord.notes()
        expected = [NoteName.A, NoteName.C, NoteName.E]
        self.assertEqual(notes, expected)
    
    def test_dominant_7_chord_notes(self):
        """测试属七和弦音符"""
        chord = Chord(NoteName.G, ChordType.DOMINANT_7)
        notes = chord.notes()
        expected = [NoteName.G, NoteName.B, NoteName.D, NoteName.F]
        self.assertEqual(notes, expected)
    
    def test_power_chord_notes(self):
        """测试强力和弦音符"""
        chord = Chord(NoteName.E, ChordType.POWER)
        notes = chord.notes()
        expected = [NoteName.E, NoteName.B]
        self.assertEqual(notes, expected)
    
    def test_chord_string(self):
        """测试和弦字符串表示"""
        self.assertEqual(str(Chord(NoteName.C, ChordType.MAJOR)), "C")
        self.assertEqual(str(Chord(NoteName.A, ChordType.MINOR)), "Am")
        self.assertEqual(str(Chord(NoteName.G, ChordType.DOMINANT_7)), "G7")
    
    def test_chord_notes_with_octave(self):
        """测试和弦音符带八度"""
        chord = Chord(NoteName.C, ChordType.MAJOR)
        notes = chord.notes_with_octave(4)
        self.assertEqual(notes[0], Note(NoteName.C, 4))
        self.assertEqual(notes[1], Note(NoteName.E, 4))
        self.assertEqual(notes[2], Note(NoteName.G, 4))
    
    def test_chord_inversion(self):
        """测试和弦转位"""
        chord = Chord(NoteName.C, ChordType.MAJOR)
        # 第一转位：E-G-C（高八度）
        voicing = chord.invert(1)
        notes = voicing.notes()
        self.assertEqual(notes[0].name, NoteName.E)
        self.assertEqual(notes[1].name, NoteName.G)
        self.assertEqual(notes[2].name, NoteName.C)
        self.assertEqual(notes[2].octave, 5)
    
    def test_chord_identify(self):
        """测试和弦识别"""
        # C大三和弦
        chord = Chord.identify([NoteName.C, NoteName.E, NoteName.G])
        self.assertIsNotNone(chord)
        self.assertEqual(chord.root, NoteName.C)
        self.assertEqual(chord.chord_type, ChordType.MAJOR)
        
        # Am小三和弦
        chord = Chord.identify([NoteName.A, NoteName.C, NoteName.E])
        self.assertIsNotNone(chord)
        self.assertEqual(chord.root, NoteName.A)
        self.assertEqual(chord.chord_type, ChordType.MINOR)
    
    def test_chord_factory_methods(self):
        """测试和弦工厂方法"""
        c_major = Chord.major(NoteName.C)
        self.assertEqual(c_major.chord_type, ChordType.MAJOR)
        
        a_minor = Chord.minor(NoteName.A)
        self.assertEqual(a_minor.chord_type, ChordType.MINOR)


class TestParseChord(unittest.TestCase):
    """测试和弦解析"""
    
    def test_parse_major_chords(self):
        """测试解析大三和弦"""
        self.assertEqual(parse_chord("C"), Chord(NoteName.C, ChordType.MAJOR))
        self.assertEqual(parse_chord("G"), Chord(NoteName.G, ChordType.MAJOR))
    
    def test_parse_minor_chords(self):
        """测试解析小三和弦"""
        self.assertEqual(parse_chord("Am"), Chord(NoteName.A, ChordType.MINOR))
        self.assertEqual(parse_chord("Dm"), Chord(NoteName.D, ChordType.MINOR))
        self.assertEqual(parse_chord("Dmin"), Chord(NoteName.D, ChordType.MINOR))
    
    def test_parse_seventh_chords(self):
        """测试解析七和弦"""
        self.assertEqual(parse_chord("G7"), Chord(NoteName.G, ChordType.DOMINANT_7))
        self.assertEqual(parse_chord("Cmaj7"), Chord(NoteName.C, ChordType.MAJOR_7))
        self.assertEqual(parse_chord("Dm7"), Chord(NoteName.D, ChordType.MINOR_7))
    
    def test_parse_other_chords(self):
        """测试解析其他和弦"""
        self.assertEqual(parse_chord("Csus4"), Chord(NoteName.C, ChordType.SUS_4))
        self.assertEqual(parse_chord("Gsus2"), Chord(NoteName.G, ChordType.SUS_2))
        self.assertEqual(parse_chord("C5"), Chord(NoteName.C, ChordType.POWER))
    
    def test_parse_sharp_flat_chords(self):
        """测试解析升降号和弦"""
        self.assertEqual(parse_chord("F#m"), Chord(NoteName.F_SHARP, ChordType.MINOR))
        self.assertEqual(parse_chord("Bbmaj7"), Chord(NoteName.A_SHARP, ChordType.MAJOR_7))


class TestCircleOfFifths(unittest.TestCase):
    """测试五度圈"""
    
    def test_circle_of_fifths_order(self):
        """测试五度圈顺序"""
        circle = circle_of_fifths()
        expected = [NoteName.C, NoteName.G, NoteName.D, NoteName.A,
                    NoteName.E, NoteName.B, NoteName.F_SHARP, NoteName.C_SHARP,
                    NoteName.G_SHARP, NoteName.D_SHARP, NoteName.A_SHARP, NoteName.F]
        self.assertEqual(circle, expected)
    
    def test_circle_of_fourths_order(self):
        """测试四度圈顺序"""
        circle = circle_of_fourths()
        expected = [NoteName.C, NoteName.F, NoteName.A_SHARP, NoteName.D_SHARP,
                    NoteName.G_SHARP, NoteName.C_SHARP, NoteName.F_SHARP, NoteName.B,
                    NoteName.E, NoteName.A, NoteName.D, NoteName.G]
        self.assertEqual(circle, expected)


class TestRelativeKeys(unittest.TestCase):
    """测试关系调"""
    
    def test_relative_minor(self):
        """测试关系小调"""
        self.assertEqual(relative_minor(NoteName.C), NoteName.A)
        self.assertEqual(relative_minor(NoteName.G), NoteName.E)
        self.assertEqual(relative_minor(NoteName.D), NoteName.B)
    
    def test_relative_major(self):
        """测试关系大调"""
        self.assertEqual(relative_major(NoteName.A), NoteName.C)
        self.assertEqual(relative_major(NoteName.E), NoteName.G)
        self.assertEqual(relative_major(NoteName.B), NoteName.D)


class TestKeySignature(unittest.TestCase):
    """测试调号"""
    
    def test_c_major_key_signature(self):
        """测试 C 大调调号（无升降号）"""
        sig = key_signature(NoteName.C, True)
        self.assertEqual(sig, [])
    
    def test_g_major_key_signature(self):
        """测试 G 大调调号（一个升号：F#）"""
        sig = key_signature(NoteName.G, True)
        self.assertEqual(sig, [NoteName.F_SHARP])
    
    def test_d_major_key_signature(self):
        """测试 D 大调调号（两个升号：F#, C#）"""
        sig = key_signature(NoteName.D, True)
        self.assertEqual(sig, [NoteName.F_SHARP, NoteName.C_SHARP])
    
    def test_f_major_key_signature(self):
        """测试 F 大调调号（一个降号：Bb）"""
        sig = key_signature(NoteName.F, True)
        self.assertEqual(sig, [NoteName.A_SHARP])


class TestMetronome(unittest.TestCase):
    """测试节拍器"""
    
    def test_bpm_to_milliseconds(self):
        """测试 BPM 到毫秒转换"""
        # 60 BPM = 1000 ms/拍
        self.assertEqual(bpm_to_milliseconds(60), 1000.0)
        # 120 BPM = 500 ms/拍
        self.assertEqual(bpm_to_milliseconds(120), 500.0)
        # 240 BPM = 250 ms/拍
        self.assertEqual(bpm_to_milliseconds(240), 250.0)
    
    def test_bpm_to_seconds(self):
        """测试 BPM 到秒转换"""
        self.assertEqual(bpm_to_seconds(60), 1.0)
        self.assertEqual(bpm_to_seconds(120), 0.5)
    
    def test_get_tempo_marking(self):
        """测试速度术语"""
        self.assertIn("Allegro", get_tempo_marking(140))
        self.assertIn("Adagio", get_tempo_marking(70))
        self.assertIn("Presto", get_tempo_marking(200))


class TestNoteValue(unittest.TestCase):
    """测试音符时值"""
    
    def test_note_value_duration(self):
        """测试音符时值"""
        self.assertEqual(NoteValue.WHOLE.duration_beats(), 4.0)
        self.assertEqual(NoteValue.HALF.duration_beats(), 2.0)
        self.assertEqual(NoteValue.QUARTER.duration_beats(), 1.0)
        self.assertEqual(NoteValue.EIGHTH.duration_beats(), 0.5)
    
    def test_note_value_with_dots(self):
        """测试带附点的时值"""
        # 四分音符 = 1拍
        self.assertEqual(NoteValue.QUARTER.duration_with_dots(0), 1.0)
        # 四分音符附点 = 1.5拍
        self.assertEqual(NoteValue.QUARTER.duration_with_dots(1), 1.5)
        # 四分音符双附点 = 1.75拍
        self.assertEqual(NoteValue.QUARTER.duration_with_dots(2), 1.75)


class TestHarmonicSeries(unittest.TestCase):
    """测试泛音列"""
    
    def test_harmonic_series(self):
        """测试泛音列生成"""
        # A4 = 440 Hz 的前几个泛音
        series = harmonic_series(440.0, 5)
        expected = [440.0, 880.0, 1320.0, 1760.0, 2200.0]
        self.assertEqual(len(series), 5)
        for i, freq in enumerate(expected):
            self.assertAlmostEqual(series[i], freq, places=1)


class TestEqualTemperament(unittest.TestCase):
    """测试十二平均律"""
    
    def test_equal_temperament_frequency(self):
        """测试十二平均律频率计算"""
        # A4 = 440 Hz (0半音距离)
        self.assertEqual(equal_temperament_frequency(0), 440.0)
        # A5 = 880 Hz (+12半音)
        self.assertAlmostEqual(equal_temperament_frequency(12), 880.0, places=1)
        # A#4 = 约 466.16 Hz (+1半音)
        self.assertAlmostEqual(equal_temperament_frequency(1), 466.16, places=1)


class TestInstrumentTuning(unittest.TestCase):
    """测试乐器调弦"""
    
    def test_guitar_standard_tuning(self):
        """测试吉他标准调弦"""
        tuning = guitar_standard_tuning()
        self.assertEqual(len(tuning), 6)
        self.assertEqual(tuning[0], Note(NoteName.E, 2))  # 6弦
        self.assertEqual(tuning[5], Note(NoteName.E, 4))  # 1弦
    
    def test_bass_standard_tuning(self):
        """测试贝斯标准调弦"""
        tuning = bass_standard_tuning()
        self.assertEqual(len(tuning), 4)
        self.assertEqual(tuning[0], Note(NoteName.E, 1))
    
    def test_ukulele_standard_tuning(self):
        """测试尤克里里标准调弦"""
        tuning = ukulele_standard_tuning()
        self.assertEqual(len(tuning), 4)
        self.assertEqual(tuning[0], Note(NoteName.G, 4))


class TestPianoKeys(unittest.TestCase):
    """测试钢琴键"""
    
    def test_piano_key_to_note(self):
        """测试钢琴键到音符"""
        # 第1键 = A0
        note = piano_key_to_note(1)
        self.assertEqual(note.name, NoteName.A)
        self.assertEqual(note.octave, 0)
        # 第88键 = C8
        note = piano_key_to_note(88)
        self.assertEqual(note.name, NoteName.C)
        self.assertEqual(note.octave, 8)
    
    def test_note_to_piano_key(self):
        """测试音符到钢琴键"""
        self.assertEqual(note_to_piano_key(Note(NoteName.A, 0)), 1)
        self.assertEqual(note_to_piano_key(Note(NoteName.C, 8)), 88)


class TestJustIntonation(unittest.TestCase):
    """测试纯律"""
    
    def test_just_intervals(self):
        """测试纯律音程"""
        self.assertEqual(JUST_INTERVALS["unison"], (1, 1, "纯一度"))
        self.assertEqual(JUST_INTERVALS["perfect_fifth"], (3, 2, "纯五度"))
        self.assertEqual(JUST_INTERVALS["major_third"], (5, 4, "大三度"))


if __name__ == "__main__":
    unittest.main()