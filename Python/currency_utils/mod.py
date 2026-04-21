"""
Currency Utils - 货币工具库

零依赖的货币处理库，支持：
- ISO 4217 货币代码验证与查询
- 货币格式化（符号、小数位、千位分隔符）
- 精确货币计算（避免浮点误差）
- 多语言本地化支持
- 汇率转换辅助
- 币种信息查询

Author: AllToolkit
License: MIT
"""

from typing import Union, List, Dict, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, getcontext
import re

# 设置 Decimal 精度
getcontext().prec = 28

# ============================================================================
# ISO 4217 货币数据
# ============================================================================

# 货币信息: (名称, 符号, 小数位数, 数字代码)
CURRENCIES: Dict[str, Tuple[str, str, int, str]] = {
    # 主要货币
    'USD': ('US Dollar', '$', 2, '840'),
    'EUR': ('Euro', '€', 2, '978'),
    'GBP': ('British Pound', '£', 2, '826'),
    'JPY': ('Japanese Yen', '¥', 0, '392'),
    'CNY': ('Chinese Yuan', '¥', 2, '156'),
    'KRW': ('South Korean Won', '₩', 0, '410'),
    'INR': ('Indian Rupee', '₹', 2, '356'),
    'AUD': ('Australian Dollar', '$', 2, '036'),
    'CAD': ('Canadian Dollar', '$', 2, '124'),
    'CHF': ('Swiss Franc', 'CHF', 2, '756'),
    'HKD': ('Hong Kong Dollar', '$', 2, '344'),
    'SGD': ('Singapore Dollar', '$', 2, '702'),
    'SEK': ('Swedish Krona', 'kr', 2, '752'),
    'NOK': ('Norwegian Krone', 'kr', 2, '578'),
    'DKK': ('Danish Krone', 'kr', 2, '208'),
    'NZD': ('New Zealand Dollar', '$', 2, '554'),
    'ZAR': ('South African Rand', 'R', 2, '710'),
    'RUB': ('Russian Ruble', '₽', 2, '643'),
    'BRL': ('Brazilian Real', 'R$', 2, '986'),
    'MXN': ('Mexican Peso', '$', 2, '484'),
    'THB': ('Thai Baht', '฿', 2, '764'),
    'IDR': ('Indonesian Rupiah', 'Rp', 0, '360'),
    'MYR': ('Malaysian Ringgit', 'RM', 2, '458'),
    'PHP': ('Philippine Peso', '₱', 2, '608'),
    'VND': ('Vietnamese Dong', '₫', 0, '704'),
    'PLN': ('Polish Zloty', 'zł', 2, '985'),
    'TRY': ('Turkish Lira', '₺', 2, '949'),
    'ILS': ('Israeli New Shekel', '₪', 2, '376'),
    'SAR': ('Saudi Riyal', '﷼', 2, '682'),
    'AED': ('UAE Dirham', 'د.إ', 2, '784'),
    'EGP': ('Egyptian Pound', '£', 2, '818'),
    'NGN': ('Nigerian Naira', '₦', 2, '566'),
    'KES': ('Kenyan Shilling', 'KSh', 2, '404'),
    'GHS': ('Ghanaian Cedi', '₵', 2, '936'),
    'UAH': ('Ukrainian Hryvnia', '₴', 2, '980'),
    'CZK': ('Czech Koruna', 'Kč', 2, '203'),
    'HUF': ('Hungarian Forint', 'Ft', 0, '348'),
    'RON': ('Romanian Leu', 'lei', 2, '946'),
    'BGN': ('Bulgarian Lev', 'лв', 2, '975'),
    'HRK': ('Croatian Kuna', 'kn', 2, '191'),
    'ISK': ('Icelandic Krona', 'kr', 0, '352'),
    'CLP': ('Chilean Peso', '$', 0, '152'),
    'COP': ('Colombian Peso', '$', 0, '170'),
    'PEN': ('Peruvian Sol', 'S/', 2, '604'),
    'ARS': ('Argentine Peso', '$', 2, '032'),
    'TWD': ('Taiwan Dollar', 'NT$', 2, '901'),
    'PKR': ('Pakistani Rupee', '₨', 2, '586'),
    'BDT': ('Bangladeshi Taka', '৳', 2, '050'),
    'LKR': ('Sri Lankan Rupee', '₨', 2, '144'),
    'NPR': ('Nepalese Rupee', '₨', 2, '524'),
    'MMK': ('Myanmar Kyat', 'K', 0, '104'),
    'KHR': ('Cambodian Riel', '៛', 2, '116'),
    'LAK': ('Lao Kip', '₭', 2, '418'),
    'MNT': ('Mongolian Tugrik', '₮', 2, '496'),
    'FJD': ('Fijian Dollar', '$', 2, '242'),
    'WST': ('Samoan Tala', 'T', 2, '882'),
    'TND': ('Tunisian Dinar', 'د.ت', 3, '788'),
    'DZD': ('Algerian Dinar', 'د.ج', 2, '012'),
    'MAD': ('Moroccan Dirham', 'د.م.', 2, '504'),
    'JOD': ('Jordanian Dinar', 'د.ا', 3, '400'),
    'KWD': ('Kuwaiti Dinar', 'د.ك', 3, '414'),
    'BHD': ('Bahraini Dinar', 'د.ب', 3, '048'),
    'OMR': ('Omani Rial', 'ر.ع.', 3, '512'),
    'QAR': ('Qatari Riyal', 'ر.ق', 2, '634'),
    'BND': ('Brunei Dollar', '$', 2, '096'),
    # 加密货币（非 ISO 4217，但常用）
    'BTC': ('Bitcoin', '₿', 8, '000'),
    'ETH': ('Ethereum', 'Ξ', 18, '000'),
    'XRP': ('Ripple', 'XRP', 6, '000'),
}

