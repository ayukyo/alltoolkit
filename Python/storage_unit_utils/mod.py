"""
Storage Unit Utils - 存储单位转换与格式化工具库

功能：
- 存储单位转换：bits/Bytes/KB/MB/GB/TB/PB/EB/ZB/YB
- 二进制单位支持：KiB/MiB/GiB/TiB/PiB/EiB/ZiB/YiB
- 智能格式化：自动选择最合适的单位
- 人类可读输出：带单位格式化字符串
- 比例计算：计算两个存储值之间的比例
- 范围解析：解析人类输入的存储大小（如 "1.5GB"）
- 进度条支持：存储进度可视化
- 零外部依赖，纯 Python 标准库实现
"""

from typing import Union, Tuple, Optional, Dict, List, Any
from enum import Enum
import re


class UnitSystem(Enum):
    """单位系统枚举"""
    DECIMAL = "decimal"  # 十进制（SI）：1000 为基数
    BINARY = "binary"    # 二进制（IEC）：1024 为基数


class StorageUnit(Enum):
    """存储单位枚举"""
    # 十进制单位（SI）
    BIT = ("bit", UnitSystem.DECIMAL, 0)
    BYTE = ("B", UnitSystem.DECIMAL, 1)
    KILOBYTE = ("KB", UnitSystem.DECIMAL, 2)
    MEGABYTE = ("MB", UnitSystem.DECIMAL, 3)
    GIGABYTE = ("GB", UnitSystem.DECIMAL, 4)
    TERABYTE = ("TB", UnitSystem.DECIMAL, 5)
    PETABYTE = ("PB", UnitSystem.DECIMAL, 6)
    EXABYTE = ("EB", UnitSystem.DECIMAL, 7)
    ZETTABYTE = ("ZB", UnitSystem.DECIMAL, 8)
    YOTTABYTE = ("YB", UnitSystem.DECIMAL, 9)
    # 二进制单位（IEC）
    KIBIBYTE = ("KiB", UnitSystem.BINARY, 2)
    MEBIBYTE = ("MiB", UnitSystem.BINARY, 3)
    GIBIBYTE = ("GiB", UnitSystem.BINARY, 4)
    TEBIBYTE = ("TiB", UnitSystem.BINARY, 5)
    PEBIBYTE = ("PiB", UnitSystem.BINARY, 6)
    EXBIBYTE = ("EiB", UnitSystem.BINARY, 7)
    ZEBIBYTE = ("ZiB", UnitSystem.BINARY, 8)
    YOBIBYTE = ("YiB", UnitSystem.BINARY, 9)


# 单位映射
UNIT_MAP: Dict[str, StorageUnit] = {
    # 十进制单位
    "bit": StorageUnit.BIT,
    "bits": StorageUnit.BIT,
    "b": StorageUnit.BIT,
    "byte": StorageUnit.BYTE,
    "bytes": StorageUnit.BYTE,
    "B": StorageUnit.BYTE,
    "KB": StorageUnit.KILOBYTE,
    "MB": StorageUnit.MEGABYTE,
    "GB": StorageUnit.GIGABYTE,
    "TB": StorageUnit.TERABYTE,
    "PB": StorageUnit.PETABYTE,
    "EB": StorageUnit.EXABYTE,
    "ZB": StorageUnit.ZETTABYTE,
    "YB": StorageUnit.YOTTABYTE,
    # 二进制单位
    "KiB": StorageUnit.KIBIBYTE,
    "MiB": StorageUnit.MEBIBYTE,
    "GiB": StorageUnit.GIBIBYTE,
    "TiB": StorageUnit.TEBIBYTE,
    "PiB": StorageUnit.PEBIBYTE,
    "EiB": StorageUnit.EXBIBYTE,
    "ZiB": StorageUnit.ZEBIBYTE,
    "YiB": StorageUnit.YOBIBYTE,
    # 常见别名（不区分大小写的会在解析时处理）
    "kb": StorageUnit.KILOBYTE,
    "mb": StorageUnit.MEGABYTE,
    "gb": StorageUnit.GIGABYTE,
    "tb": StorageUnit.TERABYTE,
    "pb": StorageUnit.PETABYTE,
    "eb": StorageUnit.EXABYTE,
    "zb": StorageUnit.ZETTABYTE,
    "yb": StorageUnit.YOTTABYTE,
    "kib": StorageUnit.KIBIBYTE,
    "mib": StorageUnit.MEBIBYTE,
    "gib": StorageUnit.GIBIBYTE,
    "tib": StorageUnit.TEBIBYTE,
    "pib": StorageUnit.PEBIBYTE,
    "eib": StorageUnit.EXBIBYTE,
    "zib": StorageUnit.ZEBIBYTE,
    "yib": StorageUnit.YOBIBYTE,
}

