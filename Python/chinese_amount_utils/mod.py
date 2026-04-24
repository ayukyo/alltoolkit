"""
AllToolkit - Chinese Amount Utilities (中文金额大写转换工具)

零依赖的中文金额转换模块，支持：
- 数字金额转中文大写金额（财务标准格式）
- 支持整数和小数金额
- 支持负数金额
- 支持大额金额（亿级以上）
- 提供多种输出格式选项
- 符合中国财务标准

Author: AllToolkit
License: MIT
"""

from typing import Optional, Tuple, Union
from decimal import Decimal, InvalidOperation


class ChineseAmountError(Exception):
    """中文金额转换异常"""
    pass


# 数字对应的中文大写
_DIGITS_CN = {
    '0': '零',
    '1': '壹',
    '2': '贰',
    '3': '叁',
    '4': '肆',
    '5': '伍',
    '6': '陆',
    '7': '柒',
    '8': '捌',
    '9': '玖',
}

# 数字对应的简体中文
_SIMPLE_DIGITS_CN = {
    '0': '零',
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
    '7': '七',
    '8': '八',
    '9': '九',
}

# 单位
_UNITS_CN = ['', '拾', '佰', '仟']
_LARGE_UNITS_CN = ['', '万', '亿', '兆']

# 货币单位
_YUAN = '元'
_JIAO = '角'
_FEN = '分'
_ZHENG = '整'


def _validate_amount(amount: Union[float, int, str, Decimal]) -> Decimal:
    """
    验证并转换金额为 Decimal 类型。
    
    Args:
        amount: 金额，支持 float, int, str, Decimal
        
    Returns:
        Decimal 类型的金额
        
    Raises:
        ChineseAmountError: 金额无效
    """
    try:
        if isinstance(amount, Decimal):
            dec_amount = amount
        elif isinstance(amount, str):
            # 移除可能的逗号和空格
            amount = amount.replace(',', '').replace(' ', '').strip()
            if not amount or amount == '-':
                raise ChineseAmountError("金额不能为空")
            dec_amount = Decimal(amount)
        else:
            dec_amount = Decimal(str(amount))
        
        return dec_amount
    except (InvalidOperation, ValueError, TypeError):
        raise ChineseAmountError(f"无效的金额格式: {amount}")


def _split_amount(amount: Decimal) -> Tuple[int, int, int]:
    """
    拆分金额为整数部分、角、分。
    
    Args:
        amount: Decimal 类型的金额
        
    Returns:
        (整数部分, 角, 分)
    """
    # 取绝对值处理
    abs_amount = abs(amount)
    
    # 整数部分
    integer_part = int(abs_amount)
    
    # 小数部分处理
    decimal_str = str(abs_amount - integer_part)
    
    # 确保有足够的小数位
    if '.' in decimal_str:
        decimal_part = decimal_str.split('.')[1]
        # 补齐到两位
        decimal_part = (decimal_part + '00')[:2]
    else:
        decimal_part = '00'
    
    jiao = int(decimal_part[0])
    fen = int(decimal_part[1])
    
    return integer_part, jiao, fen


def _convert_group_to_chinese(num: int, is_first_group: bool = False) -> str:
    """
    将一组数字（最多4位）转换为中文大写。
    
    Args:
        num: 数字组（0-9999）
        is_first_group: 是否是最高位组（影响拾的处理）
        
    Returns:
        中文大写字符串
    """
    if num == 0:
        return ''
    
    result = []
    has_zero = False  # 标记是否需要补零（只有当高位已有数字时才补）
    
    # 千位
    if num >= 1000:
        digit = num // 1000
        result.append(_DIGITS_CN[str(digit)] + '仟')
        num %= 1000
        if num == 0:
            return ''.join(result)
    
    # 百位
    if num >= 100:
        digit = num // 100
        result.append(_DIGITS_CN[str(digit)] + '佰')
        num %= 100
        if num == 0:
            return ''.join(result)
    elif num > 0 and result:
        # 百位为零，且前面（千位）已有数字，需要补零
        has_zero = True
    
    # 十位（特殊处理：拾前面不加壹）
    if num >= 10:
        if has_zero:
            result.append('零')
            has_zero = False
        digit = num // 10
        if digit == 1 and is_first_group and not result:
            # 最高位组的十位为1时且前面没有其他数字，只写"拾"不加"壹"
            result.append('拾')
        else:
            result.append(_DIGITS_CN[str(digit)] + '拾')
        num %= 10
        if num == 0:
            return ''.join(result)
    elif num > 0 and result:
        # 十位为零，且前面已有数字，需要补零
        has_zero = True
    
    # 个位
    if num > 0:
        if has_zero:
            result.append('零')
        result.append(_DIGITS_CN[str(num)])
    
    return ''.join(result)


