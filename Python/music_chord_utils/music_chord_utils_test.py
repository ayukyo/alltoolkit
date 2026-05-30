"""
Music Chord Utils Tests
音乐和弦工具测试

Tests for:
- 音符转换（音名、MIDI、频率）
- 和弦构建与识别
- 音阶生成
- 音程计算
- 和弦转位
- 移调
"""

import sys
import os
import math

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from music_chord_utils.mod import (
    normalize_note,
    note_to_semitone,
    semitone_to_note,
    midi_to_note,
    note_to_midi,
    note_to_frequency,
    midi_to_frequency,
    frequency_to_midi,
    get_interval,
    calculate_interval,
    build_chord,
    identify_chord,
    invert_chord,
    get_chord_inversions,
    build_scale,
    get_scale_degrees,
    get_diatonic_chords,
    get_key_signature,
    transpose_note,
    transpose_chord,
    get_relative_key,
    get_enharmonic,
    is_diatonic,
    get_note_name_variants,
    parse_chord_symbol,
    c_major_scale,
    a_minor_scale,
    circle_of_fifths,
    circle_of_fourths,
    Chord,
    NOTE_NAMES_SHARP,
    NOTE_NAMES_FLAT,
    CHORD_FORMULAS,
    SCALE_FORMULAS,
)


class TestNoteConversion:
    """音符转换测试"""
    
    def test_normalize_note(self):
        """测试音符标准化"""
        assert normalize_note('C') == 'C'
        assert normalize_note('c') == 'C'
        assert normalize_note('Db') == 'C#'  # 降号转升号
        assert normalize_note('Bb') == 'A#'
        assert normalize_note('Gb') == 'F#'
    
    def test_note_to_semitone(self):
        """测试音符转半音编号"""
        assert note_to_semitone('C') == 0
        assert note_to_semitone('C#') == 1
        assert note_to_semitone('D') == 2
        assert note_to_semitone('A') == 9
        assert note_to_semitone('B') == 11
        assert note_to_semitone('Db') == 1  # Db = C#
    
    def test_semitone_to_note(self):
        """测试半音编号转音符"""
        assert semitone_to_note(0) == 'C'
        assert semitone_to_note(1) == 'C#'
        assert semitone_to_note(1, use_flat=True) == 'Db'
        assert semitone_to_note(11) == 'B'
    
    def test_midi_to_note(self):
        """测试MIDI编号转音符"""
        assert midi_to_note(60) == 'C4'
        assert midi_to_note(61) == 'C#4'
        assert midi_to_note(69) == 'A4'
        assert midi_to_note(21) == 'A0'
        assert midi_to_note(108) == 'C8'
    
    def test_note_to_midi(self):
        """测试音符转MIDI编号"""
        assert note_to_midi('C4') == 60
        assert note_to_midi('A4') == 69
        assert note_to_midi('C0') == 12
        assert note_to_midi('C#4') == 61
        assert note_to_midi('Db4') == 61
    
    def test_note_to_frequency(self):
        """测试音符转频率"""
        # A4 = 440 Hz
        assert math.isclose(note_to_frequency('A4'), 440.0, rel_tol=0.01)
        # A5 = 880 Hz (高八度)
        assert math.isclose(note_to_frequency('A5'), 880.0, rel_tol=0.01)
        # A3 = 220 Hz (低八度)
        assert math.isclose(note_to_frequency('A3'), 220.0, rel_tol=0.01)
    
    def test_midi_to_frequency(self):
        """测试MIDI编号转频率"""
        assert math.isclose(midi_to_frequency(69), 440.0, rel_tol=0.01)
        assert math.isclose(midi_to_frequency(81), 880.0, rel_tol=0.01)
    
    def test_frequency_to_midi(self):
        """测试频率转MIDI编号"""
        assert frequency_to_midi(440.0) == 69
        assert frequency_to_midi(880.0) == 81
        assert frequency_to_midi(220.0) == 57
    
    def test_note_roundtrip(self):
        """测试音符往返转换"""
        for midi in [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]:
            note = midi_to_note(midi)
            result = note_to_midi(note)
            assert result == midi, f"Roundtrip failed for MIDI {midi}: {note} -> {result}"