# 十进制单位列表
DECIMAL_UNITS = [
    StorageUnit.BIT,
    StorageUnit.BYTE,
    StorageUnit.KILOBYTE,
    StorageUnit.MEGABYTE,
    StorageUnit.GIGABYTE,
    StorageUnit.TERABYTE,
    StorageUnit.PETABYTE,
    StorageUnit.EXABYTE,
    StorageUnit.ZETTABYTE,
    StorageUnit.YOTTABYTE,
]

# 二进制单位列表
BINARY_UNITS = [
    StorageUnit.BIT,
    StorageUnit.BYTE,
    StorageUnit.KIBIBYTE,
    StorageUnit.MEBIBYTE,
    StorageUnit.GIBIBYTE,
    StorageUnit.TEBIBYTE,
    StorageUnit.PEBIBYTE,
    StorageUnit.EXBIBYTE,
    StorageUnit.ZEBIBYTE,
    StorageUnit.YOBIBYTE,
]


def _get_base(unit: StorageUnit) -> int:
    """获取单位的基数（1000 或 1024）"""
    return 1024 if unit.value[1] == UnitSystem.BINARY else 1000


def _get_level(unit: StorageUnit) -> int:
    """获取单位的级别（用于计算乘数）"""
    return unit.value[2]


def convert(
    value: Union[int, float],
    from_unit: Union[str, Any],
    to_unit: Union[str, Any]
) -> float:
    """
    在存储单位之间转换值
    
    Args:
        value: 要转换的值
        from_unit: 源单位（字符串或 StorageUnit）
        to_unit: 目标单位（字符串或 StorageUnit）
    
    Returns:
        转换后的值
    
    Examples:
        >>> convert(1024, "MB", "GB")
        1.024
        >>> convert(1, "GiB", "MiB")
        1024.0
        >>> convert(8, "bit", "B")
        1.0
    """
    if isinstance(from_unit, str):
        from_unit = UNIT_MAP.get(from_unit) or UNIT_MAP.get(from_unit.upper())
        if from_unit is None:
            raise ValueError(f"Unknown unit: {from_unit}")
    
    if isinstance(to_unit, str):
        to_unit = UNIT_MAP.get(to_unit) or UNIT_MAP.get(to_unit.upper())
        if to_unit is None:
            raise ValueError(f"Unknown unit: {to_unit}")
    
    if value == 0:
        return 0.0
    
    from_level = _get_level(from_unit)
    to_level = _get_level(to_unit)
    from_base = _get_base(from_unit)
    to_base = _get_base(to_unit)
    
    # 先转换为字节
    if from_unit == StorageUnit.BIT:
        bytes_value = value / 8
    elif from_level == 1:  # BYTE
        bytes_value = value
    else:
        # KB level=2, 所以乘以 base^(2-1) = base^1
        bytes_value = value * (from_base ** (from_level - 1))
    
    # 从字节转换为目标单位
    if to_unit == StorageUnit.BIT:
        result = bytes_value * 8
    elif to_level == 1:  # BYTE
        result = bytes_value
    else:
        # KB level=2, 所以除以 base^(2-1) = base^1
        result = bytes_value / (to_base ** (to_level - 1))
    
    return result


