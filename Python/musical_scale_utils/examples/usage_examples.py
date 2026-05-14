"""
Musical Scale Utils 使用示例

展示音乐音阶与和弦理论工具库的核心功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Note, Scale, Chord,
    ScaleType, ChordType, Interval,
    midi_to_note, midi_to_frequency, frequency_to_midi,
    generate_scale, generate_chord, get_interval, get_interval_name,
    transpose_note, get_key_signature, get_scale_degrees,
    get_chord_progression_degrees, get_beat_durations,
    generate_arpeggio, invert_chord, generate_circle_of_fifths,
    analyze_chord_quality, get_relative_keys,
    get_all_modes_of_scale, compare_scales,
)
import os


def print_section(title: str):
    """打印分隔标题"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def example_note_basics():
    """音符基础功能示例"""
    print_section("音符基础功能")
    
    # 创建音符
    c4 = Note('C', 4, '')
    a4 = Note('A', 4, '')
    c_sharp = Note('C', 4, '#')
    
    print(f"音符创建:")
    print(f"  C4: {c4.get_full_name()}")
    print(f"  A4: {a4.get_full_name()}")
    print(f"  C#4: {c_sharp.get_full_name()}")
    
    print(f"\nMIDI 编号:")
    print(f"  C4 MIDI: {c4.get_midi_number()}")
    print(f"  A4 MIDI: {a4.get_midi_number()}")
    
    print(f"\n频率计算:")
    print(f"  C4 频率: {c4.get_frequency():.2f} Hz")
    print(f"  A4 频率: {a4.get_frequency():.2f} Hz")
    print(f"  C#4 频率: {c_sharp.get_frequency():.2f} Hz")


def example_scale_generation():
    """音阶生成示例"""
    print_section("音阶生成")
    
    # 大调音阶
    c_major = generate_scale('C', ScaleType.MAJOR)
    print(f"C 大调音阶:")
    print(f"  音符: {[n.get_full_name() for n in c_major.notes]}")
    
    # 自然小调
    a_minor = generate_scale('A', ScaleType.MINOR_NATURAL)
    print(f"\nA 自然小调音阶:")
    print(f"  音符: {[n.get_full_name() for n in a_minor.notes]}")
    
    # 五声音阶
    c_penta = generate_scale('C', ScaleType.PENTATONIC_MAJOR)
    print(f"\nC 大调五声音阶:")
    print(f"  音符: {[n.get_full_name() for n in c_penta.notes]}")
    
    # 蓝调音阶
    a_blues = generate_scale('A', ScaleType.PENTATONIC_BLUES)
    print(f"\nA 蓝调音阶:")
    print(f"  音符: {[n.get_full_name() for n in a_blues.notes]}")
    
    # 多利亚调式
    d_dorian = generate_scale('D', ScaleType.DORIAN)
    print(f"\nD 多利亚调式:")
    print(f"  音符: {[n.get_full_name() for n in d_dorian.notes]}")


def example_chord_generation():
    """和弦生成示例"""
    print_section("和弦生成")
    
    # 三和弦
    c_major = generate_chord('C', ChordType.MAJOR_TRIAD)
    a_minor = generate_chord('A', ChordType.MINOR_TRIAD)
    
    print(f"三和弦:")
    print(f"  C 大三和弦: {[n.get_full_name() for n in c_major.notes]}")
    print(f"  A 小三和弦: {[n.get_full_name() for n in a_minor.notes]}")
    
    # 七和弦
    cmaj7 = generate_chord('C', ChordType.MAJOR_7)
    g7 = generate_chord('G', ChordType.DOMINANT_7)
    
    print(f"\n七和弦:")
    print(f"  Cmaj7: {[n.get_full_name() for n in cmaj7.notes]}")
    print(f"  G7: {[n.get_full_name() for n in g7.notes]}")
    
    # 挂留和弦
    csus4 = generate_chord('C', ChordType.SUS_4)
    print(f"\n挂留和弦:")
    print(f"  Csus4: {[n.get_full_name() for n in csus4.notes]}")


def example_intervals():
    """音程示例"""
    print_section("音程")
    
    c4 = Note('C', 4, '')
    
    # 计算音程
    notes_to_check = [
        ('E', 4, '', "大三度"),
        ('G', 4, '', "纯五度"),
        ('A', 4, '', "大六度"),
        ('B', 4, '', "大七度"),
    ]
    
    print(f"从 C4 到各音的音程:")
    for note_name, octave, acc, expected_cn in notes_to_check:
        note = Note(note_name, octave, acc)
        interval = get_interval(c4, note)
        print(f"  C4 → {note.get_full_name()}: {get_interval_name(interval)} ({interval.value})")


def example_key_signature():
    """调号示例"""
    print_section("调号")
    
    keys = ['C major', 'G major', 'D major', 'F major', 'Bb major']
    
    print(f"各调的调号信息:")
    for key in keys:
        sig = get_key_signature(key)
        print(f"  {key}:")
        print(f"    升降记号数: {sig['accidentals']}")
        print(f"    具体记号: {sig['accidental_notes']}")


