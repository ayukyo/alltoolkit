"""
LZ77 Compression Utils - LZ77 压缩算法工具

零依赖的 LZ77 压缩/解压缩实现。LZ77 是一种基于滑动窗口的无损压缩算法，
是 DEFLATE、gzip、PNG 等格式的基础。

Features:
- LZ77 压缩和解压缩
- 可配置的窗口大小和前瞻缓冲区
- 支持字符串和字节数据
- 令牌表示和分析
- 压缩率计算
- 流式处理支持
- 零外部依赖，纯 Python 实现
"""

from dataclasses import dataclass
from typing import List, Tuple, Union, Iterator, Optional
from enum import Enum


class TokenType(Enum):
    """令牌类型枚举"""
    LITERAL = "literal"      # 字面量（单个字符/字节）
    MATCH = "match"         # 匹配（从窗口复制）


@dataclass
class LZ77Token:
    """
    LZ77 令牌
    
    对于字面量：offset=0, length=0, value=字符/字节
    对于匹配：offset=回溯距离, length=匹配长度, value=None
    """
    offset: int         # 回溯距离（0 表示字面量）
    length: int         # 匹配长度（0 表示字面量）
    value: Optional[Union[str, int]] = None  # 字面量值
    
    @property
    def is_literal(self) -> bool:
        """是否为字面量令牌"""
        return self.offset == 0 and self.length == 0
    
    @property
    def is_match(self) -> bool:
        """是否为匹配令牌"""
        return self.length > 0
    
    def __repr__(self) -> str:
        if self.is_literal:
            v = self.value if isinstance(self.value, int) else repr(self.value)
            return f"LZ77Token(literal={v})"
        return f"LZ77Token(offset={self.offset}, length={self.length})"
    
    def to_tuple(self) -> Tuple[int, int, Optional[Union[str, int]]]:
        """转换为元组格式 (offset, length, value)"""
        return (self.offset, self.length, self.value)
    
    @classmethod
    def literal(cls, value: Union[str, int]) -> 'LZ77Token':
        """创建字面量令牌"""
        return cls(offset=0, length=0, value=value)
    
    @classmethod
    def match(cls, offset: int, length: int) -> 'LZ77Token':
        """创建匹配令牌"""
        return cls(offset=offset, length=length, value=None)


@dataclass
class LZ77Result:
    """LZ77 压缩结果"""
    tokens: List[LZ77Token]         # 令牌列表
    original_size: int               # 原始数据大小（字节）
    compressed_size: int             # 压缩后大小（估算）
    literal_count: int                # 字面量数量
    match_count: int                  # 匹配令牌数量
    window_size: int                  # 窗口大小
    min_match_length: int             # 最小匹配长度
    
    @property
    def compression_ratio(self) -> float:
        """压缩率（原始/压缩）"""
        if self.compressed_size == 0:
            return 0.0
        return self.original_size / self.compressed_size
    
    @property
    def space_saving(self) -> float:
        """空间节省百分比"""
        if self.original_size == 0:
            return 0.0
        return (1 - self.compressed_size / self.original_size) * 100
    
    @property
    def total_tokens(self) -> int:
        """总令牌数"""
        return len(self.tokens)
    
    @property
    def match_ratio(self) -> float:
        """匹配令牌占比"""
        if self.total_tokens == 0:
            return 0.0
        return self.match_count / self.total_tokens