def to_bytes(
    value: Union[int, float],
    unit: Union[str, Any]
) -> int:
    """
    将存储值转换为字节数
    
    Args:
        value: 存储值
        unit: 单位
    
    Returns:
        字节数（整数）
    
    Examples:
        >>> to_bytes(1, "KB")
        1000
        >>> to_bytes(1, "KiB")
        1024
        >>> to_bytes(1.5, "GB")
        1500000000
    """
    return int(convert(value, unit, StorageUnit.BYTE))


def from_bytes(
    bytes_value: int,
    unit: Union[str, Any]
) -> float:
    """
    将字节数转换为指定单位
    
    Args:
        bytes_value: 字节数
        unit: 目标单位
    
    Returns:
        转换后的值
    
    Examples:
        >>> from_bytes(1024, "KB")
        1.024
        >>> from_bytes(1024, "KiB")
        1.0
    """
    return convert(bytes_value, StorageUnit.BYTE, unit)


def format_size(
    bytes_value: Union[int, float],
    binary: bool = False,
    precision: int = 2,
    separator: str = " "
) -> str:
    """
    将字节数格式化为人类可读的字符串
    
    Args:
        bytes_value: 字节数
        binary: 是否使用二进制单位（KiB/MiB/GiB...）
        precision: 小数位数
        separator: 数值和单位之间的分隔符
    
    Returns:
        格式化后的字符串
    
    Examples:
        >>> format_size(0)
        '0 B'
        >>> format_size(1024)
        '1.02 KB'
        >>> format_size(1024, binary=True)
        '1.00 KiB'
        >>> format_size(1536000000)
        '1.54 GB'
    """
    if bytes_value == 0:
        return f"0{separator}B"
    
    units = BINARY_UNITS if binary else DECIMAL_UNITS
    base = 1024 if binary else 1000
    
    # 找到最合适的单位
    abs_value = abs(bytes_value)
    for unit in reversed(units):
        if unit == StorageUnit.BIT:
            continue  # 跳过 bit
        level = _get_level(unit)
        if level == 1:  # BYTE
            continue  # 字节级别在最后处理
        # KB level=2, 1KB = base^1 bytes
        if abs_value >= base ** (level - 1):
            converted = convert(bytes_value, StorageUnit.BYTE, unit)
            return f"{converted:.{precision}f}{separator}{unit.value[0]}"
    
    # 对于小于 1KB 的情况，直接显示字节
    return f"{bytes_value:.{precision}f}{separator}B"


def format_bits(
    bits_value: Union[int, float],
    precision: int = 2,
    separator: str = " "
) -> str:
    """
    将比特数格式化为人类可读的字符串
    
    Args:
        bits_value: 比特数
        precision: 小数位数
        separator: 数值和单位之间的分隔符
    
    Returns:
        格式化后的字符串
    
    Examples:
        >>> format_bits(1000)
        '1.00 Kbit'
        >>> format_bits(1000000)
        '1.00 Mbit'
    """
    if bits_value == 0:
        return f"0{separator}bit"
    
    abs_value = abs(bits_value)
    units = ["bit", "Kbit", "Mbit", "Gbit", "Tbit", "Pbit", "Ebit", "Zbit", "Ybit"]
    
    for i, unit in enumerate(reversed(units)):
        if i == 0:
            continue
        threshold = 1000 ** (len(units) - 1 - i)
        if abs_value >= threshold:
            converted = bits_value / threshold
            return f"{converted:.{precision}f}{separator}{unit}"
    
    return f"{bits_value:.{precision}f}{separator}bit"


