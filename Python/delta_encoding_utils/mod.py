"""
Delta Encoding 工具模块

提供差分编码（Delta Encoding）算法实现，用于高效存储和传输有序数据序列。
核心思想：存储相邻元素之间的差值而非原始值，对单调递增或相似数据效果显著。

功能特性：
- 整数序列差分编码/解码
- 浮点数序列 XOR 差分编码
- 时间戳序列差分编码
- 字符串序列字典编码
- ZigZag 编码支持（处理负差值）
- 压缩统计信息

零外部依赖，纯 Python 实现。
"""

from typing import List, Dict, Tuple, Optional, Union, Any
from datetime import datetime
import struct


class DeltaEncoder:
    """整数序列差分编码器"""
    
    def __init__(self, use_zigzag: bool = True):
        """
        初始化编码器
        
        Args:
            use_zigzag: 是否使用 ZigZag 编码处理负差值
        """
        self.use_zigzag = use_zigzag
    
    @staticmethod
    def zigzag_encode(n: int) -> int:
        """
        ZigZag 编码：将负数映射到正数
        
        Examples:
            0 -> 0
            -1 -> 1
            1 -> 2
            -2 -> 3
            2 -> 4
        """
        return (n << 1) ^ (n >> 63)
    
    @staticmethod
    def zigzag_decode(n: int) -> int:
        """ZigZag 解码"""
        return (n >> 1) ^ -(n & 1)
    
    def encode(self, values: List[int]) -> List[int]:
        """
        对整数序列进行差分编码
        
        Args:
            values: 整数序列
            
        Returns:
            差分编码后的序列（第一个元素为基准值，其余为差值）
            
        Example:
            >>> encoder = DeltaEncoder()
            >>> encoder.encode([100, 101, 105, 110, 108])
            [100, 1, 4, 5, -2]
        """
        if not values:
            return []
        
        if len(values) == 1:
            return [values[0]]
        
        result = [values[0]]
        
        for i in range(1, len(values)):
            delta = values[i] - values[i - 1]
            if self.use_zigzag:
                delta = self.zigzag_encode(delta)
            result.append(delta)
        
        return result
    
    def decode(self, encoded: List[int]) -> List[int]:
        """
        对差分编码序列进行解码
        
        Args:
            encoded: 差分编码序列
            
        Returns:
            原始整数序列
            
        Example:
            >>> encoder = DeltaEncoder()
            >>> encoder.decode([100, 1, 4, 5, -2])
            [100, 101, 105, 110, 108]
        """
        if not encoded:
            return []
        
        if len(encoded) == 1:
            return [encoded[0]]
        
        result = [encoded[0]]
        current = encoded[0]
        
        for i in range(1, len(encoded)):
            delta = encoded[i]
            if self.use_zigzag:
                delta = self.zigzag_decode(delta)
            current += delta
            result.append(current)
        
        return result


class FloatDeltaEncoder:
    """浮点数序列 XOR 差分编码器
    
    使用 XOR 运算处理浮点数，避免精度问题
    """
    
    @staticmethod
    def float_to_int(f: float) -> int:
        """将浮点数转换为整数表示"""
        return struct.unpack('>Q', struct.pack('>d', f))[0]
    
    @staticmethod
    def int_to_float(i: int) -> float:
        """将整数表示转换回浮点数"""
        return struct.unpack('>d', struct.pack('>Q', i))[0]
    
    def encode(self, values: List[float]) -> List[Tuple[int, Optional[int]]]:
        """
        对浮点数序列进行 XOR 差分编码
        
        Args:
            values: 浮点数序列
            
        Returns:
            编码序列，每个元素为 (值, xor差分)
            第一个元素: (原始值整数表示, None)
            后续元素: (原始值整数表示, 与前值的XOR)
            
        Example:
            >>> encoder = FloatDeltaEncoder()
            >>> encoder.encode([1.5, 1.5, 2.0, 2.0, 3.0])
            [(4609434218613702656, None), (4609434218613702656, 0), ...]
        """
        if not values:
            return []
        
        result = []
        prev_int = None
        
        for val in values:
            current_int = self.float_to_int(val)
            
            if prev_int is None:
                result.append((current_int, None))
            else:
                xor_diff = current_int ^ prev_int
                result.append((current_int, xor_diff))
            
            prev_int = current_int
        
        return result
    
    def decode(self, encoded: List[Tuple[int, Optional[int]]]) -> List[float]:
        """
        对 XOR 差分编码序列进行解码
        
        Args:
            encoded: 编码序列
            
        Returns:
            原始浮点数序列
        """
        if not encoded:
            return []
        
        result = []
        prev_int = None
        
        for val_int, xor_diff in encoded:
            if xor_diff is None:
                current_int = val_int
            else:
                current_int = prev_int ^ xor_diff
            
            result.append(self.int_to_float(current_int))
            prev_int = current_int
        
        return result
    
    def encode_compact(self, values: List[float]) -> Dict[str, Any]:
        """
        紧凑编码：只存储首个值和 XOR 差分
        
        Args:
            values: 浮点数序列
            
        Returns:
            包含 first_value 和 xor_deltas 的字典
        """
        if not values:
            return {'first_value': None, 'xor_deltas': []}
        
        encoded = self.encode(values)
        xor_deltas = [e[1] for e in encoded[1:]]
        
        return {
            'first_value': encoded[0][0],
            'xor_deltas': xor_deltas
        }
    
    def decode_compact(self, compact: Dict[str, Any]) -> List[float]:
        """
        解码紧凑格式
        
        Args:
            compact: 紧凑编码字典
            
        Returns:
            原始浮点数序列
        """
        if compact['first_value'] is None:
            return []
        
        encoded = [(compact['first_value'], None)]
        
        for xor_delta in compact['xor_deltas']:
            val_int = encoded[-1][0] ^ xor_delta
            encoded.append((val_int, xor_delta))
        
        return self.decode(encoded)


