"""
Sound Utilities 使用示例

展示声音与音频工具的各种应用场景。
"""

import math
from mod import (
    # 频率转换
    frequency_to_note, note_to_frequency, midi_to_frequency, frequency_to_midi,
    MusicalNote,
    # 波长计算
    speed_of_sound_to_wavelength, wavelength_to_frequency, speed_of_sound_temperature,
    # 分贝计算
    power_ratio_to_decibels, decibels_to_power_ratio,
    amplitude_ratio_to_decibels, decibels_to_amplitude_ratio,
    sound_pressure_to_spl, spl_to_sound_pressure, combine_decibels,
    # BPM 计算
    bpm_to_beat_duration_ms, beat_duration_to_bpm, bpm_to_note_duration,
    bpm_to_measure_duration, calculate_delay_time_ms,
    # 音频采样
    calculate_audio_file_size, calculate_audio_duration, calculate_bit_rate,
    get_audio_info, samples_to_milliseconds, milliseconds_to_samples,
    # 泛音
    generate_harmonics, generate_overtones_series,
    # 音程和弦
    calculate_interval, generate_chord_frequencies, get_scale_notes,
    transpose_frequency, cents_to_frequency_ratio, frequency_ratio_to_cents,
    # 常量
    A4_FREQUENCY, SPEED_OF_SOUND_AIR, REFERENCE_SOUND_PRESSURE,
    COMMON_FREQUENCIES, SAMPLE_RATES, BIT_DEPTHS, SPL_REFERENCE,
)


def example_frequency_conversion():
    """频率与音符转换示例"""
    print("\n" + "=" * 60)
    print("频率与音符转换示例")
    print("=" * 60)
    
    # 1. 频率转音符
    print("\n1. 频率转音符:")
    frequencies = [440.0, 261.63, 329.63, 196.0, 880.0]
    for freq in frequencies:
        note = frequency_to_note(freq)
        print(f"  {freq} Hz -> {note.name}{note.octave} (MIDI: {note.midi_note})")
        if note.cents_deviation != 0:
            print(f"    偏差: {note.cents_deviation} 音分")
    
    # 2. 音符转频率
    print("\n2. 音符转频率:")
    notes = [("C", 4), ("A", 4), ("E", 4), ("G", 3), ("C#", 5)]
    for name, octave in notes:
        freq = note_to_frequency(name, octave)
        print(f"  {name}{octave} -> {freq:.2f} Hz")
    
    # 3. 使用降号
    print("\n3. 使用降号写法:")
    flats = ["Db", "Eb", "Gb", "Ab", "Bb"]
    for note in flats:
        freq = note_to_frequency(note, 4)
        print(f"  {note}4 -> {freq:.2f} Hz")


def example_wavelength_calculation():
    """波长计算示例"""
    print("\n" + "=" * 60)
    print("波长计算示例")
    print("=" * 60)
    
    # 1. 不同频率的波长
    print("\n1. 不同频率在空气中的波长 (声速 343 m/s):")
    frequencies = [20, 100, 440, 1000, 5000, 20000]
    for freq in frequencies:
        wavelength = speed_of_sound_to_wavelength(343, freq)
        print(f"  {freq} Hz -> {wavelength:.4f} 米 ({wavelength * 100:.2f} cm)")
    
    # 2. 温度对声速的影响
    print("\n2. 温度对声速的影响:")
    temps = [-20, 0, 20, 30, 40]
    for temp in temps:
        speed = speed_of_sound_temperature(temp)
        wavelength_440 = speed_of_sound_to_wavelength(speed, 440)
        print(f"  {temp}°C: 声速 {speed:.1f} m/s, A4波长 {wavelength_440:.4f} m")


def example_decibel_calculation():
    """分贝计算示例"""
    print("\n" + "=" * 60)
    print("分贝计算示例")
    print("=" * 60)
    
    # 1. 功率比分贝
    print("\n1. 功率比分贝转换:")
    ratios = [2, 10, 100, 1000]
    for ratio in ratios:
        db = power_ratio_to_decibels(ratio)
        print(f"  功率比 {ratio}x -> {db:.2f} dB")
    
    # 2. 振幅比分贝
    print("\n2. 振幅比分贝转换:")
    ratios = [2, 10, 100]
    for ratio in ratios:
        db = amplitude_ratio_to_decibels(ratio)
        print(f"  振幅比 {ratio}x -> {db:.2f} dB")
    
    # 3. 声压级转换
    print("\n3. 常见声压级:")
    for name, spl in SPL_REFERENCE.items():
        pressure = spl_to_sound_pressure(spl)
        print(f"  {name}: {spl} dB SPL -> {pressure:.6f} Pa")
    
    # 4. 分贝合并
    print("\n4. 多声源合并:")
    scenarios = [
        ([60, 60], "两个相同声源"),
        ([60, 60, 60], "三个相同声源"),
        ([70, 60], "不同声源"),
        ([80, 70, 60], "三个不同声源"),
    ]
    for dbs, desc in scenarios:
        combined = combine_decibels(dbs)
        print(f"  {desc} ({dbs}): {combined:.2f} dB")


