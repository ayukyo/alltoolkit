"""
Golomb Coding Utilities - Golomb 编码工具

提供完整的 Golomb 编码实现，包括：
- Golomb 编码/解码
- Rice 编码 (Golomb 编码的特例)
- 参数 M 自动计算
- 比特流读写操作
- 有序整数序列压缩
- 与 Delta 编码配合使用

Golomb 编码适用于：
- 压缩有序整数序列 (如倒排索引中的文档 ID)
- 几何分布数据的高效压缩
- 搜索引擎倒排列表压缩
- 数据库索引压缩

零外部依赖，纯 Python 实现。
"""

from typing import List, Tuple, Optional, BinaryIO, Iterator
from dataclasses import dataclass
from math import log2, ceil, floor
import struct


@dataclass
class BitWriter:
    """
    比特写入器
    
    用于将比特流写入字节缓冲区。
    支持写入单个比特、多位整数和一元编码。
    """
    
    buffer: bytearray = None
    current_byte: int = 0
    bit_position: int = 0  # 当前比特位置 (0-7)
    
    def __post_init__(self):
        if self.buffer is None:
            self.buffer = bytearray()
    
    def write_bit(self, bit: int) -> None:
        """
        写入单个比特
        
        Args:
            bit: 0 或 1
        """
        if bit:
            self.current_byte |= (1 << (7 - self.bit_position))
        
        self.bit_position += 1
        
        if self.bit_position == 8:
            self.buffer.append(self.current_byte)
            self.current_byte = 0
            self.bit_position = 0
    
    def write_bits(self, value: int, num_bits: int) -> None:
        """
        写入多比特整数
        
        Args:
            value: 要写入的值
            num_bits: 比特数量
        """
        for i in range(num_bits - 1, -1, -1):
            self.write_bit((value >> i) & 1)
    
    def write_unary(self, value: int) -> None:
        """
        写入一元编码
        
        对于值 n，写入 n 个 0 后跟一个 1
        
        Args:
            value: 要编码的值 (非负整数)
        """
        for _ in range(value):
            self.write_bit(0)
        self.write_bit(1)
    
    def write_gamma(self, value: int) -> None:
        """
        写入 Gamma 编码
        
        Gamma 编码: 使用一元编码表示长度，后跟二进制值
        
        Args:
            value: 要编码的值 (正整数)
        """
        if value < 1:
            raise ValueError("Gamma 编码要求值 >= 1")
        
        # 计算长度
        length = value.bit_length() - 1
        
        # 写入长度的一元编码
        self.write_unary(length)
        
        # 写入值的剩余部分 (不含最高位)
        if length > 0:
            self.write_bits(value, length)
    
    def flush(self) -> bytes:
        """
        刷新并返回字节数据
        
        如果有未完成的字节，用 0 填充剩余比特。
        
        Returns:
            完整的字节数据
        """
        if self.bit_position > 0:
            self.buffer.append(self.current_byte)
        return bytes(self.buffer)
    
    def get_bytes(self) -> bytes:
        """获取当前缓冲区内容 (不刷新)"""
        return bytes(self.buffer)
    
    def reset(self) -> None:
        """重置写入器状态"""
        self.buffer = bytearray()
        self.current_byte = 0
        self.bit_position = 0


