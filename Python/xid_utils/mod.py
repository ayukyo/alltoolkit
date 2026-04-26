"""
XID Utils - 全局唯一、时间排序的ID生成与解析工具

XID 是一种紧凑的全局唯一标识符：
- 12字节（比UUID的16字节更短）
- 时间排序（可按ID排序）
- URL安全（Base32Hex编码，无填充）
- 分布式友好（包含机器ID和进程ID）

格式（12字节）：
- 4字节：Unix时间戳（秒）
- 3字节：机器ID
- 2字节：进程ID
- 3字节：计数器

零外部依赖，纯Python实现。
"""

import os
import time
import socket
import struct
import threading
from datetime import datetime, timezone
from typing import Optional, Tuple, Union


# Base32Hex 字母表（RFC 2938）
BASE32HEX_ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUV'
BASE32HEX_DECODE = {c: i for i, c in enumerate(BASE32HEX_ALPHABET)}


class XIDError(Exception):
    """XID 相关错误"""
    pass


class XID:
    """
    XID 对象 - 表示一个全局唯一、时间排序的标识符
    
    特性：
    - 12字节二进制数据
    - 20字符Base32Hex字符串表示
    - 时间排序
    - 包含生成信息（时间、机器、进程、计数器）
    """
    
    # 类级别的计数器和锁
    _counter: int = 0
    _lock: threading.Lock = threading.Lock()
    _last_timestamp: int = 0
    
    # 缓存的机器ID和进程ID
    _machine_id: Optional[bytes] = None
    _process_id: Optional[int] = None
    
    def __init__(self, value: Optional[Union[bytes, str]] = None):
        """
        创建XID对象
        
        Args:
            value: 可选的初始值
                   - None: 生成新的XID
                   - bytes: 12字节二进制数据
                   - str: 20字符Base32Hex字符串
        """
        if value is None:
            self._data = self._generate()
        elif isinstance(value, bytes):
            if len(value) != 12:
                raise XIDError(f"XID must be 12 bytes, got {len(value)}")
            self._data = value
        elif isinstance(value, str):
            self._data = self._decode(value)
        else:
            raise XIDError(f"Invalid XID value type: {type(value)}")
    
    @classmethod
    def _get_machine_id(cls) -> bytes:
        """获取机器ID（3字节）"""
        if cls._machine_id is None:
            # 尝试获取主机名并生成机器ID
            try:
                hostname = socket.gethostname().encode('utf-8')
            except Exception:
                hostname = b'localhost'
            
            # 使用主机名的hash生成3字节机器ID
            import hashlib
            digest = hashlib.md5(hostname).digest()
            cls._machine_id = digest[:3]
        
        return cls._machine_id
    
    @classmethod
    def _get_process_id(cls) -> int:
        """获取进程ID（2字节范围内）"""
        if cls._process_id is None:
            cls._process_id = os.getpid() & 0xFFFF
        return cls._process_id
    
    @classmethod
    def _generate(cls) -> bytes:
        """
        生成新的XID
        
        Returns:
            12字节二进制XID
        """
        with cls._lock:
            timestamp = int(time.time())
            
            # 如果时间戳改变，重置计数器
            if timestamp != cls._last_timestamp:
                cls._last_timestamp = timestamp
                # 使用随机数初始化计数器（避免重启后重复）
                cls._counter = int.from_bytes(os.urandom(3), 'big') & 0xFFFFFF
            
            # 递增计数器
            cls._counter = (cls._counter + 1) & 0xFFFFFF
            
            # 构建XID
            machine_id = cls._get_machine_id()
            process_id = cls._get_process_id()
            
            # 打包为12字节
            # 4字节时间戳 + 3字节机器ID + 2字节进程ID + 3字节计数器
            data = struct.pack(
                '>I',  # 4字节大端时间戳
                timestamp
            ) + machine_id + struct.pack(
                '>H',  # 2字节大端进程ID
                process_id
            ) + struct.pack(
                '>I',  # 4字节大端（取低3字节计数器）
                cls._counter
            )[1:]  # 取后3字节
            
            return data
    
    @staticmethod
    def _decode(s: str) -> bytes:
        """
        将Base32Hex字符串解码为字节
        
        Args:
            s: 20字符Base32Hex字符串
            
        Returns:
            12字节二进制数据
        """
        if len(s) != 20:
            raise XIDError(f"XID string must be 20 characters, got {len(s)}")
        
        s = s.upper()
        
        # Base32Hex解码
        result = bytearray()
        buffer = 0
        bits = 0
        
        for char in s:
            if char not in BASE32HEX_DECODE:
                raise XIDError(f"Invalid character in XID: {char}")
            
            buffer = (buffer << 5) | BASE32HEX_DECODE[char]
            bits += 5
            
            if bits >= 8:
                bits -= 8
                result.append((buffer >> bits) & 0xFF)
                buffer &= (1 << bits) - 1
        
        return bytes(result)
    
    def encode(self) -> str:
        """
        将XID编码为Base32Hex字符串
        
        Returns:
            20字符Base32Hex字符串
        """
        # Base32Hex编码
        result = []
        buffer = 0
        bits = 0
        
        for byte in self._data:
            buffer = (buffer << 8) | byte
            bits += 8
            
            while bits >= 5:
                bits -= 5
                result.append(BASE32HEX_ALPHABET[(buffer >> bits) & 0x1F])
                buffer &= (1 << bits) - 1
        
        # 处理剩余位
        if bits > 0:
            result.append(BASE32HEX_ALPHABET[(buffer << (5 - bits)) & 0x1F])
        
        return ''.join(result)
    
    @property
    def bytes(self) -> bytes:
        """获取原始字节"""
        return self._data
    
    @property
    def timestamp(self) -> int:
        """获取Unix时间戳（秒）"""
        return struct.unpack('>I', self._data[:4])[0]
    
    @property
    def datetime(self) -> datetime:
        """获取时间戳对应的datetime对象（UTC）"""
        return datetime.fromtimestamp(self.timestamp, tz=timezone.utc)
    
    @property
    def machine_id(self) -> bytes:
        """获取机器ID（3字节）"""
        return self._data[4:7]
    
    @property
    def process_id(self) -> int:
        """获取进程ID"""
        return struct.unpack('>H', self._data[7:9])[0]
    
    @property
    def counter(self) -> int:
        """获取计数器值"""
        return struct.unpack('>I', b'\x00' + self._data[9:12])[0]
    
    def __str__(self) -> str:
        return self.encode()
    
    def __repr__(self) -> str:
        return f"XID('{self.encode()}')"
    
    def __bytes__(self) -> bytes:
        return self._data
    
    def __eq__(self, other) -> bool:
        if isinstance(other, XID):
            return self._data == other._data
        return False
    
    def __hash__(self) -> int:
        return hash(self._data)
    
    def __lt__(self, other) -> bool:
        if isinstance(other, XID):
            return self._data < other._data
        return NotImplemented
    
    def __le__(self, other) -> bool:
        if isinstance(other, XID):
            return self._data <= other._data
        return NotImplemented
    
    def __gt__(self, other) -> bool:
        if isinstance(other, XID):
            return self._data > other._data
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        if isinstance(other, XID):
            return self._data >= other._data
        return NotImplemented
    
    def __len__(self) -> int:
        return 12