# 货币符号到代码的映射（多对一）
SYMBOL_TO_CURRENCIES: Dict[str, List[str]] = {}
for code, (_, symbol, _, _) in CURRENCIES.items():
    if symbol not in SYMBOL_TO_CURRENCIES:
        SYMBOL_TO_CURRENCIES[symbol] = []
    SYMBOL_TO_CURRENCIES[symbol].append(code)

# 数字代码到字母代码的映射
NUMERIC_TO_CODE: Dict[str, str] = {
    num_code: code for code, (_, _, _, num_code) in CURRENCIES.items()
    if num_code != '000'  # 排除加密货币
}


# ============================================================================
# 异常类
# ============================================================================

class CurrencyError(Exception):
    """货币错误基类"""
    pass


class InvalidCurrencyError(CurrencyError):
    """无效货币代码错误"""
    pass


class InvalidAmountError(CurrencyError):
    """无效金额错误"""
    pass


class UnsupportedLocaleError(CurrencyError):
    """不支持的本地化错误"""
    pass


# ============================================================================
# 本地化格式配置
# ============================================================================

# 本地化格式: (小数分隔符, 千位分隔符, 符号位置, 符号与金额间距)
# 符号位置: 'before' 或 'after'
LOCALE_FORMATS: Dict[str, Tuple[str, str, str, str]] = {
    'en_US': ('.', ',', 'before', ''),       # $1,234.56
    'en_GB': ('.', ',', 'before', ''),       # £1,234.56
    'de_DE': (',', '.', 'after', ' '),       # 1.234,56 €
    'fr_FR': (',', ' ', 'after', ' '),       # 1 234,56 €
    'ja_JP': ('.', ',', 'before', ''),       # ¥1,234
    'zh_CN': ('.', ',', 'before', ''),       # ¥1,234.56
    'zh_TW': ('.', ',', 'before', ''),       # NT$1,234.56
    'ko_KR': ('.', ',', 'before', ''),       # ₩1,234
    'ru_RU': (',', ' ', 'after', ' '),       # 1 234,56 ₽
    'pt_BR': (',', '.', 'before', ' '),      # R$ 1.234,56
    'es_ES': (',', '.', 'after', ' '),       # 1.234,56 €
    'es_MX': ('.', ',', 'before', ''),       # $1,234.56
    'it_IT': (',', '.', 'after', ' '),       # 1.234,56 €
    'nl_NL': (',', '.', 'before', ' '),      # € 1.234,56
    'pl_PL': (',', ' ', 'after', ' '),       # 1 234,56 zł
    'tr_TR': (',', '.', 'after', ' '),       # 1.234,56 ₺
    'th_TH': ('.', ',', 'before', ''),       # ฿1,234.56
    'vi_VN': (',', '.', 'after', ''),        # 1.234₫
    'id_ID': (',', '.', 'before', ''),       # Rp1.234
    'ms_MY': ('.', ',', 'before', ''),       # RM1,234.56
    'ar_SA': ('.', ',', 'before', ' '),      # ﷼ 1,234.56
    'he_IL': ('.', ',', 'before', ' '),      # ₪1,234.56
    'hi_IN': ('.', ',', 'before', ''),       # ₹1,234.56
    'bn_BD': ('.', ',', 'before', ''),       # ৳1,234.56
}


# ============================================================================
# 核心类
# ============================================================================

