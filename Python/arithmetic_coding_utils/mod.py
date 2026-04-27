"""
Arithmetic Coding Utils - 算术编码工具模块

算术编码是一种高效的无损数据压缩算法，将整个消息编码为一个浮点数。
相比哈夫曼编码，算术编码可以更接近信息熵的理论极限。

核心功能：
1. 静态算术编码/解码 - 使用预定义的概率分布
2. 自适应算术编码/解码 - 动态更新概率分布
3. 模型构建 - 从数据构建概率模型
4. 二进制算术编码 - 专门针对二进制数据的优化

特点：
- 零外部依赖
- 支持任意符号集
- 高精度计算，避免精度损失
- 支持自适应模型
"""

from typing import Dict, List, Tuple, Optional, Callable
from collections import Counter
from decimal import Decimal, getcontext
import math

# 设置高精度
getcontext().prec = 200


class ArithmeticModel:
    """算术编码概率模型"""
    
    def __init__(self, symbols: Optional[List] = None, counts: Optional[Dict] = None):
        """
        初始化模型
        
        Args:
            symbols: 符号列表
            counts: 符号计数字典
        """
        self.counts: Dict = {}
        self.total = 0
        
        if counts:
            self.counts = dict(counts)
            self.total = sum(counts.values())
        elif symbols:
            for symbol in symbols:
                self.update(symbol, initialize=True)
    
    def update(self, symbol, initialize: bool = False):
        """更新符号计数"""
        if symbol not in self.counts:
            self.counts[symbol] = 0
        self.counts[symbol] += 1
        if not initialize:
            self.total += 1
        else:
            self.total = sum(self.counts.values())
    
    def get_probability(self, symbol) -> float:
        """获取符号概率"""
        if self.total == 0:
            return 0
        return self.counts.get(symbol, 0) / self.total
    
    def get_cumulative_range(self, symbol) -> Tuple[float, float]:
        """
        获取符号的累积概率范围 [low, high)
        
        Returns:
            (low, high) 累积概率范围
        """
        low = 0.0
        for s, count in sorted(self.counts.items()):
            if s == symbol:
                return (low, low + count / self.total)
            low += count / self.total
        return (0.0, 0.0)
    
    def get_symbol_from_range(self, value: float) -> Optional[Tuple]:
        """
        根据累积概率值获取符号
        
        Args:
            value: 累积概率值
            
        Returns:
            (symbol, low, high) 或 None
        """
        low = 0.0
        for s, count in sorted(self.counts.items()):
            high = low + count / self.total
            if low <= value < high:
                return (s, low, high)
            low = high
        return None
    
    def get_symbols(self) -> List:
        """获取所有符号"""
        return list(self.counts.keys())


