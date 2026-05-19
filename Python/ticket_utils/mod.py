"""
ticket_utils - 票据/工单编号生成器

功能：
- 生成多种格式的票据编号（支持自定义前缀、日期、序号、校验位等）
- 支持多种常见票据格式（订单号、发票号、工单号、退款单号等）
- 校验位计算与验证
- 编号解析
- 零外部依赖
"""

import time
import hashlib
import random
import string
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any


class TicketGenerator:
    """票据编号生成器"""
    
    def __init__(self, prefix: str = "", separator: str = "-"):
        """
        初始化票据生成器
        
        Args:
            prefix: 票据前缀（如 "ORD" 表示订单）
            separator: 分隔符，默认为 "-"
        """
        self.prefix = prefix
        self.separator = separator
        self._counter = 0
        self._last_timestamp = 0
    
    def generate_serial(
        self,
        length: int = 6,
        pad_char: str = "0",
        start: int = 1
    ) -> str:
        """
        生成流水号格式票据
        
        格式: PREFIX-YYYYMMDD-NNNNNN
        
        Args:
            length: 序号长度，默认6位
            pad_char: 填充字符，默认为 "0"
            start: 起始序号
        
        Returns:
            票据编号字符串
        """
        date_str = datetime.now().strftime("%Y%m%d")
        serial = str(start).zfill(length)
        if self.prefix:
            return f"{self.prefix}{self.separator}{date_str}{self.separator}{serial}"
        return f"{date_str}{self.separator}{serial}"
    
    def generate_timestamp(
        self,
        include_ms: bool = False,
        random_suffix: int = 0
    ) -> str:
        """
        生成时间戳格式票据
        
        格式: PREFIX-YYYYMMDDHHMMSS[MS][-RAND]
        
        Args:
            include_ms: 是否包含毫秒
            random_suffix: 随机后缀位数
        
        Returns:
            票据编号字符串
        """
        fmt = "%Y%m%d%H%M%S"
        if include_ms:
            timestamp = datetime.now().strftime(fmt) + f"{datetime.now().microsecond // 1000:03d}"
        else:
            timestamp = datetime.now().strftime(fmt)
        
        parts = [timestamp]
        if random_suffix > 0:
            chars = string.digits + string.ascii_uppercase
            suffix = ''.join(random.choices(chars, k=random_suffix))
            parts.append(suffix)
        
        result = self.separator.join(parts)
        if self.prefix:
            result = f"{self.prefix}{self.separator}{result}"
        return result
    
    def generate_hash(
        self,
        data: Optional[str] = None,
        algorithm: str = "md5",
        length: int = 8
    ) -> str:
        """
        生成哈希格式票据
        
        格式: PREFIX-HASH
        
        Args:
            data: 用于生成哈希的数据，如果为空则使用时间戳+随机数
            algorithm: 哈希算法 (md5, sha1, sha256)
            length: 截取长度
        
        Returns:
            票据编号字符串
        """
        if data is None:
            data = f"{time.time()}{random.random()}"
        
        algo_map = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256
        }
        
        hash_func = algo_map.get(algorithm, hashlib.md5)
        hash_value = hash_func(data.encode()).hexdigest()[:length].upper()
        
        if self.prefix:
            return f"{self.prefix}{self.separator}{hash_value}"
        return hash_value
    
    def generate_snowflake_like(
        self,
        machine_id: int = 1,
        epoch: int = 1704067200  # 2024-01-01 00:00:00 UTC
    ) -> str:
        """
        生成类 Snowflake 格式票据
        
        格式: PREFIX-TIMESTAMP-MACHINEID-SEQUENCE
        
        Args:
            machine_id: 机器ID (0-1023)
            epoch: 起始时间戳
        
        Returns:
            票据编号字符串
        """
        current_time = int(time.time() * 1000)
        timestamp = current_time - (epoch * 1000)
        
        # 确保时间戳递增
        if current_time != self._last_timestamp:
            self._last_timestamp = current_time
            self._counter = 0
        else:
            self._counter += 1
        
        # 生成编号
        ticket_id = (timestamp << 22) | (machine_id << 12) | self._counter
        
        if self.prefix:
            return f"{self.prefix}{self.separator}{ticket_id}"
        return str(ticket_id)
    
    def generate_luhn(
        self,
        base_number: Optional[str] = None,
        length: int = 12
    ) -> str:
        """
        生成带 Luhn 校验位的票据编号
        
        格式: PREFIX-BASENUMBER-CHECKDIGIT
        
        Args:
            base_number: 基础编号，如果为空则自动生成
            length: 编号长度（不包含校验位）
        
        Returns:
            带校验位的票据编号字符串
        """
        if base_number is None:
            # 生成随机基础编号
            base_number = ''.join(random.choices(string.digits, k=length))
        
        # 计算 Luhn 校验位
        check_digit = self._calculate_luhn_check(base_number)
        full_number = f"{base_number}{check_digit}"
        
        if self.prefix:
            return f"{self.prefix}{self.separator}{full_number}"
        return full_number
    
    def _calculate_luhn_check(self, number: str) -> str:
        """计算 Luhn 校验位"""
        digits = [int(d) for d in number]
        
        # 从右往左，每隔一位乘以2
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        total = sum(digits)
        check_digit = (10 - (total % 10)) % 10
        return str(check_digit)


