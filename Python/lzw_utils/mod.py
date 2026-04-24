"""
LZW (Lempel-Ziv-Welch) 压缩算法工具库

LZW 是一种基于字典的无损压缩算法，广泛用于 GIF、TIFF、PDF 等格式。
本模块提供完整的 LZW 压缩和解压缩功能，支持字节流和字符串处理。

核心功能：
- compress: 压缩字节数据
- decompress: 解压缩字节数据
- compress_string: 压缩字符串
- decompress_string: 解压缩字符串
- compress_to_hex: 压缩为十六进制字符串
- decompress_from_hex: 从十六进制字符串解压
- get_compression_ratio: 计算压缩率
- LZWEncoder: 编码器类（支持流式编码）
- LZWDecoder: 解码器类（支持流式解码）

特点：
- 零外部依赖，纯 Python 实现
- 支持可变位宽（9-16位）
- 支持提前字典重置
- 内存高效，支持大数据处理
"""

from typing import List, Tuple, Optional, Iterator
import struct


# 默认配置
DEFAULT_MIN_CODE_SIZE = 9
DEFAULT_MAX_CODE_SIZE = 16
INITIAL_DICT_SIZE = 256  # 初始字典大小（0-255 为原始字节）


class LZWEncoder:
    """
    LZW 编码器类
    
    支持流式编码，适用于大文件处理。
    
    示例:
        encoder = LZWEncoder()
        encoder.update(b"hello")
        encoder.update(b" world")
        compressed = encoder.finish()
    """
    
    def __init__(
        self,
        min_code_size: int = DEFAULT_MIN_CODE_SIZE,
        max_code_size: int = DEFAULT_MAX_CODE_SIZE,
        early_change: bool = False
    ):
        """
        初始化编码器
        
        Args:
            min_code_size: 最小代码位宽（默认9位）
            max_code_size: 最大代码位宽（默认16位）
            early_change: 是否在代码达到最大值前提前增加位宽
        """
        self.min_code_size = min_code_size
        self.max_code_size = max_code_size
        self.early_change = early_change
        
        # 初始化字典
        self._reset()
        
    def _reset(self):
        """重置编码器状态"""
        self.dictionary = {bytes([i]): i for i in range(INITIAL_DICT_SIZE)}
        self.next_code = INITIAL_DICT_SIZE
        self.current_code_size = self.min_code_size
        self.max_code = (1 << self.current_code_size) - 1
        
        # 缓冲区
        self._buffer = []
        self._current = b''
        self._bit_buffer = 0
        self._bit_count = 0
        
    def _add_to_dictionary(self, sequence: bytes) -> bool:
        """
        添加新序列到字典
        
        Returns:
            是否成功添加（如果字典已满则返回 False）
        """
        if self.next_code > self.max_code:
            if self.current_code_size < self.max_code_size:
                self.current_code_size += 1
                self.max_code = (1 << self.current_code_size) - 1
            else:
                return False
        
        self.dictionary[sequence] = self.next_code
        self.next_code += 1
        return True
    
    def _write_code(self, code: int) -> None:
        """写入一个代码到位缓冲区"""
        self._bit_buffer |= code << self._bit_count
        self._bit_count += self.current_code_size
        
        while self._bit_count >= 8:
            self._buffer.append(self._bit_buffer & 0xFF)
            self._bit_buffer >>= 8
            self._bit_count -= 8
    
    def update(self, data: bytes) -> None:
        """
        更新编码器数据
        
        Args:
            data: 要编码的字节数据
        """
        for byte in data:
            char = bytes([byte])
            combined = self._current + char
            
            if combined in self.dictionary:
                self._current = combined
            else:
                # 输出当前序列的代码
                self._write_code(self.dictionary[self._current])
                
                # 添加新序列到字典
                if not self._add_to_dictionary(combined):
                    # 字典已满，重置
                    self._reset()
                
                self._current = char
    
    def finish(self) -> bytes:
        """
        完成编码并返回压缩数据
        
        Returns:
            压缩后的字节数据
        """
        # 输出最后的数据
        if self._current:
            self._write_code(self.dictionary[self._current])
        
        # 刷新位缓冲区
        if self._bit_count > 0:
            self._buffer.append(self._bit_buffer & 0xFF)
        
        result = bytes(self._buffer)
        self._reset()
        return result


