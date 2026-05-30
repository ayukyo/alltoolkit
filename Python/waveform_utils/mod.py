"""
Waveform Utilities - 波形生成与分析工具

提供常见波形的生成、分析和变换功能，零外部依赖。
支持：正弦波、方波、锯齿波、三角波、脉冲波、噪声等。

应用场景：
- 音频合成与分析
- 信号处理教学
- 波形可视化
- 音频测试信号生成
"""

import math
import random
from typing import List, Tuple, Optional, Union, Callable
from enum import Enum


class WaveformType(Enum):
    """波形类型枚举"""
    SINE = "sine"
    SQUARE = "square"
    SAWTOOTH = "sawtooth"
    TRIANGLE = "triangle"
    PULSE = "pulse"
    WHITE_NOISE = "white_noise"
    PINK_NOISE = "pink_noise"
    SAWTOOTH_REVERSE = "sawtooth_reverse"


class WaveformGenerator:
    """波形生成器"""
    
    def __init__(self, sample_rate: int = 44100):
        """
        初始化波形生成器
        
        Args:
            sample_rate: 采样率（Hz），默认 44100
        """
        self.sample_rate = sample_rate
    
    def generate(
        self,
        waveform_type: WaveformType,
        frequency: float,
        duration: float,
        amplitude: float = 1.0,
        phase: float = 0.0,
        **kwargs
    ) -> List[float]:
        """
        生成指定类型的波形
        
        Args:
            waveform_type: 波形类型
            frequency: 频率（Hz）
            duration: 持续时间（秒）
            amplitude: 振幅（0.0-1.0）
            phase: 相位偏移（弧度）
            **kwargs: 额外参数（如脉冲波的占空比）
            
        Returns:
            波形采样点列表
        """
        num_samples = int(self.sample_rate * duration)
        
        generators = {
            WaveformType.SINE: self._sine_wave,
            WaveformType.SQUARE: self._square_wave,
            WaveformType.SAWTOOTH: self._sawtooth_wave,
            WaveformType.TRIANGLE: self._triangle_wave,
            WaveformType.PULSE: self._pulse_wave,
            WaveformType.WHITE_NOISE: self._white_noise,
            WaveformType.PINK_NOISE: self._pink_noise,
            WaveformType.SAWTOOTH_REVERSE: self._sawtooth_reverse_wave,
        }
        
        generator = generators.get(waveform_type, self._sine_wave)
        return generator(num_samples, frequency, amplitude, phase, **kwargs)
    
    def _sine_wave(
        self, 
        num_samples: int, 
        frequency: float, 
        amplitude: float, 
        phase: float,
        **kwargs
    ) -> List[float]:
        """生成正弦波"""
        samples = []
        for i in range(num_samples):
            t = i / self.sample_rate
            value = amplitude * math.sin(2 * math.pi * frequency * t + phase)
            samples.append(value)
        return samples
    
    def _square_wave(
        self, 
        num_samples: int, 
        frequency: float, 
        amplitude: float, 
        phase: float,
        **kwargs
    ) -> List[float]:
        """生成方波"""
        samples = []
        for i in range(num_samples):
            t = i / self.sample_rate
            angle = 2 * math.pi * frequency * t + phase
            value = amplitude if math.sin(angle) >= 0 else -amplitude
            samples.append(value)
        return samples
    
    def _sawtooth_wave(
        self, 
        num_samples: int, 
        frequency: float, 
        amplitude: float, 
        phase: float,
        **kwargs
    ) -> List[float]:
        """生成锯齿波（上升）"""
        samples = []
        period = self.sample_rate / frequency
        for i in range(num_samples):
            t = (i + phase / (2 * math.pi) * period) % period
            value = amplitude * (2 * t / period - 1)
            samples.append(value)
        return samples
    
    def _sawtooth_reverse_wave(
        self, 
        num_samples: int, 
        frequency: float, 
        amplitude: float, 
        phase: float,
        **kwargs
    ) -> List[float]:
        """生成反向锯齿波（下降）"""
        samples = self._sawtooth_wave(num_samples, frequency, amplitude, phase, **kwargs)
        return [-s for s in samples]
    
    def _triangle_wave(
        self, 
        num_samples: int, 
        frequency: float, 
        amplitude: float, 
        phase: float,
        **kwargs
    ) -> List[float]:
        """生成三角波"""
        samples = []
        period = self.sample_rate / frequency
        for i in range(num_samples):
            t = (i + phase / (2 * math.pi) * period) % period
            normalized = t / period
            if normalized < 0.5:
                value = amplitude * (4 * normalized - 1)
            else:
                value = amplitude * (3 - 4 * normalized)
            samples.append(value)
        return samples
    
    def _pulse_wave(
        self, 
        num_samples: int, 
        frequency: float, 
        amplitude: float, 
        phase: float,
        duty_cycle: float = 0.5,
        **kwargs
    ) -> List[float]:
        """
        生成脉冲波
        
        Args:
            duty_cycle: 占空比（0.0-1.0），默认 0.5
        """
        duty_cycle = max(0.0, min(1.0, duty_cycle))
        samples = []
        period = self.sample_rate / frequency
        for i in range(num_samples):
            t = (i + phase / (2 * math.pi) * period) % period
            normalized = t / period
            value = amplitude if normalized < duty_cycle else -amplitude
            samples.append(value)
        return samples
    
    def _white_noise(
        self, 
        num_samples: int, 
        frequency: float, 
        amplitude: float, 
        phase: float,
        seed: Optional[int] = None,
        **kwargs
    ) -> List[float]:
        """生成白噪声"""
        if seed is not None:
            random.seed(seed)
        return [random.uniform(-amplitude, amplitude) for _ in range(num_samples)]
    
    def _pink_noise(
        self, 
        num_samples: int, 
        frequency: float, 
        amplitude: float, 
        phase: float,
        **kwargs
    ) -> List[float]:
        """
        生成粉红噪声（1/f 噪声）
        使用 Voss-McCartney 算法
        """
        samples = []
        b = [0.0] * 7
        for i in range(num_samples):
            # 更新随机值
            white = random.uniform(-1, 1)
            b[0] = 0.99886 * b[0] + white * 0.0555179
            b[1] = 0.99332 * b[1] + white * 0.0750759
            b[2] = 0.96900 * b[2] + white * 0.1538520
            b[3] = 0.86650 * b[3] + white * 0.3104856
            b[4] = 0.55000 * b[4] + white * 0.5329522
            b[5] = -0.7616 * b[5] - white * 0.0168980
            pink = (b[0] + b[1] + b[2] + b[3] + b[4] + b[5] + b[6] + white * 0.5362)
            pink *= 0.11  # 缩放因子
            b[6] = white * 0.115926
            samples.append(pink * amplitude)
        return samples


