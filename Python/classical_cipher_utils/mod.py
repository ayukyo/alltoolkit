"""
Classical Cipher Utilities - 古典密码工具集

提供多种经典加密算法的实现，包括：
- Caesar Cipher (凯撒密码)
- Vigenère Cipher (维吉尼亚密码)
- Atbash Cipher (埃特巴什密码)
- ROT13 (ROT13加密)
- Affine Cipher (仿射密码)
- Playfair Cipher (普莱费尔密码)
- Rail Fence Cipher (栅栏密码)
- Columnar Transposition Cipher (列置换密码)

所有算法均为零外部依赖的纯 Python 实现。
"""

import string
from typing import List, Tuple, Optional


class CaesarCipher:
    """
    凯撒密码 - 最简单的替换密码
    
    通过将字母表中的每个字母移动固定位数来实现加密。
    """
    
    @staticmethod
    def encrypt(text: str, shift: int = 3) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
            shift: 位移量（默认为3，经典凯撒密码）
        
        Returns:
            加密后的文本
        """
        result = []
        for char in text:
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            elif char.islower():
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def decrypt(text: str, shift: int = 3) -> str:
        """
        解密文本
        
        Args:
            text: 待解密文本
            shift: 位移量（默认为3）
        
        Returns:
            解密后的文本
        """
        return CaesarCipher.encrypt(text, -shift)
    
    @staticmethod
    def brute_force(text: str) -> List[Tuple[int, str]]:
        """
        暴力破解凯撒密码，返回所有可能的解密结果
        
        Args:
            text: 加密文本
        
        Returns:
            列表，每个元素为 (位移量, 解密文本)
        """
        results = []
        for shift in range(26):
            decrypted = CaesarCipher.decrypt(text, shift)
            results.append((shift, decrypted))
        return results


class ROT13:
    """
    ROT13 - 凯撒密码的特例
    
    将字母移动13位，加密和解密使用相同操作。
    """
    
    @staticmethod
    def transform(text: str) -> str:
        """
        执行ROT13变换（加密和解密相同）
        
        Args:
            text: 待处理文本
        
        Returns:
            变换后的文本
        """
        return CaesarCipher.encrypt(text, 13)
    
    # 别名
    encrypt = transform
    decrypt = transform


class AtbashCipher:
    """
    埃特巴什密码 - 字母表反转替换
    
    将A替换为Z，B替换为Y，以此类推。
    """
    
    @staticmethod
    def encrypt(text: str) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
        
        Returns:
            加密后的文本
        """
        result = []
        for char in text:
            if char.isupper():
                result.append(chr(ord('Z') - (ord(char) - ord('A'))))
            elif char.islower():
                result.append(chr(ord('z') - (ord(char) - ord('a'))))
            else:
                result.append(char)
        return ''.join(result)
    
    # 埃特巴什密码是对称的，加密即解密
    decrypt = encrypt


