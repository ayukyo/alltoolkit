"""
Luhn Algorithm Utilities - 零依赖Luhn算法工具

功能:
- 验证数字字符串是否符合Luhn算法（信用卡、IMEI等）
- 生成校验位
- 格式化数字字符串
- 识别常见卡号类型

Luhn算法 (又称模10算法) 用于验证各种识别号码：
- 信用卡号
- IMEI号码
- 加拿大社会保险号
- 美国雇主识别号等
"""

from typing import Optional, Tuple, List


def luhn_checksum(number: str) -> int:
    """
    计算Luhn校验和
    
    Args:
        number: 数字字符串（不含校验位）
    
    Returns:
        校验和值 (0-9)
    """
    # 移除非数字字符
    digits = [int(d) for d in number if d.isdigit()]
    
    # 从右到左，每隔一位乘以2
    total = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 0:  # 奇数位（从0开始计数）
            total += digit
        else:  # 偶数位
            doubled = digit * 2
            total += doubled - 9 if doubled > 9 else doubled
    
    return total % 10


def calculate_check_digit(number: str) -> int:
    """
    计算Luhn校验位
    
    Args:
        number: 数字字符串（不含校验位）
    
    Returns:
        校验位 (0-9)
    """
    checksum = luhn_checksum(number + "0")
    return (10 - checksum) % 10


def validate(number: str) -> bool:
    """
    验证数字字符串是否符合Luhn算法
    
    Args:
        number: 包含校验位的完整数字字符串
    
    Returns:
        True 如果有效，False 如果无效
    """
    # 移除非数字字符
    digits = ''.join(d for d in number if d.isdigit())
    
    if len(digits) < 2:
        return False
    
    return luhn_checksum(digits) == 0


def generate_with_check_digit(number: str) -> str:
    """
    生成带校验位的完整号码
    
    Args:
        number: 不含校验位的数字字符串
    
    Returns:
        包含校验位的完整号码
    """
    check_digit = calculate_check_digit(number)
    return ''.join(d for d in number if d.isdigit()) + str(check_digit)


def format_card_number(number: str, separator: str = " ") -> str:
    """
    格式化卡号为4位一组
    
    Args:
        number: 数字字符串
        separator: 分隔符，默认为空格
    
    Returns:
        格式化后的字符串
    """
    digits = ''.join(d for d in number if d.isdigit())
    return separator.join(digits[i:i+4] for i in range(0, len(digits), 4))


def mask_card_number(number: str, show_first: int = 4, show_last: int = 4, mask_char: str = "*") -> str:
    """
    遮蔽卡号中间部分
    
    Args:
        number: 数字字符串
        show_first: 显示前几位，默认4
        show_last: 显示后几位，默认4
        mask_char: 遮蔽字符，默认*
    
    Returns:
        遮蔽后的字符串
    """
    digits = ''.join(d for d in number if d.isdigit())
    
    if len(digits) <= show_first + show_last:
        return digits
    
    masked_length = len(digits) - show_first - show_last
    return digits[:show_first] + mask_char * masked_length + digits[-show_last:]


# 卡号类型识别模式
CARD_PATTERNS = {
    "Visa": [
        (r"^4", "13,16"),  # 以4开头，13或16位
    ],
    "MasterCard": [
        (r"^5[1-5]", "16"),  # 以51-55开头，16位
        (r"^2[2-7]", "16"),  # 以2221-2720开头，16位
    ],
    "American Express": [
        (r"^3[47]", "15"),  # 以34或37开头，15位
    ],
    "Discover": [
        (r"^6011", "16"),
        (r"^65", "16"),
        (r"^64[4-9]", "16"),
    ],
    "JCB": [
        (r"^35", "16"),
    ],
    "Diners Club": [
        (r"^3(?:0[0-5]|[68])", "14"),
    ],
    "UnionPay": [
        (r"^62", "16-19"),
    ],
    "Maestro": [
        (r"^(5018|5020|5038|6304|6759|6761|6762|6763)", "12-19"),
    ],
}


def identify_card_type(number: str) -> Optional[str]:
    """
    识别信用卡类型
    
    Args:
        number: 卡号字符串
    
    Returns:
        卡类型名称，如果无法识别返回 None
    """
    import re
    
    digits = ''.join(d for d in number if d.isdigit())
    
    for card_type, patterns in CARD_PATTERNS.items():
        for pattern, lengths in patterns:
            # 使用正则匹配前缀
            if re.match(pattern, digits):
                # 检查长度
                valid_lengths = []
                for l in lengths.split(","):
                    if "-" in l:
                        start, end = map(int, l.split("-"))
                        valid_lengths.extend(range(start, end + 1))
                    else:
                        valid_lengths.append(int(l))
                
                if len(digits) in valid_lengths:
                    return card_type
    
    return None