def generate_order_number(
    prefix: str = "ORD",
    separator: str = "-",
    include_check: bool = False
) -> str:
    """
    生成订单号
    
    格式: ORD-YYYYMMDD-NNNNNN[-CHECK]
    
    Args:
        prefix: 订单前缀，默认 "ORD"
        separator: 分隔符
        include_check: 是否包含校验位
    
    Returns:
        订单号字符串
    """
    generator = TicketGenerator(prefix, separator)
    date_str = datetime.now().strftime("%Y%m%d")
    serial = ''.join(random.choices(string.digits, k=6))
    
    parts = [date_str, serial]
    
    if include_check:
        check = str(sum(int(d) for d in serial) % 10)
        parts.append(check)
    
    return f"{prefix}{separator}{separator.join(parts)}"


def generate_invoice_number(
    prefix: str = "INV",
    separator: str = "-",
    year: Optional[int] = None
) -> str:
    """
    生成发票号
    
    格式: INV-YY-NNNNNN
    
    Args:
        prefix: 发票前缀，默认 "INV"
        separator: 分隔符
        year: 年份，默认当前年
    
    Returns:
        发票号字符串
    """
    if year is None:
        year = datetime.now().year
    
    year_short = str(year)[2:]  # 取后两位
    serial = ''.join(random.choices(string.digits, k=6))
    
    return f"{prefix}{separator}{year_short}{separator}{serial}"


def generate_ticket_number(
    prefix: str = "TKT",
    separator: str = "-"
) -> str:
    """
    生成工单号
    
    格式: TKT-YYYYMMDD-HHMMSS-RAND
    
    Args:
        prefix: 工单前缀，默认 "TKT"
        separator: 分隔符
    
    Returns:
        工单号字符串
    """
    date_str = datetime.now().strftime("%Y%m%d")
    time_str = datetime.now().strftime("%H%M%S")
    rand = ''.join(random.choices(string.digits + string.ascii_uppercase, k=4))
    
    return f"{prefix}{separator}{date_str}{separator}{time_str}{separator}{rand}"


def generate_refund_number(
    prefix: str = "REF",
    separator: str = "-"
) -> str:
    """
    生成退款单号
    
    格式: REF-YYYYMMDD-NNNNNN
    
    Args:
        prefix: 退款单前缀，默认 "REF"
        separator: 分隔符
    
    Returns:
        退款单号字符串
    """
    date_str = datetime.now().strftime("%Y%m%d")
    serial = ''.join(random.choices(string.digits, k=6))
    
    return f"{prefix}{separator}{date_str}{separator}{serial}"


def generate_tracking_number(
    carrier: str = "SF",
    separator: str = ""
) -> str:
    """
    生成物流追踪号
    
    格式: CARRIER + 随机编号
    
    Args:
        carrier: 承运商代码
        separator: 分隔符
    
    Returns:
        物流追踪号字符串
    """
    # 不同承运商的编号格式
    formats = {
        "SF": lambda: f"SF{random.randint(1000000000, 9999999999)}",  # 顺丰
        "YTO": lambda: f"YT{random.randint(1000000000, 9999999999)}",  # 圆通
        "ZTO": lambda: f"ZT{random.randint(1000000000, 9999999999)}",  # 中通
        "STO": lambda: f"ST{random.randint(1000000000, 9999999999)}",  # 申通
        "YD": lambda: f"YD{random.randint(1000000000, 9999999999)}",   # 韵达
        "EMS": lambda: f"EMS{random.randint(100000000, 999999999)}",   # EMS
        "JD": lambda: f"JD{random.randint(1000000000, 9999999999)}",   # 京东
        "DEFAULT": lambda: f"{carrier}{random.randint(1000000000, 9999999999)}"
    }
    
    generator = formats.get(carrier, formats["DEFAULT"])
    return generator()