class WaveformAnalyzer:
    """波形分析器"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def get_statistics(self, samples: List[float]) -> dict:
        """
        计算波形的统计信息
        
        Returns:
            包含 min, max, mean, rms, peak_to_peak 的字典
        """
        if not samples:
            return {
                "min": 0.0,
                "max": 0.0,
                "mean": 0.0,
                "rms": 0.0,
                "peak_to_peak": 0.0,
            }
        
        n = len(samples)
        min_val = min(samples)
        max_val = max(samples)
        mean = sum(samples) / n
        rms = math.sqrt(sum(s * s for s in samples) / n)
        
        return {
            "min": min_val,
            "max": max_val,
            "mean": mean,
            "rms": rms,
            "peak_to_peak": max_val - min_val,
        }
    
    def zero_crossing_rate(self, samples: List[float]) -> float:
        """
        计算过零率
        
        Returns:
            过零率（每秒过零次数）
        """
        if len(samples) < 2:
            return 0.0
        
        crossings = 0
        for i in range(1, len(samples)):
            if (samples[i-1] >= 0 and samples[i] < 0) or \
               (samples[i-1] < 0 and samples[i] >= 0):
                crossings += 1
        
        duration = len(samples) / self.sample_rate
        return crossings / duration if duration > 0 else 0.0
    
    def estimate_frequency(self, samples: List[float]) -> float:
        """
        使用过零法估算频率
        
        Returns:
            估算的频率（Hz）
        """
        zcr = self.zero_crossing_rate(samples)
        return zcr / 2.0
    
    def calculate_dc_offset(self, samples: List[float]) -> float:
        """
        计算 DC 偏移量
        
        Returns:
            DC 偏移量
        """
        if not samples:
            return 0.0
        return sum(samples) / len(samples)
    
    def remove_dc_offset(self, samples: List[float]) -> List[float]:
        """
        移除 DC 偏移
        
        Returns:
            移除 DC 偏移后的波形
        """
        dc = self.calculate_dc_offset(samples)
        return [s - dc for s in samples]
    
    def normalize(self, samples: List[float], target_peak: float = 1.0) -> List[float]:
        """
        归一化波形到目标峰值
        
        Args:
            samples: 输入波形
            target_peak: 目标峰值
            
        Returns:
            归一化后的波形
        """
        if not samples:
            return []
        
        max_abs = max(abs(s) for s in samples)
        if max_abs == 0:
            return samples
        
        scale = target_peak / max_abs
        return [s * scale for s in samples]
    
    def clip(self, samples: List[float], threshold: float = 1.0) -> List[float]:
        """
        限幅/削波
        
        Args:
            samples: 输入波形
            threshold: 限幅阈值
            
        Returns:
            限幅后的波形
        """
        return [max(-threshold, min(threshold, s)) for s in samples]
    
    def detect_silence(
        self, 
        samples: List[float], 
        threshold: float = 0.01,
        min_duration: float = 0.1
    ) -> List[Tuple[int, int]]:
        """
        检测静音区域
        
        Args:
            samples: 输入波形
            threshold: 静音阈值
            min_duration: 最小静音时长（秒）
            
        Returns:
            静音区域的 (start, end) 索引列表
        """
        min_samples = int(min_duration * self.sample_rate)
        silence_regions = []
        in_silence = False
        start = 0
        
        for i, s in enumerate(samples):
            if abs(s) < threshold:
                if not in_silence:
                    in_silence = True
                    start = i
            else:
                if in_silence:
                    if i - start >= min_samples:
                        silence_regions.append((start, i))
                    in_silence = False
        
        if in_silence and len(samples) - start >= min_samples:
            silence_regions.append((start, len(samples)))
        
        return silence_regions


class WaveformTransformer:
    """波形变换器"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def fade_in(
        self, 
        samples: List[float], 
        duration: float,
        curve: str = "linear"
    ) -> List[float]:
        """
        淡入效果
        
        Args:
            samples: 输入波形
            duration: 淡入时长（秒）
            curve: 曲线类型 (linear, exponential, logarithmic, cosine)
            
        Returns:
            应用淡入后的波形
        """
        num_fade = min(int(duration * self.sample_rate), len(samples))
        result = samples.copy()
        
        for i in range(num_fade):
            progress = i / num_fade
            if curve == "linear":
                factor = progress
            elif curve == "exponential":
                factor = progress ** 2
            elif curve == "logarithmic":
                factor = 1 - math.exp(-3 * progress)
            elif curve == "cosine":
                factor = (1 - math.cos(math.pi * progress)) / 2
            else:
                factor = progress
            
            result[i] = samples[i] * factor
        
        return result
    
    def fade_out(
        self, 
        samples: List[float], 
        duration: float,
        curve: str = "linear"
    ) -> List[float]:
        """
        淡出效果
        
        Args:
            samples: 输入波形
            duration: 淡出时长（秒）
            curve: 曲线类型
            
        Returns:
            应用淡出后的波形
        """
        num_fade = min(int(duration * self.sample_rate), len(samples))
        result = samples.copy()
        start = len(samples) - num_fade
        
        for i in range(num_fade):
            progress = i / num_fade
            if curve == "linear":
                factor = 1 - progress
            elif curve == "exponential":
                factor = (1 - progress) ** 2
            elif curve == "logarithmic":
                factor = math.exp(-3 * progress)
            elif curve == "cosine":
                factor = (1 + math.cos(math.pi * progress)) / 2
            else:
                factor = 1 - progress
            
            result[start + i] = samples[start + i] * factor
        
        return result
    
    def mix(
        self, 
        samples_list: List[List[float]], 
        weights: Optional[List[float]] = None
    ) -> List[float]:
        """
        混合多个波形
        
        Args:
            samples_list: 波形列表
            weights: 各波形的权重列表
            
        Returns:
            混合后的波形
        """
        if not samples_list:
            return []
        
        if weights is None:
            weights = [1.0] * len(samples_list)
        
        max_length = max(len(s) for s in samples_list)
        result = [0.0] * max_length
        
        for samples, weight in zip(samples_list, weights):
            for i, s in enumerate(samples):
                result[i] += s * weight
        
        return result
    
    def amplitude_modulate(
        self, 
        carrier: List[float], 
        modulator: List[float], 
        depth: float = 1.0
    ) -> List[float]:
        """
        振幅调制
        
        Args:
            carrier: 载波信号
            modulator: 调制信号
            depth: 调制深度 (0.0-1.0)
            
        Returns:
            调制后的波形
        """
        length = min(len(carrier), len(modulator))
        result = []
        
        for i in range(length):
            mod_factor = 1.0 + depth * modulator[i]
            result.append(carrier[i] * mod_factor)
        
        return result
    
    def time_stretch(
        self, 
        samples: List[float], 
        factor: float
    ) -> List[float]:
        """
        简单的时间拉伸（重采样）
        
        Args:
            samples: 输入波形
            factor: 拉伸因子 (>1 变慢，<1 变快)
            
        Returns:
            拉伸后的波形
        """
        if factor <= 0 or not samples:
            return []
        
        new_length = int(len(samples) * factor)
        result = []
        
        for i in range(new_length):
            src_idx = i / factor
            idx = int(src_idx)
            
            if idx + 1 < len(samples):
                # 线性插值
                frac = src_idx - idx
                interpolated = samples[idx] * (1 - frac) + samples[idx + 1] * frac
                result.append(interpolated)
            elif idx < len(samples):
                result.append(samples[idx])
        
        return result
    
    def reverse(self, samples: List[float]) -> List[float]:
        """反转波形"""
        return samples[::-1]
    
    def delay(
        self, 
        samples: List[float], 
        delay_time: float, 
        decay: float = 0.5,
        feedback: float = 0.0
    ) -> List[float]:
        """
        延迟效果
        
        Args:
            samples: 输入波形
            delay_time: 延迟时间（秒）
            decay: 延迟衰减
            feedback: 反馈量
            
        Returns:
            添加延迟后的波形
        """
        delay_samples = int(delay_time * self.sample_rate)
        result = samples.copy()
        
        # 添加延迟
        for i, s in enumerate(samples):
            if i + delay_samples < len(result):
                result[i + delay_samples] += s * decay
        
        # 添加反馈
        if feedback > 0:
            for iteration in range(1, 4):  # 最多 4 次反馈
                fb_delay = delay_samples * (iteration + 1)
                fb_decay = decay * (feedback ** iteration)
                for i, s in enumerate(samples):
                    if i + fb_delay < len(result):
                        result[i + fb_delay] += s * fb_decay
        
        return result