class VigenereCipher:
    """
    维吉尼亚密码 - 多表替换密码
    
    使用关键词生成不同的位移量进行加密。
    """
    
    @staticmethod
    def _expand_key(text: str, key: str) -> str:
        """扩展密钥以匹配文本长度"""
        key = key.upper()
        expanded = []
        key_index = 0
        for char in text:
            if char.isalpha():
                expanded.append(key[key_index % len(key)])
                key_index += 1
            else:
                expanded.append(char)
        return ''.join(expanded)
    
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
            key: 加密密钥
        
        Returns:
            加密后的文本
        """
        if not key:
            raise ValueError("密钥不能为空")
        
        expanded_key = VigenereCipher._expand_key(text, key)
        result = []
        
        for i, char in enumerate(text):
            if char.isupper():
                shift = ord(expanded_key[i]) - ord('A')
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            elif char.islower():
                shift = ord(expanded_key[i].lower()) - ord('a')
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def decrypt(text: str, key: str) -> str:
        """
        解密文本
        
        Args:
            text: 待解密文本
            key: 解密密钥
        
        Returns:
            解密后的文本
        """
        if not key:
            raise ValueError("密钥不能为空")
        
        expanded_key = VigenereCipher._expand_key(text, key)
        result = []
        
        for i, char in enumerate(text):
            if char.isupper():
                shift = ord(expanded_key[i]) - ord('A')
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            elif char.islower():
                shift = ord(expanded_key[i].lower()) - ord('a')
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(char)
        
        return ''.join(result)


class AffineCipher:
    """
    仿射密码 - 数学函数替换密码
    
    使用公式 E(x) = (ax + b) mod 26 进行加密。
    a 必须与26互质（即 gcd(a, 26) = 1）。
    """
    
    # 与26互质的数
    VALID_A_VALUES = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    
    @staticmethod
    def _gcd(a: int, b: int) -> int:
        """计算最大公约数"""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def _mod_inverse(a: int, m: int) -> int:
        """计算模逆元（扩展欧几里得算法）"""
        def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
    @staticmethod
    def encrypt(text: str, a: int, b: int) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
            a: 乘数（必须与26互质）
            b: 位移量
        
        Returns:
            加密后的文本
        """
        if AffineCipher._gcd(a, 26) != 1:
            raise ValueError(f"参数 a={a} 必须与26互质。有效值: {AffineCipher.VALID_A_VALUES}")
        
        result = []
        for char in text:
            if char.isupper():
                x = ord(char) - ord('A')
                y = (a * x + b) % 26
                result.append(chr(y + ord('A')))
            elif char.islower():
                x = ord(char) - ord('a')
                y = (a * x + b) % 26
                result.append(chr(y + ord('a')))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def decrypt(text: str, a: int, b: int) -> str:
        """
        解密文本
        
        Args:
            text: 待解密文本
            a: 乘数
            b: 位移量
        
        Returns:
            解密后的文本
        """
        if AffineCipher._gcd(a, 26) != 1:
            raise ValueError(f"参数 a={a} 必须与26互质。有效值: {AffineCipher.VALID_A_VALUES}")
        
        a_inverse = AffineCipher._mod_inverse(a, 26)
        result = []
        
        for char in text:
            if char.isupper():
                y = ord(char) - ord('A')
                x = (a_inverse * (y - b)) % 26
                result.append(chr(x + ord('A')))
            elif char.islower():
                y = ord(char) - ord('a')
                x = (a_inverse * (y - b)) % 26
                result.append(chr(x + ord('a')))
            else:
                result.append(char)
        
        return ''.join(result)


