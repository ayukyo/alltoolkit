"""
Elias 编码工具模块

Elias 编码是一系列用于编码正整数的通用编码方法，广泛应用于数据压缩、
信息检索、搜索引擎索引等领域。

本模块实现：
- Elias Gamma 编码：适用于较小的整数
- Elias Delta 编码：更高效的编码，适用于较大的整数
- Elias Omega 编码：可变长度编码，理论上可编码任意大的正整数

特点：
- 零外部依赖
- 支持 bitstring 和 bytes 两种输出格式
- 支持编码和解码
- 高效的位操作实现
"""

from typing import List, Tuple, Union
import math


class BitWriter:
    """位写入器，用于构建二进制字符串"""
    
    def __init__(self):
        self._bits: List[int] = []
    
    def write_bit(self, bit: int) -> None:
        """写入单个位"""
        if bit not in (0, 1):
            raise ValueError(f"位值必须是 0 或 1，得到: {bit}")
        self._bits.append(bit)
    
    def write_bits(self, bits: str) -> None:
        """写入多个位（字符串形式）"""
        for bit in bits:
            self.write_bit(int(bit))
    
    def to_bitstring(self) -> str:
        """转换为二进制字符串"""
        return ''.join(str(b) for b in self._bits)
    
    def to_bytes(self) -> bytes:
        """转换为字节"""
        bitstring = self.to_bitstring()
        # 补齐到 8 的倍数
        padding = (8 - len(bitstring) % 8) % 8
        bitstring += '0' * padding
        
        result = bytearray()
        for i in range(0, len(bitstring), 8):
            byte_str = bitstring[i:i+8]
            result.append(int(byte_str, 2))
        
        # 在第一个字节存储填充位数
        if padding > 0:
            result = bytearray([padding]) + result
        
        return bytes(result)
    
    def __len__(self) -> int:
        return len(self._bits)


class BitReader:
    """位读取器，用于解析二进制字符串"""
    
    def __init__(self, data: Union[str, bytes]):
        self._position = 0
        
        if isinstance(data, bytes):
            if len(data) == 0:
                self._bits = ""
                self._padding = 0
            else:
                # 第一个字节是填充位数
                self._padding = data[0] if len(data) > 1 or data[0] < 8 else 0
                if self._padding > 0 and len(data) > 1:
                    # 跳过填充字节头
                    data = data[1:]
                else:
                    self._padding = 0
                
                bits_list = []
                for byte in data:
                    bits_list.append(format(byte, '08b'))
                bitstring = ''.join(bits_list)
                # 移除填充位
                self._bits = bitstring[:-self._padding] if self._padding > 0 else bitstring
        else:
            self._bits = data
            self._padding = 0
    
    def read_bit(self) -> int:
        """读取单个位"""
        if self._position >= len(self._bits):
            raise EOFError("已到达数据末尾")
        bit = int(self._bits[self._position])
        self._position += 1
        return bit
    
    def read_bits(self, n: int) -> str:
        """读取 n 个位"""
        if self._position + n > len(self._bits):
            raise EOFError("已到达数据末尾")
        bits = self._bits[self._position:self._position + n]
        self._position += n
        return bits
    
    def peek_bit(self) -> int:
        """查看下一个位但不移动位置"""
        if self._position >= len(self._bits):
            raise EOFError("已到达数据末尾")
        return int(self._bits[self._position])
    
    def has_more(self) -> bool:
        """是否还有更多数据"""
        return self._position < len(self._bits)
    
    @property
    def position(self) -> int:
        return self._position
    
    @property
    def total_bits(self) -> int:
        return len(self._bits)


# ============== Elias Gamma 编码 ==============