def generate_coupon_code(
    prefix: str = "CPN",
    length: int = 8,
    separator: str = "-"
) -> str:
    """
    生成优惠券码
    
    格式: PREFIX-XXXXXXXX (字母数字混合)
    
    Args:
        prefix: 优惠券前缀
        length: 随机部分长度
        separator: 分隔符
    
    Returns:
        优惠券码字符串
    """
    chars = string.digits + string.ascii_uppercase
    # 排除易混淆字符
    chars = chars.replace('0', '').replace('O', '').replace('1', '').replace('I', '')
    
    code = ''.join(random.choices(chars, k=length))
    
    return f"{prefix}{separator}{code}"


def generate_batch_number(
    prefix: str = "BAT",
    separator: str = "-"
) -> str:
    """
    生成批次号
    
    格式: BAT-YYYYMMDD-NNN
    
    Args:
        prefix: 批次前缀
        separator: 分隔符
    
    Returns:
        批次号字符串
    """
    date_str = datetime.now().strftime("%Y%m%d")
    serial = str(random.randint(1, 999)).zfill(3)
    
    return f"{prefix}{separator}{date_str}{separator}{serial}"


def generate_receipt_number(
    prefix: str = "RCP",
    separator: str = "-"
) -> str:
    """
    生成收据号
    
    格式: RCP-YYYYMMDD-NNNNNN
    
    Args:
        prefix: 收据前缀
        separator: 分隔符
    
    Returns:
        收据号字符串
    """
    date_str = datetime.now().strftime("%Y%m%d")
    serial = ''.join(random.choices(string.digits, k=6))
    
    return f"{prefix}{separator}{date_str}{separator}{serial}"


def parse_ticket_number(ticket: str, separator: str = "-") -> Dict[str, Any]:
    """
    解析票据编号
    
    Args:
        ticket: 票据编号
        separator: 分隔符
    
    Returns:
        解析结果字典，包含 prefix, date, time, serial 等字段
    """
    result = {
        "original": ticket,
        "valid": False,
        "prefix": None,
        "date": None,
        "time": None,
        "serial": None,
        "check_digit": None
    }
    
    parts = ticket.split(separator)
    
    if len(parts) < 2:
        return result
    
    # 尝试识别前缀
    first_part = parts[0]
    if first_part.isalpha() or (first_part[:-1].isalpha() and first_part[-1].isdigit()):
        result["prefix"] = first_part
        parts = parts[1:]
    
    # 尝试解析日期
    for i, part in enumerate(parts):
        if len(part) == 8 and part.isdigit():
            try:
                result["date"] = datetime.strptime(part, "%Y%m%d").strftime("%Y-%m-%d")
                parts.pop(i)
                break
            except ValueError:
                pass
    
    # 尝试解析时间
    for i, part in enumerate(parts):
        if len(part) == 6 and part.isdigit():
            try:
                result["time"] = datetime.strptime(part, "%H%M%S").strftime("%H:%M:%S")
                parts.pop(i)
                break
            except ValueError:
                pass
    
    # 剩余部分作为序号
    if parts:
        result["serial"] = separator.join(parts)
    
    result["valid"] = True
    return result


def validate_luhn(number: str) -> bool:
    """
    验证 Luhn 校验位
    
    Args:
        number: 带校验位的编号
    
    Returns:
        是否有效
    """
    if not number.isdigit():
        return False
    
    digits = [int(d) for d in number]
    check_digit = digits.pop()
    
    # 从右往左，每隔一位乘以2
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    total = sum(digits)
    expected_check = (10 - (total % 10)) % 10
    
    return check_digit == expected_check


def generate_custom_ticket(
    template: str,
    values: Optional[Dict[str, str]] = None
) -> str:
    """
    根据模板生成自定义票据编号
    
    模板变量:
        {prefix} - 前缀
        {date} - 日期 YYYYMMDD
        {year} - 年份
        {month} - 月份
        {day} - 日
        {time} - 时间 HHMMSS
        {serial} - 流水号
        {rand:N} - N位随机数字
        {rand_alpha:N} - N位随机字母
        {rand_alnum:N} - N位随机字母数字
    
    Args:
        template: 模板字符串
        values: 自定义变量值
    
    Returns:
        生成的票据编号
    """
    values = values or {}
    now = datetime.now()
    
    # 默认变量
    defaults = {
        "prefix": values.get("prefix", ""),
        "date": now.strftime("%Y%m%d"),
        "year": now.strftime("%Y"),
        "month": now.strftime("%m"),
        "day": now.strftime("%d"),
        "time": now.strftime("%H%M%S"),
        "serial": str(random.randint(1, 999999)).zfill(6)
    }
    
    result = template
    
    # 替换基础变量
    for key, value in defaults.items():
        result = result.replace(f"{{{key}}}", value)
    
    # 替换随机变量
    import re
    
    # 随机数字
    for match in re.finditer(r'\{rand:(\d+)\}', result):
        n = int(match.group(1))
        rand_val = ''.join(random.choices(string.digits, k=n))
        result = result.replace(match.group(0), rand_val)
    
    # 随机字母
    for match in re.finditer(r'\{rand_alpha:(\d+)\}', result):
        n = int(match.group(1))
        rand_val = ''.join(random.choices(string.ascii_uppercase, k=n))
        result = result.replace(match.group(0), rand_val)
    
    # 随机字母数字
    for match in re.finditer(r'\{rand_alnum:(\d+)\}', result):
        n = int(match.group(1))
        rand_val = ''.join(random.choices(string.digits + string.ascii_uppercase, k=n))
        result = result.replace(match.group(0), rand_val)
    
    # 替换自定义变量
    for key, value in values.items():
        result = result.replace(f"{{{key}}}", value)
    
    return result


