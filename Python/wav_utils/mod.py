"""
WAV 音频文件工具集
==================

无依赖的 WAV 音频文件读写和处理工具。

功能：
- WAV 文件读取和解析
- WAV 文件生成和写入
- 音频格式转换
- 音频数据处理（静音检测、归一化、混音等）
- 零外部依赖，仅使用 Python 标准库

作者: AllToolkit 自动生成
日期: 2026-04-22
"""

import struct
import array
from typing import Union, Tuple, List, Optional, BinaryIO
from dataclasses import dataclass
from enum import Enum


class WavFormat(Enum):
    """WAV 音频格式枚举"""
    PCM = 1          # 线性 PCM
    FLOAT = 3        # IEEE 浮点
    ALAW = 6         # A-law
    MULAW = 7        # μ-law


@dataclass
class WavInfo:
    """WAV 文件元信息"""
    channels: int
    sample_rate: int
    bits_per_sample: int
    format_tag: int
    num_samples: int
    data_size: int
    
    @property
    def duration(self) -> float:
        """音频时长（秒）"""
        if self.sample_rate == 0 or self.channels == 0:
            return 0.0
        return self.num_samples / self.sample_rate
    
    @property
    def byte_rate(self) -> int:
        """字节率"""
        return self.sample_rate * self.channels * self.bits_per_sample // 8
    
    @property
    def block_align(self) -> int:
        """块对齐"""
        return self.channels * self.bits_per_sample // 8


