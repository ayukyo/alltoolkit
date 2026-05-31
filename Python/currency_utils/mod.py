"""
Currency Utils - 货币处理工具模块

提供货币相关的实用功能：
- 货币格式化和解析
- 汇率转换（支持离线固定汇率）
- 货币代码验证
- 多币种显示
- 价格舍入规则

注意：汇率数据为静态示例数据，实际使用时需替换为实时数据源
"""

from typing import Optional, Dict, Tuple, List, Union
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_FLOOR, ROUND_CEILING
import re


# ISO 4217 货币代码映射
CURRENCY_DATA: Dict[str, Dict] = {
    "USD": {"name": "US Dollar", "symbol": "$", "decimals": 2, "code": "USD"},
    "EUR": {"name": "Euro", "symbol": "€", "decimals": 2, "code": "EUR"},
    "GBP": {"name": "British Pound", "symbol": "£", "decimals": 2, "code": "GBP"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥", "decimals": 0, "code": "JPY"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥", "decimals": 2, "code": "CNY"},
    "KRW": {"name": "South Korean Won", "symbol": "₩", "decimals": 0, "code": "KRW"},
    "INR": {"name": "Indian Rupee", "symbol": "₹", "decimals": 2, "code": "INR"},
    "AUD": {"name": "Australian Dollar", "symbol": "A$", "decimals": 2, "code": "AUD"},
    "CAD": {"name": "Canadian Dollar", "symbol": "C$", "decimals": 2, "code": "CAD"},
    "CHF": {"name": "Swiss Franc", "symbol": "CHF", "decimals": 2, "code": "CHF"},
    "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$", "decimals": 2, "code": "HKD"},
    "SGD": {"name": "Singapore Dollar", "symbol": "S$", "decimals": 2, "code": "SGD"},
    "SEK": {"name": "Swedish Krona", "symbol": "kr", "decimals": 2, "code": "SEK"},
    "NOK": {"name": "Norwegian Krone", "symbol": "kr", "decimals": 2, "code": "NOK"},
    "MXN": {"name": "Mexican Peso", "symbol": "$", "decimals": 2, "code": "MXN"},
    "BRL": {"name": "Brazilian Real", "symbol": "R$", "decimals": 2, "code": "BRL"},
    "RUB": {"name": "Russian Ruble", "symbol": "₽", "decimals": 2, "code": "RUB"},
    "ZAR": {"name": "South African Rand", "symbol": "R", "decimals": 2, "code": "ZAR"},
    "TRY": {"name": "Turkish Lira", "symbol": "₺", "decimals": 2, "code": "TRY"},
    "PLN": {"name": "Polish Zloty", "symbol": "zł", "decimals": 2, "code": "PLN"},
    "THB": {"name": "Thai Baht", "symbol": "฿", "decimals": 2, "code": "THB"},
    "IDR": {"name": "Indonesian Rupiah", "symbol": "Rp", "decimals": 0, "code": "IDR"},
    "MYR": {"name": "Malaysian Ringgit", "symbol": "RM", "decimals": 2, "code": "MYR"},
    "PHP": {"name": "Philippine Peso", "symbol": "₱", "decimals": 2, "code": "PHP"},
    "VND": {"name": "Vietnamese Dong", "symbol": "₫", "decimals": 0, "code": "VND"},
    "AED": {"name": "UAE Dirham", "symbol": "د.إ", "decimals": 2, "code": "AED"},
    "SAR": {"name": "Saudi Riyal", "symbol": "﷼", "decimals": 2, "code": "SAR"},
    "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$", "decimals": 2, "code": "NZD"},
    "DKK": {"name": "Danish Krone", "symbol": "kr", "decimals": 2, "code": "DKK"},
    "CZK": {"name": "Czech Koruna", "symbol": "Kč", "decimals": 2, "code": "CZK"},
    "HUF": {"name": "Hungarian Forint", "symbol": "Ft", "decimals": 2, "code": "HUF"},
    "ILS": {"name": "Israeli Shekel", "symbol": "₪", "decimals": 2, "code": "ILS"},
    "CLP": {"name": "Chilean Peso", "symbol": "$", "decimals": 0, "code": "CLP"},
    "PKR": {"name": "Pakistani Rupee", "symbol": "₨", "decimals": 2, "code": "PKR"},
    "EGP": {"name": "Egyptian Pound", "symbol": "E£", "decimals": 2, "code": "EGP"},
    "BDT": {"name": "Bangladeshi Taka", "symbol": "৳", "decimals": 2, "code": "BDT"},
}