# ============== 便捷函数 ==============

def generate() -> XID:
    """
    生成新的XID
    
    Returns:
        新的XID对象
        
    Example:
        >>> xid = generate()
        >>> str(xid)
        '9m4e2mr0ui3e8a215n4g'
    """
    return XID()


def from_string(s: str) -> XID:
    """
    从字符串解析XID
    
    Args:
        s: 20字符Base32Hex字符串
        
    Returns:
        XID对象
        
    Example:
        >>> xid = from_string('9m4e2mr0ui3e8a215n4g')
        >>> xid.timestamp
        1234567890
    """
    return XID(s)


def from_bytes(data: bytes) -> XID:
    """
    从字节创建XID
    
    Args:
        data: 12字节二进制数据
        
    Returns:
        XID对象
        
    Example:
        >>> xid = from_bytes(b'\\x00' * 12)
        >>> str(xid)
        '00000000000000000000'
    """
    return XID(data)


def is_valid(s: str) -> bool:
    """
    验证字符串是否为有效的XID
    
    Args:
        s: 要验证的字符串
        
    Returns:
        是否为有效的XID字符串
        
    Example:
        >>> is_valid('9m4e2mr0ui3e8a215n4g')
        True
        >>> is_valid('invalid')
        False
    """
    if not isinstance(s, str) or len(s) != 20:
        return False
    
    try:
        XID(s)
        return True
    except XIDError:
        return False


def extract_timestamp(xid: Union[XID, str, bytes]) -> int:
    """
    从XID提取时间戳
    
    Args:
        xid: XID对象、字符串或字节
        
    Returns:
        Unix时间戳（秒）
        
    Example:
        >>> extract_timestamp('9m4e2mr0ui3e8a215n4g')
        1234567890
    """
    if isinstance(xid, XID):
        return xid.timestamp
    return XID(xid).timestamp


def extract_datetime(xid: Union[XID, str, bytes]) -> datetime:
    """
    从XID提取datetime对象
    
    Args:
        xid: XID对象、字符串或字节
        
    Returns:
        UTC datetime对象
        
    Example:
        >>> extract_datetime('9m4e2mr0ui3e8a215n4g')
        datetime.datetime(2009, 2, 13, 23, 31, 30, tzinfo=datetime.timezone.utc)
    """
    if isinstance(xid, XID):
        return xid.datetime
    return XID(xid).datetime


