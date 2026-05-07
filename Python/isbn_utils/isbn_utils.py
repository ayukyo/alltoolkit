"""
ISBN Utils - 国际标准书号(ISBN)验证与处理工具库

ISBN (International Standard Book Number) 是国际标准书号，
用于唯一标识图书。支持 ISBN-10 (2007年前) 和 ISBN-13 (2007年后)。

ISBN-10 格式: X-XXXXX-XXX-X (分组-出版商-标题-检验位)
ISBN-13 格式: XXX-X-XXXX-XXXX-X (前缀-分组-出版商-标题-检验位)

参考: https://www.isbn-international.org/
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Tuple, Set


class ISBNType(Enum):
    """ISBN类型枚举"""
    ISBN10 = "ISBN-10"
    ISBN13 = "ISBN-13"
    UNKNOWN = "Unknown"


@dataclass
class ISBNInfo:
    """ISBN详细信息"""
    isbn: str
    isbn_type: ISBNType
    is_valid: bool
    normalized: str
    formatted: str
    prefix: Optional[str] = None
    group: Optional[str] = None
    publisher: Optional[str] = None
    title: Optional[str] = None
    check_digit: Optional[str] = None
    isbn13: Optional[str] = None  # ISBN-13格式
    isbn10: Optional[str] = None   # ISBN-10格式(如果可转换)


class ISBN:
    """
    ISBN 国际标准书号处理类
    
    支持ISBN-10和ISBN-13的验证、转换、格式化和解析。
    
    示例:
        >>> isbn = ISBN("978-7-111-54739-3")
        >>> isbn.is_valid()
        True
        >>> isbn.to_isbn13()
        '9787111547393'
        >>> isbn.format()
        '978-7-111-54739-3'
    """
    
    # ISBN-13前缀范围 (ISBN-13专用)
    ISBN13_PREFIXES = {'978', '979'}
    
    # 常见分组代码 (非完整列表)
    GROUP_RANGES = {
        '0': ('英语国家', '0-5', '0-5'),  # 英语国家
        '1': ('英语国家', '0-5', '0-5'),
        '2': ('法语国家', '0-5', '0-5'),
        '3': ('德语国家', '0-5', '0-5'),
        '4': ('日本', '0-5', '0-5'),
        '5': ('俄语国家', '0-5', '0-5'),
        '7': ('中国', '0-5', '0-5'),
        '80': ('捷克/斯洛伐克', '0-5', '0-5'),
        '81': ('印度', '0-5', '0-5'),
        '82': ('挪威', '0-5', '0-5'),
        '83': ('波兰', '0-5', '0-5'),
        '84': ('西班牙', '0-5', '0-5'),
        '85': ('巴西', '0-5', '0-5'),
        '86': ('塞尔维亚', '0-5', '0-5'),
        '87': ('丹麦', '0-5', '0-5'),
        '88': ('意大利', '0-5', '0-5'),
        '89': ('韩国', '0-5', '0-5'),
        '90': ('荷兰', '0-5', '0-5'),
        '91': ('瑞典', '0-5', '0-5'),
        '92': ('国际组织', '0-5', '0-5'),
        '93': ('印度', '0-5', '0-5'),
        '94': ('荷兰', '0-5', '0-5'),
        '952': ('芬兰', '0-5', '0-5'),
        '953': ('克罗地亚', '0-5', '0-5'),
        '954': ('保加利亚', '0-5', '0-5'),
        '955': ('斯里兰卡', '0-5', '0-5'),
        '956': ('智利', '0-5', '0-5'),
        '957': ('中国台湾', '0-5', '0-5'),
        '958': ('哥伦比亚', '0-5', '0-5'),
        '959': ('泰国', '0-5', '0-5'),
        '960': ('希腊', '0-5', '0-5'),
        '961': ('斯洛文尼亚', '0-5', '0-5'),
        '962': ('中国香港', '0-5', '0-5'),
        '963': ('匈牙利', '0-5', '0-5'),
        '964': ('伊朗', '0-5', '0-5'),
        '965': ('以色列', '0-5', '0-5'),
        '966': ('乌克兰', '0-5', '0-5'),
        '967': ('马来西亚', '0-5', '0-5'),
        '968': ('墨西哥', '0-5', '0-5'),
        '969': ('巴基斯坦', '0-5', '0-5'),
        '970': ('墨西哥', '0-5', '0-5'),
        '971': ('菲律宾', '0-5', '0-5'),
        '972': ('葡萄牙', '0-5', '0-5'),
        '973': ('罗马尼亚', '0-5', '0-5'),
        '974': ('泰国', '0-5', '0-5'),
        '975': ('土耳其', '0-5', '0-5'),
        '976': ('加勒比海地区', '0-5', '0-5'),
        '977': ('埃及', '0-5', '0-5'),
        '978': ('ISBN-13前缀', '0-5', '0-5'),  # 这里的978是EAN前缀
        '979': ('ISBN-13前缀', '0-5', '0-5'),  # 这里的979是EAN前缀
    }
    
    # 中国出版商代码范围 (部分)
    CHINA_PUBLISHER_RANGES = {
        '0': ('人民邮电出版社', '7-111'),
        '1': ('机械工业出版社', '7-111'),
        '111': ('机械工业出版社', '7-111'),
        '302': ('清华大学出版社', '7-302'),
        '301': ('北京大学出版社', '7-301'),
        '5086': ('中国电力出版社', '7-5086'),
        '115': ('人民交通出版社', '7-115'),
        '121': ('电子工业出版社', '7-121'),
        '5063': ('作家出版社', '7-5063'),
        '02': ('人民教育出版社', '7-02'),
        '03': ('科学出版社', '7-03'),
        '04': ('高等教育出版社', '7-04'),
        '100': ('商务印书馆', '7-100'),
        '101': ('中华书局', '7-101'),
        '102': ('中国大百科全书出版社', '7-102'),
        '103': ('中国书籍出版社', '7-103'),
        '104': ('人民出版社', '7-104'),
        '105': ('中国人民大学出版社', '7-105'),
        '106': ('法律出版社', '7-106'),
        '107': ('中国社会科学出版社', '7-107'),
        '108': ('中国财政经济出版社', '7-108'),
        '109': ('中国计划出版社', '7-109'),
        '110': ('中国建筑工业出版社', '7-110'),
    }
    
    def __init__(self, isbn: str):
        """
        初始化ISBN对象
        
        Args:
            isbn: ISBN字符串(可含分隔符)
        """
        self._raw = isbn
        self._normalized: Optional[str] = None
        self._isbn_type: Optional[ISBNType] = None
        self._is_valid: Optional[bool] = None
        self._parsed_parts: Optional[Tuple] = None
        self._analyze()
    
    def _analyze(self) -> None:
        """分析ISBN并确定类型"""
        # 标准化：移除所有分隔符
        cleaned = re.sub(r'[-\s]', '', self._raw.upper())
        
        # 判断类型
        if len(cleaned) == 10:
            # ISBN-10
            if re.match(r'^\d{9}[\dX]$', cleaned):
                self._normalized = cleaned
                self._isbn_type = ISBNType.ISBN10
                self._is_valid = self._validate_isbn10(cleaned)
            else:
                self._normalized = cleaned
                self._isbn_type = ISBNType.ISBN10
                self._is_valid = False
        
        elif len(cleaned) == 13:
            # ISBN-13
            if re.match(r'^\d{13}$', cleaned):
                self._normalized = cleaned
                self._isbn_type = ISBNType.ISBN13
                self._is_valid = self._validate_isbn13(cleaned)
            else:
                self._normalized = cleaned
                self._isbn_type = ISBNType.ISBN13
                self._is_valid = False
        
        else:
            self._normalized = cleaned
            self._isbn_type = ISBNType.UNKNOWN
            self._is_valid = False
    
    @staticmethod
    def _validate_isbn10(isbn: str) -> bool:
        """
        验证ISBN-10
        
        ISBN-10使用模11算法:
        d₁×10 + d₂×9 + d₃×8 + d₄×7 + d₅×6 + d₆×5 + d₇×4 + d₈×3 + d₉×2 + d₁₀×1 ≡ 0 (mod 11)
        """
        if not re.match(r'^\d{9}[\dX]$', isbn):
            return False
        
        total = 0
        for i, char in enumerate(isbn):
            if char == 'X':
                value = 10
            else:
                value = int(char)
            total += value * (10 - i)
        
        return total % 11 == 0
    
    @staticmethod
    def _validate_isbn13(isbn: str) -> bool:
        """
        验证ISBN-13
        
        ISBN-13使用EAN-13算法(模10):
        奇数位×1 + 偶数位×3 的和应能被10整除
        """
        if not re.match(r'^\d{13}$', isbn):
            return False
        
        total = 0
        for i, char in enumerate(isbn):
            digit = int(char)
            if i % 2 == 0:  # 奇数位(从0开始)
                total += digit * 1
            else:  # 偶数位
                total += digit * 3
        
        return total % 10 == 0
    
    def is_valid(self) -> bool:
        """验证ISBN是否有效"""
        return self._is_valid if self._is_valid is not None else False
    
    def get_type(self) -> ISBNType:
        """获取ISBN类型"""
        return self._isbn_type if self._isbn_type is not None else ISBNType.UNKNOWN
    
    def normalize(self) -> str:
        """返回标准化的ISBN(无分隔符)"""
        return self._normalized if self._normalized else ''
    
    def format(self, separator: str = '-') -> str:
        """
        格式化ISBN显示
        
        Args:
            separator: 分隔符(默认为'-')
        
        Returns:
            格式化后的ISBN字符串
        """
        if not self._normalized:
            return self._raw
        
        isbn = self._normalized
        
        if self._isbn_type == ISBNType.ISBN10 and len(isbn) == 10:
            # ISBN-10: X-XXXX-XXX-X (分组-出版商-标题-检验位)
            return f"{isbn[0]}{separator}{isbn[1:5]}{separator}{isbn[5:9]}{separator}{isbn[9]}"
        
        elif self._isbn_type == ISBNType.ISBN13 and len(isbn) == 13:
            # ISBN-13: XXX-X-XXXX-XXXX-X (前缀-分组-出版商-标题-检验位)
            return f"{isbn[0:3]}{separator}{isbn[3]}{separator}{isbn[4:8]}{separator}{isbn[8:12]}{separator}{isbn[12]}"
        
        return isbn
    
    def to_isbn13(self) -> Optional[str]:
        """
        转换为ISBN-13
        
        Returns:
            ISBN-13字符串，如果转换失败返回None
        """
        if self._isbn_type == ISBNType.ISBN13 and self._is_valid:
            return self._normalized
        
        if self._isbn_type == ISBNType.ISBN10 and self._is_valid:
            # ISBN-10转ISBN-13: 添加978前缀，重新计算检验位
            base = '978' + self._normalized[:9]
            check = calculate_isbn13_check_digit(base)
            return base + check
        
        return None
    
    def to_isbn10(self) -> Optional[str]:
        """
        转换为ISBN-10
        
        Returns:
            ISBN-10字符串，如果无法转换返回None
        
        Note:
            只有978前缀的ISBN-13才能转换为ISBN-10
        """
        if self._isbn_type == ISBNType.ISBN10 and self._is_valid:
            return self._normalized
        
        if self._isbn_type == ISBNType.ISBN13 and self._is_valid:
            # 只有978前缀可以转换
            if self._normalized.startswith('978'):
                base = self._normalized[3:12]
                check = calculate_isbn10_check_digit(base)
                return base + check
        
        return None
    
    def get_info(self) -> ISBNInfo:
        """获取ISBN详细信息"""
        return get_isbn_info(self._normalized if self._normalized else self._raw)
    
    def __str__(self) -> str:
        return self.format()
    
    def __repr__(self) -> str:
        return f"ISBN('{self._raw}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, ISBN):
            return self.normalize() == other.normalize()
        elif isinstance(other, str):
            return self.normalize() == normalize_isbn(other)
        return False
    
    def __hash__(self) -> int:
        return hash(self.normalize())


# ==================== 模块级便捷函数 ====================

def is_valid_isbn10(isbn: str) -> bool:
    """
    验证ISBN-10是否有效
    
    Args:
        isbn: ISBN-10字符串(可含分隔符)
    
    Returns:
        是否有效
    
    示例:
        >>> is_valid_isbn10('0-306-40615-2')
        True
        >>> is_valid_isbn10('0306406152')
        True
        >>> is_valid_isbn10('0-306-40615-X')
        False
    """
    cleaned = re.sub(r'[-\s]', '', isbn.upper())
    if len(cleaned) != 10:
        return False
    return ISBN._validate_isbn10(cleaned)


def is_valid_isbn13(isbn: str) -> bool:
    """
    验证ISBN-13是否有效
    
    Args:
        isbn: ISBN-13字符串(可含分隔符)
    
    Returns:
        是否有效
    
    示例:
        >>> is_valid_isbn13('978-7-111-54739-3')
        True
        >>> is_valid_isbn13('9787111547393')
        True
        >>> is_valid_isbn13('978-7-111-54739-0')
        False
    """
    cleaned = re.sub(r'[-\s]', '', isbn.upper())
    if len(cleaned) != 13:
        return False
    return ISBN._validate_isbn13(cleaned)


def is_valid_isbn(isbn: str) -> bool:
    """
    验证ISBN是否有效(自动检测类型)
    
    Args:
        isbn: ISBN字符串(可含分隔符)
    
    Returns:
        是否有效
    
    示例:
        >>> is_valid_isbn('978-7-111-54739-3')
        True
        >>> is_valid_isbn('0-306-40615-2')
        True
    """
    cleaned = re.sub(r'[-\s]', '', isbn.upper())
    if len(cleaned) == 10:
        return ISBN._validate_isbn10(cleaned)
    elif len(cleaned) == 13:
        return ISBN._validate_isbn13(cleaned)
    return False


def calculate_isbn10_check_digit(digits: str) -> str:
    """
    计算ISBN-10检验位
    
    Args:
        digits: 前9位数字
    
    Returns:
        检验位(0-9或X)
    
    示例:
        >>> calculate_isbn10_check_digit('030640615')
        '2'
        >>> calculate_isbn10_check_digit('047195869')
        'X'
    """
    if not digits or len(digits) != 9 or not digits.isdigit():
        raise ValueError("需要9位数字")
    
    total = sum(int(d) * (10 - i) for i, d in enumerate(digits))
    remainder = total % 11
    check = (11 - remainder) % 11
    
    return 'X' if check == 10 else str(check)


def calculate_isbn13_check_digit(digits: str) -> str:
    """
    计算ISBN-13检验位
    
    Args:
        digits: 前12位数字
    
    Returns:
        检验位(0-9)
    
    示例:
        >>> calculate_isbn13_check_digit('978030640615')
        '7'
    """
    if not digits or len(digits) != 12 or not digits.isdigit():
        raise ValueError("需要12位数字")
    
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
    check = (10 - (total % 10)) % 10
    return str(check)


def isbn10_to_isbn13(isbn10: str) -> str:
    """
    将ISBN-10转换为ISBN-13
    
    Args:
        isbn10: 有效的ISBN-10字符串
    
    Returns:
        ISBN-13字符串
    
    Raises:
        ValueError: 如果ISBN-10无效
    
    示例:
        >>> isbn10_to_isbn13('0-306-40615-2')
        '9780306406157'
    """
    cleaned = re.sub(r'[-\s]', '', isbn10.upper())
    
    if not is_valid_isbn10(cleaned):
        raise ValueError(f"无效的ISBN-10: {isbn10}")
    
    base = '978' + cleaned[:9]
    check = calculate_isbn13_check_digit(base)
    return base + check


def isbn13_to_isbn10(isbn13: str) -> Optional[str]:
    """
    将ISBN-13转换为ISBN-10
    
    Args:
        isbn13: 有效的ISBN-13字符串
    
    Returns:
        ISBN-10字符串，如果无法转换返回None
    
    Note:
        只有978前缀的ISBN-13才能转换
    
    示例:
        >>> isbn13_to_isbn10('978-0-306-40615-7')
        '0306406152'
        >>> isbn13_to_isbn10('979-1-234-56789-0')
        None
    """
    cleaned = re.sub(r'[-\s]', '', isbn13.upper())
    
    if not is_valid_isbn13(cleaned):
        return None
    
    # 只有978前缀可以转换
    if not cleaned.startswith('978'):
        return None
    
    base = cleaned[3:12]
    check = calculate_isbn10_check_digit(base)
    return base + check


def format_isbn(isbn: str, separator: str = '-') -> str:
    """
    格式化ISBN字符串
    
    Args:
        isbn: ISBN字符串
        separator: 分隔符(默认为'-')
    
    Returns:
        格式化后的ISBN，如果无效返回原字符串
    
    示例:
        >>> format_isbn('9787111547393')
        '978-7-111-54739-3'
        >>> format_isbn('0306406152')
        '0-3064-0615-2'
    """
    isbn_obj = ISBN(isbn)
    return isbn_obj.format(separator)


def normalize_isbn(isbn: str) -> str:
    """
    标准化ISBN(移除所有分隔符)
    
    Args:
        isbn: ISBN字符串
    
    Returns:
        标准化后的ISBN
    
    示例:
        >>> normalize_isbn('978-7-111-54739-3')
        '9787111547393'
        >>> normalize_isbn('0 306 40615 2')
        '0306406152'
    """
    return re.sub(r'[-\s]', '', isbn.upper())


def parse_isbn(isbn: str) -> ISBNInfo:
    """
    解析ISBN并返回详细信息
    
    Args:
        isbn: ISBN字符串
    
    Returns:
        ISBNInfo对象
    
    示例:
        >>> info = parse_isbn('978-7-111-54739-3')
        >>> info.is_valid
        True
        >>> info.isbn_type
        <ISBNType.ISBN13: 'ISBN-13'>
    """
    return get_isbn_info(isbn)


def get_isbn_info(isbn: str) -> ISBNInfo:
    """
    获取ISBN详细信息
    
    Args:
        isbn: ISBN字符串
    
    Returns:
        ISBNInfo对象，包含完整解析信息
    """
    isbn_obj = ISBN(isbn)
    normalized = isbn_obj.normalize()
    isbn_type = isbn_obj.get_type()
    is_valid = isbn_obj.is_valid()
    
    info = ISBNInfo(
        isbn=isbn,
        isbn_type=isbn_type,
        is_valid=is_valid,
        normalized=normalized,
        formatted=isbn_obj.format()
    )
    
    if not is_valid:
        return info
    
    # 解析各部分
    if isbn_type == ISBNType.ISBN10:
        info.check_digit = normalized[9]
        # ISBN-10: X-XXXX-XXX-X
        # 第一位可能是分组代码
        group_code = identify_prefix(normalized[:1])
        info.group = group_code
        info.isbn13 = isbn_obj.to_isbn13()
        info.isbn10 = normalized
        
    elif isbn_type == ISBNType.ISBN13:
        info.check_digit = normalized[12]
        info.prefix = normalized[:3]
        
        # ISBN-13: XXX-X-XXXX-XXXX-X
        # 第4位是分组代码
        group_code = identify_prefix(normalized[3])
        info.group = group_code
        info.isbn13 = normalized
        info.isbn10 = isbn_obj.to_isbn10()
    
    return info


def identify_prefix(code: str) -> Optional[str]:
    """
    识别分组前缀
    
    Args:
        code: 分组代码
    
    Returns:
        分组名称，如果无法识别返回None
    
    示例:
        >>> identify_prefix('7')
        '中国'
        >>> identify_prefix('0')
        '英语国家'
    """
    # 尝试精确匹配
    if code in ISBN.GROUP_RANGES:
        return ISBN.GROUP_RANGES[code][0]
    
    # 尝试前缀匹配(最长优先)
    for length in [3, 2, 1]:
        prefix = code[:length] if len(code) >= length else code
        if prefix in ISBN.GROUP_RANGES:
            return ISBN.GROUP_RANGES[prefix][0]
    
    return None


def extract_isbns(text: str) -> List[str]:
    """
    从文本中提取所有有效的ISBN
    
    Args:
        text: 待提取的文本
    
    Returns:
        有效ISBN列表
    
    示例:
        >>> text = "这本书的ISBN是978-7-111-54739-3，另一本是0-306-40615-2"
        >>> extract_isbns(text)
        ['9787111547393', '0306406152']
    """
    # 匹配ISBN-10和ISBN-13模式
    # ISBN-13: 13位数字，可能包含分隔符
    # ISBN-10: 9位数字+1位数字或X，可能包含分隔符
    
    results = []
    
    # ISBN-13模式: 允许分隔符的13位数字
    isbn13_pattern = r'97[89][-\s]?\d[-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?\d'
    
    # ISBN-10模式: 允许分隔符的10位(最后一位可能是X)
    isbn10_pattern = r'\d[-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?[\dXx]'
    
    # 查找所有匹配
    for match in re.finditer(isbn13_pattern, text):
        candidate = match.group()
        normalized = normalize_isbn(candidate)
        if is_valid_isbn13(normalized):
            results.append(normalized)
    
    for match in re.finditer(isbn10_pattern, text):
        candidate = match.group()
        normalized = normalize_isbn(candidate)
        # 避免重复(如果已经被识别为ISBN-13的一部分)
        if is_valid_isbn10(normalized) and normalized not in results:
            # 检查是否是ISBN-13的一部分(去掉978前缀后的部分)
            if len(normalized) == 10:
                isbn13_candidate = '978' + normalized[:9]
                check = calculate_isbn13_check_digit(isbn13_candidate)
                isbn13_candidate += check
                if isbn13_candidate in results:
                    continue
            results.append(normalized)
    
    return results


def batch_validate(isbns: List[str]) -> dict:
    """
    批量验证ISBN
    
    Args:
        isbns: ISBN字符串列表
    
    Returns:
        包含验证结果的字典:
        {
            'valid': [...],      # 有效ISBN列表
            'invalid': [...],    # 无效ISBN列表
            'isbn10': [...],     # ISBN-10列表
            'isbn13': [...],     # ISBN-13列表
            'stats': {...}       # 统计信息
        }
    
    示例:
        >>> result = batch_validate(['978-7-111-54739-3', '0-306-40615-2', 'invalid'])
        >>> result['valid']
        ['9787111547393', '0306406152']
    """
    valid = []
    invalid = []
    isbn10_list = []
    isbn13_list = []
    
    for isbn in isbns:
        normalized = normalize_isbn(isbn)
        
        if len(normalized) == 10 and is_valid_isbn10(normalized):
            valid.append(normalized)
            isbn10_list.append(normalized)
        elif len(normalized) == 13 and is_valid_isbn13(normalized):
            valid.append(normalized)
            isbn13_list.append(normalized)
        else:
            invalid.append(isbn)
    
    return {
        'valid': valid,
        'invalid': invalid,
        'isbn10': isbn10_list,
        'isbn13': isbn13_list,
        'stats': {
            'total': len(isbns),
            'valid_count': len(valid),
            'invalid_count': len(invalid),
            'isbn10_count': len(isbn10_list),
            'isbn13_count': len(isbn13_list)
        }
    }