class PlayfairCipher:
    """
    普莱费尔密码 - 双字母替换密码
    
    使用5x5矩阵进行加密，支持I/J合并或分开处理。
    """
    
    @staticmethod
    def _create_matrix(key: str, merge_ij: bool = True) -> List[List[str]]:
        """创建5x5密钥矩阵"""
        key = key.upper().replace('J', 'I') if merge_ij else key.upper()
        alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ' if merge_ij else 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        # 移除重复字符
        seen = set()
        unique_key = []
        for char in key + alphabet:
            if char.isalpha() and char not in seen:
                seen.add(char)
                unique_key.append(char)
        
        # 创建5x5矩阵
        matrix = []
        for i in range(5):
            matrix.append(unique_key[i*5:(i+1)*5])
        
        return matrix
    
    @staticmethod
    def _find_position(matrix: List[List[str]], char: str) -> Tuple[int, int]:
        """查找字符在矩阵中的位置"""
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return (i, j)
        raise ValueError(f"字符 {char} 不在矩阵中")
    
    @staticmethod
    def _prepare_text(text: str, merge_ij: bool = True) -> str:
        """准备文本：转大写，处理重复字母，补充X"""
        text = text.upper().replace('J', 'I') if merge_ij else text.upper()
        text = ''.join(c for c in text if c.isalpha())
        
        # 处理重复字母
        prepared = []
        i = 0
        while i < len(text):
            prepared.append(text[i])
            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    prepared.append('X')  # 插入填充字符
                else:
                    prepared.append(text[i + 1])
                    i += 1
            i += 1
        
        # 如果长度为奇数，补充X
        if len(prepared) % 2 == 1:
            prepared.append('X')
        
        return ''.join(prepared)
    
    @staticmethod
    def encrypt(text: str, key: str, merge_ij: bool = True) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
            key: 加密密钥
            merge_ij: 是否合并I和J（默认True）
        
        Returns:
            加密后的文本
        """
        matrix = PlayfairCipher._create_matrix(key, merge_ij)
        prepared = PlayfairCipher._prepare_text(text, merge_ij)
        
        result = []
        for i in range(0, len(prepared), 2):
            char1, char2 = prepared[i], prepared[i + 1]
            row1, col1 = PlayfairCipher._find_position(matrix, char1)
            row2, col2 = PlayfairCipher._find_position(matrix, char2)
            
            if row1 == row2:
                # 同行
                result.append(matrix[row1][(col1 + 1) % 5])
                result.append(matrix[row2][(col2 + 1) % 5])
            elif col1 == col2:
                # 同列
                result.append(matrix[(row1 + 1) % 5][col1])
                result.append(matrix[(row2 + 1) % 5][col2])
            else:
                # 矩形
                result.append(matrix[row1][col2])
                result.append(matrix[row2][col1])
        
        return ''.join(result)
    
    @staticmethod
    def decrypt(text: str, key: str, merge_ij: bool = True) -> str:
        """
        解密文本
        
        Args:
            text: 待解密文本
            key: 解密密钥
            merge_ij: 是否合并I和J（默认True）
        
        Returns:
            解密后的文本
        """
        matrix = PlayfairCipher._create_matrix(key, merge_ij)
        text = text.upper()
        if merge_ij:
            text = text.replace('J', 'I')
        text = ''.join(c for c in text if c.isalpha())
        
        if len(text) % 2 != 0:
            raise ValueError("密文长度必须为偶数")
        
        result = []
        for i in range(0, len(text), 2):
            char1, char2 = text[i], text[i + 1]
            row1, col1 = PlayfairCipher._find_position(matrix, char1)
            row2, col2 = PlayfairCipher._find_position(matrix, char2)
            
            if row1 == row2:
                # 同行
                result.append(matrix[row1][(col1 - 1) % 5])
                result.append(matrix[row2][(col2 - 1) % 5])
            elif col1 == col2:
                # 同列
                result.append(matrix[(row1 - 1) % 5][col1])
                result.append(matrix[(row2 - 1) % 5][col2])
            else:
                # 矩形
                result.append(matrix[row1][col2])
                result.append(matrix[row2][col1])
        
        return ''.join(result)


class RailFenceCipher:
    """
    栅栏密码 - 换位密码
    
    将明文按"之"字形排列在多行上，然后逐行读取。
    """
    
    @staticmethod
    def encrypt(text: str, rails: int = 2) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
            rails: 栅栏数量（行数，默认为2）
        
        Returns:
            加密后的文本
        """
        if rails < 2:
            raise ValueError("栅栏数量必须大于等于2")
        
        if len(text) <= 1:
            return text
        
        # 创建栅栏矩阵
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1  # 1: 向下, -1: 向上
        
        for char in text:
            fence[rail].append(char)
            rail += direction
            
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # 逐行读取
        return ''.join(''.join(row) for row in fence)
    
    @staticmethod
    def decrypt(text: str, rails: int = 2) -> str:
        """
        解密文本
        
        Args:
            text: 待解密文本
            rails: 栅栏数量（行数）
        
        Returns:
            解密后的文本
        """
        if rails < 2:
            raise ValueError("栅栏数量必须大于等于2")
        
        if len(text) <= 1:
            return text
        
        # 计算每个栅栏的字符数量
        rail_lengths = [0] * rails
        rail = 0
        direction = 1
        
        for _ in text:
            rail_lengths[rail] += 1
            rail += direction
            
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # 根据长度分割密文
        fence = []
        index = 0
        for length in rail_lengths:
            fence.append(list(text[index:index + length]))
            index += length
        
        # 按"之"字形读取
        result = []
        rail = 0
        direction = 1
        rail_indices = [0] * rails
        
        for _ in text:
            result.append(fence[rail][rail_indices[rail]])
            rail_indices[rail] += 1
            rail += direction
            
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        return ''.join(result)