class Money:
    """
    货币金额类，支持精确计算
    
    使用 Decimal 避免浮点精度问题
    """
    
    def __init__(
        self,
        amount: Union[int, float, str, Decimal],
        currency: str
    ):
        """
        初始化货币金额
        
        Args:
            amount: 金额
            currency: 货币代码
        
        Raises:
            InvalidCurrencyError: 无效的货币代码
            InvalidAmountError: 无效的金额
        """
        currency = currency.upper()
        if currency not in CURRENCIES:
            raise InvalidCurrencyError(f"无效的货币代码: {currency}")
        
        self.currency = currency
        
        # 转换为 Decimal
        try:
            if isinstance(amount, Decimal):
                self._amount = amount
            elif isinstance(amount, float):
                # 浮点数转换需要特殊处理
                self._amount = Decimal(str(amount))
            else:
                self._amount = Decimal(str(amount))
        except Exception as e:
            raise InvalidAmountError(f"无效的金额: {amount}") from e
        
        # 获取小数位数
        self._decimals = CURRENCIES[currency][2]
    
    @property
    def amount(self) -> Decimal:
        """获取金额"""
        return self._amount
    
    @property
    def decimals(self) -> int:
        """获取小数位数"""
        return self._decimals
    
    @property
    def symbol(self) -> str:
        """获取货币符号"""
        return CURRENCIES[self.currency][1]
    
    @property
    def name(self) -> str:
        """获取货币名称"""
        return CURRENCIES[self.currency][0]
    
    @property
    def numeric_code(self) -> str:
        """获取数字代码"""
        return CURRENCIES[self.currency][3]
    
    def round(self) -> 'Money':
        """按照货币精度四舍五入"""
        quantize_str = '1.' + '0' * self._decimals
        rounded = self._amount.quantize(
            Decimal(quantize_str),
            rounding=ROUND_HALF_UP
        )
        return Money(rounded, self.currency)
    
    def format(
        self,
        locale: str = 'en_US',
        include_symbol: bool = True,
        include_code: bool = False
    ) -> str:
        """
        格式化货币
        
        Args:
            locale: 本地化设置
            include_symbol: 是否包含货币符号
            include_code: 是否包含货币代码
        
        Returns:
            格式化后的字符串
        """
        return format_money(
            self._amount,
            self.currency,
            locale,
            include_symbol,
            include_code
        )
    
    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("只能与 Money 对象相加")
        if self.currency != other.currency:
            raise CurrencyError(f"货币不匹配: {self.currency} vs {other.currency}")
        return Money(self._amount + other._amount, self.currency)
    
    def __sub__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("只能与 Money 对象相减")
        if self.currency != other.currency:
            raise CurrencyError(f"货币不匹配: {self.currency} vs {other.currency}")
        return Money(self._amount - other._amount, self.currency)
    
    def __mul__(self, other: Union[int, float, Decimal]) -> 'Money':
        if isinstance(other, float):
            other = Decimal(str(other))
        return Money(self._amount * other, self.currency)
    
    def __rmul__(self, other: Union[int, float, Decimal]) -> 'Money':
        return self.__mul__(other)
    
    def __truediv__(self, other: Union[int, float, Decimal]) -> 'Money':
        if isinstance(other, float):
            other = Decimal(str(other))
        if other == 0:
            raise ZeroDivisionError("不能除以零")
        return Money(self._amount / other, self.currency)
    
    def __floordiv__(self, other: Union[int, float, Decimal]) -> 'Money':
        if isinstance(other, float):
            other = Decimal(str(other))
        if other == 0:
            raise ZeroDivisionError("不能除以零")
        return Money(self._amount // other, self.currency)
    
    def __mod__(self, other: Union[int, float, Decimal]) -> 'Money':
        if isinstance(other, float):
            other = Decimal(str(other))
        if other == 0:
            raise ZeroDivisionError("不能除以零")
        return Money(self._amount % other, self.currency)
    
    def __neg__(self) -> 'Money':
        return Money(-self._amount, self.currency)
    
    def __abs__(self) -> 'Money':
        return Money(abs(self._amount), self.currency)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self._amount == other._amount and self.currency == other.currency
    
    def __lt__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise CurrencyError(f"货币不匹配: {self.currency} vs {other.currency}")
        return self._amount < other._amount
    
    def __le__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise CurrencyError(f"货币不匹配: {self.currency} vs {other.currency}")
        return self._amount <= other._amount
    
    def __gt__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise CurrencyError(f"货币不匹配: {self.currency} vs {other.currency}")
        return self._amount > other._amount
    
    def __ge__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise CurrencyError(f"货币不匹配: {self.currency} vs {other.currency}")
        return self._amount >= other._amount
    
    def __bool__(self) -> bool:
        return self._amount != 0
    
    def __repr__(self) -> str:
        return f"Money({self._amount}, '{self.currency}')"
    
    def __str__(self) -> str:
        return self.format()


# ============================================================================
# 货币验证函数
# ============================================================================

def is_valid_currency(code: str) -> bool:
    """
    验证货币代码是否有效
    
    Args:
        code: 货币代码
    
    Returns:
        是否为有效的货币代码
    
    Example:
        >>> is_valid_currency('USD')
        True
        >>> is_valid_currency('XXX')
        False
    """
    return code.upper() in CURRENCIES


def is_valid_numeric_code(code: str) -> bool:
    """
    验证数字代码是否有效
    
    Args:
        code: 数字代码
    
    Returns:
        是否为有效的数字代码
    
    Example:
        >>> is_valid_numeric_code('840')
        True
        >>> is_valid_numeric_code('000')
        False
    """
    return code in NUMERIC_TO_CODE


def get_currency_info(code: str) -> Dict[str, Union[str, int]]:
    """
    获取货币信息
    
    Args:
        code: 货币代码
    
    Returns:
        货币信息字典
    
    Raises:
        InvalidCurrencyError: 无效的货币代码
    
    Example:
        >>> info = get_currency_info('USD')
        >>> info['name']
        'US Dollar'
        >>> info['symbol']
        '$'
    """
    code = code.upper()
    if code not in CURRENCIES:
        raise InvalidCurrencyError(f"无效的货币代码: {code}")
    
    name, symbol, decimals, numeric = CURRENCIES[code]
    return {
        'code': code,
        'name': name,
        'symbol': symbol,
        'decimals': decimals,
        'numeric_code': numeric,
    }


def get_currencies_by_symbol(symbol: str) -> List[str]:
    """
    根据符号获取货币代码列表
    
    Args:
        symbol: 货币符号
    
    Returns:
        货币代码列表
    
    Example:
        >>> get_currencies_by_symbol('$')
        ['USD', 'AUD', 'CAD', 'HKD', 'SGD', 'NZD', 'MXN', 'BND', 'CLP', 'COP', 'ARS', 'FJD', 'TWD']
    """
    return SYMBOL_TO_CURRENCIES.get(symbol, [])


def get_all_currencies() -> List[str]:
    """
    获取所有货币代码
    
    Returns:
        货币代码列表
    
    Example:
        >>> 'USD' in get_all_currencies()
        True
    """
    return list(CURRENCIES.keys())


def get_major_currencies() -> List[str]:
    """
    获取主要货币代码
    
    Returns:
        主要货币代码列表
    
    Example:
        >>> 'USD' in get_major_currencies()
        True
    """
    return ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'AUD', 'CAD', 'HKD', 'SGD']