def elias_gamma_encode(n: int, as_bytes: bool = False) -> Union[str, bytes]:
    """
    Elias Gamma 编码
    
    编码规则：
    1. 计算 N = floor(log2(n))，写入 N 个 0
    2. 写入 n 的二进制表示（共 N+1 位）
    
    例如：
    - 1 -> "1"
    - 2 -> "010"
    - 3 -> "011"
    - 4 -> "00100"
    - 5 -> "00101"
    
    参数：
        n: 正整数 (n >= 1)
        as_bytes: 是否返回字节格式
    
    返回：
        编码后的二进制字符串或字节
    """
    if n < 1:
        raise ValueError(f"Elias Gamma 只能编码正整数，得到: {n}")
    
    writer = BitWriter()
    
    if n == 1:
        writer.write_bit(1)
    else:
        # 计算前导零的数量
        num_bits = n.bit_length()
        num_zeros = num_bits - 1
        
        # 写入前导零
        for _ in range(num_zeros):
            writer.write_bit(0)
        
        # 写入 n 的二进制表示
        binary = format(n, 'b')
        writer.write_bits(binary)
    
    return writer.to_bytes() if as_bytes else writer.to_bitstring()


def elias_gamma_decode(data: Union[str, bytes]) -> int:
    """
    Elias Gamma 解码
    
    参数：
        data: 编码后的二进制字符串或字节
    
    返回：
        解码后的正整数
    """
    reader = BitReader(data)
    
    # 计数前导零
    zero_count = 0
    while reader.has_more() and reader.peek_bit() == 0:
        reader.read_bit()
        zero_count += 1
    
    if not reader.has_more():
        raise ValueError("无效的 Elias Gamma 编码：数据不完整")
    
    # 读取第一个 1 和后续的位
    bits = reader.read_bits(zero_count + 1)
    
    return int(bits, 2)


def elias_gamma_encode_sequence(numbers: List[int], as_bytes: bool = False) -> Union[str, bytes]:
    """
    编码整数序列
    
    参数：
        numbers: 正整数列表
        as_bytes: 是否返回字节格式
    
    返回：
        编码后的二进制字符串或字节
    """
    writer = BitWriter()
    for n in numbers:
        if n < 1:
            raise ValueError(f"Elias Gamma 只能编码正整数，得到: {n}")
        
        if n == 1:
            writer.write_bit(1)
        else:
            num_bits = n.bit_length()
            num_zeros = num_bits - 1
            for _ in range(num_zeros):
                writer.write_bit(0)
            writer.write_bits(format(n, 'b'))
    
    return writer.to_bytes() if as_bytes else writer.to_bitstring()


def elias_gamma_decode_sequence(data: Union[str, bytes], count: int) -> List[int]:
    """
    解码整数序列
    
    参数：
        data: 编码后的二进制字符串或字节
        count: 要解码的整数个数
    
    返回：
        解码后的正整数列表
    """
    reader = BitReader(data)
    numbers = []
    
    for _ in range(count):
        zero_count = 0
        while reader.has_more() and reader.peek_bit() == 0:
            reader.read_bit()
            zero_count += 1
        
        if not reader.has_more():
            raise ValueError("无效的 Elias Gamma 编码：数据不完整")
        
        bits = reader.read_bits(zero_count + 1)
        numbers.append(int(bits, 2))
    
    return numbers


# ============== Elias Delta 编码 ==============

def elias_delta_encode(n: int, as_bytes: bool = False) -> Union[str, bytes]:
    """
    Elias Delta 编码
    
    编码规则：
    1. 计算 N = floor(log2(n))
    2. 使用 Elias Gamma 编码 N+1
    3. 写入 n 的低 N 位（去掉最高位的 1）
    
    例如：
    - 1 -> "1"
    - 2 -> "0100"
    - 3 -> "0101"
    - 4 -> "01100"
    - 5 -> "01101"
    
    参数：
        n: 正整数 (n >= 1)
        as_bytes: 是否返回字节格式
    
    返回：
        编码后的二进制字符串或字节
    """
    if n < 1:
        raise ValueError(f"Elias Delta 只能编码正整数，得到: {n}")
    
    writer = BitWriter()
    
    if n == 1:
        writer.write_bit(1)
    else:
        N = n.bit_length() - 1
        
        # 编码 N+1 使用 Gamma 编码
        gamma_N_plus_1 = elias_gamma_encode(N + 1)
        writer.write_bits(gamma_N_plus_1)
        
        # 写入 n 的低 N 位
        lower_bits = format(n, 'b')[1:]  # 去掉最高位的 1
        if lower_bits:  # 只有当 N > 0 时才有低位
            writer.write_bits(lower_bits)
    
    return writer.to_bytes() if as_bytes else writer.to_bitstring()