class ArithmeticEncoder:
    """算术编码器"""
    
    def __init__(self, model: Optional[ArithmeticModel] = None, adaptive: bool = False):
        """
        初始化编码器
        
        Args:
            model: 概率模型
            adaptive: 是否使用自适应模式
        """
        self.model = model or ArithmeticModel()
        self.adaptive = adaptive
        self.low = Decimal('0.0')
        self.high = Decimal('1.0')
        self._precision = 50
    
    def encode(self, symbols: List) -> float:
        """
        编码符号序列
        
        Args:
            symbols: 符号列表
            
        Returns:
            编码后的浮点数值
        """
        if not symbols:
            return 0.0
        
        # 如果不是自适应模式且模型为空，先构建模型
        if not self.adaptive and self.model.total == 0:
            self.model = ArithmeticModel(symbols=symbols)
        
        self.low = Decimal('0.0')
        self.high = Decimal('1.0')
        
        # 用于自适应模式的临时模型
        temp_model = ArithmeticModel(counts=dict(self.model.counts)) if self.adaptive else self.model
        
        for symbol in symbols:
            if self.adaptive:
                # 自适应模式：使用当前模型
                low_prob, high_prob = temp_model.get_cumulative_range(symbol)
                if low_prob == high_prob:
                    # 符号不存在，分配一个小概率
                    high_prob = 1.0 / (temp_model.total + 1)
                    low_prob = 0.0
            else:
                low_prob, high_prob = self.model.get_cumulative_range(symbol)
            
            # 使用 Decimal 避免精度损失
            range_width = self.high - self.low
            self.high = self.low + range_width * Decimal(str(high_prob))
            self.low = self.low + range_width * Decimal(str(low_prob))
            
            if self.adaptive:
                temp_model.update(symbol)
        
        # 返回区间的中点
        return float((self.low + self.high) / 2)
    
    def encode_to_bits(self, symbols: List) -> str:
        """
        编码为二进制位串
        
        Args:
            symbols: 符号列表
            
        Returns:
            二进制位字符串
        """
        code = self.encode(symbols)
        
        # 将浮点数转换为二进制表示
        bits = []
        value = Decimal(str(code))
        
        for _ in range(self._precision * 2):
            value *= 2
            if value >= 1:
                bits.append('1')
                value -= 1
            else:
                bits.append('0')
            
            # 检查是否已经足够精确
            if value < Decimal('1e-40'):
                break
        
        return ''.join(bits)
    
    def get_encoded_value(self) -> Tuple[float, float, float]:
        """
        获取当前编码状态
        
        Returns:
            (low, high, mid) 当前区间范围
        """
        mid = float((self.low + self.high) / 2)
        return (float(self.low), float(self.high), mid)


class ArithmeticDecoder:
    """算术解码器"""
    
    def __init__(self, model: Optional[ArithmeticModel] = None, adaptive: bool = False):
        """
        初始化解码器
        
        Args:
            model: 概率模型
            adaptive: 是否使用自适应模式
        """
        self.model = model or ArithmeticModel()
        self.adaptive = adaptive
        self._precision = 50
    
    def decode(self, code: float, num_symbols: int) -> List:
        """
        解码
        
        Args:
            code: 编码值
            num_symbols: 符号数量
            
        Returns:
            解码后的符号列表
        """
        if num_symbols == 0:
            return []
        
        symbols = []
        low = Decimal('0.0')
        high = Decimal('1.0')
        value = Decimal(str(code))
        
        # 用于自适应模式的临时模型
        temp_model = ArithmeticModel(counts=dict(self.model.counts)) if self.adaptive else self.model
        
        for _ in range(num_symbols):
            # 计算当前值在 [0,1) 区间的相对位置
            range_width = high - low
            if range_width == 0:
                break
            
            # 将值归一化到 [0,1) 区间
            normalized = (value - low) / range_width
            
            # 使用当前模型找到对应的符号
            result = temp_model.get_symbol_from_range(float(normalized))
            if result is None:
                break
            
            symbol, sym_low, sym_high = result
            symbols.append(symbol)
            
            # 更新区间
            high = low + range_width * Decimal(str(sym_high))
            low = low + range_width * Decimal(str(sym_low))
            
            # 自适应模式下更新模型
            if self.adaptive:
                temp_model.update(symbol)
        
        return symbols
    
    def decode_from_bits(self, bits: str, num_symbols: int) -> List:
        """
        从二进制位串解码
        
        Args:
            bits: 二进制位字符串
            num_symbols: 符号数量
            
        Returns:
            解码后的符号列表
        """
        # 将二进制转换为浮点数
        value = Decimal('0.0')
        power = Decimal('0.5')
        
        for bit in bits:
            if bit == '1':
                value += power
            power /= 2
        
        return self.decode(float(value), num_symbols)


