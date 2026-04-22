"""
RLE (Run-Length Encoding) Utilities - 游程编码工具

提供完整的游程编码实现，包括：
- 基本游程编码/解码
- 可配置的最小运行长度
- 支持字符串和字节序列
- 多种编码格式输出
- 高效的流式处理

零外部依赖，纯 Python 实现。
"""

from typing import Union, List, Tuple, Iterator, Optional
from dataclasses import dataclass


@dataclass
class RLERun:
    """表示一个游程（连续相同元素的序列）"""
    value: Union[str, int, bytes]
    count: int
    
    def __repr__(self) -> str:
        return f"RLERun(value={self.value!r}, count={self.count})"


class RLEEncoder:
    """
    游程编码器
    
    将连续重复的元素压缩为 (值, 计数) 对。
    支持字符串、字节序列和任意可迭代对象。
    """
    
    def __init__(self, min_run_length: int = 2, max_count: int = None):
        """
        初始化编码器
        
        Args:
            min_run_length: 最小游程长度，小于此长度的重复序列不编码
            max_count: 单次编码的最大计数（用于某些格式限制）
        """
        if min_run_length < 2:
            raise ValueError("min_run_length must be at least 2")
        self.min_run_length = min_run_length
        self.max_count = max_count or float('inf')
    
    def encode_string(self, data: str) -> List[RLERun]:
        """
        编码字符串
        
        Args:
            data: 输入字符串
            
        Returns:
            游程列表
            
        Example:
            >>> encoder = RLEEncoder()
            >>> encoder.encode_string("AAABBC")
            [RLERun(value='A', count=3), RLERun(value='B', count=2), RLERun(value='C', count=1)]
        
        Note:
            优化版本：添加单字符快速路径，
            边界处理：空输入返回空列表。
        """
        # 边界处理：空输入快速返回
        if not data:
            return []
        
        # 快速路径：单字符直接返回
        if len(data) == 1:
            return [RLERun(value=data[0], count=1)]
        
        runs: List[RLERun] = []
        current_char = data[0]
        count = 1
        
        for char in data[1:]:
            if char == current_char and count < self.max_count:
                count += 1
            else:
                runs.append(RLERun(value=current_char, count=count))
                current_char = char
                count = 1
        
        runs.append(RLERun(value=current_char, count=count))
        return runs
    
    def encode_bytes(self, data: bytes) -> List[RLERun]:
        """
        编码字节序列
        
        Args:
            data: 输入字节序列
            
        Returns:
            游程列表
            
        Example:
            >>> encoder = RLEEncoder()
            >>> encoder.encode_bytes(b'\\x00\\x00\\x00\\xFF\\xFF')
            [RLERun(value=0, count=3), RLERun(value=255, count=2)]
        """
        if not data:
            return []
        
        runs: List[RLERun] = []
        current_byte = data[0]
        count = 1
        
        for byte in data[1:]:
            if byte == current_byte and count < self.max_count:
                count += 1
            else:
                runs.append(RLERun(value=current_byte, count=count))
                current_byte = byte
                count = 1
        
        runs.append(RLERun(value=current_byte, count=count))
        return runs
    
    def encode_iterable(self, data: Iterator) -> List[RLERun]:
        """
        编码任意可迭代对象
        
        Args:
            data: 输入可迭代对象
            
        Returns:
            游程列表
        """
        iterator = iter(data)
        try:
            current = next(iterator)
        except StopIteration:
            return []
        
        runs: List[RLERun] = []
        count = 1
        
        for item in iterator:
            if item == current and count < self.max_count:
                count += 1
            else:
                runs.append(RLERun(value=current, count=count))
                current = item
                count = 1
        
        runs.append(RLERun(value=current, count=count))
        return runs
    
    def encode_to_tuples(self, data: Union[str, bytes, Iterator]) -> List[Tuple]:
        """
        编码为元组列表格式
        
        Args:
            data: 输入数据（字符串、字节序列或可迭代对象）
            
        Returns:
            (值, 计数) 元组列表
        """
        if isinstance(data, str):
            runs = self.encode_string(data)
        elif isinstance(data, bytes):
            runs = self.encode_bytes(data)
        else:
            runs = self.encode_iterable(data)
        
        return [(run.value, run.count) for run in runs]
    
    def encode_compact(self, data: str) -> str:
        """
        编码为紧凑字符串格式
        
        格式：对于游程长度 >= min_run_length 的，编码为 "计数+字符"，
              否则原样输出字符。
        
        Args:
            data: 输入字符串
            
        Returns:
            紧凑编码字符串
            
        Example:
            >>> encoder = RLEEncoder(min_run_length=2)
            >>> encoder.encode_compact("AAABBCDDD")
            '3A2BC3D'
        """
        runs = self.encode_string(data)
        result = []
        
        for run in runs:
            if run.count >= self.min_run_length:
                result.append(f"{run.count}{run.value}")
            else:
                result.append(run.value * run.count)
        
        return ''.join(result)
    
    def encode_bytes_packed(self, data: bytes) -> bytes:
        """
        编码字节序列为打包格式
        
        格式：每个游程编码为 [计数-1, 字节值] 对（计数最大 256）
        注意：计数为 0 表示 1，计数为 255 表示 256
        
        Args:
            data: 输入字节序列
            
        Returns:
            打包编码字节
            
        Example:
            >>> encoder = RLEEncoder()
            >>> encoder.encode_bytes_packed(b'\\x00\\x00\\x00\\xFF')
            b'\\x02\\x00\\x00\\xFF'  # 3个0, 1个255
        """
        runs = self.encode_bytes(data)
        result = bytearray()
        
        for run in runs:
            remaining = run.count
            value = run.value
            
            while remaining > 0:
                # 每次最多编码 256 个
                count = min(remaining, 256)
                result.append(count - 1)  # 0 表示 1，255 表示 256
                result.append(value)
                remaining -= count
        
        return bytes(result)


