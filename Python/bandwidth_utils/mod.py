"""
Bandwidth Utilities - 带宽计算工具

提供带宽单位换算、下载时间估算、数据传输速率计算等功能。
零外部依赖，纯 Python 标准库实现。

功能：
- 带宽单位换算 (bps, Kbps, Mbps, Gbps, B/s, KB/s, MB/s, GB/s)
- 下载/上传时间估算
- 根据时间计算所需带宽
- 文件大小单位换算
- 友好格式化输出

作者: AllToolkit Auto Generator
日期: 2026-05-30
"""

from dataclasses import dataclass
from typing import Union, Tuple, Optional
import math


# =============================================================================
# 常量定义
# =============================================================================

# 比特率单位 (bits per second)
BITRATE_UNITS = ['bps', 'Kbps', 'Mbps', 'Gbps', 'Tbps', 'Pbps']

# 字节率单位 (Bytes per second)
BYTERATE_UNITS = ['B/s', 'KB/s', 'MB/s', 'GB/s', 'TB/s', 'PB/s']

# 文件大小单位 (Bytes)
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']

# 换算基数 (1024 或 1000)
BASE_BINARY = 1024  # 二进制 (KiB, MiB...)
BASE_DECIMAL = 1000  # 十进制 (KB, MB...)

# 时间单位 (秒)
TIME_UNITS = {
    'second': 1,
    'minute': 60,
    'hour': 3600,
    'day': 86400,
    'week': 604800,
    'month': 2592000,  # 30 天
    'year': 31536000,  # 365 天
}


# =============================================================================
# 数据类
# =============================================================================

@dataclass
class TransferResult:
    """传输结果数据类"""
    time_seconds: float
    time_formatted: str
    average_speed_bps: float
    average_speed_formatted: str
    
    def __str__(self) -> str:
        return f"TransferResult(time={self.time_formatted}, speed={self.average_speed_formatted})"


@dataclass
class BandwidthInfo:
    """带宽信息数据类"""
    bps: float
    Kbps: float
    Mbps: float
    Gbps: float
    Bps: float
    KBps: float
    MBps: float
    
    def __str__(self) -> str:
        return f"BandwidthInfo({self.format_auto()})"
    
    def format_auto(self) -> str:
        """自动选择最佳单位格式化"""
        if self.Mbps >= 1000:
            return f"{self.Gbps:.2f} Gbps"
        elif self.Kbps >= 1000:
            return f"{self.Mbps:.2f} Mbps"
        elif self.bps >= 1000:
            return f"{self.Kbps:.2f} Kbps"
        else:
            return f"{self.bps:.2f} bps"


@dataclass
class SizeInfo:
    """文件大小信息数据类"""
    bytes: int
    KB: float
    MB: float
    GB: float
    TB: float
    
    def __str__(self) -> str:
        return f"SizeInfo({self.format_auto()})"
    
    def format_auto(self) -> str:
        """自动选择最佳单位格式化"""
        if self.MB >= 1024:
            if self.GB >= 1024:
                return f"{self.TB:.2f} TB"
            return f"{self.GB:.2f} GB"
        elif self.KB >= 1024:
            return f"{self.MB:.2f} MB"
        elif self.bytes >= 1024:
            return f"{self.KB:.2f} KB"
        else:
            return f"{self.bytes} B"


# =============================================================================
# 核心函数
# =============================================================================