class ColumnarTranspositionCipher:
    """
    列置换密码 - 换位密码
    
    将明文按行写入表格，按密钥顺序读取列。
    """
    
    @staticmethod
    def _get_column_order(key: str) -> List[int]:
        """根据密钥获取列的读取顺序"""
        # 对密钥字符排序，获取原始索引
        indexed = [(char, i) for i, char in enumerate(key.upper())]
        sorted_indexed = sorted(enumerate(indexed), key=lambda x: (x[1][0], x[0]))
        return [item[0] for item in sorted_indexed]
    
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
            key: 加密密钥（决定列数和读取顺序）
        
        Returns:
            加密后的文本
        """
        if not key:
            raise ValueError("密钥不能为空")
        
        key = key.upper()
        num_cols = len(key)
        
        # 填充文本使其能被列数整除
        padding_length = (num_cols - len(text) % num_cols) % num_cols
        padded_text = text + 'X' * padding_length
        
        # 创建矩阵
        num_rows = len(padded_text) // num_cols
        matrix = []
        for i in range(num_rows):
            matrix.append(list(padded_text[i * num_cols:(i + 1) * num_cols]))
        
        # 获取列顺序
        order = ColumnarTranspositionCipher._get_column_order(key)
        
        # 按顺序读取列
        result = []
        for col_index in order:
            for row in matrix:
                result.append(row[col_index])
        
        return ''.join(result)
    
    @staticmethod
    def decrypt(text: str, key: str) -> str:
        """
        解密文本
        
        Args:
            text: 待解密文本
            key: 解密密钥
        
        Returns:
            解密后的文本
        """
        if not key:
            raise ValueError("密钥不能为空")
        
        key = key.upper()
        num_cols = len(key)
        
        if len(text) % num_cols != 0:
            raise ValueError("密文长度必须能被密钥长度整除")
        
        num_rows = len(text) // num_cols
        
        # 获取列顺序
        order = ColumnarTranspositionCipher._get_column_order(key)
        
        # 将密文分割成列
        col_length = num_rows
        columns = []
        for i in range(num_cols):
            start = i * col_length
            columns.append(list(text[start:start + col_length]))
        
        # 重建矩阵
        matrix = [[''] * num_cols for _ in range(num_rows)]
        for i, col_index in enumerate(order):
            for row in range(num_rows):
                matrix[row][col_index] = columns[i][row]
        
        # 按行读取
        result = ''.join(''.join(row) for row in matrix)
        
        return result


class SimpleSubstitutionCipher:
    """
    简单替换密码 - 单表替换密码
    
    使用自定义字母映射表进行加密。
    """
    
    @staticmethod
    def _create_key_map(key: str) -> Tuple[dict, dict]:
        """创建加密和解密映射表"""
        key = key.upper()
        alphabet = string.ascii_uppercase
        
        # 移除重复字符
        seen = set()
        unique_key = []
        for char in key:
            if char not in seen and char.isalpha():
                seen.add(char)
                unique_key.append(char)
        
        # 补充剩余字母
        for char in alphabet:
            if char not in seen:
                unique_key.append(char)
        
        # 创建映射
        encrypt_map = {alphabet[i]: unique_key[i] for i in range(26)}
        decrypt_map = {unique_key[i]: alphabet[i] for i in range(26)}
        
        return encrypt_map, decrypt_map
    
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
            key: 替换密钥（至少包含部分字母）
        
        Returns:
            加密后的文本
        """
        encrypt_map, _ = SimpleSubstitutionCipher._create_key_map(key)
        
        result = []
        for char in text:
            if char.isupper():
                result.append(encrypt_map[char])
            elif char.islower():
                result.append(encrypt_map[char.upper()].lower())
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def decrypt(text: str, key: str) -> str:
        """
        解密文本
        
        Args:
            text: 待解密文本
            key: 替换密钥
        
        Returns:
            解密后的文本
        """
        _, decrypt_map = SimpleSubstitutionCipher._create_key_map(key)
        
        result = []
        for char in text:
            if char.isupper():
                result.append(decrypt_map[char])
            elif char.islower():
                result.append(decrypt_map[char.upper()].lower())
            else:
                result.append(char)
        
        return ''.join(result)


class PolybiusSquareCipher:
    """
    波利比乌斯方阵密码
    
    使用5x5方阵将字母转换为坐标对。
    """
    
    # 标准波利比乌斯方阵（I/J合并）
    STANDARD_SQUARE = [
        ['A', 'B', 'C', 'D', 'E'],
        ['F', 'G', 'H', 'I', 'K'],  # I/J
        ['L', 'M', 'N', 'O', 'P'],
        ['Q', 'R', 'S', 'T', 'U'],
        ['V', 'W', 'X', 'Y', 'Z']
    ]
    
    @staticmethod
    def _find_in_square(square: List[List[str]], char: str) -> Optional[Tuple[int, int]]:
        """在方阵中查找字符位置"""
        char = char.upper()
        if char == 'J':
            char = 'I'
        
        for i in range(5):
            for j in range(5):
                if square[i][j] == char:
                    return (i + 1, j + 1)  # 返回1-based坐标
        return None
    
    @staticmethod
    def encrypt(text: str, square: Optional[List[List[str]]] = None) -> str:
        """
        加密文本
        
        Args:
            text: 待加密文本
            square: 自定义5x5方阵（默认使用标准方阵）
        
        Returns:
            加密后的坐标数字串
        """
        if square is None:
            square = PolybiusSquareCipher.STANDARD_SQUARE
        
        result = []
        for char in text.upper():
            if char.isalpha():
                pos = PolybiusSquareCipher._find_in_square(square, char)
                if pos:
                    result.extend([str(pos[0]), str(pos[1])])
            # 非字母字符忽略
        
        return ''.join(result)
    
    @staticmethod
    def decrypt(text: str, square: Optional[List[List[str]]] = None) -> str:
        """
        解密文本
        
        Args:
            text: 待解密的数字串
            square: 自定义5x5方阵（默认使用标准方阵）
        
        Returns:
            解密后的文本
        """
        if square is None:
            square = PolybiusSquareCipher.STANDARD_SQUARE
        
        # 提取数字
        digits = [c for c in text if c.isdigit()]
        
        if len(digits) % 2 != 0:
            raise ValueError("密文数字个数必须为偶数")
        
        result = []
        for i in range(0, len(digits), 2):
            row = int(digits[i]) - 1  # 转为0-based
            col = int(digits[i + 1]) - 1
            
            if 0 <= row < 5 and 0 <= col < 5:
                result.append(square[row][col])
            else:
                raise ValueError(f"无效坐标: ({row+1}, {col+1})")
        
        return ''.join(result)