# 默认汇率（以 USD 为基准，示例数据）
DEFAULT_RATES: Dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.50,
    "CNY": 7.24,
    "KRW": 1330.0,
    "INR": 83.12,
    "AUD": 1.53,
    "CAD": 1.36,
    "CHF": 0.88,
    "HKD": 7.82,
    "SGD": 1.34,
    "SEK": 10.42,
    "NOK": 10.65,
    "MXN": 17.15,
    "BRL": 4.97,
    "RUB": 91.50,
    "ZAR": 18.65,
    "TRY": 32.15,
    "PLN": 3.98,
    "THB": 35.50,
    "IDR": 15650.0,
    "MYR": 4.72,
    "PHP": 56.20,
    "VND": 24850.0,
    "AED": 3.67,
    "SAR": 3.75,
    "NZD": 1.64,
    "DKK": 6.87,
    "CZK": 22.85,
    "HUF": 356.0,
    "ILS": 3.68,
    "CLP": 895.0,
    "PKR": 278.5,
    "EGP": 30.90,
    "BDT": 109.50,
}


class Currency:
    """货币对象"""
    
    def __init__(self, amount: Union[int, float, Decimal, str], code: str = "USD"):
        """初始化货币
        
        Args:
            amount: 金额（支持 int, float, Decimal 或字符串）
            code: ISO 4217 货币代码
        """
        if not validate_code(code):
            raise ValueError(f"无效的货币代码: {code}")
        
        self.code = code.upper()
        self._amount = Decimal(str(amount))
        self._decimal_places = CURRENCY_DATA[self.code]["decimals"]
    
    @property
    def amount(self) -> Decimal:
        """获取金额"""
        return self._amount
    
    @amount.setter
    def amount(self, value: Union[int, float, Decimal, str]):
        """设置金额"""
        self._amount = Decimal(str(value))
    
    @property
    def symbol(self) -> str:
        """获取货币符号"""
        return CURRENCY_DATA[self.code]["symbol"]
    
    @property
    def name(self) -> str:
        """获取货币名称"""
        return CURRENCY_DATA[self.code]["name"]
    
    @property
    def decimals(self) -> int:
        """获取小数位数"""
        return self._decimal_places
    
    def formatted(self, locale: str = "en_US") -> str:
        """获取格式化后的字符串
        
        Args:
            locale: 区域设置（目前支持 en_US, zh_CN）
            
        Returns:
            格式化的货币字符串
        """
        return format_currency(self._amount, self.code, locale)
    
    def __repr__(self) -> str:
        return f"Currency({self._amount}, '{self.code}')"
    
    def __str__(self) -> str:
        return self.formatted()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Currency):
            return False
        return self.code == other.code and self._amount == other._amount
    
    def __add__(self, other) -> 'Currency':
        if isinstance(other, Currency):
            if self.code != other.code:
                raise ValueError(f"货币代码不匹配: {self.code} vs {other.code}")
            return Currency(self._amount + other._amount, self.code)
        return Currency(self._amount + Decimal(str(other)), self.code)
    
    def __sub__(self, other) -> 'Currency':
        if isinstance(other, Currency):
            if self.code != other.code:
                raise ValueError(f"货币代码不匹配: {self.code} vs {other.code}")
            return Currency(self._amount - other._amount, self.code)
        return Currency(self._amount - Decimal(str(other)), self.code)
    
    def __mul__(self, multiplier: Union[int, float, Decimal]) -> 'Currency':
        return Currency(self._amount * Decimal(str(multiplier)), self.code)
    
    def __rmul__(self, multiplier: Union[int, float, Decimal]) -> 'Currency':
        return self.__mul__(multiplier)
    
    def __truediv__(self, divisor: Union[int, float, Decimal]) -> 'Currency':
        return Currency(self._amount / Decimal(str(divisor)), self.code)
    
    def __lt__(self, other) -> bool:
        if isinstance(other, Currency):
            if self.code != other.code:
                raise ValueError(f"货币代码不匹配: {self.code} vs {other.code}")
            return self._amount < other._amount
        return self._amount < Decimal(str(other))
    
    def __le__(self, other) -> bool:
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        return not self <= other
    
    def __ge__(self, other) -> bool:
        return not self < other


def validate_code(code: str) -> bool:
    """验证货币代码是否有效
    
    Args:
        code: ISO 4217 货币代码
        
    Returns:
        是否有效
    """
    return code.upper() in CURRENCY_DATA