class BinaryArithmeticEncoder:
    """
    二进制算术编码器
    
    专门针对二进制数据（0/1）优化的编码器
    """
    
    def __init__(self, probability_one: float = 0.5, adaptive: bool = True):
        """
        初始化二进制编码器
        
        Args:
            probability_one: 符号1的初始概率
            adaptive: 是否自适应更新概率
        """
        self.prob_one = probability_one
        self.adaptive = adaptive
        self.count_0 = 1
        self.count_1 = 1 if probability_one == 0.5 else int(probability_one * 2)
    
    def encode(self, bits: List[int]) -> float:
        """
        编码二进制序列
        
        Args:
            bits: 二进制位列表 [0, 1, 1, 0, ...]
            
        Returns:
            编码值
        """
        low = Decimal('0.0')
        high = Decimal('1.0')
        
        count_0 = self.count_0
        count_1 = self.count_1
        
        for bit in bits:
            total = count_0 + count_1
            prob_1 = Decimal(str(count_1)) / Decimal(str(total))
            
            range_width = high - low
            
            if bit == 1:
                low = low + range_width * (1 - prob_1)
            else:
                high = low + range_width * (1 - prob_1)
            
            if self.adaptive:
                if bit == 1:
                    count_1 += 1
                else:
                    count_0 += 1
        
        return float((low + high) / 2)
    
    def decode(self, code: float, num_bits: int) -> List[int]:
        """
        解码二进制序列
        
        Args:
            code: 编码值
            num_bits: 位数
            
        Returns:
            解码后的二进制位列表
        """
        bits = []
        value = Decimal(str(code))
        low = Decimal('0.0')
        high = Decimal('1.0')
        
        count_0 = self.count_0
        count_1 = self.count_1
        
        for _ in range(num_bits):
            total = count_0 + count_1
            prob_1 = Decimal(str(count_1)) / Decimal(str(total))
            
            mid = low + (high - low) * (1 - prob_1)
            
            if value >= mid:
                bits.append(1)
                low = mid
                if self.adaptive:
                    count_1 += 1
            else:
                bits.append(0)
                high = mid
                if self.adaptive:
                    count_0 += 1
        
        return bits


def build_model_from_data(data: List, smoothing: float = 0.0) -> ArithmeticModel:
    """
    从数据构建概率模型
    
    Args:
        data: 数据序列
        smoothing: 平滑因子，避免零概率
        
    Returns:
        ArithmeticModel 实例
    """
    counter = Counter(data)
    
    if smoothing > 0:
        for symbol in set(data):
            counter[symbol] += smoothing
    
    return ArithmeticModel(counts=dict(counter))


def encode_string(text: str, adaptive: bool = False) -> Tuple[float, Dict[str, int], int]:
    """
    编码字符串的便捷函数
    
    Args:
        text: 输入字符串
        adaptive: 是否使用自适应编码（需要预初始化模型）
        
    Returns:
        (编码值, 符号计数字典, 符号数量)
    """
    symbols = list(text)
    num_symbols = len(symbols)
    
    if adaptive:
        # 自适应模式：预初始化模型包含所有符号
        initial_counts = {s: 1 for s in set(symbols)}
        model = ArithmeticModel(counts=initial_counts)
        encoder = ArithmeticEncoder(model=model, adaptive=True)
        code = encoder.encode(symbols)
        return (code, initial_counts, num_symbols)
    else:
        # 静态模式：先分析数据，再编码
        model = ArithmeticModel(symbols=symbols)
        encoder = ArithmeticEncoder(model=model, adaptive=False)
        code = encoder.encode(symbols)
        return (code, dict(model.counts), num_symbols)


def decode_string(code: float, counts: Dict[str, int], num_symbols: int, adaptive: bool = False) -> str:
    """
    解码字符串的便捷函数
    
    Args:
        code: 编码值
        counts: 符号计数字典
        num_symbols: 符号数量
        adaptive: 是否使用自适应解码
        
    Returns:
        解码后的字符串
    """
    model = ArithmeticModel(counts=counts)
    decoder = ArithmeticDecoder(model=model, adaptive=adaptive)
    symbols = decoder.decode(code, num_symbols)
    return ''.join(symbols)


