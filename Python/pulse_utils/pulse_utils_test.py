"""
Pulse Utils 测试套件

测试脉冲/心跳工具模块的所有功能。
"""

import sys
import os
import math
import time

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    WaveType, Pulse, PulseSequence,
    generate_square_wave, generate_sine_wave, generate_triangle_wave,
    generate_sawtooth_wave, generate_pulse_train,
    bpm_to_frequency, frequency_to_bpm, bpm_to_interval_ms, interval_ms_to_bpm,
    generate_metronome,
    calculate_duty_cycle, calculate_high_time, analyze_pulse_signal,
    detect_pulses, count_pulses,
    pulse_generator,
    HeartbeatPattern, simulate_heartbeat, analyze_heartbeat,
    note_to_frequency, frequency_to_note, get_harmonics,
    mix_signals, normalize_signal, amplify_signal, clip_signal
)


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, message: str = ""):
        """运行单个测试"""
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
        else:
            self.failed += 1
            error_msg = f"  ❌ {name}"
            if message:
                error_msg += f" - {message}"
            print(error_msg)
            self.errors.append((name, message))
    
    def test_exception(self, name: str, func, expected_exception, *args):
        """测试是否抛出预期异常"""
        try:
            func(*args)
            self.failed += 1
            print(f"  ❌ {name} - 未抛出 {expected_exception.__name__}")
            self.errors.append((name, f"未抛出 {expected_exception.__name__}"))
        except expected_exception:
            self.passed += 1
            print(f"  ✅ {name}")
        except Exception as e:
            self.failed += 1
            print(f"  ❌ {name} - 抛出了 {type(e).__name__} 而不是 {expected_exception.__name__}")
            self.errors.append((name, f"错误的异常类型: {type(e).__name__}"))
    
    def summary(self):
        """打印测试总结"""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试完成: {self.passed}/{total} 通过")
        if self.errors:
            print(f"\n失败的测试:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}")
        return self.failed == 0


def test_wave_generation(runner: TestRunner):
    """测试波形生成"""
    print("\n📊 波形生成测试")
    
    # 方波测试
    print("  方波生成:")
    square = generate_square_wave(440, 0.1, 44100, 0.5)
    runner.test("方波正确长度", len(square) == 4410, f"长度: {len(square)}")
    runner.test("方波最大值", max(square) == 1.0, f"最大值: {max(square)}")
    runner.test("方波最小值", min(square) == -1.0 or min(square) == 0, f"最小值: {min(square)}")
    
    # 不同占空比
    square_25 = generate_square_wave(440, 0.1, 44100, 0.25)
    high_count_25 = sum(1 for s in square_25[:100] if s > 0)
    high_count_50 = sum(1 for s in square[:100] if s > 0)
    runner.test("方波占空比影响输出", high_count_25 < high_count_50)
    
    # 正弦波测试
    print("  正弦波生成:")
    sine = generate_sine_wave(440, 0.1, 44100)
    runner.test("正弦波正确长度", len(sine) == 4410)
    runner.test("正弦波最大值", max(sine) <= 1.0)
    runner.test("正弦波最小值", min(sine) >= -1.0)
    runner.test("正弦波包含正值", any(s > 0 for s in sine))
    runner.test("正弦波包含负值", any(s < 0 for s in sine))
    
    # 正弦波相位测试
    sine_shifted = generate_sine_wave(440, 0.1, 44100, phase=math.pi/2)
    runner.test("相位影响正弦波", sine[0] != sine_shifted[0])
    
    # 三角波测试
    print("  三角波生成:")
    triangle = generate_triangle_wave(220, 0.1, 44100)
    runner.test("三角波正确长度", len(triangle) == 4410)
    runner.test("三角波最大值", max(triangle) <= 1.0)
    runner.test("三角波最小值", min(triangle) >= -1.0)
    
    # 锯齿波测试
    print("  锯齿波生成:")
    sawtooth = generate_sawtooth_wave(330, 0.1, 44100)
    runner.test("锯齿波正确长度", len(sawtooth) == 4410)
    runner.test("锯齿波最大值", max(sawtooth) <= 1.0)
    runner.test("锯齿波最小值", min(sawtooth) >= -1.0)
    
    # 上升/下降锯齿波
    sawtooth_down = generate_sawtooth_wave(330, 0.1, 44100, rising=False)
    runner.test("锯齿波方向影响输出", sawtooth[1] != sawtooth_down[1])
    
    # 脉冲序列测试
    print("  脉冲序列生成:")
    pulses = generate_pulse_train(10, 1.0, 0.01, 44100)
    runner.test("脉冲序列正确长度", len(pulses) == 44100)
    runner.test("脉冲序列包含脉冲", sum(1 for s in pulses if s > 0) > 0)
    
    # 边界值测试
    print("  边界值测试:")
    runner.test_exception("频率为0抛出异常", generate_square_wave, ValueError, 0, 0.1)
    runner.test_exception("持续时间为0抛出异常", generate_square_wave, ValueError, 440, 0)
    runner.test_exception("占空比为0抛出异常", generate_square_wave, ValueError, 440, 0.1, 44100, 0)
    runner.test_exception("振幅为0抛出异常", generate_square_wave, ValueError, 440, 0.1, 44100, 0.5, 0)