def parse_size(size_str: str) -> Tuple[float, StorageUnit]:
    """
    解析存储大小字符串
    
    Args:
        size_str: 存储大小字符串（如 "1.5GB", "1024 KiB"）
    
    Returns:
        (值, 单位) 元组
    
    Raises:
        ValueError: 如果无法解析
    
    Examples:
        >>> parse_size("1GB")
        (1.0, StorageUnit.GIGABYTE)
        >>> parse_size("1.5 KiB")
        (1.5, StorageUnit.KIBIBYTE)
        >>> parse_size("1024")
        (1024.0, StorageUnit.BYTE)
    """
    size_str = size_str.strip()
    
    # 匹配数字和可选单位
    pattern = r'^([\d,.]+)\s*([a-zA-Z]+)?$'
    match = re.match(pattern, size_str)
    
    if not match:
        raise ValueError(f"Cannot parse size: {size_str}")
    
    value_str, unit_str = match.groups()
    
    # 清理数字字符串
    value = float(value_str.replace(',', ''))
    
    if unit_str is None:
        return (value, StorageUnit.BYTE)
    
    # 查找单位
    unit_str = unit_str.strip()
    unit = UNIT_MAP.get(unit_str) or UNIT_MAP.get(unit_str.upper())
    
    if unit is None:
        raise ValueError(f"Unknown unit: {unit_str}")
    
    return (value, unit)


def parse_to_bytes(size_str: str) -> int:
    """
    解析存储大小字符串并返回字节数
    
    Args:
        size_str: 存储大小字符串
    
    Returns:
        字节数
    
    Examples:
        >>> parse_to_bytes("1KB")
        1000
        >>> parse_to_bytes("1KiB")
        1024
        >>> parse_to_bytes("1.5GB")
        1500000000
    """
    value, unit = parse_size(size_str)
    return to_bytes(value, unit)


def smart_format(
    bytes_value: Union[int, float],
    precision: int = 2,
    prefer_binary: bool = False
) -> str:
    """
    智能格式化存储大小
    
    自动选择最合适的单位，支持混合单位系统
    
    Args:
        bytes_value: 字节数
        precision: 小数位数
        prefer_binary: 是否优先使用二进制单位
    
    Returns:
        格式化后的字符串
    
    Examples:
        >>> smart_format(500)
        '500 B'
        >>> smart_format(1500)
        '1.50 KB'
        >>> smart_format(1536, prefer_binary=True)
        '1.50 KiB'
    """
    return format_size(bytes_value, binary=prefer_binary, precision=precision)


def ratio(
    part: Union[int, float],
    total: Union[int, float]
) -> float:
    """
    计算存储比例
    
    Args:
        part: 部分值
        total: 总值
    
    Returns:
        比例（0.0 到 1.0）
    
    Examples:
        >>> ratio(500, 1000)
        0.5
        >>> ratio(0, 1000)
        0.0
    """
    if total == 0:
        return 0.0
    return min(1.0, max(0.0, part / total))


def percentage(
    part: Union[int, float],
    total: Union[int, float],
    precision: int = 1
) -> str:
    """
    计算存储百分比字符串
    
    Args:
        part: 部分值
        total: 总值
        precision: 小数位数
    
    Returns:
        百分比字符串
    
    Examples:
        >>> percentage(500, 1000)
        '50.0%'
        >>> percentage(256, 1024)
        '25.0%'
    """
    return f"{ratio(part, total) * 100:.{precision}f}%"


def progress_bar(
    used: Union[int, float],
    total: Union[int, float],
    width: int = 20,
    filled: str = "█",
    empty: str = "░",
    binary: bool = False,
    precision: int = 1
) -> str:
    """
    生成存储进度条
    
    Args:
        used: 已使用字节数
        total: 总字节数
        width: 进度条宽度（字符数）
        filled: 已填充字符
        empty: 未填充字符
        binary: 是否使用二进制单位
        precision: 小数位数
    
    Returns:
        进度条字符串
    
    Examples:
        >>> progress_bar(500, 1000, width=10)
        '█████░░░░░ 50.0%'
        >>> progress_bar(512, 1024, binary=True)
        '████████░░░░░░░░░░ 50.0%'
    """
    if total == 0:
        pct = 0.0
    else:
        pct = min(1.0, max(0.0, used / total))
    
    filled_count = int(pct * width)
    bar = filled * filled_count + empty * (width - filled_count)
    
    used_str = format_size(used, binary=binary, precision=precision)
    total_str = format_size(total, binary=binary, precision=precision)
    
    return f"{bar} {pct * 100:.{precision}f}% ({used_str}/{total_str})"