class TimestampDeltaEncoder:
    """时间戳序列差分编码器
    
    专为时间序列数据优化，支持毫秒级精度
    """
    
    def __init__(self, unit: str = 'ms'):
        """
        初始化编码器
        
        Args:
            unit: 时间单位 ('ms' 毫秒, 's' 秒, 'us' 微秒)
        """
        self.unit = unit
        self.multiplier = {
            's': 1,
            'ms': 1000,
            'us': 1000000
        }.get(unit, 1000)
    
    def to_timestamp(self, dt: datetime) -> int:
        """将 datetime 转换为时间戳"""
        ts = dt.timestamp()
        return int(ts * self.multiplier)
    
    def from_timestamp(self, ts: int) -> datetime:
        """将时间戳转换为 datetime"""
        return datetime.fromtimestamp(ts / self.multiplier)
    
    def encode(self, datetimes: List[datetime]) -> Tuple[int, List[int]]:
        """
        对时间戳序列进行差分编码
        
        Args:
            datetimes: datetime 序列
            
        Returns:
            (基准时间戳, 差分列表)
            
        Example:
            >>> encoder = TimestampDeltaEncoder()
            >>> base_ts, deltas = encoder.encode([
            ...     datetime(2024, 1, 1, 0, 0, 0),
            ...     datetime(2024, 1, 1, 0, 0, 1),
            ...     datetime(2024, 1, 1, 0, 0, 2)
            ... ])
        """
        if not datetimes:
            return (0, [])
        
        timestamps = [self.to_timestamp(dt) for dt in datetimes]
        
        if len(timestamps) == 1:
            return (timestamps[0], [0])
        
        deltas = [0]  # 第一个差分为0，表示相对于基准
        for i in range(1, len(timestamps)):
            deltas.append(timestamps[i] - timestamps[i - 1])
        
        return (timestamps[0], deltas)
    
    def decode(self, base_ts: int, deltas: List[int]) -> List[datetime]:
        """
        解码时间戳序列
        
        Args:
            base_ts: 基准时间戳
            deltas: 差分列表
            
        Returns:
            datetime 序列
        """
        if not deltas:
            return []
        
        timestamps = [base_ts]
        for i in range(1, len(deltas)):
            timestamps.append(timestamps[-1] + deltas[i])
        
        return [self.from_timestamp(ts) for ts in timestamps]
    
    def encode_with_delta_of_delta(self, datetimes: List[datetime]) -> Dict[str, Any]:
        """
        使用二阶差分编码（Delta-of-Delta）
        
        适用于等间隔或近似等间隔的时间序列，压缩效果更好
        
        Args:
            datetimes: datetime 序列
            
        Returns:
            编码结果字典
        """
        if not datetimes:
            return {'base_ts': 0, 'first_delta': 0, 'dod': []}
        
        timestamps = [self.to_timestamp(dt) for dt in datetimes]
        
        if len(timestamps) == 1:
            return {
                'base_ts': timestamps[0],
                'first_delta': 0,
                'dod': []
            }
        
        # 计算一阶差分
        deltas = []
        for i in range(1, len(timestamps)):
            deltas.append(timestamps[i] - timestamps[i - 1])
        
        # 计算二阶差分（Delta-of-Delta）
        dod = [0]  # 第一个点没有二阶差分
        for i in range(1, len(deltas)):
            dod.append(deltas[i] - deltas[i - 1])
        
        return {
            'base_ts': timestamps[0],
            'first_delta': deltas[0] if deltas else 0,
            'dod': dod
        }
    
    def decode_with_delta_of_delta(self, encoded: Dict[str, Any]) -> List[datetime]:
        """
        解码二阶差分编码
        
        Args:
            encoded: 编码结果字典
            
        Returns:
            datetime 序列
        """
        base_ts = encoded['base_ts']
        first_delta = encoded['first_delta']
        dod = encoded['dod']
        
        if not dod:
            if base_ts:
                return [self.from_timestamp(base_ts)]
            return []
        
        # 重建一阶差分
        deltas = [first_delta]
        for i in range(1, len(dod)):
            deltas.append(deltas[-1] + dod[i])
        
        # 重建时间戳
        timestamps = [base_ts]
        for delta in deltas:
            timestamps.append(timestamps[-1] + delta)
        
        return [self.from_timestamp(ts) for ts in timestamps]


