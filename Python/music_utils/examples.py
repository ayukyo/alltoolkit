"""
Music Utils 使用示例

演示乐理工具库的主要功能
"""

from music_utils import (
    Note, NoteName, Interval, Scale, ScaleType, Chord, ChordType,
    parse_note, parse_chord, circle_of_fifths, circle_of_fourths,
    relative_minor, relative_major, key_signature,
    bpm_to_milliseconds, get_tempo_marking, NoteValue,
    harmonic_series, equal_temperament_frequency,
    guitar_standard_tuning, fret_positions,
    piano_key_to_note, note_to_piano_key,
)


def demo_notes():
    """演示音符操作"""
    print("=" * 50)
    print("音符操作示例")
    print("=" * 50)
    
    # 创建音符
    c4 = Note(NoteName.C, 4)
    a4 = Note(NoteName.A, 4)
    
    print(f"\n音符 C4:")
    print(f"  - MIDI 音符号: {c4.midi()}")
    print(f"  - 频率: {c4.frequency():.2f} Hz")
    print(f"  - 字符串表示: {c4}")
    
    print(f"\n音符 A4 (标准音):")
    print(f"  - MIDI 音符号: {a4.midi()}")
    print(f"  - 频率: {a4.frequency():.2f} Hz")
    
    # 移调
    d4 = c4.transpose(2)  # 移高大二度
    print(f"\nC4 移高大二度: {d4}")
    
    # 从频率获取音符
    freq = 880.0
    note = Note.from_frequency(freq)
    print(f"\n频率 {freq} Hz 对应音符: {note}")
    
    # 解析音符字符串
    parsed = parse_note("F#5")
    print(f"\n解析 'F#5': {parsed} (频率: {parsed.frequency():.2f} Hz)")


def demo_intervals():
    """演示音程"""
    print("\n" + "=" * 50)
    print("音程示例")
    print("=" * 50)
    
    print("\n常用音程:")
    intervals = [
        Interval.UNISON,
        Interval.MINOR_SECOND,
        Interval.MAJOR_SECOND,
        Interval.MINOR_THIRD,
        Interval.MAJOR_THIRD,
        Interval.PERFECT_FOURTH,
        Interval.PERFECT_FIFTH,
        Interval.MAJOR_SIXTH,
        Interval.MAJOR_SEVENTH,
        Interval.OCTAVE,
    ]
    
    for interval in intervals:
        print(f"  {interval} - {interval.name_zh()} ({int(interval)} 半音)")
    
    # 音程计算
    c4 = Note(NoteName.C, 4)
    e4 = Note(NoteName.E, 4)
    interval = c4.interval_to(e4)
    print(f"\nC4 到 E4 的音程: {interval.name_zh()}")


def demo_scales():
    """演示音阶"""
    print("\n" + "=" * 50)
    print("音阶示例")
    print("=" * 50)
    
    # C 大调
    c_major = Scale(NoteName.C, ScaleType.MAJOR)
    print(f"\nC 大调音阶:")
    print(f"  音符: {[str(n) for n in c_major.notes()]}")
    print(f"  频率 (C4): {[f'{f:.2f}' for f in c_major.frequencies(4, 1)]}")
    
    # A 小调
    a_minor = Scale(NoteName.A, ScaleType.MINOR)
    print(f"\nA 自然小调音阶:")
    print(f"  音符: {[str(n) for n in a_minor.notes()]}")
    
    # A 布鲁斯
    a_blues = Scale(NoteName.A, ScaleType.BLUES)
    print(f"\nA 布鲁斯音阶:")
    print(f"  音符: {[str(n) for n in a_blues.notes()]}")
    
    # C 大调五声
    c_penta = Scale(NoteName.C, ScaleType.PENTATONIC_MAJOR)
    print(f"\nC 大调五声音阶:")
    print(f"  音符: {[str(n) for n in c_penta.notes()]}")
    
    # 调内和弦
    print(f"\nC 大调调内和弦:")
    for degree in range(1, 8):
        triad = c_major.triad(degree)
        print(f"  {degree}级: {triad}")


def demo_chords():
    """演示和弦"""
    print("\n" + "=" * 50)
    print("和弦示例")
    print("=" * 50)
    
    # 大三和弦
    c_major = Chord(NoteName.C, ChordType.MAJOR)
    print(f"\nC 大三和弦:")
    print(f"  音符: {[str(n) for n in c_major.notes()]}")
    print(f"  符号: {c_major}")
    
    # 七和弦
    g7 = Chord(NoteName.G, ChordType.DOMINANT_7)
    print(f"\nG7 属七和弦:")
    print(f"  音符: {[str(n) for n in g7.notes()]}")
    
    # 小三和弦
    am = Chord(NoteName.A, ChordType.MINOR)
    print(f"\nAm 小三和弦:")
    print(f"  音符: {[str(n) for n in am.notes()]}")
    
    # 和弦转位
    print(f"\nC 大三和弦转位:")
    for inversion in range(3):
        voicing = c_major.invert(inversion)
        notes = voicing.notes()
        print(f"  {inversion}转位: {[str(n) for n in notes]}")
    
    # 和弦识别
    print(f"\n和弦识别:")
    notes = [NoteName.C, NoteName.E, NoteName.G]
    chord = Chord.identify(notes)
    print(f"  [C, E, G] -> {chord}")
    
    # 解析和弦字符串
    parsed = parse_chord("Dm7")
    print(f"\n解析 'Dm7': {parsed}")
    print(f"  音符: {[str(n) for n in parsed.notes()]}")