@dataclass
class BitReader:
    """
    比特读取器
    
    用于从字节数据中读取比特流。
    支持读取单个比特、多位整数和一元编码。
    """
    
    data: bytes
    byte_position: int = 0
    bit_position: int = 0  # 当前比特位置 (0-7)
    
    def read_bit(self) -> int:
        """
        读取单个比特
        
        Returns:
            0 或 1
            
        Raises:
            EOFError: 数据已读完
        """
        if self.byte_position >= len(self.data):
            raise EOFError("已到达数据末尾")
        
        bit = (self.data[self.byte_position] >> (7 - self.bit_position)) & 1
        
        self.bit_position += 1
        if self.bit_position == 8:
            self.bit_position = 0
            self.byte_position += 1
        
        return bit
    
    def read_bits(self, num_bits: int) -> int:
        """
        读取多比特整数
        
        Args:
            num_bits: 要读取的比特数量
            
        Returns:
            读取的整数值
        """
        value = 0
        for _ in range(num_bits):
            value = (value << 1) | self.read_bit()
        return value
    
    def read_unary(self) -> int:
        """
        读取一元编码
        
        Returns:
            解码后的值
        """
        value = 0
        while self.read_bit() == 0:
            value += 1
        return value
    
    def read_gamma(self) -> int:
        """
        读取 Gamma 编码
        
        Returns:
            解码后的值
        """
        # 读取长度
        length = self.read_unary()
        
        # 读取值的高位 (隐含 1)
        value = 1 << length
        
        # 读取低位
        if length > 0:
            value |= self.read_bits(length)
        
        return value
    
    def has_more(self) -> bool:
        """是否还有未读数据"""
        return self.byte_position < len(self.data)
    
    def reset(self, data: bytes) -> None:
        """重置读取器状态"""
        self.data = data
        self.byte_position = 0
        self.bit_position = 0


class GolombCoding:
    """
    Golomb 编码器
    
    Golomb 编码是一种适用于几何分布数据的压缩编码。
    对于参数 M，将值 N 编码为：
    - 商 q = floor(N / M)，使用一元编码
    - 余数 r = N mod M，使用固定长度二进制编码
    
    当 M 是 2 的幂时，称为 Rice 编码，实现更高效。
    """
    
    def __init__(self, m: int):
        """
        初始化 Golomb 编码器
        
        Args:
            m: 参数 M (必须 > 0)
        """
        if m < 1:
            raise ValueError("参数 M 必须大于 0")
        
        self.m = m
        self._is_power_of_two = (m & (m - 1)) == 0  # Rice 编码优化
        
        if self._is_power_of_two:
            self._log_m = m.bit_length() - 1
    
    @staticmethod
    def optimal_m(values: List[int]) -> int:
        """
        计算最优参数 M
        
        对于几何分布，最优 M 约为 ceil(-1 / log(1 - p))，
        其中 p 是成功概率。对于有序整数序列，可使用平均值近似。
        
        Args:
            values: 要编码的值列表 (非负整数)
            
        Returns:
            推荐的 M 值
        """
        if not values:
            return 1
        
        # 过滤非负值
        non_neg = [v for v in values if v >= 0]
        if not non_neg:
            return 1
        
        # 使用平均值作为几何分布参数的估计
        avg = sum(non_neg) / len(non_neg)
        
        if avg == 0:
            return 1
        
        # 最优 M ≈ 0.69 * avg (对几何分布)
        optimal = ceil(0.69 * avg)
        
        # 向上舍入到最近的 2 的幂 (Rice 编码更高效)
        power = 1
        while power < optimal:
            power <<= 1
        
        return max(1, power)
    
    def encode(self, value: int) -> Tuple[int, int]:
        """
        计算编码的商和余数
        
        Args:
            value: 要编码的值 (非负整数)
            
        Returns:
            (商 q, 余数 r)
        """
        if value < 0:
            raise ValueError("Golomb 编码要求非负整数")
        
        q = value // self.m
        r = value % self.m
        return (q, r)
    
    def decode(self, q: int, r: int) -> int:
        """
        从商和余数解码值
        
        Args:
            q: 商
            r: 余数
            
        Returns:
            解码后的值
        """
        return q * self.m + r
    
    def encode_to_writer(self, writer: BitWriter, value: int) -> None:
        """
        将值编码并写入比特流
        
        Args:
            writer: 比特写入器
            value: 要编码的值
        """
        q, r = self.encode(value)
        
        # 写入商的一元编码
        writer.write_unary(q)
        
        # 写入余数
        if self._is_power_of_two:
            # Rice 编码: 固定长度二进制
            writer.write_bits(r, self._log_m)
        else:
            # 一般 Golomb 编码
            # 使用截断二进制编码
            self._write_truncated_binary(writer, r, self.m)
    
    def decode_from_reader(self, reader: BitReader) -> int:
        """
        从比特流读取并解码值
        
        Args:
            reader: 比特读取器
            
        Returns:
            解码后的值
        """
        # 读取商
        q = reader.read_unary()
        
        # 读取余数
        if self._is_power_of_two:
            r = reader.read_bits(self._log_m)
        else:
            r = self._read_truncated_binary(reader, self.m)
        
        return self.decode(q, r)
    
    def _write_truncated_binary(self, writer: BitWriter, value: int, m: int) -> None:
        """
        写入截断二进制编码
        
        用于编码 0 到 m-1 范围内的值，当 m 不是 2 的幂时更高效。
        """
        b = ceil(log2(m))
        threshold = (1 << b) - m
        
        if value < threshold:
            # 使用 b-1 位
            writer.write_bits(value, b - 1)
        else:
            # 使用 b 位
            writer.write_bits(value + threshold, b)
    
    def _read_truncated_binary(self, reader: BitReader, m: int) -> int:
        """读取截断二进制编码"""
        b = ceil(log2(m))
        threshold = (1 << b) - m
        
        # 读取前 b-1 位
        value = reader.read_bits(b - 1)
        
        if value >= threshold:
            # 需要读取额外的一位
            extra = reader.read_bit()
            value = (value << 1) | extra
            value -= threshold
        
        return value
    
    def encode_sequence(self, values: List[int]) -> bytes:
        """
        编码整数序列
        
        Args:
            values: 非负整数列表
            
        Returns:
            编码后的字节数据
        """
        writer = BitWriter()
        
        for value in values:
            self.encode_to_writer(writer, value)
        
        return writer.flush()
    
    def decode_sequence(self, data: bytes, count: int) -> List[int]:
        """
        解码整数序列
        
        Args:
            data: 编码的字节数据
            count: 要解码的整数数量
            
        Returns:
            解码后的整数列表
        """
        reader = BitReader(data)
        values = []
        
        for _ in range(count):
            values.append(self.decode_from_reader(reader))
        
        return values


