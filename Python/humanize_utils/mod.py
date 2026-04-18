"""
humanize_utils - 人性化格式工具库
将各种数据转换为人类可读的格式

功能：
- 文件大小格式化（1024 → "1.00 KB"）
- 时间间隔格式化（3600 → "1小时"）
- 数字格式化（1000000 → "1M"）
- 相对时间格式化（时间戳 → "3分钟前"）
- 持续时间格式化（秒数 → "01:30:45"）
- 列表格式化（["a", "b", "c"] → "a、b 和 c"）
"""

from typing import Union, List, Optional
import time


# ============ 文件大小格式化 ============

# 预定义的单位列表，避免每次调用时创建
_BINARY_UNITS = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')
_DECIMAL_UNITS = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')


def format_bytes(
    size: Union[int, float],
    precision: int = 2,
    binary: bool = False,
    use_space: bool = True
) -> str:
    """
    将字节数格式化为人类可读格式
    
    Args:
        size: 字节数
        precision: 小数位数，默认2
        binary: 是否使用二进制单位（KiB, MiB），默认使用十进制（KB, MB）
        use_space: 是否在数字和单位之间加空格
    
    Returns:
        格式化后的字符串，如 "1.50 MB" 或 "1.50 MiB"
    
    Examples:
        >>> format_bytes(1024)
        '1.02 KB'
        >>> format_bytes(1536)
        '1.54 KB'
        >>> format_bytes(1024, binary=True)
        '1.00 KiB'
        >>> format_bytes(1500000)
        '1.50 MB'
    
    Note:
        优化版本：使用预定义常量减少内存分配，
        使用 math.log 快速计算单位索引。
    """
    import math
    
    # 快速处理特殊情况
    if size == 0:
        return f"0{' ' if use_space else ''}B"
    
    if size < 0:
        return f"-{format_bytes(abs(size), precision, binary, use_space)}"
    
    # 使用预定义的单位列表
    units = _BINARY_UNITS if binary else _DECIMAL_UNITS
    base = 1024 if binary else 1000
    
    # 使用 log 快速计算单位索引
    if size < base:
        return f"{int(size)}{' ' if use_space else ''}B"
    
    # 计算单位索引（使用 log 优化）
    unit_index = min(int(math.log(size, base)), len(units) - 1)
    size_in_unit = size / (base ** unit_index)
    
    space = ' ' if use_space else ''
    
    # 格式化数字
    return f"{size_in_unit:.{precision}f}{space}{units[unit_index]}"


def parse_size(size_str: str) -> int:
    """
    解析文件大小字符串为字节数
    
    Args:
        size_str: 大小字符串，如 "1.5MB", "2GB", "500KB"
    
    Returns:
        字节数
    
    Examples:
        >>> parse_size("1KB")
        1000
        >>> parse_size("1KiB")
        1024
        >>> parse_size("1.5MB")
        1500000
        >>> parse_size("2GB")
        2000000000
    """
    size_str = size_str.strip().upper()
    
    # 二进制单位
    binary_units = {
        'KIB': 1024,
        'MIB': 1024 ** 2,
        'GIB': 1024 ** 3,
        'TIB': 1024 ** 4,
        'PIB': 1024 ** 5,
        'EIB': 1024 ** 6,
        'ZIB': 1024 ** 7,
        'YIB': 1024 ** 8,
    }
    
    # 十进制单位
    decimal_units = {
        'KB': 1000,
        'MB': 1000 ** 2,
        'GB': 1000 ** 3,
        'TB': 1000 ** 4,
        'PB': 1000 ** 5,
        'EB': 1000 ** 6,
        'ZB': 1000 ** 7,
        'YB': 1000 ** 8,
        'B': 1,
    }
    
    # 先检查二进制单位
    for unit, multiplier in binary_units.items():
        if size_str.endswith(unit):
            num = float(size_str[:-len(unit)].strip())
            return int(num * multiplier)
    
    # 再检查十进制单位
    for unit, multiplier in decimal_units.items():
        if size_str.endswith(unit):
            num = float(size_str[:-len(unit)].strip())
            return int(num * multiplier)
    
    # 纯数字
    return int(float(size_str))


# ============ 数字格式化 ============