def compare(
    size1: Union[int, float, str],
    size2: Union[int, float, str],
    unit1: Optional[Union[str, Any]] = None,
    unit2: Optional[Union[str, Any]] = None
) -> int:
    """
    比较两个存储大小
    
    Args:
        size1: 第一个大小（数值或字符串）
        size2: 第二个大小（数值或字符串）
        unit1: 第一个单位（如果 size1 是数值）
        unit2: 第二个单位（如果 size2 是数值）
    
    Returns:
        -1 如果 size1 < size2，0 如果相等，1 如果 size1 > size2
    
    Examples:
        >>> compare("1GB", "500MB")
        1
        >>> compare(1024, 1, "MB", "GB")
        0
        >>> compare("500MB", "1GB")
        -1
    """
    # 解析大小
    if isinstance(size1, str):
        bytes1 = parse_to_bytes(size1)
    elif unit1 is None:
        bytes1 = int(size1)
    else:
        bytes1 = to_bytes(size1, unit1)
    
    if isinstance(size2, str):
        bytes2 = parse_to_bytes(size2)
    elif unit2 is None:
        bytes2 = int(size2)
    else:
        bytes2 = to_bytes(size2, unit2)
    
    if bytes1 < bytes2:
        return -1
    elif bytes1 > bytes2:
        return 1
    return 0


def add(
    *sizes: Union[int, float, str],
    unit: Optional[Union[str, Any]] = None
) -> Union[int, Tuple[int, Any]]:
    """
    存储大小相加
    
    Args:
        *sizes: 要相加的大小（数值或字符串）
        unit: 返回单位（如果指定）
    
    Returns:
        字节数或指定单位的值
    
    Examples:
        >>> add("1GB", "500MB")
        1500000000
        >>> add("1GB", "500MB", unit="MB")
        1500.0
    """
    total_bytes = 0
    
    for size in sizes:
        if isinstance(size, str):
            total_bytes += parse_to_bytes(size)
        else:
            total_bytes += int(size)
    
    if unit is not None:
        return from_bytes(total_bytes, unit)
    return total_bytes


def subtract(
    size1: Union[int, float, str],
    size2: Union[int, float, str],
    unit: Optional[Union[str, Any]] = None
) -> Union[int, float]:
    """
    存储大小相减
    
    Args:
        size1: 第一个大小
        size2: 第二个大小
        unit: 返回单位
    
    Returns:
        差值（字节数或指定单位）
    
    Examples:
        >>> subtract("2GB", "500MB")
        1500000000
        >>> subtract("2GB", "500MB", unit="MB")
        1500.0
    """
    bytes1 = parse_to_bytes(size1) if isinstance(size1, str) else int(size1)
    bytes2 = parse_to_bytes(size2) if isinstance(size2, str) else int(size2)
    
    diff = bytes1 - bytes2
    
    if unit is not None:
        return from_bytes(diff, unit)
    return diff