class DictionaryEncoder:
    """字典编码器
    
    将字符串序列转换为整数ID，适用于重复字符串较多的场景
    """
    
    def __init__(self):
        self._dictionary: Dict[str, int] = {}
        self._reverse_dict: Dict[int, str] = {}
        self._next_id = 0
    
    def encode(self, values: List[str]) -> Tuple[List[int], Dict[str, int]]:
        """
        对字符串序列进行字典编码
        
        Args:
            values: 字符串序列
            
        Returns:
            (ID序列, 字典映射)
            
        Example:
            >>> encoder = DictionaryEncoder()
            >>> ids, dictionary = encoder.encode(['apple', 'banana', 'apple', 'cherry'])
            >>> ids
            [0, 1, 0, 2]
        """
        ids = []
        
        for val in values:
            if val not in self._dictionary:
                self._dictionary[val] = self._next_id
                self._reverse_dict[self._next_id] = val
                self._next_id += 1
            
            ids.append(self._dictionary[val])
        
        return (ids, dict(self._dictionary))
    
    def decode(self, ids: List[int], dictionary: Optional[Dict[str, int]] = None) -> List[str]:
        """
        解码字典编码序列
        
        Args:
            ids: ID 序列
            dictionary: 字典映射（可选，使用当前编码器状态）
            
        Returns:
            字符串序列
        """
        if dictionary:
            reverse = {v: k for k, v in dictionary.items()}
        else:
            reverse = self._reverse_dict
        
        return [reverse[id_] for id_ in ids]
    
    def get_dictionary(self) -> Dict[str, int]:
        """获取当前字典"""
        return dict(self._dictionary)
    
    def get_vocabulary_size(self) -> int:
        """获取词汇表大小"""
        return len(self._dictionary)
    
    def clear(self):
        """清空字典"""
        self._dictionary.clear()
        self._reverse_dict.clear()
        self._next_id = 0


class DeltaEncodingStats:
    """差分编码统计工具"""
    
    @staticmethod
    def analyze_integers(values: List[int], use_zigzag: bool = True) -> Dict[str, Any]:
        """
        分析整数序列的差分编码效果
        
        Args:
            values: 整数序列
            use_zigzag: 是否使用 ZigZag 编码
            
        Returns:
            统计信息字典
        """
        if not values:
            return {
                'original_count': 0,
                'original_size_bytes': 0,
                'encoded_size_bytes': 0,
                'compression_ratio': 0,
                'avg_delta': 0,
                'max_delta': 0,
                'min_delta': 0
            }
        
        encoder = DeltaEncoder(use_zigzag=use_zigzag)
        encoded = encoder.encode(values)
        
        # 计算原始大小（假设64位整数）
        original_size = len(values) * 8
        
        # 计算编码后大小（估算）
        # 对于 ZigZag 编码，较小的值使用更少的位
        encoded_size = 8  # 基准值
        for delta in encoded[1:]:
            delta = abs(encoder.zigzag_decode(delta) if use_zigzag else delta)
            if delta < 128:
                encoded_size += 1
            elif delta < 32768:
                encoded_size += 2
            elif delta < 8388608:
                encoded_size += 3
            else:
                encoded_size += 4
        
        # 计算差分统计
        deltas = []
        for i in range(1, len(values)):
            deltas.append(values[i] - values[i - 1])
        
        return {
            'original_count': len(values),
            'original_size_bytes': original_size,
            'encoded_size_bytes': encoded_size,
            'compression_ratio': original_size / encoded_size if encoded_size > 0 else 0,
            'avg_delta': sum(deltas) / len(deltas) if deltas else 0,
            'max_delta': max(deltas) if deltas else 0,
            'min_delta': min(deltas) if deltas else 0
        }
    
    @staticmethod
    def analyze_strings(values: List[str]) -> Dict[str, Any]:
        """
        分析字符串序列的字典编码效果
        
        Args:
            values: 字符串序列
            
        Returns:
            统计信息字典
        """
        if not values:
            return {
                'original_count': 0,
                'unique_count': 0,
                'original_size_bytes': 0,
                'encoded_size_bytes': 0,
                'compression_ratio': 0,
                'redundancy_ratio': 0
            }
        
        encoder = DictionaryEncoder()
        ids, _ = encoder.encode(values)
        
        # 计算原始大小
        original_size = sum(len(s.encode('utf-8')) for s in values)
        
        # 计算编码后大小
        # 字典存储 + ID存储
        dictionary = encoder.get_dictionary()
        dict_size = sum(len(k.encode('utf-8')) + 4 for k in dictionary)  # 字符串 + ID
        id_size = len(ids) * 4  # 每个 ID 4 字节
        encoded_size = dict_size + id_size
        
        unique_count = len(dictionary)
        redundancy_ratio = (len(values) - unique_count) / len(values) if values else 0
        
        return {
            'original_count': len(values),
            'unique_count': unique_count,
            'original_size_bytes': original_size,
            'encoded_size_bytes': encoded_size,
            'compression_ratio': original_size / encoded_size if encoded_size > 0 else 0,
            'redundancy_ratio': redundancy_ratio
        }


