#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Period Utilities Examples
========================================
使用示例展示 period_utils 模块的各种功能。

运行方式: python usage_examples.py
"""

import sys
sys.path.insert(0, '..')

from mod import (
    # Conversion functions
    bpm_to_ms, ms_to_bpm, hz_to_period_ms, period_ms_to_hz,
    note_name_to_frequency, frequency_to_note_name,
    seconds_to_samples, samples_to_seconds,
    
    # Wave generation
    generate_wave, generate_sine_wave, generate_square_wave,
    generate_triangle_wave, generate_sawtooth_wave,
    
    # Pattern functions
    generate_periodic_sequence, generate_heartbeat_pattern,
    generate_metronome_pattern, generate_lfo_pattern,
    generate_tremolo_pattern, generate_vibrato_pattern,
    
    # Rhythm functions
    generate_rhythm_pattern, analyze_rhythm_pattern,
    create_custom_pattern, RHYTHM_PATTERNS,
    
    # Utility functions
    calculate_harmonics, calculate_octave_equivalent,
    quantize_to_grid, calculate_swing_offset,
    format_time_ms, format_bpm, format_frequency,
    
    # Generator class
    PeriodGenerator,
    
    # Constants
    DEFAULT_SAMPLE_RATE,
)


def print_section(title: str):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demo_bpm_conversion():
    """演示 BPM 转换"""
    print_section("BPM 转换演示")
    
    print("\n常见 BPM 对应的每拍时长:")
    bpm_values = [40, 60, 80, 90, 100, 120, 140, 160, 180, 200]
    
    print("\n{:<10} {:<15} {:<15} {:<15}".format(
        "BPM", "每拍(ms)", "八分音符(ms)", "十六分音符(ms)"
    ))
    print("-" * 55)
    
    for bpm in bpm_values:
        beat_ms = bpm_to_ms(bpm)
        eighth_ms = beat_ms / 2
        sixteenth_ms = beat_ms / 4
        print("{:<10} {:<15.1f} {:<15.1f} {:<15.1f}".format(
            bpm, beat_ms, eighth_ms, sixteenth_ms
        ))
    
    # 反向转换示例
    print("\n反向转换示例:")
    test_ms = [250, 500, 750, 1000]
    for ms in test_ms:
        bpm = ms_to_bpm(ms)
        print(f"{ms}ms per beat = {bpm:.1f} BPM")


def demo_frequency_conversion():
    """演示频率转换"""
    print_section("频率转换演示")
    
    print("\n常见频率对应的周期:")
    freq_values = [0.5, 1, 2, 5, 10, 50, 100, 440, 1000]
    
    print("\n{:<15} {:<20} {:<20}".format("频率(Hz)", "周期(ms)", "周期(秒)"))
    print("-" * 55)
    
    for freq in freq_values:
        period_ms = hz_to_period_ms(freq)
        period_s = period_ms / 1000
        print("{:<15} {:<20.3f} {:<20.5f}".format(freq, period_ms, period_s))
    
    # 音符频率对照
    print("\n常见音符频率:")
    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    print("\n{:<10} {:<15} {:<20}".format("音符", "频率(Hz)", "最接近的频率"))
    print("-" * 45)
    
    for note in notes:
        freq = note_name_to_frequency(note)
        print("{:<10} {:<15.2f} {:<20}".format(note, freq, f"{freq:.2f}Hz"))


def demo_wave_generation():
    """演示波形生成"""
    print_section("波形生成演示")
    
    wave_types = ['sine', 'square', 'triangle', 'sawtooth', 'pulse']
    frequency = 440  # A4
    duration = 1.0  # 1 second
    
    print(f"\n生成 {frequency}Hz ({format_frequency(frequency)}) 的各种波形:")
    print("时长: 1秒")
    
    print("\n{:<15} {:<10} {:<15} {:<15}".format(
        "波形类型", "采样数", "最大值", "最小值"
    ))
    print("-" * 55)
    
    for wave_type in wave_types:
        num_samples = seconds_to_samples(duration)
        wave = generate_wave(wave_type, num_samples, frequency)
        
        max_val = max(wave)
        min_val = min(wave)
        
        print("{:<15} {:<10} {:<15.3f} {:<15.3f}".format(
            wave_type, len(wave), max_val, min_val
        ))
    
    # 演示振幅控制
    print("\n振幅控制演示 (正弦波 440Hz):")
    amplitudes = [1.0, 0.8, 0.5, 0.3, 0.1]
    for amp in amplitudes:
        wave = generate_sine_wave(44100, frequency, amplitude=amp)
        print(f"振幅 {amp}: 最大值 {max(wave):.3f}")


def demo_pattern_generation():
    """演示模式生成"""
    print_section("周期模式生成演示")
    
    # 周期性序列
    print("\n周期性序列生成:")
    pattern = [1, 0, 0.5, 0]
    print(f"基础模式: {pattern}")
    
    for repeats in [1, 2, 3]:
        result = generate_periodic_sequence(pattern, repeats)
        print(f"重复 {repeats} 次: {result}")
    
    # 心跳模式
    print("\n心跳模式生成:")
    bpm_values = [60, 72, 90, 100]
    duration = 10.0
    
    print("\n{:<10} {:<15} {:<20}".format("心率(BPM)", "10秒采样数", "预期心跳次数"))
    print("-" * 45)
    
    for bpm in bpm_values:
        pattern = generate_heartbeat_pattern(bpm, duration)
        expected_beats = int(bpm * duration / 60)
        print("{:<10} {:<15} {:<20}".format(bpm, len(pattern), expected_beats))
    
    # LFO模式
    print("\nLFO (低频振荡器) 模式:")
    rates = [0.5, 1, 5, 10]
    
    print("\n{:<10} {:<15} {:<20}".format("速率(Hz)", "周期(秒)", "每秒周期数"))
    print("-" * 45)
    
    for rate in rates:
        period = 1 / rate
        lfo = generate_lfo_pattern(44100, rate, depth=1.0)
        print("{:<10} {:<15.1f} {:<20.0f}".format(rate, period, rate))


def demo_rhythm_patterns():
    """演示节奏模式"""
    print_section("节奏模式演示")
    
    # 预设节奏模式
    print("\n内置节奏模式:")
    
    print("\n{:<20} {:<30} {:<10}".format("模式名称", "模式", "密度"))
    print("-" * 60)
    
    for name, pattern in RHYTHM_PATTERNS.items():
        analysis = analyze_rhythm_pattern(pattern)
        pattern_str = str(pattern)[:28] + "..." if len(str(pattern)) > 30 else str(pattern)
        print("{:<20} {:<30} {:<10.2f}".format(
            name, pattern_str, analysis['density']
        ))
    
    # 节奏分析
    print("\n节奏模式分析示例:")
    patterns = [
        [1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
    ]
    
    print("\n{:<25} {:<10} {:<10} {:<10} {:<10}".format(
        "模式", "拍数", "休止数", "密度", "切分数"
    ))
    print("-" * 55)
    
    for pattern in patterns:
        analysis = analyze_rhythm_pattern(pattern)
        pattern_str = str(pattern)[:22] + "..." if len(str(pattern)) > 25 else str(pattern)
        print("{:<25} {:<10} {:<10} {:<10.2f} {:<10}".format(
            pattern_str,
            analysis['beat_count'],
            analysis['rest_count'],
            analysis['density'],
            analysis['syncopation_count']
        ))
    
    # 自定义模式创建
    print("\n创建自定义节奏模式:")
    
    # 创建一个4拍模式，只在每小节第一拍
    custom = create_custom_pattern([0, 4, 8, 12], 16)
    print(f"每4拍一击: {custom}")
    
    # 创建带强度的模式
    custom_strength = create_custom_pattern([0, 2, 4, 6], 8, strengths=[1.0, 0.5, 0.3, 0.2])
    print(f"渐弱模式: {custom_strength}")


def demo_harmonics():
    """演示谐波计算"""
    print_section("谐波计算演示")
    
    print("\n各音符的谐波系列:")
    notes = ['C4', 'E4', 'G4', 'A4']
    
    for note in notes:
        freq = note_name_to_frequency(note)
        harmonics = calculate_harmonics(freq, 5)
        
        print(f"\n{note} ({freq:.2f} Hz) 的前5个谐波:")
        
        harmonic_notes = []
        for h in harmonics:
            note_name = frequency_to_note_name(h)
            harmonic_notes.append(f"{h:.0f}Hz ({note_name})")
        
        print("  " + ", ".join(harmonic_notes))
    
    # 八度等效
    print("\n八度等效计算:")
    print("\n{:<15} {:<15} {:<15}".format("原频率", "原音符", "A4等效"))
    print("-" * 45)
    
    test_freqs = [220, 330, 440, 660, 880, 1320]
    for freq in test_freqs:
        note = frequency_to_note_name(freq)
        equiv = calculate_octave_equivalent(freq, 4)
        equiv_note = frequency_to_note_name(equiv)
        print("{:<15} {:<15} {:<15.1f} ({})".format(
            f"{freq}Hz", note, equiv, equiv_note
        ))


def demo_quantization():
    """演示量化功能"""
    print_section("量化功能演示")
    
    # 时间量化
    print("\n时间量化到网格:")
    grid_sizes = [10, 25, 50, 100, 250, 500]
    test_times = [123, 456, 789, 1234]
    
    print("\n{:<12} {:<12} {:<12} {:<12} {:<12}".format(
        "原时间(ms)", "网格10ms", "网格50ms", "网格100ms", "网格500ms"
    ))
    print("-" * 60)
    
    for time in test_times:
        results = [quantize_to_grid(time, grid) for grid in [10, 50, 100, 500]]
        print("{:<12} {:<12} {:<12} {:<12} {:<12}".format(
            time, results[0], results[1], results[2], results[3]
        ))
    
    # 摇摆偏移
    print("\n摇摆节奏偏移计算:")
    swing_amounts = [0.5, 0.55, 0.6, 0.66, 0.7]
    
    print("\n{:<15} {:<15} {:<15} {:<15}".format(
        "摇摆量", "位置0偏移", "位置1偏移", "位置2偏移"
    ))
    print("-" * 60)
    
    for swing in swing_amounts:
        offsets = [
            calculate_swing_offset(0, swing, 8),
            calculate_swing_offset(1, swing, 8),
            calculate_swing_offset(2, swing, 8),
        ]
        print("{:<15} {:<15.2f} {:<15.2f} {:<15.2f}".format(
            swing, offsets[0], offsets[1], offsets[2]
        ))


def demo_generator_class():
    """演示生成器类"""
    print_section("PeriodGenerator 类演示")
    
    print("\n使用 PeriodGenerator 构建复合波形:")
    
    # 创建生成器
    gen = PeriodGenerator()
    
    # 添加基础波形
    gen.add_wave('sine', 440, 1.0, amplitude=0.5)
    print("添加: 正弦波 440Hz (A4), 振幅 0.5")
    
    # 添加谐波
    gen.add_wave('sine', 880, 1.0, amplitude=0.25)
    print("添加: 正弦波 880Hz (A5 - 第二谐波), 振幅 0.25")
    
    gen.add_wave('sine', 1320, 1.0, amplitude=0.1)
    print("添加: 正弦波 1320Hz (第三谐波), 振幅 0.1")
    
    # 归一化
    gen.normalize()
    print("归一化")
    
    # 显示结果信息
    info = gen.info()
    print("\n生成结果:")
    print(f"  采样率: {info['sample_rate']} Hz")
    print(f"  时长: {info['duration_seconds']} 秒")
    print(f"  采样数: {info['num_samples']}")
    
    # 心跳模式生成器
    print("\n使用生成器创建心跳模式:")
    heartbeat_gen = PeriodGenerator().add_heartbeat(72, 5.0)
    hb_info = heartbeat_gen.info()
    print(f"心率 72 BPM, 5秒: {hb_info['num_samples']} samples")
    
    # 添加包络
    heartbeat_gen.apply_envelope(attack_ms=500, release_ms=1000)
    print("添加淡入淡出包络")


def demo_formatting():
    """演示格式化功能"""
    print_section("格式化功能演示")
    
    print("\n时间格式化:")
    times_ms = [10, 100, 500, 1000, 1234, 5000, 60000]
    for ms in times_ms:
        formatted = format_time_ms(ms)
        print(f"  {ms}ms -> {formatted}")
    
    print("\nBPM 格式化:")
    bpm_values = [60, 80, 120, 128.5, 140, 175.5]
    for bpm in bpm_values:
        formatted = format_bpm(bpm)
        print(f"  {bpm} -> {formatted}")
    
    print("\n频率格式化:")
    freq_values = [20, 100, 440, 1000, 5000, 15000, 20000]
    for freq in freq_values:
        formatted = format_frequency(freq)
        print(f"  {freq}Hz -> {formatted}")


def main():
    """运行所有演示"""
    print("\n" + "=" * 60)
    print(" AllToolkit - Period Utilities 使用示例")
    print("=" * 60)
    
    demo_bpm_conversion()
    demo_frequency_conversion()
    demo_wave_generation()
    demo_pattern_generation()
    demo_rhythm_patterns()
    demo_harmonics()
    demo_quantization()
    demo_generator_class()
    demo_formatting()
    
    print("\n" + "=" * 60)
    print(" 演示完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()