def _convert_integer_to_chinese(num: int) -> str:
    """
    将整数转换为中文大写。
    
    Args:
        num: 整数（非负）
        
    Returns:
        中文大写字符串
    """
    if num == 0:
        return '零'
    
    # 分组：每4位一组
    groups = []
    while num > 0:
        groups.append(num % 10000)
        num //= 10000
    
    result = []
    
    # 从高位到低位处理（反向遍历）
    for i in range(len(groups) - 1, -1, -1):
        group = groups[i]
        
        if group == 0:
            continue
        
        # 是否是最高位组
        is_first = (i == len(groups) - 1)
        
        group_str = _convert_group_to_chinese(group, is_first)
        
        # 添加大单位
        if i > 0:
            unit = _LARGE_UNITS_CN[i]
            group_str = group_str + unit
        
        # 判断是否需要在组后面补零
        # 如果当前组 < 1000（有前导零），且下面有低位组
        if group < 1000 and i > 0:
            # 检查下面的低位组是否有非零数字，且该数字不足千位
            for j in range(i - 1, -1, -1):
                if groups[j] > 0:
                    # 如果低位组 >= 1000，说明低位组的千位有数字，不需要补零
                    # 如果低位组 < 1000，说明低位组的千位为零，需要补零
                    if groups[j] < 1000:
                        group_str = group_str + '零'
                    break
        
        result.append(group_str)
    
    # 处理连续零的问题
    final = ''.join(result)
    
    return final


def to_chinese_amount(
    amount: Union[float, int, str, Decimal],
    *,
    currency: str = '元',
    sub_currency_1: str = '角',
    sub_currency_2: str = '分',
    suffix: str = '整',
    prefix_negative: str = '负',
    simplified: bool = False
) -> str:
    """
    将数字金额转换为中文大写金额。
    
    Args:
        amount: 金额数值，支持 float, int, str, Decimal 类型
        currency: 主货币单位，默认 '元'
        sub_currency_1: 第一级辅币单位，默认 '角'
        sub_currency_2: 第二级辅币单位，默认 '分'
        suffix: 整数金额后缀，默认 '整'
        prefix_negative: 负数前缀，默认 '负'
        simplified: 是否使用简化格式（不添加货币单位），默认 False
        
    Returns:
        中文大写金额字符串
        
    Raises:
        ChineseAmountError: 金额无效
        
    Examples:
        >>> to_chinese_amount(1234.56)
        '壹仟贰佰叁拾肆元伍角陆分'
        >>> to_chinese_amount(100)
        '壹佰元整'
        >>> to_chinese_amount(0.5)
        '伍角'
        >>> to_chinese_amount(-100.01)
        '负壹佰元零壹分'
    """
    # 验证金额
    dec_amount = _validate_amount(amount)
    
    # 处理零金额
    if dec_amount == 0:
        if simplified:
            return '零'
        return '零' + currency + suffix
    
    # 拆分整数和小数部分
    integer_part, jiao, fen = _split_amount(dec_amount)
    
    # 构建结果
    parts = []
    
    # 处理负数
    is_negative = dec_amount < 0
    if is_negative:
        parts.append(prefix_negative)
    
    # 处理整数部分
    if integer_part > 0:
        integer_str = _convert_integer_to_chinese(integer_part)
        if simplified:
            parts.append(integer_str)
        else:
            parts.append(integer_str + currency)
    elif jiao > 0 or fen > 0:
        # 有小数但无整数，需要补零
        if not simplified:
            parts.append('零' + currency)
    else:
        # 整数为零，无小数
        if simplified:
            parts.append('零')
        else:
            parts.append('零' + currency + suffix)
        return ''.join(parts)
    
    # 处理角
    if jiao > 0:
        parts.append(_DIGITS_CN[str(jiao)] + sub_currency_1)
    elif fen > 0 and integer_part > 0:
        # 有分无角，需要补零
        parts.append('零')
    
    # 处理分
    if fen > 0:
        parts.append(_DIGITS_CN[str(fen)] + sub_currency_2)
    
    # 整数金额添加"整"字
    if jiao == 0 and fen == 0 and integer_part > 0:
        if not simplified:
            parts.append(suffix)
    
    return ''.join(parts)