def human_readable(
    bytes_value: Union[int, float],
    style: str = "short",
    binary: bool = False,
    precision: int = 2
) -> str:
    """
    生成人类可读的存储大小描述
    
    Args:
        bytes_value: 字节数
        style: 样式（"short" 或 "long"）
        binary: 是否使用二进制单位
        precision: 小数位数
    
    Returns:
        描述字符串
    
    Examples:
        >>> human_readable(1500000000)
        '1.50 GB'
        >>> human_readable(1500000000, style="long")
        '1.50 Gigabytes'
        >>> human_readable(1024, binary=True, style="long")
        '1.00 Kibibytes'
    """
    if bytes_value == 0:
        return "0 Bytes" if style == "long" else "0 B"
    
    units = BINARY_UNITS if binary else DECIMAL_UNITS
    base = 1024 if binary else 1000
    
    unit_names_short = {
        StorageUnit.BYTE: "B",
        StorageUnit.KILOBYTE: "KB",
        StorageUnit.MEGABYTE: "MB",
        StorageUnit.GIGABYTE: "GB",
        StorageUnit.TERABYTE: "TB",
        StorageUnit.PETABYTE: "PB",
        StorageUnit.EXABYTE: "EB",
        StorageUnit.ZETTABYTE: "ZB",
        StorageUnit.YOTTABYTE: "YB",
        StorageUnit.KIBIBYTE: "KiB",
        StorageUnit.MEBIBYTE: "MiB",
        StorageUnit.GIBIBYTE: "GiB",
        StorageUnit.TEBIBYTE: "TiB",
        StorageUnit.PEBIBYTE: "PiB",
        StorageUnit.EXBIBYTE: "EiB",
        StorageUnit.ZEBIBYTE: "ZiB",
        StorageUnit.YOBIBYTE: "YiB",
    }
    
    unit_names_long = {
        StorageUnit.BYTE: ("Byte", "Bytes"),
        StorageUnit.KILOBYTE: ("Kilobyte", "Kilobytes"),
        StorageUnit.MEGABYTE: ("Megabyte", "Megabytes"),
        StorageUnit.GIGABYTE: ("Gigabyte", "Gigabytes"),
        StorageUnit.TERABYTE: ("Terabyte", "Terabytes"),
        StorageUnit.PETABYTE: ("Petabyte", "Petabytes"),
        StorageUnit.EXABYTE: ("Exabyte", "Exabytes"),
        StorageUnit.ZETTABYTE: ("Zettabyte", "Zettabytes"),
        StorageUnit.YOTTABYTE: ("Yottabyte", "Yottabytes"),
        StorageUnit.KIBIBYTE: ("Kibibyte", "Kibibytes"),
        StorageUnit.MEBIBYTE: ("Mebibyte", "Mebibytes"),
        StorageUnit.GIBIBYTE: ("Gibibyte", "Gibibytes"),
        StorageUnit.TEBIBYTE: ("Tebibyte", "Tebibytes"),
        StorageUnit.PEBIBYTE: ("Pebibyte", "Pebibytes"),
        StorageUnit.EXBIBYTE: ("Exbibyte", "Exbibytes"),
        StorageUnit.ZEBIBYTE: ("Zebibyte", "Zebibytes"),
        StorageUnit.YOBIBYTE: ("Yobibyte", "Yobibytes"),
    }
    
    abs_value = abs(bytes_value)
    
    for unit in reversed(units):
        if unit == StorageUnit.BIT:
            continue
        level = _get_level(unit)
        if level == 1:  # BYTE, skip and handle at the end
            continue
        # KB level=2, 1KB = base^1 bytes
        if abs_value >= base ** (level - 1):
            converted = convert(bytes_value, StorageUnit.BYTE, unit)
            if style == "short":
                return f"{converted:.{precision}f} {unit_names_short[unit]}"
            else:
                singular, plural = unit_names_long[unit]
                unit_name = plural if abs(converted) != 1 else singular
                return f"{converted:.{precision}f} {unit_name}"
    
    # 字节
    if style == "short":
        return f"{bytes_value:.{precision}f} B"
    else:
        unit_name = "Byte" if abs(bytes_value) == 1 else "Bytes"
        return f"{bytes_value:.{precision}f} {unit_name}"