class RiceCoding(GolombCoding):
    """
    Rice 编码器
    
    Rice 编码是 Golomb 编码的特例，当 M 是 2 的幂时。
    实现更简单高效，因为余数部分可以直接使用固定长度二进制编码。
    
    常用于：
    - 音频压缩 (FLAC, ALAC)
    - 图像压缩
    - 倒排索引压缩
    """
    
    def __init__(self, k: int):
        """
        初始化 Rice 编码器
        
        Args:
            k: 参数 k，M = 2^k (k >= 0)
        """
        if k < 0:
            raise ValueError("参数 k 必须非负")
        
        self.k = k
        super().__init__(1 << k)  # M = 2^k
    
    @staticmethod
    def optimal_k(values: List[int]) -> int:
        """
        计算最优参数 k
        
        Args:
            values: 要编码的值列表
            
        Returns:
            推荐的 k 值
        """
        if not values:
            return 0
        
        # 过滤非负值
        non_neg = [v for v in values if v >= 0]
        if not non_neg:
            return 0
        
        avg = sum(non_neg) / len(non_neg)
        
        if avg <= 0:
            return 0
        
        # 经验公式
        k = max(0, floor(log2(max(1, avg * 0.69))))
        return k
    
    def encode_to_writer(self, writer: BitWriter, value: int) -> None:
        """
        将值编码并写入比特流 (Rice 优化版本)
        
        Args:
            writer: 比特写入器
            value: 要编码的值
        """
        q, r = self.encode(value)
        
        # 写入商的一元编码
        writer.write_unary(q)
        
        # 写入余数的固定长度二进制 (k 位)
        writer.write_bits(r, self.k)
    
    def decode_from_reader(self, reader: BitReader) -> int:
        """
        从比特流读取并解码值 (Rice 优化版本)
        
        Args:
            reader: 比特读取器
            
        Returns:
            解码后的值
        """
        # 读取商
        q = reader.read_unary()
        
        # 读取余数 (k 位)
        r = reader.read_bits(self.k)
        
        return self.decode(q, r)