class RLEDecoder:
    """
    游程解码器
    
    将游程编码数据解码还原。
    """
    
    def decode_string(self, runs: List[RLERun]) -> str:
        """
        解码字符串游程
        
        Args:
            runs: 游程列表
            
        Returns:
            解码后的字符串
        """
        return ''.join(run.value * run.count for run in runs)
    
    def decode_bytes(self, runs: List[RLERun]) -> bytes:
        """
        解码字节序列游程
        
        Args:
            runs: 游程列表
            
        Returns:
            解码后的字节序列
        """
        result = bytearray()
        for run in runs:
            result.extend([run.value] * run.count)
        return bytes(result)
    
    def decode_tuples(self, tuples: List[Tuple], as_bytes: bool = False) -> Union[str, bytes]:
        """
        解码元组列表
        
        Args:
            tuples: (值, 计数) 元组列表
            as_bytes: 是否输出字节序列
            
        Returns:
            解码后的数据
        """
        runs = [RLERun(value=v, count=c) for v, c in tuples]
        if as_bytes:
            return self.decode_bytes(runs)
        return self.decode_string(runs)
    
    def decode_compact(self, data: str) -> str:
        """
        解码紧凑字符串格式
        
        Args:
            data: 紧凑编码字符串
            
        Returns:
            解码后的字符串
            
        Example:
            >>> decoder = RLEDecoder()
            >>> decoder.decode_compact('3A2BC3D')
            'AAABBCDDD'
        """
        result = []
        i = 0
        n = len(data)
        
        while i < n:
            # 读取计数（可能有多位数字）
            count_str = ''
            while i < n and data[i].isdigit():
                count_str += data[i]
                i += 1
            
            if i >= n:
                break
            
            char = data[i]
            i += 1
            
            if count_str:
                count = int(count_str)
                result.append(char * count)
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decode_bytes_packed(self, data: bytes) -> bytes:
        """
        解码打包字节格式
        
        Args:
            data: 打包编码字节
            
        Returns:
            解码后的字节序列
        """
        result = bytearray()
        i = 0
        n = len(data)
        
        while i + 1 < n:
            count = data[i] + 1  # 0 表示 1
            value = data[i + 1]
            result.extend([value] * count)
            i += 2
        
        return bytes(result)