class TestIntervals:
    """音程测试"""
    
    def test_get_interval(self):
        """测试获取音程信息"""
        interval = get_interval(0)
        assert interval.name == "纯一度"
        
        interval = get_interval(7)
        assert interval.name == "纯五度"
        
        interval = get_interval(12)
        assert interval.name == "纯八度"
    
    def test_calculate_interval(self):
        """测试计算音程"""
        interval = calculate_interval('C', 'G')
        assert interval.name == "纯五度"
        
        interval = calculate_interval('C', 'E')
        assert interval.name == "大三度"
        
        interval = calculate_interval('C', 'Eb')
        assert interval.name == "小三度"
        
        interval = calculate_interval('C', 'F')
        assert interval.name == "纯四度"


class TestChords:
    """和弦测试"""
    
    def test_build_major_chord(self):
        """测试构建大三和弦"""
        chord = build_chord('C', 'major')
        assert chord.root == 'C'
        assert chord.quality == 'major'
        assert chord.notes == ['C', 'E', 'G']
    
    def test_build_minor_chord(self):
        """测试构建小三和弦"""
        chord = build_chord('A', 'minor')
        assert chord.root == 'A'
        assert chord.quality == 'minor'
        assert chord.notes == ['A', 'C', 'E']
    
    def test_build_dim_chord(self):
        """测试构建减三和弦"""
        chord = build_chord('B', 'dim')
        assert chord.notes == ['B', 'D', 'F']
    
    def test_build_aug_chord(self):
        """测试构建增三和弦"""
        chord = build_chord('C', 'aug')
        assert chord.notes == ['C', 'E', 'G#']
    
    def test_build_seventh_chords(self):
        """测试构建七和弦"""
        # 属七和弦
        chord = build_chord('G', '7')
        assert chord.notes == ['G', 'B', 'D', 'F']
        
        # 大七和弦
        chord = build_chord('C', 'maj7')
        assert chord.notes == ['C', 'E', 'G', 'B']
        
        # 小七和弦
        chord = build_chord('A', 'm7')
        assert chord.notes == ['A', 'C', 'E', 'G']
    
    def test_build_sus_chords(self):
        """测试构建挂留和弦"""
        chord = build_chord('D', 'sus2')
        assert chord.notes == ['D', 'E', 'A']
        
        chord = build_chord('G', 'sus4')
        assert chord.notes == ['G', 'C', 'D']
    
    def test_build_power_chord(self):
        """测试构建强力和弦"""
        chord = build_chord('E', 'power')
        assert chord.notes == ['E', 'B']
    
    def test_identify_major_chord(self):
        """测试识别大三和弦"""
        result = identify_chord(['C', 'E', 'G'])
        assert result == ('C', 'major')
    
    def test_identify_minor_chord(self):
        """测试识别小三和弦"""
        result = identify_chord(['A', 'C', 'E'])
        assert result == ('A', 'minor')
    
    def test_identify_seventh_chord(self):
        """测试识别七和弦"""
        result = identify_chord(['G', 'B', 'D', 'F'])
        assert result == ('G', '7')
        
        result = identify_chord(['A', 'C', 'E', 'G'])
        assert result == ('A', 'm7')
    
    def test_identify_dim_chord(self):
        """测试识别减三和弦"""
        result = identify_chord(['B', 'D', 'F'])
        assert result == ('B', 'dim')
    
    def test_identify_no_match(self):
        """测试无法识别的和弦（两个相邻音符不构成和弦）"""
        result = identify_chord(['C', 'D'])  # intervals = [0, 2]，不匹配任何和弦
        # [0, 2] 可能匹配 sus2，让我们测试一个确实不匹配的情况
        result = identify_chord(['C', 'C#', 'D'])  # 三个连续半音，不匹配任何和弦
        assert result is None  # 这种组合不构成标准和弦
    
    def test_chord_inversion(self):
        """测试和弦转位"""
        # C大三和弦原位
        assert invert_chord(['C', 'E', 'G'], 0) == ['C', 'E', 'G']
        # 第一转位
        assert invert_chord(['C', 'E', 'G'], 1) == ['E', 'G', 'C']
        # 第二转位
        assert invert_chord(['C', 'E', 'G'], 2) == ['G', 'C', 'E']
        # 循环转位
        assert invert_chord(['C', 'E', 'G'], 3) == ['C', 'E', 'G']
    
    def test_get_chord_inversions(self):
        """测试获取所有转位"""
        inversions = get_chord_inversions('C', 'major')
        assert len(inversions) == 3
        assert inversions[0] == ['C', 'E', 'G']
        assert inversions[1] == ['E', 'G', 'C']
        assert inversions[2] == ['G', 'C', 'E']