def elias_delta_decode(data: Union[str, bytes]) -> int:
    """
    Elias Delta 解码
    
    参数：
        data: 编码后的二进制字符串或字节
    
    返回：
        解码后的正整数
    """
    reader = BitReader(data)
    
    if not reader.has_more():
        raise ValueError("无效的 Elias Delta 编码：数据为空")
    
    if reader.peek_bit() == 1:
        # 第一个位是 1，说明 n=1
        reader.read_bit()
        return 1
    
    # 解码 N+1（使用 Gamma 解码）
    zero_count = 0
    while reader.has_more() and reader.peek_bit() == 0:
        reader.read_bit()
        zero_count += 1
    
    if not reader.has_more():
        raise ValueError("无效的 Elias Delta 编码：数据不完整")
    
    bits = reader.read_bits(zero_count + 1)
    N_plus_1 = int(bits, 2)
    N = N_plus_1 - 1
    
    if N == 0:
        return 1
    
    # 读取低 N 位
    lower_bits = reader.read_bits(N)
    
    # 重构原数
    return (1 << N) | int(lower_bits, 2)


def elias_delta_encode_sequence(numbers: List[int], as_bytes: bool = False) -> Union[str, bytes]:
    """
    编码整数序列
    
    参数：
        numbers: 正整数列表
        as_bytes: 是否返回字节格式
    
    返回：
        编码后的二进制字符串或字节
    """
    writer = BitWriter()
    for n in numbers:
        encoded = elias_delta_encode(n)
        writer.write_bits(encoded)
    
    return writer.to_bytes() if as_bytes else writer.to_bitstring()


def elias_delta_decode_sequence(data: Union[str, bytes], count: int) -> List[int]:
    """
    解码整数序列
    
    参数：
        data: 编码后的二进制字符串或字节
        count: 要解码的整数个数
    
    返回：
        解码后的正整数列表
    """
    reader = BitReader(data)
    numbers = []
    
    for _ in range(count):
        if not reader.has_more():
            raise ValueError("无效的 Elias Delta 编码：数据不完整")
        
        if reader.peek_bit() == 1:
            reader.read_bit()
            numbers.append(1)
            continue
        
        # 解码 N+1
        zero_count = 0
        while reader.has_more() and reader.peek_bit() == 0:
            reader.read_bit()
            zero_count += 1
        
        if not reader.has_more():
            raise ValueError("无效的 Elias Delta 编码：数据不完整")
        
        bits = reader.read_bits(zero_count + 1)
        N_plus_1 = int(bits, 2)
        N = N_plus_1 - 1
        
        if N == 0:
            numbers.append(1)
        else:
            lower_bits = reader.read_bits(N)
            numbers.append((1 << N) | int(lower_bits, 2))
    
    return numbers


# ============== Elias Omega 编码 ==============

