"""
scale_utils 使用示例

演示音阶工具库的各种功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scale_utils.mod import (
    parse_note, Note, note_to_semitone, semitone_to_note,
    transpose_note, interval_between, generate_scale, generate_scale_notes,
    identify_scale, get_relative_minor, get_relative_major,
    circle_of_fifths, key_signature,
    get_scale_chords, is_diatonic, get_enharmonic, list_scales,
    major_scale, minor_scale, pentatonic, blues_scale, mode,
    SCALE_PATTERNS, SCALE_NAMES_CN
)


def print_separator(title: str):
    """打印分隔符"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


def example_basic_notes():
    """基本音符操作"""
    print_separator("基本音符操作")
    
    # 解析音符
    print("解析音符:")
    notes = ['C', 'C#', 'Db', 'F#4', 'Bb5']
    for n in notes:
        parsed = parse_note(n)
        print(f"  {n} -> {parsed}")
    
    # 音符转换
    print("\n音符到半音:")
    for note_name in ['C4', 'A4', 'C5']:
        note = parse_note(note_name)
        semitone = note_to_semitone(note)
        print(f"  {note_name} -> {semitone}")
    
    # 移调
    print("\n移调:")
    c4 = Note('C', '', 4)
    print(f"  C4 + 2半音 = {transpose_note(c4, 2)}")
    print(f"  C4 + 7半音 = {transpose_note(c4, 7)}")
    print(f"  C4 - 1半音 = {transpose_note(c4, -1)}")
    
    # 音程
    print("\n音程:")
    pairs = [
        ('C', 'D'), ('C', 'E'), ('C', 'F'), ('C', 'G'),
        ('C', 'A'), ('C', 'B'), ('C', 'C5')
    ]
    for n1, n2 in pairs:
        note1 = parse_note(n1)
        note2 = parse_note(n2)
        interval = interval_between(note1, note2)
        print(f"  {n1} -> {n2}: {interval.name} ({interval.short_name})")


def example_major_scales():
    """大调音阶"""
    print_separator("大调音阶")
    
    keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F']
    for key in keys:
        scale = major_scale(key)
        print(f"{key}大调: {' - '.join(scale)}")


def example_minor_scales():
    """小调音阶"""
    print_separator("小调音阶")
    
    print("A自然小调: " + ' - '.join(minor_scale('A', 'natural')))
    print("A和声小调: " + ' - '.join(minor_scale('A', 'harmonic')))
    print("A旋律小调: " + ' - '.join(minor_scale('A', 'melodic')))


def example_pentatonic_scales():
    """五声音阶"""
    print_separator("五声音阶")
    
    print("C大调五声: " + ' - '.join(pentatonic('C', 'major')))
    print("A小调五声: " + ' - '.join(pentatonic('A', 'minor')))
    
    print("\nE大调五声: " + ' - '.join(pentatonic('E', 'major')))
    print("E小调五声: " + ' - '.join(pentatonic('E', 'minor')))


def example_blues_scales():
    """蓝调音阶"""
    print_separator("蓝调音阶")
    
    keys = ['A', 'E', 'G', 'C']
    for key in keys:
        scale = blues_scale(key)
        print(f"{key}蓝调: {' - '.join(scale)}")


def example_modes():
    """教会调式"""
    print_separator("教会调式")
    
    modes_list = [
        ('ionian', '伊奥尼亚（大调）'),
        ('dorian', '多利亚'),
        ('phrygian', '弗里吉亚'),
        ('lydian', '利底亚'),
        ('mixolydian', '混合利底亚'),
        ('aeolian', '爱奥利亚（自然小调）'),
        ('locrian', '洛克里亚'),
    ]
    
    for mode_name, mode_cn in modes_list:
        scale = mode('C', mode_name)
        print(f"{mode_cn}: {' - '.join(scale)}")


def example_exotic_scales():
    """异域/特殊音阶"""
    print_separator("异域音阶")
    
    exotic_scales = [
        ('hungarian_minor', '匈牙利小调'),
        ('spanish_gypsy', '西班牙吉普赛'),
        ('japanese_hirajoshi', '日本平调子'),
        ('whole_tone', '全音音阶'),
        ('diminished_half', '减音阶（半全）'),
        ('augmented', '增音阶'),
    ]
    
    for scale_type, scale_name in exotic_scales:
        scale = generate_scale('C', scale_type)
        print(f"{scale_name}: {' - '.join(scale)}")


def example_scale_identification():
    """音阶识别"""
    print_separator("音阶识别")
    
    examples = [
        (['C', 'D', 'E', 'F', 'G', 'A', 'B'], 'C D E F G A B'),
        (['A', 'B', 'C', 'D', 'E', 'F', 'G'], 'A B C D E F G'),
        (['C', 'D', 'E', 'G', 'A'], 'C D E G A'),
        (['A', 'C', 'D', 'D#', 'E', 'G'], 'A C D D# E G'),
        (['C', 'D', 'E', 'F#', 'G', 'A', 'B'], 'C D E F# G A B'),
    ]
    
    for notes, desc in examples:
        results = identify_scale(notes)
        print(f"\n音符: {desc}")
        print("可能的音阶:")
        for root, stype, name in results[:5]:
            print(f"  - {root} {name}")