class TestScales:
    """音阶测试"""
    
    def test_c_major_scale(self):
        """测试C大调音阶"""
        scale = build_scale('C', 'major')
        assert scale == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    
    def test_g_major_scale(self):
        """测试G大调音阶"""
        scale = build_scale('G', 'major')
        assert scale == ['G', 'A', 'B', 'C', 'D', 'E', 'F#']
    
    def test_a_minor_scale(self):
        """测试A小调音阶"""
        scale = build_scale('A', 'natural_minor')
        assert scale == ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    def test_pentatonic_major_scale(self):
        """测试大调五声音阶"""
        scale = build_scale('C', 'pentatonic_major')
        assert scale == ['C', 'D', 'E', 'G', 'A']
    
    def test_pentatonic_minor_scale(self):
        """测试小调五声音阶"""
        scale = build_scale('A', 'pentatonic_minor')
        assert scale == ['A', 'C', 'D', 'E', 'G']
    
    def test_blues_scale(self):
        """测试蓝调音阶"""
        scale = build_scale('A', 'blues')
        assert scale == ['A', 'C', 'D', 'D#', 'E', 'G']
    
    def test_dorian_mode(self):
        """测试多利亚调式"""
        scale = build_scale('D', 'dorian')
        assert scale == ['D', 'E', 'F', 'G', 'A', 'B', 'C']
    
    def test_chromatic_scale(self):
        """测试半音阶"""
        scale = build_scale('C', 'chromatic')
        assert len(scale) == 12
        assert scale == ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def test_get_scale_degrees(self):
        """测试获取音阶度数"""
        degrees = get_scale_degrees('major')
        assert degrees == ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        
        degrees = get_scale_degrees('pentatonic_major')
        assert len(degrees) == 5
    
    def test_get_diatonic_chords(self):
        """测试顺阶和弦"""
        chords = get_diatonic_chords('C', 'major')
        assert len(chords) == 7
        
        # I 级大三和弦
        assert chords[0].notes == ['C', 'E', 'G']
        assert chords[0].quality == 'major'
        
        # II 级小三和弦
        assert chords[1].notes == ['D', 'F', 'A']
        assert chords[1].quality == 'minor'
        
        # VII 级减三和弦
        assert chords[6].notes == ['B', 'D', 'F']
        assert chords[6].quality == 'dim'


class TestKeySignature:
    """调号测试"""
    
    def test_c_major_key_signature(self):
        """测试C大调调号（无升降号）"""
        accidentals, is_sharp = get_key_signature('C', 'major')
        assert accidentals == []
    
    def test_g_major_key_signature(self):
        """测试G大调调号（1个升号）"""
        accidentals, is_sharp = get_key_signature('G', 'major')
        assert 'F#' in accidentals
        assert is_sharp == True
    
    def test_d_major_key_signature(self):
        """测试D大调调号（2个升号）"""
        accidentals, is_sharp = get_key_signature('D', 'major')
        assert 'F#' in accidentals
        assert 'C#' in accidentals
    
    def test_f_major_key_signature(self):
        """测试F大调调号（1个降号）"""
        accidentals, is_sharp = get_key_signature('F', 'major')
        assert is_sharp == False


class TestTransposition:
    """移调测试"""
    
    def test_transpose_note_up(self):
        """测试音符上移"""
        assert transpose_note('C', 2) == 'D'
        assert transpose_note('C', 4) == 'E'
        assert transpose_note('C', 7) == 'G'
        assert transpose_note('C', 12) == 'C'
    
    def test_transpose_note_down(self):
        """测试音符下移"""
        assert transpose_note('D', -2) == 'C'
        assert transpose_note('E', -1) == 'D#'
        assert transpose_note('G', -7) == 'C'
    
    def test_transpose_chord(self):
        """测试和弦移调"""
        assert transpose_chord('C', 2) == 'D'
        assert transpose_chord('Cm', 2) == 'Dm'
        assert transpose_chord('Cmaj7', 5) == 'Fmaj7'
        assert transpose_chord('Am7', 3) == 'Cm7'
    
    def test_transpose_chord_with_sharp(self):
        """测试带升号和弦移调"""
        assert transpose_chord('C#', 2) == 'D#'
        assert transpose_chord('F#m7', 2) == 'G#m7'