def example_bpm_timing():
    """BPM 与时间计算示例"""
    print("\n" + "=" * 60)
    print("BPM 与时间计算示例")
    print("=" * 60)
    
    # 1. 不同 BPM 的拍时长
    print("\n1. 不同 BPM 的每拍时长:")
    bpms = [60, 80, 100, 120, 140, 160, 180]
    for bpm in bpms:
        ms = bpm_to_beat_duration_ms(bpm)
        print(f"  {bpm} BPM -> {ms:.2f} ms/拍")
    
    # 2. 音符时长计算
    print("\n2. 120 BPM 各音符时长:")
    notes = ["whole", "half", "quarter", "eighth", "sixteenth"]
    for note_type in notes:
        ms = bpm_to_note_duration(120, note_type)
        print(f"  {note_type}: {ms:.2f} ms")
    
    # 3. 常见延迟设置
    print("\n3. 常见延迟时间 (同步 BPM):")
    bpm = 120
    subdivisions = ["quarter", "eighth", "dotted_eighth", "sixteenth", "triplet_eighth"]
    for sub in subdivisions:
        ms = calculate_delay_time_ms(bpm, sub)
        print(f"  {bpm} BPM {sub}: {ms:.2f} ms")
    
    # 4. 小节时长
    print("\n4. 不同拍号的小节时长 (120 BPM):")
    time_signatures = ["4/4", "3/4", "2/4", "6/8", "5/4"]
    for ts in time_signatures:
        ms = bpm_to_measure_duration(120, ts)
        print(f"  {ts}: {ms:.2f} ms ({ms/1000:.2f} 秒)")


def example_audio_calculations():
    """音频文件计算示例"""
    print("\n" + "=" * 60)
    print("音频文件计算示例")
    print("=" * 60)
    
    # 1. CD 质量
    print("\n1. CD 质量 (44.1 kHz, 16 bit, 立体声):")
    durations = [1, 3, 5, 10, 60]
    for minutes in durations:
        size = calculate_audio_file_size(minutes * 60, 44100, 16, 2)
        print(f"  {minutes} 分钟 -> {size / 1024 / 1024:.2f} MB")
    
    # 2. 不同质量对比
    print("\n2. 5分钟音频不同质量对比:")
    configs = [
        ("电话质量", 8000, 8, 1),
        ("语音聊天", 16000, 16, 1),
        ("CD 质量", 44100, 16, 2),
        ("DVD 质量", 48000, 16, 2),
        ("专业音频", 96000, 24, 2),
        ("高精度", 192000, 32, 2),
    ]
    for name, sr, bd, ch in configs:
        size = calculate_audio_file_size(5 * 60, sr, bd, ch)
        bitrate = calculate_bit_rate(sr, bd, ch)
        print(f"  {name}: {size / 1024 / 1024:.2f} MB, 比特率 {bitrate / 1000:.0f} kbps")
    
    # 3. 采样与毫秒转换
    print("\n3. 常见采样数与时间:")
    sample_rates = [44100, 48000, 96000]
    for sr in sample_rates:
        print(f"\n  采样率 {sr} Hz:")
        samples_list = [1, 512, 1024, 2048, 4096]
        for samples in samples_list:
            ms = samples_to_milliseconds(samples, sr)
            print(f"    {samples} samples -> {ms:.2f} ms")


def example_harmonics():
    """泛音系列示例"""
    print("\n" + "=" * 60)
    print("泛音系列示例")
    print("=" * 60)
    
    # 1. A4 的泛音
    print("\n1. A4 (440 Hz) 的前 16 个泛音:")
    harmonics = generate_harmonics(440, 16)
    for n, freq, note_name in harmonics:
        # 标记和谐和不和谐的泛音
        consonance = "和谐" if n in [1, 2, 3, 4, 5, 6, 8] else "不和谐"
        print(f"  {n}次泛音: {freq:.1f} Hz ({note_name}) [{consonance}]")
    
    # 2. 不同波形类型的泛音分布
    print("\n2. 不同波形的泛音分布 (基频 100 Hz):")
    for series_type in ["harmonic", "odd", "even"]:
        series = generate_overtones_series(100, series_type)
        print(f"  {series_type}: {series[:6]} Hz")