def to_chinese_amount_simple(amount: Union[float, int, str, Decimal]) -> str:
    """
    将数字转换为简化的中文大写（不含货币单位）。
    
    Args:
        amount: 金额数值
        
    Returns:
        简化的中文大写字符串
        
    Examples:
        >>> to_chinese_amount_simple(1234)
        '壹仟贰佰叁拾肆'
        >>> to_chinese_amount_simple(100000000)
        '壹亿'
    """
    dec_amount = _validate_amount(amount)
    integer_part = int(abs(dec_amount))
    
    if integer_part == 0:
        return '零'
    
    result = []
    
    if dec_amount < 0:
        result.append('负')
    
    result.append(_convert_integer_to_chinese(integer_part))
    
    return ''.join(result)


def to_chinese_number(num: Union[int, str]) -> str:
    """
    将整数转换为中文数字（普通写法）。
    
    Args:
        num: 整数
        
    Returns:
        中文数字字符串
        
    Examples:
        >>> to_chinese_number(123)
        '一百二十三'
        >>> to_chinese_number(10001)
        '一万零一'
    """
    try:
        if isinstance(num, str):
            num = int(num.replace(',', '').strip())
        else:
            num = int(num)
    except (ValueError, TypeError):
        raise ChineseAmountError(f"无效的数字: {num}")
    
    if num == 0:
        return '零'
    
    is_negative = num < 0
    num = abs(num)
    
    # 分组处理
    groups = []
    while num > 0:
        groups.append(num % 10000)
        num //= 10000
    
    result = []
    
    for i, group in enumerate(groups):
        if group == 0:
            # 需要补零（除非后面没有更高位）
            if i > 0 and i < len(groups) - 1:
                result.insert(0, '零')
            continue
        
        group_str = ''
        
        # 千位
        if group >= 1000:
            digit = group // 1000
            group_str += _SIMPLE_DIGITS_CN[str(digit)] + '千'
            group %= 1000
        
        # 百位
        if group >= 100:
            digit = group // 100
            group_str += _SIMPLE_DIGITS_CN[str(digit)] + '百'
            group %= 100
        elif group_str and group > 0:
            group_str += '零'
        
        # 十位
        if group >= 10:
            digit = group // 10
            if digit == 1 and i == len(groups) - 1 and not group_str:
                # 最高位组的十位为1时，只写"十"
                group_str += '十'
            else:
                group_str += _SIMPLE_DIGITS_CN[str(digit)] + '十'
            group %= 10
        elif group_str and group > 0:
            group_str += '零'
        
        # 个位
        if group > 0:
            group_str += _SIMPLE_DIGITS_CN[str(group)]
        
        # 添加大单位
        if i > 0:
            unit = _LARGE_UNITS_CN[i]
            group_str = group_str + unit
        
        result.insert(0, group_str)
    
    # 处理连续的零
    while '零零' in ''.join(result):
        result_str = ''.join(result)
        result_str = result_str.replace('零零', '零')
        result = [result_str]
    
    final = ''.join(result)
    
    # 移除结尾的零
    if final.endswith('零'):
        final = final[:-1]
    
    if is_negative:
        final = '负' + final
    
    return final