def get_currency_info(code: str) -> Optional[Dict]:
    """获取货币信息
    
    Args:
        code: ISO 4217 货币代码
        
    Returns:
        货币信息字典，包含 name, symbol, decimals, code
        如果代码无效返回 None
    """
    return CURRENCY_DATA.get(code.upper())


def format_currency(
    amount: Union[int, float, Decimal, str],
    code: str = "USD",
    locale: str = "en_US"
) -> str:
    """格式化货币金额
    
    Args:
        amount: 金额
        code: 货币代码
        locale: 区域设置 (en_US, zh_CN)
        
    Returns:
        格式化的货币字符串
    """
    if not validate_code(code):
        raise ValueError(f"无效的货币代码: {code}")
    
    amount = Decimal(str(amount))
    decimals = CURRENCY_DATA[code.upper()]["decimals"]
    symbol = CURRENCY_DATA[code.upper()]["symbol"]
    
    # 舍入
    quantize_str = '0.' + '0' * decimals if decimals > 0 else '1'
    rounded = amount.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
    
    # 分组格式
    if decimals > 0:
        integer_part = str(rounded)
        integer_part = abs(int(integer_part.split('.')[0] if '.' in integer_part else integer_part))
        fractional_part = str(rounded).split('.')[-1] if '.' in str(rounded) else '0' * decimals
        fractional_part = fractional_part.ljust(decimals, '0')
    else:
        integer_part = str(abs(int(rounded)))
        fractional_part = ''
    
    # 添加千位分隔符
    integer_str = f"{int(integer_part):,}"
    if integer_part == 0 and rounded < 0:
        integer_str = '0'
    
    # 处理负数
    prefix = '-' if rounded < 0 else ''
    
    if decimals > 0:
        formatted = f"{prefix}{symbol}{integer_str}.{fractional_part}"
    else:
        formatted = f"{prefix}{symbol}{integer_str}"
    
    return formatted


def parse_currency(
    value: str,
    code: Optional[str] = None
) -> Tuple[Decimal, Optional[str]]:
    """解析货币字符串
    
    Args:
        value: 货币字符串，支持以下格式：
               - $1,234.56
               - €1.234,56
               - ¥1234
               - 1234.56 USD
               - 1234,56
        code: 强制指定货币代码
        
    Returns:
        (金额, 检测到的货币代码或None)
    """
    if code:
        code = code.upper()
        if not validate_code(code):
            raise ValueError(f"无效的货币代码: {code}")
    
    original = value.strip()
    
    # 检测货币代码
    detected_code = None
    if not code:
        # 尝试从字符串末尾提取代码
        parts = original.split()
        if len(parts) > 1:
            last_part = parts[-1].upper()
            if validate_code(last_part):
                detected_code = last_part
                value = ' '.join(parts[:-1])
            else:
                value = original
        else:
            value = original
    
    # 尝试使用提供的代码
    if code:
        detected_code = code.upper()
    
    if not detected_code:
        detected_code = "USD"  # 默认
    
    # 提取符号
    symbol = CURRENCY_DATA[detected_code]["symbol"]
    
    # 移除符号和空白
    work_str = value.strip()
    
    # 移除货币代码前缀（如果还有）
    if detected_code:
        for c in CURRENCY_DATA.get(detected_code, {}).get("symbol", ""):
            if c not in [',', '.', '-', ' ', '\u4e00-\u9fff', '\u3000-\u303f', '\uff00-\uffef']:
                work_str = work_str.replace(c, '')
        # 也处理无符号格式 "USD 1,234.56"
        code_prefix = detected_code + ' '
        if work_str.upper().startswith(code_prefix):
            work_str = work_str[len(code_prefix):]
    
    # 移除可能的负号和括号
    is_negative = False
    if work_str.startswith('-') or work_str.startswith('('):
        is_negative = work_str.startswith('-')
        work_str = re.sub(r'^[\-()]+', '', work_str)
    
    # 提取数字部分
    numeric_str = re.sub(r'[^\d.,]', '', work_str)
    if not numeric_str:
        return Decimal('0'), detected_code
    
    # 处理欧式格式（使用逗号作为小数点）
    has_european_format = '.' in numeric_str and ',' in numeric_str
    if has_european_format:
        if numeric_str.rfind(',') > numeric_str.rfind('.'):
            # 欧式格式: 1.234,56
            numeric_str = numeric_str.replace('.', '').replace(',', '.')
        else:
            # 美式格式: 1,234.56
            numeric_str = numeric_str.replace(',', '')
    else:
        # 只有逗号：可能是千位分隔符或小数点
        comma_count = numeric_str.count(',')
        dot_count = numeric_str.count('.')
        
        if comma_count == 1 and dot_count == 0:
            # 检查逗号位置：如果是3位分隔符，通常在第4位之后
            idx = numeric_str.find(',')
            if len(numeric_str) - idx - 1 == 3:
                # 千位分隔符
                numeric_str = numeric_str.replace(',', '')
            else:
                # 小数点
                numeric_str = numeric_str.replace(',', '.')
        elif comma_count > 1 and dot_count == 0:
            # 多个逗号，应该是千位分隔符
            numeric_str = numeric_str.replace(',', '')
        elif dot_count > 0 and comma_count == 0:
            # 只有点，根据位数判断
            idx = numeric_str.find('.')
            if len(numeric_str) - idx - 1 == 2 or len(numeric_str) - idx - 1 <= 3:
                # 可能是小数点
                pass
            else:
                # 可能是千位分隔符
                numeric_str = numeric_str.replace('.', '')
        elif comma_count > 0 and dot_count > 0:
            # 两者都有，判断哪个是小数点
            if numeric_str.find(',') < numeric_str.find('.'):
                numeric_str = numeric_str.replace(',', '')
            else:
                numeric_str = numeric_str.replace('.', '').replace(',', '.')
    
    try:
        result = Decimal(numeric_str)
        if is_negative:
            result = -result
        return result, detected_code
    except Exception:
        raise ValueError(f"无法解析货币字符串: {value}")