def calculate_compression_ratio(original_size: int, encoded_bits: int) -> float:
    """
    计算压缩比
    
    Args:
        original_size: 原始数据大小（字节）
        encoded_bits: 编码后的位数
        
    Returns:
        压缩比（原始/压缩后）
    """
    if encoded_bits == 0:
        return float('inf')
    encoded_bytes = encoded_bits / 8
    return original_size / encoded_bytes


def calculate_theoretical_bits(symbols: List, model: ArithmeticModel) -> float:
    """
    计算理论最优编码位数（基于信息熵）
    
    Args:
        symbols: 符号序列
        model: 概率模型
        
    Returns:
        理论最优位数
    """
    total_bits = 0.0
    for symbol in symbols:
        prob = model.get_probability(symbol)
        if prob > 0:
            total_bits += -math.log2(prob)
    return total_bits


class AdaptiveArithmeticCodec:
    """
    自适应算术编解码器
    
    动态更新概率模型，适合分布未知的场景
    """
    
    def __init__(self, initial_counts: Optional[Dict] = None):
        """
        初始化编解码器
        
        Args:
            initial_counts: 初始符号计数
        """
        self.model = ArithmeticModel(counts=initial_counts)
        self.encoder = ArithmeticEncoder(model=self.model, adaptive=True)
        self.decoder = ArithmeticDecoder(model=self.model, adaptive=True)
    
    def encode(self, symbols: List) -> float:
        """编码"""
        return self.encoder.encode(symbols)
    
    def decode(self, code: float, num_symbols: int) -> List:
        """解码"""
        return self.decoder.decode(code, num_symbols)
    
    def get_model(self) -> ArithmeticModel:
        """获取当前模型"""
        return self.model


# 上下文管理器支持
class ArithmeticCodingSession:
    """算术编码会话管理器"""
    
    def __init__(self, adaptive: bool = True):
        self.adaptive = adaptive
        self.model: Optional[ArithmeticModel] = None
        self.encoder: Optional[ArithmeticEncoder] = None
        self.decoder: Optional[ArithmeticDecoder] = None
    
    def __enter__(self):
        self.model = ArithmeticModel()
        self.encoder = ArithmeticEncoder(model=self.model, adaptive=self.adaptive)
        self.decoder = ArithmeticDecoder(model=self.model, adaptive=self.adaptive)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def encode(self, symbols: List) -> float:
        return self.encoder.encode(symbols)
    
    def decode(self, code: float, num_symbols: int) -> List:
        return self.decoder.decode(code, num_symbols)


if __name__ == "__main__":
    # 简单演示
    print("=== 算术编码演示 ===\n")
    
    # 1. 基本编码/解码
    text = "HELLO"
    print(f"原始文本: {text}")
    
    code, counts = encode_string(text, adaptive=True)
    print(f"编码值: {code}")
    print(f"符号计数: {counts}")
    
    decoded = decode_string(code, counts, adaptive=True)
    print(f"解码文本: {decoded}")
    print(f"解码正确: {decoded == text}\n")
    
    # 2. 二进制编码
    print("=== 二进制算术编码 ===")
    binary_data = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
    print(f"原始数据: {binary_data}")
    
    bin_encoder = BinaryArithmeticEncoder(probability_one=0.5, adaptive=True)
    bin_code = bin_encoder.encode(binary_data)
    print(f"编码值: {bin_code}")
    
    bin_decoder = BinaryArithmeticEncoder(probability_one=0.5, adaptive=True)
    decoded_bin = bin_decoder.decode(bin_code, len(binary_data))
    print(f"解码数据: {decoded_bin}")
    print(f"解码正确: {decoded_bin == binary_data}\n")
    
    # 3. 压缩效率
    print("=== 压缩效率分析 ===")
    long_text = "AAABBBCCDDDD"
    model = build_model_from_data(list(long_text))
    theoretical = calculate_theoretical_bits(list(long_text), model)
    print(f"文本: {long_text}")
    print(f"理论最优位数: {theoretical:.2f} bits")
    print(f"原始大小: {len(long_text) * 8} bits (假设每字符8位)")