# ============================================================================
# 格式化函数
# ============================================================================

def format_money(
    amount: Union[int, float, str, Decimal],
    currency: str,
    locale: str = 'en_US',
    include_symbol: bool = True,
    include_code: bool = False
) -> str:
    """
    格式化货币金额
    
    Args:
        amount: 金额
        currency: 货币代码
        locale: 本地化设置
        include_symbol: 是否包含货币符号
        include_code: 是否包含货币代码
    
    Returns:
        格式化后的字符串
    
    Raises:
        InvalidCurrencyError: 无效的货币代码
    
    Example:
        >>> format_money(1234.56, 'USD')
        '$1,234.56'
        >>> format_money(1234.56, 'EUR', 'de_DE')
        '1.234,56 €'
        >>> format_money(1234, 'JPY')
        '¥1,234'
    """
    currency = currency.upper()
    if currency not in CURRENCIES:
        raise InvalidCurrencyError(f"无效的货币代码: {currency}")
    
    # 转换为 Decimal
    if isinstance(amount, Decimal):
        dec_amount = amount
    elif isinstance(amount, float):
        dec_amount = Decimal(str(amount))
    else:
        dec_amount = Decimal(str(amount))
    
    # 获取货币信息
    _, symbol, decimals, _ = CURRENCIES[currency]
    
    # 四舍五入到货币精度
    quantize_str = '1.' + '0' * decimals
    dec_amount = dec_amount.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
    
    # 获取本地化格式
    if locale in LOCALE_FORMATS:
        decimal_sep, thousand_sep, symbol_pos, symbol_space = LOCALE_FORMATS[locale]
    else:
        # 默认美式格式
        decimal_sep, thousand_sep, symbol_pos, symbol_space = '.', ',', 'before', ''
    
    # 转换为字符串并分割整数和小数部分
    amount_str = str(dec_amount)
    if '.' in amount_str:
        int_part, dec_part = amount_str.split('.')
    else:
        int_part = amount_str
        dec_part = ''
    
    # 处理负数
    is_negative = int_part.startswith('-')
    if is_negative:
        int_part = int_part[1:]
    
    # 添加千位分隔符
    if thousand_sep:
        formatted_int = ''
        for i, digit in enumerate(reversed(int_part)):
            if i > 0 and i % 3 == 0:
                formatted_int = thousand_sep + formatted_int
            formatted_int = digit + formatted_int
    else:
        formatted_int = int_part
    
    # 组合整数和小数部分
    if decimals > 0:
        # 有小数位的货币，总是显示指定的小数位
        if dec_part:
            formatted_amount = formatted_int + decimal_sep + dec_part[:decimals].ljust(decimals, '0')
        else:
            formatted_amount = formatted_int + decimal_sep + '0' * decimals
    else:
        # 无小数位的货币
        formatted_amount = formatted_int
    
    # 添加负号
    if is_negative:
        formatted_amount = '-' + formatted_amount
    
    # 添加货币符号
    result = formatted_amount
    if include_symbol:
        if is_negative:
            # 负数：符号在负号之前
            result = '-' + symbol + symbol_space + formatted_amount[1:] if formatted_amount.startswith('-') else '-' + symbol + symbol_space + formatted_amount
        elif symbol_pos == 'before':
            result = symbol + symbol_space + result
        else:
            result = result + symbol_space + symbol
    
    # 添加货币代码
    if include_code:
        result = result + ' ' + currency
    
    return result