def format_number(
    number: Union[int, float],
    precision: int = 1,
    use_chinese: bool = False
) -> str:
    """
    将大数字格式化为缩写形式
    
    Args:
        number: 数字
        precision: 小数位数，默认1
        use_chinese: 是否使用中文单位（万、亿）
    
    Returns:
        格式化后的字符串，如 "1.5M" 或 "1.5亿"
    
    Examples:
        >>> format_number(1500000)
        '1.5M'
        >>> format_number(1500000000)
        '1.5B'
        >>> format_number(1500000000000)
        '1.5T'
        >>> format_number(15000, use_chinese=True)
        '1.5万'
        >>> format_number(150000000, use_chinese=True)
        '1.5亿'
    """
    if use_chinese:
        if abs(number) >= 1_0000_0000_0000:  # 万亿
            return f"{number / 1_0000_0000_0000:.{precision}f}万亿"
        elif abs(number) >= 1_0000_0000:  # 亿
            return f"{number / 1_0000_0000:.{precision}f}亿"
        elif abs(number) >= 1_0000:  # 万
            return f"{number / 1_0000:.{precision}f}万"
        else:
            return str(int(number))
    else:
        units = ['', 'K', 'M', 'B', 'T', 'Q']
        abs_num = abs(number)
        unit_index = 0
        
        while abs_num >= 1000 and unit_index < len(units) - 1:
            abs_num /= 1000
            unit_index += 1
        
        if unit_index == 0:
            return str(int(number))
        else:
            return f"{number / (1000 ** unit_index):.{precision}f}{units[unit_index]}"


def format_percentage(
    value: Union[int, float],
    precision: int = 1,
    show_sign: bool = False
) -> str:
    """
    格式化百分比
    
    Args:
        value: 数值（0-1 或 0-100）
        precision: 小数位数
        show_sign: 是否显示正负号
    
    Returns:
        格式化后的百分比字符串
    
    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(50)
        '50.0%'
        >>> format_percentage(0.256, precision=2)
        '25.60%'
        >>> format_percentage(0.5, show_sign=True)
        '+50.0%'
    """
    # 判断值是否在 -1 到 1 范围内（处理负数）
    if -1 <= value <= 1:
        percent = value * 100
    else:
        percent = value
    
    if show_sign:
        if percent > 0:
            return f"+{percent:.{precision}f}%"
        elif percent < 0:
            return f"{percent:.{precision}f}%"
    return f"{percent:.{precision}f}%"


def format_with_commas(number: Union[int, float], decimal_places: Optional[int] = None) -> str:
    """
    用千分位分隔符格式化数字
    
    Args:
        number: 数字
        decimal_places: 小数位数，None 表示保留原始精度
    
    Returns:
        格式化后的字符串
    
    Examples:
        >>> format_with_commas(1000000)
        '1,000,000'
        >>> format_with_commas(1234567.891, decimal_places=2)
        '1,234,567.89'
    """
    if decimal_places is not None:
        formatted = f"{number:,.{decimal_places}f}"
    else:
        if isinstance(number, float):
            # 保留原始精度，移除末尾的 0
            formatted = f"{number:,}"
            # 如果有科学计数法，转换为普通格式
            if 'e' in formatted or 'E' in formatted:
                formatted = f"{number:,.15f}".rstrip('0').rstrip('.')
        else:
            formatted = f"{number:,}"
    
    return formatted


# ============ 时间格式化 ============