class LZ77Encoder:
    """
    LZ77 编码器
    
    使用滑动窗口方法进行数据压缩。窗口分为两部分：
    - 搜索窗口（已编码数据，用于查找匹配）
    - 前瞻缓冲区（待编码数据）
    
    Args:
        window_size: 搜索窗口大小（默认 4096）
        look_ahead_size: 前瞻缓冲区大小（默认 18）
        min_match_length: 最小匹配长度（默认 3）
    """
    
    # 常用配置预设
    PRESETS = {
        'fast': {'window_size': 1024, 'look_ahead_size': 15, 'min_match_length': 3},
        'balanced': {'window_size': 4096, 'look_ahead_size': 18, 'min_match_length': 3},
        'maximum': {'window_size': 32768, 'look_ahead_size': 258, 'min_match_length': 3},
        'small': {'window_size': 256, 'look_ahead_size': 15, 'min_match_length': 2},
    }
    
    def __init__(
        self,
        window_size: int = 4096,
        look_ahead_size: int = 18,
        min_match_length: int = 3
    ):
        if window_size < 1:
            raise ValueError("window_size must be at least 1")
        if look_ahead_size < 1:
            raise ValueError("look_ahead_size must be at least 1")
        if min_match_length < 2:
            raise ValueError("min_match_length must be at least 2")
        if min_match_length > look_ahead_size:
            raise ValueError("min_match_length cannot exceed look_ahead_size")
        
        self.window_size = window_size
        self.look_ahead_size = look_ahead_size
        self.min_match_length = min_match_length
    
    @classmethod
    def from_preset(cls, preset: str) -> 'LZ77Encoder':
        """从预设创建编码器"""
        if preset not in cls.PRESETS:
            raise ValueError(f"Unknown preset: {preset}. Available: {list(cls.PRESETS.keys())}")
        return cls(**cls.PRESETS[preset])
    
    def encode(self, data: Union[str, bytes]) -> LZ77Result:
        """
        编码数据
        
        Args:
            data: 输入数据（字符串或字节）
        
        Returns:
            LZ77Result: 压缩结果
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        tokens: List[LZ77Token] = []
        pos = 0
        n = len(data)
        literal_count = 0
        match_count = 0
        compressed_size = 0
        
        while pos < n:
            # 计算窗口边界
            window_start = max(0, pos - self.window_size)
            look_ahead_end = min(n, pos + self.look_ahead_size)
            
            # 查找最长匹配
            best_offset, best_length = self._find_longest_match(
                data, window_start, pos, look_ahead_end
            )
            
            if best_length >= self.min_match_length:
                # 找到匹配，输出匹配令牌
                token = LZ77Token.match(best_offset, best_length)
                tokens.append(token)
                match_count += 1
                # 估算压缩大小：(offset, length) 对大约占用 2-3 字节
                compressed_size += self._estimate_match_size(best_offset, best_length)
                pos += best_length
            else:
                # 没有足够长的匹配，输出字面量
                token = LZ77Token.literal(data[pos])
                tokens.append(token)
                literal_count += 1
                compressed_size += 1  # 字面量占 1 字节
                pos += 1
        
        return LZ77Result(
            tokens=tokens,
            original_size=n,
            compressed_size=compressed_size,
            literal_count=literal_count,
            match_count=match_count,
            window_size=self.window_size,
            min_match_length=self.min_match_length
        )
    
    def _find_longest_match(
        self,
        data: bytes,
        window_start: int,
        pos: int,
        look_ahead_end: int
    ) -> Tuple[int, int]:
        """
        在窗口中查找最长匹配
        
        Returns:
            (offset, length): offset=回溯距离, length=匹配长度
        """
        best_offset = 0
        best_length = 0
        
        # 从当前位置向前搜索
        search_start = max(window_start, 0)
        
        for i in range(pos - 1, search_start - 1, -1):
            offset = pos - i
            if offset > self.window_size:
                break
            
            # 计算匹配长度
            length = 0
            max_length = min(look_ahead_end - pos, self.look_ahead_size)
            
            while (length < max_length and 
                   pos + length < len(data) and
                   data[i + (length % (pos - i))] == data[pos + length]):
                length += 1
            
            if length > best_length:
                best_length = length
                best_offset = offset
                
                # 如果达到最大可能长度，提前退出
                if best_length >= max_length:
                    break
        
        return best_offset, best_length
    
    def _estimate_match_size(self, offset: int, length: int) -> int:
        """估算匹配令牌的编码大小"""
        # 简单估算：offset 和 length 各需要一定位数
        # 实际编码中，这取决于具体的位打包方式
        offset_bits = (offset.bit_length() + 7) // 8
        length_bits = (length.bit_length() + 7) // 8
        return max(1, offset_bits + length_bits)
    
    def encode_to_tuples(self, data: Union[str, bytes]) -> List[Tuple[int, int, Optional[int]]]:
        """
        编码为元组列表格式
        
        Returns:
            [(offset, length, literal), ...]
            - 字面量: (0, 0, literal_value)
            - 匹配: (offset, length, None)
        """
        result = self.encode(data)
        return [t.to_tuple() for t in result.tokens]
    
    def encode_iter(self, data: Union[str, bytes]) -> Iterator[LZ77Token]:
        """
        流式编码（生成器）
        
        Yields:
            LZ77Token: 逐个输出令牌
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        pos = 0
        n = len(data)
        
        while pos < n:
            window_start = max(0, pos - self.window_size)
            look_ahead_end = min(n, pos + self.look_ahead_size)
            
            best_offset, best_length = self._find_longest_match(
                data, window_start, pos, look_ahead_end
            )
            
            if best_length >= self.min_match_length:
                yield LZ77Token.match(best_offset, best_length)
                pos += best_length
            else:
                yield LZ77Token.literal(data[pos])
                pos += 1