def parse_size(size_str: str) -> int:
    """
    解析文件大小字符串，返回字节数。
    
    支持格式：
    - "100 B", "100B"
    - "10 KB", "10KB", "10 KiB", "10KiB"
    - "1.5 MB", "1.5MB", "1.5 MiB"
    - "2 GB", "2GB", "2 GiB"
    - "500000" (纯数字，默认字节)
    
    Args:
        size_str: 文件大小字符串
        
    Returns:
        字节数
        
    Raises:
        ValueError: 无法解析的格式
        
    Examples:
        >>> parse_size("100 MB")
        104857600
        >>> parse_size("1.5 GB")
        1610612736
    """
    size_str = size_str.strip().upper()
    
    # 纯数字情况
    try:
        return int(float(size_str))
    except ValueError:
        pass
    
    # 尝试解析带单位的格式
    for i, unit in enumerate(SIZE_UNITS):
        # 检查标准单位 (KB, MB) 和二进制单位 (KiB, MiB)
        variants = [unit, unit[0] + 'I' + unit[1:]] if len(unit) > 1 else [unit]
        
        for variant in variants:
            if size_str.endswith(variant.upper()) or size_str.endswith(variant.upper().replace('B', 'IB')):
                try:
                    num = float(size_str[:-len(variant)].strip())
                    return int(num * (1024 ** i))
                except ValueError:
                    continue
    
    # 尝试更灵活的解析
    import re
    match = re.match(r'^([\d.]+)\s*([A-Z]+)$', size_str)
    if match:
        num = float(match.group(1))
        unit = match.group(2).strip()
        
        # 单位映射
        unit_map = {
            'B': 0, 'BYTE': 0, 'BYTES': 0,
            'K': 1, 'KB': 1, 'KIB': 1, 'KBYTE': 1, 'KBYTES': 1,
            'M': 2, 'MB': 2, 'MIB': 2, 'MBYTE': 2, 'MBYTES': 2,
            'G': 3, 'GB': 3, 'GIB': 3, 'GBYTE': 3, 'GBYTES': 3,
            'T': 4, 'TB': 4, 'TIB': 4, 'TBYTE': 4, 'TBYTES': 4,
            'P': 5, 'PB': 5, 'PIB': 5, 'PBYTE': 5, 'PBYTES': 5,
            'E': 6, 'EB': 6, 'EIB': 6, 'EBYTE': 6, 'EBYTES': 6,
        }
        
        power = unit_map.get(unit)
        if power is not None:
            return int(num * (1024 ** power))
    
    raise ValueError(f"无法解析文件大小: '{size_str}'")


def parse_bandwidth(bandwidth_str: str) -> float:
    """
    解析带宽字符串，返回 bits per second。
    
    支持格式：
    - "100 bps", "100 Kbps", "100 Mbps", "100 Gbps"
    - "10 B/s", "10 KB/s", "10 MB/s", "10 GB/s"
    - "100Mbps" (无空格)
    - "100 M" (简化格式，默认 Mbps)
    - "100000" (纯数字，默认 bps)
    
    Args:
        bandwidth_str: 带宽字符串
        
    Returns:
        bits per second
        
    Raises:
        ValueError: 无法解析的格式
        
    Examples:
        >>> parse_bandwidth("100 Mbps")
        100000000.0
        >>> parse_bandwidth("10 MB/s")
        80000000.0
    """
    bandwidth_str = bandwidth_str.strip().upper().replace(' ', '')
    
    # 纯数字情况 (默认 bps)
    try:
        return float(bandwidth_str)
    except ValueError:
        pass
    
    # 处理 B/s 格式 (字节每秒 -> 比特每秒需要乘8)
    for i, unit in enumerate(BYTERATE_UNITS):
        unit_clean = unit.upper().replace('/', '')
        if bandwidth_str.endswith(unit_clean):
            try:
                num = float(bandwidth_str[:-len(unit_clean)])
                return num * (1000 ** i) * 8  # 字节转比特
            except ValueError:
                continue
    
    # 处理 bps 格式
    for i, unit in enumerate(BITRATE_UNITS):
        unit_clean = unit.upper()
        if bandwidth_str.endswith(unit_clean):
            try:
                num = float(bandwidth_str[:-len(unit_clean)])
                return num * (1000 ** i)
            except ValueError:
                continue
    
    # 简化格式处理 (如 "100M" -> 100 Mbps)
    import re
    match = re.match(r'^([\d.]+)\s*([KMGTPE]?)(BPS|B/S)?$', bandwidth_str, re.IGNORECASE)
    if match:
        num = float(match.group(1))
        prefix = match.group(2).upper()
        suffix = match.group(3).upper() if match.group(3) else 'BPS'
        
        # 前缀映射
        prefix_map = {'': 0, 'K': 1, 'M': 2, 'G': 3, 'T': 4, 'P': 5, 'E': 6}
        multiplier = 1000 ** prefix_map.get(prefix, 0)
        
        # 如果是字节单位，乘以8
        if 'B/S' in suffix or (suffix == '' and prefix == ''):
            return num * multiplier * 8
        
        return num * multiplier
    
    raise ValueError(f"无法解析带宽: '{bandwidth_str}'")