def convert(
    amount: Union[int, float, Decimal, str],
    from_code: str,
    to_code: str,
    rates: Optional[Dict[str, float]] = None
) -> Decimal:
    """货币转换
    
    Args:
        amount: 金额
        from_code: 源货币代码
        to_code: 目标货币代码
        rates: 汇率字典（以 USD 为基准），默认使用内置汇率
        
    Returns:
        转换后的金额
    """
    if from_code.upper() == to_code.upper():
        return Decimal(str(amount))
    
    if rates is None:
        rates = DEFAULT_RATES
    
    from_code = from_code.upper()
    to_code = to_code.upper()
    
    if from_code not in rates or to_code not in rates:
        raise ValueError(f"不支持的货币代码: {from_code} 或 {to_code}")
    
    amount = Decimal(str(amount))
    
    # 转换为 USD
    usd_amount = amount / Decimal(str(rates[from_code]))
    
    # 从 USD 转换为目标货币
    result = usd_amount * Decimal(str(rates[to_code]))
    
    # 舍入到目标货币的小数位
    decimals = CURRENCY_DATA[to_code]["decimals"]
    quantize_str = '0.' + '0' * decimals if decimals > 0 else '1'
    return result.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)


def exchange(
    amount: Union[int, float, Decimal, str],
    from_code: str,
    to_code: str,
    rates: Optional[Dict[str, float]] = None
) -> Currency:
    """货币兑换（返回 Currency 对象）
    
    Args:
        amount: 金额
        from_code: 源货币代码
        to_code: 目标货币代码
        rates: 汇率字典
        
    Returns:
        Currency 对象
    """
    result = convert(amount, from_code, to_code, rates)
    return Currency(result, to_code)


def get_rate(from_code: str, to_code: str, rates: Optional[Dict[str, float]] = None) -> float:
    """获取汇率
    
    Args:
        from_code: 源货币代码
        to_code: 目标货币代码
        rates: 汇率字典
        
    Returns:
        汇率（1 单位源货币对应的目标货币数量）
    """
    if from_code.upper() == to_code.upper():
        return 1.0
    
    if rates is None:
        rates = DEFAULT_RATES
    
    from_code = from_code.upper()
    to_code = to_code.upper()
    
    if from_code not in rates or to_code not in rates:
        raise ValueError(f"不支持的货币代码: {from_code} 或 {to_code}")
    
    return rates[to_code] / rates[from_code]