class WavReader:
    """WAV 文件读取器"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._info: Optional[WavInfo] = None
        self._data_offset: int = 0
    
    def read_info(self) -> WavInfo:
        """读取 WAV 文件信息"""
        if self._info is not None:
            return self._info
        
        with open(self.filepath, 'rb') as f:
            # 读取 RIFF 头
            riff_id = f.read(4)
            if riff_id != b'RIFF':
                raise ValueError(f"不是有效的 WAV 文件: RIFF 头缺失")
            
            file_size = struct.unpack('<I', f.read(4))[0]
            wave_id = f.read(4)
            if wave_id != b'WAVE':
                raise ValueError(f"不是有效的 WAV 文件: WAVE 标识缺失")
            
            # 读取 chunks
            fmt_chunk = None
            data_chunk_size = None
            
            while True:
                chunk_id = f.read(4)
                if len(chunk_id) < 4:
                    break
                
                chunk_size = struct.unpack('<I', f.read(4))[0]
                
                if chunk_id == b'fmt ':
                    fmt_chunk = f.read(chunk_size)
                elif chunk_id == b'data':
                    data_chunk_size = chunk_size
                    self._data_offset = f.tell()
                    break
                else:
                    # 跳过其他 chunk
                    f.seek(chunk_size, 1)
            
            if fmt_chunk is None:
                raise ValueError("WAV 文件缺少 fmt chunk")
            if data_chunk_size is None:
                raise ValueError("WAV 文件缺少 data chunk")
            
            # 解析 fmt chunk
            format_tag = struct.unpack('<H', fmt_chunk[0:2])[0]
            channels = struct.unpack('<H', fmt_chunk[2:4])[0]
            sample_rate = struct.unpack('<I', fmt_chunk[4:8])[0]
            bits_per_sample = struct.unpack('<H', fmt_chunk[14:16])[0]
            
            # 计算样本数
            num_samples = data_chunk_size // (channels * bits_per_sample // 8)
            
            self._info = WavInfo(
                channels=channels,
                sample_rate=sample_rate,
                bits_per_sample=bits_per_sample,
                format_tag=format_tag,
                num_samples=num_samples,
                data_size=data_chunk_size
            )
            
        return self._info
    
    def read_samples(self) -> List[List[int]]:
        """
        读取所有音频样本
        
        返回:
            List[List[int]]: 每个通道的样本列表
        """
        info = self.read_info()
        
        with open(self.filepath, 'rb') as f:
            f.seek(self._data_offset)
            raw_data = f.read(info.data_size)
        
        # 根据位深解析样本
        if info.bits_per_sample == 8:
            samples = list(raw_data)
            # 8-bit 是无符号的，转换为有符号
            samples = [s - 128 for s in samples]
        elif info.bits_per_sample == 16:
            samples = list(struct.unpack(f'<{len(raw_data)//2}h', raw_data))
        elif info.bits_per_sample == 24:
            samples = []
            for i in range(0, len(raw_data), 3):
                b = raw_data[i:i+3]
                sample = b[0] | (b[1] << 8) | (b[2] << 16)
                if sample >= 0x800000:  # 负数
                    sample -= 0x1000000
                samples.append(sample)
        elif info.bits_per_sample == 32:
            samples = list(struct.unpack(f'<{len(raw_data)//4}i', raw_data))
        else:
            raise ValueError(f"不支持的位深: {info.bits_per_sample}")
        
        # 分离通道
        channels = info.channels
        result = [[] for _ in range(channels)]
        for i, sample in enumerate(samples):
            result[i % channels].append(sample)
        
        return result
    
    def read_samples_mono(self) -> List[int]:
        """
        读取单声道样本（多声道自动混合）
        
        返回:
            List[int]: 混合后的样本列表
        """
        channels = self.read_samples()
        if len(channels) == 1:
            return channels[0]
        
        # 混合多声道
        mono = []
        for i in range(len(channels[0])):
            total = sum(ch[i] for ch in channels)
            mono.append(total // len(channels))
        return mono


class WavWriter:
    """WAV 文件写入器"""
    
    def __init__(self, filepath: str, sample_rate: int = 44100, 
                 channels: int = 1, bits_per_sample: int = 16):
        self.filepath = filepath
        self.sample_rate = sample_rate
        self.channels = channels
        self.bits_per_sample = bits_per_sample
        self._samples: List[List[int]] = [[] for _ in range(channels)]
    
    def add_samples(self, samples: Union[List[int], List[List[int]]]) -> 'WavWriter':
        """
        添加样本数据
        
        参数:
            samples: 单声道样本列表或多声道样本列表
        
        返回:
            self (支持链式调用)
        """
        if isinstance(samples[0], list):
            # 多声道
            for i, ch_samples in enumerate(samples):
                if i < len(self._samples):
                    self._samples[i].extend(ch_samples)
        else:
            # 单声道
            if self.channels == 1:
                self._samples[0].extend(samples)
            else:
                # 复制到所有通道
                for ch in self._samples:
                    ch.extend(samples)
        
        return self
    
    def add_silence(self, duration_ms: int) -> 'WavWriter':
        """
        添加静音
        
        参数:
            duration_ms: 静音时长（毫秒）
        
        返回:
            self
        """
        num_samples = int(self.sample_rate * duration_ms / 1000)
        for ch in self._samples:
            ch.extend([0] * num_samples)
        return self
    
    def add_sine_wave(self, frequency: float, duration_ms: int, 
                       amplitude: float = 1.0) -> 'WavWriter':
        """
        添加正弦波
        
        参数:
            frequency: 频率（Hz）
            duration_ms: 时长（毫秒）
            amplitude: 振幅（0.0 - 1.0）
        
        返回:
            self
        """
        import math
        
        num_samples = int(self.sample_rate * duration_ms / 1000)
        max_val = (1 << (self.bits_per_sample - 1)) - 1
        
        for i in range(num_samples):
            t = i / self.sample_rate
            sample = int(amplitude * max_val * math.sin(2 * math.pi * frequency * t))
            for ch in self._samples:
                ch.append(sample)
        
        return self
    
    def write(self) -> WavInfo:
        """
        写入 WAV 文件
        
        返回:
            WavInfo: 文件信息
        """
        # 确定样本数（取最小通道长度）
        num_samples = min(len(ch) for ch in self._samples) if any(self._samples) else 0
        
        # 计算数据大小
        bytes_per_sample = self.bits_per_sample // 8
        data_size = num_samples * self.channels * bytes_per_sample
        
        # 获取最大/最小值用于裁剪
        max_val = (1 << (self.bits_per_sample - 1)) - 1
        min_val = -(1 << (self.bits_per_sample - 1))
        
        with open(self.filepath, 'wb') as f:
            # RIFF 头
            f.write(b'RIFF')
            f.write(struct.pack('<I', 36 + data_size))  # 文件大小 - 8
            f.write(b'WAVE')
            
            # fmt chunk
            f.write(b'fmt ')
            f.write(struct.pack('<I', 16))  # fmt chunk 大小
            f.write(struct.pack('<H', WavFormat.PCM.value))  # 格式
            f.write(struct.pack('<H', self.channels))  # 通道数
            f.write(struct.pack('<I', self.sample_rate))  # 采样率
            f.write(struct.pack('<I', self.sample_rate * self.channels * bytes_per_sample))  # 字节率
            f.write(struct.pack('<H', self.channels * bytes_per_sample))  # 块对齐
            f.write(struct.pack('<H', self.bits_per_sample))  # 位深
            
            # data chunk
            f.write(b'data')
            f.write(struct.pack('<I', data_size))
            
            # 写入样本数据
            for i in range(num_samples):
                for ch in range(self.channels):
                    sample = self._samples[ch][i] if ch < len(self._samples) and i < len(self._samples[ch]) else 0
                    
                    # 裁剪到有效范围
                    sample = max(min_val, min(max_val, sample))
                    
                    if self.bits_per_sample == 8:
                        f.write(struct.pack('<B', sample + 128))
                    elif self.bits_per_sample == 16:
                        f.write(struct.pack('<h', sample))
                    elif self.bits_per_sample == 24:
                        # 24-bit little-endian
                        b = sample & 0xFFFFFF
                        f.write(bytes([b & 0xFF, (b >> 8) & 0xFF, (b >> 16) & 0xFF]))
                    elif self.bits_per_sample == 32:
                        f.write(struct.pack('<i', sample))
        
        return WavInfo(
            channels=self.channels,
            sample_rate=self.sample_rate,
            bits_per_sample=self.bits_per_sample,
            format_tag=WavFormat.PCM.value,
            num_samples=num_samples,
            data_size=data_size
        )


class WavProcessor:
    """WAV 音频处理器"""
    
    @staticmethod
    def normalize(samples: List[int], target_peak: float = 0.9) -> List[int]:
        """
        归一化音频样本
        
        参数:
            samples: 样本列表
            target_peak: 目标峰值（0.0 - 1.0）
        
        返回:
            归一化后的样本列表
        """
        if not samples:
            return samples
        
        max_val = max(abs(s) for s in samples)
        if max_val == 0:
            return samples
        
        # 假设 16-bit
        scale = target_peak * 32767 / max_val
        return [int(s * scale) for s in samples]
    
    @staticmethod
    def amplify(samples: List[int], gain_db: float) -> List[int]:
        """
        增益调整
        
        参数:
            samples: 样本列表
            gain_db: 增益（分贝）
        
        返回:
            调整后的样本列表
        """
        import math
        
        gain_linear = 10 ** (gain_db / 20)
        return [max(-32768, min(32767, int(s * gain_linear))) for s in samples]
    
    @staticmethod
    def find_silence(samples: List[int], threshold: int = 500, 
                     min_duration_ms: int = 100, sample_rate: int = 44100) -> List[Tuple[int, int]]:
        """
        检测静音区间
        
        参数:
            samples: 样本列表
            threshold: 静音阈值
            min_duration_ms: 最小静音时长（毫秒）
            sample_rate: 采样率
        
        返回:
            List[Tuple[int, int]]: 静音区间的 (开始, 结束) 索引列表
        """
        min_samples = int(sample_rate * min_duration_ms / 1000)
        silence_regions = []
        
        in_silence = False
        silence_start = 0
        
        for i, s in enumerate(samples):
            if abs(s) < threshold:
                if not in_silence:
                    in_silence = True
                    silence_start = i
            else:
                if in_silence:
                    duration = i - silence_start
                    if duration >= min_samples:
                        silence_regions.append((silence_start, i))
                    in_silence = False
        
        # 检查文件结尾的静音
        if in_silence:
            duration = len(samples) - silence_start
            if duration >= min_samples:
                silence_regions.append((silence_start, len(samples)))
        
        return silence_regions
    
    @staticmethod
    def trim_silence(samples: List[int], threshold: int = 500, 
                     sample_rate: int = 44100) -> List[int]:
        """
        去除首尾静音
        
        参数:
            samples: 样本列表
            threshold: 静音阈值
            sample_rate: 采样率
        
        返回:
            去除静音后的样本列表
        """
        if not samples:
            return samples
        
        # 找到第一个非静音样本
        start = 0
        for i, s in enumerate(samples):
            if abs(s) >= threshold:
                start = i
                break
        
        # 找到最后一个非静音样本
        end = len(samples) - 1
        for i in range(len(samples) - 1, -1, -1):
            if abs(samples[i]) >= threshold:
                end = i
                break
        
        return samples[start:end + 1]
    
    @staticmethod
    def mix(sources: List[List[int]], weights: Optional[List[float]] = None) -> List[int]:
        """
        混合多个音频轨道
        
        参数:
            sources: 音频源列表
            weights: 各源权重（可选）
        
        返回:
            混合后的样本列表
        """
        if not sources:
            return []
        
        if weights is None:
            weights = [1.0 / len(sources)] * len(sources)
        
        # 确保权重数量与源数量匹配
        while len(weights) < len(sources):
            weights.append(weights[-1])
        
        max_len = max(len(s) for s in sources)
        result = []
        
        for i in range(max_len):
            total = 0
            for j, source in enumerate(sources):
                if i < len(source):
                    total += int(source[i] * weights[j])
            result.append(max(-32768, min(32767, total)))
        
        return result
    
    @staticmethod
    def resample(samples: List[int], from_rate: int, to_rate: int) -> List[int]:
        """
        简单重采样（线性插值）
        
        参数:
            samples: 样本列表
            from_rate: 原始采样率
            to_rate: 目标采样率
        
        返回:
            重采样后的样本列表
        """
        if not samples or from_rate == to_rate:
            return samples
        
        ratio = from_rate / to_rate
        new_length = int(len(samples) * to_rate / from_rate)
        result = []
        
        for i in range(new_length):
            pos = i * ratio
            idx = int(pos)
            
            if idx + 1 < len(samples):
                # 线性插值
                frac = pos - idx
                sample = int(samples[idx] * (1 - frac) + samples[idx + 1] * frac)
            else:
                sample = samples[idx] if idx < len(samples) else 0
            
            result.append(sample)
        
        return result
    
    @staticmethod
    def reverse(samples: List[int]) -> List[int]:
        """
        反转音频
        
        参数:
            samples: 样本列表
        
        返回:
            反转后的样本列表
        """
        return samples[::-1]
    
    @staticmethod
    def fade_in(samples: List[int], duration_ms: int, sample_rate: int = 44100) -> List[int]:
        """
        淡入效果
        
        参数:
            samples: 样本列表
            duration_ms: 淡入时长（毫秒）
            sample_rate: 采样率
        
        返回:
            处理后的样本列表
        """
        if not samples:
            return samples
        
        fade_samples = min(int(sample_rate * duration_ms / 1000), len(samples))
        result = samples.copy()
        
        for i in range(fade_samples):
            factor = i / fade_samples
            result[i] = int(samples[i] * factor)
        
        return result
    
    @staticmethod
    def fade_out(samples: List[int], duration_ms: int, sample_rate: int = 44100) -> List[int]:
        """
        淡出效果
        
        参数:
            samples: 样本列表
            duration_ms: 淡出时长（毫秒）
            sample_rate: 采样率
        
        返回:
            处理后的样本列表
        """
        if not samples:
            return samples
        
        fade_samples = min(int(sample_rate * duration_ms / 1000), len(samples))
        result = samples.copy()
        
        for i in range(fade_samples):
            factor = 1 - (i / fade_samples)
            idx = len(samples) - fade_samples + i
            result[idx] = int(samples[idx] * factor)
        
        return result


# 便捷函数
def read_wav(filepath: str) -> Tuple[WavInfo, List[List[int]]]:
    """
    读取 WAV 文件
    
    参数:
        filepath: 文件路径
    
    返回:
        (WavInfo, 样本列表)
    """
    reader = WavReader(filepath)
    info = reader.read_info()
    samples = reader.read_samples()
    return info, samples


def write_wav(filepath: str, samples: Union[List[int], List[List[int]]], 
              sample_rate: int = 44100, bits_per_sample: int = 16) -> WavInfo:
    """
    写入 WAV 文件
    
    参数:
        filepath: 文件路径
        samples: 样本数据（单声道或多声道）
        sample_rate: 采样率
        bits_per_sample: 位深
    
    返回:
        WavInfo: 文件信息
    """
    if isinstance(samples[0], list):
        channels = len(samples)
    else:
        channels = 1
        samples = [samples]
    
    writer = WavWriter(filepath, sample_rate, channels, bits_per_sample)
    writer.add_samples(samples)
    return writer.write()


def get_wav_info(filepath: str) -> WavInfo:
    """
    获取 WAV 文件信息
    
    参数:
        filepath: 文件路径
    
    返回:
        WavInfo: 文件信息
    """
    return WavReader(filepath).read_info()


def create_sine_wav(filepath: str, frequency: float, duration_ms: int,
                    sample_rate: int = 44100, amplitude: float = 1.0) -> WavInfo:
    """
    创建正弦波 WAV 文件
    
    参数:
        filepath: 文件路径
        frequency: 频率（Hz）
        duration_ms: 时长（毫秒）
        sample_rate: 采样率
        amplitude: 振幅（0.0 - 1.0）
    
    返回:
        WavInfo: 文件信息
    """
    writer = WavWriter(filepath, sample_rate, 1, 16)
    writer.add_sine_wave(frequency, duration_ms, amplitude)
    return writer.write()


if __name__ == '__main__':
    # 简单演示
    import os
    
    # 创建测试文件
    test_file = 'test_tone.wav'
    
    print("创建 440Hz 正弦波测试文件...")
    create_sine_wav(test_file, frequency=440, duration_ms=1000, amplitude=0.5)
    
    # 读取文件信息
    info = get_wav_info(test_file)
    print(f"文件信息:")
    print(f"  通道数: {info.channels}")
    print(f"  采样率: {info.sample_rate} Hz")
    print(f"  位深: {info.bits_per_sample} bits")
    print(f"  时长: {info.duration:.2f} 秒")
    print(f"  样本数: {info.num_samples}")
    
    # 读取样本
    reader = WavReader(test_file)
    samples = reader.read_samples_mono()
    print(f"读取了 {len(samples)} 个样本")
    
    # 清理
    os.remove(test_file)
    print("测试完成！")