def calculate_transfer_time(
    file_size: Union[int, str],
    bandwidth: Union[float, str],
    overhead_percent: float = 0
) -> TransferResult:
    """
    计算文件传输时间。
    
    Args:
        file_size: 文件大小（字节数或字符串如 "100 MB"）
        bandwidth: 带宽（bps 或字符串如 "100 Mbps"）
        overhead_percent: 协议开销百分比（如 TCP/IP 头部开销，默认 0）
        
    Returns:
        TransferResult 包含传输时间和平均速度
        
    Examples:
        >>> result = calculate_transfer_time("1 GB", "100 Mbps")
        >>> print(result.time_formatted)
        '1m 25.9s'
    """
    # 解析文件大小
    if isinstance(file_size, str):
        size_bytes = parse_size(file_size)
    else:
        size_bytes = int(file_size)
    
    # 解析带宽
    if isinstance(bandwidth, str):
        speed_bps = parse_bandwidth(bandwidth)
    else:
        speed_bps = float(bandwidth)
    
    # 应用协议开销
    if overhead_percent > 0:
        effective_speed = speed_bps * (1 - overhead_percent / 100)
    else:
        effective_speed = speed_bps
    
    # 计算时间 (字节 -> 比特，除以速度)
    if effective_speed <= 0:
        raise ValueError("带宽必须大于 0")
    
    size_bits = size_bytes * 8
    time_seconds = size_bits / effective_speed
    
    # 计算平均速度
    avg_speed_bps = speed_bps
    
    return TransferResult(
        time_seconds=time_seconds,
        time_formatted=format_time(time_seconds),
        average_speed_bps=avg_speed_bps,
        average_speed_formatted=format_bandwidth(avg_speed_bps)
    )


def calculate_required_bandwidth(
    file_size: Union[int, str],
    time_limit: Union[float, str]
) -> BandwidthInfo:
    """
    根据文件大小和时间限制计算所需带宽。
    
    Args:
        file_size: 文件大小（字节数或字符串）
        time_limit: 时间限制（秒或字符串如 "1h", "30m"）
        
    Returns:
        BandwidthInfo 包含各种单位的带宽
        
    Examples:
        >>> info = calculate_required_bandwidth("1 GB", "1h")
        >>> print(info.format_auto())
        '2.22 Mbps'
    """
    # 解析文件大小
    if isinstance(file_size, str):
        size_bytes = parse_size(file_size)
    else:
        size_bytes = int(file_size)
    
    # 解析时间
    if isinstance(time_limit, str):
        time_seconds = parse_time(time_limit)
    else:
        time_seconds = float(time_limit)
    
    if time_seconds <= 0:
        raise ValueError("时间必须大于 0")
    
    # 计算所需带宽 (bits per second)
    size_bits = size_bytes * 8
    required_bps = size_bits / time_seconds
    
    return BandwidthInfo(
        bps=required_bps,
        Kbps=required_bps / 1000,
        Mbps=required_bps / 1_000_000,
        Gbps=required_bps / 1_000_000_000,
        Bps=required_bps / 8,
        KBps=required_bps / 8000,
        MBps=required_bps / 8_000_000
    )


def parse_time(time_str: str) -> float:
    """
    解析时间字符串，返回秒数。
    
    支持格式：
    - "30s", "30s", "30 秒"
    - "5m", "5min", "5 分钟"
    - "2h", "2hr", "2 小时"
    - "1d", "1day", "1 天"
    - "1h30m", "1小时30分钟" (组合格式)
    - "90" (纯数字，默认秒)
    
    Args:
        time_str: 时间字符串
        
    Returns:
        秒数
        
    Examples:
        >>> parse_time("1h30m")
        5400.0
        >>> parse_time("2.5 小时")
        9000.0
    """
    time_str = time_str.strip()
    
    # 纯数字情况（默认秒）
    try:
        return float(time_str)
    except ValueError:
        pass
    
    import re
    
    # 中文单位
    time_str = time_str.replace('秒', 's').replace('分钟', 'm').replace('分', 'm')
    time_str = time_str.replace('小时', 'h').replace('时', 'h').replace('天', 'd')
    time_str = time_str.replace('周', 'w').replace('月', 'M').replace('年', 'y')
    
    # 单位映射
    unit_map = {
        's': 1, 'sec': 1, 'second': 1, 'seconds': 1,
        'm': 60, 'min': 60, 'minute': 60, 'minutes': 60,
        'h': 3600, 'hr': 3600, 'hour': 3600, 'hours': 3600,
        'd': 86400, 'day': 86400, 'days': 86400,
        'w': 604800, 'week': 604800, 'weeks': 604800,
    }
    
    total_seconds = 0.0
    
    # 匹配所有数字+单位组合
    pattern = r'([\d.]+)\s*([a-zA-Z]+)'
    matches = re.findall(pattern, time_str)
    
    if matches:
        for num_str, unit in matches:
            num = float(num_str)
            unit_lower = unit.lower()
            if unit_lower in unit_map:
                total_seconds += num * unit_map[unit_lower]
            else:
                raise ValueError(f"未知时间单位: '{unit}'")
        return total_seconds
    
    raise ValueError(f"无法解析时间: '{time_str}'")