class InterleavedGolombCoding:
    """
    交织 Golomb 编码
    
    一种将一元编码和二进制编码交织的方式，
    可以在某些情况下提供更好的压缩效率。
    """
    
    def __init__(self, m: int):
        """
        初始化交织 Golomb 编码器
        
        Args:
            m: 参数 M
        """
        self.m = m
        self._b = ceil(log2(m))
    
    def encode_to_writer(self, writer: BitWriter, value: int) -> None:
        """
        使用交织方式编码
        
        将商和余数的比特交替写入。
        """
        q = value // self.m
        r = value % self.m
        
        # 写入交织的商和余数
        # 先写入商的一元编码 (0 序列)
        for _ in range(q):
            writer.write_bit(0)
        
        # 写入分隔的 1
        writer.write_bit(1)
        
        # 写入余数
        self._write_truncated_binary(writer, r, self.m)
    
    def decode_from_reader(self, reader: BitReader) -> int:
        """使用交织方式解码"""
        # 读取商
        q = reader.read_unary()
        
        # 读取余数
        r = self._read_truncated_binary(reader, self.m)
        
        return q * self.m + r
    
    def _write_truncated_binary(self, writer: BitWriter, value: int, m: int) -> None:
        """写入截断二进制编码"""
        b = self._b
        threshold = (1 << b) - m
        
        if value < threshold:
            writer.write_bits(value, b - 1)
        else:
            writer.write_bits(value + threshold, b)
    
    def _read_truncated_binary(self, reader: BitReader, m: int) -> int:
        """读取截断二进制编码"""
        b = self._b
        threshold = (1 << b) - m
        
        value = reader.read_bits(b - 1)
        
        if value >= threshold:
            extra = reader.read_bit()
            value = (value << 1) | extra
            value -= threshold
        
        return value


class DeltaGolombCompressor:
    """
    Delta + Golomb 压缩器
    
    结合 Delta 编码和 Golomb 编码，
    专门用于压缩有序整数序列。
    
    工作流程：
    1. 对序列应用 Delta 编码 (计算相邻差值)
    2. 对差值应用 Golomb 编码
    
    适用于：
    - 倒排索引中的文档 ID 列表
    - 有序的时间戳序列
    - 递增的主键列表
    """
    
    def __init__(self, m: Optional[int] = None):
        """
        初始化压缩器
        
        Args:
            m: Golomb 参数 M，None 表示自动计算
        """
        self.m = m
    
    @staticmethod
    def delta_encode(values: List[int]) -> List[int]:
        """
        Delta 编码：计算有序序列的差值
        
        Args:
            values: 有序整数序列 (升序)
            
        Returns:
            差值列表 (第一个元素为原值)
        """
        if not values:
            return []
        
        deltas = [values[0]]
        for i in range(1, len(values)):
            delta = values[i] - values[i - 1]
            if delta < 0:
                raise ValueError("序列必须是有序的 (升序)")
            deltas.append(delta)
        
        return deltas
    
    @staticmethod
    def delta_decode(deltas: List[int]) -> List[int]:
        """
        Delta 解码：从差值恢复原序列
        
        Args:
            deltas: 差值列表
            
        Returns:
            原始整数序列
        """
        if not deltas:
            return []
        
        values = [deltas[0]]
        for i in range(1, len(deltas)):
            values.append(values[-1] + deltas[i])
        
        return values
    
    def compress(self, values: List[int]) -> bytes:
        """
        压缩有序整数序列
        
        Args:
            values: 有序整数序列
            
        Returns:
            压缩后的字节数据
            
        数据格式：
            - 4 字节: 元素数量 (uint32)
            - 4 字节: 参数 M (uint32)
            - 剩余: 编码数据
        """
        if not values:
            return struct.pack('<II', 0, 0)
        
        # Delta 编码
        deltas = self.delta_encode(values)
        
        # 计算 M
        m = self.m if self.m else GolombCoding.optimal_m(deltas)
        
        # 创建编码器
        coder = GolombCoding(m)
        
        # 编码
        writer = BitWriter()
        for delta in deltas:
            coder.encode_to_writer(writer, delta)
        
        encoded = writer.flush()
        
        # 组装结果
        result = bytearray()
        result.extend(struct.pack('<I', len(values)))  # 元素数量
        result.extend(struct.pack('<I', m))  # 参数 M
        result.extend(encoded)  # 编码数据
        
        return bytes(result)
    
    def decompress(self, data: bytes) -> List[int]:
        """
        解压缩整数序列
        
        Args:
            data: 压缩的字节数据
            
        Returns:
            解压后的整数序列
        """
        if len(data) < 8:
            return []
        
        # 解析头部
        count = struct.unpack('<I', data[0:4])[0]
        m = struct.unpack('<I', data[4:8])[0]
        
        if count == 0:
            return []
        
        # 创建解码器
        coder = GolombCoding(m)
        
        # 解码
        reader = BitReader(data[8:])
        deltas = []
        for _ in range(count):
            deltas.append(coder.decode_from_reader(reader))
        
        # Delta 解码
        return self.delta_decode(deltas)
    
    def get_compression_ratio(self, values: List[int]) -> float:
        """
        计算压缩比
        
        Args:
            values: 整数序列
            
        Returns:
            压缩比 (原始大小 / 压缩后大小)
        """
        if not values:
            return 1.0
        
        # 原始大小 (假设 4 字节整数)
        original_size = len(values) * 4
        
        # 压缩后大小
        compressed = self.compress(values)
        compressed_size = len(compressed)
        
        return original_size / compressed_size if compressed_size > 0 else 1.0