class LZ77Decoder:
    """
    LZ77 解码器
    
    将 LZ77 编码的令牌序列还原为原始数据。
    """
    
    def decode(self, tokens: List[LZ77Token]) -> bytes:
        """
        解码令牌列表
        
        Args:
            tokens: LZ77 令牌列表
        
        Returns:
            bytes: 解码后的原始数据
        """
        output = bytearray()
        
        for token in tokens:
            if token.is_literal:
                if isinstance(token.value, int):
                    output.append(token.value)
                elif isinstance(token.value, str):
                    output.extend(token.value.encode('utf-8'))
                else:
                    raise ValueError(f"Invalid literal value: {token.value}")
            else:
                # 匹配：从已解码数据中复制
                if token.offset > len(output):
                    raise ValueError(
                        f"Invalid offset: {token.offset} > buffer size {len(output)}"
                    )
                
                start = len(output) - token.offset
                for i in range(token.length):
                    # 支持重叠复制（offset < length 的情况）
                    output.append(output[start + (i % token.offset)])
        
        return bytes(output)
    
    def decode_to_string(self, tokens: List[LZ77Token], encoding: str = 'utf-8') -> str:
        """
        解码为字符串
        
        Args:
            tokens: LZ77 令牌列表
            encoding: 字符编码（默认 UTF-8）
        
        Returns:
            str: 解码后的字符串
        """
        return self.decode(tokens).decode(encoding)
    
    def decode_tuples(self, tuples: List[Tuple[int, int, Optional[int]]]) -> bytes:
        """
        从元组格式解码
        
        Args:
            tuples: [(offset, length, literal), ...]
        """
        tokens = []
        for offset, length, value in tuples:
            if offset == 0 and length == 0:
                tokens.append(LZ77Token.literal(value))
            else:
                tokens.append(LZ77Token.match(offset, length))
        return self.decode(tokens)