def example_scale_degrees():
    """音阶级数示例"""
    print_section("音阶级数")
    
    c_major = generate_scale('C', ScaleType.MAJOR)
    degrees = get_scale_degrees(c_major)
    
    print(f"C 大调音阶各音级:")
    for deg in degrees:
        if 'interval_from_root' in deg:
            print(f"  {deg['degree']} ({deg['degree_cn']}): {deg['note']} - {deg['interval_cn']}")
        else:
            print(f"  {deg['degree']} ({deg['degree_cn']}): {deg['note']} (主音)")


def example_chord_progression():
    """调内和弦示例"""
    print_section("调内和弦")
    
    c_major = generate_scale('C', ScaleType.MAJOR)
    progression = get_chord_progression_degrees(c_major)
    
    print(f"C 大调调内和弦:")
    for chord in progression:
        print(f"  {chord['degree']}: {chord['chord']} ({chord['notes']})")


def example_tempo_rhythm():
    """节拍节奏示例"""
    print_section("节拍与节奏")
    
    bpm = 120
    
    durations = get_beat_durations(bpm)
    print(f"120 BPM 时各节拍时长:")
    for name, duration in durations.items():
        if duration >= 0.5:
            print(f"  {name}: {duration:.2f} 秒")
    
    print(f"\n示例计算:")
    print(f"  4 个四分音符 (120 BPM): {durations['quarter_note'] * 4:.2f} 秒")
    print(f"  8 个八分音符 (120 BPM): {durations['eighth_note'] * 8:.2f} 秒")


def example_chord_inversion():
    """和弦转位示例"""
    print_section("和弦转位")
    
    c_major = generate_chord('C', ChordType.MAJOR_TRIAD)
    
    print(f"C 大三和弦转位:")
    print(f"  原位: {[n.get_full_name() for n in c_major.notes]}")
    
    first = invert_chord(c_major, 1)
    print(f"  第一转位: {[n.get_full_name() for n in first.notes]}")
    
    second = invert_chord(c_major, 2)
    print(f"  第二转位: {[n.get_full_name() for n in second.notes]}")


def example_arpeggio():
    """琶音示例"""
    print_section("琶音")
    
    cmaj7 = generate_chord('C', ChordType.MAJOR_7)
    
    print(f"Cmaj7 琶音:")
    
    up = generate_arpeggio(cmaj7, 'up', 1)
    print(f"  上行: {[n.get_full_name() for n in up]}")
    
    down = generate_arpeggio(cmaj7, 'down', 1)
    print(f"  下行: {[n.get_full_name() for n in down]}")
    
    up_down = generate_arpeggio(cmaj7, 'up_down', 1)
    print(f"  上下行: {[n.get_full_name() for n in up_down]}")


def example_modes():
    """调式示例"""
    print_section("教会调式")
    
    modes = get_all_modes_of_scale('C')
    
    print(f"C 为根音的各调式:")
    for name, scale in modes.items():
        notes = [n.get_full_name() for n in scale.notes]
        print(f"  {name}: {notes}")


def example_circle_of_fifths():
    """五度圈示例"""
    print_section("五度圈")
    
    circle = generate_circle_of_fifths()
    
    print(f"五度圈 (大调):")
    for item in circle[:7]:
        print(f"  {item['major_key']} major -> {item['relative_minor']} minor")
        print(f"    升记号数: {item['accidentals']}")


def example_relative_keys():
    """近关系调示例"""
    print_section("近关系调")
    
    relatives = get_relative_keys('C major')
    
    print(f"C 大调的近关系调:")
    for key_type, keys in relatives.items():
        if keys:
            print(f"  {key_type}: {keys}")


def example_transpose():
    """移调示例"""
    print_section("移调")
    
    c4 = Note('C', 4, '')
    
    print(f"从 C4 移调:")
    
    # 移调到 E (大三度)
    e4 = transpose_note(c4, 4)
    print(f"  上移大三度 (4 半音): {e4.get_full_name()}")
    
    # 移调到 G (纯五度)
    g4 = transpose_note(c4, 7)
    print(f"  上移纯五度 (7 半音): {g4.get_full_name()}")
    
    # 移调一个八度
    c5 = transpose_note(c4, 12)
    print(f"  上移八度 (12 半音): {c5.get_full_name()}")


def example_midi_conversion():
    """MIDI 转换示例"""
    print_section("MIDI 转换")
    
    print(f"MIDI 编号到音符:")
    for midi in [60, 69, 72, 84]:
        note = midi_to_note(midi)
        freq = midi_to_frequency(midi)
        print(f"  MIDI {midi}: {note.get_full_name()} ({freq:.2f} Hz)")
    
    print(f"\n频率到 MIDI:")
    for freq in [261.63, 440.0, 880.0]:
        midi = frequency_to_midi(freq)
        note = midi_to_note(midi)
        print(f"  {freq:.2f} Hz: MIDI {midi} ({note.get_full_name()})")


def main():
    """运行所有示例"""
    example_note_basics()
    example_scale_generation()
    example_chord_generation()
    example_intervals()
    example_key_signature()
    example_scale_degrees()
    example_chord_progression()
    example_tempo_rhythm()
    example_chord_inversion()
    example_arpeggio()
    example_modes()
    example_circle_of_fifths()
    example_relative_keys()
    example_transpose()
    example_midi_conversion()
    
    print("\n" + "=" * 50)
    print("  所有示例完成!")
    print("=" * 50)


if __name__ == '__main__':
    main()