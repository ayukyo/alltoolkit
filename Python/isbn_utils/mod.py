"""
ISBN Utils - 国际标准书号工具模块

功能：
- ISBN-10 和 ISBN-13 验证
- ISBN 格式转换（10位转13位，13位转10位）
- 校验位计算
- 随机生成有效 ISBN（用于测试）
- ISBN 解析和格式化

零外部依赖，纯 Python 标准库实现。
"""

import re
import random
from typing import Optional, Tuple, Dict, Any


class ISBNError(Exception):
    """ISBN 相关错误基类"""
    pass


class InvalidISBNError(ISBNError):
    """无效的 ISBN"""
    pass


class ISBNConversionError(ISBNError):
    """ISBN 转换错误"""
    pass


class ISBNUtils:
    """ISBN 工具类"""
    
    # ISBN-13 前缀
    ISBN_13_PREFIX = "978"
    ISBN_13_PREFIX_ALT = "979"  # 新的前缀，用于 ISBN-10 用尽后
    
    @staticmethod
    def clean(isbn: str) -> str:
        """
        清理 ISBN 字符串，移除所有非数字字符（保留 X）
        
        Args:
            isbn: 原始 ISBN 字符串
            
        Returns:
            清理后的纯数字字符串（可能包含 X）
        """
        return re.sub(r'[^0-9Xx]', '', isbn).upper()
    
    @staticmethod
    def detect_version(isbn: str) -> Optional[int]:
        """
        检测 ISBN 版本
        
        Args:
            isbn: ISBN 字符串
            
        Returns:
            10 或 13，如果无法识别返回 None
        """
        cleaned = ISBNUtils.clean(isbn)
        if len(cleaned) == 10:
            return 10
        elif len(cleaned) == 13:
            return 13
        return None
    
    @staticmethod
    def calculate_check_digit_10(isbn9: str) -> str:
        """
        计算 ISBN-10 校验位
        
        ISBN-10 校验位计算：
        - 前9位数字分别乘以 10, 9, 8, ..., 2
        - 求和
        - 对 11 取模
        - 结果为 11 - (sum % 11)，如果为 10 则为 X
        
        Args:
            isbn9: ISBN-10 的前9位数字
            
        Returns:
            校验位（0-9 或 X）
        """
        if len(isbn9) != 9 or not isbn9.isdigit():
            raise InvalidISBNError("需要9位数字来计算 ISBN-10 校验位")
        
        total = sum(int(digit) * (10 - i) for i, digit in enumerate(isbn9))
        remainder = total % 11
        check = (11 - remainder) % 11
        
        return 'X' if check == 10 else str(check)
    
    @staticmethod
    def calculate_check_digit_12(isbn12: str) -> str:
        """
        计算 ISBN-13 校验位
        
        ISBN-13 校验位计算：
        - 前12位数字，奇数位乘以1，偶数位乘以3
        - 求和
        - 对 10 取模
        - 结果为 (10 - (sum % 10)) % 10
        
        Args:
            isbn12: ISBN-13 的前12位数字
            
        Returns:
            校验位（0-9）
        """
        if len(isbn12) != 12 or not isbn12.isdigit():
            raise InvalidISBNError("需要12位数字来计算 ISBN-13 校验位")
        
        total = sum(int(digit) * (1 if i % 2 == 0 else 3) 
                   for i, digit in enumerate(isbn12))
        return str((10 - (total % 10)) % 10)
    
    @staticmethod
    def validate(isbn: str) -> bool:
        """
        验证 ISBN 是否有效
        
        Args:
            isbn: ISBN 字符串（可以是 ISBN-10 或 ISBN-13）
            
        Returns:
            True 如果有效，False 否则
        """
        try:
            ISBNUtils.validate_strict(isbn)
            return True
        except InvalidISBNError:
            return False
    
    @staticmethod
    def validate_strict(isbn: str) -> Dict[str, Any]:
        """
        严格验证 ISBN 并返回详细信息
        
        Args:
            isbn: ISBN 字符串
            
        Returns:
            包含验证信息的字典
            
        Raises:
            InvalidISBNError: 如果 ISBN 无效
        """
        cleaned = ISBNUtils.clean(isbn)
        version = ISBNUtils.detect_version(cleaned)
        
        if version == 10:
            return ISBNUtils._validate_isbn10(cleaned)
        elif version == 13:
            return ISBNUtils._validate_isbn13(cleaned)
        else:
            raise InvalidISBNError(f"无效的 ISBN 格式：{isbn}（清理后长度：{len(cleaned)}）")
    
    @staticmethod
    def _validate_isbn10(isbn: str) -> Dict[str, Any]:
        """验证 ISBN-10"""
        if len(isbn) != 10:
            raise InvalidISBNError(f"ISBN-10 长度必须为 10，当前：{len(isbn)}")
        
        # 前9位必须是数字
        if not isbn[:9].isdigit():
            raise InvalidISBNError("ISBN-10 前9位必须是数字")
        
        # 最后一位可以是数字或 X
        if not (isbn[9].isdigit() or isbn[9] == 'X'):
            raise InvalidISBNError("ISBN-10 最后一位必须是数字或 X")
        
        expected_check = ISBNUtils.calculate_check_digit_10(isbn[:9])
        actual_check = isbn[9]
        
        if expected_check != actual_check:
            raise InvalidISBNError(
                f"ISBN-10 校验位错误：期望 {expected_check}，实际 {actual_check}"
            )
        
        return {
            'valid': True,
            'version': 10,
            'isbn': isbn,
            'isbn_formatted': ISBNUtils.format(isbn),
            'check_digit': actual_check
        }
    
    @staticmethod
    def _validate_isbn13(isbn: str) -> Dict[str, Any]:
        """验证 ISBN-13"""
        if len(isbn) != 13 or not isbn.isdigit():
            raise InvalidISBNError("ISBN-13 必须是 13 位数字")
        
        # 检查前缀
        if not isbn.startswith(('978', '979')):
            raise InvalidISBNError("ISBN-13 必须以 978 或 979 开头")
        
        expected_check = ISBNUtils.calculate_check_digit_12(isbn[:12])
        actual_check = isbn[12]
        
        if expected_check != actual_check:
            raise InvalidISBNError(
                f"ISBN-13 校验位错误：期望 {expected_check}，实际 {actual_check}"
            )
        
        return {
            'valid': True,
            'version': 13,
            'isbn': isbn,
            'isbn_formatted': ISBNUtils.format(isbn),
            'check_digit': actual_check,
            'prefix': isbn[:3]
        }
    
    @staticmethod
    def convert_to_13(isbn: str) -> str:
        """
        将 ISBN-10 转换为 ISBN-13
        
        Args:
            isbn: ISBN-10 字符串
            
        Returns:
            ISBN-13 字符串
            
        Raises:
            ISBNConversionError: 如果转换失败
        """
        cleaned = ISBNUtils.clean(isbn)
        
        if len(cleaned) == 13:
            return cleaned  # 已经是 ISBN-13
        
        if len(cleaned) != 10:
            raise ISBNConversionError(f"无法转换：{isbn}（不是有效的 ISBN-10）")
        
        # 先验证 ISBN-10
        try:
            ISBNUtils._validate_isbn10(cleaned)
        except InvalidISBNError as e:
            raise ISBNConversionError(f"无法转换无效的 ISBN-10：{e}")
        
        # 添加 978 前缀（去掉原校验位）
        isbn12 = '978' + cleaned[:9]
        
        # 计算新的校验位
        check_digit = ISBNUtils.calculate_check_digit_12(isbn12)
        
        return isbn12 + check_digit
    
    @staticmethod
    def convert_to_10(isbn: str) -> str:
        """
        将 ISBN-13 转换为 ISBN-10
        
        注意：只有 978 前缀的 ISBN-13 可以转换为 ISBN-10
        979 前缀的 ISBN-13 没有对应的 ISBN-10
        
        Args:
            isbn: ISBN-13 字符串
            
        Returns:
            ISBN-10 字符串
            
        Raises:
            ISBNConversionError: 如果转换失败
        """
        cleaned = ISBNUtils.clean(isbn)
        
        if len(cleaned) == 10:
            return cleaned  # 已经是 ISBN-10
        
        if len(cleaned) != 13:
            raise ISBNConversionError(f"无法转换：{isbn}（不是有效的 ISBN-13）")
        
        # 验证 ISBN-13
        try:
            ISBNUtils._validate_isbn13(cleaned)
        except InvalidISBNError as e:
            raise ISBNConversionError(f"无法转换无效的 ISBN-13：{e}")
        
        # 只有 978 前缀可以转换
        if not cleaned.startswith('978'):
            raise ISBNConversionError(
                f"只有 978 前缀的 ISBN-13 可以转换为 ISBN-10，当前前缀：{cleaned[:3]}"
            )
        
        # 去掉前缀和校验位，得到 ISBN-10 的前9位
        isbn9 = cleaned[3:12]
        
        # 计算新的校验位
        check_digit = ISBNUtils.calculate_check_digit_10(isbn9)
        
        return isbn9 + check_digit
    
    @staticmethod
    def format(isbn: str, separator: str = '-') -> str:
        """
        格式化 ISBN 为标准显示格式
        
        简化版格式（均匀分割）：
        ISBN-10: X-XXXX-XXXX-X
        ISBN-13: XXX-X-XXXX-XXXX-X
        
        Args:
            isbn: ISBN 字符串
            separator: 分隔符，默认为 '-'
            
        Returns:
            格式化后的 ISBN 字符串
        """
        cleaned = ISBNUtils.clean(isbn)
        version = ISBNUtils.detect_version(cleaned)
        
        if version == 10:
            # ISBN-10: X-XXXX-XXXX-X
            return separator.join([cleaned[:1], cleaned[1:5], cleaned[5:9], cleaned[9]])
        elif version == 13:
            # ISBN-13: XXX-X-XXXX-XXXX-X
            return separator.join([
                cleaned[:3], cleaned[3], cleaned[4:8], cleaned[8:12], cleaned[12]
            ])
        else:
            return isbn  # 无法识别格式，返回原值
    
    @staticmethod
    def parse(isbn: str) -> Dict[str, Any]:
        """
        解析 ISBN 并返回详细信息
        
        Args:
            isbn: ISBN 字符串
            
        Returns:
            包含解析信息的字典
        """
        cleaned = ISBNUtils.clean(isbn)
        version = ISBNUtils.detect_version(cleaned)
        
        result = {
            'original': isbn,
            'cleaned': cleaned,
            'version': version,
            'valid': False
        }
        
        if version is None:
            result['error'] = f"无法识别的 ISBN 格式，长度：{len(cleaned)}"
            return result
        
        try:
            validation = ISBNUtils.validate_strict(cleaned)
            result.update(validation)
            result['valid'] = True
            
            if version == 10:
                # 尝试转换为 ISBN-13
                try:
                    result['isbn13'] = ISBNUtils.convert_to_13(cleaned)
                except:
                    pass
            elif version == 13:
                # 尝试转换为 ISBN-10
                try:
                    result['isbn10'] = ISBNUtils.convert_to_10(cleaned)
                except:
                    result['isbn10'] = None  # 979 前缀无法转换
                
        except InvalidISBNError as e:
            result['error'] = str(e)
        
        return result
    
    @staticmethod
    def generate_random(version: int = 13, prefix: str = None) -> str:
        """
        生成随机有效 ISBN（用于测试）
        
        Args:
            version: ISBN 版本，10 或 13
            prefix: ISBN-13 的前缀（仅用于 version=13），默认随机
            
        Returns:
            随机生成的有效 ISBN 字符串
            
        Raises:
            ValueError: 如果版本不是 10 或 13
        """
        if version == 10:
            # 生成随机的前9位
            isbn9 = ''.join(str(random.randint(0, 9)) for _ in range(9))
            check = ISBNUtils.calculate_check_digit_10(isbn9)
            return isbn9 + check
        
        elif version == 13:
            # 选择前缀
            if prefix is None:
                prefix = random.choice(['978', '979'])
            
            if prefix not in ('978', '979'):
                raise ValueError("ISBN-13 前缀必须是 978 或 979")
            
            # 生成随机的后9位（共12位）
            isbn12 = prefix + ''.join(str(random.randint(0, 9)) for _ in range(9))
            check = ISBNUtils.calculate_check_digit_12(isbn12)
            return isbn12 + check
        
        else:
            raise ValueError("版本必须是 10 或 13")
    
    @staticmethod
    def generate_batch(count: int, version: int = 13) -> list:
        """
        批量生成随机有效 ISBN
        
        Args:
            count: 生成数量
            version: ISBN 版本，10 或 13
            
        Returns:
            ISBN 字符串列表
        """
        return [ISBNUtils.generate_random(version) for _ in range(count)]
    
    @staticmethod
    def extract_from_text(text: str) -> list:
        """
        从文本中提取所有 ISBN
        
        Args:
            text: 要搜索的文本
            
        Returns:
            找到的 ISBN 列表（已验证有效）
        """
        # 匹配可能的 ISBN 模式
        # ISBN-10: 10位数字/X，可能有分隔符
        # ISBN-13: 13位数字，可能有分隔符
        patterns = [
            r'\b(?:ISBN[-\s]?)?(97[89][-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?[\dX])\b',  # ISBN-13
            r'\b(?:ISBN[-\s]?)?(\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?[\dXx])\b',  # ISBN-10
        ]
        
        found = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                cleaned = ISBNUtils.clean(match)
                if ISBNUtils.validate(cleaned):
                    found.add(cleaned)
        
        return list(found)
    
    @staticmethod
    def get_registration_group(isbn: str) -> Optional[str]:
        """
        获取 ISBN 的注册组（国家/地区/语言区）
        
        这是一个简化版本，只识别常见的组区号
        
        Args:
            isbn: ISBN 字符串
            
        Returns:
            注册组名称，如果无法识别返回 None
        """
        cleaned = ISBNUtils.clean(isbn)
        
        # 提取组区号部分
        if len(cleaned) == 13:
            # ISBN-13: 去掉 978/979 前缀
            group_part = cleaned[3:]
        elif len(cleaned) == 10:
            group_part = cleaned
        else:
            return None
        
        # 常见组区号映射（简化版）
        group_map = {
            '0': '英语区',
            '1': '英语区',
            '2': '法语区',
            '3': '德语区',
            '4': '日本',
            '5': '俄语区',
            '7': '中国',
            '80': '捷克/斯洛伐克',
            '81': '印度',
            '82': '挪威',
            '83': '波兰',
            '84': '西班牙',
            '85': '巴西',
            '86': '塞尔维亚',
            '87': '丹麦',
            '88': '意大利',
            '89': '韩国',
            '90': '荷兰/比利时',
            '91': '瑞典',
            '92': '国际组织',
            '93': '印度',
            '94': '荷兰',
            '95': '伊朗',
            '96': '台湾',
            '97': '泰国',
            '98': '伊朗',
            '99': '其他国家'
        }
        
        # 尝试匹配（从长到短）
        for length in [2, 1]:
            if len(group_part) >= length:
                group = group_part[:length]
                if group in group_map:
                    return group_map[group]
        
        return None


