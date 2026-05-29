"""
ISBN Utils - ISBN 编码验证与解析工具

功能：
- 验证 ISBN-10 和 ISBN-13 格式
- 计算校验位
- 提取 ISBN 组成部分（前缀、注册组、出版者、项目号）
- ISBN-10 与 ISBN-13 互转
- 格式化输出
- 批量验证

零外部依赖，纯 Python 实现
"""

import re
from typing import Optional, Dict, List, Tuple, Union
from dataclasses import dataclass


@dataclass
class ISBNInfo:
    """ISBN 解析结果"""
    isbn: str
    isbn10: Optional[str]
    isbn13: str
    is_valid: bool
    prefix: Optional[str] = None  # 仅 ISBN-13 有
    registration_group: Optional[str] = None
    registrant: Optional[str] = None
    publication: Optional[str] = None
    check_digit: str = ""


# ISBN 注册组前缀映射（简化版，包含主要国家/地区）
REGISTRATION_GROUPS = {
    # 英语区
    '0': 'English (English language)',
    '1': 'English (English language)',
    # 中文区
    '7': 'China',
    # 日语
    '4': 'Japan',
    # 韩语
    '89': 'Korea',
    '979-11': 'Korea',
    # 德语
    '3': 'German',
    # 法语
    '2': 'French',
    # 西班牙语
    '84': 'Spain',
    # 意大利语
    '88': 'Italy',
    # 葡萄牙语
    '972': 'Portugal',
    '989': 'Portugal',
    # 俄语
    '5': 'Russia',
    # 印度
    '81': 'India',
    '93': 'India',
    # 巴西
    '85': 'Brazil',
    # 其他
    '6': 'Thailand/Other',
    '957': 'Taiwan',
    '986': 'Taiwan',
    '962': 'Hong Kong',
    '988': 'Hong Kong',
    '967': 'Malaysia',
    '983': 'Malaysia',
    '979': 'Indonesia/Korea/Other',
    '9979': 'Iceland',
    '99914': 'Iceland',
}


def clean_isbn(isbn: str) -> str:
    """
    清理 ISBN 字符串，移除格式字符
    
    Args:
        isbn: 原始 ISBN 字符串
        
    Returns:
        清理后的纯数字字符串（ISBN-10 可能包含 X）
    """
    # 移除连字符、空格
    cleaned = re.sub(r'[-\s]', '', isbn.upper())
    return cleaned


def calculate_check_digit_isbn10(digits: str) -> str:
    """
    计算 ISBN-10 校验位
    
    ISBN-10 校验算法：
    d1*10 + d2*9 + d3*8 + ... + d9*2 = sum
    check = 11 - (sum % 11)
    如果 check = 10，用 'X' 表示
    如果 check = 11，用 '0' 表示
    
    Args:
        digits: ISBN-10 前9位数字
        
    Returns:
        校验位字符 ('0'-'9' 或 'X')
    """
    if len(digits) != 9 or not digits.isdigit():
        raise ValueError("ISBN-10 需要 9 位数字")
    
    total = sum(int(d) * (10 - i) for i, d in enumerate(digits))
    check = 11 - (total % 11)
    
    if check == 10:
        return 'X'
    elif check == 11:
        return '0'
    else:
        return str(check)


def calculate_check_digit_isbn13(digits: str) -> str:
    """
    计算 ISBN-13 校验位
    
    ISBN-13 使用 EAN-13 校验算法：
    奇数位 * 1 + 偶数位 * 3，求和后取模
    check = (10 - (sum % 10)) % 10
    
    Args:
        digits: ISBN-13 前12位数字
        
    Returns:
        校验位数字 ('0'-'9')
    """
    if len(digits) != 12 or not digits.isdigit():
        raise ValueError("ISBN-13 需要 12 位数字")
    
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
    check = (10 - (total % 10)) % 10
    return str(check)


def is_valid_isbn10(isbn: str) -> bool:
    """
    验证 ISBN-10 格式
    
    Args:
        isbn: ISBN-10 字符串
        
    Returns:
        是否为有效的 ISBN-10
    """
    cleaned = clean_isbn(isbn)
    
    if len(cleaned) != 10:
        return False
    
    # 前9位必须是数字
    if not cleaned[:9].isdigit():
        return False
    
    # 最后一位可以是数字或 X
    if cleaned[9] not in '0123456789X':
        return False
    
    # 验证校验位
    expected = calculate_check_digit_isbn10(cleaned[:9])
    return cleaned[9] == expected


def is_valid_isbn13(isbn: str) -> bool:
    """
    验证 ISBN-13 格式
    
    Args:
        isbn: ISBN-13 字符串
        
    Returns:
        是否为有效的 ISBN-13
    """
    cleaned = clean_isbn(isbn)
    
    if len(cleaned) != 13:
        return False
    
    if not cleaned.isdigit():
        return False
    
    # 验证前缀（978 或 979）
    if cleaned[:3] not in ('978', '979'):
        return False
    
    # 验证校验位
    expected = calculate_check_digit_isbn13(cleaned[:12])
    return cleaned[12] == expected