def round_currency(
    amount: Union[int, float, Decimal, str],
    code: str,
    mode: str = "HALF_UP"
) -> Decimal:
    """根据货币规则舍入金额
    
    Args:
        amount: 金额
        code: 货币代码
        mode: 舍入模式 (HALF_UP, HALF_DOWN, FLOOR, CEILING)
        
    Returns:
        舍入后的金额
    """
    if not validate_code(code):
        raise ValueError(f"无效的货币代码: {code}")
    
    amount = Decimal(str(amount))
    decimals = CURRENCY_DATA[code.upper()]["decimals"]
    
    rounding_modes = {
        "HALF_UP": ROUND_HALF_UP,
        "HALF_DOWN": ROUND_HALF_DOWN,
        "FLOOR": ROUND_FLOOR,
        "CEILING": ROUND_CEILING,
    }
    
    rounding_mode = rounding_modes.get(mode.upper(), ROUND_HALF_UP)
    
    quantize_str = '0.' + '0' * decimals if decimals > 0 else '1'
    return amount.quantize(Decimal(quantize_str), rounding=rounding_mode)


def format_multi(
    amount: Union[int, float, Decimal, str],
    code: str = "USD",
    target_codes: Optional[List[str]] = None,
    rates: Optional[Dict[str, float]] = None
) -> Dict[str, str]:
    """多币种格式化显示
    
    Args:
        amount: 金额
        code: 源货币代码
        target_codes: 目标货币代码列表（默认包含主要货币）
        rates: 汇率字典
        
    Returns:
        字典：货币代码 -> 格式化后的字符串
    """
    if target_codes is None:
        target_codes = ["USD", "EUR", "GBP", "JPY", "CNY"]
    
    result = {}
    amount_dec = Decimal(str(amount))
    
    for target in target_codes:
        try:
            converted = convert(amount, code, target, rates)
            result[target] = format_currency(converted, target)
        except ValueError:
            continue
    
    return result


def compare(a: Union[Currency, int, float, Decimal, str], b: Union[Currency, int, float, Decimal, str]) -> int:
    """比较两个货币金额（自动转换后比较）
    
    Args:
        a: 第一个金额或 Currency 对象
        b: 第二个金额或 Currency 对象
        
    Returns:
        -1: a < b
         0: a == b
         1: a > b
    """
    a_obj = a if isinstance(a, Currency) else Currency(a, "USD")
    b_obj = b if isinstance(b, Currency) else Currency(b, "USD")
    
    # 尝试转换到同一货币
    try:
        a_value = convert(a_obj.amount, a_obj.code, "USD") if a_obj.code != "USD" else a_obj.amount
        b_value = convert(b_obj.amount, b_obj.code, "USD") if b_obj.code != "USD" else b_obj.amount
    except ValueError:
        # 如果转换失败，直接比较
        a_value = a_obj.amount
        b_value = b_obj.amount
    
    if a_value < b_value:
        return -1
    elif a_value > b_value:
        return 1
    return 0


def calculate_fees(
    amount: Union[int, float, Decimal, str],
    code: str = "USD",
    fee_percent: float = 0.0,
    fee_fixed: Union[int, float, Decimal, str] = 0,
    min_fee: Union[int, float, Decimal, str] = 0,
    max_fee: Optional[Union[int, float, Decimal, str]] = None
) -> Dict[str, Decimal]:
    """计算手续费
    
    Args:
        amount: 金额
        code: 货币代码
        fee_percent: 百分比手续费（0.03 = 3%）
        fee_fixed: 固定手续费
        min_fee: 最低手续费
        max_fee: 最高手续费上限
        
    Returns:
        包含 fee_percent, fee_fixed, total_fee, net_amount 的字典
    """
    amount = Decimal(str(amount))
    fee_fixed = Decimal(str(fee_fixed))
    min_fee = Decimal(str(min_fee))
    
    # 计算百分比手续费
    percent_fee = amount * Decimal(str(fee_percent))
    
    # 计算总手续费
    total_fee = percent_fee + fee_fixed
    
    # 应用最小/最大限制
    if min_fee > 0:
        total_fee = max(total_fee, min_fee)
    
    if max_fee is not None:
        max_fee_dec = Decimal(str(max_fee))
        total_fee = min(total_fee, max_fee_dec)
    
    return {
        "fee_percent": percent_fee.quantize(Decimal('0.01')),
        "fee_fixed": fee_fixed.quantize(Decimal('0.01')),
        "total_fee": total_fee.quantize(Decimal('0.01')),
        "net_amount": (amount - total_fee).quantize(Decimal('0.01')),
        "gross_amount": amount.quantize(Decimal('0.01'))
    }


def cents_to_amount(cents: int, code: str = "USD") -> Decimal:
    """将整数（最小货币单位，如分、 cent）转换为金额
    
    Args:
        cents: 整数金额（最小单位）
        code: 货币代码
        
    Returns:
        转换后的金额
    """
    if not validate_code(code):
        raise ValueError(f"无效的货币代码: {code}")
    
    decimals = CURRENCY_DATA[code.upper()]["decimals"]
    divisor = Decimal('10') ** decimals
    
    return Decimal(str(cents)) / divisor


