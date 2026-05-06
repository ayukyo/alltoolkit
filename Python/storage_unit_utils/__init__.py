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

from .mod import (
    # 枚举
    StorageUnit, UnitSystem,
    # 核心转换
    convert, to_bytes, from_bytes,
    # 格式化
    format_size, format_bits, smart_format,
    # 解析
    parse_size, parse_to_bytes,
    # 比例和百分比
    ratio, percentage, progress_bar,
    # 比较和计算
    compare, add, subtract,
    # 高级格式化
    human_readable,
    # 查找极值
    find_largest_unit, find_smallest_unit,
    # 总计
    total_size,
    # 速度和带宽
    speed_format, bandwidth_format, estimate_time,
    # 便捷函数
    kb, mb, gb, tb, kib, mib, gib, tib,
    # 常量
    DECIMAL_UNITS, BINARY_UNITS, UNIT_MAP,
)

__all__ = [
    # 枚举
    "StorageUnit",
    "UnitSystem",
    # 核心转换
    "convert",
    "to_bytes",
    "from_bytes",
    # 格式化
    "format_size",
    "format_bits",
    "smart_format",
    # 解析
    "parse_size",
    "parse_to_bytes",
    # 比例和百分比
    "ratio",
    "percentage",
    "progress_bar",
    # 比较和计算
    "compare",
    "add",
    "subtract",
    # 高级格式化
    "human_readable",
    # 查找极值
    "find_largest_unit",
    "find_smallest_unit",
    # 总计
    "total_size",
    # 速度和带宽
    "speed_format",
    "bandwidth_format",
    "estimate_time",
    # 便捷函数
    "kb",
    "mb",
    "gb",
    "tb",
    "kib",
    "mib",
    "gib",
    "tib",
    # 常量
    "DECIMAL_UNITS",
    "BINARY_UNITS",
    "UNIT_MAP",
]

__version__ = "1.0.0"