def test_bpm_tools(runner: TestRunner):
    """测试BPM转换工具"""
    print("\n🎵 BPM转换测试")
    
    # BPM转频率
    runner.test("60 BPM = 1 Hz", bpm_to_frequency(60) == 1.0)
    runner.test("120 BPM = 2 Hz", bpm_to_frequency(120) == 2.0)
    runner.test("30 BPM = 0.5 Hz", bpm_to_frequency(30) == 0.5)
    
    # 频率转BPM
    runner.test("1 Hz = 60 BPM", frequency_to_bpm(1.0) == 60.0)
    runner.test("2 Hz = 120 BPM", frequency_to_bpm(2.0) == 120.0)
    runner.test("0.5 Hz = 30 BPM", frequency_to_bpm(0.5) == 30.0)
    
    # BPM转间隔
    runner.test("60 BPM = 1000ms", bpm_to_interval_ms(60) == 1000.0)
    runner.test("120 BPM = 500ms", bpm_to_interval_ms(120) == 500.0)
    runner.test("30 BPM = 2000ms", bpm_to_interval_ms(30) == 2000.0)
    
    # 间隔转BPM
    runner.test("1000ms = 60 BPM", interval_ms_to_bpm(1000) == 60.0)
    runner.test("500ms = 120 BPM", interval_ms_to_bpm(500) == 120.0)
    
    # 双向转换一致性
    for bpm in [40, 60, 90, 120, 150, 180]:
        freq = bpm_to_frequency(bpm)
        back = frequency_to_bpm(freq)
        runner.test(f"BPM往返转换 {bpm}", abs(back - bpm) < 0.001)
    
    # 异常测试
    runner.test_exception("BPM为0抛出异常", bpm_to_frequency, ValueError, 0)
    runner.test_exception("频率为0抛出异常", frequency_to_bpm, ValueError, 0)
    runner.test_exception("间隔为0抛出异常", interval_ms_to_bpm, ValueError, 0)


def test_metronome(runner: TestRunner):
    """测试节拍器"""
    print("\n🎺 节拍器测试")
    
    # 基本节拍器
    metro = generate_metronome(60, 2.0)
    runner.test("节拍器正确长度", len(metro) == 88200)
    runner.test("节拍器有声音", sum(1 for s in metro if s > 0) > 0)
    
    # 不同BPM
    metro_fast = generate_metronome(120, 1.0)
    runner.test("快速节拍器正确长度", len(metro_fast) == 44100)
    
    # 重音模式
    pattern = [1, 0, 0, 0]  # 4/4拍
    metro_pattern = generate_metronome(60, 4.0, accent_pattern=pattern)
    runner.test("重音模式节拍器正确长度", len(metro_pattern) == 176400)
    
    # 边界值
    runner.test_exception("BPM为0抛出异常", generate_metronome, ValueError, 0, 1.0)
    runner.test_exception("持续时间为0抛出异常", generate_metronome, ValueError, 60, 0)


