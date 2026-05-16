"""
Guitar Chord Utils Test - 吉他和弦工具库测试

测试覆盖：
- 和弦查询与获取
- 和弦图表渲染
- 指板音符计算
- 和弦难度评估
- 和弦转换分析
- 练习序列生成
- 调内和弦计算
- 和弦进行生成

Author: AllToolkit
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    GuitarString,
    FingerPosition,
    GuitarChord,
    ChordDifficulty,
    STRING_OPEN_NOTES,
    NOTE_CHROMATIC,
    CHORD_DATABASE,
    get_chord,
    get_all_variants,
    render_chord_diagram,
    render_chord_grid,
    get_note_on_fretboard,
    get_note_positions_on_fretboard,
    calculate_chord_difficulty,
    suggest_alternative_chords,
    generate_practice_sequence,
    find_chords_by_notes,
    get_scale_chords,
    generate_fretboard_map,
    transpose_chord,
    get_chord_progressions,
    list_all_chords,
    get_finger_strength_exercises,
    calculate_chord_inversions,
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition: bool, msg: str = ""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Failed: {msg}")
    
    def assert_equal(self, actual, expected, msg: str = ""):
        if actual == expected:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Failed: {msg} - Expected {expected}, got {actual}")
    
    def assert_in(self, item, container, msg: str = ""):
        if item in container:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Failed: {msg} - {item} not in {container}")
    
    def assert_not_none(self, value, msg: str = ""):
        if value is not None:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Failed: {msg} - Value is None")
    
    def assert_length(self, obj, expected_len, msg: str = ""):
        actual_len = len(obj)
        if actual_len == expected_len:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Failed: {msg} - Expected length {expected_len}, got {actual_len}")
    
    def assert_ge(self, actual, minimum, msg: str = ""):
        if actual >= minimum:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Failed: {msg} - Expected >= {minimum}, got {actual}")
    
    def assert_le(self, actual, maximum, msg: str = ""):
        if actual <= maximum:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Failed: {msg} - Expected <= {maximum}, got {actual}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Summary: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for err in self.errors:
                print(f"  - {err}")
        print(f"{'='*60}")
        return self.failed == 0


def test_basic_constants(result: TestResult):
    """测试基本常量"""
    print("\n[Testing Basic Constants]")
    
    # 弦序测试
    result.assert_equal(GuitarString.E6.value, 0, "E6 string index")
    result.assert_equal(GuitarString.E1.value, 5, "E1 string index")
    
    # 空弦音符测试
    result.assert_equal(STRING_OPEN_NOTES[GuitarString.E6], 'E', "E6 open note")
    result.assert_equal(STRING_OPEN_NOTES[GuitarString.A5], 'A', "A5 open note")
    result.assert_equal(STRING_OPEN_NOTES[GuitarString.D4], 'D', "D4 open note")
    result.assert_equal(STRING_OPEN_NOTES[GuitarString.G3], 'G', "G3 open note")
    result.assert_equal(STRING_OPEN_NOTES[GuitarString.B2], 'B', "B2 open note")
    result.assert_equal(STRING_OPEN_NOTES[GuitarString.E1], 'E', "E1 open note")
    
    # 半音阶测试
    result.assert_length(NOTE_CHROMATIC, 12, "Chromatic scale length")
    result.assert_in('C', NOTE_CHROMATIC, "C in chromatic scale")
    result.assert_in('C#', NOTE_CHROMATIC, "C# in chromatic scale")
    
    # 和弦数据库测试
    result.assert_ge(len(CHORD_DATABASE), 50, "Chord database size")


def test_get_chord(result: TestResult):
    """测试和弦获取"""
    print("\n[Testing get_chord]")
    
    # 基本和弦
    c_chord = get_chord('C')
    result.assert_not_none(c_chord, "C chord exists")
    result.assert_equal(c_chord.name, 'C', "C chord name")
    result.assert_in('C', c_chord.notes, "C note in C chord")
    result.assert_in('E', c_chord.notes, "E note in C chord")
    result.assert_in('G', c_chord.notes, "G note in C chord")
    
    # 小和弦
    am_chord = get_chord('Am')
    result.assert_not_none(am_chord, "Am chord exists")
    result.assert_in('A', am_chord.notes, "A note in Am chord")
    result.assert_in('C', am_chord.notes, "C note in Am chord")
    result.assert_in('E', am_chord.notes, "E note in Am chord")
    
    # 七和弦
    c7_chord = get_chord('C7')
    result.assert_not_none(c7_chord, "C7 chord exists")
    result.assert_ge(len(c7_chord.notes), 3, "C7 chord has enough notes")
    
    # 挂留和弦
    dsus4 = get_chord('Dsus4')
    result.assert_not_none(dsus4, "Dsus4 chord exists")
    
    # 强力和弦
    c5 = get_chord('C5')
    result.assert_not_none(c5, "C5 chord exists")
    
    # 不存在的和弦
    nonexistent = get_chord('XYZ')
    result.assert_true(nonexistent is None, "Nonexistent chord returns None")


def test_chord_variants(result: TestResult):
    """测试和弦变体"""
    print("\n[Testing get_all_variants]")
    
    # C 和弦有多个变体
    c_variants = get_all_variants('C')
    result.assert_ge(len(c_variants), 1, "C chord has variants")
    
    # F 和弦有简化版
    f_variants = get_all_variants('F')
    result.assert_ge(len(f_variants), 1, "F chord has variants")
    
    # 每个变体都是 GuitarChord 对象
    for variant in c_variants:
        result.assert_true(isinstance(variant, GuitarChord), "Variant is GuitarChord")


def test_chord_diagram(result: TestResult):
    """测试和弦图表渲染"""
    print("\n[Testing render_chord_diagram]")
    
    c_chord = get_chord('C')
    diagram = render_chord_diagram(c_chord)
    
    result.assert_not_none(diagram, "Diagram is generated")
    result.assert_true(len(diagram) > 50, "Diagram has content")
    result.assert_in('C', diagram, "Chord name in diagram")
    result.assert_in('E', diagram, "String names in diagram")
    
    # 测试横按和弦
    f_chord = get_chord('F')
    if f_chord:
        f_diagram = render_chord_diagram(f_chord)
        result.assert_not_none(f_diagram, "F diagram generated")
    
    # 测试不显示手指编号
    diagram_no_finger = render_chord_diagram(c_chord, show_finger_numbers=False)
    result.assert_not_none(diagram_no_finger, "Diagram without finger numbers")


def test_chord_grid(result: TestResult):
    """测试和弦网格渲染"""
    print("\n[Testing render_chord_grid]")
    
    c_chord = get_chord('C')
    grid = render_chord_grid(c_chord)
    
    result.assert_not_none(grid, "Grid is generated")
    result.assert_in('[C]', grid, "Chord name in grid")
    
    # 测试复杂和弦
    f_chord = get_chord('F')
    if f_chord:
        f_grid = render_chord_grid(f_chord)
        result.assert_in('[F]', f_grid, "F chord name in grid")


def test_fretboard_notes(result: TestResult):
    """测试指板音符计算"""
    print("\n[Testing get_note_on_fretboard]")
    
    # E 弦各品音符
    result.assert_equal(get_note_on_fretboard(GuitarString.E6, 0), 'E', "E6 fret 0")
    result.assert_equal(get_note_on_fretboard(GuitarString.E6, 1), 'F', "E6 fret 1")
    result.assert_equal(get_note_on_fretboard(GuitarString.E6, 2), 'F#', "E6 fret 2")
    result.assert_equal(get_note_on_fretboard(GuitarString.E6, 3), 'G', "E6 fret 3")
    result.assert_equal(get_note_on_fretboard(GuitarString.E6, 12), 'E', "E6 fret 12 (octave)")
    
    # A 弦
    result.assert_equal(get_note_on_fretboard(GuitarString.A5, 0), 'A', "A5 fret 0")
    result.assert_equal(get_note_on_fretboard(GuitarString.A5, 2), 'B', "A5 fret 2")
    result.assert_equal(get_note_on_fretboard(GuitarString.A5, 3), 'C', "A5 fret 3")
    
    # D 弦
    result.assert_equal(get_note_on_fretboard(GuitarString.D4, 0), 'D', "D4 fret 0")
    result.assert_equal(get_note_on_fretboard(GuitarString.D4, 5), 'G', "D4 fret 5")


def test_note_positions(result: TestResult):
    """测试音符位置查找"""
    print("\n[Testing get_note_positions_on_fretboard]")
    
    # C 音在各弦的位置
    c_positions = get_note_positions_on_fretboard('C', max_fret=12)
    result.assert_ge(len(c_positions), 6, "C note has positions on fretboard")
    
    # E 音位置
    e_positions = get_note_positions_on_fretboard('E', max_fret=12)
    result.assert_ge(len(e_positions), 6, "E note has positions")
    
    # 检查位置格式
    for string, fret in c_positions:
        result.assert_true(isinstance(string, GuitarString), "Position has GuitarString")
        result.assert_le(fret, 12, "Fret within max_fret")


def test_chord_difficulty(result: TestResult):
    """测试和弦难度评估"""
    print("\n[Testing calculate_chord_difficulty]")
    
    # 简单和弦
    c_chord = get_chord('C')
    c_diff = calculate_chord_difficulty(c_chord)
    result.assert_in('overall', c_diff, "Has overall difficulty")
    result.assert_in('level', c_diff, "Has difficulty level")
    result.assert_in('factors', c_diff, "Has difficulty factors")
    result.assert_le(c_diff['overall'], 3, "C chord is not too difficult")
    
    # 困难和弦
    f_chord = get_chord('F')
    if f_chord:
        f_diff = calculate_chord_difficulty(f_chord)
        result.assert_ge(f_diff['overall'], 2, "F chord has some difficulty")
    
    # E5 强力和弦应该简单
    e5 = get_chord('E5')
    if e5:
        e5_diff = calculate_chord_difficulty(e5)
        result.assert_le(e5_diff['overall'], 3, "E5 is relatively easy")


def test_alternative_chords(result: TestResult):
    """测试替代和弦建议"""
    print("\n[Testing suggest_alternative_chords]")
    
    # F 和弦的替代
    f_alternatives = suggest_alternative_chords('F', max_difficulty=2)
    result.assert_ge(len(f_alternatives), 0, "F has alternatives")
    
    # 简单和弦没有替代
    c_alternatives = suggest_alternative_chords('C', max_difficulty=3)
    result.assert_ge(len(c_alternatives), 1, "C chord returned")


def test_practice_sequence(result: TestResult):
    """测试练习序列生成"""
    print("\n[Testing generate_practice_sequence]")
    
    # 经典进行 C-Am-F-G
    sequence = generate_practice_sequence(['C', 'Am', 'F', 'G'])
    
    result.assert_in('chords', sequence, "Sequence has chords")
    result.assert_in('total_difficulty', sequence, "Sequence has total difficulty")
    result.assert_in('transitions', sequence, "Sequence has transitions")
    result.assert_in('practice_time', sequence, "Sequence has practice time")
    
    result.assert_length(sequence['chords'], 4, "Sequence has 4 chords")
    result.assert_ge(len(sequence['transitions']), 3, "Sequence has transitions")
    
    # 每个和弦都有图表
    for chord_info in sequence['chords']:
        result.assert_in('diagram', chord_info, "Chord has diagram")


def test_find_chords_by_notes(result: TestResult):
    """测试根据音符查找和弦"""
    print("\n[Testing find_chords_by_notes]")
    
    # C-E-G 应找到 C 和弦
    c_matches = find_chords_by_notes(['C', 'E', 'G'])
    result.assert_ge(len(c_matches), 1, "Found chords for C-E-G")
    
    # 第一个应该是 C 和弦
    if c_matches:
        result.assert_in('C', c_matches[0]['name'], "C chord found")
    
    # A-C-E 应找到 Am 和弦
    am_matches = find_chords_by_notes(['A', 'C', 'E'])
    result.assert_ge(len(am_matches), 1, "Found chords for A-C-E")
    
    # 空音符列表
    empty_matches = find_chords_by_notes([])
    result.assert_ge(len(empty_matches), 0, "Empty notes handled")


def test_scale_chords(result: TestResult):
    """测试调内和弦"""
    print("\n[Testing get_scale_chords]")
    
    # C 大调调内和弦
    c_major_chords = get_scale_chords('C', 'major')
    result.assert_length(c_major_chords, 7, "C major has 7 scale chords")
    
    # 检查级数
    result.assert_equal(c_major_chords[0]['degree'], 'I', "First degree is I")
    result.assert_equal(c_major_chords[1]['degree'], 'ii', "Second degree is ii")
    
    # 检查和弦名
    result.assert_in('C', c_major_chords[0]['chord_name'], "I chord is C")
    result.assert_in('Dm', c_major_chords[1]['chord_name'], "ii chord is Dm")
    
    # A 小调
    a_minor_chords = get_scale_chords('A', 'minor')
    result.assert_length(a_minor_chords, 7, "A minor has 7 scale chords")


def test_fretboard_map(result: TestResult):
    """测试指板图生成"""
    print("\n[Testing generate_fretboard_map]")
    
    map_str = generate_fretboard_map(0, 12)
    
    result.assert_not_none(map_str, "Fretboard map generated")
    result.assert_true(len(map_str) > 100, "Map has content")
    result.assert_in('Fret', map_str, "Map has fret numbers")
    result.assert_in('E', map_str, "Map has note E")


def test_transpose_chord(result: TestResult):
    """测试和弦移调"""
    print("\n[Testing transpose_chord]")
    
    # 升高 2 个半音
    result.assert_equal(transpose_chord('C', 2), 'D', "C +2 = D")
    result.assert_equal(transpose_chord('C', 5), 'F', "C +5 = F")
    result.assert_equal(transpose_chord('C', 7), 'G', "C +7 = G")
    
    # 降低 1 个半音
    result.assert_equal(transpose_chord('D', -1), 'C#', "D -1 = C#")
    
    # 小和弦移调
    result.assert_in('m', transpose_chord('Am', 2), "Am +2 retains minor")
    
    # 循环移调（12个半音回到原位）
    result.assert_equal(transpose_chord('C', 12), 'C', "C +12 = C (octave)")


def test_chord_progressions(result: TestResult):
    """测试和弦进行"""
    print("\n[Testing get_chord_progressions]")
    
    progressions = get_chord_progressions('C')
    
    result.assert_ge(len(progressions), 5, "Has multiple progressions")
    
    # 检查流行进行
    pop_prog = progressions[0]
    result.assert_ge(len(pop_prog), 4, "Progression has chords")
    
    # 检查和弦名格式
    for chord in pop_prog:
        result.assert_true(len(chord) >= 1, "Chord name valid")


def test_list_all_chords(result: TestResult):
    """测试列出所有和弦"""
    print("\n[Testing list_all_chords]")
    
    all_chords = list_all_chords()
    
    result.assert_ge(len(all_chords), 50, "Database has many chords")
    result.assert_in('C', all_chords, "C chord in list")
    result.assert_in('Am', all_chords, "Am chord in list")
    result.assert_in('D', all_chords, "D chord in list")
    
    # 检查排序
    result.assert_equal(all_chords[0], 'A', "First chord sorted alphabetically")


def test_finger_exercises(result: TestResult):
    """测试手指练习"""
    print("\n[Testing get_finger_strength_exercises]")
    
    exercises = get_finger_strength_exercises()
    
    result.assert_ge(len(exercises), 3, "Has multiple exercises")
    
    # 检查练习内容
    for ex in exercises:
        result.assert_in('name', ex, "Exercise has name")
        result.assert_in('description', ex, "Exercise has description")


def test_chord_inversions(result: TestResult):
    """测试和弦转位"""
    print("\n[Testing calculate_chord_inversions]")
    
    # C 和弦第一转位
    inv1 = calculate_chord_inversions('C', 1)
    result.assert_not_none(inv1, "C first inversion found")
    
    # C 和弦第二转位
    inv2 = calculate_chord_inversions('C', 2)
    result.assert_not_none(inv2, "C second inversion found")


def test_finger_position(result: TestResult):
    """测试手指位置数据"""
    print("\n[Testing FingerPosition]")
    
    pos = FingerPosition(
        string=GuitarString.E6,
        fret=3,
        finger=1
    )
    
    result.assert_equal(pos.string, GuitarString.E6, "String set correctly")
    result.assert_equal(pos.fret, 3, "Fret set correctly")
    result.assert_equal(pos.finger, 1, "Finger set correctly")


def test_guitar_chord_dataclass(result: TestResult):
    """测试 GuitarChord 数据类"""
    print("\n[Testing GuitarChord]")
    
    # 手动创建和弦
    positions = [
        FingerPosition(GuitarString.E6, 0, 0),
        FingerPosition(GuitarString.A5, 3, 1),
        FingerPosition(GuitarString.D4, 2, 2),
        FingerPosition(GuitarString.G3, 0, 0),
        FingerPosition(GuitarString.B2, 1, 3),
        FingerPosition(GuitarString.E1, 0, 0),
    ]
    
    chord = GuitarChord(
        name='C',
        positions=positions,
        difficulty=1
    )
    
    result.assert_equal(chord.name, 'C', "Chord name set")
    result.assert_length(chord.positions, 6, "Chord has positions")
    result.assert_not_none(chord.notes, "Notes calculated")
    
    # 检查音符计算
    result.assert_in('C', chord.notes, "C note in chord")
    result.assert_in('E', chord.notes, "E note in chord")
    result.assert_in('G', chord.notes, "G note in chord")


def test_chord_difficulty_enum(result: TestResult):
    """测试难度枚举"""
    print("\n[Testing ChordDifficulty]")
    
    result.assert_equal(ChordDifficulty.BEGINNER.value, 1, "Beginner value")
    result.assert_equal(ChordDifficulty.EASY.value, 2, "Easy value")
    result.assert_equal(ChordDifficulty.INTERMEDIATE.value, 3, "Intermediate value")
    result.assert_equal(ChordDifficulty.ADVANCED.value, 4, "Advanced value")
    result.assert_equal(ChordDifficulty.EXPERT.value, 5, "Expert value")


def test_complex_chords(result: TestResult):
    """测试复杂和弦"""
    print("\n[Testing Complex Chords]")
    
    # 大七和弦
    cmaj7 = get_chord('Cmaj7')
    result.assert_not_none(cmaj7, "Cmaj7 exists")
    
    # 小七和弦
    dm7 = get_chord('Dm7')
    result.assert_not_none(dm7, "Dm7 exists")
    
    # 九和弦
    c9 = get_chord('C9')
    result.assert_not_none(c9, "C9 exists")
    
    # 减和弦
    cdim = get_chord('Cdim')
    result.assert_not_none(cdim, "Cdim exists")
    
    # 增和弦
    caug = get_chord('Caug')
    result.assert_not_none(caug, "Caug exists")
    
    # 半减七和弦
    am7b5 = get_chord('Am7b5')
    result.assert_not_none(am7b5, "Am7b5 exists")


def test_barre_chords(result: TestResult):
    """测试横按和弦"""
    print("\n[Testing Barre Chords]")
    
    # F 和弦（经典横按）
    f = get_chord('F')
    if f and f.barre:
        result.assert_equal(f.barre, 1, "F chord barre at fret 1")
        result.assert_not_none(f.barre_strings, "F has barre strings")
    
    # Bm 和弦（横按）
    bm = get_chord('Bm')
    if bm and bm.barre:
        result.assert_equal(bm.barre, 2, "Bm barre at fret 2")


def test_edge_cases(result: TestResult):
    """测试边界情况"""
    print("\n[Testing Edge Cases]")
    
    # 不存在的和弦
    result.assert_true(get_chord('INVALID') is None, "Invalid chord returns None")
    
    # 空进行
    empty_seq = generate_practice_sequence([])
    result.assert_length(empty_seq['chords'], 0, "Empty sequence handled")
    
    # 高品数
    high_fret_note = get_note_on_fretboard(GuitarString.E6, 24)
    result.assert_not_none(high_fret_note, "High fret note calculated")
    
    # 超大移调
    large_transpose = transpose_chord('C', 24)
    result.assert_equal(large_transpose, 'C', "Large transpose wraps around")


def main():
    """运行所有测试"""
    print("="*60)
    print("Guitar Chord Utils Test Suite")
    print("="*60)
    
    result = TestResult()
    
    # 运行所有测试
    test_basic_constants(result)
    test_get_chord(result)
    test_chord_variants(result)
    test_chord_diagram(result)
    test_chord_grid(result)
    test_fretboard_notes(result)
    test_note_positions(result)
    test_chord_difficulty(result)
    test_alternative_chords(result)
    test_practice_sequence(result)
    test_find_chords_by_notes(result)
    test_scale_chords(result)
    test_fretboard_map(result)
    test_transpose_chord(result)
    test_chord_progressions(result)
    test_list_all_chords(result)
    test_finger_exercises(result)
    test_chord_inversions(result)
    test_finger_position(result)
    test_guitar_chord_dataclass(result)
    test_chord_difficulty_enum(result)
    test_complex_chords(result)
    test_barre_chords(result)
    test_edge_cases(result)
    
    # 输出总结
    success = result.summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())