class LZWDecoder:
    """
    LZW 解码器类
    
    支持流式解码，适用于大文件处理。
    """
    
    def __init__(
        self,
        min_code_size: int = DEFAULT_MIN_CODE_SIZE,
        max_code_size: int = DEFAULT_MAX_CODE_SIZE,
        early_change: bool = False
    ):
        """
        初始化解码器
        
        Args:
            min_code_size: 最小代码位宽（默认9位）
            max_code_size: 最大代码位宽（默认16位）
            early_change: 是否在代码达到最大值前提前增加位宽
        """
        self.min_code_size = min_code_size
        self.max_code_size = max_code_size
        self.early_change = early_change
        self._reset()
    
    def _reset(self):
        """重置解码器状态"""
        self.dictionary = {i: bytes([i]) for i in range(INITIAL_DICT_SIZE)}
        self.next_code = INITIAL_DICT_SIZE
        self.current_code_size = self.min_code_size
        self.max_code = (1 << self.current_code_size) - 1
        
        self._bit_buffer = 0
        self._bit_count = 0
        self._previous = None
    
    def _read_code(self, data: bytes, pos: int) -> Tuple[Optional[int], int]:
        """
        从数据中读取一个代码
        
        Args:
            data: 字节数据
            pos: 当前位置
            
        Returns:
            (代码, 新位置) 或 (None, 原位置) 如果数据不足
        """
        # 填充位缓冲区
        while self._bit_count < self.current_code_size and pos < len(data):
            self._bit_buffer |= data[pos] << self._bit_count
            self._bit_count += 8
            pos += 1
        
        if self._bit_count < self.current_code_size:
            return None, pos
        
        code = self._bit_buffer & ((1 << self.current_code_size) - 1)
        self._bit_buffer >>= self.current_code_size
        self._bit_count -= self.current_code_size
        
        return code, pos
    
    def update(self, data: bytes) -> bytes:
        """
        更新解码器数据
        
        Args:
            data: 要解码的压缩数据
            
        Returns:
            解压后的数据
        """
        result = bytearray()
        pos = 0
        
        while pos < len(data) or self._bit_count >= self.current_code_size:
            code, pos = self._read_code(data, pos)
            if code is None:
                break
            
            if code < INITIAL_DICT_SIZE:
                # 原始字节
                entry = bytes([code])
            elif code in self.dictionary:
                # 已知序列
                entry = self.dictionary[code]
            elif code == self.next_code:
                # 特殊情况：代码尚未添加到字典
                # 此时 entry = previous + previous[0]
                if self._previous is None:
                    raise ValueError(f"无效的 LZW 代码: {code}")
                entry = self._previous + bytes([self._previous[0]])
            else:
                raise ValueError(f"无效的 LZW 代码: {code}")
            
            result.extend(entry)
            
            # 添加新序列到字典
            if self._previous is not None:
                new_entry = self._previous + bytes([entry[0]])
                
                if self.next_code <= self.max_code:
                    self.dictionary[self.next_code] = new_entry
                    self.next_code += 1
                    
                    # 检查是否需要增加位宽
                    if self.next_code > self.max_code and self.current_code_size < self.max_code_size:
                        self.current_code_size += 1
                        self.max_code = (1 << self.current_code_size) - 1
                else:
                    # 字典已满，重置
                    self._reset()
            
            self._previous = entry
        
        return bytes(result)
    
    def finish(self) -> bytes:
        """完成解码"""
        return b''


def compress(
    data: bytes,
    min_code_size: int = DEFAULT_MIN_CODE_SIZE,
    max_code_size: int = DEFAULT_MAX_CODE_SIZE
) -> bytes:
    """
    压缩字节数据
    
    Args:
        data: 要压缩的字节数据
        min_code_size: 最小代码位宽（默认9位）
        max_code_size: 最大代码位宽（默认16位）
        
    Returns:
        压缩后的字节数据
        
    示例:
        >>> original = b"TOBEORNOTTOBEORTOBEORNOT"
        >>> compressed = compress(original)
        >>> len(compressed) < len(original)
        True
    """
    if not data:
        return b''
    
    encoder = LZWEncoder(min_code_size, max_code_size)
    encoder.update(data)
    return encoder.finish()


def decompress(
    data: bytes,
    min_code_size: int = DEFAULT_MIN_CODE_SIZE,
    max_code_size: int = DEFAULT_MAX_CODE_SIZE
) -> bytes:
    """
    解压缩字节数据
    
    Args:
        data: 压缩数据
        min_code_size: 最小代码位宽（默认9位）
        max_code_size: 最大代码位宽（默认16位）
        
    Returns:
        解压后的原始数据
        
    Raises:
        ValueError: 如果压缩数据无效
        
    示例:
        >>> original = b"TOBEORNOTTOBEORTOBEORNOT"
        >>> compressed = compress(original)
        >>> decompress(compressed) == original
        True
    """
    if not data:
        return b''
    
    decoder = LZWDecoder(min_code_size, max_code_size)
    return decoder.update(data)


