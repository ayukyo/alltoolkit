#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XOR Utils - XOR（异或）操作工具模块
===================================
提供 XOR 加密、解密、校验和位操作功能。
零外部依赖，仅使用 Python 标准库。

主要功能:
- XOR 加密/解密（单密钥、多密钥、滚动密钥）
- XOR 校验和计算
- XOR 密码分析（频率分析、密钥长度推测）
- 位运算工具（位翻转、位交换）
- XOR 编码/解码（十六进制、Base64）
- XOR 模式检测
- 批量 XOR 操作

作者: AllToolkit
日期: 2026-04-27
"""

from typing import List, Tuple, Optional, Union, Dict, Generator
from dataclasses import dataclass
from enum import Enum
import string


class XORMode(Enum):
    """XOR 操作模式"""
    SINGLE_KEY = "single"      # 单密钥 XOR
    MULTI_KEY = "multi"        # 多密钥 XOR
    ROLLING_KEY = "rolling"    # 滚动密钥 XOR
    REPEATING_KEY = "repeating"  # 重复密钥 XOR


@dataclass
class XORResult:
    """XOR 操作结果"""
    data: bytes           # XOR 后的数据
    key: bytes            # 使用的密钥
    checksum: int         # XOR 校验和
    
    def to_hex(self) -> str:
        """转换为十六进制字符串"""
        return self.data.hex()
    
    def to_base64(self) -> str:
        """转换为 Base64 字符串（无外部依赖实现）"""
        import base64
        return base64.b64encode(self.data).decode('ascii')
    
    def to_string(self, encoding: str = 'utf-8') -> str:
        """尝试转换为字符串"""
        try:
            return self.data.decode(encoding)
        except UnicodeDecodeError:
            return self.to_hex()


# ==================== 基础 XOR 操作 ====================

def xor_byte(data: bytes, key: int) -> bytes:
    """
    单字节 XOR 操作
    
    Args:
        data: 要处理的数据
        key: XOR 密钥（0-255）
    
    Returns:
        XOR 后的数据
    
    Examples:
        >>> xor_byte(b'Hello', 0x55)
        b'\\x1d\\x34\\x39\\x39\\x36'
        >>> xor_byte(xor_byte(b'Test', 0xAA), 0xAA)  # XOR 是对称的
        b'Test'
    """
    if not 0 <= key <= 255:
        raise ValueError("密钥必须在 0-255 范围内")
    return bytes(b ^ key for b in data)


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """
    多字节 XOR 操作（重复密钥）
    
    Args:
        data: 要处理的数据
        key: XOR 密钥字节序列
    
    Returns:
        XOR 后的数据
    
    Examples:
        >>> xor_bytes(b'Hello World', b'KEY')
        b'\\x0b\\x05\\x1eK\\x05\\x11\\x05\\x1eK\\x05'
        >>> xor_bytes(xor_bytes(b'Data', b'ABC'), b'ABC')
        b'Data'
    """
    if not key:
        raise ValueError("密钥不能为空")
    
    key_len = len(key)
    return bytes(data[i] ^ key[i % key_len] for i in range(len(data)))


def xor_single_pass(data: bytes, key: bytes) -> bytes:
    """
    单次 XOR（密钥只使用一次，数据截断到密钥长度）
    
    Args:
        data: 要处理的数据
        key: XOR 密钥
    
    Returns:
        XOR 后的数据（长度等于 min(len(data), len(key))）
    
    Examples:
        >>> xor_single_pass(b'Hello', b'KEY')
        b'\\x0b\\x05\\x1e'
    """
    length = min(len(data), len(key))
    return bytes(data[i] ^ key[i] for i in range(length))


def xor_rolling_key(data: bytes, seed: int = 0) -> bytes:
    """
    滚动密钥 XOR（每个字节使用不同的密钥）
    
    密钥生成算法：key[i] = (seed + i) & 0xFF
    
    Args:
        data: 要处理的数据
        seed: 密钥种子
    
    Returns:
        XOR 后的数据
    
    Examples:
        >>> xor_rolling_key(b'Hello', 0)
        b'Hello'  # seed=0 时，key[i]=i，自 XOR 结果不变位置
    """
    return bytes(b ^ ((seed + i) & 0xFF) for i, b in enumerate(data))


def xor_chain(data: bytes, keys: List[int]) -> bytes:
    """
    链式 XOR（多个单字节密钥依次 XOR）
    
    Args:
        data: 要处理的数据
        keys: 密钥列表（0-255）
    
    Returns:
        XOR 后的数据
    
    Examples:
        >>> xor_chain(b'Hello', [0x55, 0xAA])  # 先 XOR 0x55，再 XOR 0xAA
        b'\\x1e\\x7f\\x7c\\x7c\\x73'
        >>> xor_chain(b'Hello', [0x55, 0xAA, 0xFF])  # 等于 XOR (0x55^0xAA^0xFF)
        b'\\xe1\\x34\\x39\\x39\\x36'
    """
    result = data
    for key in keys:
        result = xor_byte(result, key)
    return result


# ==================== XOR 校验和 ====================

def xor_checksum(data: bytes) -> int:
    """
    计算 XOR 校验和（所有字节 XOR 的结果）
    
    Args:
        data: 要计算的数据
    
    Returns:
        XOR 校验和（0-255）
    
    Examples:
        >>> xor_checksum(b'\\x01\\x02\\x03')
        0
        >>> xor_checksum(b'Hello')
        22
    """
    if not data:
        return 0
    result = 0
    for b in data:
        result ^= b
    return result


def xor_checksum_range(data: bytes, start: int, end: int) -> int:
    """
    计算指定范围的 XOR 校验和
    
    Args:
        data: 数据
        start: 起始位置
        end: 结束位置
    
    Returns:
        XOR 校验和
    
    Examples:
        >>> xor_checksum_range(b'Hello World', 0, 5)
        22  # 'Hello' 的校验和
    """
    return xor_checksum(data[start:end])


def xor_checksum_blocks(data: bytes, block_size: int) -> List[int]:
    """
    分块计算 XOR 校验和
    
    Args:
        data: 数据
        block_size: 块大小
    
    Returns:
        每块的 XOR 校验和列表
    
    Examples:
        >>> xor_checksum_blocks(b'HelloWorld', 5)
        [22, 87]  # 'Hello' 和 'World' 的校验和
    """
    if block_size <= 0:
        raise ValueError("块大小必须大于 0")
    
    checksums = []
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        checksums.append(xor_checksum(block))
    return checksums


def verify_xor_checksum(data: bytes, expected: int) -> bool:
    """
    验证 XOR 校验和
    
    Args:
        data: 数据
        expected: 期望的校验和
    
    Returns:
        是否匹配
    
    Examples:
        >>> verify_xor_checksum(b'Hello', 22)
        True
    """
    return xor_checksum(data) == expected


# ==================== XOR 密码分析 ====================

def frequency_analysis(data: bytes) -> Dict[int, int]:
    """
    字节频率分析
    
    Args:
        data: 要分析的数据
    
    Returns:
        字节频率字典 {byte_value: count}
    
    Examples:
        >>> freq = frequency_analysis(b'Hello')
        >>> freq[ord('l')]
        2
    """
    freq: Dict[int, int] = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    return freq


def find_most_frequent(data: bytes, top_n: int = 10) -> List[Tuple[int, int]]:
    """
    找出最频繁的字节
    
    Args:
        data: 数据
        top_n: 返回前 N 个
    
    Returns:
        [(byte_value, count), ...] 按频率排序
    
    Examples:
        >>> find_most_frequent(b'Hello', 3)
        [(108, 2), (72, 1), (101, 1)]  # 'l'=108 出现 2 次
    """
    freq = frequency_analysis(data)
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq[:top_n]


def guess_single_byte_key(data: bytes, 
                          known_plaintext: Optional[bytes] = None) -> List[Tuple[int, float]]:
    """
    推测单字节 XOR 密钥
    
    使用频率分析方法，假设明文是英文文本。
    
    Args:
        data: 密文数据
        known_plaintext: 已知的明文片段（可选）
    
    Returns:
        [(可能的密钥, 置信度), ...] 按置信度排序
    
    Examples:
        >>> ciphertext = xor_byte(b'Hello World', 0x55)
        >>> guess_single_byte_key(ciphertext)[:3]  # 返回前 3 个猜测
        [(85, 0.8), (...), (...)]  # 85 = 0x55
    """
    # 英文字符频率（简化版）
    english_freq = {
        ord('e'): 12.7, ord('t'): 9.1, ord('a'): 8.2, ord('o'): 7.5,
        ord('i'): 7.0, ord('n'): 6.7, ord('s'): 6.3, ord('h'): 6.1,
        ord('r'): 6.0, ord('d'): 4.3, ord('l'): 4.0, ord('c'): 2.8,
        ord('u'): 2.8, ord('m'): 2.4, ord('w'): 2.4, ord('f'): 2.2,
        ord('g'): 2.0, ord('y'): 2.0, ord('p'): 1.9, ord('b'): 1.5,
        ord('v'): 1.0, ord('k'): 0.8, ord('j'): 0.15, ord('x'): 0.15,
        ord('q'): 0.10, ord('z'): 0.07, ord(' '): 13.0
    }
    
    scores: Dict[int, float] = {}
    
    for key in range(256):
        decrypted = xor_byte(data, key)
        
        # 计算得分
        score = 0.0
        for b in decrypted:
            if b in english_freq:
                score += english_freq[b]
            elif b in range(65, 91) or b in range(97, 123):  # A-Z, a-z
                score += 1.0
            elif b == ord(' '):
                score += 13.0
            elif b in range(32, 127):  # 可打印 ASCII
                score += 0.5
            elif b == 0 or b > 127:  # 控制字符或非 ASCII
                score -= 5.0
        
        scores[key] = score
    
    # 如果有已知明文
    if known_plaintext:
        for key in range(256):
            decrypted = xor_byte(data[:len(known_plaintext)], key)
            if decrypted == known_plaintext:
                scores[key] += 100.0  # 大幅提升置信度
    
    # 按得分排序
    total = max(scores.values()) if scores else 1
    sorted_keys = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # 转换为置信度（0-1）
    results = []
    for key, score in sorted_keys[:20]:
        confidence = score / total if total > 0 else 0
        results.append((key, min(confidence, 1.0)))
    
    return results


def guess_key_length(data: bytes, max_length: int = 32) -> List[Tuple[int, float]]:
    """
    推测重复密钥的长度（使用 Hamming 距离方法）
    
    Args:
        data: 密文数据
        max_length: 最大测试长度
    
    Returns:
        [(可能的长度, 得分), ...] 按得分排序
    
    Examples:
        >>> ciphertext = xor_bytes(b'Hello World Hello', b'KEY')
        >>> guess_key_length(ciphertext)[:3]
        [(3, 0.9), (...), (...)]  # 密钥长度为 3
    """
    def hamming_distance(b1: bytes, b2: bytes) -> int:
        """计算 Hamming 距离（不同位的数量）"""
        distance = 0
        for x, y in zip(b1, b2):
            distance += bin(x ^ y).count('1')
        return distance
    
    if len(data) < max_length * 2:
        max_length = len(data) // 2
    
    scores: Dict[int, float] = {}
    
    for keysize in range(2, max_length + 1):
        # 取多个块计算平均 Hamming 距离
        num_blocks = min(8, len(data) // keysize)
        if num_blocks < 2:
            continue
        
        total_distance = 0
        comparisons = 0
        
        for i in range(num_blocks - 1):
            block1 = data[i * keysize:(i + 1) * keysize]
            block2 = data[(i + 1) * keysize:(i + 2) * keysize]
            total_distance += hamming_distance(block1, block2)
            comparisons += 1
        
        if comparisons > 0:
            # 归一化 Hamming 距离
            normalized = total_distance / comparisons / keysize
            # 得分：距离越小越好，转换为得分
            scores[keysize] = 8.0 - normalized  # 8 是最大 Hamming 距离/字节
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:10]


def break_repeating_key_xor(data: bytes, 
                            key_length: Optional[int] = None) -> Tuple[bytes, bytes]:
    """
    破解重复密钥 XOR 加密
    
    Args:
        data: 密文数据
        key_length: 密钥长度（可选，自动推测）
    
    Returns:
        (密钥, 解密后的明文)
    
    Examples:
        >>> ciphertext = xor_bytes(b'Hello World!', b'KEY')
        >>> key, plaintext = break_repeating_key_xor(ciphertext)
        >>> plaintext[:5]
        b'Hello'
    """
    # 如果未提供密钥长度，自动推测
    if key_length is None:
        guesses = guess_key_length(data)
        if not guesses:
            return b'', data
        key_length = guesses[0][0]
    
    # 将数据按密钥长度分块
    key = bytearray(key_length)
    
    for i in range(key_length):
        # 收集位置 i 的所有字节
        column = bytes(data[j] for j in range(i, len(data), key_length))
        
        # 对每列进行单字节密钥推测
        guesses = guess_single_byte_key(column)
        if guesses:
            key[i] = guesses[0][0]
    
    # 解密
    plaintext = xor_bytes(data, bytes(key))
    
    return bytes(key), plaintext


# ==================== 位操作工具 ====================

def flip_bits(data: bytes, positions: List[int]) -> bytes:
    """
    翻转指定位置的位
    
    Args:
        data: 数据
        positions: 要翻转的位位置列表（全局位置）
    
    Returns:
        翻转后的数据
    
    Examples:
        >>> flip_bits(b'\\x00', [0, 1, 2])  # 翻转第 0, 1, 2 位
        b'\\x07'
    """
    result = bytearray(data)
    for pos in positions:
        byte_index = pos // 8
        bit_index = pos % 8
        if byte_index < len(result):
            result[byte_index] ^= (1 << bit_index)
    return bytes(result)


def swap_bits(data: bytes, pos1: int, pos2: int) -> bytes:
    """
    交换两个位
    
    Args:
        data: 数据
        pos1: 第一个位位置
        pos2: 第二个位位置
    
    Returns:
        交换后的数据
    
    Examples:
        >>> swap_bits(b'\\x01', 0, 7)  # 交换第 0 位和第 7 位
        b'\\x80'
    """
    result = bytearray(data)
    
    byte1 = pos1 // 8
    bit1 = pos1 % 8
    byte2 = pos2 // 8
    bit2 = pos2 % 8
    
    if byte1 < len(result) and byte2 < len(result):
        # 获取两个位的值
        val1 = (result[byte1] >> bit1) & 1
        val2 = (result[byte2] >> bit2) & 1
        
        # 如果值不同，交换
        if val1 != val2:
            result[byte1] ^= (1 << bit1)
            result[byte2] ^= (1 << bit2)
    
    return bytes(result)


def reverse_bits(data: bytes) -> bytes:
    """
    反转每个字节内的位
    
    Args:
        data: 数据
    
    Returns:
        位反转后的数据
    
    Examples:
        >>> reverse_bits(b'\\x01')  # 00000001 -> 10000000
        b'\\x80'
        >>> reverse_bits(b'\\xF0')  # 11110000 -> 00001111
        b'\\x0F'
    """
    result = bytearray(len(data))
    for i, b in enumerate(data):
        # 反转 8 位
        reversed_byte = 0
        for j in range(8):
            if b & (1 << j):
                reversed_byte |= (1 << (7 - j))
        result[i] = reversed_byte
    return bytes(result)


def count_bits(data: bytes) -> int:
    """
    计算数据中值为 1 的位数量
    
    Args:
        data: 数据
    
    Returns:
        1 位数量
    
    Examples:
        >>> count_bits(b'\\xFF\\x00')
        8
        >>> count_bits(b'\\x0F')
        4
    """
    total = 0
    for b in data:
        total += bin(b).count('1')
    return total


def bit_diff(data1: bytes, data2: bytes) -> int:
    """
    计算两个数据之间的位差（Hamming 距离）
    
    Args:
        data1: 第一个数据
        data2: 第二个数据
    
    Returns:
        Hamming 距离
    
    Examples:
        >>> bit_diff(b'\\x00', b'\\xFF')
        8
        >>> bit_diff(b'Hello', b'Hallo')
        2
    """
    min_len = min(len(data1), len(data2))
    distance = 0
    
    for i in range(min_len):
        xor_result = data1[i] ^ data2[i]
        distance += bin(xor_result).count('1')
    
    # 长度差异也算作位差
    distance += abs(len(data1) - len(data2)) * 8
    
    return distance


# ==================== XOR 编码/解码 ====================

def xor_encode_hex(data: bytes, key: bytes) -> str:
    """
    XOR 加密并编码为十六进制
    
    Args:
        data: 明文数据
        key: 密钥
    
    Returns:
        十六进制字符串
    
    Examples:
        >>> xor_encode_hex(b'Hello', b'K')
        '1d34393936'
    """
    return xor_bytes(data, key).hex()


def xor_decode_hex(hex_string: str, key: bytes) -> bytes:
    """
    从十六进制解码并 XOR 解密
    
    Args:
        hex_string: 十六进制字符串
        key: 密钥
    
    Returns:
        解密后的数据
    
    Examples:
        >>> xor_decode_hex('1d34393936', b'K')
        b'Hello'
    """
    data = bytes.fromhex(hex_string)
    return xor_bytes(data, key)


def xor_encode_string(plaintext: str, key: str, encoding: str = 'utf-8') -> str:
    """
    XOR 加密字符串并返回十六进制结果
    
    Args:
        plaintext: 明文字符串
        key: 密钥字符串
        encoding: 编码方式
    
    Returns:
        十六进制字符串
    
    Examples:
        >>> xor_encode_string('Hello', 'KEY')
        '0b051e4b05'
    """
    data = plaintext.encode(encoding)
    key_bytes = key.encode(encoding)
    return xor_bytes(data, key_bytes).hex()


def xor_decode_string(hex_string: str, key: str, encoding: str = 'utf-8') -> str:
    """
    从十六进制解码并 XOR 解密为字符串
    
    Args:
        hex_string: 十六进制字符串
        key: 密钥字符串
        encoding: 编码方式
    
    Returns:
        解密后的字符串
    
    Examples:
        >>> xor_decode_string('0b051e4b05', 'KEY')
        'Hello'
    """
    data = bytes.fromhex(hex_string)
    key_bytes = key.encode(encoding)
    decrypted = xor_bytes(data, key_bytes)
    return decrypted.decode(encoding)


# ==================== XOR 模式检测 ====================

def detect_xor_pattern(data: bytes, min_pattern_len: int = 3) -> List[Tuple[bytes, int]]:
    """
    检测 XOR 加密后的重复模式
    
    Args:
        data: 数据
        min_pattern_len: 最小模式长度
    
    Returns:
        [(重复模式, 出现次数), ...]
    
    Examples:
        >>> ciphertext = xor_bytes(b'ABCABCABC', b'K')
        >>> patterns = detect_xor_pattern(ciphertext, 3)
        >>> len(patterns) > 0  # 应检测到重复模式
        True
    """
    patterns: Dict[bytes, int] = {}
    
    for length in range(min_pattern_len, min(32, len(data) // 2 + 1)):
        for start in range(len(data) - length):
            pattern = data[start:start + length]
            # 检查这个模式是否在其他位置出现
            count = 1
            for other_start in range(start + length, len(data) - length + 1):
                if data[other_start:other_start + length] == pattern:
                    count += 1
            if count >= 2:
                patterns[pattern] = max(patterns.get(pattern, 0), count)
    
    # 按出现次数排序
    sorted_patterns = sorted(patterns.items(), key=lambda x: (x[1], len(x[0])), reverse=True)
    return sorted_patterns[:20]


def find_xor_collisions(data1: bytes, data2: bytes) -> List[int]:
    """
    找出两个数据 XOR 后相同的位置
    
    Args:
        data1: 第一个数据
        data2: 第二个数据
    
    Returns:
        XOR 结果为 0 的位置列表
    
    Examples:
        >>> find_xor_collisions(b'Hello', b'Hallo')
        [0]  # 只有位置 0 相同
    """
    min_len = min(len(data1), len(data2))
    collisions = []
    
    for i in range(min_len):
        if data1[i] == data2[i]:
            collisions.append(i)
    
    return collisions


# ==================== 批量 XOR 操作 ====================

def xor_all_with_key(datas: List[bytes], key: bytes) -> List[bytes]:
    """
    对多个数据使用同一密钥进行 XOR
    
    Args:
        datas: 数据列表
        key: 密钥
    
    Returns:
        XOR 后的数据列表
    
    Examples:
        >>> xor_all_with_key([b'Hello', b'World'], b'K')
        [b'\\x1d\\x34\\x39\\x39\\x36', b'\\x16\\x38\\x36\\x3b\\x37']
    """
    return [xor_bytes(d, key) for d in datas]


def xor_pairs(datas1: List[bytes], datas2: List[bytes]) -> List[bytes]:
    """
    对两个列表中的对应数据进行 XOR
    
    Args:
        datas1: 第一个数据列表
        datas2: 第二个数据列表
    
    Returns:
        XOR 后的数据列表
    
    Examples:
        >>> xor_pairs([b'Hello', b'Test'], [b'KEYKE', b'ABC'])
        [b'\\x0b\\x05\\x1eK\\x05', b'\\x15\\x07\\x17']
    """
    min_len = min(len(datas1), len(datas2))
    results = []
    
    for i in range(min_len):
        min_data_len = min(len(datas1[i]), len(datas2[i]))
        result = bytes(datas1[i][j] ^ datas2[i][j] for j in range(min_data_len))
        results.append(result)
    
    return results


def generate_xor_key_stream(seed: int, length: int) -> bytes:
    """
    生成 XOR 密钥流（简单的 LFSR 实现）
    
    Args:
        seed: 种子值
        length: 生成长度
    
    Returns:
        密钥流
    
    Examples:
        >>> key_stream = generate_xor_key_stream(0x55, 10)
        >>> len(key_stream)
        10
    """
    result = bytearray(length)
    state = seed
    
    for i in range(length):
        # 简单的伪随机生成
        state = (state * 1103515245 + 12345) & 0xFF
        result[i] = state
    
    return bytes(result)


# ==================== 工具函数 ====================

def create_xor_result(data: bytes, key: bytes) -> XORResult:
    """
    创建 XOR 操作结果对象
    
    Args:
        data: 原始数据
        key: 密钥
    
    Returns:
        XORResult 对象
    
    Examples:
        >>> result = create_xor_result(b'Hello', b'K')
        >>> result.checksum
        22
    """
    xor_data = xor_bytes(data, key)
    checksum = xor_checksum(xor_data)
    return XORResult(data=xor_data, key=key, checksum=checksum)


def xor_encrypt_file_content(content: bytes, key: bytes, 
                             add_checksum: bool = True) -> bytes:
    """
    加密文件内容（带可选校验和）
    
    Args:
        content: 文件内容
        key: 密钥
        add_checksum: 是否添加校验和
    
    Returns:
        加密后的数据
    
    Examples:
        >>> encrypted = xor_encrypt_file_content(b'Hello', b'KEY', True)
        >>> encrypted[-1]  # 最后一个字节是校验和
        ...
    """
    encrypted = xor_bytes(content, key)
    if add_checksum:
        checksum = xor_checksum(content)
        encrypted += bytes([checksum])
    return encrypted


def xor_decrypt_file_content(encrypted: bytes, key: bytes,
                             verify_checksum: bool = True) -> Tuple[bytes, bool]:
    """
    解密文件内容（带校验和验证）
    
    Args:
        encrypted: 加密数据
        key: 密钥
        verify_checksum: 是否验证校验和
    
    Returns:
        (解密内容, 校验和是否正确)
    
    Examples:
        >>> encrypted = xor_encrypt_file_content(b'Hello', b'KEY', True)
        >>> content, valid = xor_decrypt_file_content(encrypted, b'KEY', True)
        >>> valid
        True
    """
    if verify_checksum and len(encrypted) > 0:
        stored_checksum = encrypted[-1]
        encrypted = encrypted[:-1]
        decrypted = xor_bytes(encrypted, key)
        computed_checksum = xor_checksum(decrypted)
        return decrypted, computed_checksum == stored_checksum
    else:
        decrypted = xor_bytes(encrypted, key)
        return decrypted, True


def printable_xor_result(data: bytes) -> str:
    """
    将 XOR 结果转换为可打印形式
    
    Args:
        data: XOR 后的数据
    
    Returns:
        可打印字符串（非打印字符用 . 表示）
    
    Examples:
        >>> printable_xor_result(b'Hello\\x00\\xFF')
        'Hello..'
    """
    result = []
    for b in data:
        if 32 <= b <= 126:
            result.append(chr(b))
        else:
            result.append('.')
    return ''.join(result)


# ==================== XOR 数据类方法 ====================

class XORCipher:
    """XOR 加密器类"""
    
    def __init__(self, key: bytes):
        """
        初始化 XOR 加密器
        
        Args:
            key: 密钥
        """
        if not key:
            raise ValueError("密钥不能为空")
        self._key = key
        self._position = 0
    
    def encrypt(self, data: bytes) -> bytes:
        """加密数据"""
        return xor_bytes(data, self._key)
    
    def decrypt(self, data: bytes) -> bytes:
        """解密数据（XOR 加密的对称性）"""
        return xor_bytes(data, self._key)
    
    def reset(self) -> None:
        """重置位置"""
        self._position = 0
    
    @property
    def key(self) -> bytes:
        """获取密钥"""
        return self._key
    
    def encrypt_stream(self, data_generator: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
        """
        流式加密
        
        Args:
            data_generator: 数据生成器
        
        Yields:
            加密后的数据块
        """
        for chunk in data_generator:
            yield self.encrypt(chunk)
    
    def decrypt_stream(self, data_generator: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
        """
        流式解密
        
        Args:
            data_generator: 数据生成器
        
        Yields:
            解密后的数据块
        """
        for chunk in data_generator:
            yield self.decrypt(chunk)


class SingleByteXORCipher:
    """单字节 XOR 加密器"""
    
    def __init__(self, key: int):
        """
        初始化
        
        Args:
            key: 单字节密钥（0-255）
        """
        if not 0 <= key <= 255:
            raise ValueError("密钥必须在 0-255 范围内")
        self._key = key
    
    def encrypt(self, data: bytes) -> bytes:
        """加密"""
        return xor_byte(data, self._key)
    
    def decrypt(self, data: bytes) -> bytes:
        """解密"""
        return xor_byte(data, self._key)
    
    @property
    def key(self) -> int:
        """获取密钥"""
        return self._key
    
    def brute_force_decrypt(self, data: bytes, 
                            top_n: int = 10) -> List[Tuple[int, bytes, float]]:
        """
        暴力破解并返回可能的明文
        
        Args:
            data: 密文
            top_n: 返回前 N 个结果
        
        Returns:
            [(密钥, 解密结果, 置信度), ...]
        """
        guesses = guess_single_byte_key(data)
        results = []
        for key, confidence in guesses[:top_n]:
            decrypted = xor_byte(data, key)
            results.append((key, decrypted, confidence))
        return results


if __name__ == "__main__":
    # 简单演示
    print("XOR Utils 演示")
    print("=" * 50)
    
    # 基础 XOR
    print("\n1. 基础 XOR 操作:")
    data = b"Hello, World!"
    key = 0x55
    encrypted = xor_byte(data, key)
    decrypted = xor_byte(encrypted, key)
    print(f"   原文: {data}")
    print(f"   单字节密钥: {key}")
    print(f"   加密: {encrypted.hex()}")
    print(f"   解密: {decrypted}")
    
    # 多字节 XOR
    print("\n2. 多字节 XOR:")
    key_bytes = b"KEY"
    encrypted2 = xor_bytes(data, key_bytes)
    decrypted2 = xor_bytes(encrypted2, key_bytes)
    print(f"   密钥: {key_bytes}")
    print(f"   加密: {encrypted2.hex()}")
    print(f"   解密: {decrypted2}")
    
    # XOR 校验和
    print("\n3. XOR 校验和:")
    checksum = xor_checksum(data)
    print(f"   XOR 校验和: {checksum}")
    
    # 位操作
    print("\n4. 位操作:")
    print(f"   数据 '{data[:5]}' 的位计数: {count_bits(data[:5])}")
    print(f"   Hamming 距离: {bit_diff(b'Hello', b'Hallo')}")
    
    # 密码分析
    print("\n5. 密码分析:")
    ciphertext = xor_byte(b"Hello World Hello World Hello", 0x55)
    guesses = guess_single_byte_key(ciphertext)[:5]
    print(f"   推测密钥: {[(k, f'{c:.2f}') for k, c in guesses]}")
    
    print("\n" + "=" * 50)
    print("演示完成")