def find_largest_unit(
    sizes: List[Union[int, float, str]]
) -> Tuple[str, float]:
    """
    找出列表中最大的存储大小
    
    Args:
        sizes: 存储大小列表
    
    Returns:
        (原始字符串, 字节数)
    
    Examples:
        >>> find_largest_unit(["1GB", "500MB", "2TB"])
        ('2TB', 2000000000000)
    """
    if not sizes:
        raise ValueError("Empty list")
    
    max_bytes = -1
    max_str = ""
    
    for size in sizes:
        if isinstance(size, str):
            bytes_val = parse_to_bytes(size)
            orig_str = size
        else:
            bytes_val = int(size)
            orig_str = f"{size}B"
        
        if bytes_val > max_bytes:
            max_bytes = bytes_val
            max_str = orig_str
    
    return (max_str, max_bytes)


def find_smallest_unit(
    sizes: List[Union[int, float, str]]
) -> Tuple[str, float]:
    """
    找出列表中最小的存储大小
    
    Args:
        sizes: 存储大小列表
    
    Returns:
        (原始字符串, 字节数)
    
    Examples:
        >>> find_smallest_unit(["1GB", "500MB", "2TB"])
        ('500MB', 500000000)
    """
    if not sizes:
        raise ValueError("Empty list")
    
    min_bytes = float('inf')
    min_str = ""
    
    for size in sizes:
        if isinstance(size, str):
            bytes_val = parse_to_bytes(size)
            orig_str = size
        else:
            bytes_val = int(size)
            orig_str = f"{size}B"
        
        if bytes_val < min_bytes:
            min_bytes = bytes_val
            min_str = orig_str
    
    return (min_str, min_bytes)


def total_size(
    *sizes: Union[int, float, str],
    unit: Optional[Union[str, Any]] = None
) -> str:
    """
    计算总大小并格式化输出
    
    Args:
        *sizes: 存储大小列表
        unit: 输出单位（自动选择如果 None）
    
    Returns:
        格式化的总大小字符串
    
    Examples:
        >>> total_size("1GB", "500MB", "100MB")
        '1.60 GB'
    """
    total_bytes = add(*sizes)
    
    if unit is not None:
        value = from_bytes(total_bytes, unit)
        unit_str = unit.value[0] if isinstance(unit, StorageUnit) else unit
        return f"{value:.2f} {unit_str}"
    
    return format_size(total_bytes)


def speed_format(
    bytes_per_second: Union[int, float],
    binary: bool = False,
    precision: int = 2
) -> str:
    """
    格式化传输速度
    
    Args:
        bytes_per_second: 每秒字节数
        binary: 是否使用二进制单位
        precision: 小数位数
    
    Returns:
        格式化的速度字符串
    
    Examples:
        >>> speed_format(1024)
        '1.02 KB/s'
        >>> speed_format(1024, binary=True)
        '1.00 KiB/s'
        >>> speed_format(125000)
        '125.00 KB/s'
    """
    size_str = format_size(bytes_per_second, binary=binary, precision=precision)
    return f"{size_str}/s"


def bandwidth_format(
    bits_per_second: Union[int, float],
    precision: int = 2
) -> str:
    """
    格式化带宽
    
    Args:
        bits_per_second: 每秒比特数
        precision: 小数位数
    
    Returns:
        格式化的带宽字符串
    
    Examples:
        >>> bandwidth_format(1000000)
        '1.00 Mbps'
        >>> bandwidth_format(1000000000)
        '1.00 Gbps'
    """
    if bits_per_second == 0:
        return "0 bps"
    
    units = ["bps", "Kbps", "Mbps", "Gbps", "Tbps", "Pbps", "Ebps", "Zbps", "Ybps"]
    abs_value = abs(bits_per_second)
    
    for i, unit in enumerate(reversed(units)):
        if i == 0:
            continue
        threshold = 1000 ** (len(units) - 1 - i)
        if abs_value >= threshold:
            converted = bits_per_second / threshold
            return f"{converted:.{precision}f} {unit}"
    
    return f"{bits_per_second:.{precision}f} bps"