def compress_string(text: str, encoding: str = 'utf-8') -> bytes:
    """
    压缩字符串
    
    Args:
        text: 要压缩的字符串
        encoding: 字符编码（默认 utf-8）
        
    Returns:
        压缩后的字节数据
        
    示例:
        >>> text = "Hello, World! " * 100
        >>> compressed = compress_string(text)
        >>> len(compressed) < len(text.encode())
        True
    """
    return compress(text.encode(encoding))


def decompress_string(data: bytes, encoding: str = 'utf-8') -> str:
    """
    解压缩为字符串
    
    Args:
        data: 压缩数据
        encoding: 字符编码（默认 utf-8）
        
    Returns:
        解压后的字符串
        
    示例:
        >>> text = "Hello, World! " * 100
        >>> compressed = compress_string(text)
        >>> decompress_string(compressed) == text
        True
    """
    return decompress(data).decode(encoding)


def compress_to_hex(data: bytes) -> str:
    """
    压缩数据并返回十六进制字符串
    
    Args:
        data: 要压缩的字节数据
        
    Returns:
        十六进制字符串
        
    示例:
        >>> original = b"ABABABABAB"
        >>> hex_str = compress_to_hex(original)
        >>> isinstance(hex_str, str)
        True
    """
    compressed = compress(data)
    return compressed.hex()


def decompress_from_hex(hex_str: str) -> bytes:
    """
    从十六进制字符串解压数据
    
    Args:
        hex_str: 十六进制字符串
        
    Returns:
        解压后的原始数据
        
    示例:
        >>> original = b"ABABABABAB"
        >>> hex_str = compress_to_hex(original)
        >>> decompress_from_hex(hex_str) == original
        True
    """
    return decompress(bytes.fromhex(hex_str))


def get_compression_ratio(original: bytes, compressed: bytes) -> float:
    """
    计算压缩率
    
    Args:
        original: 原始数据
        compressed: 压缩数据
        
    Returns:
        压缩率（0-1，越小表示压缩效果越好）
        
    示例:
        >>> original = b"A" * 1000
        >>> compressed = compress(original)
        >>> ratio = get_compression_ratio(original, compressed)
        >>> ratio < 1
        True
    """
    if not original:
        return 0.0
    return len(compressed) / len(original)


def get_compression_stats(original: bytes, compressed: bytes) -> dict:
    """
    获取压缩统计信息
    
    Args:
        original: 原始数据
        compressed: 压缩数据
        
    Returns:
        包含统计信息的字典
        
    示例:
        >>> original = b"TOBEORNOTTOBEORTOBEORNOT" * 10
        >>> compressed = compress(original)
        >>> stats = get_compression_stats(original, compressed)
        >>> stats['ratio'] < 1
        True
    """
    ratio = get_compression_ratio(original, compressed)
    return {
        'original_size': len(original),
        'compressed_size': len(compressed),
        'ratio': ratio,
        'saved_bytes': len(original) - len(compressed),
        'saved_percent': (1 - ratio) * 100,
        'is_efficient': ratio < 1
    }


def compress_stream(
    data: bytes,
    chunk_size: int = 8192
) -> Iterator[bytes]:
    """
    流式压缩（生成器版本）
    
    适用于大数据压缩，减少内存使用。
    
    Args:
        data: 要压缩的数据
        chunk_size: 每次处理的块大小
        
    Yields:
        压缩后的数据块
        
    示例:
        >>> data = b"Hello, World! " * 10000
        >>> result = b''.join(compress_stream(data))
        >>> decompress(result) == data
        True
    """
    encoder = LZWEncoder()
    
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        encoder.update(chunk)
    
    yield encoder.finish()


