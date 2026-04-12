"""
Audio Utilities Module
音频处理工具函数库

提供常用的音频文件处理功能，包括 WAV/AIFF/AU 文件读写、格式转换、
音频信息提取、音量调整、音频拼接等。仅使用 Python 标准库，零依赖。

Author: AllToolkit
Version: 1.0.0
"""

import wave
import aifc
import sunau
import audioop
import contextlib
import io
from pathlib import Path
from typing import Union, Optional, Tuple, List, BinaryIO
from dataclasses import dataclass


PathLike = Union[str, Path]


@dataclass
class AudioInfo:
    """音频文件信息"""
    filepath: str
    format: str  # 'WAV', 'AIFF', 'AU'
    channels: int
    sample_width: int  # bytes per sample
    framerate: int  # Hz
    frames: int
    duration: float  # seconds
    compression_type: Optional[str] = None
    compression_name: Optional[str] = None


class AudioUtilsError(Exception):
    """音频工具异常基类"""
    pass


class UnsupportedFormatError(AudioUtilsError):
    """不支持的音频格式"""
    pass


class InvalidAudioError(AudioUtilsError):
    """无效的音频文件"""
    pass


def get_audio_info(filepath: PathLike) -> AudioInfo:
    """
    获取音频文件信息
    
    功能：读取音频文件的基本信息，包括格式、采样率、声道数、时长等。
    
    Args:
        filepath: 音频文件路径，支持 WAV/AIFF/AU 格式
    
    Returns:
        AudioInfo 数据类，包含音频文件的详细信息
    
    Raises:
        UnsupportedFormatError: 不支持的文件格式
        InvalidAudioError: 文件不是有效的音频文件
    
    Examples:
        >>> info = get_audio_info('sample.wav')
        >>> print(f"Duration: {info.duration:.2f}s, Channels: {info.channels}")
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    suffix = path.suffix.lower()
    
    try:
        if suffix == '.wav':
            with wave.open(str(path), 'rb') as wf:
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()
                frames = wf.getnframes()
                duration = frames / framerate if framerate > 0 else 0
                return AudioInfo(
                    filepath=str(path),
                    format='WAV',
                    channels=channels,
                    sample_width=sample_width,
                    framerate=framerate,
                    frames=frames,
                    duration=duration
                )
        elif suffix in ('.aif', '.aiff'):
            with aifc.open(str(path), 'rb') as af:
                channels = af.getnchannels()
                sample_width = af.getsampwidth()
                framerate = af.getframerate()
                frames = af.getnframes()
                duration = frames / framerate if framerate > 0 else 0
                comp_type = af.getcomptype()
                comp_name = af.getcompname()
                return AudioInfo(
                    filepath=str(path),
                    format='AIFF',
                    channels=channels,
                    sample_width=sample_width,
                    framerate=framerate,
                    frames=frames,
                    duration=duration,
                    compression_type=comp_type,
                    compression_name=comp_name
                )
        elif suffix in ('.au', '.snd'):
            with sunau.open(str(path), 'rb') as sf:
                channels = sf.getnchannels()
                sample_width = sf.getsampwidth()
                framerate = sf.getframerate()
                frames = sf.getnframes()
                duration = frames / framerate if framerate > 0 else 0
                comp_type = sf.getcomptype()
                comp_name = sf.getcompname()
                return AudioInfo(
                    filepath=str(path),
                    format='AU',
                    channels=channels,
                    sample_width=sample_width,
                    framerate=framerate,
                    frames=frames,
                    duration=duration,
                    compression_type=comp_type,
                    compression_name=comp_name
                )
        else:
            raise UnsupportedFormatError(f"Unsupported format: {suffix}")
    except (wave.Error, aifc.Error, sunau.Error) as e:
        raise InvalidAudioError(f"Invalid audio file: {e}")


def read_audio(filepath: PathLike) -> Tuple[bytes, int, int, int]:
    """
    读取音频文件原始数据
    
    功能：读取音频文件的原始 PCM 数据和参数。
    
    Args:
        filepath: 音频文件路径
    
    Returns:
        tuple: (raw_data, channels, sample_width, framerate)
            - raw_data: 原始 PCM 数据 (bytes)
            - channels: 声道数
            - sample_width: 每采样字节数
            - framerate: 采样率
    
    Examples:
        >>> data, ch, sw, fr = read_audio('sample.wav')
        >>> print(f"Read {len(data)} bytes of audio data")
    """
    path = Path(filepath)
    suffix = path.suffix.lower()
    
    try:
        if suffix == '.wav':
            with wave.open(str(path), 'rb') as wf:
                return (wf.readframes(wf.getnframes()), 
                        wf.getnchannels(), 
                        wf.getsampwidth(), 
                        wf.getframerate())
        elif suffix in ('.aif', '.aiff'):
            with aifc.open(str(path), 'rb') as af:
                return (af.readframes(af.getnframes()),
                        af.getnchannels(),
                        af.getsampwidth(),
                        af.getframerate())
        elif suffix in ('.au', '.snd'):
            with sunau.open(str(path), 'rb') as sf:
                return (sf.readframes(sf.getnframes()),
                        sf.getnchannels(),
                        sf.getsampwidth(),
                        sf.getframerate())
        else:
            raise UnsupportedFormatError(f"Unsupported format: {suffix}")
    except (wave.Error, aifc.Error, sunau.Error) as e:
        raise InvalidAudioError(f"Failed to read audio: {e}")


def write_audio(filepath: PathLike, data: bytes, channels: int, 
                sample_width: int, framerate: int) -> bool:
    """
    写入 WAV 音频文件
    
    功能：将原始 PCM 数据写入 WAV 文件。
    
    Args:
        filepath: 输出文件路径
        data: 原始 PCM 数据
        channels: 声道数 (1=单声道，2=立体声)
        sample_width: 每采样字节数 (1=8-bit, 2=16-bit, 4=32-bit)
        framerate: 采样率 (Hz)，常见值：8000, 16000, 44100, 48000
    
    Returns:
        写入成功返回 True，失败返回 False
    
    Examples:
        >>> # 生成 1 秒 440Hz 正弦波 (16-bit, 单声道，44100Hz)
        >>> import math
        >>> data = bytes()
        >>> for i in range(44100):
        ...     value = int(32767 * math.sin(2 * math.pi * 440 * i / 44100))
        ...     data += value.to_bytes(2, 'little', signed=True)
        >>> write_audio('tone.wav', data, channels=1, sample_width=2, framerate=44100)
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with wave.open(str(path), 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(framerate)
            wf.writeframes(data)
        return True
    except (wave.Error, IOError, OSError) as e:
        return False


def adjust_volume(filepath: PathLike, output_path: PathLike, 
                  factor: float) -> bool:
    """
    调整音频音量
    
    功能：按比例调整音频文件的音量，支持放大和衰减。
    
    Args:
        filepath: 输入音频文件路径
        output_path: 输出音频文件路径
        factor: 音量因子 (0.0-1.0=衰减，1.0=不变，>1.0=放大)
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Examples:
        >>> adjust_volume('quiet.wav', 'loud.wav', factor=2.0)  # 放大 2 倍
        >>> adjust_volume('loud.wav', 'quiet.wav', factor=0.5)  # 衰减到 50%
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        # 使用 audioop 模块调整音量
        adjusted_data = audioop.mul(data, sample_width, factor)
        
        return write_audio(output_path, adjusted_data, channels, sample_width, framerate)
    except (AudioUtilsError, IOError):
        return False


def fade_in(filepath: PathLike, output_path: PathLike, 
            duration: float = 1.0) -> bool:
    """
    添加淡入效果
    
    功能：在音频开头添加线性淡入效果。
    
    Args:
        filepath: 输入音频文件路径
        output_path: 输出音频文件路径
        duration: 淡入时长（秒），默认为 1.0 秒
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Examples:
        >>> fade_in('music.wav', 'music_fadein.wav', duration=2.0)
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        # 计算淡入采样数
        fade_samples = int(duration * framerate)
        total_samples = len(data) // (channels * sample_width)
        
        if fade_samples > total_samples:
            fade_samples = total_samples
        
        # 手动实现淡入：逐样本应用增益
        faded_data = bytearray(data)
        bytes_per_sample = sample_width * channels
        
        for i in range(fade_samples):
            # 计算增益 (0.0 -> 1.0)
            gain = i / fade_samples
            
            # 对每个声道应用增益
            for ch in range(channels):
                sample_offset = i * bytes_per_sample + ch * sample_width
                
                # 读取样本
                if sample_width == 1:
                    original = faded_data[sample_offset]
                    faded = int(128 + (original - 128) * gain)
                    faded_data[sample_offset] = max(0, min(255, faded))
                elif sample_width == 2:
                    original = int.from_bytes(
                        faded_data[sample_offset:sample_offset+2], 
                        'little', signed=True
                    )
                    faded = int(original * gain)
                    faded_data[sample_offset:sample_offset+2] = \
                        faded.to_bytes(2, 'little', signed=True)
                elif sample_width == 4:
                    original = int.from_bytes(
                        faded_data[sample_offset:sample_offset+4], 
                        'little', signed=True
                    )
                    faded = int(original * gain)
                    faded_data[sample_offset:sample_offset+4] = \
                        faded.to_bytes(4, 'little', signed=True)
        
        return write_audio(output_path, bytes(faded_data), channels, sample_width, framerate)
    except (AudioUtilsError, IOError):
        return False


def fade_out(filepath: PathLike, output_path: PathLike, 
             duration: float = 1.0) -> bool:
    """
    添加淡出效果
    
    功能：在音频结尾添加线性淡出效果。
    
    Args:
        filepath: 输入音频文件路径
        output_path: 输出音频文件路径
        duration: 淡出时长（秒），默认为 1.0 秒
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Examples:
        >>> fade_out('music.wav', 'music_fadeout.wav', duration=2.0)
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        # 计算淡出采样数
        fade_samples = int(duration * framerate)
        total_samples = len(data) // (channels * sample_width)
        
        if fade_samples > total_samples:
            fade_samples = total_samples
        
        # 淡出起始位置
        start_sample = total_samples - fade_samples
        
        # 手动实现淡出：逐样本应用增益
        faded_data = bytearray(data)
        bytes_per_sample = sample_width * channels
        
        for i in range(start_sample, total_samples):
            # 计算增益 (1.0 -> 0.0)
            progress = (i - start_sample) / fade_samples
            gain = 1.0 - progress
            
            # 对每个声道应用增益
            for ch in range(channels):
                sample_offset = i * bytes_per_sample + ch * sample_width
                
                # 读取样本
                if sample_width == 1:
                    original = faded_data[sample_offset]
                    faded = int(128 + (original - 128) * gain)
                    faded_data[sample_offset] = max(0, min(255, faded))
                elif sample_width == 2:
                    original = int.from_bytes(
                        faded_data[sample_offset:sample_offset+2], 
                        'little', signed=True
                    )
                    faded = int(original * gain)
                    faded_data[sample_offset:sample_offset+2] = \
                        faded.to_bytes(2, 'little', signed=True)
                elif sample_width == 4:
                    original = int.from_bytes(
                        faded_data[sample_offset:sample_offset+4], 
                        'little', signed=True
                    )
                    faded = int(original * gain)
                    faded_data[sample_offset:sample_offset+4] = \
                        faded.to_bytes(4, 'little', signed=True)
        
        return write_audio(output_path, bytes(faded_data), channels, sample_width, framerate)
    except (AudioUtilsError, IOError):
        return False


def concatenate_audio(filepaths: List[PathLike], output_path: PathLike) -> bool:
    """
    拼接多个音频文件
    
    功能：将多个音频文件按顺序拼接成一个文件。
    
    Args:
        filepaths: 输入音频文件路径列表
        output_path: 输出音频文件路径
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Raises:
        InvalidAudioError: 音频文件参数不匹配（采样率、声道数等）
    
    Examples:
        >>> concatenate_audio(['intro.wav', 'main.wav', 'outro.wav'], 'full.wav')
    """
    if not filepaths:
        return False
    
    try:
        # 读取第一个文件作为基准
        all_data = []
        base_channels = None
        base_sample_width = None
        base_framerate = None
        
        for fp in filepaths:
            data, channels, sample_width, framerate = read_audio(fp)
            
            # 检查参数一致性
            if base_channels is None:
                base_channels = channels
                base_sample_width = sample_width
                base_framerate = framerate
            else:
                if channels != base_channels:
                    raise InvalidAudioError(
                        f"Channel mismatch: {fp} has {channels} channels, "
                        f"expected {base_channels}"
                    )
                if sample_width != base_sample_width:
                    raise InvalidAudioError(
                        f"Sample width mismatch: {fp} has {sample_width} bytes, "
                        f"expected {base_sample_width}"
                    )
                if framerate != base_framerate:
                    raise InvalidAudioError(
                        f"Framerate mismatch: {fp} has {framerate} Hz, "
                        f"expected {base_framerate}"
                    )
            
            all_data.append(data)
        
        # 拼接数据
        combined_data = b''.join(all_data)
        
        return write_audio(output_path, combined_data, base_channels, 
                          base_sample_width, base_framerate)
    except (AudioUtilsError, IOError) as e:
        return False


def extract_segment(filepath: PathLike, output_path: PathLike,
                    start_time: float, end_time: float) -> bool:
    """
    提取音频片段
    
    功能：从音频文件中提取指定时间段的片段。
    
    Args:
        filepath: 输入音频文件路径
        output_path: 输出音频文件路径
        start_time: 起始时间（秒）
        end_time: 结束时间（秒）
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Examples:
        >>> extract_segment('song.wav', 'chorus.wav', start_time=60.0, end_time=90.0)
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        # 计算帧范围
        bytes_per_frame = channels * sample_width
        start_frame = int(start_time * framerate)
        end_frame = int(end_time * framerate)
        
        start_byte = start_frame * bytes_per_frame
        end_byte = end_frame * bytes_per_frame
        
        # 边界检查
        if start_byte < 0:
            start_byte = 0
        if end_byte > len(data):
            end_byte = len(data)
        if start_byte >= end_byte:
            return False
        
        # 提取片段
        segment_data = data[start_byte:end_byte]
        
        return write_audio(output_path, segment_data, channels, sample_width, framerate)
    except (AudioUtilsError, IOError):
        return False


def convert_to_mono(filepath: PathLike, output_path: PathLike) -> bool:
    """
    转换为单声道
    
    功能：将立体声音频转换为单声道（混合左右声道）。
    
    Args:
        filepath: 输入音频文件路径
        output_path: 输出音频文件路径
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Examples:
        >>> convert_to_mono('stereo.wav', 'mono.wav')
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        if channels == 1:
            # 已经是单声道，直接复制
            return write_audio(output_path, data, 1, sample_width, framerate)
        
        # 使用 audioop 转换为单声道
        mono_data = audioop.tomono(data, sample_width, 0.5, 0.5)
        
        return write_audio(output_path, mono_data, 1, sample_width, framerate)
    except (AudioUtilsError, IOError):
        return False


def reverse_audio(filepath: PathLike, output_path: PathLike) -> bool:
    """
    反转音频
    
    功能：将音频数据反向播放（倒放效果）。
    
    Args:
        filepath: 输入音频文件路径
        output_path: 输出音频文件路径
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Examples:
        >>> reverse_audio('normal.wav', 'reversed.wav')
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        # 使用 audioop 反转
        reversed_data = audioop.reverse(data, sample_width)
        
        return write_audio(output_path, reversed_data, channels, sample_width, framerate)
    except (AudioUtilsError, IOError):
        return False


def generate_sine_wave(frequency: float, duration: float, 
                       framerate: int = 44100, amplitude: float = 0.5,
                       channels: int = 1, sample_width: int = 2) -> bytes:
    """
    生成正弦波音频
    
    功能：生成指定频率和时长的正弦波音频数据。
    
    Args:
        frequency: 频率 (Hz)
        duration: 时长（秒）
        framerate: 采样率 (Hz)，默认为 44100
        amplitude: 振幅 (0.0-1.0)，默认为 0.5
        channels: 声道数，默认为 1
        sample_width: 每采样字节数，默认为 2 (16-bit)
    
    Returns:
        原始 PCM 数据 (bytes)
    
    Examples:
        >>> # 生成 440Hz A 音，1 秒时长
        >>> data = generate_sine_wave(440.0, 1.0)
        >>> write_audio('a4.wav', data, channels=1, sample_width=2, framerate=44100)
    """
    import math
    
    total_samples = int(duration * framerate)
    
    if sample_width == 1:
        # 8-bit unsigned
        max_val = 255
        center = 128
        audio_data = bytes(
            int(center + amplitude * max_val * math.sin(2 * math.pi * frequency * i / framerate))
            for i in range(total_samples)
        )
    elif sample_width == 2:
        # 16-bit signed
        max_val = 32767
        audio_data = b''.join(
            int(amplitude * max_val * math.sin(2 * math.pi * frequency * i / framerate))
            .to_bytes(2, 'little', signed=True)
            for i in range(total_samples)
        )
    elif sample_width == 4:
        # 32-bit signed
        max_val = 2147483647
        audio_data = b''.join(
            int(amplitude * max_val * math.sin(2 * math.pi * frequency * i / framerate))
            .to_bytes(4, 'little', signed=True)
            for i in range(total_samples)
        )
    else:
        raise ValueError(f"Unsupported sample_width: {sample_width}")
    
    # 如果是多声道，复制数据
    if channels > 1:
        audio_data = audioop.tostereo(audio_data, sample_width, 1.0, 1.0)
    
    return audio_data


def detect_silence(filepath: PathLike, threshold: int = 100) -> List[Tuple[float, float]]:
    """
    检测静音片段
    
    功能：检测音频文件中的静音片段，返回静音时间段列表。
    
    Args:
        filepath: 输入音频文件路径
        threshold: 静音阈值（0-65535），值越小检测越严格，默认为 100
    
    Returns:
        静音时间段列表 [(start_time, end_time), ...]
    
    Examples:
        >>> silences = detect_silence('speech.wav', threshold=200)
        >>> for start, end in silences:
        ...     print(f"Silence from {start:.2f}s to {end:.2f}s")
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        # 手动实现静音检测
        total_samples = len(data) // (channels * sample_width)
        bytes_per_sample = sample_width * channels
        
        silence_ranges = []
        in_silence = False
        silence_start = 0
        
        for i in range(total_samples):
            # 计算该样本所有声道的平均振幅
            sample_offset = i * bytes_per_sample
            total_amplitude = 0
            
            for ch in range(channels):
                ch_offset = sample_offset + ch * sample_width
                
                if sample_width == 1:
                    # 8-bit unsigned, center=128
                    value = abs(data[ch_offset] - 128)
                elif sample_width == 2:
                    value = abs(int.from_bytes(data[ch_offset:ch_offset+2], 'little', signed=True))
                elif sample_width == 4:
                    value = abs(int.from_bytes(data[ch_offset:ch_offset+4], 'little', signed=True))
                else:
                    value = 0
                
                total_amplitude += value
            
            avg_amplitude = total_amplitude / channels if channels > 0 else 0
            
            # 判断是否为静音
            is_silent = avg_amplitude < threshold
            
            if is_silent and not in_silence:
                # 开始静音
                in_silence = True
                silence_start = i
            elif not is_silent and in_silence:
                # 结束静音
                in_silence = False
                silence_ranges.append((silence_start, i))
        
        # 如果文件以静音结束
        if in_silence:
            silence_ranges.append((silence_start, total_samples))
        
        # 转换为时间
        result = []
        for start_sample, end_sample in silence_ranges:
            start_time = start_sample / framerate
            end_time = end_sample / framerate
            result.append((start_time, end_time))
        
        return result
    except (AudioUtilsError, IOError):
        return []


def get_peak_amplitude(filepath: PathLike) -> float:
    """
    获取音频峰值振幅
    
    功能：计算音频文件的峰值振幅（最大音量）。
    
    Args:
        filepath: 输入音频文件路径
    
    Returns:
        峰值振幅 (0.0-1.0)，失败返回 0.0
    
    Examples:
        >>> peak = get_peak_amplitude('audio.wav')
        >>> print(f"Peak amplitude: {peak:.2%}")
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        # 使用 audioop 获取最大值
        max_val = audioop.max(data, sample_width)
        
        # 归一化到 0-1
        if sample_width == 1:
            return max_val / 128.0  # 8-bit unsigned, center=128
        elif sample_width == 2:
            return max_val / 32767.0  # 16-bit signed
        elif sample_width == 4:
            return max_val / 2147483647.0  # 32-bit signed
        else:
            return 0.0
    except (AudioUtilsError, IOError):
        return 0.0


def normalize_audio(filepath: PathLike, output_path: PathLike,
                    target_peak: float = 0.95) -> bool:
    """
    音频标准化
    
    功能：将音频音量标准化到指定峰值。
    
    Args:
        filepath: 输入音频文件路径
        output_path: 输出音频文件路径
        target_peak: 目标峰值 (0.0-1.0)，默认为 0.95
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Examples:
        >>> normalize_audio('quiet.wav', 'normalized.wav', target_peak=0.9)
    """
    try:
        current_peak = get_peak_amplitude(filepath)
        
        if current_peak == 0:
            return False
        
        # 计算需要的增益
        gain = target_peak / current_peak
        
        return adjust_volume(filepath, output_path, gain)
    except (AudioUtilsError, IOError):
        return False


# 便捷函数
def create_tone(filepath: PathLike, frequency: float, duration: float,
                framerate: int = 44100) -> bool:
    """
    创建音调文件（便捷函数）
    
    功能：快速生成指定频率和时长的音调文件。
    
    Args:
        filepath: 输出文件路径
        frequency: 频率 (Hz)
        duration: 时长（秒）
        framerate: 采样率 (Hz)
    
    Returns:
        生成成功返回 True，失败返回 False
    
    Examples:
        >>> create_tone('beep.wav', 1000.0, 0.5)  # 1kHz, 0.5 秒
    """
    try:
        data = generate_sine_wave(frequency, duration, framerate)
        return write_audio(filepath, data, channels=1, sample_width=2, framerate=framerate)
    except (AudioUtilsError, IOError):
        return False


def split_stereo(filepath: PathLike, output_left: PathLike, 
                 output_right: PathLike) -> bool:
    """
    分离立体声声道
    
    功能：将立体声音频分离为左右两个单声道文件。
    
    Args:
        filepath: 输入立体声音频文件路径
        output_left: 左声道输出路径
        output_right: 右声道输出路径
    
    Returns:
        处理成功返回 True，失败返回 False
    
    Examples:
        >>> split_stereo('stereo.wav', 'left.wav', 'right.wav')
    """
    try:
        data, channels, sample_width, framerate = read_audio(filepath)
        
        if channels != 2:
            raise InvalidAudioError("Input must be stereo (2 channels)")
        
        # 分离声道
        left_data = audioop.tomono(data, sample_width, 1.0, 0.0)
        right_data = audioop.tomono(data, sample_width, 0.0, 1.0)
        
        success_left = write_audio(output_left, left_data, 1, sample_width, framerate)
        success_right = write_audio(output_right, right_data, 1, sample_width, framerate)
        
        return success_left and success_right
    except (AudioUtilsError, IOError):
        return False