def example_relative_keys():
    """关系调"""
    print_separator("关系调")
    
    print("大调的关系小调:")
    major_keys = ['C', 'G', 'D', 'A', 'E', 'F', 'Bb']
    for key in major_keys:
        relative_minor = get_relative_minor(key)
        print(f"  {key}大调 -> {relative_minor}小调")
    
    print("\n小调的关系大调:")
    minor_keys = ['A', 'E', 'B', 'F#', 'C#', 'D', 'G']
    for key in minor_keys:
        relative_major = get_relative_major(key)
        print(f"  {key}小调 -> {relative_major}大调")


def example_circle_of_fifths():
    """五度圈"""
    print_separator("五度圈")
    
    print("五度圈（顺时针）:")
    fifths = circle_of_fifths('C', 12)
    print(' -> '.join(fifths))
    
    print("\n四度圈（逆时针）:")
    fourths = circle_of_fifths('C', 12, direction='fourths')
    print(' -> '.join(fourths))
    
    print("\n从不同起点开始:")
    print("从G开始: " + ' -> '.join(circle_of_fifths('G', 7)))
    print("从F开始: " + ' -> '.join(circle_of_fifths('F', 7)))


def example_key_signatures():
    """调号"""
    print_separator("调号")
    
    keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#',
            'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']
    
    print("升号调:")
    for key in ['G', 'D', 'A', 'E', 'B', 'F#']:
        sharps, flats = key_signature(key)
        if sharps:
            print(f"  {key}大调: {' '.join(sharps)}")
        else:
            print(f"  {key}大调: 无升降号")
    
    print("\n降号调:")
    for key in ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']:
        sharps, flats = key_signature(key)
        if flats:
            print(f"  {key}大调: {' '.join(flats)}")
        else:
            print(f"  {key}大调: 无升降号")


def example_chord_scale():
    """和弦音阶关系"""
    print_separator("和弦音阶关系")
    
    print("C大调和弦进行:")
    chords = get_scale_chords('C', 'major')
    for note, chord_type, symbol in chords:
        chord_name = note
        if chord_type == 'minor':
            chord_name += 'm'
        elif chord_type == 'diminished':
            chord_name += '°'
        elif chord_type == 'augmented':
            chord_name += '+'
        print(f"  {symbol}: {chord_name} ({chord_type})")
    
    print("\nA小调和弦进行:")
    chords = get_scale_chords('A', 'natural_minor')
    for note, chord_type, symbol in chords:
        chord_name = note
        if chord_type == 'minor':
            chord_name += 'm'
        elif chord_type == 'diminished':
            chord_name += '°'
        elif chord_type == 'augmented':
            chord_name += '+'
        print(f"  {symbol}: {chord_name} ({chord_type})")


def example_transposition_practice():
    """移调练习"""
    print_separator("移调应用")
    
    # 将旋律从C调移到G调
    melody = ['C', 'D', 'E', 'G', 'A', 'G', 'E', 'D', 'C']
    
    print("原旋律 (C调):")
    print(' - '.join(melody))
    
    # C到G是纯五度，向上7个半音
    transposed = []
    for note in melody:
        n = parse_note(note)
        transposed.append(str(transpose_note(n, 7)))
    
    print("\n移调到G调 (纯五度上):")
    print(' - '.join(transposed))
    
    # 移到F调（纯四度上，或纯五度下）
    transposed_f = []
    for note in melody:
        n = parse_note(note)
        transposed_f.append(str(transpose_note(n, 5)))
    
    print("\n移调到F调 (纯四度上):")
    print(' - '.join(transposed_f))


def example_scale_comparison():
    """音阶比较"""
    print_separator("音阶比较")
    
    print("比较不同音阶的音符组成:")
    
    # 以C为根音的多种音阶
    scales_to_compare = [
        ('major', '大调'),
        ('natural_minor', '自然小调'),
        ('harmonic_minor', '和声小调'),
        ('melodic_minor', '旋律小调'),
        ('dorian', '多利亚'),
        ('phrygian', '弗里吉亚'),
        ('lydian', '利底亚'),
        ('mixolydian', '混合利底亚'),
    ]
    
    for scale_type, name in scales_to_compare:
        scale = generate_scale('C', scale_type)
        notes_only = scale[:-1]  # 去掉结尾的八度
        # 使用音级表示
        print(f"{name}: {notes_only}")


def example_list_all_scales():
    """列出所有音阶"""
    print_separator("所有支持的音阶")
    
    scales = list_scales()
    
    print(f"共支持 {len(scales)} 种音阶:\n")
    
    # 按音符数量分组
    by_notes = {}
    for stype, name, count in scales:
        if count not in by_notes:
            by_notes[count] = []
        by_notes[count].append((stype, name))
    
    for count in sorted(by_notes.keys()):
        print(f"\n{count}个音符的音阶:")
        for stype, name in by_notes[count]:
            if name != stype:
                print(f"  - {stype}: {name}")
            else:
                print(f"  - {stype}")


def main():
    """主函数"""
    print("\n" + "="*50)
    print("  scale_utils 音阶工具库使用示例")
    print("="*50)
    
    example_basic_notes()
    example_major_scales()
    example_minor_scales()
    example_pentatonic_scales()
    example_blues_scales()
    example_modes()
    example_exotic_scales()
    example_scale_identification()
    example_relative_keys()
    example_circle_of_fifths()
    example_key_signatures()
    example_chord_scale()
    example_transposition_practice()
    example_scale_comparison()
    example_list_all_scales()
    
    print("\n" + "="*50)
    print("  示例结束")
    print("="*50 + "\n")


if __name__ == '__main__':
    main()