def parse_money(
    money_str: str,
    currency: Optional[str] = None,
    locale: str = 'en_US'
) -> Tuple[Decimal, str]:
    """
    解析货币字符串
    
    Args:
        money_str: 货币字符串
        currency: 货币代码（如果字符串中不包含）
        locale: 本地化设置
    
    Returns:
        (金额, 货币代码)
    
    Raises:
        InvalidAmountError: 无法解析金额
        InvalidCurrencyError: 无法确定货币代码
    
    Example:
        >>> parse_money('$1,234.56', 'USD')
        (Decimal('1234.56'), 'USD')
        >>> parse_money('1.234,56 €', locale='de_DE')
        (Decimal('1234.56'), 'EUR')
    """
    # 移除空白
    money_str = money_str.strip()
    
    # 尝试识别货币符号
    detected_currency = None
    for symbol, codes in SYMBOL_TO_CURRENCIES.items():
        if symbol in money_str:
            # 如果只有一个货币使用此符号
            if len(codes) == 1:
                detected_currency = codes[0]
                break
            # 如果有多个，使用第一个（通常是主要货币）
            detected_currency = codes[0]
    
    # 确定货币
    final_currency = currency or detected_currency
    if not final_currency:
        raise InvalidCurrencyError("无法确定货币代码")
    
    final_currency = final_currency.upper()
    
    # 验证货币
    if final_currency not in CURRENCIES:
        raise InvalidCurrencyError(f"无效的货币代码: {final_currency}")
    
    # 获取本地化格式
    if locale in LOCALE_FORMATS:
        decimal_sep, thousand_sep, _, _ = LOCALE_FORMATS[locale]
    else:
        decimal_sep, thousand_sep = '.', ','
    
    # 移除货币符号
    clean_str = money_str
    for symbol in SYMBOL_TO_CURRENCIES.keys():
        clean_str = clean_str.replace(symbol, '')
    
    # 移除货币代码
    clean_str = re.sub(r'\b[A-Z]{3}\b', '', clean_str)
    
    # 移除空白
    clean_str = clean_str.strip()
    
    # 处理千位分隔符和小数点
    if thousand_sep:
        clean_str = clean_str.replace(thousand_sep, '')
    if decimal_sep != '.':
        clean_str = clean_str.replace(decimal_sep, '.')
    
    # 解析金额
    try:
        amount = Decimal(clean_str)
    except Exception as e:
        raise InvalidAmountError(f"无法解析金额: {money_str}") from e
    
    return amount, final_currency


def format_number(
    number: Union[int, float, str, Decimal],
    decimals: int = 2,
    locale: str = 'en_US'
) -> str:
    """
    格式化数字
    
    Args:
        number: 数字
        decimals: 小数位数
        locale: 本地化设置
    
    Returns:
        格式化后的字符串
    
    Example:
        >>> format_number(1234.5678, 2)
        '1,234.57'
        >>> format_number(1234.5678, 2, 'de_DE')
        '1.234,57'
    """
    # 转换为 Decimal
    if isinstance(number, Decimal):
        dec_number = number
    elif isinstance(number, float):
        dec_number = Decimal(str(number))
    else:
        dec_number = Decimal(str(number))
    
    # 四舍五入
    quantize_str = '1.' + '0' * decimals
    dec_number = dec_number.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
    
    # 获取本地化格式
    if locale in LOCALE_FORMATS:
        decimal_sep, thousand_sep, _, _ = LOCALE_FORMATS[locale]
    else:
        decimal_sep, thousand_sep = '.', ','
    
    # 转换为字符串
    number_str = str(dec_number)
    
    # 处理负数
    is_negative = number_str.startswith('-')
    if is_negative:
        number_str = number_str[1:]
    
    # 分割整数和小数部分
    if '.' in number_str:
        int_part, dec_part = number_str.split('.')
    else:
        int_part = number_str
        dec_part = '0' * decimals
    
    # 添加千位分隔符
    if thousand_sep:
        formatted_int = ''
        for i, digit in enumerate(reversed(int_part)):
            if i > 0 and i % 3 == 0:
                formatted_int = thousand_sep + formatted_int
            formatted_int = digit + formatted_int
    else:
        formatted_int = int_part
    
    # 组合
    if decimals > 0:
        result = formatted_int + decimal_sep + dec_part[:decimals].ljust(decimals, '0')
    else:
        result = formatted_int
    
    if is_negative:
        result = '-' + result
    
    return result