def test_duty_cycle(runner: TestRunner):
    """测试占空比计算"""
    print("\n📐 占空比测试")
    
    # 基本计算
    runner.test("50%占空比", calculate_duty_cycle(0.5, 1.0) == 0.5)
    runner.test("25%占空比", calculate_duty_cycle(0.25, 1.0) == 0.25)
    runner.test("75%占空比", calculate_duty_cycle(0.75, 1.0) == 0.75)
    runner.test("不同周期", calculate_duty_cycle(0.5, 2.0) == 0.25)
    
    # 反向计算
    runner.test("高电平时间50%", calculate_high_time(0.5, 1.0) == 0.5)
    runner.test("高电平时间25%", calculate_high_time(0.25, 1.0) == 0.25)
    runner.test("高电平时间75%", calculate_high_time(0.75, 1.0) == 0.75)
    
    # 边界值
    runner.test("0%占空比", calculate_duty_cycle(0, 1.0) == 0)
    runner.test("100%占空比", calculate_duty_cycle(1.0, 1.0) == 1.0)
    runner.test("0%高电平时间", calculate_high_time(0, 1.0) == 0)
    runner.test("100%高电平时间", calculate_high_time(1.0, 1.0) == 1.0)
    
    # 异常测试
    runner.test_exception("高电平时间超过周期", calculate_duty_cycle, ValueError, 2.0, 1.0)
    runner.test_exception("周期为0", calculate_duty_cycle, ValueError, 0.5, 0)
    runner.test_exception("占空比>1", calculate_high_time, ValueError, 1.5, 1.0)
    runner.test_exception("占空比<0", calculate_high_time, ValueError, -0.1, 1.0)


def test_pulse_analysis(runner: TestRunner):
    """测试脉冲分析"""
    print("\n📈 脉冲分析测试")
    
    # 分析方波
    square = generate_square_wave(10, 1.0, 44100, 0.5)
    result = analyze_pulse_signal(square, 44100)
    runner.test("脉冲计数>0", result['pulse_count'] > 0)
    runner.test("平均占空比约50%", abs(result['avg_duty_cycle'] - 0.5) < 0.1)
    runner.test("频率约10Hz", abs(result['frequency'] - 10) < 1)
    
    # 分析不同占空比
    square_25 = generate_square_wave(10, 1.0, 44100, 0.25)
    result_25 = analyze_pulse_signal(square_25, 44100)
    runner.test("25%占空比分析", result_25['avg_duty_cycle'] < 0.4)
    
    # 空信号
    empty_result = analyze_pulse_signal([])
    runner.test("空信号分析", empty_result['pulse_count'] == 0)


def test_pulse_detection(runner: TestRunner):
    """测试脉冲检测"""
    print("\n🔍 脉冲检测测试")
    
    # 检测脉冲序列
    pulses = generate_pulse_train(10, 1.0, 0.01)
    detected = detect_pulses(pulses, 44100, threshold=0.5)
    runner.test("检测到脉冲", len(detected) > 0)
    runner.test("检测脉冲数量约10", abs(len(detected) - 10) <= 1)
    
    # 检测脉冲属性
    if detected:
        first_pulse = detected[0]
        runner.test("脉冲有时间戳", first_pulse.timestamp >= 0)
        runner.test("脉冲有值", first_pulse.value > 0)
        runner.test("脉冲有持续时间", first_pulse.duration > 0)
    
    # 计数测试
    count = count_pulses(pulses)
    runner.test("脉冲计数约10", abs(count - 10) <= 1)
    
    # 空信号
    empty_detected = detect_pulses([], 44100)
    runner.test("空信号无脉冲", len(empty_detected) == 0)
    
    empty_count = count_pulses([])
    runner.test("空信号计数0", empty_count == 0)


