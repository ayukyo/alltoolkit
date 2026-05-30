"""
Music Chord Utils - 使用示例
音乐和弦与音阶工具使用示例

展示如何使用 music_chord_utils 模块的各种功能：
1. 音符转换
2. 和弦构建与识别
3. 音阶生成
4. 移调
5. 调号与关系调
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from music_chord_utils.mod import (
    # 音符转换
    normalize_note,
    note_to_semitone,
    semitone_to_note,
    midi_to_note,
    note_to_midi,
    note_to_frequency,
    midi_to_frequency,
    frequency_to_midi,
    
    # 音程
    get_interval,
    calculate_interval,
    
    # 和弦
    build_chord,
    identify_chord,
    invert_chord,
    get_chord_inversions,
    parse_chord_symbol,
    
    # 音阶
    build_scale,
    get_scale_degrees,
    get_diatonic_chords,
    
    # 调号
    get_key_signature,
    get_relative_key,
    
    # 移调
    transpose_note,
    transpose_chord,
    
    # 工具函数
    is_diatonic,
    get_enharmonic,
    get_note_name_variants,
    
    # 便捷函数
    c_major_scale,
    a_minor_scale,
    circle_of_fifths,
    circle_of_fourths,
    
    # 数据
    CHORD_QUALITY_NAMES,
    SCALE_NAMES,
)


def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def example_note_conversion():
    """示例：音符转换"""
    print_section("1. 音符转换")
    
    # 音符标准化
    print("音符标准化:")
    print(f"  Db → {normalize_note('Db')} (降号转升号)")
    print(f"  Bb → {normalize_note('Bb')}")
    
    # 音符与半音编号
    print("\n音符与半音编号:")
    for note in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        print(f"  {note} = {note_to_semitone(note)} 半音")
    
    # MIDI与音符
    print("\nMIDI与音符:")
    for midi in [60, 64, 67, 69, 72]:
        print(f"  MIDI {midi} = {midi_to_note(midi)}")
    
    # 频率转换
    print("\n频率转换:")
    print(f"  A4 = {note_to_frequency('A4'):.2f} Hz")
    print(f"  C4 = {note_to_frequency('C4'):.2f} Hz")
    print(f"  MIDI 69 = {midi_to_frequency(69):.2f} Hz")
    print(f"  440 Hz = MIDI {frequency_to_midi(440)}")


def example_intervals():
    """示例：音程计算"""
    print_section("2. 音程计算")
    
    # 音程信息
    print("音程表:")
    for semitones in [0, 1, 2, 3, 4, 5, 7, 12]:
        interval = get_interval(semitones)
        print(f"  {semitones:2d} 半音 = {interval.name} ({interval.abbreviation})")
    
    # 计算两个音之间的音程
    print("\n计算音程:")
    pairs = [('C', 'E'), ('C', 'G'), ('C', 'Bb'), ('D', 'A')]
    for note1, note2 in pairs:
        interval = calculate_interval(note1, note2)
        print(f"  {note1} → {note2}: {interval.name}")


def example_chords():
    """示例：和弦构建与识别"""
    print_section("3. 和弦构建与识别")
    
    # 构建各种和弦
    print("构建和弦:")
    qualities = ['major', 'minor', 'dim', 'aug', '7', 'maj7', 'm7', 'sus2', 'sus4']
    for quality in qualities:
        chord = build_chord('C', quality)
        chinese_name = CHORD_QUALITY_NAMES.get(quality, quality)
        print(f"  C{quality if quality != 'major' else ''}: {chinese_name} = {chord.notes}")
    
    # 和弦转位
    print("\n和弦转位 (C大三和弦):")
    inversions = get_chord_inversions('C', 'major')
    names = ['原位', '第一转位', '第二转位']
    for i, inv in enumerate(inversions):
        print(f"  {names[i]}: {inv}")
    
    # 和弦识别
    print("\n识别和弦:")
    chord_notes = [
        ['C', 'E', 'G'],
        ['A', 'C', 'E'],
        ['G', 'B', 'D', 'F'],
        ['C', 'Eb', 'Gb'],
    ]
    for notes in chord_notes:
        result = identify_chord(notes)
        if result:
            root, quality = result
            chinese = CHORD_QUALITY_NAMES.get(quality, quality)
            print(f"  {notes} → {root}{quality if quality != 'major' else ''} ({chinese})")
        else:
            print(f"  {notes} → 无法识别")


def example_scales():
    """示例：音阶生成"""
    print_section("4. 音阶生成")
    
    # 各种音阶
    print("常见音阶:")
    scale_types = ['major', 'natural_minor', 'harmonic_minor', 'pentatonic_major', 'blues', 'dorian']
    for scale_type in scale_types:
        scale = build_scale('C', scale_type)
        chinese = SCALE_NAMES.get(scale_type, scale_type)
        print(f"  C {chinese}: {scale}")
    
    # C大调顺阶和弦
    print("\nC大调顺阶和弦:")
    chords = get_diatonic_chords('C', 'major')
    degrees = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    quality_map = {'major': '', 'minor': 'm', 'dim': 'dim'}
    for i, chord in enumerate(chords):
        suffix = quality_map.get(chord.quality, chord.quality)
        print(f"  {degrees[i]}: {chord.root}{suffix} = {chord.notes}")


def example_key_signatures():
    """示例：调号"""
    print_section("5. 调号与关系调")
    
    # 调号
    print("调号:")
    keys = ['C', 'G', 'D', 'F', 'A']
    for key in keys:
        accidentals, is_sharp = get_key_signature(key, 'major')
        symbol = '升' if is_sharp else '降'
        if accidentals:
            print(f"  {key}大调: {len(accidentals)}个{symbol}号 ({', '.join(accidentals)})")
        else:
            print(f"  {key}大调: 无升降号")
    
    # 关系调
    print("\n关系调:")
    for key in ['C', 'G', 'D', 'F']:
        relative_root, relative_type = get_relative_key(key, 'major')
        print(f"  {key}大调的关系小调: {relative_root}小调")


def example_transposition():
    """示例：移调"""
    print_section("6. 移调")
    
    # 音符移调
    print("音符移调:")
    print(f"  C 上移 2 个半音 → {transpose_note('C', 2)}")
    print(f"  C 上移 7 个半音 → {transpose_note('C', 7)}")
    print(f"  E 下移 1 个半音 → {transpose_note('E', -1)}")
    
    # 和弦移调
    print("\n和弦移调:")
    chord_transpositions = [
        ('C', 2, 'D'),
        ('Am7', 3, 'Cm7'),
        ('G7', 5, 'C7'),
        ('Fmaj7', 7, 'Cmaj7'),
    ]
    for original, semitones, expected in chord_transpositions:
        result = transpose_chord(original, semitones)
        print(f"  {original} 上移 {semitones} 半音 → {result}")


def example_enharmonics():
    """示例：等音"""
    print_section("7. 等音与调内音")
    
    # 等音
    print("等音:")
    for note in ['C#', 'F#', 'G#']:
        print(f"  {note} 的等音: {get_enharmonic(note)}")
    
    # 音符变体
    print("\n音符变体:")
    for note in ['C#', 'D#', 'F#']:
        variants = get_note_name_variants(note)
        print(f"  {note}: {variants}")
    
    # 调内音判断
    print("\n调内音判断:")
    test_notes = [('E', 'C'), ('F#', 'C'), ('F#', 'G'), ('Bb', 'F')]
    for note, key in test_notes:
        is_dia = is_diatonic(note, key, 'major')
        status = "✓ 调内音" if is_dia else "✗ 变化音"
        print(f"  {note} 在 {key}大调中: {status}")


def example_circles():
    """示例：五度圈和四度圈"""
    print_section("8. 五度圈与四度圈")
    
    # 五度圈
    print("五度圈:")
    circle = circle_of_fifths()
    print(f"  {' → '.join(circle)}")
    
    # 四度圈
    print("\n四度圈:")
    circle = circle_of_fourths()
    print(f"  {' → '.join(circle)}")


def example_practical_usage():
    """示例：实际应用"""
    print_section("9. 实际应用场景")
    
    # 场景1: 分析一段和弦进行
    print("场景1: 分析和弦进行 C - Am - F - G")
    progression = ['C', 'Am', 'F', 'G']
    print("和弦分析:")
    for symbol in progression:
        root, quality = parse_chord_symbol(symbol)
        chord = build_chord(root, quality)
        chinese = CHORD_QUALITY_NAMES.get(quality, quality)
        print(f"  {symbol}: {chinese}, 音符 {chord.notes}")
    
    # 场景2: 转调
    print("\n场景2: 将 C 大调旋律转调到 D 大调")
    melody = ['C', 'D', 'E', 'F', 'G']
    transposed = [transpose_note(note, 2) for note in melody]
    print(f"  原调: {' - '.join(melody)}")
    print(f"  新调: {' - '.join(transposed)}")
    
    # 场景3: 找和弦转位
    print("\n场景3: G7 和弦的所有转位")
    inversions = get_chord_inversions('G', '7')
    for i, inv in enumerate(inversions):
        print(f"  转位{i}: {' - '.join(inv)}")
    
    # 场景4: 生成练习音阶
    print("\n场景4: 生成蓝调音阶用于练习")
    keys = ['A', 'E', 'G']
    for key in keys:
        scale = build_scale(key, 'blues')
        print(f"  {key}蓝调: {' '.join(scale)}")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("  Music Chord Utils - 音乐和弦与音阶工具")
    print("  使用示例")
    print("="*60)
    
    example_note_conversion()
    example_intervals()
    example_chords()
    example_scales()
    example_key_signatures()
    example_transposition()
    example_enharmonics()
    example_circles()
    example_practical_usage()
    
    print("\n" + "="*60)
    print("  示例演示完成!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()