class GolombRiceCoder:
    """
    高级 Golomb/Rice 编码器
    
    提供自动选择最佳编码方式的智能编码器。
    """
    
    @staticmethod
    def analyze(values: List[int]) -> dict:
        """
        分析数据并推荐最佳编码参数
        
        Args:
            values: 整数序列
            
        Returns:
            分析结果字典
        """
        if not values:
            return {
                'count': 0,
                'min': 0,
                'max': 0,
                'mean': 0,
                'recommended_m': 1,
                'recommended_k': 0,
                'recommended_type': 'rice',
            }
        
        non_neg = [v for v in values if v >= 0]
        
        if not non_neg:
            non_neg = [0]
        
        count = len(non_neg)
        min_val = min(non_neg)
        max_val = max(non_neg)
        mean = sum(non_neg) / count
        
        recommended_m = GolombCoding.optimal_m(non_neg)
        recommended_k = RiceCoding.optimal_k(non_neg)
        
        # 比较 Golomb 和 Rice
        golomb_coder = GolombCoding(recommended_m)
        rice_coder = RiceCoding(recommended_k)
        
        golomb_size = len(golomb_coder.encode_sequence(non_neg))
        rice_size = len(rice_coder.encode_sequence(non_neg))
        
        return {
            'count': count,
            'min': min_val,
            'max': max_val,
            'mean': mean,
            'recommended_m': recommended_m,
            'recommended_k': recommended_k,
            'recommended_type': 'rice' if rice_size <= golomb_size else 'golomb',
            'golomb_size': golomb_size,
            'rice_size': rice_size,
            'compression_efficiency': 'good' if mean > 10 else 'moderate',
        }
    
    @staticmethod
    def encode_optimal(values: List[int]) -> Tuple[bytes, dict]:
        """
        使用最优参数编码
        
        Args:
            values: 整数序列
            
        Returns:
            (编码数据, 元数据字典)
        """
        analysis = GolombRiceCoder.analyze(values)
        
        if analysis['recommended_type'] == 'rice':
            coder = RiceCoding(analysis['recommended_k'])
            metadata = {
                'type': 'rice',
                'k': analysis['recommended_k'],
                'm': 1 << analysis['recommended_k'],
            }
        else:
            coder = GolombCoding(analysis['recommended_m'])
            metadata = {
                'type': 'golomb',
                'm': analysis['recommended_m'],
            }
        
        encoded = coder.encode_sequence(values)
        metadata['count'] = len(values)
        
        return (encoded, metadata)
    
    @staticmethod
    def decode(data: bytes, metadata: dict) -> List[int]:
        """
        根据元数据解码
        
        Args:
            data: 编码数据
            metadata: 元数据字典
            
        Returns:
            解码后的整数列表
        """
        count = metadata.get('count', 0)
        
        if metadata.get('type') == 'rice':
            coder = RiceCoding(metadata['k'])
        else:
            coder = GolombCoding(metadata['m'])
        
        return coder.decode_sequence(data, count)