class RLE:
    """
    游程编码高级接口
    
    提供简化的静态方法进行编码和解码。
    """
    
    @staticmethod
    def encode(data: Union[str, bytes, Iterator], min_run_length: int = 2) -> List[Tuple]:
        """
        编码数据
        
        Args:
            data: 输入数据
            min_run_length: 最小游程长度
            
        Returns:
            (值, 计数) 元组列表
            
        Example:
            >>> RLE.encode("AAABBC")
            [('A', 3), ('B', 2), ('C', 1)]
        """
        encoder = RLEEncoder(min_run_length=min_run_length)
        return encoder.encode_to_tuples(data)
    
    @staticmethod
    def decode(tuples: List[Tuple], as_bytes: bool = False) -> Union[str, bytes]:
        """
        解码数据
        
        Args:
            tuples: (值, 计数) 元组列表
            as_bytes: 是否输出字节序列
            
        Returns:
            解码后的数据
            
        Example:
            >>> RLE.decode([('A', 3), ('B', 2), ('C', 1)])
            'AAABBC'
        """
        decoder = RLEDecoder()
        return decoder.decode_tuples(tuples, as_bytes=as_bytes)
    
    @staticmethod
    def encode_compact(data: str, min_run_length: int = 2) -> str:
        """
        编码为紧凑字符串
        
        Args:
            data: 输入字符串
            min_run_length: 最小游程长度
            
        Returns:
            紧凑编码字符串
        """
        encoder = RLEEncoder(min_run_length=min_run_length)
        return encoder.encode_compact(data)
    
    @staticmethod
    def decode_compact(data: str) -> str:
        """
        解码紧凑字符串
        
        Args:
            data: 紧凑编码字符串
            
        Returns:
            解码后的字符串
        """
        decoder = RLEDecoder()
        return decoder.decode_compact(data)
    
    @staticmethod
    def encode_bytes(data: bytes) -> bytes:
        """
        编码字节序列为打包格式
        
        Args:
            data: 输入字节序列
            
        Returns:
            打包编码字节
        """
        encoder = RLEEncoder()
        return encoder.encode_bytes_packed(data)
    
    @staticmethod
    def decode_bytes(data: bytes) -> bytes:
        """
        解码打包字节格式
        
        Args:
            data: 打包编码字节
            
        Returns:
            解码后的字节序列
        """
        decoder = RLEDecoder()
        return decoder.decode_bytes_packed(data)
    
    @staticmethod
    def compress_ratio(original: Union[str, bytes], encoded: Union[str, bytes, List]) -> float:
        """
        计算压缩比
        
        Args:
            original: 原始数据
            encoded: 编码后数据
            
        Returns:
            压缩比（原始大小 / 编码后大小）
        """
        original_size = len(original)
        if isinstance(encoded, list):
            # 元组列表格式，估算大小
            encoded_size = sum(2 for _ in encoded)  # 每个元组约2个单元
        else:
            encoded_size = len(encoded)
        
        if encoded_size == 0:
            return 0.0
        
        return original_size / encoded_size
    
    @staticmethod
    def analyze(data: Union[str, bytes]) -> dict:
        """
        分析数据的游程特征
        
        Args:
            data: 输入数据
            
        Returns:
            分析结果字典，包含：
            - total_runs: 总游程数
            - max_run_length: 最大游程长度
            - avg_run_length: 平均游程长度
            - compression_potential: 压缩潜力（0-1）
            - run_distribution: 游程长度分布
        """
        if isinstance(data, str):
            encoder = RLEEncoder()
            runs = encoder.encode_string(data)
        else:
            encoder = RLEEncoder()
            runs = encoder.encode_bytes(data)
        
        if not runs:
            return {
                'total_runs': 0,
                'max_run_length': 0,
                'avg_run_length': 0.0,
                'compression_potential': 0.0,
                'run_distribution': {}
            }
        
        run_lengths = [run.count for run in runs]
        total_length = sum(run_lengths)
        max_run = max(run_lengths)
        avg_run = total_length / len(runs)
        
        # 计算压缩潜力：被压缩的字符比例
        compressible = sum(length for length in run_lengths if length >= 2)
        compression_potential = compressible / total_length if total_length > 0 else 0
        
        # 游程长度分布
        distribution = {}
        for length in run_lengths:
            distribution[length] = distribution.get(length, 0) + 1
        
        return {
            'total_runs': len(runs),
            'max_run_length': max_run,
            'avg_run_length': round(avg_run, 2),
            'compression_potential': round(compression_potential, 2),
            'run_distribution': distribution
        }


