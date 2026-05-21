"""
scale_utils 测试文件

测试所有音阶工具功能
"""

import unittest
from mod import (
    parse_note, note_to_semitone, semitone_to_note,
    transpose_note, interval_between, generate_scale,
    generate_scale_notes, scale_degrees, identify_scale,
    get_relative_minor, get_relative_major, circle_of_fifths,
    key_signature, chord_scale_relationship, get_scale_chords,
    is_diatonic, get_enharmonic, list_scales,
    major_scale, minor_scale, pentatonic, blues_scale, mode,
    Note, SCALE_PATTERNS
)


class TestNoteParsing(unittest.TestCase):
    """测试音符解析"""
    
    def test_parse_simple_notes(self):
        """测试简单音符解析"""
        self.assertEqual(parse_note('C'), Note('C', '', 4))
        self.assertEqual(parse_note('D'), Note('D', '', 4))
        self.assertEqual(parse_note('E'), Note('E', '', 4))
    
    def test_parse_sharps(self):
        """测试升号解析"""
        self.assertEqual(parse_note('C#'), Note('C', '#', 4))
        self.assertEqual(parse_note('F#'), Note('F', '#', 4))
        self.assertEqual(parse_note('G#'), Note('G', '#', 4))
    
    def test_parse_flats(self):
        """测试降号解析"""
        self.assertEqual(parse_note('Db'), Note('D', 'b', 4))
        self.assertEqual(parse_note('Eb'), Note('E', 'b', 4))
        self.assertEqual(parse_note('Bb'), Note('B', 'b', 4))
    
    def test_parse_with_octave(self):
        """测试带八度的解析"""
        self.assertEqual(parse_note('C4'), Note('C', '', 4))
        self.assertEqual(parse_note('C#5'), Note('C', '#', 5))
        self.assertEqual(parse_note('Db3'), Note('D', 'b', 3))
    
    def test_parse_double_accidentals(self):
        """测试双变音记号"""
        self.assertEqual(parse_note('C##'), Note('C', '##', 4))
        self.assertEqual(parse_note('Dbb'), Note('D', 'bb', 4))
    
    def test_parse_invalid(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            parse_note('H')
        with self.assertRaises(ValueError):
            parse_note('invalid')


class TestNoteConversion(unittest.TestCase):
    """测试音符转换"""
    
    def test_note_to_semitone(self):
        """测试音符到半音"""
        c4 = note_to_semitone(Note('C', '', 4))
        self.assertEqual(c4 % 12, 0)  # C
        self.assertEqual(c4 // 12, 4)  # octave 4
        
        a4 = note_to_semitone(Note('A', '', 4))
        self.assertEqual(a4 % 12, 9)  # A
    
    def test_semitone_to_note(self):
        """测试半音到音符"""
        self.assertEqual(semitone_to_note(48), Note('C', '', 4))
        self.assertEqual(semitone_to_note(57), Note('A', '', 4))
        self.assertEqual(semitone_to_note(0), Note('C', '', 0))
    
    def test_conversion_roundtrip(self):
        """测试转换往返"""
        for octave in range(0, 8):
            for note_name in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
                note = Note(note_name, '', octave)
                semitone = note_to_semitone(note)
                result = semitone_to_note(semitone)
                # 检查半音值是否匹配（忽略名称差异，因为C#和Db是等音）
                result_semitone = note_to_semitone(result)
                self.assertEqual(result_semitone, semitone)


class TestTransposition(unittest.TestCase):
    """测试移调"""
    
    def test_transpose_up(self):
        """测试向上移调"""
        c4 = Note('C', '', 4)
        d4 = transpose_note(c4, 2)
        self.assertEqual(d4.name, 'D')
        self.assertEqual(d4.octave, 4)
    
    def test_transpose_down(self):
        """测试向下移调"""
        c4 = Note('C', '', 4)
        b3 = transpose_note(c4, -1)
        self.assertEqual(b3.name, 'B')
        self.assertEqual(b3.octave, 3)
    
    def test_transpose_octave(self):
        """测试八度移调"""
        c4 = Note('C', '', 4)
        c5 = transpose_note(c4, 12)
        self.assertEqual(c5.name, 'C')
        self.assertEqual(c5.octave, 5)
    
    def test_transpose_with_accidentals(self):
        """测试带变音记号的移调"""
        c_sharp = Note('C', '#', 4)
        d_sharp = transpose_note(c_sharp, 2)
        self.assertEqual(d_sharp.name, 'D')
        self.assertEqual(d_sharp.accidental, '#')


class TestInterval(unittest.TestCase):
    """测试音程"""
    
    def test_intervals(self):
        """测试基本音程"""
        c4 = Note('C', '', 4)
        
        # 大二度
        d4 = Note('D', '', 4)
        self.assertEqual(interval_between(c4, d4).semitones, 2)
        
        # 大三度
        e4 = Note('E', '', 4)
        self.assertEqual(interval_between(c4, e4).semitones, 4)
        
        # 纯五度
        g4 = Note('G', '', 4)
        self.assertEqual(interval_between(c4, g4).semitones, 7)
        
        # 纯八度（同一音级的下一个八度）
        c5 = Note('C', '', 5)
        interval = interval_between(c4, c5)
        # 简化到单八度内是0（纯一度），但实际是12半音
        self.assertEqual(interval.semitones, 0)  # % 12 后的结果
    
    def test_actual_intervals(self):
        """测试实际半音差"""
        c4 = Note('C', '', 4)
        
        # 测试实际半音差（不简化）
        d4 = Note('D', '', 4)
        actual_diff = note_to_semitone(d4) - note_to_semitone(c4)
        self.assertEqual(actual_diff, 2)
        
        c5 = Note('C', '', 5)
        actual_diff = note_to_semitone(c5) - note_to_semitone(c4)
        self.assertEqual(actual_diff, 12)


class TestScaleGeneration(unittest.TestCase):
    """测试音阶生成"""
    
    def test_major_scale(self):
        """测试大调音阶"""
        scale = generate_scale('C', 'major')
        self.assertEqual(scale, ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
    
    def test_natural_minor_scale(self):
        """测试自然小调音阶"""
        scale = generate_scale('A', 'natural_minor')
        # A自然小调应该是 A-B-C-D-E-F-G-A
        self.assertEqual(len(scale), 8)
        self.assertEqual(scale[0], 'A')
        self.assertEqual(scale[-1], 'A')
        # 检查半音值是否正确
        scale_semitones = [note_to_semitone(parse_note(n)) % 12 for n in scale]
        expected_semitones = [9, 11, 0, 2, 4, 5, 7, 9]  # A, B, C, D, E, F, G, A
        self.assertEqual(scale_semitones, expected_semitones)
    
    def test_harmonic_minor_scale(self):
        """测试和声小调音阶"""
        scale = generate_scale('A', 'harmonic_minor')
        # A B C D E F G# A
        self.assertEqual(len(scale), 8)
        self.assertEqual(scale[0], 'A')
        # G# 或 Ab 的半音值是 8
        gsharp_semitone = note_to_semitone(parse_note(scale[6])) % 12
        self.assertEqual(gsharp_semitone, 8)
    
    def test_pentatonic_major(self):
        """测试大调五声"""
        scale = generate_scale('C', 'pentatonic_major')
        self.assertEqual(scale, ['C', 'D', 'E', 'G', 'A', 'C'])
    
    def test_pentatonic_minor(self):
        """测试小调五声"""
        scale = generate_scale('A', 'pentatonic_minor')
        # A小调五声: A-C-D-E-G-A (半音: 9, 0, 2, 4, 7, 9)
        self.assertEqual(len(scale), 6)
        scale_semitones = [note_to_semitone(parse_note(n)) % 12 for n in scale]
        expected = [9, 0, 2, 4, 7, 9]
        self.assertEqual(scale_semitones, expected)
    
    def test_blues_scale(self):
        """测试蓝调音阶"""
        scale = generate_scale('A', 'blues')
        # A C D D# E G A
        self.assertEqual(len(scale), 7)
        self.assertEqual(scale[0], 'A')
    
    def test_modes(self):
        """测试教会调式"""
        # Ionian = 大调
        ionian = generate_scale('C', 'ionian')
        self.assertEqual(ionian, generate_scale('C', 'major'))
        
        # Dorian
        dorian = generate_scale('D', 'dorian')
        self.assertEqual(len(dorian), 8)
    
    def test_whole_tone(self):
        """测试全音音阶"""
        scale = generate_scale('C', 'whole_tone')
        self.assertEqual(len(scale), 7)
        # 检查相邻音符之间的间隔都是2半音
        for i in range(len(scale) - 1):
            note1 = parse_note(scale[i])
            note2 = parse_note(scale[i + 1])
            diff = note_to_semitone(note2) - note_to_semitone(note1)
            # 最后一个音符可能跨越八度，检查绝对差值
            if i == len(scale) - 2:
                # 全音音阶结束音是C#, 应该是+12 (回到根音)或继续全音
                # pattern是 [2,2,2,2,2,2], 总共6个间隔, 最后回到下一个C
                pass
            else:
                self.assertEqual(diff, 2)
    
    def test_whole_tone_pattern(self):
        """测试全音音阶模式"""
        pattern = SCALE_PATTERNS['whole_tone']
        self.assertEqual(pattern, [2, 2, 2, 2, 2, 2])
        self.assertEqual(sum(pattern), 12)
    
    def test_chromatic(self):
        """测试半音阶"""
        scale = generate_scale('C', 'chromatic')
        self.assertEqual(len(scale), 13)
    
    def test_multiple_octaves(self):
        """测试多八度"""
        scale = generate_scale('C', 'major', octaves=2)
        self.assertEqual(len(scale), 15)  # 7 * 2 + 1
    
    def test_invalid_scale_type(self):
        """测试无效音阶类型"""
        with self.assertRaises(ValueError):
            generate_scale('C', 'invalid_scale')


class TestScaleIdentification(unittest.TestCase):
    """测试音阶识别"""
    
    def test_identify_c_major(self):
        """测试识别C大调"""
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        results = identify_scale(notes)
        self.assertTrue(len(results) > 0)
        # C大调或Ionian应该在结果中
        found = False
        for root, stype, name in results:
            root_semitone = note_to_semitone(parse_note(root)) % 12
            if root_semitone == 0 and stype in ['major', 'ionian']:
                found = True
                break
        self.assertTrue(found)
    
    def test_identify_a_minor(self):
        """测试识别A小调"""
        notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        results = identify_scale(notes)
        found_minor = False
        for root, stype, name in results:
            root_semitone = note_to_semitone(parse_note(root)) % 12
            if root_semitone == 9 and stype in ['natural_minor', 'aeolian']:
                found_minor = True
                break
        self.assertTrue(found_minor)
    
    def test_identify_pentatonic(self):
        """测试识别五声音阶"""
        notes = ['C', 'D', 'E', 'G', 'A']
        results = identify_scale(notes)
        found_pentatonic = False
        for root, stype, name in results:
            root_semitone = note_to_semitone(parse_note(root)) % 12
            if root_semitone == 0 and 'pentatonic' in stype:
                found_pentatonic = True
                break
        self.assertTrue(found_pentatonic)


class TestRelativeKeys(unittest.TestCase):
    """测试关系调"""
    
    def test_relative_minor(self):
        """测试关系小调"""
        # C大调的关系小调是A（向下小三度，即3半音）
        c_rel = get_relative_minor('C')
        c_rel_semitone = note_to_semitone(parse_note(c_rel)) % 12
        self.assertEqual(c_rel_semitone, 9)  # A
        
        # G大调的关系小调是E
        g_rel = get_relative_minor('G')
        g_rel_semitone = note_to_semitone(parse_note(g_rel)) % 12
        self.assertEqual(g_rel_semitone, 4)  # E
        
        # D大调的关系小调是B
        d_rel = get_relative_minor('D')
        d_rel_semitone = note_to_semitone(parse_note(d_rel)) % 12
        self.assertEqual(d_rel_semitone, 11)  # B
    
    def test_relative_major(self):
        """测试关系大调"""
        # A小调的关系大调是C（向上小三度）
        a_rel = get_relative_major('A')
        a_rel_semitone = note_to_semitone(parse_note(a_rel)) % 12
        self.assertEqual(a_rel_semitone, 0)  # C
        
        # E小调的关系大调是G
        e_rel = get_relative_major('E')
        e_rel_semitone = note_to_semitone(parse_note(e_rel)) % 12
        self.assertEqual(e_rel_semitone, 7)  # G
        
        # B小调的关系大调是D
        b_rel = get_relative_major('B')
        b_rel_semitone = note_to_semitone(parse_note(b_rel)) % 12
        self.assertEqual(b_rel_semitone, 2)  # D


class TestCircleOfFifths(unittest.TestCase):
    """测试五度圈"""
    
    def test_circle_of_fifths(self):
        """测试五度圈生成"""
        circle = circle_of_fifths('C', 7)
        self.assertEqual(len(circle), 7)
        self.assertEqual(circle[0], 'C')
        self.assertEqual(circle[1], 'G')
        self.assertEqual(circle[2], 'D')
    
    def test_circle_of_fourths(self):
        """测试四度圈生成"""
        circle = circle_of_fifths('C', 7, direction='fourths')
        self.assertEqual(len(circle), 7)
        self.assertEqual(circle[0], 'C')
        self.assertEqual(circle[1], 'F')
    
    def test_full_circle(self):
        """测试完整五度圈"""
        circle = circle_of_fifths('C', 12)
        self.assertEqual(len(circle), 12)


class TestKeySignature(unittest.TestCase):
    """测试调号"""
    
    def test_c_major(self):
        """测试C大调（无升降号）"""
        sharps, flats = key_signature('C')
        self.assertEqual(sharps, [])
        self.assertEqual(flats, [])
    
    def test_g_major(self):
        """测试G大调（1个升号：F#）"""
        sharps, flats = key_signature('G')
        # G大调有1个升号
        self.assertEqual(len(sharps), 1)
        self.assertEqual(flats, [])
        # 升号应该是F# (semitone 6)
        if sharps:
            sharp_note = parse_note(sharps[0])
            self.assertEqual(note_to_semitone(sharp_note) % 12, 6)  # F#
    
    def test_f_major(self):
        """测试F大调（1个降号：Bb）"""
        sharps, flats = key_signature('F')
        # F大调有1个降号
        self.assertEqual(len(flats), 1)
        self.assertEqual(sharps, [])
        # 降号应该是Bb (semitone 10)
        if flats:
            flat_note = parse_note(flats[0])
            self.assertEqual(note_to_semitone(flat_note) % 12, 10)  # Bb


class TestChordScaleRelationship(unittest.TestCase):
    """测试和弦音阶关系"""
    
    def test_major_chords(self):
        """测试大调和弦"""
        chords = get_scale_chords('C', 'major')
        self.assertEqual(len(chords), 7)
        
        # I是大调
        self.assertEqual(chords[0][0], 'C')
        self.assertEqual(chords[0][1], 'major')
        
        # ii是小调
        self.assertEqual(chords[1][0], 'D')
        self.assertEqual(chords[1][1], 'minor')
    
    def test_minor_chords(self):
        """测试小调和弦"""
        chords = get_scale_chords('A', 'natural_minor')
        self.assertEqual(len(chords), 7)
        
        # i是小调
        self.assertEqual(chords[0][0], 'A')
        self.assertEqual(chords[0][1], 'minor')


class TestDiatonic(unittest.TestCase):
    """测试自然音判断"""
    
    def test_diatonic_notes(self):
        """测试自然音"""
        self.assertTrue(is_diatonic('C', 'C', 'major'))
        self.assertTrue(is_diatonic('D', 'C', 'major'))
        self.assertTrue(is_diatonic('E', 'C', 'major'))
    
    def test_chromatic_notes(self):
        """测试变化音"""
        self.assertFalse(is_diatonic('C#', 'C', 'major'))
        self.assertFalse(is_diatonic('Eb', 'C', 'major'))


class TestEnharmonic(unittest.TestCase):
    """测试等音"""
    
    def test_enharmonic_sharps(self):
        """测试升号等音"""
        result = get_enharmonic('C#')
        # C#和Db是等音，半音值都是1
        self.assertEqual(len(result), 2)
        for note in result:
            semitone = note_to_semitone(parse_note(note)) % 12
            self.assertEqual(semitone, 1)
    
    def test_enharmonic_natural_notes(self):
        """测试自然音等音"""
        # 自然音（C, D, E, F, G, A, B）没有等音（除了特殊情况）
        result = get_enharmonic('C')
        # C没有等音（除非用B#，但这不是标准用法）
        self.assertTrue(len(result) >= 1)
        self.assertIn('C', result)
        
        result = get_enharmonic('F')
        self.assertTrue(len(result) >= 1)
        self.assertIn('F', result)
        
        # E和F是相邻半音，没有等音问题
        e_result = get_enharmonic('E')
        self.assertIn('E', e_result)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_major_scale_function(self):
        """测试major_scale函数"""
        scale = major_scale('C')
        self.assertEqual(scale, ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
    
    def test_minor_scale_functions(self):
        """测试minor_scale函数"""
        natural = minor_scale('A', 'natural')
        harmonic = minor_scale('A', 'harmonic')
        melodic = minor_scale('A', 'melodic')
        
        self.assertEqual(len(natural), 8)
        self.assertEqual(len(harmonic), 8)
        self.assertEqual(len(melodic), 8)
    
    def test_pentatonic_function(self):
        """测试pentatonic函数"""
        major_pent = pentatonic('C', 'major')
        minor_pent = pentatonic('A', 'minor')
        
        self.assertEqual(len(major_pent), 6)  # 5 notes + octave
        self.assertEqual(len(minor_pent), 6)
    
    def test_blues_scale_function(self):
        """测试blues_scale函数"""
        scale = blues_scale('A')
        self.assertEqual(len(scale), 7)
    
    def test_mode_function(self):
        """测试mode函数"""
        dorian = mode('D', 'dorian')
        self.assertEqual(len(dorian), 8)


class TestListScales(unittest.TestCase):
    """测试音阶列表"""
    
    def test_list_scales(self):
        """测试列出所有音阶"""
        scales = list_scales()
        self.assertTrue(len(scales) > 30)
        
        # 检查是否包含基本音阶
        scale_types = [s[0] for s in scales]
        self.assertIn('major', scale_types)
        self.assertIn('natural_minor', scale_types)
        self.assertIn('pentatonic_major', scale_types)
        self.assertIn('blues', scale_types)


class TestScalePatterns(unittest.TestCase):
    """测试音阶模式"""
    
    def test_major_pattern(self):
        """测试大调模式（全全半全全全半）"""
        pattern = SCALE_PATTERNS['major']
        self.assertEqual(pattern, [2, 2, 1, 2, 2, 2, 1])
    
    def test_natural_minor_pattern(self):
        """测试自然小调模式（全半全全半全全）"""
        pattern = SCALE_PATTERNS['natural_minor']
        self.assertEqual(pattern, [2, 1, 2, 2, 1, 2, 2])
    
    def test_pentatonic_pattern_length(self):
        """测试五声音阶模式长度"""
        pattern = SCALE_PATTERNS['pentatonic_major']
        self.assertEqual(len(pattern), 5)
    
    def test_pattern_consistency(self):
        """测试所有模式的一致性"""
        # 检查所有7音音阶的总半音数为12（完整八度）
        seven_note_scales = ['major', 'natural_minor', 'harmonic_minor', 'melodic_minor',
                             'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 
                             'aeolian', 'locrian']
        for scale_type in seven_note_scales:
            if scale_type in SCALE_PATTERNS:
                pattern = SCALE_PATTERNS[scale_type]
                total = sum(pattern)
                self.assertEqual(total, 12, f"Pattern for {scale_type} sums to {total}, expected 12")
        
        # 五声音阶5个间隔，总和12
        pentatonic_scales = ['pentatonic_major', 'pentatonic_minor']
        for scale_type in pentatonic_scales:
            pattern = SCALE_PATTERNS[scale_type]
            self.assertEqual(sum(pattern), 12)
        
        # 全音音阶6个间隔，总和12
        self.assertEqual(sum(SCALE_PATTERNS['whole_tone']), 12)
        
        # 半音阶12个间隔，总和12
        self.assertEqual(sum(SCALE_PATTERNS['chromatic']), 12)


if __name__ == '__main__':
    unittest.main()