def is_valid_isbn(isbn: str) -> bool:
    """
    验证 ISBN（自动检测格式）
    
    Args:
        isbn: ISBN 字符串
        
    Returns:
        是否为有效的 ISBN
    """
    return is_valid_isbn10(isbn) or is_valid_isbn13(isbn)


def isbn10_to_isbn13(isbn10: str) -> str:
    """
    将 ISBN-10 转换为 ISBN-13
    
    Args:
        isbn10: 有效的 ISBN-10 字符串
        
    Returns:
        ISBN-13 字符串
        
    Raises:
        ValueError: 如果 ISBN-10 无效
    """
    cleaned = clean_isbn(isbn10)
    
    if not is_valid_isbn10(cleaned):
        raise ValueError(f"无效的 ISBN-10: {isbn10}")
    
    # 添加 978 前缀
    isbn13_base = '978' + cleaned[:9]
    check_digit = calculate_check_digit_isbn13(isbn13_base)
    
    return isbn13_base + check_digit


def isbn13_to_isbn10(isbn13: str) -> Optional[str]:
    """
    将 ISBN-13 转换为 ISBN-10
    
    注意：只有前缀为 978 的 ISBN-13 可以转换为 ISBN-10
    
    Args:
        isbn13: 有效的 ISBN-13 字符串
        
    Returns:
        ISBN-10 字符串，如果无法转换则返回 None
        
    Raises:
        ValueError: 如果 ISBN-13 无效
    """
    cleaned = clean_isbn(isbn13)
    
    if not is_valid_isbn13(cleaned):
        raise ValueError(f"无效的 ISBN-13: {isbn13}")
    
    # 只有 978 前缀可以转换为 ISBN-10
    if not cleaned.startswith('978'):
        return None
    
    # 移除前缀，取前9位
    isbn10_base = cleaned[3:12]
    check_digit = calculate_check_digit_isbn10(isbn10_base[:9])
    
    return isbn10_base[:9] + check_digit


def detect_isbn_type(isbn: str) -> Optional[str]:
    """
    检测 ISBN 类型
    
    Args:
        isbn: ISBN 字符串
        
    Returns:
        'ISBN-10', 'ISBN-13', 或 None（无效）
    """
    cleaned = clean_isbn(isbn)
    
    if is_valid_isbn10(cleaned):
        return 'ISBN-10'
    elif is_valid_isbn13(cleaned):
        return 'ISBN-13'
    else:
        return None


def format_isbn(isbn: str, separator: str = '-') -> str:
    """
    格式化 ISBN 显示
    
    Args:
        isbn: ISBN 字符串
        separator: 分隔符，默认为 '-'
        
    Returns:
        格式化后的 ISBN 字符串
        
    Examples:
        >>> format_isbn('9780306406157')
        '978-0-306-40615-7'
        >>> format_isbn('0306406152')
        '0-306-40615-2'
    """
    cleaned = clean_isbn(isbn)
    
    if len(cleaned) == 13:
        # ISBN-13: 978-GROUP-REGISTRANT-PUBLICATION-CHECK
        return separator.join([cleaned[:3], cleaned[3], cleaned[4:7], cleaned[7:12], cleaned[12]])
    elif len(cleaned) == 10:
        # ISBN-10: GROUP-REGISTRANT-PUBLICATION-CHECK
        return separator.join([cleaned[0], cleaned[1:4], cleaned[4:9], cleaned[9]])
    else:
        return isbn


def get_registration_group(isbn: str) -> Optional[str]:
    """
    获取 ISBN 注册组（国家/地区）
    
    Args:
        isbn: ISBN 字符串
        
    Returns:
        注册组名称或 None
    """
    cleaned = clean_isbn(isbn)
    
    # 对于 ISBN-13，需要查看第4位开始的组代码
    if len(cleaned) == 13:
        if not cleaned.startswith('978') and not cleaned.startswith('979'):
            return None
        # 检查第4位开始的组代码
        group_part = cleaned[3:]
    elif len(cleaned) == 10:
        group_part = cleaned
    else:
        return None
    
    # 按长度从长到短匹配（优先匹配更长的前缀）
    for prefix in sorted(REGISTRATION_GROUPS.keys(), key=len, reverse=True):
        if group_part.startswith(prefix):
            return REGISTRATION_GROUPS[prefix]
    
    return None