# ============================================================================
# 汇率转换函数
# ============================================================================

class ExchangeRates:
    """
    汇率管理类
    
    存储和管理汇率数据，支持货币转换
    """
    
    def __init__(self, base_currency: str = 'USD'):
        """
        初始化汇率管理器
        
        Args:
            base_currency: 基准货币
        """
        self.base_currency = base_currency.upper()
        self._rates: Dict[str, Decimal] = {self.base_currency: Decimal('1')}
    
    def set_rate(self, currency: str, rate: Union[int, float, str, Decimal]) -> None:
        """
        设置汇率（相对于基准货币）
        
        Args:
            currency: 货币代码
            rate: 汇率
        """
        currency = currency.upper()
        if isinstance(rate, float):
            rate = Decimal(str(rate))
        else:
            rate = Decimal(str(rate))
        self._rates[currency] = rate
    
    def set_rates(self, rates: Dict[str, Union[int, float, str, Decimal]]) -> None:
        """
        批量设置汇率
        
        Args:
            rates: 汇率字典
        """
        for currency, rate in rates.items():
            self.set_rate(currency, rate)
    
    def get_rate(self, currency: str) -> Optional[Decimal]:
        """
        获取汇率
        
        Args:
            currency: 货币代码
        
        Returns:
            汇率，如果不存在则返回 None
        """
        return self._rates.get(currency.upper())
    
    def convert(
        self,
        amount: Union[int, float, str, Decimal, Money],
        from_currency: str = None,
        to_currency: str = None
    ) -> Money:
        """
        货币转换
        
        Args:
            amount: 金额（Money 对象或数值）
            from_currency: 源货币代码（如果 amount 是数值则需要）
            to_currency: 目标货币代码
        
        Returns:
            转换后的 Money 对象
        
        Raises:
            InvalidCurrencyError: 货币代码无效或汇率缺失
        """
        # 处理 Money 对象
        if isinstance(amount, Money):
            from_currency = amount.currency
            amount = amount.amount
        
        if from_currency is None or to_currency is None:
            raise InvalidCurrencyError("必须指定源货币和目标货币")
        
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # 验证货币
        if from_currency not in CURRENCIES:
            raise InvalidCurrencyError(f"无效的源货币: {from_currency}")
        if to_currency not in CURRENCIES:
            raise InvalidCurrencyError(f"无效的目标货币: {to_currency}")
        
        # 转换为 Decimal
        if isinstance(amount, float):
            amount = Decimal(str(amount))
        else:
            amount = Decimal(str(amount))
        
        # 相同货币
        if from_currency == to_currency:
            return Money(amount, to_currency)
        
        # 获取汇率
        from_rate = self._rates.get(from_currency)
        to_rate = self._rates.get(to_currency)
        
        if from_rate is None:
            raise InvalidCurrencyError(f"缺少 {from_currency} 的汇率")
        if to_rate is None:
            raise InvalidCurrencyError(f"缺少 {to_currency} 的汇率")
        
        # 转换：先转成基准货币，再转成目标货币
        base_amount = amount / from_rate
        converted = base_amount * to_rate
        
        return Money(converted, to_currency)
    
    def get_supported_currencies(self) -> List[str]:
        """获取支持的货币列表"""
        return list(self._rates.keys())
    
    def __repr__(self) -> str:
        return f"ExchangeRates(base='{self.base_currency}', rates={len(self._rates)})"


def convert_money(
    amount: Union[int, float, str, Decimal, Money],
    from_currency: str,
    to_currency: str,
    rate: Union[int, float, str, Decimal]
) -> Money:
    """
    简单货币转换
    
    Args:
        amount: 金额
        from_currency: 源货币代码
        to_currency: 目标货币代码
        rate: 汇率（1 源货币 = rate 目标货币）
    
    Returns:
        转换后的 Money 对象
    
    Example:
        >>> convert_money(100, 'USD', 'CNY', 7.2)
        Money(720, 'CNY')
    """
    # 处理 Money 对象
    if isinstance(amount, Money):
        from_currency = amount.currency
        amount = amount.amount
    
    # 验证货币
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    if from_currency not in CURRENCIES:
        raise InvalidCurrencyError(f"无效的源货币: {from_currency}")
    if to_currency not in CURRENCIES:
        raise InvalidCurrencyError(f"无效的目标货币: {to_currency}")
    
    # 转换
    if isinstance(amount, float):
        amount = Decimal(str(amount))
    else:
        amount = Decimal(str(amount))
    
    if isinstance(rate, float):
        rate = Decimal(str(rate))
    else:
        rate = Decimal(str(rate))
    
    converted = amount * rate
    
    return Money(converted, to_currency)


# ============================================================================
# 货币计算辅助函数
# ============================================================================