class LZ77Compressor:
    """
    LZ77 压缩器 - 高级接口
    
    提供简单的压缩/解压缩接口，自动处理字符串和字节数据。
    """
    
    def __init__(
        self,
        window_size: int = 4096,
        look_ahead_size: int = 18,
        min_match_length: int = 3
    ):
        self.encoder = LZ77Encoder(window_size, look_ahead_size, min_match_length)
        self.decoder = LZ77Decoder()
    
    @classmethod
    def fast(cls) -> 'LZ77Compressor':
        """快速压缩（较小窗口，较低压缩率）"""
        return cls(**LZ77Encoder.PRESETS['fast'])
    
    @classmethod
    def balanced(cls) -> 'LZ77Compressor':
        """平衡压缩（中等窗口，平衡压缩率和速度）"""
        return cls(**LZ77Encoder.PRESETS['balanced'])
    
    @classmethod
    def maximum(cls) -> 'LZ77Compressor':
        """最大压缩（大窗口，最高压缩率）"""
        return cls(**LZ77Encoder.PRESETS['maximum'])
    
    def compress(self, data: Union[str, bytes]) -> LZ77Result:
        """压缩数据"""
        return self.encoder.encode(data)
    
    def decompress(self, tokens: List[LZ77Token]) -> bytes:
        """解压数据"""
        return self.decoder.decode(tokens)
    
    def decompress_to_string(self, tokens: List[LZ77Token], encoding: str = 'utf-8') -> str:
        """解压为字符串"""
        return self.decoder.decode_to_string(tokens, encoding)
    
    def roundtrip(self, data: Union[str, bytes]) -> Tuple[LZ77Result, bool]:
        """
        执行压缩和解压，验证数据完整性
        
        Returns:
            (压缩结果, 是否成功)
        """
        original = data.encode('utf-8') if isinstance(data, str) else data
        result = self.compress(original)
        decompressed = self.decompress(result.tokens)
        return result, decompressed == original