def example_chords():
    """和弦与音阶示例"""
    print("\n" + "=" * 60)
    print("和弦与音阶示例")
    print("=" * 60)
    
    # 1. 各类和弦
    print("\n1. C 和弦类型:")
    chord_types = ["major", "minor", "diminished", "augmented", "sus4", "major7", "minor7", "dominant7"]
    for chord_type in chord_types:
        chord = generate_chord_frequencies("C", 4, chord_type)
        notes = list(chord.keys())
        print(f"  C{chord_type}: {notes}")
    
    # 2. 不同根音的大三和弦
    print("\n2. 不同根音的大三和弦:")
    roots = ["C", "D", "E", "F", "G", "A", "B"]
    for root in roots:
        chord = generate_chord_frequencies(root, 4, "major")
        notes = list(chord.keys())
        print(f"  {root} 大三和弦: {notes}")
    
    # 3. 音阶
    print("\n3. C 为根音的各种音阶:")
    scales = ["major", "minor", "pentatonic_major", "pentatonic_minor", "blues", "dorian", "lydian"]
    for scale_type in scales:
        notes = get_scale_notes("C", scale_type)
        print(f"  C {scale_type}: {' - '.join(notes)}")


def example_intervals():
    """音程计算示例"""
    print("\n" + "=" * 60)
    print("音程计算示例")
    print("=" * 60)
    
    # 1. 从 C4 开始的各种音程
    print("\n1. C4 (261.63 Hz) 的音程:")
    c4 = note_to_frequency("C", 4)
    intervals = [
        ("小二度", "D", 4, 1),
        ("大二度", "D", 4, 2),
        ("小三度", "Eb", 4, 3),
        ("大三度", "E", 4, 4),
        ("纯四度", "F", 4, 5),
        ("增四度", "F#", 4, 6),
        ("纯五度", "G", 4, 7),
        ("小六度", "Ab", 4, 8),
        ("大六度", "A", 4, 9),
        ("小七度", "Bb", 4, 10),
        ("大七度", "B", 4, 11),
        ("纯八度", "C", 5, 12),
    ]
    
    for name, note, octave, semitones in intervals:
        freq = note_to_frequency(note, octave)
        s, i_name, ratio = calculate_interval(c4, freq)
        print(f"  {name}: {note}{octave} ({freq:.2f} Hz), 比值 {ratio:.4f}")
    
    # 2. 移调示例
    print("\n2. 移调示例:")
    original = 440.0
    transpositions = [0, 1, 2, 3, 4, 5, 7, 12, -12]
    for semitones in transpositions:
        new_freq = transpose_frequency(original, semitones)
        print(f"  A4 + {semitones} 半音 -> {new_freq:.2f} Hz")


def example_music_theory():
    """音乐理论示例"""
    print("\n" + "=" * 60)
    print("音乐理论示例")
    print("=" * 60)
    
    # 1. 音分计算
    print("\n1. 音分与频率比:")
    cents_values = [0, 100, 200, 500, 700, 1200]
    for cents in cents_values:
        ratio = cents_to_frequency_ratio(cents)
        back = frequency_ratio_to_cents(ratio)
        print(f"  {cents} 音分 -> 比值 {ratio:.4f} -> {back:.0f} 音分")
    
    # 2. 常见频率比对应的音分
    print("\n2. 常见频率比:")
    ratios = [
        (1.0, "纯一度"),
        (9/8, "大全音 (Pythagorean)"),
        (5/4, "大三度 (Just)"),
        (4/3, "纯四度 (Just)"),
        (3/2, "纯五度 (Just)"),
        (5/3, "大六度 (Just)"),
        (2.0, "纯八度"),
    ]
    for ratio, name in ratios:
        cents = frequency_ratio_to_cents(ratio)
        print(f"  {name}: 比值 {ratio:.4f} -> {cents:.1f} 音分")


def example_practical_apps():
    """实际应用示例"""
    print("\n" + "=" * 60)
    print("实际应用示例")
    print("=" * 60)
    
    # 1. 音频设备设置
    print("\n1. 常见音频设备采样率与位深度:")
    for name, sr in SAMPLE_RATES.items():
        for depth_name, bd in BIT_DEPTHS.items():
            bitrate = calculate_bit_rate(sr, bd, 2)
            if bitrate > 0:
                print(f"  {name} @ {depth_name}: {bitrate / 1000:.0f} kbps")
    
    # 2. 人声频率范围
    print("\n2. 人声频率范围:")
    voice_types = [
        ("男低音", "bass_low", "bass_high"),
        ("男高音", "tenor_low", "tenor_high"),
        ("女中音", "alto_low", "alto_high"),
        ("女高音", "soprano_low", "soprano_high"),
    ]
    for name, low_key, high_key in voice_types:
        low_freq = COMMON_FREQUENCIES[low_key]
        high_freq = COMMON_FREQUENCIES[high_key]
        low_note = frequency_to_note(low_freq)
        high_note = frequency_to_note(high_freq)
        print(f"  {name}: {low_note.name}{low_note.octave} ({low_freq:.1f} Hz) - "
              f"{high_note.name}{high_note.octave} ({high_freq:.1f} Hz)")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("声音与音频工具 - 使用示例")
    print("=" * 60)
    
    example_frequency_conversion()
    example_wavelength_calculation()
    example_decibel_calculation()
    example_bpm_timing()
    example_audio_calculations()
    example_harmonics()
    example_chords()
    example_intervals()
    example_music_theory()
    example_practical_apps()
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    main()