def add_taxes(
    amount: Union[int, float, str, Decimal, Money],
    tax_rate: Union[int, float, str, Decimal],
    currency: str = None
) -> Money:
    """
    添加税费
    
    Args:
        amount: 金额
        tax_rate: 税率（如 0.1 表示 10%）
        currency: 货币代码（如果 amount 不是 Money 对象）
    
    Returns:
        包含税费的总金额
    
    Example:
        >>> add_taxes(100, 0.1, 'USD')
        Money(110, 'USD')
    """
    if isinstance(amount, Money):
        currency = amount.currency
        amount = amount.amount
    elif currency is None:
        raise InvalidCurrencyError("必须指定货币代码")
    
    if isinstance(amount, float):
        amount = Decimal(str(amount))
    else:
        amount = Decimal(str(amount))
    
    if isinstance(tax_rate, float):
        tax_rate = Decimal(str(tax_rate))
    else:
        tax_rate = Decimal(str(tax_rate))
    
    total = amount * (Decimal('1') + tax_rate)
    
    return Money(total, currency)


def apply_discount(
    amount: Union[int, float, str, Decimal, Money],
    discount: Union[int, float, str, Decimal],
    discount_type: str = 'percent',
    currency: str = None
) -> Money:
    """
    应用折扣
    
    Args:
        amount: 原金额
        discount: 折扣值
        discount_type: 折扣类型 ('percent' 或 'fixed')
        currency: 货币代码（如果 amount 不是 Money 对象）
    
    Returns:
        折扣后的金额
    
    Example:
        >>> apply_discount(100, 0.1, 'percent', 'USD')
        Money(90, 'USD')
        >>> apply_discount(100, 10, 'fixed', 'USD')
        Money(90, 'USD')
    """
    if isinstance(amount, Money):
        currency = amount.currency
        amount = amount.amount
    elif currency is None:
        raise InvalidCurrencyError("必须指定货币代码")
    
    if isinstance(amount, float):
        amount = Decimal(str(amount))
    else:
        amount = Decimal(str(amount))
    
    if isinstance(discount, float):
        discount = Decimal(str(discount))
    else:
        discount = Decimal(str(discount))
    
    if discount_type == 'percent':
        result = amount * (Decimal('1') - discount)
    elif discount_type == 'fixed':
        result = amount - discount
    else:
        raise ValueError("discount_type 必须是 'percent' 或 'fixed'")
    
    return Money(result, currency)


def split_amount(
    amount: Union[int, float, str, Decimal, Money],
    parts: int,
    currency: str = None
) -> List[Money]:
    """
    分割金额（避免浮点误差）
    
    Args:
        amount: 金额
        parts: 分割份数
        currency: 货币代码（如果 amount 不是 Money 对象）
    
    Returns:
        分割后的金额列表（确保总和等于原金额）
    
    Example:
        >>> split_amount(100, 3, 'USD')
        [Money('33.34', 'USD'), Money('33.33', 'USD'), Money('33.33', 'USD')]
    """
    if isinstance(amount, Money):
        currency = amount.currency
        amount = amount.amount
    elif currency is None:
        raise InvalidCurrencyError("必须指定货币代码")
    
    if parts <= 0:
        raise ValueError("分割份数必须大于 0")
    
    if isinstance(amount, float):
        amount = Decimal(str(amount))
    else:
        amount = Decimal(str(amount))
    
    # 获取货币精度
    decimals = CURRENCIES[currency][2]
    
    # 计算最小单位
    if decimals > 0:
        min_unit = Decimal('0.' + '0' * (decimals - 1) + '1')
        quantize_str = '1.' + '0' * decimals
    else:
        min_unit = Decimal('1')
        quantize_str = '1'
    
    # 计算基础每份金额（向下舍入）
    each = (amount / parts).quantize(Decimal(quantize_str), rounding=ROUND_DOWN)
    
    # 计算剩余金额（用于分配到前几个部分）
    remainder = amount - (each * parts)
    
    # 计算需要增加的部分数量
    extra_parts = int(remainder / min_unit) if remainder > 0 else 0
    
    # 创建结果列表
    result = []
    for i in range(parts):
        if i < extra_parts:
            result.append(Money(each + min_unit, currency))
        else:
            result.append(Money(each, currency))
    
    return result


def compare_amounts(
    amount1: Union[int, float, str, Decimal, Money],
    amount2: Union[int, float, str, Decimal, Money],
    currency: str = None
) -> int:
    """
    比较两个金额
    
    Args:
        amount1: 第一个金额
        amount2: 第二个金额
        currency: 货币代码（如果金额不是 Money 对象）
    
    Returns:
        -1: amount1 < amount2
        0: amount1 == amount2
        1: amount1 > amount2
    
    Example:
        >>> compare_amounts(100, 200, 'USD')
        -1
    """
    def to_decimal(a: Union[int, float, str, Decimal, Money]) -> Decimal:
        if isinstance(a, Money):
            return a.amount
        if isinstance(a, float):
            return Decimal(str(a))
        return Decimal(str(a))
    
    a1 = to_decimal(amount1)
    a2 = to_decimal(amount2)
    
    if a1 < a2:
        return -1
    elif a1 > a2:
        return 1
    else:
        return 0