def elias_omega_encode(n: int, as_bytes: bool = False) -> Union[str, bytes]:
    """
    Elias Omega 编码（也称为递归 Elias 编码）
    
    编码规则（标准 Wikipedia 定义）：
    To encode a positive integer N:
    1. Place an "initial" N on the output stream.
    2. If N = 1, stop.
    3. Let N be the number of bits in the binary representation of N, 
       not counting leading zeros.
    4. Go back to step 1.
    5. The output stream now contains the codeword in reverse order.
    
    实际上，这说的是：先写出数值的二进制，然后用位数继续编码，直到位数=1。
    最后反转输出并加终止符 0。
    
    例如编码 4：
    - N = 4，写 "100"
    - N = len("100") = 3，写 "11"
    - N = len("11") = 2，写 "10"
    - N = len("10") = 2，继续写 "10"... 不对
    
    正确理解：
    - 步骤 1：写 4 的二进制 "100"
    - 步骤 3：N = len("100") = 3
    - 步骤 1：写 3 的二进制 "11"
    - 步骤 3：N = len("11") = 2
    - 步骤 1：写 2 的二进制 "10"
    - 步骤 3：N = len("10") = 2... 继续？
    
    Wikipedia 说 "If N = 1, stop"，所以当 N = 1 时停止，不是当 len = 1。
    
    对于 4：
    - N = 4，写 "100"，len = 3
    - N = 3，写 "11"，len = 2
    - N = 2，写 "10"，len = 2... 继续？
    
    问题：N = 2 时继续还是停止？
    如果 N = 1 停止，那么 N = 2 继续：
    - N = 2，写 "10"，len = 2，N 又变成 2... 无限循环
    
    正确规则应该是：当 N <= 1 时停止。
    
    让我重新实现：
    
    参数：
        n: 正整数 (n >= 1)
        as_bytes: 是否返回字节格式
    
    返回：
        编码后的二进制字符串或字节
    """
    if n < 1:
        raise ValueError(f"Elias Omega 只能编码正整数，得到: {n}")
    
    if n == 1:
        return bytes([0]) if as_bytes else "0"
    
    # 标准 Elias Omega 编码：
    # 步骤：
    # 1. 记录 N 的二进制
    # 2. 用 len(binary) 替换 N（不是 len-1）
    # 3. 当 N <= 1 时停止
    # 4. 反转序列并加终止符 0
    
    sequence = []
    current = n
    
    while True:
        binary = format(current, 'b')
        sequence.append(binary)
        length = len(binary)
        # 当长度为 1 或 2 时停止（因为无法继续添加有意义的前缀）
        if length <= 2:
            break
        current = length
    
    # 反转序列并连接，然后加终止符 0
    result = ''.join(reversed(sequence)) + '0'
    
    if as_bytes:
        writer = BitWriter()
        writer.write_bits(result)
        return writer.to_bytes()
    
    return result


def elias_omega_decode(data: Union[str, bytes]) -> int:
    """
    Elias Omega 解码
    
    参数：
        data: 编码后的二进制字符串或字节
    
    返回：
        解码后的正整数
    """
    reader = BitReader(data)
    
    if not reader.has_more():
        raise ValueError("无效的 Elias Omega 编码：数据为空")
    
    # Elias Omega 解码算法：
    # 1. 初始化 n = 1
    # 2. 读取一个位 b
    # 3. 如果 b == 0，返回 n
    # 4. 否则，读取 n-1 个后续位，组合成新的 n（总共 n 位）
    # 5. 继续步骤 2
    
    # 编码格式：
    # 从最短前缀开始，逐层读取，直到终止符 0
    # 例如 "111000"（编码 4）：
    # - 前缀 "11"（二进制 3，表示下一段是 3 位）
    # - 数值 "100"（二进制 4）
    # - 终止符 "0"
    
    n = 1
    
    while reader.has_more():
        first_bit = reader.read_bit()
        if first_bit == 0:
            return n
        
        # 读取 n-1 个后续位
        bits = str(first_bit)
        if n > 1:
            bits += reader.read_bits(n - 1)
        else:
            # 当 n == 1 时，需要再读取一个位来构成 2 位数
            bits += str(reader.read_bit())
        
        n = int(bits, 2)
    
    raise ValueError("无效的 Elias Omega 编码：未找到终止符")


def elias_omega_encode_sequence(numbers: List[int], as_bytes: bool = False) -> Union[str, bytes]:
    """
    编码整数序列
    
    参数：
        numbers: 正整数列表
        as_bytes: 是否返回字节格式
    
    返回：
        编码后的二进制字符串或字节
    """
    writer = BitWriter()
    for n in numbers:
        encoded = elias_omega_encode(n)
        writer.write_bits(encoded)
    
    return writer.to_bytes() if as_bytes else writer.to_bitstring()