def format_duration(
    seconds: Union[int, float],
    format_type: str = "auto",
    use_chinese: bool = False,
    show_zeros: bool = False
) -> str:
    """
    将秒数格式化为持续时间
    
    Args:
        seconds: 秒数
        format_type: 格式类型
            - "auto": 自动选择合适格式
            - "full": 完整格式（HH:MM:SS）
            - "compact": 紧凑格式（1h30m）
            - "text": 文字格式（1小时30分钟）
        use_chinese: 是否使用中文单位
        show_zeros: 是否显示零值单位（仅用于 compact 格式）
    
    Returns:
        格式化后的时间字符串
    
    Examples:
        >>> format_duration(3665)
        '01:01:05'
        >>> format_duration(3665, format_type="text", use_chinese=True)
        '1小时1分钟5秒'
        >>> format_duration(3665, format_type="compact")
        '1h1m5s'
        >>> format_duration(3600, format_type="compact", show_zeros=True)
        '1h0m0s'
    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), format_type, use_chinese, show_zeros)}"
    
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    
    if format_type == "full":
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    elif format_type == "compact":
        parts = []
        if hours or show_zeros:
            parts.append(f"{hours}h")
        if minutes or show_zeros:
            parts.append(f"{minutes}m")
        if secs or not parts or show_zeros:
            parts.append(f"{secs}s")
        return "".join(parts)
    
    elif format_type == "text" or format_type == "auto":
        if use_chinese:
            parts = []
            if hours:
                parts.append(f"{hours}小时")
            if minutes:
                parts.append(f"{minutes}分钟")
            if secs or not parts:
                parts.append(f"{secs}秒")
            return "".join(parts)
        else:
            parts = []
            if hours:
                parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes:
                parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            if secs or not parts:
                parts.append(f"{secs} second{'s' if secs != 1 else ''}")
            return " ".join(parts)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_relative_time(
    timestamp: Union[int, float],
    reference: Optional[Union[int, float]] = None,
    use_chinese: bool = True
) -> str:
    """
    将时间戳格式化为相对时间（如"3分钟前"）
    
    Args:
        timestamp: 时间戳（秒）
        reference: 参考时间戳，默认当前时间
        use_chinese: 是否使用中文
    
    Returns:
        相对时间字符串
    
    Examples:
        >>> # 假设当前时间是 1000000000
        >>> format_relative_time(999999940)  # 60秒前
        '1分钟前'
        >>> format_relative_time(999999400)  # 10分钟前
        '10分钟前'
    """
    if reference is None:
        reference = time.time()
    
    diff = reference - timestamp
    
    if diff < 0:
        # 未来时间
        diff = abs(diff)
        suffix = "后" if use_chinese else " from now"
    else:
        suffix = "前" if use_chinese else " ago"
    
    if use_chinese:
        if diff < 60:
            return f"{int(diff)}秒{suffix}"
        elif diff < 3600:
            return f"{int(diff / 60)}分钟{suffix}"
        elif diff < 86400:
            return f"{int(diff / 3600)}小时{suffix}"
        elif diff < 2592000:  # 30天
            return f"{int(diff / 86400)}天{suffix}"
        elif diff < 31536000:  # 365天
            return f"{int(diff / 2592000)}个月{suffix}"
        else:
            return f"{int(diff / 31536000)}年{suffix}"
    else:
        def pluralize(count: int, word: str) -> str:
            return f"{count} {word}{'s' if count != 1 else ''}"
        
        if diff < 60:
            return f"{pluralize(int(diff), 'second')}{suffix}"
        elif diff < 3600:
            return f"{pluralize(int(diff / 60), 'minute')}{suffix}"
        elif diff < 86400:
            return f"{pluralize(int(diff / 3600), 'hour')}{suffix}"
        elif diff < 2592000:
            return f"{pluralize(int(diff / 86400), 'day')}{suffix}"
        elif diff < 31536000:
            return f"{pluralize(int(diff / 2592000), 'month')}{suffix}"
        else:
            return f"{pluralize(int(diff / 31536000), 'year')}{suffix}"


def format_time_ago(
    seconds: Union[int, float],
    use_chinese: bool = True
) -> str:
    """
    将过去的秒数格式化为"多长时间前"
    
    Args:
        seconds: 过去的秒数
        use_chinese: 是否使用中文
    
    Returns:
        时间描述字符串
    
    Examples:
        >>> format_time_ago(3600)
        '1小时前'
        >>> format_time_ago(86400)
        '1天前'
        >>> format_time_ago(3600, use_chinese=False)
        '1 hour ago'
    """
    return format_relative_time(time.time() - seconds, use_chinese=use_chinese)


# ============ 列表格式化 ============

def format_list(
    items: List[str],
    use_chinese: bool = True,
    limit: Optional[int] = None,
    limit_text: Optional[str] = None
) -> str:
    """
    将列表格式化为自然语言字符串
    
    Args:
        items: 字符串列表
        use_chinese: 是否使用中文分隔符
        limit: 限制显示数量，其余显示为 limit_text
        limit_text: 超出限制时的文本
    
    Returns:
        格式化后的字符串
    
    Examples:
        >>> format_list(["a", "b", "c"])
        'a、b 和 c'
        >>> format_list(["a", "b", "c"], use_chinese=False)
        'a, b and c'
        >>> format_list(["a", "b", "c", "d", "e"], limit=3)
        'a、b、c 等 5 项'
    
    Note:
        优化版本：避免递归调用，直接构建结果字符串，
        边界处理：空列表、None 输入、超长列表。
    """
    # 边界处理：空列表或 None 输入
    if items is None or not items:
        return ""
    
    # 处理限制（优化：避免递归，直接构建结果）
    if limit is not None and len(items) > limit:
        display_items = items[:limit]
        remaining = len(items) - limit
        if limit_text is None:
            limit_text = f"等 {len(items)} 项" if use_chinese else f"and {len(items)} more"
        else:
            limit_text = limit_text.format(total=len(items), remaining=remaining)
        # 直接构建结果，不使用递归
        if use_chinese:
            return f"{'、'.join(display_items)} {limit_text}"
        else:
            return f"{', '.join(display_items)} {limit_text}"
    
    # 无限制情况下的处理
    if len(items) == 1:
        return items[0]
    elif len(items) == 2:
        if use_chinese:
            return f"{items[0]} 和 {items[1]}"
        else:
            return f"{items[0]} and {items[1]}"
    else:
        if use_chinese:
            # 性能优化：使用 join 而非字符串拼接
            return f"{'、'.join(items[:-1])} 和 {items[-1]}"
        else:
            return f"{', '.join(items[:-1])} and {items[-1]}"


# ============ 其他实用函数 ============

def format_phone(phone: str, format_type: str = "standard") -> str:
    """
    格式化电话号码
    
    Args:
        phone: 电话号码字符串
        format_type: 格式类型
            - "standard": 标准格式 (138 0000 0000)
            - "hyphen": 连字符格式 (138-0000-0000)
            - "international": 国际格式 (+86 138 0000 0000)
    
    Returns:
        格式化后的电话号码
    
    Examples:
        >>> format_phone("13800000000")
        '138 0000 0000'
        >>> format_phone("13800000000", format_type="hyphen")
        '138-0000-0000'
        >>> format_phone("13800000000", format_type="international")
        '+86 138 0000 0000'
    """
    # 移除所有非数字字符
    digits = ''.join(filter(str.isdigit, phone))
    
    # 处理中国大陆手机号
    if len(digits) == 11:
        if format_type == "standard":
            return f"{digits[:3]} {digits[3:7]} {digits[7:]}"
        elif format_type == "hyphen":
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        elif format_type == "international":
            return f"+86 {digits[:3]} {digits[3:7]} {digits[7:]}"
    
    # 处理带区号的号码
    if len(digits) == 13 and digits.startswith("86"):
        digits = digits[2:]
        if format_type == "international":
            return f"+86 {digits[:3]} {digits[3:7]} {digits[7:]}"
        return format_phone(digits, format_type)
    
    # 其他情况，原样返回
    return phone


def format_card_number(card_number: str, mask: bool = False) -> str:
    """
    格式化银行卡号
    
    Args:
        card_number: 银行卡号
        mask: 是否遮盖中间部分
    
    Returns:
        格式化后的银行卡号
    
    Examples:
        >>> format_card_number("6222021234567890123")
        '6222 0212 3456 7890 123'
        >>> format_card_number("6222021234567890123", mask=True)
        '6222 **** **** **** 123'
    """
    # 移除所有非数字字符
    digits = ''.join(filter(str.isdigit, card_number))
    
    if mask and len(digits) > 8:
        # 保留前4位和后3位，中间用星号替换
        prefix = digits[:4]
        suffix = digits[-3:]
        masked_part = '*' * (len(digits) - 7)
        # 每4位一组显示
        masked_groups = [masked_part[i:i+4] for i in range(0, len(masked_part), 4)]
        result_parts = [prefix] + ['****'] * len(masked_groups) + [suffix]
        return ' '.join(result_parts)
    
    # 每4位一组
    groups = [digits[i:i+4] for i in range(0, len(digits), 4)]
    return ' '.join(groups)


def format_json(data, indent: int = 2, ensure_ascii: bool = False) -> str:
    """
    格式化 JSON 数据
    
    Args:
        data: Python 对象
        indent: 缩进空格数
        ensure_ascii: 是否转义非 ASCII 字符
    
    Returns:
        格式化后的 JSON 字符串
    """
    import json
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, default=str)


def truncate_text(
    text: str,
    max_length: int = 100,
    suffix: str = "...",
    word_boundary: bool = False
) -> str:
    """
    截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度（包含后缀）
        suffix: 截断后缀
        word_boundary: 是否在单词边界截断
    
    Returns:
        截断后的文本
    
    Examples:
        >>> truncate_text("这是一段很长的文本需要截断", max_length=10)
        '这是一段很...'
        >>> truncate_text("Hello world this is a test", max_length=15, word_boundary=True)
        'Hello world...'
    """
    if len(text) <= max_length:
        return text
    
    # 计算实际内容长度（减去后缀长度）
    content_length = max_length - len(suffix)
    if content_length <= 0:
        return suffix
    
    if word_boundary:
        # 找到最后一个空格的位置
        last_space = text[:content_length].rfind(' ')
        if last_space > 0:
            return text[:last_space] + suffix
    
    return text[:content_length] + suffix


def format_ordinal(number: int, use_chinese: bool = False) -> str:
    """
    将数字转换为序数词
    
    Args:
        number: 数字
        use_chinese: 是否使用中文
    
    Returns:
        序数词字符串
    
    Examples:
        >>> format_ordinal(1)
        '1st'
        >>> format_ordinal(2)
        '2nd'
        >>> format_ordinal(21)
        '21st'
        >>> format_ordinal(1, use_chinese=True)
        '第1'
    """
    if use_chinese:
        return f"第{number}"
    
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    
    return f"{number}{suffix}"


# 导出所有公共函数
__all__ = [
    # 文件大小
    'format_bytes',
    'parse_size',
    # 数字
    'format_number',
    'format_percentage',
    'format_with_commas',
    # 时间
    'format_duration',
    'format_relative_time',
    'format_time_ago',
    # 列表
    'format_list',
    # 其他
    'format_phone',
    'format_card_number',
    'format_json',
    'truncate_text',
    'format_ordinal',
]