def batch_generate(
    count: int,
    generator_func,
    unique: bool = True,
    **kwargs
) -> List[str]:
    """
    批量生成票据编号
    
    Args:
        count: 生成数量
        generator_func: 生成函数
        unique: 是否保证唯一
        **kwargs: 传递给生成函数的参数
    
    Returns:
        票据编号列表
    """
    if not unique:
        return [generator_func(**kwargs) for _ in range(count)]
    
    tickets = set()
    while len(tickets) < count:
        tickets.add(generator_func(**kwargs))
    
    return list(tickets)


def ticket_info(ticket: str) -> Dict[str, Any]:
    """
    获取票据信息
    
    Args:
        ticket: 票据编号
    
    Returns:
        票据信息字典
    """
    info = parse_ticket_number(ticket)
    
    # 根据前缀识别票据类型
    prefix_types = {
        "ORD": "订单号",
        "INV": "发票号",
        "TKT": "工单号",
        "REF": "退款单号",
        "BAT": "批次号",
        "RCP": "收据号",
        "CPN": "优惠券码",
        "SF": "顺丰快递",
        "YTO": "圆通快递",
        "ZTO": "中通快递",
        "STO": "申通快递",
        "YD": "韵达快递",
        "EMS": "EMS快递",
        "JD": "京东快递"
    }
    
    if info["prefix"]:
        info["type"] = prefix_types.get(info["prefix"], "未知类型")
    else:
        info["type"] = "未知类型"
    
    # 检查是否包含 Luhn 校验
    numbers = ''.join(c for c in ticket if c.isdigit())
    if len(numbers) >= 2:
        info["luhn_valid"] = validate_luhn(numbers)
    
    return info


class SequentialTicketGenerator:
    """顺序票据生成器（支持持久化）"""
    
    def __init__(
        self,
        prefix: str = "TKT",
        separator: str = "-",
        start_serial: int = 1,
        serial_length: int = 6
    ):
        """
        初始化顺序票据生成器
        
        Args:
            prefix: 票据前缀
            separator: 分隔符
            start_serial: 起始序号
            serial_length: 序号位数
        """
        self.prefix = prefix
        self.separator = separator
        self.current_serial = start_serial
        self.serial_length = serial_length
        self.current_date = datetime.now().strftime("%Y%m%d")
        self._generated_count = 0
    
    def generate(self) -> str:
        """
        生成下一个顺序票据编号
        
        Returns:
            票据编号字符串
        """
        today = datetime.now().strftime("%Y%m%d")
        
        # 如果日期变化，重置序号
        if today != self.current_date:
            self.current_date = today
            self.current_serial = 1
        
        serial = str(self.current_serial).zfill(self.serial_length)
        self.current_serial += 1
        self._generated_count += 1
        
        if self.prefix:
            return f"{self.prefix}{self.separator}{self.current_date}{self.separator}{serial}"
        return f"{self.current_date}{self.separator}{serial}"
    
    def peek_next(self) -> str:
        """
        预览下一个票据编号（不消耗序号）
        
        Returns:
            票据编号字符串
        """
        today = datetime.now().strftime("%Y%m%d")
        serial = str(self.current_serial).zfill(self.serial_length)
        
        if self.prefix:
            return f"{self.prefix}{self.separator}{today}{self.separator}{serial}"
        return f"{today}{self.separator}{serial}"
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取生成器统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "prefix": self.prefix,
            "current_date": self.current_date,
            "current_serial": self.current_serial,
            "serial_length": self.serial_length,
            "generated_count": self._generated_count
        }
    
    def reset(self, start_serial: int = 1):
        """
        重置生成器
        
        Args:
            start_serial: 起始序号
        """
        self.current_serial = start_serial
        self.current_date = datetime.now().strftime("%Y%m%d")
        self._generated_count = 0