def elias_omega_decode_sequence(data: Union[str, bytes], count: int) -> List[int]:
    """
    解码整数序列
    
    参数：
        data: 编码后的二进制字符串或字节
        count: 要解码的整数个数
    
    返回：
        解码后的正整数列表
    """
    reader = BitReader(data)
    numbers = []
    
    for _ in range(count):
        n = 1
        
        while reader.has_more():
            bit = reader.read_bit()
            if bit == 0:
                numbers.append(n)
                break
            
            bits = str(bit)
            if n > 1:
                bits += reader.read_bits(n - 1)
            else:
                # 当 n == 1 时，需要读取额外的位来构成 2 位数
                bits += str(reader.read_bit())
            n = int(bits, 2)
    
    return numbers


# ============== 工具函数 ==============

def compare_encodings(n: int) -> dict:
    """
    比较不同 Elias 编码的长度
    
    参数：
        n: 正整数
    
    返回：
        包含各编码长度的字典
    """
    gamma = elias_gamma_encode(n)
    delta = elias_delta_encode(n)
    omega = elias_omega_encode(n)
    
    return {
        'number': n,
        'binary_length': n.bit_length(),
        'gamma': {
            'encoded': gamma,
            'length': len(gamma)
        },
        'delta': {
            'encoded': delta,
            'length': len(delta)
        },
        'omega': {
            'encoded': omega,
            'length': len(omega)
        },
        'recommendation': 'gamma' if len(gamma) <= len(delta) and len(gamma) <= len(omega)
                         else 'delta' if len(delta) <= len(omega) else 'omega'
    }


def optimal_encode(n: int, as_bytes: bool = False) -> Tuple[str, str]:
    """
    选择最优的 Elias 编码方式
    
    参数：
        n: 正整数
        as_bytes: 是否返回字节格式
    
    返回：
        (编码结果, 使用的编码类型)
    """
    gamma = elias_gamma_encode(n)
    delta = elias_delta_encode(n)
    omega = elias_omega_encode(n)
    
    lengths = {
        'gamma': len(gamma),
        'delta': len(delta),
        'omega': len(omega)
    }
    
    best = min(lengths, key=lengths.get)
    
    if best == 'gamma':
        return (elias_gamma_encode(n, as_bytes), 'gamma')
    elif best == 'delta':
        return (elias_delta_encode(n, as_bytes), 'delta')
    else:
        return (elias_omega_encode(n, as_bytes), 'omega')


def get_encoding_stats(numbers: List[int]) -> dict:
    """
    获取整数序列的编码统计信息
    
    参数：
        numbers: 正整数列表
    
    返回：
        编码统计信息
    """
    gamma_total = sum(len(elias_gamma_encode(n)) for n in numbers)
    delta_total = sum(len(elias_delta_encode(n)) for n in numbers)
    omega_total = sum(len(elias_omega_encode(n)) for n in numbers)
    
    # 计算普通二进制编码需要的位数
    binary_total = sum(max(1, n.bit_length()) for n in numbers)
    
    return {
        'count': len(numbers),
        'min': min(numbers),
        'max': max(numbers),
        'average': sum(numbers) / len(numbers),
        'binary_bits': binary_total,
        'gamma_bits': gamma_total,
        'delta_bits': delta_total,
        'omega_bits': omega_total,
        'best_method': min(
            [('gamma', gamma_total), ('delta', delta_total), ('omega', omega_total)],
            key=lambda x: x[1]
        )[0]
    }


# ============== 高级功能 ==============

