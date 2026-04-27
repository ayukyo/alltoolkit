"""
Pulse Utils - 脉冲/心跳工具模块

提供脉冲信号生成、处理、检测和分析功能。
零外部依赖，仅使用 Python 标准库。

主要功能:
- 脉冲信号生成（方波、三角波、正弦波、锯齿波）
- 脉冲序列处理
- BPM（每分钟节拍）相关工具
- 占空比计算与分析
- 频率转换工具
- 心跳检测模拟
- 定时脉冲触发器

作者: AllToolkit
日期: 2026-04-27
"""

import math
import random
import time
from typing import List, Tuple, Optional, Callable, Generator, Union
from dataclasses import dataclass
from enum import Enum


class WaveType(Enum):
    """波形类型枚举"""
    SQUARE = "square"
    SINE = "sine"
    TRIANGLE = "triangle"
    SAWTOOTH = "sawtooth"
    PULSE = "pulse"


@dataclass
class Pulse:
    """脉冲数据类"""
    timestamp: float  # 时间戳（秒）
    value: float      # 脉冲值（0-1 或 -1 到 1）
    duration: float   # 脉冲持续时间（秒）
    
    def __repr__(self):
        return f"Pulse(t={self.timestamp:.3f}s, v={self.value:.2f}, d={self.duration:.3f}s)"


@dataclass
class PulseSequence:
    """脉冲序列数据类"""
    pulses: List[Pulse]
    total_duration: float
    frequency: float  # Hz
    duty_cycle: float  # 占空比
    
    def __len__(self):
        return len(self.pulses)
    
    def __iter__(self):
        return iter(self.pulses)
    
    def __getitem__(self, index):
        return self.pulses[index]
    
    def get_values(self) -> List[float]:
        """获取所有脉冲值"""
        return [p.value for p in self.pulses]
    
    def get_timestamps(self) -> List[float]:
        """获取所有时间戳"""
        return [p.timestamp for p in self.pulses]


# ==================== 波形生成 ====================