def test_heartbeat(runner: TestRunner):
    """测试心跳模拟"""
    print("\n❤️ 心跳模拟测试")
    
    # 基本心跳生成
    heartbeat = simulate_heartbeat(5.0)
    runner.test("心跳正确长度", len(heartbeat) == 220500)  # 5秒 * 44100
    runner.test("心跳有信号", max(heartbeat) > 0)
    
    # 自定义模式
    pattern = HeartbeatPattern(
        base_bpm=60,
        variability=10,
        double_beat=True
    )
    custom_heartbeat = simulate_heartbeat(5.0, pattern)
    runner.test("自定义心跳正确长度", len(custom_heartbeat) == 220500)
    
    # 单跳模式
    single_pattern = HeartbeatPattern(
        base_bpm=72,
        double_beat=False
    )
    single_heartbeat = simulate_heartbeat(5.0, single_pattern)
    runner.test("单跳模式正确长度", len(single_heartbeat) == 220500)
    
    # 心跳分析
    analysis = analyze_heartbeat(heartbeat)
    runner.test("分析有估计BPM", analysis['estimated_bpm'] > 0)
    runner.test("分析有脉冲计数", analysis['pulse_count'] > 0)
    runner.test("分析有规律性", 0 <= analysis['regularity'] <= 1)
    
    # 空心跳分析
    empty_analysis = analyze_heartbeat([])
    runner.test("空心跳分析", empty_analysis['estimated_bpm'] == 0)


def test_note_frequency(runner: TestRunner):
    """测试音符频率转换"""
    print("\n🎹 音符频率测试")
    
    # 音符转频率
    runner.test("A4 = 440Hz", note_to_frequency('A4') == 440.0)
    runner.test("A3 = 220Hz", abs(note_to_frequency('A3') - 220) < 0.01)
    runner.test("A5 = 880Hz", abs(note_to_frequency('A5') - 880) < 0.01)
    
    # C4测试（中间C）
    c4_freq = note_to_frequency('C4')
    runner.test("C4约261.63Hz", abs(c4_freq - 261.63) < 0.01)
    
    # 升号测试
    csharp4_freq = note_to_frequency('C#4')
    runner.test("C#4 > C4", csharp4_freq > c4_freq)
    
    # 频率转音符
    runner.test("440Hz = A4", frequency_to_note(440) == 'A4')
    runner.test("220Hz = A3", frequency_to_note(220) == 'A3')
    runner.test("880Hz = A5", frequency_to_note(880) == 'A5')
    
    # 往返转换
    for note in ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']:
        freq = note_to_frequency(note)
        back = frequency_to_note(freq)
        runner.test(f"往返转换 {note}", back == note)
    
    # 异常测试
    runner.test_exception("无效音符", note_to_frequency, ValueError, 'H4')
    runner.test_exception("频率为0", frequency_to_note, ValueError, 0)


def test_harmonics(runner: TestRunner):
    """测试谐波生成"""
    print("\n🔊 谐波测试")
    
    # 基本谐波
    harmonics = get_harmonics(440, 4)
    runner.test("谐波数量正确", len(harmonics) == 4)
    runner.test("基频正确", harmonics[0] == 440.0)
    runner.test("第2谐波正确", harmonics[1] == 880.0)
    runner.test("第3谐波正确", harmonics[2] == 1320.0)
    runner.test("第4谐波正确", harmonics[3] == 1760.0)
    
    # 不同基频
    harmonics_c = get_harmonics(261.63, 3)
    runner.test("C4谐波数量", len(harmonics_c) == 3)
    runner.test("C4基频", abs(harmonics_c[0] - 261.63) < 0.01)
    
    # 异常测试
    runner.test_exception("基频为0", get_harmonics, ValueError, 0, 4)
    runner.test_exception("谐波数为0", get_harmonics, ValueError, 440, 0)