# 便捷函数
def caesar_encrypt(text: str, shift: int = 3) -> str:
    """凯撒加密"""
    return CaesarCipher.encrypt(text, shift)


def caesar_decrypt(text: str, shift: int = 3) -> str:
    """凯撒解密"""
    return CaesarCipher.decrypt(text, shift)


def rot13(text: str) -> str:
    """ROT13变换"""
    return ROT13.transform(text)


def atbash(text: str) -> str:
    """埃特巴什密码"""
    return AtbashCipher.encrypt(text)


def vigenere_encrypt(text: str, key: str) -> str:
    """维吉尼亚加密"""
    return VigenereCipher.encrypt(text, key)


def vigenere_decrypt(text: str, key: str) -> str:
    """维吉尼亚解密"""
    return VigenereCipher.decrypt(text, key)


def affine_encrypt(text: str, a: int, b: int) -> str:
    """仿射加密"""
    return AffineCipher.encrypt(text, a, b)


def affine_decrypt(text: str, a: int, b: int) -> str:
    """仿射解密"""
    return AffineCipher.decrypt(text, a, b)


def rail_fence_encrypt(text: str, rails: int = 2) -> str:
    """栅栏加密"""
    return RailFenceCipher.encrypt(text, rails)


def rail_fence_decrypt(text: str, rails: int = 2) -> str:
    """栅栏解密"""
    return RailFenceCipher.decrypt(text, rails)


def playfair_encrypt(text: str, key: str) -> str:
    """普莱费尔加密"""
    return PlayfairCipher.encrypt(text, key)


def playfair_decrypt(text: str, key: str) -> str:
    """普莱费尔解密"""
    return PlayfairCipher.decrypt(text, key)


if __name__ == "__main__":
    # 演示
    print("=== Classical Cipher Utils Demo ===\n")
    
    # 凯撒密码
    text = "Hello World"
    encrypted = CaesarCipher.encrypt(text, 3)
    print(f"Caesar Cipher:")
    print(f"  原文: {text}")
    print(f"  密文: {encrypted}")
    print(f"  解密: {CaesarCipher.decrypt(encrypted, 3)}\n")
    
    # ROT13
    text = "Python"
    print(f"ROT13:")
    print(f"  原文: {text}")
    print(f"  变换: {ROT13.transform(text)}\n")
    
    # 维吉尼亚密码
    text = "ATTACKATDAWN"
    key = "LEMON"
    encrypted = VigenereCipher.encrypt(text, key)
    print(f"Vigenere Cipher:")
    print(f"  原文: {text}")
    print(f"  密钥: {key}")
    print(f"  密文: {encrypted}")
    print(f"  解密: {VigenereCipher.decrypt(encrypted, key)}\n")
    
    # 仿射密码
    text = "AFFINE"
    encrypted = AffineCipher.encrypt(text, 5, 8)
    print(f"Affine Cipher:")
    print(f"  原文: {text}")
    print(f"  密文: {encrypted}")
    print(f"  解密: {AffineCipher.decrypt(encrypted, 5, 8)}\n")
    
    # 栅栏密码
    text = "WE ARE DISCOVERED FLEE AT ONCE"
    encrypted = RailFenceCipher.encrypt(text, 3)
    print(f"Rail Fence Cipher:")
    print(f"  原文: {text}")
    print(f"  密文: {encrypted}")
    print(f"  解密: {RailFenceCipher.decrypt(encrypted, 3)}\n")
    
    # 普莱费尔密码
    text = "HELLOWORLD"
    key = "PLAYFAIR"
    encrypted = PlayfairCipher.encrypt(text, key)
    print(f"Playfair Cipher:")
    print(f"  原文: {text}")
    print(f"  密钥: {key}")
    print(f"  密文: {encrypted}")
    print(f"  解密: {PlayfairCipher.decrypt(encrypted, key)}\n")