def validate_card(number: str) -> Tuple[bool, Optional[str], str]:
    """
    验证信用卡号（包括Luhn校验和类型识别）
    
    Args:
        number: 卡号字符串
    
    Returns:
        (是否有效, 卡类型, 格式化后的卡号)
    """
    digits = ''.join(d for d in number if d.isdigit())
    
    is_valid = validate(digits)
    card_type = identify_card_type(digits) if is_valid else None
    formatted = format_card_number(digits)
    
    return is_valid, card_type, formatted


def generate_test_card(card_type: str = "Visa") -> str:
    """
    生成测试用信用卡号（仅供测试，非真实有效卡号）
    
    Args:
        card_type: 卡类型 ("Visa", "MasterCard", "American Express", "Discover")
    
    Returns:
        测试卡号
    """
    # 测试用前缀（符合各卡组织规范）
    # 16位卡号需要15位前缀，15位卡号需要14位前缀
    test_prefixes = {
        "Visa": "411111111111111",  # 15位，以4开头
        "MasterCard": "555555555555555",  # 15位，以55开头
        "American Express": "3782822463100",  # 14位，以37开头
        "Discover": "601111111111111",  # 15位，以6011开头
        "JCB": "353011133330000",  # 15位，以35开头
    }
    
    prefix = test_prefixes.get(card_type, "411111111111111")
    
    # 前缀长度已经正确，直接生成
    return generate_with_check_digit(prefix)


# IMEI 相关工具

def validate_imei(imei: str) -> bool:
    """
    验证IMEI号码
    
    Args:
        imei: IMEI号码字符串
    
    Returns:
        True 如果有效
    """
    digits = ''.join(d for d in imei if d.isdigit())
    
    if len(digits) != 15:
        return False
    
    return validate(digits)


def generate_imei(tac: str = "01234567", serial: str = "123456") -> str:
    """
    生成IMEI号码（仅供测试）
    
    Args:
        tac: Type Allocation Code (8位，新版IMEI标准)
        serial: 序列号 (6位)
    
    Returns:
        15位IMEI号码（TAC 8位 + SNR 6位 + 校验位 1位）
    """
    tac = ''.join(d for d in tac if d.isdigit())[:8].ljust(8, '0')
    serial = ''.join(d for d in serial if d.isdigit())[:6].ljust(6, '0')
    
    # IMEI = TAC(8) + SNR(6) + 校验位(1) = 15位
    base = tac + serial
    check_digit = calculate_check_digit(base)
    return base + str(check_digit)


def extract_luhn_info(number: str) -> dict:
    """
    提取Luhn相关信息
    
    Args:
        number: 数字字符串
    
    Returns:
        包含校验信息的字典
    """
    digits = ''.join(d for d in number if d.isdigit())
    
    if not digits:
        return {
            "valid": False,
            "error": "无有效数字"
        }
    
    check_digit = int(digits[-1]) if digits else None
    calculated_check = calculate_check_digit(digits[:-1]) if len(digits) > 1 else None
    
    return {
        "number": digits,
        "length": len(digits),
        "valid": validate(digits),
        "check_digit": check_digit,
        "calculated_check_digit": calculated_check,
        "check_digit_correct": check_digit == calculated_check if check_digit and calculated_check else False,
        "formatted": format_card_number(digits),
        "masked": mask_card_number(digits),
        "card_type": identify_card_type(digits) if validate(digits) else None,
    }


if __name__ == "__main__":
    # 简单演示
    print("=== Luhn算法工具演示 ===\n")
    
    # 测试卡号验证
    test_cards = [
        "4532015112830366",  # Visa
        "5555555555554444",  # MasterCard
        "378282246310005",   # American Express
        "6011111111111117",  # Discover
        "1234567890123456",  # 无效
    ]
    
    print("信用卡验证测试:")
    for card in test_cards:
        is_valid, card_type, formatted = validate_card(card)
        status = "✓ 有效" if is_valid else "✗ 无效"
        type_str = f" ({card_type})" if card_type else ""
        print(f"  {formatted}: {status}{type_str}")
    
    print("\n生成测试卡号:")
    for card_type in ["Visa", "MasterCard", "American Express", "Discover"]:
        test_num = generate_test_card(card_type)
        is_valid = validate(test_num)
        print(f"  {card_type}: {test_num} ({'有效' if is_valid else '无效'})")
    
    print("\nIMEI验证:")
    test_imei = "490154203237518"
    print(f"  {test_imei}: {'有效' if validate_imei(test_imei) else '无效'}")
    print(f"  生成测试IMEI: {generate_imei()}")
    
    print("\n卡号遮蔽:")
    print(f"  原始: 4532015112830366")
    print(f"  遮蔽: {mask_card_number('4532015112830366')}")
    
    print("\n详细信息提取:")
    info = extract_luhn_info("4532015112830366")
    for key, value in info.items():
        print(f"  {key}: {value}")