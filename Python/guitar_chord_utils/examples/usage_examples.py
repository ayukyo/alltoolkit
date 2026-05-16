"""
Guitar Chord Utils - 使用示例

展示吉他和弦工具库的各种功能：
1. 基本和弦查询
2. 和弦图表渲染
3. 指板音符计算
4. 和弦难度评估
5. 练习序列生成
6. 调内和弦分析
7. 和弦进行生成

Author: AllToolkit
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    GuitarString,
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
)


def example_basic_chords():
    """示例：基本和弦查询"""
    print("\n" + "="*60)
    print("Example 1: Basic Chord Lookup")
    print("="*60)
    
    # C 和弦
    c = get_chord('C')
    print(f"\nC Chord:")
    print(f"  Notes: {c.notes}")
    print(f"  Difficulty: {c.difficulty}")
    print(f"  Positions: {len(c.positions)} strings")
    
    # Am 和弦
    am = get_chord('Am')
    print(f"\nAm Chord:")
    print(f"  Notes: {am.notes}")
    print(f"  Difficulty: {am.difficulty}")
    
    # E 和弦
    e = get_chord('E')
    print(f"\nE Chord:")
    print(f"  Notes: {e.notes}")


def example_chord_diagrams():
    """示例：和弦图表渲染"""
    print("\n" + "="*60)
    print("Example 2: Chord Diagram Rendering")
    print("="*60)
    
    # C 和弦详细图表
    c = get_chord('C')
    print("\nC Chord - Full Diagram:")
    print(render_chord_diagram(c, frets_to_show=5))
    
    # Am 和弦详细图表
    am = get_chord('Am')
    print("\nAm Chord - Full Diagram:")
    print(render_chord_diagram(am))
    
    # F 和弦（带横按）
    f = get_chord('F')
    print("\nF Chord - Barre Chord:")
    print(render_chord_diagram(f))
    
    # 紧凑网格格式
    print("\nCompact Grid Format:")
    print(render_chord_grid(c))
    print(render_chord_grid(am))
    print(render_chord_grid(get_chord('G')))


def example_chord_variants():
    """示例：和弦变体"""
    print("\n" + "="*60)
    print("Example 3: Chord Variants")
    print("="*60)
    
    # C 和弦的所有变体
    c_variants = get_all_variants('C')
    print(f"\nC chord has {len(c_variants)} playing positions:")
    
    for i, variant in enumerate(c_variants):
        diff = calculate_chord_difficulty(variant)
        print(f"\nVariant {i+1} (Difficulty: {diff['overall']}/5 - {diff['level']})")
        print(render_chord_grid(variant))
    
    # F 和弦变体（简化版）
    f_variants = get_all_variants('F')
    print(f"\nF chord has {len(f_variants)} variants:")
    for i, v in enumerate(f_variants):
        print(f"  Variant {i+1}: Difficulty {v.difficulty}")


def example_fretboard_notes():
    """示例：指板音符计算"""
    print("\n" + "="*60)
    print("Example 4: Fretboard Note Calculation")
    print("="*60)
    
    # E 弦前5品音符
    print("\nE6 String (Low E) - First 5 frets:")
    for fret in range(6):
        note = get_note_on_fretboard(GuitarString.E6, fret)
        print(f"  Fret {fret}: {note}")
    
    # A 張前5品音符
    print("\nA5 String - First 5 frets:")
    for fret in range(6):
        note = get_note_on_fretboard(GuitarString.A5, fret)
        print(f"  Fret {fret}: {note}")
    
    # 查找 C 音的所有位置
    print("\nAll positions of C note (frets 0-12):")
    c_positions = get_note_positions_on_fretboard('C', max_fret=12)
    for string, fret in c_positions:
        string_name = ['E6', 'A5', 'D4', 'G3', 'B2', 'E1'][string.value]
        print(f"  {string_name} string, fret {fret}")
    
    # 指板图
    print("\nFull Fretboard Map (0-12 frets):")
    print(generate_fretboard_map(0, 12))


def example_chord_difficulty():
    """示例：和弦难度评估"""
    print("\n" + "="*60)
    print("Example 5: Chord Difficulty Assessment")
    print("="*60)
    
    # 评估常见和弦难度
    chords_to_check = ['C', 'D', 'E', 'Am', 'Em', 'F', 'Bm', 'G', 'A', 'E5']
    
    print("\nDifficulty ratings:")
    for name in chords_to_check:
        chord = get_chord(name)
        if chord:
            diff = calculate_chord_difficulty(chord)
            print(f"\n{name}: {diff['overall']}/5 ({diff['level']})")
            print(f"  Factors: barre={diff['factors']['barre']}, "
                  f"stretch={diff['factors']['stretch']}, "
                  f"fingers={diff['factors']['finger_count']}")
            print(f"  Recommendation: {diff['recommendation']}")
    
    # F 和弦的替代建议
    print("\nAlternative suggestions for F chord (max difficulty 3):")
    alternatives = suggest_alternative_chords('F', max_difficulty=3)
    for alt in alternatives:
        print(f"  {alt.name} (difficulty {alt.difficulty})")


def example_practice_sequence():
    """示例：练习序列生成"""
    print("\n" + "="*60)
    print("Example 6: Practice Sequence Generation")
    print("="*60)
    
    # 经典 C-Am-F-G 进行
    print("\nPractice sequence for C-Am-F-G:")
    sequence = generate_practice_sequence(['C', 'Am', 'F', 'G'])
    
    print(f"\nTotal difficulty: {sequence['total_difficulty']}")
    print(f"Practice time: {sequence['practice_time']}")
    
    print("\nChords in sequence:")
    for chord_info in sequence['chords']:
        print(f"\n{chord_info['name']} (difficulty {chord_info['difficulty']})")
        print(chord_info['diagram'])
    
    print("\nTransition analysis:")
    for transition in sequence['transitions']:
        print(f"  {transition['from']} -> {transition['to']}: "
              f"difficulty {transition['difficulty']}/5")
        for move in transition['moves']:
            print(f"    Finger {move['finger']}: {move['from']} to {move['to']}")


def example_find_chords():
    """示例：根据音符查找和弦"""
    print("\n" + "="*60)
    print("Example 7: Find Chords by Notes")
    print("="*60)
    
    # C-E-G 应找到 C 和弦
    print("\nFinding chords containing C, E, G:")
    matches = find_chords_by_notes(['C', 'E', 'G'])
    for match in matches[:5]:
        print(f"  {match['name']}: match ratio {match['match_ratio']}, "
              f"notes {match['all_notes']}")
    
    # A-C-E 应找到 Am
    print("\nFinding chords containing A, C, E:")
    matches = find_chords_by_notes(['A', 'C', 'E'])
    for match in matches[:5]:
        print(f"  {match['name']}: match ratio {match['match_ratio']}")


def example_scale_chords():
    """示例：调内和弦"""
    print("\n" + "="*60)
    print("Example 8: Scale Chords (Key Chords)")
    print("="*60)
    
    # C 大调调内和弦
    print("\nC Major scale chords:")
    c_major = get_scale_chords('C', 'major')
    for chord_info in c_major:
        print(f"  {chord_info['degree']}: {chord_info['chord_name']} "
              f"(notes: {chord_info['notes']})")
    
    # A 小调调内和弦
    print("\nA Minor scale chords:")
    a_minor = get_scale_chords('A', 'minor')
    for chord_info in a_minor:
        print(f"  {chord_info['degree']}: {chord_info['chord_name']}")


def example_transpose():
    """示例：和弦移调"""
    print("\n" + "="*60)
    print("Example 9: Chord Transposition")
    print("="*60)
    
    # 常用移调
    print("\nTransposing chords:")
    
    # C 调移到 D 调（+2 半音）
    print("\nC -> D (+2 semitones):")
    c_chords = ['C', 'Am', 'F', 'G']
    for chord in c_chords:
        transposed = transpose_chord(chord, 2)
        print(f"  {chord} -> {transposed}")
    
    # C 调移到 G 调（+7 半音）
    print("\nC -> G (+7 semitones):")
    for chord in c_chords:
        transposed = transpose_chord(chord, 7)
        print(f"  {chord} -> {transposed}")


def example_progressions():
    """示例：和弦进行"""
    print("\n" + "="*60)
    print("Example 10: Common Chord Progressions")
    print("="*60)
    
    # C 调常用进行
    print("\nCommon progressions in C:")
    progressions = get_chord_progressions('C')
    
    prog_names = [
        "Pop progression (I-V-vi-IV)",
        "Classic progression (I-IV-V-I)",
        "Pop variation (I-vi-IV-V)",
        "Jazz progression (ii-V-I)",
        "Canon progression",
        "Minor start (vi-IV-I-V)",
        "Rock progression",
        "Simple progression",
    ]
    
    for i, prog in enumerate(progressions):
        name = prog_names[i] if i < len(prog_names) else f"Progression {i+1}"
        print(f"\n{name}:")
        print(f"  {' - '.join(prog)}")


def example_list_chords():
    """示例：列出所有和弦"""
    print("\n" + "="*60)
    print("Example 11: List All Available Chords")
    print("="*60)
    
    all_chords = list_all_chords()
    print(f"\nTotal chords in database: {len(all_chords)}")
    
    # 分类显示
    print("\nMajor chords:")
    majors = [c for c in all_chords if not c.endswith('m') and 
              not c.endswith('7') and 'dim' not in c and 'aug' not in c and
              'sus' not in c and 'add' not in c and c[-1].isdigit()]
    print(f"  {', '.join(majors[:15])}...")
    
    print("\nMinor chords:")
    minors = [c for c in all_chords if c.endswith('m') and not c.endswith('m7') and 
              not c.endswith('dim') and 'm7b5' not in c]
    print(f"  {', '.join(minors[:15])}...")
    
    print("\n7th chords:")
    sevenths = [c for c in all_chords if c.endswith('7') or c.endswith('m7') or 
                'maj7' in c or 'm7b5' in c]
    print(f"  {', '.join(sevenths[:15])}...")
    
    print("\nPower chords (5):")
    power = [c for c in all_chords if c.endswith('5')]
    print(f"  {', '.join(power)}")


def example_exercises():
    """示例：手指练习"""
    print("\n" + "="*60)
    print("Example 12: Finger Strength Exercises")
    print("="*60)
    
    exercises = get_finger_strength_exercises()
    
    for ex in exercises:
        print(f"\n{ex['name']}:")
        print(f"  Description: {ex['description']}")
        if 'chords' in ex:
            print(f"  Chords: {', '.join(ex['chords'])}")
        print(f"  Duration: {ex['duration']}")


def example_comprehensive():
    """综合示例：完整练习计划"""
    print("\n" + "="*60)
    print("Example 13: Comprehensive Practice Plan")
    print("="*60)
    
    # 生成完整练习计划
    chords = ['C', 'Am', 'Dm', 'G', 'Em', 'F']
    
    print(f"\nPractice chords: {', '.join(chords)}")
    
    # 获取所有和弦信息
    print("\nChord diagrams:")
    for name in chords:
        chord = get_chord(name)
        if chord:
            diff = calculate_chord_difficulty(chord)
            print(f"\n{name} (difficulty {diff['overall']}/5):")
            print(render_chord_grid(chord))
    
    # 生成练习序列
    sequence = generate_practice_sequence(chords)
    
    print(f"\nTotal practice difficulty: {sequence['total_difficulty']}")
    print(f"Recommended practice time: {sequence['practice_time']}")
    
    # 显示练习建议
    print("\nPractice suggestions:")
    for suggestion in sequence['suggestions']:
        print(f"  - {suggestion}")
    
    # 相关和弦进行
    print("\nRelated chord progressions in C:")
    progressions = get_chord_progressions('C')[:3]
    for prog in progressions:
        print(f"  {' -> '.join(prog)}")


def main():
    """运行所有示例"""
    print("="*60)
    print("Guitar Chord Utils - Usage Examples")
    print("="*60)
    
    example_basic_chords()
    example_chord_diagrams()
    example_chord_variants()
    example_fretboard_notes()
    example_chord_difficulty()
    example_practice_sequence()
    example_find_chords()
    example_scale_chords()
    example_transpose()
    example_progressions()
    example_list_chords()
    example_exercises()
    example_comprehensive()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()