# 便捷函数
def golomb_encode(value: int, m: int) -> Tuple[int, int]:
    """Golomb 编码便捷函数"""
    return GolombCoding(m).encode(value)


def golomb_decode(q: int, r: int, m: int) -> int:
    """Golomb 解码便捷函数"""
    return q * m + r


def rice_encode(value: int, k: int) -> Tuple[int, int]:
    """Rice 编码便捷函数"""
    return RiceCoding(k).encode(value)


def rice_decode(q: int, r: int, k: int) -> int:
    """Rice 解码便捷函数"""
    m = 1 << k
    return q * m + r


def compress_sorted_integers(values: List[int], m: Optional[int] = None) -> bytes:
    """压缩有序整数序列便捷函数"""
    return DeltaGolombCompressor(m).compress(values)


def decompress_sorted_integers(data: bytes) -> List[int]:
    """解压缩整数序列便捷函数"""
    return DeltaGolombCompressor().decompress(data)


def optimal_parameter(values: List[int]) -> int:
    """计算最优 M 参数便捷函数"""
    return GolombCoding.optimal_m(values)


if __name__ == "__main__":
    # 简单演示
    print("=== Golomb 编码工具演示 ===")
    
    # 1. 基本 Golomb 编码
    print("\n--- Golomb 编码 ---")
    m = 8
    coder = GolombCoding(m)
    
    for value in [0, 1, 7, 8, 15, 16, 23, 24, 100]:
        q, r = coder.encode(value)
        decoded = coder.decode(q, r)
        print(f"值: {value:3d} -> 商: {q}, 余: {r}, 解码: {decoded}")
    
    # 2. Rice 编码
    print("\n--- Rice 编码 ---")
    k = 3  # M = 8
    rice = RiceCoding(k)
    
    encoded = rice.encode_sequence([1, 5, 10, 15, 20, 100])
    print(f"编码后长度: {len(encoded)} 字节")
    
    decoded = rice.decode_sequence(encoded, 6)
    print(f"解码结果: {decoded}")
    
    # 3. Delta + Golomb 压缩
    print("\n--- Delta + Golomb 压缩 ---")
    sorted_ids = [1, 5, 10, 15, 20, 100, 200, 500, 1000, 2000, 5000]
    
    compressor = DeltaGolombCompressor()
    compressed = compressor.compress(sorted_ids)
    print(f"原始数据: {sorted_ids}")
    print(f"压缩后: {len(compressed)} 字节")
    print(f"压缩比: {compressor.get_compression_ratio(sorted_ids):.2f}x")
    
    decompressed = compressor.decompress(compressed)
    print(f"解压后: {decompressed}")
    print(f"数据完整: {sorted_ids == decompressed}")
    
    # 4. 自动参数选择
    print("\n--- 自动参数选择 ---")
    values = [1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 80, 100]
    analysis = GolombRiceCoder.analyze(values)
    print(f"数据统计: {analysis}")
    
    encoded, metadata = GolombRiceCoder.encode_optimal(values)
    decoded = GolombRiceCoder.decode(encoded, metadata)
    print(f"编码元数据: {metadata}")
    print(f"编码后长度: {len(encoded)} 字节")
    print(f"解码验证: {values == decoded}")
    
    # 5. 比特流操作
    print("\n--- 比特流操作 ---")
    writer = BitWriter()
    
    # 写入不同类型的数据
    writer.write_bit(1)
    writer.write_bits(5, 3)  # 写入 101 (3 位)
    writer.write_unary(3)    # 写入 0001
    writer.write_gamma(10)   # 写入 Gamma 编码
    
    data = writer.flush()
    print(f"写入数据: {data.hex()}")
    
    # 读取
    reader = BitReader(data)
    print(f"读取比特: {reader.read_bit()}")
    print(f"读取 3 位: {reader.read_bits(3)}")
    print(f"读取一元: {reader.read_unary()}")
    print(f"读取 Gamma: {reader.read_gamma()}")