# GIF 格式兼容的 LZW 压缩
def compress_gif(data: bytes, min_code_size: int = 8) -> bytes:
    """
    GIF 格式兼容的 LZW 压缩
    
    GIF 使用特殊的 LZW 变体：
    - 位宽从 min_code_size + 1 开始
    - 有清零代码和结束代码
    
    Args:
        data: 要压缩的数据
        min_code_size: 最小代码位宽（GIF 通常为 8）
        
    Returns:
        GIF 格式压缩数据
    """
    if not data:
        return b''
    
    # GIF 使用 min_code_size + 1 作为起始位宽
    code_size = min_code_size + 1
    clear_code = 1 << min_code_size
    end_code = clear_code + 1
    
    # 初始化字典
    dictionary = {bytes([i]): i for i in range(clear_code)}
    next_code = end_code + 1
    max_code = (1 << code_size) - 1
    
    # 输出缓冲区
    output = bytearray()
    bit_buffer = 0
    bit_count = 0
    
    def write_code(code: int):
        nonlocal bit_buffer, bit_count, code_size, max_code, next_code, dictionary
        
        bit_buffer |= code << bit_count
        bit_count += code_size
        
        while bit_count >= 8:
            output.append(bit_buffer & 0xFF)
            bit_buffer >>= 8
            bit_count -= 8
    
    # 写入清零代码
    write_code(clear_code)
    
    current = b''
    for byte in data:
        char = bytes([byte])
        combined = current + char
        
        if combined in dictionary:
            current = combined
        else:
            write_code(dictionary[current])
            
            if next_code <= 4095:  # GIF 最大代码
                dictionary[combined] = next_code
                next_code += 1
                
                # 在添加新代码后检查是否需要增加位宽
                if next_code > max_code and code_size < 12:
                    code_size += 1
                    max_code = (1 << code_size) - 1
            else:
                # 字典已满，重新初始化
                write_code(clear_code)
                dictionary = {bytes([i]): i for i in range(clear_code)}
                next_code = end_code + 1
                code_size = min_code_size + 1
                max_code = (1 << code_size) - 1
            
            current = char
    
    if current:
        write_code(dictionary[current])
    
    # 写入结束代码
    write_code(end_code)
    
    # 刷新剩余位
    if bit_count > 0:
        output.append(bit_buffer & 0xFF)
    
    return bytes(output)


def decompress_gif(data: bytes, min_code_size: int = 8) -> bytes:
    """
    GIF 格式兼容的 LZW 解压
    
    Args:
        data: GIF 格式压缩数据
        min_code_size: 最小代码位宽（GIF 通常为 8）
        
    Returns:
        解压后的原始数据
    """
    if not data:
        return b''
    
    code_size = min_code_size + 1
    clear_code = 1 << min_code_size
    end_code = clear_code + 1
    
    # 初始化字典
    dictionary = {i: bytes([i]) for i in range(clear_code)}
    next_code = end_code + 1
    max_code = (1 << code_size) - 1
    
    # 位读取
    bit_buffer = 0
    bit_count = 0
    byte_pos = 0
    
    def read_code():
        nonlocal bit_buffer, bit_count, byte_pos, code_size
        
        while bit_count < code_size and byte_pos < len(data):
            bit_buffer |= data[byte_pos] << bit_count
            bit_count += 8
            byte_pos += 1
        
        if bit_count < code_size:
            return None
        
        code = bit_buffer & ((1 << code_size) - 1)
        bit_buffer >>= code_size
        bit_count -= code_size
        
        return code
    
    output = bytearray()
    previous = None
    
    while True:
        code = read_code()
        if code is None:
            break
        
        if code == clear_code:
            # 清零代码，重置字典
            dictionary = {i: bytes([i]) for i in range(clear_code)}
            next_code = end_code + 1
            code_size = min_code_size + 1
            max_code = (1 << code_size) - 1
            previous = None
            continue
        
        if code == end_code:
            break
        
        if code < next_code:
            if code in dictionary:
                entry = dictionary[code]
            else:
                raise ValueError(f"无效代码: {code}")
        elif code == next_code:
            # 特殊情况：解码器看到新代码，但字典中还没有
            # 此时 entry = previous + previous[0]
            if previous is None:
                raise ValueError(f"无效的 LZW 序列")
            entry = previous + bytes([previous[0]])
        else:
            raise ValueError(f"无效代码: {code} (next_code={next_code})")
        
        output.extend(entry)
        
        if previous is not None and next_code <= 4095:
            dictionary[next_code] = previous + bytes([entry[0]])
            next_code += 1
            
            # 在添加新代码后检查是否需要增加位宽
            if next_code > max_code and code_size < 12:
                code_size += 1
                max_code = (1 << code_size) - 1
        
        previous = entry
    
    return bytes(output)


if __name__ == '__main__':
    # 简单测试
    test_data = b"TOBEORNOTTOBEORTOBEORNOT" * 10
    compressed = compress(test_data)
    decompressed = decompress(compressed)
    
    print(f"原始大小: {len(test_data)} 字节")
    print(f"压缩后: {len(compressed)} 字节")
    print(f"压缩率: {get_compression_ratio(test_data, compressed):.2%}")
    print(f"验证: {test_data == decompressed}")