class TestRelativeKey:
    """关系调测试"""
    
    def test_c_major_relative_minor(self):
        """测试C大调关系小调"""
        root, scale_type = get_relative_key('C', 'major')
        assert root == 'A'
        assert scale_type == 'natural_minor'
    
    def test_a_minor_relative_major(self):
        """测试A小调关系大调"""
        root, scale_type = get_relative_key('A', 'minor')
        assert root == 'C'
        assert scale_type == 'major'
    
    def test_g_major_relative_minor(self):
        """测试G大调关系小调"""
        root, scale_type = get_relative_key('G', 'major')
        assert root == 'E'


class TestEnharmonic:
    """等音测试"""
    
    def test_enharmonic_sharp_to_flat(self):
        """测试升号等音"""
        assert get_enharmonic('C#') == 'Db'
        assert get_enharmonic('F#') == 'Gb'
        assert get_enharmonic('G#') == 'Ab'
    
    def test_enharmonic_flat_to_sharp(self):
        """测试自然音返回自身（没有等音变化）"""
        assert get_enharmonic('C') == 'C'  # C 是自然音，没有等音
        assert get_enharmonic('D') == 'D'  # D 是自然音，没有等音
    
    def test_enharmonic_flat_to_sharp_input(self):
        """测试降号音符返回升号"""
        assert get_enharmonic('Db') == 'C#'  # Db 的等音是 C#
        assert get_enharmonic('Eb') == 'D#'  # Eb 的等音是 D#
    
    def test_note_variants(self):
        """测试音符变体"""
        variants = get_note_name_variants('C#')
        assert 'C#' in variants
        assert 'Db' in variants


class TestDiatonic:
    """调内音测试"""
    
    def test_is_diatonic_c_major(self):
        """测试C大调调内音"""
        assert is_diatonic('C', 'C', 'major') == True
        assert is_diatonic('D', 'C', 'major') == True
        assert is_diatonic('E', 'C', 'major') == True
        assert is_diatonic('F#', 'C', 'major') == False
        assert is_diatonic('G#', 'C', 'major') == False
    
    def test_is_diatonic_g_major(self):
        """测试G大调调内音"""
        assert is_diatonic('G', 'G', 'major') == True
        assert is_diatonic('F#', 'G', 'major') == True  # G大调有F#
        assert is_diatonic('F', 'G', 'major') == False  # F是还原音


class TestParseChordSymbol:
    """和弦符号解析测试"""
    
    def test_parse_major_chord(self):
        """测试解析大三和弦"""
        root, quality = parse_chord_symbol('C')
        assert root == 'C'
        assert quality == 'major'
    
    def test_parse_minor_chord(self):
        """测试解析小三和弦"""
        root, quality = parse_chord_symbol('Am')
        assert root == 'A'
        assert quality == 'minor'
        
        root, quality = parse_chord_symbol('Dmin')
        assert root == 'D'
        assert quality == 'minor'
    
    def test_parse_seventh_chords(self):
        """测试解析七和弦"""
        root, quality = parse_chord_symbol('G7')
        assert root == 'G'
        assert quality == '7'
        
        root, quality = parse_chord_symbol('Cmaj7')
        assert root == 'C'
        assert quality == 'maj7'
        
        root, quality = parse_chord_symbol('Em7')
        assert root == 'E'
        assert quality == 'm7'
    
    def test_parse_sus_chords(self):
        """测试解析挂留和弦"""
        root, quality = parse_chord_symbol('Dsus2')
        assert root == 'D'
        assert quality == 'sus2'
        
        root, quality = parse_chord_symbol('Gsus4')
        assert root == 'G'
        assert quality == 'sus4'
    
    def test_parse_sharp_flat_chords(self):
        """测试解析升降号和弦"""
        root, quality = parse_chord_symbol('C#m7')
        assert root == 'C#'
        assert quality == 'm7'
        
        root, quality = parse_chord_symbol('Bb7')
        assert root == 'A#'  # 标准化为升号
        assert quality == '7'


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_c_major_scale_func(self):
        """测试C大调音阶便捷函数"""
        scale = c_major_scale()
        assert scale == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    
    def test_a_minor_scale_func(self):
        """测试A小调音阶便捷函数"""
        scale = a_minor_scale()
        assert scale == ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    def test_circle_of_fifths(self):
        """测试五度圈"""
        circle = circle_of_fifths()
        assert circle[0] == 'C'
        assert circle[1] == 'G'  # C上方五度
        assert circle[2] == 'D'  # G上方五度
        assert len(circle) == 12
    
    def test_circle_of_fourths(self):
        """测试四度圈"""
        circle = circle_of_fourths()
        assert circle[0] == 'C'
        assert circle[1] == 'F'  # C上方四度
        assert circle[2] == 'A#'  # F上方四度（Bb转A#）
        assert len(circle) == 12