def amount_to_cents(amount: Union[int, float, Decimal, str], code: str = "USD") -> int:
    """将金额转换为整数（最小货币单位）
    
    Args:
        amount: 金额
        code: 货币代码
        
    Returns:
        整数金额（最小单位）
    """
    if not validate_code(code):
        raise ValueError(f"无效的货币代码: {code}")
    
    amount = Decimal(str(amount))
    decimals = CURRENCY_DATA[code.upper()]["decimals"]
    multiplier = Decimal('10') ** decimals
    
    return int((amount * multiplier).quantize(Decimal('1')))


def list_currencies() -> List[str]:
    """获取所有支持的货币代码列表
    
    Returns:
        货币代码列表
    """
    return sorted(CURRENCY_DATA.keys())


def get_supported_currencies() -> Dict[str, Dict]:
    """获取所有支持的货币信息
    
    Returns:
        货币代码 -> 货币信息字典
    """
    return CURRENCY_DATA.copy()


# ============ 测试代码 ============

def _run_tests():
    """运行测试"""
    print("Currency Utils - 货币处理工具模块测试")
    print("=" * 50)
    
    # 测试 Currency 类
    print("\n1. Currency 类测试:")
    price = Currency(1234.567, "USD")
    print(f"   金额: {price.amount}")
    print(f"   符号: {price.symbol}")
    print(f"   名称: {price.name}")
    print(f"   格式化: {price.formatted()}")
    
    # 算术运算
    price2 = Currency(100, "USD")
    print(f"   加法: {price + price2}")
    print(f"   乘法: {price * 2}")
    
    # 测试格式化和解析
    print("\n2. 格式化和解析测试:")
    test_values = [
        ("$1,234.56", None),
        ("€1.234,56", "EUR"),
        ("¥1234", "JPY"),
        ("1234.56 USD", None),
        ("-1,234.56", None),
    ]
    
    for value, code in test_values:
        try:
            amount, detected = parse_currency(value, code)
            print(f"   解析 '{value}': {amount} ({detected})")
        except Exception as e:
            print(f"   解析 '{value}' 失败: {e}")
    
    # 测试货币转换
    print("\n3. 货币转换测试:")
    amounts = [100, 1000.50, 10000]
    for amt in amounts:
        usd = Currency(amt, "USD")
        eur = exchange(amt, "USD", "EUR")
        cny = exchange(amt, "USD", "CNY")
        jpy = exchange(amt, "USD", "JPY")
        print(f"   ${amt} USD = {eur} EUR = {cny} CNY = {jpy} JPY")
    
    # 测试汇率获取
    print("\n4. 汇率测试:")
    print(f"   USD -> EUR: {get_rate('USD', 'EUR'):.4f}")
    print(f"   EUR -> JPY: {get_rate('EUR', 'JPY'):.4f}")
    print(f"   CNY -> USD: {get_rate('CNY', 'USD'):.4f}")
    
    # 测试多币种显示
    print("\n5. 多币种显示测试:")
    multi = format_multi(1000, "USD", ["USD", "EUR", "GBP", "CNY", "JPY"])
    for code, formatted in multi.items():
        print(f"   {code}: {formatted}")
    
    # 测试手续费计算
    print("\n6. 手续费计算测试:")
    fee_result = calculate_fees(1000, "USD", fee_percent=0.0325, fee_fixed=1.50, min_fee=2)
    print(f"   订单金额: ${fee_result['gross_amount']}")
    print(f"   百分比费: ${fee_result['fee_percent']}")
    print(f"   固定费: ${fee_result['fee_fixed']}")
    print(f"   总手续费: ${fee_result['total_fee']}")
    print(f"   净额: ${fee_result['net_amount']}")
    
    # 测试分/元转换
    print("\n7. 最小单位转换测试:")
    for code in ["USD", "JPY", "KRW"]:
        cents = amount_to_cents(100.50, code)
        back = cents_to_amount(cents, code)
        print(f"   {code}: 100.50 -> {cents} cents -> {back}")
    
    # 测试支持的货币列表
    print("\n8. 支持的货币列表:")
    currencies = list_currencies()
    print(f"   共 {len(currencies)} 种货币")
    print(f"   示例: {', '.join(currencies[:10])}...")
    
    print("\n" + "=" * 50)
    print("测试完成!")


if __name__ == "__main__":
    _run_tests()