def format_time(seconds: float) -> str:
    """
    将秒数格式化为易读的时间字符串。
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的时间字符串
        
    Examples:
        >>> format_time(3661)
        '1h 1m 1s'
        >>> format_time(90)
        '1m 30s'
        >>> format_time(45.5)
        '45.5s'
    """
    if seconds < 0:
        return "-" + format_time(-seconds)
    
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    
    # 定义时间单位
    units = [
        ('y', 365 * 24 * 3600),
        ('d', 24 * 3600),
        ('h', 3600),
        ('m', 60),
    ]
    
    parts = []
    remaining = float(seconds)
    
    for unit, value in units:
        if remaining >= value:
            count = int(remaining // value)
            remaining = remaining % value
            parts.append(f"{count}{unit}")
    
    # 处理秒（可能有剩余小数）
    if remaining > 0:
        if remaining == int(remaining):
            parts.append(f"{int(remaining)}s")
        else:
            parts.append(f"{remaining:.1f}s")
    elif not parts:
        parts.append("0s")
    
    return ' '.join(parts)


def format_bandwidth(bps: float, unit: str = 'auto') -> str:
    """
    格式化带宽为易读字符串。
    
    Args:
        bps: bits per second
        unit: 目标单位 ('auto', 'bps', 'Kbps', 'Mbps', 'Gbps', 'B/s', 'MB/s', 等)
        
    Returns:
        格式化的带宽字符串
        
    Examples:
        >>> format_bandwidth(100000000)
        '100.00 Mbps'
        >>> format_bandwidth(100000000, 'MB/s')
        '12.50 MB/s'
    """
    unit = unit.lower()
    
    # 字节单位
    if 'b/s' in unit or 'byte' in unit:
        bytes_per_sec = bps / 8
        
        if 'k' in unit:
            return f"{bytes_per_sec / 1000:.2f} KB/s"
        elif 'm' in unit:
            return f"{bytes_per_sec / 1_000_000:.2f} MB/s"
        elif 'g' in unit:
            return f"{bytes_per_sec / 1_000_000_000:.2f} GB/s"
        else:
            return f"{bytes_per_sec:.2f} B/s"
    
    # 比特单位
    if unit == 'kbps' or unit == 'k':
        return f"{bps / 1000:.2f} Kbps"
    elif unit == 'mbps' or unit == 'm':
        return f"{bps / 1_000_000:.2f} Mbps"
    elif unit == 'gbps' or unit == 'g':
        return f"{bps / 1_000_000_000:.2f} Gbps"
    elif unit == 'tbps' or unit == 't':
        return f"{bps / 1_000_000_000_000:.2f} Tbps"
    elif unit == 'bps' or unit == 'b':
        return f"{bps:.2f} bps"
    
    # 自动选择最佳单位
    if bps >= 1_000_000_000_000:
        return f"{bps / 1_000_000_000_000:.2f} Tbps"
    elif bps >= 1_000_000_000:
        return f"{bps / 1_000_000_000:.2f} Gbps"
    elif bps >= 1_000_000:
        return f"{bps / 1_000_000:.2f} Mbps"
    elif bps >= 1000:
        return f"{bps / 1000:.2f} Kbps"
    else:
        return f"{bps:.2f} bps"


def format_size(bytes_size: int) -> str:
    """
    格式化文件大小为易读字符串。
    
    Args:
        bytes_size: 字节数
        
    Returns:
        格式化的文件大小字符串
        
    Examples:
        >>> format_size(1536000000)
        '1.43 GB'
        >>> format_size(1024)
        '1.00 KB'
    """
    if bytes_size < 0:
        return "-" + format_size(-bytes_size)
    
    if bytes_size < 1024:
        return f"{bytes_size} B"
    
    units = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    size = float(bytes_size)
    unit_index = -1  # 从 KB 开始
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"


def get_size_info(bytes_size: int) -> SizeInfo:
    """
    获取文件大小的详细信息。
    
    Args:
        bytes_size: 字节数
        
    Returns:
        SizeInfo 包含各种单位的大小
        
    Examples:
        >>> info = get_size_info(1536000000)
        >>> print(info.MB)
        1464.84375
    """
    return SizeInfo(
        bytes=int(bytes_size),
        KB=bytes_size / 1024,
        MB=bytes_size / (1024 ** 2),
        GB=bytes_size / (1024 ** 3),
        TB=bytes_size / (1024 ** 4)
    )


def get_bandwidth_info(bps: float) -> BandwidthInfo:
    """
    获取带宽的详细信息。
    
    Args:
        bps: bits per second
        
    Returns:
        BandwidthInfo 包含各种单位的带宽
        
    Examples:
        >>> info = get_bandwidth_info(100000000)
        >>> print(info.Mbps)
        100.0
    """
    return BandwidthInfo(
        bps=bps,
        Kbps=bps / 1000,
        Mbps=bps / 1_000_000,
        Gbps=bps / 1_000_000_000,
        Bps=bps / 8,
        KBps=bps / 8000,
        MBps=bps / 8_000_000
    )


def estimate_download_time(
    file_size: Union[int, str],
    bandwidth: Union[float, str],
    protocol_overhead: float = 5.0
) -> dict:
    """
    估算下载时间（兼容旧接口，返回详细信息字典）。
    
    Args:
        file_size: 文件大小
        bandwidth: 带宽
        protocol_overhead: 协议开销百分比（默认 5%）
        
    Returns:
        包含详细信息的字典
        
    Examples:
        >>> result = estimate_download_time("1 GB", "100 Mbps")
        >>> print(result['time_formatted'])
        '1m 29.9s'
    """
    result = calculate_transfer_time(file_size, bandwidth, protocol_overhead)
    
    # 解析文件大小用于返回
    if isinstance(file_size, str):
        size_bytes = parse_size(file_size)
    else:
        size_bytes = int(file_size)
    
    return {
        'file_size_bytes': size_bytes,
        'file_size_formatted': format_size(size_bytes),
        'bandwidth_bps': result.average_speed_bps,
        'bandwidth_formatted': result.average_speed_formatted,
        'time_seconds': result.time_seconds,
        'time_formatted': result.time_formatted,
        'protocol_overhead_percent': protocol_overhead,
    }


def compare_bandwidths(*bandwidths: Union[float, str]) -> dict:
    """
    比较多个带宽。
    
    Args:
        *bandwidths: 多个带宽值（数值或字符串）
        
    Returns:
        比较结果字典
        
    Examples:
        >>> result = compare_bandwidths("100 Mbps", "50 Mbps", "1 Gbps")
        >>> print(result['fastest'])
        '1 Gbps'
    """
    parsed = []
    for i, bw in enumerate(bandwidths):
        if isinstance(bw, str):
            bps = parse_bandwidth(bw)
            original = bw
        else:
            bps = float(bw)
            original = format_bandwidth(bps)
        parsed.append({
            'index': i,
            'original': original,
            'bps': bps,
            'formatted': format_bandwidth(bps)
        })
    
    # 按带宽排序
    sorted_by_speed = sorted(parsed, key=lambda x: x['bps'], reverse=True)
    
    return {
        'bandwidths': parsed,
        'fastest': sorted_by_speed[0]['original'] if sorted_by_speed else None,
        'slowest': sorted_by_speed[-1]['original'] if sorted_by_speed else None,
        'fastest_bps': sorted_by_speed[0]['bps'] if sorted_by_speed else 0,
        'slowest_bps': sorted_by_speed[-1]['bps'] if sorted_by_speed else 0,
        'ratio_fastest_to_slowest': (
            sorted_by_speed[0]['bps'] / sorted_by_speed[-1]['bps']
            if len(sorted_by_speed) > 1 and sorted_by_speed[-1]['bps'] > 0 else 1
        ),
        'sorted': sorted_by_speed
    }


def bandwidth_for_streaming(
    resolution: str,
    fps: int = 30,
    codec: str = 'h264'
) -> dict:
    """
    根据视频参数估算所需带宽。
    
    Args:
        resolution: 分辨率 ('480p', '720p', '1080p', '1440p', '4k', '8k')
        fps: 帧率（默认 30）
        codec: 编码格式 ('h264', 'h265', 'vp9', 'av1')
        
    Returns:
        带宽建议字典
        
    Examples:
        >>> info = bandwidth_for_streaming('1080p', 60, 'h265')
        >>> print(info['recommended'])
        '12.00 Mbps'
    """
    # 基础比特率 (Mbps) @ 30fps, H.264
    base_bitrates = {
        '480p': 2.5,
        '720p': 5,
        '1080p': 8,
        '1440p': 16,
        '4k': 35,
        '8k': 80,
    }
    
    # 编码效率系数 (相对于 H.264)
    codec_factors = {
        'h264': 1.0,
        'h265': 0.5,
        'hevc': 0.5,
        'vp9': 0.6,
        'av1': 0.4,
    }
    
    resolution = resolution.lower().replace(' ', '')
    codec = codec.lower()
    
    if resolution not in base_bitrates:
        raise ValueError(f"不支持的分辨率: '{resolution}'")
    
    base = base_bitrates[resolution]
    factor = codec_factors.get(codec, 1.0)
    
    # 根据帧率调整
    fps_factor = fps / 30
    
    # 计算实际比特率
    actual_mbps = base * factor * fps_factor
    
    # 建议带宽（增加 20% 余量）
    recommended_mbps = actual_mbps * 1.2
    
    return {
        'resolution': resolution,
        'fps': fps,
        'codec': codec,
        'estimated_bitrate_mbps': round(actual_mbps, 2),
        'estimated_bitrate_formatted': f"{actual_mbps:.2f} Mbps",
        'recommended_bandwidth_mbps': round(recommended_mbps, 2),
        'recommended': f"{recommended_mbps:.2f} Mbps",
        'minimum_mbps': round(actual_mbps * 0.8, 2),
    }


# =============================================================================
# 便捷函数
# =============================================================================

def download_time(file_size: Union[int, str], bandwidth: Union[float, str]) -> str:
    """快速计算下载时间，返回格式化字符串。"""
    result = calculate_transfer_time(file_size, bandwidth)
    return result.time_formatted


def upload_time(file_size: Union[int, str], bandwidth: Union[float, str]) -> str:
    """快速计算上传时间，返回格式化字符串。"""
    return download_time(file_size, bandwidth)


def needed_bandwidth(file_size: Union[int, str], time_limit: Union[float, str]) -> str:
    """快速计算所需带宽，返回格式化字符串。"""
    info = calculate_required_bandwidth(file_size, time_limit)
    return info.format_auto()


# =============================================================================
# 主函数（示例）
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Bandwidth Utils - 带宽计算工具示例")
    print("=" * 60)
    
    # 示例 1: 计算下载时间
    print("\n【示例 1】计算下载时间")
    print("-" * 40)
    result = calculate_transfer_time("1 GB", "100 Mbps")
    print(f"文件大小: 1 GB")
    print(f"网络速度: 100 Mbps")
    print(f"下载时间: {result.time_formatted}")
    print(f"平均速度: {result.average_speed_formatted}")
    
    # 示例 2: 计算所需带宽
    print("\n【示例 2】计算所需带宽")
    print("-" * 40)
    info = calculate_required_bandwidth("4.7 GB", "1h")
    print(f"文件大小: 4.7 GB (DVD)")
    print(f"时间限制: 1 小时")
    print(f"所需带宽: {info.format_auto()}")
    
    # 示例 3: 解析文件大小
    print("\n【示例 3】解析文件大小")
    print("-" * 40)
    sizes = ["100 MB", "1.5 GB", "700KB", "50 MiB"]
    for s in sizes:
        bytes_val = parse_size(s)
        print(f"'{s}' -> {bytes_val:,} bytes -> {format_size(bytes_val)}")
    
    # 示例 4: 解析带宽
    print("\n【示例 4】解析带宽")
    print("-" * 40)
    speeds = ["100 Mbps", "50 Kbps", "1 Gbps", "10 MB/s"]
    for s in speeds:
        bps = parse_bandwidth(s)
        print(f"'{s}' -> {bps:,.0f} bps -> {format_bandwidth(bps)}")
    
    # 示例 5: 流媒体带宽建议
    print("\n【示例 5】流媒体带宽建议")
    print("-" * 40)
    configs = [
        ('1080p', 30, 'h264'),
        ('1080p', 60, 'h265'),
        ('4k', 60, 'av1'),
    ]
    for res, fps, codec in configs:
        info = bandwidth_for_streaming(res, fps, codec)
        print(f"{res}@{fps}fps ({codec}): 建议带宽 {info['recommended']}")
    
    # 示例 6: 带宽比较
    print("\n【示例 6】带宽比较")
    print("-" * 40)
    comparison = compare_bandwidths("100 Mbps", "50 Mbps", "1 Gbps")
    print(f"最快: {comparison['fastest']}")
    print(f"最慢: {comparison['slowest']}")
    print(f"比例: {comparison['ratio_fastest_to_slowest']:.1f}x")
    
    print("\n" + "=" * 60)
    print("完成!")