class TestEdgeCases:
    """边界情况测试"""
    
    def test_invalid_note(self):
        """测试无效音符"""
        try:
            note_to_semitone('H')
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    def test_invalid_chord_quality(self):
        """测试无效和弦品质"""
        try:
            build_chord('C', 'invalid_quality')
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    def test_invalid_scale_type(self):
        """测试无效音阶类型"""
        try:
            build_scale('C', 'invalid_scale')
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    def test_midi_range(self):
        """测试MIDI范围边界"""
        # 有效范围
        assert midi_to_note(0) == 'C-1'
        assert midi_to_note(127) == 'G9'
        
        # 无效范围
        try:
            midi_to_note(128)
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    def test_chord_with_single_note(self):
        """测试单音和弦"""
        result = identify_chord(['C'])
        assert result is None
    
    def test_empty_notes(self):
        """测试空音符列表"""
        result = identify_chord([])
        assert result is None
    
    def test_transpose_wrap_around(self):
        """测试移调回绕"""
        # 上移超过八度
        assert transpose_note('C', 14) == 'D'  # 14 % 12 = 2
        # 下移超过八度
        assert transpose_note('C', -14) == 'A#'  # -14 % 12 = 10


class TestChordDataClass:
    """Chord数据类测试"""
    
    def test_chord_properties(self):
        """测试和弦属性"""
        chord = build_chord('C', 'maj7')
        
        assert chord.root == 'C'
        assert chord.quality == 'maj7'
        assert chord.notes == ['C', 'E', 'G', 'B']
        assert chord.symbol == 'Cmaj7'
    
    def test_chord_equality(self):
        """测试和弦相等性"""
        chord1 = build_chord('C', 'major')
        chord2 = build_chord('C', 'major')
        
        # 数据类自动实现相等性比较
        assert chord1.root == chord2.root
        assert chord1.quality == chord2.quality
        assert chord1.notes == chord2.notes


def run_tests():
    """运行所有测试"""
    test_classes = [
        TestNoteConversion,
        TestIntervals,
        TestChords,
        TestScales,
        TestKeySignature,
        TestTransposition,
        TestRelativeKey,
        TestEnharmonic,
        TestDiatonic,
        TestParseChordSymbol,
        TestConvenienceFunctions,
        TestEdgeCases,
        TestChordDataClass,
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        instance = test_class()
        methods = [m for m in dir(instance) if m.startswith('test_')]
        
        for method in methods:
            total_tests += 1
            try:
                getattr(instance, method)()
                passed_tests += 1
                print(f"✓ {test_class.__name__}.{method}")
            except AssertionError as e:
                failed_tests += 1
                print(f"✗ {test_class.__name__}.{method}: {e}")
            except Exception as e:
                failed_tests += 1
                print(f"✗ {test_class.__name__}.{method}: {type(e).__name__}: {e}")
    
    print(f"\n{'='*60}")
    print(f"测试结果: {passed_tests}/{total_tests} 通过")
    if failed_tests > 0:
        print(f"失败: {failed_tests}")
    print(f"{'='*60}")
    
    return failed_tests == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)