def parse_chinese_amount(chinese_str: str) -> Decimal:
    """
    将中文大写金额转换为数字金额。
    
    Args:
        chinese_str: 中文大写金额字符串
        
    Returns:
        Decimal 类型的金额
        
    Raises:
        ChineseAmountError: 无法解析
        
    Examples:
        >>> parse_chinese_amount('壹仟贰佰叁拾肆元伍角陆分')
        Decimal('1234.56')
        >>> parse_chinese_amount('壹佰元整')
        Decimal('100')
    """
    if not chinese_str or not chinese_str.strip():
        raise ChineseAmountError("输入不能为空")
    
    chinese_str = chinese_str.strip()
    
    # 移除"整"、"正"等后缀
    chinese_str = chinese_str.rstrip('整正')
    
    # 处理负数
    is_negative = False
    if chinese_str.startswith('负'):
        is_negative = True
        chinese_str = chinese_str[1:]
    
    # 中文数字到阿拉伯数字的映射
    cn_to_digit = {
        '零': 0, '〇': 0,
        '壹': 1, '一': 1,
        '贰': 2, '二': 2, '两': 2,
        '叁': 3, '三': 3,
        '肆': 4, '四': 4,
        '伍': 5, '五': 5,
        '陆': 6, '六': 6,
        '柒': 7, '七': 7,
        '捌': 8, '八': 8,
        '玖': 9, '九': 9,
    }
    
    # 中文单位到数值的映射
    cn_to_unit = {
        '拾': 10, '十': 10,
        '佰': 100, '百': 100,
        '仟': 1000, '千': 1000,
        '万': 10000,
        '亿': 100000000,
    }
    
    # 分离元、角、分
    yuan_part = ''
    jiao_part = 0
    fen_part = 0
    
    # 找到元的位置
    yuan_pos = -1
    for unit in ['元', '圆']:
        if unit in chinese_str:
            yuan_pos = chinese_str.index(unit)
            break
    
    if yuan_pos >= 0:
        yuan_part = chinese_str[:yuan_pos]
        remaining = chinese_str[yuan_pos + 1:]
    else:
        yuan_part = chinese_str
        remaining = ''
    
    # 解析角
    for unit in ['角', '毛']:
        if unit in remaining:
            jiao_pos = remaining.index(unit)
            # 角前面的数字
            jiao_str = remaining[:jiao_pos]
            if jiao_str and jiao_str[-1] in cn_to_digit:
                jiao_part = cn_to_digit[jiao_str[-1]]
            remaining = remaining[jiao_pos + 1:]
            break
    
    # 解析分
    if '分' in remaining:
        fen_pos = remaining.index('分')
        fen_str = remaining[:fen_pos]
        if fen_str and fen_str[-1] in cn_to_digit:
            fen_part = cn_to_digit[fen_str[-1]]
    
    # 解析元部分
    def parse_section(section: str) -> int:
        """解析中文数字段"""
        if not section or section == '零':
            return 0
        
        total = 0
        temp = 0
        i = 0
        
        while i < len(section):
            char = section[i]
            
            if char in cn_to_digit:
                digit = cn_to_digit[char]
                # 看下一个是否是单位
                if i + 1 < len(section) and section[i + 1] in cn_to_unit:
                    unit = cn_to_unit[section[i + 1]]
                    if unit >= 10000:
                        # 大单位：万、亿
                        temp = (temp + digit) * unit
                        total += temp
                        temp = 0
                    else:
                        temp += digit * unit
                    i += 2
                else:
                    temp += digit
                    i += 1
            elif char in cn_to_unit:
                # 单独的单位（如"拾万"中的拾）
                unit = cn_to_unit[char]
                if temp == 0:
                    temp = 1
                if unit >= 10000:
                    temp = temp * unit
                    total += temp
                    temp = 0
                else:
                    temp *= unit
                i += 1
            elif char == '零':
                i += 1
            else:
                i += 1
        
        return total + temp
    
    yuan_value = parse_section(yuan_part)
    
    # 组合结果
    result = Decimal(str(yuan_value)) + Decimal(str(jiao_part)) / 10 + Decimal(str(fen_part)) / 100
    
    if is_negative:
        result = -result
    
    return result