class StreamingLZ77Encoder:
    """
    流式 LZ77 编码器
    
    支持分块处理大型数据，适用于流式场景。
    """
    
    def __init__(
        self,
        window_size: int = 4096,
        look_ahead_size: int = 18,
        min_match_length: int = 3
    ):
        self.window_size = window_size
        self.look_ahead_size = look_ahead_size
        self.min_match_length = min_match_length
        self.buffer = bytearray()
        self.processed = 0
    
    def feed(self, data: Union[str, bytes]) -> List[LZ77Token]:
        """
        输入数据块，返回产生的令牌
        
        Args:
            data: 输入数据块
        
        Returns:
            本轮产生的令牌列表
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.buffer.extend(data)
        tokens = []
        
        # 处理缓冲区中的数据
        while self.processed + self.min_match_length <= len(self.buffer):
            window_start = max(0, self.processed - self.window_size)
            look_ahead_end = min(len(self.buffer), self.processed + self.look_ahead_size)
            
            # 如果前瞻缓冲区太小，等待更多数据
            if look_ahead_end - self.processed < self.min_match_length:
                break
            
            # 查找匹配
            best_offset, best_length = self._find_longest_match(
                bytes(self.buffer), window_start, self.processed, look_ahead_end
            )
            
            if best_length >= self.min_match_length:
                tokens.append(LZ77Token.match(best_offset, best_length))
                self.processed += best_length
            else:
                tokens.append(LZ77Token.literal(self.buffer[self.processed]))
                self.processed += 1
        
        return tokens
    
    def flush(self) -> List[LZ77Token]:
        """
        刷新剩余数据
        
        Returns:
            剩余的字面量令牌
        """
        tokens = []
        while self.processed < len(self.buffer):
            tokens.append(LZ77Token.literal(self.buffer[self.processed]))
            self.processed += 1
        return tokens
    
    def reset(self):
        """重置编码器状态"""
        self.buffer = bytearray()
        self.processed = 0
    
    def _find_longest_match(
        self,
        data: bytes,
        window_start: int,
        pos: int,
        look_ahead_end: int
    ) -> Tuple[int, int]:
        """查找最长匹配"""
        best_offset = 0
        best_length = 0
        
        search_start = max(window_start, 0)
        
        for i in range(pos - 1, search_start - 1, -1):
            offset = pos - i
            if offset > self.window_size:
                break
            
            length = 0
            max_length = min(look_ahead_end - pos, self.look_ahead_size)
            
            while (length < max_length and 
                   pos + length < len(data) and
                   data[i + (length % (pos - i))] == data[pos + length]):
                length += 1
            
            if length > best_length:
                best_length = length
                best_offset = offset
                if best_length >= max_length:
                    break
        
        return best_offset, best_length


# 便捷函数
def lz77_encode(
    data: Union[str, bytes],
    window_size: int = 4096,
    look_ahead_size: int = 18,
    min_match_length: int = 3
) -> LZ77Result:
    """
    LZ77 编码便捷函数
    
    Args:
        data: 输入数据
        window_size: 窗口大小
        look_ahead_size: 前瞻缓冲区大小
        min_match_length: 最小匹配长度
    
    Returns:
        LZ77Result: 压缩结果
    """
    encoder = LZ77Encoder(window_size, look_ahead_size, min_match_length)
    return encoder.encode(data)


def lz77_decode(tokens: List[LZ77Token]) -> bytes:
    """
    LZ77 解码便捷函数
    
    Args:
        tokens: 令牌列表
    
    Returns:
        bytes: 解码后的数据
    """
    decoder = LZ77Decoder()
    return decoder.decode(tokens)


def lz77_decode_to_string(
    tokens: List[LZ77Token],
    encoding: str = 'utf-8'
) -> str:
    """
    LZ77 解码为字符串便捷函数
    """
    decoder = LZ77Decoder()
    return decoder.decode_to_string(tokens, encoding)


def lz77_compress(
    data: Union[str, bytes],
    preset: str = 'balanced'
) -> LZ77Result:
    """
    LZ77 压缩便捷函数（使用预设）
    
    Args:
        data: 输入数据
        preset: 预设名称 ('fast', 'balanced', 'maximum', 'small')
    
    Returns:
        LZ77Result: 压缩结果
    """
    compressor = LZ77Compressor(**LZ77Encoder.PRESETS.get(preset, {}))
    return compressor.compress(data)


def analyze_lz77(data: Union[str, bytes], window_size: int = 4096) -> dict:
    """
    分析 LZ77 压缩特性
    
    Args:
        data: 输入数据
        window_size: 窗口大小
    
    Returns:
        分析结果字典
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    encoder = LZ77Encoder(window_size=window_size)
    result = encoder.encode(data)
    
    # 计算匹配长度分布
    match_lengths = {}
    match_offsets = {}
    for token in result.tokens:
        if token.is_match:
            match_lengths[token.length] = match_lengths.get(token.length, 0) + 1
            match_offsets[token.offset] = match_offsets.get(token.offset, 0) + 1
    
    # 最长匹配
    max_match_length = max(match_lengths.keys()) if match_lengths else 0
    avg_match_length = (
        sum(l * c for l, c in match_lengths.items()) / sum(match_lengths.values())
        if match_lengths else 0
    )
    
    return {
        'original_size': result.original_size,
        'compressed_size': result.compressed_size,
        'compression_ratio': result.compression_ratio,
        'space_saving': result.space_saving,
        'total_tokens': result.total_tokens,
        'literal_count': result.literal_count,
        'match_count': result.match_count,
        'match_ratio': result.match_ratio,
        'max_match_length': max_match_length,
        'avg_match_length': avg_match_length,
        'match_lengths_distribution': dict(sorted(match_lengths.items())),
        'match_offsets_distribution': dict(sorted(match_offsets.items())[:20]),
    }


def compare_presets(data: Union[str, bytes]) -> dict:
    """
    比较不同预设的压缩效果
    
    Args:
        data: 输入数据
    
    Returns:
        各预设的压缩结果对比
    """
    results = {}
    for preset_name, preset_config in LZ77Encoder.PRESETS.items():
        compressor = LZ77Compressor(**preset_config)
        result = compressor.compress(data)
        results[preset_name] = {
            'original_size': result.original_size,
            'compressed_size': result.compressed_size,
            'compression_ratio': result.compression_ratio,
            'space_saving': result.space_saving,
            'literal_count': result.literal_count,
            'match_count': result.match_count,
            'total_tokens': result.total_tokens,
        }
    return results


# 导出公共 API
__all__ = [
    'TokenType',
    'LZ77Token',
    'LZ77Result',
    'LZ77Encoder',
    'LZ77Decoder',
    'LZ77Compressor',
    'StreamingLZ77Encoder',
    'lz77_encode',
    'lz77_decode',
    'lz77_decode_to_string',
    'lz77_compress',
    'analyze_lz77',
    'compare_presets',
]