class StreamingRLEEncoder:
    """
    流式游程编码器
    
    支持分块处理大型数据，适用于流式场景。
    """
    
    def __init__(self, min_run_length: int = 2):
        """
        初始化流式编码器
        
        Args:
            min_run_length: 最小游程长度
        """
        self.min_run_length = min_run_length
        self._buffer: List = []
        self._current_value = None
        self._current_count = 0
        self._completed_runs: List[RLERun] = []
    
    def feed(self, data: Union[str, bytes, Iterator]) -> List[RLERun]:
        """
        输入数据块
        
        Args:
            data: 输入数据块
            
        Returns:
            已完成的游程列表（可能有延迟）
        """
        completed = []
        
        if isinstance(data, str):
            iterable = data
        elif isinstance(data, bytes):
            iterable = data
        else:
            iterable = data
        
        for item in iterable:
            if self._current_value is None:
                self._current_value = item
                self._current_count = 1
            elif item == self._current_value:
                self._current_count += 1
            else:
                # 游程结束
                run = RLERun(value=self._current_value, count=self._current_count)
                completed.append(run)
                self._current_value = item
                self._current_count = 1
        
        self._completed_runs.extend(completed)
        return completed
    
    def flush(self) -> Optional[RLERun]:
        """
        刷新缓冲区，返回最后一个游程
        
        Returns:
            最后的游程（如果有）
        """
        if self._current_value is not None and self._current_count > 0:
            run = RLERun(value=self._current_value, count=self._current_count)
            self._current_value = None
            self._current_count = 0
            return run
        return None
    
    def reset(self):
        """重置编码器状态"""
        self._current_value = None
        self._current_count = 0
        self._completed_runs.clear()


# 便捷函数
def rle_encode(data: Union[str, bytes], min_run_length: int = 2) -> List[Tuple]:
    """便捷编码函数"""
    return RLE.encode(data, min_run_length)


def rle_decode(tuples: List[Tuple], as_bytes: bool = False) -> Union[str, bytes]:
    """便捷解码函数"""
    return RLE.decode(tuples, as_bytes)


def rle_compress(data: str) -> str:
    """便捷紧凑编码函数"""
    return RLE.encode_compact(data)


def rle_decompress(data: str) -> str:
    """便捷紧凑解码函数"""
    return RLE.decode_compact(data)


if __name__ == "__main__":
    # 简单演示
    print("=== RLE 编码演示 ===")
    
    # 字符串编码
    text = "AAABBBCCCCDD"
    encoded = rle_encode(text)
    print(f"原文: {text}")
    print(f"编码: {encoded}")
    print(f"解码: {rle_decode(encoded)}")
    
    # 紧凑格式
    compact = rle_compress(text)
    print(f"紧凑编码: {compact}")
    print(f"紧凑解码: {rle_decompress(compact)}")
    
    # 字节编码
    data = bytes([0, 0, 0, 255, 255, 128])
    encoded_bytes = RLE.encode_bytes(data)
    print(f"\n字节编码: {data.hex()} -> {encoded_bytes.hex()}")
    print(f"字节解码: {RLE.decode_bytes(encoded_bytes).hex()}")
    
    # 分析
    analysis = RLE.analyze("AAABBBCCCCDD")
    print(f"\n数据分析: {analysis}")