def parse_isbn(isbn: str) -> ISBNInfo:
    """
    解析 ISBN，返回详细信息
    
    Args:
        isbn: ISBN 字符串
        
    Returns:
        ISBNInfo 对象包含解析结果
    """
    cleaned = clean_isbn(isbn)
    isbn_type = detect_isbn_type(cleaned)
    is_valid = isbn_type is not None
    
    info = ISBNInfo(
        isbn=cleaned,
        isbn10=None,
        isbn13='',
        is_valid=is_valid,
        check_digit=cleaned[-1] if cleaned else ''
    )
    
    if not is_valid:
        return info
    
    # 获取标准形式
    if isbn_type == 'ISBN-10':
        info.isbn10 = cleaned
        info.isbn13 = isbn10_to_isbn13(cleaned)
        info.prefix = None  # ISBN-10 无前缀
    else:  # ISBN-13
        info.isbn13 = cleaned
        info.isbn10 = isbn13_to_isbn10(cleaned)
        info.prefix = cleaned[:3]
    
    # 解析注册组
    info.registration_group = get_registration_group(cleaned)
    
    # 解析出版者代码（简化处理）
    if isbn_type == 'ISBN-13':
        # ISBN-13: 978-GROUP-REGISTRANT-PUBLICATION-CHECK
        info.registrant = cleaned[4:7]
        info.publication = cleaned[7:12]
    else:  # ISBN-10
        # ISBN-10: GROUP-REGISTRANT-PUBLICATION-CHECK
        info.registrant = cleaned[1:4]
        info.publication = cleaned[4:9]
    
    return info


def batch_validate(isbns: List[str]) -> Dict[str, bool]:
    """
    批量验证 ISBN
    
    Args:
        isbns: ISBN 字符串列表
        
    Returns:
        字典，键为 ISBN，值为是否有效
    """
    return {isbn: is_valid_isbn(isbn) for isbn in isbns}


def generate_isbn13_from_isbn10(isbn10: str) -> str:
    """
    从 ISBN-10 生成 ISBN-13（别名函数）
    
    Args:
        isbn10: 有效的 ISBN-10 字符串
        
    Returns:
        ISBN-13 字符串
    """
    return isbn10_to_isbn13(isbn10)


def find_isbns_in_text(text: str) -> List[str]:
    """
    从文本中提取所有可能的 ISBN
    
    Args:
        text: 包含可能 ISBN 的文本
        
    Returns:
        找到的有效 ISBN 列表
    """
    # 匹配 ISBN-10 和 ISBN-13 模式（可能包含连字符或空格）
    # ISBN-13: 978/979 开头的 13 位数字
    # ISBN-10: 10 位（数字或末尾 X）
    
    patterns = [
        r'97[89][- ]?\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?[\dX]',  # ISBN-13
        r'\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?[\dXx]',  # ISBN-10
    ]
    
    found = set()
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            cleaned = clean_isbn(match)
            if is_valid_isbn(cleaned):
                found.add(cleaned)
    
    return list(found)


def compare_isbns(isbn1: str, isbn2: str) -> bool:
    """
    比较两个 ISBN 是否等价
    
    同一本书的 ISBN-10 和 ISBN-13 应该被视为等价
    
    Args:
        isbn1: 第一个 ISBN
        isbn2: 第二个 ISBN
        
    Returns:
        是否等价
    """
    cleaned1 = clean_isbn(isbn1)
    cleaned2 = clean_isbn(isbn2)
    
    # 如果都有效，转换为 ISBN-13 比较
    if is_valid_isbn(cleaned1) and is_valid_isbn(cleaned2):
        isbn13_1 = isbn10_to_isbn13(cleaned1) if len(cleaned1) == 10 else cleaned1
        isbn13_2 = isbn10_to_isbn13(cleaned2) if len(cleaned2) == 10 else cleaned2
        return isbn13_1 == isbn13_2
    
    return False


# 常用示例 ISBN（已验证校验位）
EXAMPLE_ISBNS = {
    '9780306406157': 'The Hitchhiker\'s Guide to the Galaxy',
    '0306406152': 'The Hitchhiker\'s Guide to the Galaxy (ISBN-10)',
    '9780262033848': 'Introduction to Algorithms',
    '0262033844': 'Introduction to Algorithms (ISBN-10)',
    '9787115538642': 'Python编程：从入门到实践',
    '7115538646': 'Python编程：从入门到实践 (ISBN-10)',
    '100308625X': '以 X 结尾的示例 ISBN-10',
}


if __name__ == '__main__':
    # 简单演示
    test_isbns = [
        '978-0-306-40615-7',
        '0-306-40615-2',
        '9787115538642',
        '7-115-53864-6',
    ]
    
    print("ISBN Utils 演示\n" + "=" * 50)
    
    for isbn in test_isbns:
        info = parse_isbn(isbn)
        print(f"\n原始: {isbn}")
        print(f"  类型: {detect_isbn_type(isbn)}")
        print(f"  有效: {info.is_valid}")
        print(f"  格式化: {format_isbn(isbn)}")
        print(f"  注册组: {info.registration_group}")
        if info.isbn10:
            print(f"  ISBN-10: {info.isbn10}")
        print(f"  ISBN-13: {info.isbn13}")