def demo_circle_of_fifths():
    """演示五度圈"""
    print("\n" + "=" * 50)
    print("五度圈与四度圈")
    print("=" * 50)
    
    fifths = circle_of_fifths()
    print(f"\n五度圈:")
    print(f"  {[str(n) for n in fifths]}")
    
    fourths = circle_of_fourths()
    print(f"\n四度圈:")
    print(f"  {[str(n) for n in fourths]}")


def demo_relative_keys():
    """演示关系调"""
    print("\n" + "=" * 50)
    print("关系调")
    print("=" * 50)
    
    # C 大调的关系小调
    print(f"\nC 大调的关系小调: {relative_minor(NoteName.C)}")
    
    # A 小调的关系大调
    print(f"A 小调的关系大调: {relative_major(NoteName.A)}")
    
    # 调号
    print(f"\n调号:")
    keys = [NoteName.C, NoteName.G, NoteName.D, NoteName.F]
    for key in keys:
        sig = key_signature(key, True)
        sig_str = [str(n) for n in sig] if sig else "无升降号"
        print(f"  {key} 大调: {sig_str}")


def demo_metronome():
    """演示节拍器"""
    print("\n" + "=" * 50)
    print("节拍器")
    print("=" * 50)
    
    # BPM 转换
    bpms = [60, 90, 120, 140, 180]
    print(f"\nBPM 转换:")
    for bpm in bpms:
        ms = bpm_to_milliseconds(bpm)
        marking = get_tempo_marking(bpm)
        print(f"  {bpm} BPM = {ms:.1f} ms/拍 ({marking})")
    
    # 音符时值
    print(f"\n音符时值 (120 BPM):")
    bpm = 120
    for note_value in [NoteValue.WHOLE, NoteValue.HALF, NoteValue.QUARTER, NoteValue.EIGHTH]:
        beats = note_value.duration_beats()
        ms = note_value.duration_ms(bpm)
        print(f"  {note_value}: {beats}拍 = {ms:.1f} ms")


def demo_harmonics():
    """演示泛音"""
    print("\n" + "=" * 50)
    print("泛音列")
    print("=" * 50)
    
    # A4 的泛音列
    fundamental = 440.0
    harmonics = harmonic_series(fundamental, 8)
    print(f"\nA4 ({fundamental} Hz) 泛音列:")
    for i, freq in enumerate(harmonics):
        note = Note.from_frequency(freq)
        print(f"  第{i+1}泛音: {freq:.1f} Hz ≈ {note}")


def demo_guitar():
    """演示吉他"""
    print("\n" + "=" * 50)
    print("吉他")
    print("=" * 50)
    
    # 标准调弦
    tuning = guitar_standard_tuning()
    print(f"\n吉他标准调弦 (从6弦到1弦):")
    for i, note in enumerate(tuning):
        print(f"  {6-i}弦: {note} ({note.frequency():.1f} Hz)")
    
    # 6弦 E2 的前12品
    print(f"\n6弦 (E2) 前12品:")
    frets = fret_positions(tuning[0], 12)
    for fret, note in enumerate(frets):
        print(f"  {fret}品: {note}")


def demo_piano():
    """演示钢琴"""
    print("\n" + "=" * 50)
    print("钢琴")
    print("=" * 50)
    
    # 钢琴键范围
    print(f"\n钢琴键范围:")
    print(f"  第1键 (A0): {piano_key_to_note(1)} ({piano_key_to_note(1).frequency():.1f} Hz)")
    print(f"  第88键 (C8): {piano_key_to_note(88)} ({piano_key_to_note(88).frequency():.1f} Hz)")
    
    # 中间键
    middle_c = Note(NoteName.C, 4)
    print(f"\n中央C (C4):")
    print(f"  钢琴键号: {note_to_piano_key(middle_c)}")
    print(f"  MIDI: {middle_c.midi()}")
    print(f"  频率: {middle_c.frequency():.2f} Hz")


def main():
    """运行所有示例"""
    demo_notes()
    demo_intervals()
    demo_scales()
    demo_chords()
    demo_circle_of_fifths()
    demo_relative_keys()
    demo_metronome()
    demo_harmonics()
    demo_guitar()
    demo_piano()
    
    print("\n" + "=" * 50)
    print("示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()