def test_signal_utils(runner: TestRunner):
    """测试信号工具"""
    print("\n🛠️ 信号工具测试")
    
    # 混合信号
    s1 = [1.0, 0.5, 0.0]
    s2 = [0.0, 0.5, 1.0]
    mixed = mix_signals(s1, s2)
    runner.test("混合信号长度", len(mixed) == 3)
    runner.test("混合信号值", mixed[0] == 0.5)
    runner.test("混合信号值", mixed[1] == 0.5)
    runner.test("混合信号值", mixed[2] == 0.5)
    
    # 带权重混合
    weighted = mix_signals(s1, s2, weights=[0.75, 0.25])
    runner.test("加权混合长度", len(weighted) == 3)
    runner.test("加权混合值", abs(weighted[0] - 0.75) < 0.001)
    
    # 归一化
    normalized = normalize_signal([0, 2, -4, 6])
    runner.test("归一化长度", len(normalized) == 4)
    runner.test("归一化最大值", max(normalized) == 1.0)
    runner.test("归一化最小值约-0.67", abs(min(normalized) - (-0.6666666666666666)) < 0.001)
    
    # 空信号归一化
    empty_norm = normalize_signal([])
    runner.test("空归一化", len(empty_norm) == 0)
    
    # 零信号归一化
    zero_norm = normalize_signal([0, 0, 0])
    runner.test("零归一化", zero_norm == [0, 0, 0])
    
    # 放大
    amplified = amplify_signal([0.5, 1.0], 2.0)
    runner.test("放大长度", len(amplified) == 2)
    runner.test("放大值", amplified[0] == 1.0)
    runner.test("放大值", amplified[1] == 2.0)
    
    # 限幅
    clipped = clip_signal([0.5, 1.5, -0.3, -1.5], 1.0)
    runner.test("限幅长度", len(clipped) == 4)
    runner.test("限幅正值", clipped[1] == 1.0)
    runner.test("限幅负值", clipped[3] == -1.0)
    runner.test("限幅中间值", clipped[0] == 0.5)
    
    # 自定义限幅值
    clipped_05 = clip_signal([0.3, 0.8], 0.5)
    runner.test("自定义限幅", clipped_05[1] == 0.5)


def test_pulse_data_class(runner: TestRunner):
    """测试Pulse数据类"""
    print("\n📦 Pulse数据类测试")
    
    pulse = Pulse(timestamp=1.5, value=0.8, duration=0.1)
    runner.test("Pulse时间戳", pulse.timestamp == 1.5)
    runner.test("Pulse值", pulse.value == 0.8)
    runner.test("Pulse持续时间", pulse.duration == 0.1)
    runner.test("Pulse字符串表示", "Pulse" in repr(pulse))


def test_pulse_sequence_class(runner: TestRunner):
    """测试PulseSequence数据类"""
    print("\n📦 PulseSequence数据类测试")
    
    pulses = [
        Pulse(timestamp=0.0, value=1.0, duration=0.1),
        Pulse(timestamp=0.5, value=1.0, duration=0.1),
        Pulse(timestamp=1.0, value=1.0, duration=0.1)
    ]
    seq = PulseSequence(
        pulses=pulses,
        total_duration=1.5,
        frequency=2.0,
        duty_cycle=0.2
    )
    
    runner.test("序列长度", len(seq) == 3)
    runner.test("序列迭代", len(list(seq)) == 3)
    runner.test("序列索引", seq[0].timestamp == 0.0)
    runner.test("获取值列表", len(seq.get_values()) == 3)
    runner.test("获取时间戳列表", len(seq.get_timestamps()) == 3)