class WaveformVisualizer:
    """波形可视化辅助工具（返回可视化数据）"""
    
    @staticmethod
    def get_ascii_waveform(
        samples: List[float], 
        width: int = 60, 
        height: int = 10
    ) -> str:
        """
        生成 ASCII 波形图
        
        Args:
            samples: 输入波形
            width: 图形宽度
            height: 图形高度
            
        Returns:
            ASCII 波形图字符串
        """
        if not samples:
            return ""
        
        # 降采样到目标宽度
        step = max(1, len(samples) // width)
        downsampled = [samples[i] for i in range(0, len(samples), step)][:width]
        
        # 归一化
        max_abs = max(abs(s) for s in downsampled) if downsampled else 1
        if max_abs == 0:
            max_abs = 1
        normalized = [s / max_abs for s in downsampled]
        
        # 创建画布
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        mid = height // 2
        
        # 绘制中线
        for x in range(width):
            canvas[mid][x] = '-'
        
        # 绘制波形
        for x, val in enumerate(normalized):
            y = mid - int(val * (mid - 1))
            y = max(0, min(height - 1, y))
            canvas[y][x] = '*'
        
        # 转换为字符串
        lines = [''.join(row) for row in canvas]
        return '\n'.join(lines)
    
    @staticmethod
    def get_histogram(
        samples: List[float], 
        bins: int = 20, 
        width: int = 40
    ) -> str:
        """
        生成振幅直方图
        
        Args:
            samples: 输入波形
            bins: 直方图区间数
            width: 图形宽度
            
        Returns:
            ASCII 直方图字符串
        """
        if not samples:
            return ""
        
        # 计算直方图
        min_val = min(samples)
        max_val = max(samples)
        range_val = max_val - min_val
        
        if range_val == 0:
            return "所有样本值相同"
        
        bin_counts = [0] * bins
        for s in samples:
            idx = int((s - min_val) / range_val * (bins - 1))
            idx = max(0, min(bins - 1, idx))
            bin_counts[idx] += 1
        
        max_count = max(bin_counts)
        if max_count == 0:
            max_count = 1
        
        # 绘制直方图
        lines = []
        for i, count in enumerate(bin_counts):
            bar_width = int(count / max_count * width)
            bar = '█' * bar_width
            bin_start = min_val + range_val * i / bins
            bin_end = min_val + range_val * (i + 1) / bins
            lines.append(f"[{bin_start:+.2f}, {bin_end:+.2f}] {bar} ({count})")
        
        return '\n'.join(lines)


# 便捷函数
def generate_waveform(
    waveform_type: Union[WaveformType, str],
    frequency: float,
    duration: float,
    amplitude: float = 1.0,
    sample_rate: int = 44100,
    **kwargs
) -> List[float]:
    """
    快速生成波形的便捷函数
    
    Args:
        waveform_type: 波形类型（枚举或字符串）
        frequency: 频率（Hz）
        duration: 持续时间（秒）
        amplitude: 振幅
        sample_rate: 采样率
        **kwargs: 额外参数
        
    Returns:
        波形采样点列表
    """
    if isinstance(waveform_type, str):
        waveform_type = WaveformType(waveform_type.lower())
    
    generator = WaveformGenerator(sample_rate)
    return generator.generate(waveform_type, frequency, duration, amplitude, **kwargs)


def analyze_waveform(samples: List[float], sample_rate: int = 44100) -> dict:
    """
    快速分析波形的便捷函数
    
    Args:
        samples: 波形数据
        sample_rate: 采样率
        
    Returns:
        包含统计信息的字典
    """
    analyzer = WaveformAnalyzer(sample_rate)
    stats = analyzer.get_statistics(samples)
    stats["zero_crossing_rate"] = analyzer.zero_crossing_rate(samples)
    stats["estimated_frequency"] = analyzer.estimate_frequency(samples)
    stats["dc_offset"] = analyzer.calculate_dc_offset(samples)
    return stats


def create_envelope(
    attack: float,
    decay: float,
    sustain: float,
    release: float,
    total_duration: float,
    sample_rate: int = 44100,
    sustain_level: float = 0.7
) -> List[float]:
    """
    创建 ADSR 包络
    
    Args:
        attack: 起音时间（秒）
        decay: 衰减时间（秒）
        sustain: 保持时间（秒）
        release: 释放时间（秒）
        total_duration: 总时长（秒）
        sample_rate: 采样率
        sustain_level: 保持电平
        
    Returns:
        包络曲线
    """
    num_samples = int(total_duration * sample_rate)
    envelope = [0.0] * num_samples
    
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    sustain_samples = int(sustain * sample_rate)
    release_samples = int(release * sample_rate)
    
    idx = 0
    
    # Attack phase
    for i in range(min(attack_samples, num_samples - idx)):
        envelope[idx] = i / attack_samples
        idx += 1
    
    # Decay phase
    for i in range(min(decay_samples, num_samples - idx)):
        progress = i / decay_samples
        envelope[idx] = 1.0 - (1.0 - sustain_level) * progress
        idx += 1
    
    # Sustain phase
    for _ in range(min(sustain_samples, num_samples - idx)):
        envelope[idx] = sustain_level
        idx += 1
    
    # Release phase
    release_start = idx
    for i in range(min(release_samples, num_samples - idx)):
        progress = i / release_samples
        start_level = envelope[release_start - 1] if release_start > 0 else sustain_level
        envelope[idx] = start_level * (1.0 - progress)
        idx += 1
    
    return envelope[:num_samples]


def apply_envelope(samples: List[float], envelope: List[float]) -> List[float]:
    """
    将包络应用到波形
    
    Args:
        samples: 输入波形
        envelope: 包络曲线
        
    Returns:
        应用包络后的波形
    """
    length = min(len(samples), len(envelope))
    return [samples[i] * envelope[i] for i in range(length)]


if __name__ == "__main__":
    # 简单演示
    print("Waveform Utils Demo")
    print("=" * 50)
    
    # 生成不同类型的波形
    gen = WaveformGenerator(sample_rate=8000)
    
    print("\n1. 生成正弦波 (440Hz, 0.1s):")
    sine = gen.generate(WaveformType.SINE, 440, 0.1)
    print(f"   采样点数: {len(sine)}")
    print(f"   前10个采样: {[f'{s:.4f}' for s in sine[:10]]}")
    
    print("\n2. 生成方波 (440Hz, 0.1s):")
    square = gen.generate(WaveformType.SQUARE, 440, 0.1)
    print(f"   前10个采样: {[f'{s:.4f}' for s in square[:10]]}")
    
    print("\n3. 波形分析:")
    analyzer = WaveformAnalyzer(sample_rate=8000)
    stats = analyzer.get_statistics(sine)
    for key, val in stats.items():
        print(f"   {key}: {val:.6f}")
    
    print("\n4. ASCII 波形图 (三角波 440Hz):")
    triangle = gen.generate(WaveformType.TRIANGLE, 440, 0.1)
    print(WaveformVisualizer.get_ascii_waveform(triangle, width=50, height=8))
    
    print("\n5. 创建 ADSR 包络:")
    env = create_envelope(attack=0.01, decay=0.05, sustain=0.1, release=0.02, total_duration=0.18)
    print(f"   包络采样点数: {len(env)}")
    print(f"   峰值位置: {env.index(max(env))}")