# 便捷函数
def validate(isbn: str) -> bool:
    """验证 ISBN 是否有效"""
    return ISBNUtils.validate(isbn)


def validate_strict(isbn: str) -> Dict[str, Any]:
    """严格验证并返回详细信息"""
    return ISBNUtils.validate_strict(isbn)


def convert_to_13(isbn: str) -> str:
    """转换为 ISBN-13"""
    return ISBNUtils.convert_to_13(isbn)


def convert_to_10(isbn: str) -> str:
    """转换为 ISBN-10"""
    return ISBNUtils.convert_to_10(isbn)


def format_isbn(isbn: str, separator: str = '-') -> str:
    """格式化 ISBN"""
    return ISBNUtils.format(isbn, separator)


def parse(isbn: str) -> Dict[str, Any]:
    """解析 ISBN"""
    return ISBNUtils.parse(isbn)


def generate_random(version: int = 13, prefix: str = None) -> str:
    """生成随机 ISBN"""
    return ISBNUtils.generate_random(version, prefix)


def extract_from_text(text: str) -> list:
    """从文本提取 ISBN"""
    return ISBNUtils.extract_from_text(text)


if __name__ == '__main__':
    # 简单演示
    print("=== ISBN Utils 演示 ===\n")
    
    # 测试有效的 ISBN-10
    isbn10 = "0-13-235088-2"  # 《代码整洁之道》
    print(f"ISBN-10: {isbn10}")
    print(f"  清理后: {ISBNUtils.clean(isbn10)}")
    print(f"  验证: {ISBNUtils.validate(isbn10)}")
    print(f"  格式化: {ISBNUtils.format(isbn10)}")
    print(f"  转换为 ISBN-13: {ISBNUtils.convert_to_13(isbn10)}")
    print(f"  注册组: {ISBNUtils.get_registration_group(isbn10)}")
    
    print()
    
    # 测试有效的 ISBN-13
    isbn13 = "978-0-13-235088-4"  # 从 ISBN-10 转换得到
    print(f"ISBN-13: {isbn13}")
    print(f"  清理后: {ISBNUtils.clean(isbn13)}")
    print(f"  验证: {ISBNUtils.validate(isbn13)}")
    print(f"  格式化: {ISBNUtils.format(isbn13)}")
    print(f"  转换为 ISBN-10: {ISBNUtils.convert_to_10(isbn13)}")
    print(f"  注册组: {ISBNUtils.get_registration_group(isbn13)}")
    
    print()
    
    # 生成随机 ISBN
    print("随机生成的 ISBN:")
    for _ in range(3):
        print(f"  ISBN-13: {ISBNUtils.generate_random(13)}")
    for _ in range(3):
        print(f"  ISBN-10: {ISBNUtils.generate_random(10)}")