def percentage_of(
    part: Union[int, float, str, Decimal, Money],
    total: Union[int, float, str, Decimal, Money]
) -> Decimal:
    """
    计算部分占总体的百分比
    
    Args:
        part: 部分金额
        total: 总金额
    
    Returns:
        百分比（如 0.25 表示 25%）
    
    Raises:
        ZeroDivisionError: 总金额为零
    
    Example:
        >>> percentage_of(25, 100)
        Decimal('0.25')
    """
    def to_decimal(a: Union[int, float, str, Decimal, Money]) -> Decimal:
        if isinstance(a, Money):
            return a.amount
        if isinstance(a, float):
            return Decimal(str(a))
        return Decimal(str(a))
    
    p = to_decimal(part)
    t = to_decimal(total)
    
    if t == 0:
        raise ZeroDivisionError("总金额不能为零")
    
    return p / t


def is_zero(
    amount: Union[int, float, str, Decimal, Money]
) -> bool:
    """
    检查金额是否为零
    
    Args:
        amount: 金额
    
    Returns:
        是否为零
    """
    if isinstance(amount, Money):
        return amount.amount == 0
    if isinstance(amount, float):
        return amount == 0
    return Decimal(str(amount)) == 0


def is_negative(
    amount: Union[int, float, str, Decimal, Money]
) -> bool:
    """
    检查金额是否为负
    
    Args:
        amount: 金额
    
    Returns:
        是否为负
    """
    if isinstance(amount, Money):
        return amount.amount < 0
    if isinstance(amount, float):
        return amount < 0
    return Decimal(str(amount)) < 0


def is_positive(
    amount: Union[int, float, str, Decimal, Money]
) -> bool:
    """
    检查金额是否为正
    
    Args:
        amount: 金额
    
    Returns:
        是否为正
    """
    if isinstance(amount, Money):
        return amount.amount > 0
    if isinstance(amount, float):
        return amount > 0
    return Decimal(str(amount)) > 0


# ============================================================================
# 便捷函数
# ============================================================================

def money(
    amount: Union[int, float, str, Decimal],
    currency: str
) -> Money:
    """创建 Money 对象的便捷函数"""
    return Money(amount, currency)


def usd(amount: Union[int, float, str, Decimal]) -> Money:
    """创建美元 Money 对象"""
    return Money(amount, 'USD')


def eur(amount: Union[int, float, str, Decimal]) -> Money:
    """创建欧元 Money 对象"""
    return Money(amount, 'EUR')


def gbp(amount: Union[int, float, str, Decimal]) -> Money:
    """创建英镑 Money 对象"""
    return Money(amount, 'GBP')


def jpy(amount: Union[int, float, str, Decimal]) -> Money:
    """创建日元 Money 对象"""
    return Money(amount, 'JPY')


def cny(amount: Union[int, float, str, Decimal]) -> Money:
    """创建人民币 Money 对象"""
    return Money(amount, 'CNY')


# ============================================================================
# 主函数演示
# ============================================================================

if __name__ == '__main__':
    print("=== 货币工具库演示 ===\n")
    
    # 创建 Money 对象
    price = Money(1234.56, 'USD')
    print(f"价格: {price}")
    print(f"格式化: {price.format()}")
    print(f"德式格式: {price.format(locale='de_DE')}")
    print(f"含税价: {add_taxes(price, 0.1)}")
    
    print()
    
    # 货币转换
    rates = ExchangeRates('USD')
    rates.set_rates({
        'EUR': Decimal('0.92'),
        'GBP': Decimal('0.79'),
        'JPY': Decimal('151.5'),
        'CNY': Decimal('7.24'),
    })
    
    usd_amount = usd(100)
    print(f"原金额: {usd_amount}")
    print(f"转欧元: {rates.convert(usd_amount, to_currency='EUR')}")
    print(f"转英镑: {rates.convert(usd_amount, to_currency='GBP')}")
    print(f"转日元: {rates.convert(usd_amount, to_currency='JPY')}")
    print(f"转人民币: {rates.convert(usd_amount, to_currency='CNY')}")
    
    print()
    
    # 分割金额
    split = split_amount(100, 3, 'USD')
    print(f"分割 $100 为 3 份: {[str(s) for s in split]}")
    print(f"验证总和: {sum(s.amount for s in split)}")
    
    print()
    
    # 折扣
    original = cny(100)
    discounted = apply_discount(original, 0.2, 'percent')
    print(f"原价: {original}")
    print(f"八折后: {discounted}")
    
    print()
    
    # 货币信息
    print(f"USD 信息: {get_currency_info('USD')}")
    print(f"使用 $ 符号的货币: {get_currencies_by_symbol('$')}")
    
    print("\n=== 演示完成 ===")