class EliasEncoder:
    """Elias 编码器类，支持流式编码"""
    
    def __init__(self, method: str = 'gamma'):
        """
        初始化编码器
        
        参数：
            method: 编码方法 ('gamma', 'delta', 'omega')
        """
        if method not in ('gamma', 'delta', 'omega'):
            raise ValueError(f"不支持的编码方法: {method}")
        self.method = method
        self._writer = BitWriter()
        self._count = 0
    
    def encode(self, n: int) -> 'EliasEncoder':
        """编码一个整数"""
        if self.method == 'gamma':
            encoded = elias_gamma_encode(n)
        elif self.method == 'delta':
            encoded = elias_delta_encode(n)
        else:
            encoded = elias_omega_encode(n)
        
        self._writer.write_bits(encoded)
        self._count += 1
        return self
    
    def encode_all(self, numbers: List[int]) -> 'EliasEncoder':
        """编码多个整数"""
        for n in numbers:
            self.encode(n)
        return self
    
    def get_result(self, as_bytes: bool = False) -> Union[str, bytes]:
        """获取编码结果"""
        return self._writer.to_bytes() if as_bytes else self._writer.to_bitstring()
    
    @property
    def count(self) -> int:
        """已编码的整数数量"""
        return self._count
    
    @property
    def bit_length(self) -> int:
        """编码的总位数"""
        return len(self._writer)


class EliasDecoder:
    """Elias 解码器类，支持流式解码"""
    
    def __init__(self, data: Union[str, bytes], method: str = 'gamma'):
        """
        初始化解码器
        
        参数：
            data: 编码数据
            method: 编码方法 ('gamma', 'delta', 'omega')
        """
        if method not in ('gamma', 'delta', 'omega'):
            raise ValueError(f"不支持的编码方法: {method}")
        self.method = method
        self._reader = BitReader(data)
        self._decoded_count = 0
    
    def decode(self) -> int:
        """解码一个整数"""
        if self.method == 'gamma':
            result = self._decode_gamma()
        elif self.method == 'delta':
            result = self._decode_delta()
        else:
            result = self._decode_omega()
        
        self._decoded_count += 1
        return result
    
    def _decode_gamma(self) -> int:
        """Gamma 解码"""
        zero_count = 0
        while self._reader.has_more() and self._reader.peek_bit() == 0:
            self._reader.read_bit()
            zero_count += 1
        
        if not self._reader.has_more():
            raise EOFError("数据已读完")
        
        bits = self._reader.read_bits(zero_count + 1)
        return int(bits, 2)
    
    def _decode_delta(self) -> int:
        """Delta 解码"""
        if self._reader.peek_bit() == 1:
            self._reader.read_bit()
            return 1
        
        zero_count = 0
        while self._reader.has_more() and self._reader.peek_bit() == 0:
            self._reader.read_bit()
            zero_count += 1
        
        if not self._reader.has_more():
            raise EOFError("数据已读完")
        
        bits = self._reader.read_bits(zero_count + 1)
        N = int(bits, 2) - 1
        
        if N == 0:
            return 1
        
        lower_bits = self._reader.read_bits(N)
        return (1 << N) | int(lower_bits, 2)
    
    def _decode_omega(self) -> int:
        """Omega 解码"""
        n = 1
        
        while self._reader.has_more():
            bit = self._reader.read_bit()
            if bit == 0:
                return n
            
            bits = str(bit)
            if n > 1:
                bits += self._reader.read_bits(n - 1)
            else:
                # 当 n == 1 时，需要读取额外的位来构成 2 位数
                bits += str(self._reader.read_bit())
            n = int(bits, 2)
        
        raise EOFError("数据已读完")
    
    def decode_all(self) -> List[int]:
        """解码所有整数"""
        numbers = []
        while self._reader.has_more():
            try:
                numbers.append(self.decode())
            except EOFError:
                break
        return numbers
    
    def decode_count(self, count: int) -> List[int]:
        """解码指定数量的整数"""
        numbers = []
        for _ in range(count):
            try:
                numbers.append(self.decode())
            except EOFError:
                break
        return numbers
    
    @property
    def decoded_count(self) -> int:
        """已解码的整数数量"""
        return self._decoded_count
    
    @property
    def has_more(self) -> bool:
        """是否还有更多数据"""
        return self._reader.has_more()