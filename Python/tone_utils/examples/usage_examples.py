"""
Tone Utilities 使用示例

展示 tone_utils 模块的各种功能用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    note_to_frequency, frequency_to_note, midi_to_frequency, frequency_to_midi,
    note_to_midi, midi_to_note, generate_scale, generate_chord, identify_chord,
    cents_difference, frequency_ratio_to_cents, cents_to_frequency_ratio,
    transpose_note, get_interval, get_harmonics, get_enharmonic_equivalents,
    is_consonant_interval, get_circle_of_fifths, Tone
)


def example_basic_conversion():
    """基础音符频率转换示例。"""
    print("=" * 60)
    print("基础音符频率转换")
    print("=" * 60)
    
    # A4 = 440Hz (标准音高)
    a4_freq = note_to_frequency('A', 4)
    print(f"A4 频率: {a4_freq:.2f} Hz")
    
    # 中央 C (C4)
    c4_freq = note_to_frequency('C', 4)
    print(f"C4 频率: {c4_freq:.2f} Hz")
    
    # 使用升号和降号
    print(f"A#4 频率: {note_to_frequency('A#', 4):.2f} Hz")
    print(f"Bb4 频率: {note_to_frequency('Bb', 4):.2f} Hz")  # 与 A#4 相同
    
    # 从频率识别音符
    note, octave, midi = frequency_to_note(440.0)
    print(f"\n440 Hz 对应音符: {note}{octave} (MIDI: {midi})")
    
    note, octave, midi = frequency_to_note(261.63)
    print(f"261.63 Hz 对应音符: {note}{octave} (MIDI: {midi})")
    
    print()


def example_midi_conversion():
    """MIDI 转换示例。"""
    print("=" * 60)
    print("MIDI 音符号转换")
    print("=" * 60)
    
    # MIDI 音符号范围: 0-127
    print("常见 MIDI 音符号及其频率:")
    print("-" * 40)
    
    important_notes = [
        (60, "C4 - 中央 C"),
        (69, "A4 - 标准音高"),
        (21, "A0 - 钢琴最低音"),
        (108, "C8 - 钢琴最高音"),
    ]
    
    for midi, desc in important_notes:
        freq = midi_to_frequency(midi)
        print(f"MIDI {midi}: {freq:.2f} Hz - {desc}")
    
    # MIDI 到音符名称
    note, octave = midi_to_note(60)
    print(f"\nMIDI 60 = {note}{octave}")
    
    # 使用降号表示
    note, octave = midi_to_note(61, prefer_flat=True)
    print(f"MIDI 61 (降号表示) = {note}{octave}")
    
    print()


def example_scale_generation():
    """音阶生成示例。"""
    print("=" * 60)
    print("音阶生成")
    print("=" * 60)
    
    # C 大调音阶
    print("C 大调音阶:")
    scale = generate_scale('C', 'major', 4)
    for note, freq in scale:
        print(f"  {note}: {freq:.2f} Hz")
    
    # A 小调音阶
    print("\nA 小调音阶 (自然小调):")
    scale = generate_scale('A', 'minor', 4)
    for note, freq in scale:
        print(f"  {note}: {freq:.2f} Hz")
    
    # C 五声音阶
    print("\nC 大调五声音阶:")
    scale = generate_scale('C', 'pentatonic_major', 4)
    for note, freq in scale:
        print(f"  {note}: {freq:.2f} Hz")
    
    # A 布鲁斯音阶
    print("\nA 布鲁斯音阶:")
    scale = generate_scale('A', 'blues', 4)
    for note, freq in scale:
        print(f"  {note}: {freq:.2f} Hz")
    
    # D 调式 (多利亚)
    print("\nD 多利亚调式:")
    scale = generate_scale('D', 'dorian', 4)
    for note, freq in scale:
        print(f"  {note}: {freq:.2f} Hz")
    
    print()


def example_chord_generation():
    """和弦生成示例。"""
    print("=" * 60)
    print("和弦生成")
    print("=" * 60)
    
    # 大三和弦
    print("C 大三和弦:")
    chord = generate_chord('C', 'major', 4)
    for note, freq in chord:
        print(f"  {note}: {freq:.2f} Hz")
    
    # 小三和弦
    print("\nA 小三和弦:")
    chord = generate_chord('A', 'minor', 4)
    for note, freq in chord:
        print(f"  {note}: {freq:.2f} Hz")
    
    # 属七和弦
    print("\nG 属七和弦 (G7):")
    chord = generate_chord('G', 'dom7', 4)
    for note, freq in chord:
        print(f"  {note}: {freq:.2f} Hz")
    
    # 大七和弦
    print("\nC 大七和弦 (Cmaj7):")
    chord = generate_chord('C', 'maj7', 4)
    for note, freq in chord:
        print(f"  {note}: {freq:.2f} Hz")
    
    # 减三和弦
    print("\nB 减三和弦:")
    chord = generate_chord('B', 'dim', 4)
    for note, freq in chord:
        print(f"  {note}: {freq:.2f} Hz")
    
    # 减七和弦
    print("\nC 减七和弦 (Cdim7):")
    chord = generate_chord('C', 'dim7', 4)
    for note, freq in chord:
        print(f"  {note}: {freq:.2f} Hz")
    
    print()


def example_chord_identification():
    """和弦识别示例。"""
    print("=" * 60)
    print("和弦识别")
    print("=" * 60)
    
    # 大三和弦识别
    notes = ['C', 'E', 'G']
    chords = identify_chord(notes)
    print(f"音符 {notes} 可能是:")
    for root, chord_type in chords:
        print(f"  {root} {chord_type}")
    
    # 小三和弦识别
    notes = ['A', 'C', 'E']
    chords = identify_chord(notes)
    print(f"\n音符 {notes} 可能是:")
    for root, chord_type in chords:
        print(f"  {root} {chord_type}")
    
    # 七和弦识别
    notes = ['C', 'E', 'G', 'B']
    chords = identify_chord(notes)
    print(f"\n音符 {notes} 可能是:")
    for root, chord_type in chords:
        print(f"  {root} {chord_type}")
    
    print()


def example_cents_calculation():
    """音分计算示例。"""
    print("=" * 60)
    print("音分计算")
    print("=" * 60)
    
    # 八度关系
    cents = cents_difference(440, 880)
    print(f"A4 到 A5 的音分差: {cents:.2f} cents (应为 1200)")
    
    # 半音关系
    cents = cents_difference(440, 466.16)
    print(f"A4 到 A#4 的音分差: {cents:.1f} cents (约为 100)")
    
    # 纯五度
    c4 = note_to_frequency('C', 4)
    g4 = note_to_frequency('G', 4)
    cents = cents_difference(c4, g4)
    print(f"C4 到 G4 的音分差: {cents:.1f} cents (约为 700)")
    
    # 频率比转音分
    print("\n频率比转音分:")
    print(f"  比例 2:1 (八度) = {frequency_ratio_to_cents(2):.2f} cents")
    print(f"  比例 3:2 (纯五度) = {frequency_ratio_to_cents(1.5):.2f} cents")
    print(f"  比例 4:3 (纯四度) = {frequency_ratio_to_cents(4/3):.2f} cents")
    print(f"  比例 5:4 (大三度) = {frequency_ratio_to_cents(1.25):.2f} cents")
    
    # 音分转频率比
    print("\n音分转频率比:")
    print(f"  1200 cents = {cents_to_frequency_ratio(1200):.2f} (八度)")
    print(f"  700 cents = {cents_to_frequency_ratio(700):.3f} (约纯五度)")
    print(f"  100 cents = {cents_to_frequency_ratio(100):.4f} (半音)")
    
    print()


def example_transpose():
    """移调示例。"""
    print("=" * 60)
    print("移调")
    print("=" * 60)
    
    # 向上移调
    note, octave = transpose_note('C', 4, 2)
    print(f"C4 向上移调 2 个半音: {note}{octave}")
    
    note, octave = transpose_note('C', 4, 4)
    print(f"C4 向上移调 4 个半音: {note}{octave}")
    
    # 向下移调
    note, octave = transpose_note('G', 4, -5)
    print(f"G4 向下移调 5 个半音: {note}{octave}")
    
    # 跨八度移调
    note, octave = transpose_note('A', 4, 3)
    print(f"A4 向上移调 3 个半音: {note}{octave}")
    
    note, octave = transpose_note('C', 4, 12)
    print(f"C4 向上移调 12 个半音 (一个八度): {note}{octave}")
    
    print()


def example_intervals():
    """音程示例。"""
    print("=" * 60)
    print("音程计算")
    print("=" * 60)
    
    intervals_to_test = [
        ('C', 4, 'D', 4),
        ('C', 4, 'E', 4),
        ('C', 4, 'F', 4),
        ('C', 4, 'G', 4),
        ('C', 4, 'A', 4),
        ('C', 4, 'B', 4),
        ('C', 4, 'C', 5),
    ]
    
    for n1, o1, n2, o2 in intervals_to_test:
        semitones, name = get_interval(n1, o1, n2, o2)
        freq1 = note_to_frequency(n1, o1)
        freq2 = note_to_frequency(n2, o2)
        print(f"{n1}{o1} -> {n2}{o2}: {semitones} 半音 ({name}), "
              f"{freq1:.2f}Hz -> {freq2:.2f}Hz")
    
    print()


def example_harmonics():
    """泛音系列示例。"""
    print("=" * 60)
    print("泛音系列")
    print("=" * 60)
    
    print("A4 (440 Hz) 的泛音系列:")
    harmonics = get_harmonics(440, 16)
    for num, freq, note in harmonics:
        print(f"  第 {num} 泛音: {freq:.2f} Hz ({note})")
    
    print("\nC4 (中央 C) 的泛音系列 (前 8 个):")
    harmonics = get_harmonics(261.63, 8)
    for num, freq, note in harmonics:
        print(f"  第 {num} 泛音: {freq:.2f} Hz ({note})")
    
    print()


def example_enharmonic():
    """等音示例。"""
    print("=" * 60)
    print("等音（同音异名）")
    print("=" * 60)
    
    for note in ['C#', 'Eb', 'G#', 'Bb']:
        equivalents = get_enharmonic_equivalents(note)
        print(f"{note} 的等音: {equivalents}")
    
    print()


def example_consonance():
    """协和度示例。"""
    print("=" * 60)
    print("音程协和度判断")
    print("=" * 60)
    
    interval_names = {
        0: '纯一度',
        1: '小二度',
        2: '大二度',
        3: '小三度',
        4: '大三度',
        5: '纯四度',
        6: '三全音',
        7: '纯五度',
        8: '小六度',
        9: '大六度',
        10: '小七度',
        11: '大七度',
        12: '纯八度',
    }
    
    for interval, name in interval_names.items():
        consonant = is_consonant_interval(interval)
        status = "协和" if consonant else "不协和"
        print(f"  {name} ({interval} 半音): {status}")
    
    print()


def example_circle_of_fifths():
    """五度圈示例。"""
    print("=" * 60)
    print("五度圈")
    print("=" * 60)
    
    circle = get_circle_of_fifths()
    
    print("调号    关系小调    调内音符")
    print("-" * 50)
    for major, minor, notes in circle:
        print(f"{major:4s}    {minor:8s}    {', '.join(notes)}")
    
    print()


def example_tone_class():
    """Tone 类使用示例。"""
    print("=" * 60)
    print("Tone 类用法")
    print("=" * 60)
    
    # 创建音符
    tone_a = Tone('A', 4)
    tone_c = Tone('C', 4)
    
    print(f"创建音符: {tone_a}")
    print(f"频率: {tone_a.frequency:.2f} Hz")
    print(f"MIDI 音符号: {tone_a.midi_note}")
    
    # 比较音符
    print(f"\n比较: C4 < A4? {tone_c < tone_a}")
    
    # 移调
    transposed = tone_c.transpose(7)  # 纯五度
    print(f"\nC4 向上移调 7 个半音: {transposed}")
    
    # 音程计算
    semitones, name = tone_c.interval_to(Tone('G', 4))
    print(f"\nC4 到 G4 的音程: {semitones} 半音 ({name})")
    
    # 泛音
    print(f"\nC4 的泛音系列 (前 5 个):")
    harmonics = tone_c.harmonics(5)
    for num, freq, note in harmonics:
        print(f"  第 {num} 泛音: {freq:.2f} Hz ({note})")
    
    # 使用运算符
    print(f"\n使用运算符:")
    print(f"  C4 + 7 = {tone_c + 7}")  # 移调
    print(f"  A4 - C4 = {tone_a - tone_c} 半音")  # 半音差
    
    print()


def example_practical_application():
    """实际应用示例。"""
    print("=" * 60)
    print("实际应用场景")
    print("=" * 60)
    
    # 场景 1: 调整音高到标准 A440
    print("场景 1: 检查音高是否准确")
    measured_freq = 442.5  # 实测频率
    note, octave, midi = frequency_to_note(measured_freq)
    cents_off = cents_difference(440, measured_freq)
    print(f"  测得频率: {measured_freq} Hz")
    print(f"  对应音符: {note}{octave}")
    print(f"  与标准 A440 偏差: {cents_off:.1f} cents")
    print(f"  建议: {('调低' if cents_off > 0 else '调高')} {abs(cents_off):.1f} cents")
    
    # 场景 2: 吉弦和弦识别
    print("\n场景 2: 吉弦和弦识别")
    guitar_notes = ['E', 'B', 'G#', 'D', 'A', 'E']  # E 大调吉弦和弦
    # 简化到前三个音符
    simplified = ['E', 'G#', 'B']
    chords = identify_chord(simplified)
    print(f"  按下的音符: {guitar_notes}")
    print(f"  核心音符: {simplified}")
    print(f"  识别为: {[f'{r} {t}' for r, t in chords]}")
    
    # 场景 3: 调号判断
    print("\n场景 3: 判断歌曲调号")
    song_notes = ['D', 'F', 'A', 'C']  # D 小调常见音符
    # D 小调的音符
    dm_scale = generate_scale('D', 'minor', 4)
    dm_notes = [n.replace('4', '') for n, _ in dm_scale]
    print(f"  歌曲中常见音符: {song_notes}")
    print(f"  D 小调音阶: {dm_notes}")
    match_count = sum(1 for n in song_notes if n in dm_notes)
    print(f"  匹配数: {match_count}/{len(song_notes)}")
    
    # 场景 4: 计算等距音程
    print("\n场景 4: 计算等距音程 (将八度分成 N 等份)")
    divisions = 12  # 标准半音
    cents_per_division = 1200 / divisions
    print(f"  将八度分成 {divisions} 等份:")
    print(f"  每份 = {cents_per_division:.2f} cents")
    print(f"  频率比 = {cents_to_frequency_ratio(cents_per_division):.4f}")
    
    divisions = 24  # 四分音
    cents_per_division = 1200 / divisions
    print(f"\n  将八度分成 {divisions} 等份 (四分音):")
    print(f"  每份 = {cents_per_division:.2f} cents")
    print(f"  频率比 = {cents_to_frequency_ratio(cents_per_division):.4f}")
    
    print()


def main():
    """运行所有示例。"""
    example_basic_conversion()
    example_midi_conversion()
    example_scale_generation()
    example_chord_generation()
    example_chord_identification()
    example_cents_calculation()
    example_transpose()
    example_intervals()
    example_harmonics()
    example_enharmonic()
    example_consonance()
    example_circle_of_fifths()
    example_tone_class()
    example_practical_application()
    
    print("=" * 60)
    print("所有示例运行完毕！")
    print("=" * 60)


if __name__ == '__main__':
    main()