def compare(xid1: Union[XID, str, bytes], xid2: Union[XID, str, bytes]) -> int:
    """
    比较两个XID（按时间排序）
    
    Args:
        xid1: 第一个XID
        xid2: 第二个XID
        
    Returns:
        -1: xid1 < xid2
         0: xid1 == xid2
         1: xid1 > xid2
        
    Example:
        >>> xid1 = generate()
        >>> import time; time.sleep(0.1)
        >>> xid2 = generate()
        >>> compare(xid1, xid2)
        -1
    """
    if not isinstance(xid1, XID):
        xid1 = XID(xid1)
    if not isinstance(xid2, XID):
        xid2 = XID(xid2)
    
    if xid1 < xid2:
        return -1
    elif xid1 > xid2:
        return 1
    return 0


def batch_generate(count: int) -> list:
    """
    批量生成XID
    
    Args:
        count: 生成数量
        
    Returns:
        XID列表
        
    Example:
        >>> xids = batch_generate(10)
        >>> len(xids)
        10
    """
    return [XID() for _ in range(count)]


def parse_info(xid: Union[XID, str, bytes]) -> dict:
    """
    解析XID的所有信息
    
    Args:
        xid: XID对象、字符串或字节
        
    Returns:
        包含时间戳、机器ID、进程ID、计数器等信息的字典
        
    Example:
        >>> info = parse_info('9m4e2mr0ui3e8a215n4g')
        >>> info['timestamp']
        1234567890
    """
    if not isinstance(xid, XID):
        xid = XID(xid)
    
    return {
        'string': str(xid),
        'bytes': xid.bytes.hex(),
        'timestamp': xid.timestamp,
        'datetime': xid.datetime.isoformat(),
        'machine_id': xid.machine_id.hex(),
        'process_id': xid.process_id,
        'counter': xid.counter
    }


def min_xid(timestamp: Optional[int] = None) -> XID:
    """
    创建指定时间戳的最小XID（计数器=0，机器ID=0，进程ID=0）
    
    用于数据库范围查询。
    
    Args:
        timestamp: Unix时间戳，None则使用当前时间
        
    Returns:
        最小XID对象
        
    Example:
        >>> xid = min_xid(1234567890)
        >>> xid.timestamp
        1234567890
    """
    if timestamp is None:
        timestamp = int(time.time())
    
    data = struct.pack('>I', timestamp) + b'\x00' * 8
    return XID(data)


def max_xid(timestamp: Optional[int] = None) -> XID:
    """
    创建指定时间戳的最大XID（计数器=max，机器ID=max，进程ID=max）
    
    用于数据库范围查询。
    
    Args:
        timestamp: Unix时间戳，None则使用当前时间
        
    Returns:
        最大XID对象
        
    Example:
        >>> xid = max_xid(1234567890)
        >>> xid.timestamp
        1234567890
    """
    if timestamp is None:
        timestamp = int(time.time())
    
    data = struct.pack('>I', timestamp) + b'\xFF' * 8
    return XID(data)


class XIDGenerator:
    """
    XID生成器类 - 支持自定义机器ID和进程ID
    
    适用于需要多租户或手动控制的场景。
    """
    
    def __init__(
        self,
        machine_id: Optional[bytes] = None,
        process_id: Optional[int] = None
    ):
        """
        初始化生成器
        
        Args:
            machine_id: 3字节机器ID，None则自动获取
            process_id: 进程ID（0-65535），None则自动获取
        """
        if machine_id is not None:
            if len(machine_id) != 3:
                raise XIDError(f"Machine ID must be 3 bytes, got {len(machine_id)}")
            self._machine_id = machine_id
        else:
            self._machine_id = XID._get_machine_id()
        
        if process_id is not None:
            if not 0 <= process_id <= 0xFFFF:
                raise XIDError(f"Process ID must be 0-65535, got {process_id}")
            self._process_id = process_id
        else:
            self._process_id = XID._get_process_id()
        
        self._counter = int.from_bytes(os.urandom(3), 'big') & 0xFFFFFF
        self._last_timestamp = 0
        self._lock = threading.Lock()
    
    def generate(self) -> XID:
        """
        生成新的XID
        
        Returns:
            新的XID对象
        """
        with self._lock:
            timestamp = int(time.time())
            
            if timestamp != self._last_timestamp:
                self._last_timestamp = timestamp
                self._counter = int.from_bytes(os.urandom(3), 'big') & 0xFFFFFF
            
            self._counter = (self._counter + 1) & 0xFFFFFF
            
            data = struct.pack('>I', timestamp) + self._machine_id + struct.pack(
                '>H', self._process_id
            ) + struct.pack('>I', self._counter)[1:]
            
            return XID(data)


# 为了兼容性，导出所有公开接口
__all__ = [
    'XID',
    'XIDError',
    'XIDGenerator',
    'generate',
    'from_string',
    'from_bytes',
    'is_valid',
    'extract_timestamp',
    'extract_datetime',
    'compare',
    'batch_generate',
    'parse_info',
    'min_xid',
    'max_xid',
]