def format_amount_for_receipt(
    amount: Union[float, int, str, Decimal],
    *,
    include_prefix: bool = True
) -> str:
    """
    格式化金额用于收据/发票（标准财务格式）。
    
    Args:
        amount: 金额
        include_prefix: 是否包含"人民币"前缀
        
    Returns:
        标准格式的中文金额
        
    Examples:
        >>> format_amount_for_receipt(1234.56)
        '人民币壹仟贰佰叁拾肆元伍角陆分'
        >>> format_amount_for_receipt(100, include_prefix=False)
        '壹佰元整'
    """
    prefix = '人民币' if include_prefix else ''
    chinese = to_chinese_amount(amount)
    return prefix + chinese


def validate_chinese_amount(chinese_str: str) -> bool:
    """
    验证中文大写金额格式是否正确。
    
    Args:
        chinese_str: 中文大写金额字符串
        
    Returns:
        是否为有效格式
        
    Examples:
        >>> validate_chinese_amount('壹仟贰佰叁拾肆元伍角陆分')
        True
        >>> validate_chinese_amount('abc')
        False
    """
    if not chinese_str or not chinese_str.strip():
        return False
    
    chinese_str = chinese_str.strip()
    
    # 检查是否包含有效字符
    valid_chars = set('零壹贰叁肆伍陆柒捌玖拾佰仟万亿元角分整正负一二三四五六七八九十百千万亿两〇')
    
    # 检查每个字符
    for char in chinese_str:
        if char not in valid_chars:
            return False
    
    # 必须包含元、角、分或整等单位
    has_currency_unit = any(unit in chinese_str for unit in ['元', '圆', '角', '分', '整', '正'])
    
    # 如果没有货币单位，检查是否有数字字符
    has_digit = any(char in chinese_str for char in valid_chars if char not in '元圆角分整正负')
    
    if not has_digit:
        return False
    
    try:
        result = parse_chinese_amount(chinese_str)
        return True
    except ChineseAmountError:
        return False


def amount_in_words(
    amount: Union[float, int, str, Decimal],
    *,
    style: str = 'standard'
) -> str:
    """
    将金额转换为文字描述（多种风格）。
    
    Args:
        amount: 金额
        style: 风格，可选 'standard'（标准财务）, 'simple'（简体）
        
    Returns:
        金额文字描述
        
    Examples:
        >>> amount_in_words(1234.56, style='standard')
        '壹仟贰佰叁拾肆元伍角陆分'
        >>> amount_in_words(1234.56, style='simple')
        '一千二百三十四元五角六分'
    """
    if style == 'standard':
        return to_chinese_amount(amount)
    elif style == 'simple':
        # 简体风格
        result = to_chinese_amount(amount)
        # 替换大写数字为简体
        replacements = {
            '壹': '一', '贰': '二', '叁': '三', '肆': '四',
            '伍': '五', '陆': '六', '柒': '七', '捌': '八',
            '玖': '九', '拾': '十', '佰': '百', '仟': '千',
        }
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result
    else:
        return to_chinese_amount(amount)


# ============================================================================
# 便捷函数
# ============================================================================

def rmb(amount: Union[float, int, str, Decimal]) -> str:
    """
    快捷函数：转换为人民币大写金额。
    
    Args:
        amount: 金额
        
    Returns:
        人民币大写金额
        
    Examples:
        >>> rmb(1234.56)
        '壹仟贰佰叁拾肆元伍角陆分'
    """
    return to_chinese_amount(amount)


def cny(amount: Union[float, int, str, Decimal]) -> str:
    """
    快捷函数：转换为人民币大写金额（同 rmb）。
    
    Args:
        amount: 金额
        
    Returns:
        人民币大写金额
    """
    return to_chinese_amount(amount)


# ============================================================================
# 模块信息
# ============================================================================

VERSION = "1.0.0"
AUTHOR = "AllToolkit"
LICENSE = "MIT"