def estimate_time(
    bytes_remaining: Union[int, float],
    bytes_per_second: Union[int, float]
) -> str:
    """
    估算剩余时间
    
    Args:
        bytes_remaining: 剩余字节数
        bytes_per_second: 每秒传输字节数
    
    Returns:
        估算时间字符串
    
    Examples:
        >>> estimate_time(1024 * 1024 * 100, 1024 * 1024)
        '1m 40s'
        >>> estimate_time(1024 * 1024 * 3600, 1024 * 1024)
        '1h 0m'
    """
    if bytes_per_second <= 0:
        return "∞"
    
    seconds = bytes_remaining / bytes_per_second
    
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        if secs == 0:
            return f"{minutes}m"
        return f"{minutes}m {secs}s"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        if minutes == 0:
            return f"{hours}h"
        return f"{hours}h {minutes}m"
    else:
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        if hours == 0:
            return f"{days}d"
        return f"{days}d {hours}h"


# 便捷函数
def kb(value: Union[int, float]) -> int:
    """千字节转字节"""
    return to_bytes(value, StorageUnit.KILOBYTE)


def mb(value: Union[int, float]) -> int:
    """兆字节转字节"""
    return to_bytes(value, StorageUnit.MEGABYTE)


def gb(value: Union[int, float]) -> int:
    """吉字节转字节"""
    return to_bytes(value, StorageUnit.GIGABYTE)


def tb(value: Union[int, float]) -> int:
    """太字节转字节"""
    return to_bytes(value, StorageUnit.TERABYTE)


def kib(value: Union[int, float]) -> int:
    """KiB 转字节"""
    return to_bytes(value, StorageUnit.KIBIBYTE)


def mib(value: Union[int, float]) -> int:
    """MiB 转字节"""
    return to_bytes(value, StorageUnit.MEBIBYTE)


def gib(value: Union[int, float]) -> int:
    """GiB 转字节"""
    return to_bytes(value, StorageUnit.GIBIBYTE)


def tib(value: Union[int, float]) -> int:
    """TiB 转字节"""
    return to_bytes(value, StorageUnit.TEBIBYTE)


if __name__ == "__main__":
    # 简单演示
    print("=== Storage Unit Utils Demo ===\n")
    
    # 格式化示例
    sizes = [0, 500, 1024, 1500000, 1500000000, 1500000000000]
    for size in sizes:
        print(f"{size:>15} bytes = {format_size(size)} (decimal) / {format_size(size, binary=True)} (binary)")
    
    print("\n=== 转换示例 ===")
    print(f"1 GB = {convert(1, 'GB', 'MB'):.2f} MB")
    print(f"1 GiB = {convert(1, 'GiB', 'MiB'):.2f} MiB")
    print(f"8 bits = {convert(8, 'bit', 'B')} bytes")
    
    print("\n=== 解析示例 ===")
    test_strings = ["1GB", "1.5 KiB", "1024", "500MB"]
    for s in test_strings:
        value, unit = parse_size(s)
        print(f"'{s}' -> {value} {unit.value[0]} = {parse_to_bytes(s)} bytes")
    
    print("\n=== 进度条示例 ===")
    print(progress_bar(500, 1000, width=20))
    print(progress_bar(750, 1000, width=20))
    print(progress_bar(1024, 4096, binary=True, width=20))
    
    print("\n=== 速度示例 ===")
    print(f"传输速度: {speed_format(1024 * 1024 * 5)}")
    print(f"带宽: {bandwidth_format(100000000)}")
    print(f"预计时间: {estimate_time(1024 * 1024 * 100, 1024 * 1024)}")
    
    print("\n=== 计算示例 ===")
    print(f"1GB + 500MB = {total_size('1GB', '500MB')}")
    print(f"比较 1GB vs 500MB: {compare('1GB', '500MB')}")
    print(f"百分比: {percentage(500, 1000)}")