def test_generator(runner: TestRunner):
    """测试脉冲生成器"""
    print("\n⚡ 脉冲生成器测试")
    
    # 基本生成器
    gen = pulse_generator(10, 0.5)
    
    # 生成几个样本（不实际等待）
    runner.test("生成器可迭代", hasattr(gen, '__iter__'))
    runner.test("生成器可next", hasattr(gen, '__next__'))
    
    # 异常测试 - 生成器在迭代时抛出异常
    try:
        gen_zero_freq = pulse_generator(0, 0.5)
        next(gen_zero_freq)
        runner.test("频率为0应抛出异常", False, "未抛出异常")
    except ValueError:
        runner.test("频率为0抛出异常", True)
    
    try:
        gen_zero_duty = pulse_generator(10, 0)
        next(gen_zero_duty)
        runner.test("占空比为0应抛出异常", False, "未抛出异常")
    except ValueError:
        runner.test("占空比为0抛出异常", True)


def test_wave_type_enum(runner: TestRunner):
    """测试波形类型枚举"""
    print("\n📊 波形类型枚举测试")
    
    runner.test("SQUARE枚举", WaveType.SQUARE.value == "square")
    runner.test("SINE枚举", WaveType.SINE.value == "sine")
    runner.test("TRIANGLE枚举", WaveType.TRIANGLE.value == "triangle")
    runner.test("SAWTOOTH枚举", WaveType.SAWTOOTH.value == "sawtooth")
    runner.test("PULSE枚举", WaveType.PULSE.value == "pulse")


def test_edge_cases(runner: TestRunner):
    """测试边界情况"""
    print("\n🔬 边界值测试")
    
    # 极小频率
    tiny_freq = generate_sine_wave(0.1, 0.1, 44100)
    runner.test("极小频率正弦波", len(tiny_freq) == 4410)
    
    # 极大频率（采样限制）
    # 注意：频率过高会有混叠，但不应该崩溃
    high_freq = generate_sine_wave(20000, 0.1, 44100)
    runner.test("高频率正弦波", len(high_freq) == 4410)
    
    # 极小持续时间
    tiny_dur = generate_square_wave(440, 0.001, 44100)
    runner.test("极小持续时间", len(tiny_dur) == 44)
    
    # 极小振幅
    tiny_amp = generate_sine_wave(440, 0.1, 44100, amplitude=0.01)
    runner.test("极小振幅最大值", max(tiny_amp) <= 0.01)
    
    # 极短脉冲
    tiny_pulse = generate_pulse_train(1, 0.1, 0.001, 44100)
    runner.test("极短脉冲", len(tiny_pulse) == 4410)
    
    # 极低BPM
    low_bpm_interval = bpm_to_interval_ms(20)
    runner.test("极低BPM间隔", low_bpm_interval == 3000.0)
    
    # 极高BPM
    high_bpm_interval = bpm_to_interval_ms(300)
    runner.test("极高BPM间隔", high_bpm_interval == 200.0)
    
    # 极长音符
    low_note_freq = note_to_frequency('C1')
    runner.test("低音符C1", low_note_freq < 100)
    
    # 极高音符
    high_note_freq = note_to_frequency('C8')
    runner.test("高音符C8", high_note_freq > 4000)


def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("Pulse Utils 测试套件")
    print("="*60)
    
    runner = TestRunner()
    
    test_wave_generation(runner)
    test_bpm_tools(runner)
    test_metronome(runner)
    test_duty_cycle(runner)
    test_pulse_analysis(runner)
    test_pulse_detection(runner)
    test_heartbeat(runner)
    test_note_frequency(runner)
    test_harmonics(runner)
    test_signal_utils(runner)
    test_pulse_data_class(runner)
    test_pulse_sequence_class(runner)
    test_generator(runner)
    test_wave_type_enum(runner)
    test_edge_cases(runner)
    
    return runner.summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)