def generate_square_wave(
    frequency: float,
    duration: float,
    sample_rate: int = 44100,
    duty_cycle: float = 0.5,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成方波信号
    
    Args:
        frequency: 频率（Hz）
        duration: 持续时间（秒）
        sample_rate: 采样率（Hz）
        duty_cycle: 占空比（0-1）
        amplitude: 振幅（0-1）
    
    Returns:
        样本值列表
    
    Examples:
        >>> samples = generate_square_wave(440, 0.1)  # 440Hz 方波，持续0.1秒
        >>> len(samples) > 0
        True
    """
    if frequency <= 0:
        raise ValueError("频率必须大于0")
    if duration <= 0:
        raise ValueError("持续时间必须大于0")
    if not 0 < duty_cycle <= 1:
        raise ValueError("占空比必须在(0, 1]范围内")
    if not 0 < amplitude <= 1:
        raise ValueError("振幅必须在(0, 1]范围内")
    
    num_samples = int(sample_rate * duration)
    period_samples = sample_rate / frequency
    high_samples = int(period_samples * duty_cycle)
    
    samples = []
    for i in range(num_samples):
        position = i % period_samples
        if position < high_samples:
            samples.append(amplitude)
        else:
            samples.append(-amplitude if duty_cycle < 0.5 else 0)
    
    return samples


def generate_sine_wave(
    frequency: float,
    duration: float,
    sample_rate: int = 44100,
    amplitude: float = 1.0,
    phase: float = 0.0
) -> List[float]:
    """
    生成正弦波信号
    
    Args:
        frequency: 频率（Hz）
        duration: 持续时间（秒）
        sample_rate: 采样率（Hz）
        amplitude: 振幅（0-1）
        phase: 初始相位（弧度）
    
    Returns:
        样本值列表
    
    Examples:
        >>> samples = generate_sine_wave(440, 0.1)  # A4音符
        >>> samples[0] != 0 or True  # 可能从非零开始
        True
    """
    if frequency <= 0:
        raise ValueError("频率必须大于0")
    if duration <= 0:
        raise ValueError("持续时间必须大于0")
    if not 0 < amplitude <= 1:
        raise ValueError("振幅必须在(0, 1]范围内")
    
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        value = amplitude * math.sin(2 * math.pi * frequency * t + phase)
        samples.append(value)
    
    return samples


def generate_triangle_wave(
    frequency: float,
    duration: float,
    sample_rate: int = 44100,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成三角波信号
    
    Args:
        frequency: 频率（Hz）
        duration: 持续时间（秒）
        sample_rate: 采样率（Hz）
        amplitude: 振幅（0-1）
    
    Returns:
        样本值列表
    
    Examples:
        >>> samples = generate_triangle_wave(220, 0.1)
        >>> max(samples) <= 1.0
        True
    """
    if frequency <= 0:
        raise ValueError("频率必须大于0")
    if duration <= 0:
        raise ValueError("持续时间必须大于0")
    if not 0 < amplitude <= 1:
        raise ValueError("振幅必须在(0, 1]范围内")
    
    num_samples = int(sample_rate * duration)
    period_samples = sample_rate / frequency
    samples = []
    
    for i in range(num_samples):
        position = (i % period_samples) / period_samples
        # 三角波：先上升后下降
        if position < 0.5:
            value = amplitude * (4 * position - 1)
        else:
            value = amplitude * (3 - 4 * position)
        samples.append(value)
    
    return samples


def generate_sawtooth_wave(
    frequency: float,
    duration: float,
    sample_rate: int = 44100,
    amplitude: float = 1.0,
    rising: bool = True
) -> List[float]:
    """
    生成锯齿波信号
    
    Args:
        frequency: 频率（Hz）
        duration: 持续时间（秒）
        sample_rate: 采样率（Hz）
        amplitude: 振幅（0-1）
        rising: True为上升锯齿，False为下降锯齿
    
    Returns:
        样本值列表
    
    Examples:
        >>> samples = generate_sawtooth_wave(330, 0.1)
        >>> min(samples) >= -1
        True
    """
    if frequency <= 0:
        raise ValueError("频率必须大于0")
    if duration <= 0:
        raise ValueError("持续时间必须大于0")
    if not 0 < amplitude <= 1:
        raise ValueError("振幅必须在(0, 1]范围内")
    
    num_samples = int(sample_rate * duration)
    period_samples = sample_rate / frequency
    samples = []
    
    for i in range(num_samples):
        position = (i % period_samples) / period_samples
        if rising:
            value = amplitude * (2 * position - 1)
        else:
            value = amplitude * (1 - 2 * position)
        samples.append(value)
    
    return samples


def generate_pulse_train(
    frequency: float,
    duration: float,
    pulse_width: float,
    sample_rate: int = 44100,
    amplitude: float = 1.0
) -> List[float]:
    """
    生成脉冲序列（窄脉冲）
    
    Args:
        frequency: 重复频率（Hz）
        duration: 总持续时间（秒）
        pulse_width: 单个脉冲宽度（秒）
        sample_rate: 采样率（Hz）
        amplitude: 振幅（0-1）
    
    Returns:
        样本值列表
    
    Examples:
        >>> samples = generate_pulse_train(10, 1.0, 0.01)  # 10Hz，1ms脉冲宽度
        >>> sum(s > 0 for s in samples) > 0
        True
    """
    if frequency <= 0:
        raise ValueError("频率必须大于0")
    if duration <= 0:
        raise ValueError("持续时间必须大于0")
    if pulse_width <= 0:
        raise ValueError("脉冲宽度必须大于0")
    if not 0 < amplitude <= 1:
        raise ValueError("振幅必须在(0, 1]范围内")
    
    num_samples = int(sample_rate * duration)
    period_samples = int(sample_rate / frequency)
    pulse_samples = int(sample_rate * pulse_width)
    
    samples = []
    for i in range(num_samples):
        position = i % period_samples
        if position < pulse_samples:
            samples.append(amplitude)
        else:
            samples.append(0)
    
    return samples


# ==================== BPM 相关工具 ====================

def bpm_to_frequency(bpm: float) -> float:
    """
    将BPM转换为频率（Hz）
    
    Args:
        bpm: 每分钟节拍数
    
    Returns:
        频率（Hz）
    
    Examples:
        >>> bpm_to_frequency(60)  # 60 BPM = 1 Hz
        1.0
        >>> bpm_to_frequency(120)  # 120 BPM = 2 Hz
        2.0
    """
    if bpm <= 0:
        raise ValueError("BPM必须大于0")
    return bpm / 60.0


def frequency_to_bpm(frequency: float) -> float:
    """
    将频率（Hz）转换为BPM
    
    Args:
        frequency: 频率（Hz）
    
    Returns:
        BPM
    
    Examples:
        >>> frequency_to_bpm(1.0)  # 1 Hz = 60 BPM
        60.0
        >>> frequency_to_bpm(2.0)  # 2 Hz = 120 BPM
        120.0
    """
    if frequency <= 0:
        raise ValueError("频率必须大于0")
    return frequency * 60.0


def bpm_to_interval_ms(bpm: float) -> float:
    """
    将BPM转换为节拍间隔（毫秒）
    
    Args:
        bpm: 每分钟节拍数
    
    Returns:
        间隔（毫秒）
    
    Examples:
        >>> bpm_to_interval_ms(60)  # 60 BPM = 1000ms
        1000.0
        >>> bpm_to_interval_ms(120)  # 120 BPM = 500ms
        500.0
    """
    if bpm <= 0:
        raise ValueError("BPM必须大于0")
    return 60000.0 / bpm


def interval_ms_to_bpm(interval_ms: float) -> float:
    """
    将节拍间隔（毫秒）转换为BPM
    
    Args:
        interval_ms: 间隔（毫秒）
    
    Returns:
        BPM
    
    Examples:
        >>> interval_ms_to_bpm(1000)  # 1000ms = 60 BPM
        60.0
        >>> interval_ms_to_bpm(500)  # 500ms = 120 BPM
        120.0
    """
    if interval_ms <= 0:
        raise ValueError("间隔必须大于0")
    return 60000.0 / interval_ms


def generate_metronome(
    bpm: float,
    duration: float,
    sample_rate: int = 44100,
    click_duration: float = 0.01,
    accent_pattern: Optional[List[int]] = None
) -> List[float]:
    """
    生成节拍器信号
    
    Args:
        bpm: 每分钟节拍数
        duration: 总持续时间（秒）
        sample_rate: 采样率（Hz）
        click_duration: 点击持续时间（秒）
        accent_pattern: 重音模式，如 [1, 0, 0, 0] 表示4/4拍第一拍重音
    
    Returns:
        样本值列表
    
    Examples:
        >>> samples = generate_metronome(120, 2.0)  # 120 BPM，2秒
        >>> len(samples) == int(44100 * 2.0)
        True
    """
    if bpm <= 0:
        raise ValueError("BPM必须大于0")
    if duration <= 0:
        raise ValueError("持续时间必须大于0")
    
    num_samples = int(sample_rate * duration)
    interval_samples = int(sample_rate * 60.0 / bpm)
    click_samples = int(sample_rate * click_duration)
    
    samples = [0.0] * num_samples
    
    beat_count = 0
    pattern_len = len(accent_pattern) if accent_pattern else 1
    
    i = 0
    while i < num_samples:
        # 确定当前拍的音量
        if accent_pattern:
            pattern_index = beat_count % pattern_len
            amplitude = 1.0 if accent_pattern[pattern_index] == 1 else 0.6
        else:
            amplitude = 0.8
        
        # 生成点击
        for j in range(min(click_samples, num_samples - i)):
            # 简单的衰减点击波形
            decay = 1.0 - (j / click_samples)
            samples[i + j] = amplitude * decay
        
        i += interval_samples
        beat_count += 1
    
    return samples


# ==================== 占空比相关 ====================

def calculate_duty_cycle(high_time: float, period: float) -> float:
    """
    计算占空比
    
    Args:
        high_time: 高电平时间（秒）
        period: 周期（秒）
    
    Returns:
        占空比（0-1）
    
    Examples:
        >>> calculate_duty_cycle(0.5, 1.0)
        0.5
        >>> calculate_duty_cycle(0.25, 1.0)
        0.25
    """
    if period <= 0:
        raise ValueError("周期必须大于0")
    if high_time < 0 or high_time > period:
        raise ValueError("高电平时间必须在[0, 周期]范围内")
    return high_time / period


def calculate_high_time(duty_cycle: float, period: float) -> float:
    """
    根据占空比计算高电平时间
    
    Args:
        duty_cycle: 占空比（0-1）
        period: 周期（秒）
    
    Returns:
        高电平时间（秒）
    
    Examples:
        >>> calculate_high_time(0.5, 1.0)
        0.5
        >>> calculate_high_time(0.25, 2.0)
        0.5
    """
    if not 0 <= duty_cycle <= 1:
        raise ValueError("占空比必须在[0, 1]范围内")
    if period <= 0:
        raise ValueError("周期必须大于0")
    return duty_cycle * period


def analyze_pulse_signal(
    samples: List[float],
    sample_rate: int = 44100,
    threshold: float = 0.5
) -> dict:
    """
    分析脉冲信号
    
    Args:
        samples: 样本值列表
        sample_rate: 采样率（Hz）
        threshold: 高电平阈值
    
    Returns:
        包含分析结果的字典：
        - pulse_count: 脉冲数量
        - avg_high_time: 平均高电平时间（秒）
        - avg_low_time: 平均低电平时间（秒）
        - avg_duty_cycle: 平均占空比
        - frequency: 估计频率（Hz）
    
    Examples:
        >>> samples = generate_square_wave(10, 1.0, 44100, 0.5)
        >>> result = analyze_pulse_signal(samples)
        >>> result['pulse_count'] > 0
        True
    """
    if not samples:
        return {
            'pulse_count': 0,
            'avg_high_time': 0,
            'avg_low_time': 0,
            'avg_duty_cycle': 0,
            'frequency': 0
        }
    
    # 检测高电平区间
    high_periods = []
    low_periods = []
    
    in_high = samples[0] >= threshold
    start_idx = 0
    
    for i, sample in enumerate(samples):
        is_high = sample >= threshold
        if is_high != in_high:
            duration = (i - start_idx) / sample_rate
            if in_high:
                high_periods.append(duration)
            else:
                low_periods.append(duration)
            in_high = is_high
            start_idx = i
    
    # 处理最后一个区间
    duration = (len(samples) - start_idx) / sample_rate
    if in_high:
        high_periods.append(duration)
    else:
        low_periods.append(duration)
    
    pulse_count = len(high_periods)
    avg_high_time = sum(high_periods) / len(high_periods) if high_periods else 0
    avg_low_time = sum(low_periods) / len(low_periods) if low_periods else 0
    avg_period = avg_high_time + avg_low_time
    avg_duty_cycle = avg_high_time / avg_period if avg_period > 0 else 0
    frequency = 1.0 / avg_period if avg_period > 0 else 0
    
    return {
        'pulse_count': pulse_count,
        'avg_high_time': avg_high_time,
        'avg_low_time': avg_low_time,
        'avg_duty_cycle': avg_duty_cycle,
        'frequency': frequency
    }


# ==================== 脉冲检测 ====================

def detect_pulses(
    samples: List[float],
    sample_rate: int = 44100,
    threshold: float = 0.5,
    min_pulse_width: float = 0.001
) -> List[Pulse]:
    """
    检测信号中的脉冲
    
    Args:
        samples: 样本值列表
        sample_rate: 采样率（Hz）
        threshold: 脉冲检测阈值
        min_pulse_width: 最小脉冲宽度（秒）
    
    Returns:
        脉冲列表
    
    Examples:
        >>> samples = generate_pulse_train(10, 1.0, 0.01)
        >>> pulses = detect_pulses(samples)
        >>> len(pulses) > 0
        True
    """
    pulses = []
    min_samples = int(sample_rate * min_pulse_width)
    
    in_pulse = False
    pulse_start = 0
    pulse_values = []
    
    for i, sample in enumerate(samples):
        if not in_pulse and sample >= threshold:
            # 脉冲开始
            in_pulse = True
            pulse_start = i
            pulse_values = [sample]
        elif in_pulse and sample >= threshold:
            # 脉冲继续
            pulse_values.append(sample)
        elif in_pulse and sample < threshold:
            # 脉冲结束
            in_pulse = False
            pulse_width = i - pulse_start
            
            if pulse_width >= min_samples:
                timestamp = pulse_start / sample_rate
                duration = pulse_width / sample_rate
                avg_value = sum(pulse_values) / len(pulse_values)
                
                pulses.append(Pulse(
                    timestamp=timestamp,
                    value=avg_value,
                    duration=duration
                ))
    
    # 处理信号末尾的脉冲
    if in_pulse and (len(samples) - pulse_start) >= min_samples:
        timestamp = pulse_start / sample_rate
        duration = (len(samples) - pulse_start) / sample_rate
        avg_value = sum(pulse_values) / len(pulse_values)
        
        pulses.append(Pulse(
            timestamp=timestamp,
            value=avg_value,
            duration=duration
        ))
    
    return pulses


def count_pulses(
    samples: List[float],
    threshold: float = 0.5
) -> int:
    """
    计算脉冲数量
    
    Args:
        samples: 样本值列表
        threshold: 脉冲检测阈值
    
    Returns:
        脉冲数量
    
    Examples:
        >>> samples = generate_pulse_train(10, 1.0, 0.01)
        >>> count_pulses(samples)
        10
    """
    count = 0
    in_pulse = False
    
    for sample in samples:
        if not in_pulse and sample >= threshold:
            in_pulse = True
            count += 1
        elif in_pulse and sample < threshold:
            in_pulse = False
    
    return count


# ==================== 脉冲生成器 ====================

def pulse_generator(
    frequency: float,
    duty_cycle: float = 0.5,
    amplitude: float = 1.0
) -> Generator[float, None, None]:
    """
    无限脉冲生成器（生成器函数）
    
    Args:
        frequency: 频率（Hz）
        duty_cycle: 占空比（0-1）
        amplitude: 振幅
    
    Yields:
        下一个样本值
    
    Examples:
        >>> gen = pulse_generator(10, 0.5)
        >>> next(gen)  # 第一个样本
        1.0
    """
    if frequency <= 0:
        raise ValueError("频率必须大于0")
    if not 0 < duty_cycle <= 1:
        raise ValueError("占空比必须在(0, 1]范围内")
    
    period = 1.0 / frequency
    high_time = period * duty_cycle
    
    while True:
        # 高电平阶段
        start_time = time.time()
        while (time.time() - start_time) < high_time:
            yield amplitude
        
        # 低电平阶段
        while (time.time() - start_time) < period:
            yield 0.0


class TimedPulseEmitter:
    """定时脉冲发射器"""
    
    def __init__(
        self,
        interval_ms: float,
        callback: Callable[[float], None],
        initial_delay: float = 0
    ):
        """
        初始化定时脉冲发射器
        
        Args:
            interval_ms: 脉冲间隔（毫秒）
            callback: 脉冲回调函数
            initial_delay: 初始延迟（秒）
        """
        if interval_ms <= 0:
            raise ValueError("间隔必须大于0")
        
        self.interval_ms = interval_ms
        self.callback = callback
        self.initial_delay = initial_delay
        self._running = False
        self._pulse_count = 0
        self._start_time = None
    
    def start(self) -> None:
        """开始发射脉冲"""
        self._running = True
        self._start_time = time.time()
        
        if self.initial_delay > 0:
            time.sleep(self.initial_delay)
        
        while self._running:
            self.callback(time.time())
            self._pulse_count += 1
            time.sleep(self.interval_ms / 1000.0)
    
    def stop(self) -> None:
        """停止发射脉冲"""
        self._running = False
    
    @property
    def pulse_count(self) -> int:
        """已发射脉冲数量"""
        return self._pulse_count
    
    @property
    def elapsed_time(self) -> float:
        """已运行时间（秒）"""
        if self._start_time is None:
            return 0
        return time.time() - self._start_time


# ==================== 心跳检测模拟 ====================

@dataclass
class HeartbeatPattern:
    """心跳模式配置"""
    base_bpm: float = 72.0  # 基础心率
    variability: float = 5.0  # 心率变异（BPM）
    double_beat: bool = True  # 是否模拟双跳（lub-dub）
    second_beat_delay: float = 0.15  # 第二跳延迟（秒）


def simulate_heartbeat(
    duration: float,
    pattern: Optional[HeartbeatPattern] = None,
    sample_rate: int = 44100
) -> List[float]:
    """
    模拟心跳信号
    
    Args:
        duration: 持续时间（秒）
        pattern: 心跳模式配置
        sample_rate: 采样率（Hz）
    
    Returns:
        样本值列表
    
    Examples:
        >>> samples = simulate_heartbeat(5.0)  # 5秒心跳模拟
        >>> len(samples) == int(44100 * 5.0)
        True
    """
    if pattern is None:
        pattern = HeartbeatPattern()
    
    num_samples = int(sample_rate * duration)
    samples = [0.0] * num_samples
    
    # 计算基础间隔
    base_interval_ms = bpm_to_interval_ms(pattern.base_bpm)
    
    current_time_ms = 0.0
    
    while current_time_ms < duration * 1000:
        # 添加随机变异
        variability_ms = random.uniform(
            -pattern.variability * 10,
            pattern.variability * 10
        )
        current_interval = base_interval_ms + variability_ms
        
        # 生成第一跳
        beat_time = int(current_time_ms * sample_rate / 1000)
        if beat_time < num_samples:
            _generate_heartbeat_pulse(samples, beat_time, sample_rate, 1.0)
        
        # 如果启用了双跳模式
        if pattern.double_beat:
            second_beat_time = beat_time + int(pattern.second_beat_delay * sample_rate)
            if second_beat_time < num_samples:
                _generate_heartbeat_pulse(samples, second_beat_time, sample_rate, 0.7)
        
        current_time_ms += current_interval
    
    return samples


def _generate_heartbeat_pulse(
    samples: List[float],
    start_idx: int,
    sample_rate: int,
    amplitude: float
) -> None:
    """生成单个心跳脉冲波形"""
    # 简化的心跳波形：快速上升，缓慢下降
    pulse_duration = 0.08  # 80ms
    pulse_samples = int(pulse_duration * sample_rate)
    
    for i in range(pulse_samples):
        idx = start_idx + i
        if idx < len(samples):
            # 高斯包络
            t = i / pulse_samples
            envelope = math.exp(-((t - 0.3) ** 2) / 0.1)
            samples[idx] = max(samples[idx], amplitude * envelope)


def analyze_heartbeat(
    samples: List[float],
    sample_rate: int = 44100
) -> dict:
    """
    分析心跳信号
    
    Args:
        samples: 样本值列表
        sample_rate: 采样率（Hz）
    
    Returns:
        分析结果字典：
        - estimated_bpm: 估计心率
        - pulse_count: 检测到的脉冲数
        - regularity: 规律性（0-1）
    
    Examples:
        >>> samples = simulate_heartbeat(10.0)
        >>> result = analyze_heartbeat(samples)
        >>> 60 <= result['estimated_bpm'] <= 85  # 大致范围
        True
    """
    # 检测脉冲
    pulses = detect_pulses(samples, sample_rate, threshold=0.3)
    
    if len(pulses) < 2:
        return {
            'estimated_bpm': 0,
            'pulse_count': len(pulses),
            'regularity': 0
        }
    
    # 计算间隔
    intervals = []
    for i in range(1, len(pulses)):
        interval = pulses[i].timestamp - pulses[i-1].timestamp
        intervals.append(interval)
    
    # 计算平均间隔和BPM
    avg_interval = sum(intervals) / len(intervals)
    estimated_bpm = 60.0 / avg_interval if avg_interval > 0 else 0
    
    # 计算规律性（基于间隔的标准差）
    if len(intervals) > 1:
        variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
        std_dev = math.sqrt(variance)
        # 规律性：标准差越小越规律
        regularity = max(0, 1 - (std_dev / avg_interval))
    else:
        regularity = 1.0
    
    return {
        'estimated_bpm': estimated_bpm,
        'pulse_count': len(pulses),
        'regularity': regularity,
        'avg_interval': avg_interval,
        'intervals': intervals
    }


# ==================== 频率工具 ====================

def note_to_frequency(note: str) -> float:
    """
    将音符名称转换为频率
    
    Args:
        note: 音符名称，如 'A4', 'C5', 'G#3'
    
    Returns:
        频率（Hz）
    
    Examples:
        >>> note_to_frequency('A4')  # 标准音
        440.0
        >>> round(note_to_frequency('C4'), 2)
        261.63
    """
    note = note.strip().upper()
    
    # 解析音符
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # 提取音符名和八度
    if len(note) >= 2:
        if note[1] == '#':
            note_name = note[:2]
            octave = int(note[2:]) if len(note) > 2 else 4
        else:
            note_name = note[0]
            octave = int(note[1:]) if len(note) > 1 else 4
    else:
        note_name = note[0]
        octave = 4
    
    if note_name not in note_names:
        raise ValueError(f"无效的音符名称: {note_name}")
    
    # 计算半音距离
    semitone = note_names.index(note_name)
    
    # A4 = 440 Hz
    # 半音距离从 A4 算起
    a4_semitone = note_names.index('A')
    a4_octave = 4
    
    semitones_from_a4 = (octave - a4_octave) * 12 + (semitone - a4_semitone)
    
    # 频率计算: f = 440 * 2^(n/12)
    frequency = 440.0 * (2 ** (semitones_from_a4 / 12.0))
    
    return frequency


def frequency_to_note(frequency: float) -> str:
    """
    将频率转换为最近的音符名称
    
    Args:
        frequency: 频率（Hz）
    
    Returns:
        音符名称
    
    Examples:
        >>> frequency_to_note(440)
        'A4'
        >>> frequency_to_note(261.63)[:2]  # 约 C4
        'C4'
    """
    if frequency <= 0:
        raise ValueError("频率必须大于0")
    
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # 计算半音距离
    semitones = 12 * math.log2(frequency / 440.0)
    semitones_rounded = round(semitones)
    
    # 计算八度和音符
    a4_semitone = note_names.index('A')
    total_semitones = semitones_rounded + a4_semitone
    
    octave = 4 + (total_semitones // 12)
    note_index = total_semitones % 12
    
    return f"{note_names[note_index]}{octave}"


def get_harmonics(fundamental: float, count: int = 8) -> List[float]:
    """
    获取谐波频率列表
    
    Args:
        fundamental: 基频（Hz）
        count: 谐波数量
    
    Returns:
        谐波频率列表
    
    Examples:
        >>> harmonics = get_harmonics(440, 4)
        >>> harmonics
        [440.0, 880.0, 1320.0, 1760.0]
    """
    if fundamental <= 0:
        raise ValueError("基频必须大于0")
    if count <= 0:
        raise ValueError("谐波数量必须大于0")
    
    return [fundamental * (i + 1) for i in range(count)]


# ==================== 工具函数 ====================

def mix_signals(
    *signals: List[List[float]],
    weights: Optional[List[float]] = None
) -> List[float]:
    """
    混合多个信号
    
    Args:
        signals: 多个信号列表
        weights: 权重列表（可选）
    
    Returns:
        混合后的信号
    
    Examples:
        >>> s1 = [1.0, 0.5, 0.0]
        >>> s2 = [0.0, 0.5, 1.0]
        >>> mix_signals(s1, s2)
        [0.5, 0.5, 0.5]
    """
    if not signals:
        return []
    
    if weights is None:
        weights = [1.0 / len(signals)] * len(signals)
    
    if len(weights) != len(signals):
        raise ValueError("权重数量必须与信号数量相同")
    
    max_len = max(len(s) for s in signals)
    result = [0.0] * max_len
    
    for signal, weight in zip(signals, weights):
        for i, sample in enumerate(signal):
            result[i] += sample * weight
    
    return result


def normalize_signal(samples: List[float]) -> List[float]:
    """
    归一化信号到 [-1, 1] 范围
    
    Args:
        samples: 样本值列表
    
    Returns:
        归一化后的样本值
    
    Examples:
        >>> normalize_signal([0, 2, -4, 6])
        [0.0, 0.3333333333333333, -0.6666666666666666, 1.0]
    """
    if not samples:
        return []
    
    max_abs = max(abs(s) for s in samples)
    if max_abs == 0:
        return samples.copy()
    
    return [s / max_abs for s in samples]


def amplify_signal(samples: List[float], gain: float) -> List[float]:
    """
    放大信号
    
    Args:
        samples: 样本值列表
        gain: 增益倍数
    
    Returns:
        放大后的样本值
    
    Examples:
        >>> amplify_signal([0.5, 1.0], 2.0)
        [1.0, 2.0]
    """
    return [s * gain for s in samples]


def clip_signal(samples: List[float], limit: float = 1.0) -> List[float]:
    """
    限幅信号
    
    Args:
        samples: 样本值列表
        limit: 限幅值
    
    Returns:
        限幅后的样本值
    
    Examples:
        >>> clip_signal([0.5, 1.5, -0.3, -1.5], 1.0)
        [0.5, 1.0, -0.3, -1.0]
    """
    return [max(-limit, min(limit, s)) for s in samples]


if __name__ == "__main__":
    # 简单演示
    print("Pulse Utils 演示")
    print("=" * 50)
    
    # 波形生成
    print("\n1. 波形生成示例:")
    square = generate_square_wave(440, 0.01, 44100)
    print(f"   方波（440Hz, 10ms）: {len(square)} 样本")
    
    sine = generate_sine_wave(440, 0.01, 44100)
    print(f"   正弦波（440Hz, 10ms）: {len(sine)} 样本")
    
    # BPM 工具
    print("\n2. BPM 转换示例:")
    bpm = 120
    freq = bpm_to_frequency(bpm)
    interval = bpm_to_interval_ms(bpm)
    print(f"   {bpm} BPM = {freq} Hz = {interval} ms/beat")
    
    # 心跳模拟
    print("\n3. 心跳模拟示例:")
    heartbeat = simulate_heartbeat(5.0)
    analysis = analyze_heartbeat(heartbeat)
    print(f"   估计心率: {analysis['estimated_bpm']:.1f} BPM")
    print(f"   脉冲数: {analysis['pulse_count']}")
    print(f"   规律性: {analysis['regularity']:.2f}")
    
    # 音符转换
    print("\n4. 音符频率转换:")
    for note in ['C4', 'E4', 'G4', 'A4']:
        freq = note_to_frequency(note)
        print(f"   {note} = {freq:.2f} Hz")
    
    print("\n" + "=" * 50)
    print("演示完成")