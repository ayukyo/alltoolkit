"""
波形工具使用示例

演示波形生成、分析和变换的各种用例。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from mod import (
    WaveformType,
    WaveformGenerator,
    WaveformAnalyzer,
    WaveformTransformer,
    WaveformVisualizer,
    generate_waveform,
    analyze_waveform,
    create_envelope,
    apply_envelope,
)


def example_01_basic_waveform_generation():
    """示例1: 基本波形生成"""
    print("=" * 60)
    print("示例1: 基本波形生成")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    
    # 生成各种波形
    waveforms = [
        ("正弦波", WaveformType.SINE, 440),
        ("方波", WaveformType.SQUARE, 440),
        ("锯齿波", WaveformType.SAWTOOTH, 440),
        ("三角波", WaveformType.TRIANGLE, 440),
        ("脉冲波", WaveformType.PULSE, 440),
    ]
    
    for name, wave_type, freq in waveforms:
        samples = gen.generate(wave_type, freq, 0.1)
        stats = analyze_waveform(samples, sample_rate=8000)
        print(f"\n{name} ({freq}Hz):")
        print(f"  采样点数: {len(samples)}")
        print(f"  RMS: {stats['rms']:.4f}")
        print(f"  峰峰值: {stats['peak_to_peak']:.4f}")


def example_02_visualization():
    """示例2: 波形可视化"""
    print("\n" + "=" * 60)
    print("示例2: 波形可视化")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    
    # 生成并可视化不同波形
    waveforms = [
        ("正弦波 440Hz", WaveformType.SINE, 440),
        ("方波 220Hz", WaveformType.SQUARE, 220),
        ("锯齿波 330Hz", WaveformType.SAWTOOTH, 330),
        ("三角波 550Hz", WaveformType.TRIANGLE, 550),
    ]
    
    for name, wave_type, freq in waveforms:
        samples = gen.generate(wave_type, freq, 0.01)  # 短时间便于显示
        print(f"\n{name}:")
        print(WaveformVisualizer.get_ascii_waveform(samples, width=50, height=8))


def example_03_frequency_estimation():
    """示例3: 频率估计"""
    print("\n" + "=" * 60)
    print("示例3: 频率估计（过零法）")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=44100)
    analyzer = WaveformAnalyzer(sample_rate=44100)
    
    # 测试不同频率
    frequencies = [100, 220, 440, 880, 1000, 2000]
    
    print(f"\n{'真实频率':>12} {'估计频率':>12} {'误差':>10}")
    print("-" * 36)
    
    for freq in frequencies:
        samples = gen.generate(WaveformType.SINE, freq, 0.5)
        estimated = analyzer.estimate_frequency(samples)
        error = abs(estimated - freq)
        print(f"{freq:>12}Hz {estimated:>12.1f}Hz {error:>10.1f}Hz")


def example_04_envelope_adsr():
    """示例4: ADSR 包络"""
    print("\n" + "=" * 60)
    print("示例4: ADSR 包络")
    print("=" * 60)
    
    # 创建不同类型的包络
    envelopes = [
        ("钢琴式", 0.01, 0.1, 0.2, 0.3),
        ("风琴式", 0.1, 0.1, 0.3, 0.1),
        ("拨弦式", 0.001, 0.3, 0.1, 0.4),
        ("打击式", 0.001, 0.2, 0.05, 0.1),
    ]
    
    for name, attack, decay, sustain, release in envelopes:
        env = create_envelope(attack, decay, sustain, release, 1.0, sample_rate=8000)
        
        # 找到峰值位置
        peak_idx = env.index(max(env))
        peak_time = peak_idx / 8000
        
        print(f"\n{name}包络:")
        print(f"  Attack: {attack}s, Decay: {decay}s, Sustain: {sustain}s, Release: {release}s")
        print(f"  峰值时间: {peak_time:.3f}s")
        
        # 显示包络形状
        ascii_env = WaveformVisualizer.get_ascii_waveform(env, width=50, height=6)
        print(ascii_env)


def example_05_fade_effects():
    """示例5: 淡入淡出效果"""
    print("\n" + "=" * 60)
    print("示例5: 淡入淡出效果")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    transformer = WaveformTransformer(sample_rate=8000)
    
    # 生成波形
    samples = gen.generate(WaveformType.SINE, 440, 0.5)
    
    print("\n原始波形（前50个采样）:")
    print([f"{s:.3f}" for s in samples[:50]])
    
    # 应用不同类型的淡入
    curves = ["linear", "exponential", "logarithmic", "cosine"]
    
    for curve in curves:
        faded = transformer.fade_in(samples, duration=0.1, curve=curve)
        print(f"\n{curve} 淡入（前50个采样）:")
        print([f"{s:.3f}" for s in faded[:50]])


def example_06_waveform_mixing():
    """示例6: 波形混合"""
    print("\n" + "=" * 60)
    print("示例6: 波形混合（加法合成）")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    transformer = WaveformTransformer(sample_rate=8000)
    analyzer = WaveformAnalyzer(sample_rate=8000)
    
    # 创建复音（基频 + 泛音）
    fundamental = gen.generate(WaveformType.SINE, 440, 0.5, amplitude=1.0)
    harmonic2 = gen.generate(WaveformType.SINE, 880, 0.5, amplitude=0.5)
    harmonic3 = gen.generate(WaveformType.SINE, 1320, 0.5, amplitude=0.33)
    harmonic4 = gen.generate(WaveformType.SINE, 1760, 0.5, amplitude=0.25)
    
    # 混合
    combined = transformer.mix(
        [fundamental, harmonic2, harmonic3, harmonic4],
        weights=[1.0, 0.5, 0.33, 0.25]
    )
    
    # 归一化
    normalized = analyzer.normalize(combined)
    
    stats = analyzer.get_statistics(normalized)
    print(f"\n混合波形统计:")
    print(f"  采样点数: {len(normalized)}")
    print(f"  最大值: {stats['max']:.4f}")
    print(f"  最小值: {stats['min']:.4f}")
    print(f"  RMS: {stats['rms']:.4f}")
    
    # 可视化
    print("\n混合波形可视化:")
    print(WaveformVisualizer.get_ascii_waveform(normalized[:800], width=50, height=8))


def example_07_amplitude_modulation():
    """示例7: 振幅调制"""
    print("\n" + "=" * 60)
    print("示例7: 振幅调制（颤音效果）")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    transformer = WaveformTransformer(sample_rate=8000)
    
    # 载波：440Hz 正弦波
    carrier = gen.generate(WaveformType.SINE, 440, 1.0)
    
    # 调制：5Hz 正弦波（颤音）
    modulator = gen.generate(WaveformType.SINE, 5, 1.0)
    
    # 应用调制
    modulated = transformer.amplitude_modulate(carrier, modulator, depth=0.5)
    
    print("\n调制参数:")
    print("  载波频率: 440Hz")
    print("  调制频率: 5Hz")
    print("  调制深度: 50%")
    
    # 显示调制后的波形
    print("\n调制后波形:")
    print(WaveformVisualizer.get_ascii_waveform(modulated[:800], width=50, height=8))


def example_08_noise_generation():
    """示例8: 噪声生成"""
    print("\n" + "=" * 60)
    print("示例8: 噪声生成")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    analyzer = WaveformAnalyzer(sample_rate=8000)
    
    # 生成白噪声和粉红噪声
    white = gen.generate(WaveformType.WHITE_NOISE, 0, 1.0, seed=42)
    pink = gen.generate(WaveformType.PINK_NOISE, 0, 1.0)
    
    white_stats = analyzer.get_statistics(white)
    pink_stats = analyzer.get_statistics(pink)
    
    print("\n白噪声:")
    print(f"  RMS: {white_stats['rms']:.4f}")
    print(f"  峰峰值: {white_stats['peak_to_peak']:.4f}")
    print(WaveformVisualizer.get_ascii_waveform(white[:400], width=50, height=5))
    
    print("\n粉红噪声:")
    print(f"  RMS: {pink_stats['rms']:.4f}")
    print(f"  峰峰值: {pink_stats['peak_to_peak']:.4f}")
    print(WaveformVisualizer.get_ascii_waveform(pink[:400], width=50, height=5))


def example_09_pulse_wave_duty_cycle():
    """示例9: 脉冲波占空比"""
    print("\n" + "=" * 60)
    print("示例9: 脉冲波占空比")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    
    duty_cycles = [0.1, 0.25, 0.5, 0.75, 0.9]
    
    for duty in duty_cycles:
        samples = gen.generate(
            WaveformType.PULSE, 
            440, 
            0.01, 
            duty_cycle=duty
        )
        
        # 计算实际占空比
        positive = sum(1 for s in samples if s > 0)
        actual_duty = positive / len(samples)
        
        print(f"\n设置占空比: {duty*100:.0f}%")
        print(f"实际占空比: {actual_duty*100:.1f}%")
        print(WaveformVisualizer.get_ascii_waveform(samples, width=50, height=6))


def example_10_time_stretch():
    """示例10: 时间拉伸"""
    print("\n" + "=" * 60)
    print("示例10: 时间拉伸")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    transformer = WaveformTransformer(sample_rate=8000)
    
    # 生成原始波形
    original = gen.generate(WaveformType.SINE, 440, 0.5)
    
    # 时间拉伸
    stretched = transformer.time_stretch(original, 2.0)  # 变慢
    compressed = transformer.time_stretch(original, 0.5)  # 变快
    
    print(f"\n原始长度: {len(original)} 采样")
    print(f"拉伸 2x 后: {len(stretched)} 采样")
    print(f"压缩 0.5x 后: {len(compressed)} 采样")


def example_11_delay_effect():
    """示例11: 延迟效果"""
    print("\n" + "=" * 60)
    print("示例11: 延迟效果（回声）")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    transformer = WaveformTransformer(sample_rate=8000)
    
    # 生成短促音
    impulse = [0.0] * 100 + [1.0] * 100 + [0.0] * 2000
    
    # 应用延迟
    delayed = transformer.delay(
        impulse,
        delay_time=0.1,  # 100ms 延迟
        decay=0.6,
        feedback=0.4
    )
    
    # 找出延迟峰值
    peaks = []
    threshold = 0.3
    for i, s in enumerate(delayed):
        if abs(s) > threshold:
            peaks.append((i / 8000, s))  # 时间, 振幅
    
    print("\n延迟参数:")
    print("  延迟时间: 100ms")
    print("  衰减: 60%")
    print("  反馈: 40%")
    
    print("\n检测到的峰值:")
    for time, amp in peaks[:5]:
        print(f"  {time*1000:.0f}ms: {amp:.3f}")


def example_12_silence_detection():
    """示例12: 静音检测"""
    print("\n" + "=" * 60)
    print("示例12: 静音检测")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    analyzer = WaveformAnalyzer(sample_rate=8000)
    
    # 创建包含静音段的音频
    sound1 = gen.generate(WaveformType.SINE, 440, 0.3)
    silence = [0.0] * int(8000 * 0.2)  # 200ms 静音
    sound2 = gen.generate(WaveformType.SINE, 880, 0.3)
    
    samples = sound1 + silence + sound2
    
    # 检测静音
    silent_regions = analyzer.detect_silence(
        samples,
        threshold=0.01,
        min_duration=0.1
    )
    
    print(f"\n总时长: {len(samples)/8000:.2f}s")
    print(f"检测到的静音区域:")
    
    for start, end in silent_regions:
        start_time = start / 8000
        end_time = end / 8000
        duration = end_time - start_time
        print(f"  {start_time:.2f}s - {end_time:.2f}s ({duration*1000:.0f}ms)")


def example_13_complete_synthesis():
    """示例13: 完整合成示例"""
    print("\n" + "=" * 60)
    print("示例13: 完整合成示例（音符合成）")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    transformer = WaveformTransformer(sample_rate=8000)
    analyzer = WaveformAnalyzer(sample_rate=8000)
    
    # 音符频率
    notes = {
        'C4': 261.63,
        'E4': 329.63,
        'G4': 392.00,
        'C5': 523.25,
    }
    
    print("\n合成音符序列:")
    
    for note, freq in notes.items():
        # 生成锯齿波
        samples = gen.generate(WaveformType.SAWTOOTH, freq, 0.3)
        
        # 应用 ADSR 包络
        env = create_envelope(0.01, 0.05, 0.15, 0.09, 0.3, sample_rate=8000)
        samples = apply_envelope(samples, env)
        
        # 归一化
        samples = analyzer.normalize(samples)
        
        stats = analyzer.get_statistics(samples)
        print(f"\n{note} ({freq:.2f}Hz):")
        print(f"  RMS: {stats['rms']:.4f}")
        print(WaveformVisualizer.get_ascii_waveform(samples[:240], width=40, height=5))


def example_14_histogram_analysis():
    """示例14: 振幅直方图分析"""
    print("\n" + "=" * 60)
    print("示例14: 振幅直方图分析")
    print("=" * 60)
    
    gen = WaveformGenerator(sample_rate=8000)
    
    # 分析不同波形的振幅分布
    waveforms = [
        ("正弦波", gen.generate(WaveformType.SINE, 440, 0.5)),
        ("方波", gen.generate(WaveformType.SQUARE, 440, 0.5)),
        ("三角波", gen.generate(WaveformType.TRIANGLE, 440, 0.5)),
    ]
    
    for name, samples in waveforms:
        print(f"\n{name} 振幅分布:")
        print(WaveformVisualizer.get_histogram(samples, bins=10, width=30))


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("波形工具示例集")
    print("=" * 60)
    
    example_01_basic_waveform_generation()
    example_02_visualization()
    example_03_frequency_estimation()
    example_04_envelope_adsr()
    example_05_fade_effects()
    example_06_waveform_mixing()
    example_07_amplitude_modulation()
    example_08_noise_generation()
    example_09_pulse_wave_duty_cycle()
    example_10_time_stretch()
    example_11_delay_effect()
    example_12_silence_detection()
    example_13_complete_synthesis()
    example_14_histogram_analysis()
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()