def delta_encode(values: List[int], use_zigzag: bool = True) -> List[int]:
    """
    快捷函数：整数差分编码
    
    Args:
        values: 整数序列
        use_zigzag: 是否使用 ZigZag 编码
        
    Returns:
        差分编码序列
    """
    encoder = DeltaEncoder(use_zigzag=use_zigzag)
    return encoder.encode(values)


def delta_decode(encoded: List[int], use_zigzag: bool = True) -> List[int]:
    """
    快捷函数：整数差分解码
    
    Args:
        encoded: 差分编码序列
        use_zigzag: 是否使用 ZigZag 编码
        
    Returns:
        原始整数序列
    """
    encoder = DeltaEncoder(use_zigzag=use_zigzag)
    return encoder.decode(encoded)


def dict_encode(values: List[str]) -> Tuple[List[int], Dict[str, int]]:
    """
    快捷函数：字典编码
    
    Args:
        values: 字符串序列
        
    Returns:
        (ID序列, 字典映射)
    """
    encoder = DictionaryEncoder()
    return encoder.encode(values)


def dict_decode(ids: List[int], dictionary: Dict[str, int]) -> List[str]:
    """
    快捷函数：字典解码
    
    Args:
        ids: ID 序列
        dictionary: 字典映射
        
    Returns:
        字符串序列
    """
    reverse = {v: k for k, v in dictionary.items()}
    return [reverse[id_] for id_ in ids]


if __name__ == "__main__":
    # 简单演示
    print("=== Delta Encoding Demo ===\n")
    
    # 整数差分编码
    print("1. 整数差分编码:")
    numbers = [100, 105, 110, 108, 115, 120, 118]
    print(f"   原始: {numbers}")
    
    encoder = DeltaEncoder()
    encoded = encoder.encode(numbers)
    print(f"   编码: {encoded}")
    
    decoded = encoder.decode(encoded)
    print(f"   解码: {decoded}")
    
    # 统计分析
    stats = DeltaEncodingStats.analyze_integers(numbers)
    print(f"   压缩比: {stats['compression_ratio']:.2f}x")
    
    print()
    
    # 浮点数 XOR 差分编码
    print("2. 浮点数 XOR 差分编码:")
    floats = [1.5, 1.5, 2.0, 2.0, 3.0, 3.0, 3.0]
    print(f"   原始: {floats}")
    
    float_encoder = FloatDeltaEncoder()
    compact = float_encoder.encode_compact(floats)
    print(f"   紧凑编码: 首值={compact['first_value']}, XOR差分={compact['xor_deltas'][:3]}...")
    
    decoded_floats = float_encoder.decode_compact(compact)
    print(f"   解码: {decoded_floats}")
    
    print()
    
    # 字典编码
    print("3. 字典编码:")
    strings = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple', 'date']
    print(f"   原始: {strings}")
    
    ids, dictionary = dict_encode(strings)
    print(f"   ID序列: {ids}")
    print(f"   字典: {dictionary}")
    
    decoded_strings = dict_decode(ids, dictionary)
    print(f"   解码: {decoded_strings}")
    
    stats = DeltaEncodingStats.analyze_strings(strings)
    print(f"   唯一词数: {stats['unique_count']}")
    print(f"   冗余率: {stats['redundancy_ratio']:.2%}")