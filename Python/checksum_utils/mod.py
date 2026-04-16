"""
checksum_utils - 零依赖校验和计算工具库

提供多种校验和算法实现：
- CRC32 / CRC64
- Adler32
- Fletcher-16 / Fletcher-32 / Fletcher-64
- Internet Checksum (IP/TCP)
- 简单校验和 (Sum / XOR)

特性：
- 零外部依赖
- 支持字节、字符串、文件
- 支持增量计算
- 纯 Python 实现
"""

from typing import Union, Optional
import struct


class CRC32:
    """CRC32 校验和计算器（IEEE 802.3 多项式）"""
    
    # IEEE 802.3 标准多项式: x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1
    POLY = 0xEDB88320
    
    _table: Optional[list] = None
    
    @classmethod
    def _init_table(cls):
        """初始化 CRC32 查找表"""
        if cls._table is not None:
            return
        cls._table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ cls.POLY
                else:
                    crc >>= 1
            cls._table.append(crc)
    
    @classmethod
    def calculate(cls, data: Union[bytes, str], crc: int = 0) -> int:
        """
        计算 CRC32 校验和
        
        Args:
            data: 输入数据（字节或字符串）
            crc: 初始 CRC 值（用于增量计算）
        
        Returns:
            CRC32 校验和（无符号 32 位整数）
        """
        cls._init_table()
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        crc = crc ^ 0xFFFFFFFF
        for byte in data:
            crc = cls._table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
        return crc ^ 0xFFFFFFFF
    
    @classmethod
    def calculate_file(cls, filepath: str, chunk_size: int = 8192) -> int:
        """
        计算文件的 CRC32 校验和
        
        Args:
            filepath: 文件路径
            chunk_size: 分块大小
        
        Returns:
            CRC32 校验和
        """
        crc = 0
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                crc = cls.calculate(chunk, crc)
        return crc


class CRC64:
    """CRC64 校验和计算器（ISO 3309 多项式）"""
    
    # ISO 3309 多项式
    POLY = 0xC96C5795D7870F42
    
    _table: Optional[list] = None
    
    @classmethod
    def _init_table(cls):
        """初始化 CRC64 查找表"""
        if cls._table is not None:
            return
        cls._table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ cls.POLY
                else:
                    crc >>= 1
            cls._table.append(crc)
    
    @classmethod
    def calculate(cls, data: Union[bytes, str], crc: int = 0) -> int:
        """
        计算 CRC64 校验和
        
        Args:
            data: 输入数据
            crc: 初始 CRC 值
        
        Returns:
            CRC64 校验和
        """
        cls._init_table()
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        crc = crc ^ 0xFFFFFFFFFFFFFFFF
        for byte in data:
            crc = cls._table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
        return crc ^ 0xFFFFFFFFFFFFFFFF
    
    @classmethod
    def calculate_file(cls, filepath: str, chunk_size: int = 8192) -> int:
        """计算文件的 CRC64 校验和"""
        crc = 0
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                crc = cls.calculate(chunk, crc)
        return crc


class Adler32:
    """Adler32 校验和计算器"""
    
    MOD_ADLER = 65521
    
    @classmethod
    def calculate(cls, data: Union[bytes, str], adler: int = 1) -> int:
        """
        计算 Adler32 校验和
        
        Args:
            data: 输入数据
            adler: 初始值（用于增量计算）
        
        Returns:
            Adler32 校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        a = adler & 0xFFFF
        b = (adler >> 16) & 0xFFFF
        
        for byte in data:
            a = (a + byte) % cls.MOD_ADLER
            b = (b + a) % cls.MOD_ADLER
        
        return (b << 16) | a
    
    @classmethod
    def calculate_file(cls, filepath: str, chunk_size: int = 8192) -> int:
        """计算文件的 Adler32 校验和"""
        adler = 1
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                adler = cls.calculate(chunk, adler)
        return adler


class Fletcher:
    """Fletcher 校验和计算器"""
    
    @staticmethod
    def fletcher16(data: Union[bytes, str]) -> int:
        """
        计算 Fletcher-16 校验和
        
        Args:
            data: 输入数据
        
        Returns:
            16 位校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        sum1 = 0
        sum2 = 0
        
        for byte in data:
            sum1 = (sum1 + byte) % 255
            sum2 = (sum2 + sum1) % 255
        
        return (sum2 << 8) | sum1
    
    @staticmethod
    def fletcher32(data: Union[bytes, str]) -> int:
        """
        计算 Fletcher-32 校验和
        
        Args:
            data: 输入数据
        
        Returns:
            32 位校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # 处理为 16 位字
        words = []
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                words.append((data[i + 1] << 8) | data[i])
            else:
                words.append(data[i])
        
        sum1 = 0
        sum2 = 0
        mod = 65535
        
        for word in words:
            sum1 = (sum1 + word) % mod
            sum2 = (sum2 + sum1) % mod
        
        return (sum2 << 16) | sum1
    
    @staticmethod
    def fletcher64(data: Union[bytes, str]) -> int:
        """
        计算 Fletcher-64 校验和
        
        Args:
            data: 输入数据
        
        Returns:
            64 位校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # 处理为 32 位字
        words = []
        for i in range(0, len(data), 4):
            word = 0
            for j in range(4):
                if i + j < len(data):
                    word |= data[i + j] << (j * 8)
            words.append(word)
        
        sum1 = 0
        sum2 = 0
        mod = 0xFFFFFFFF
        
        for word in words:
            sum1 = (sum1 + word) % mod
            sum2 = (sum2 + sum1) % mod
        
        return (sum2 << 32) | sum1


class InternetChecksum:
    """Internet Checksum (IP/TCP/UDP 校验和)"""
    
    @staticmethod
    def calculate(data: Union[bytes, str]) -> int:
        """
        计算 Internet 校验和（RFC 1071）
        
        Args:
            data: 输入数据
        
        Returns:
            16 位校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # 补齐到偶数长度
        if len(data) % 2 == 1:
            data = data + b'\x00'
        
        # 计算所有 16 位字的和
        total = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) | data[i + 1]
            total += word
        
        # 折叠进位
        while total >> 16:
            total = (total & 0xFFFF) + (total >> 16)
        
        return ~total & 0xFFFF
    
    @staticmethod
    def verify(data: Union[bytes, str], checksum: int) -> bool:
        """
        验证 Internet 校验和
        
        Args:
            data: 输入数据（包含校验和）
            checksum: 校验和值
        
        Returns:
            验证结果
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # 补齐到偶数长度
        if len(data) % 2 == 1:
            data = data + b'\x00'
        
        total = checksum
        for i in range(0, len(data), 2):
            word = (data[i] << 8) | data[i + 1]
            total += word
        
        # 折叠进位
        while total >> 16:
            total = (total & 0xFFFF) + (total >> 16)
        
        return total == 0xFFFF


class SimpleChecksum:
    """简单校验和算法"""
    
    @staticmethod
    def sum8(data: Union[bytes, str]) -> int:
        """
        计算 8 位求和校验和
        
        Args:
            data: 输入数据
        
        Returns:
            8 位校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return sum(data) & 0xFF
    
    @staticmethod
    def sum16(data: Union[bytes, str]) -> int:
        """
        计算 16 位求和校验和
        
        Args:
            data: 输入数据
        
        Returns:
            16 位校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        total = 0
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                total += (data[i] << 8) | data[i + 1]
            else:
                total += data[i]
        return total & 0xFFFF
    
    @staticmethod
    def sum32(data: Union[bytes, str]) -> int:
        """
        计算 32 位求和校验和
        
        Args:
            data: 输入数据
        
        Returns:
            32 位校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        total = 0
        for i in range(0, len(data), 4):
            word = 0
            for j in range(4):
                if i + j < len(data):
                    word |= data[i + j] << (j * 8)
            total += word
        return total & 0xFFFFFFFF
    
    @staticmethod
    def xor8(data: Union[bytes, str]) -> int:
        """
        计算 8 位异或校验和
        
        Args:
            data: 输入数据
        
        Returns:
            8 位异或校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        result = 0
        for byte in data:
            result ^= byte
        return result
    
    @staticmethod
    def lrc(data: Union[bytes, str]) -> int:
        """
        计算 LRC (Longitudinal Redundancy Check) 校验和
        
        Args:
            data: 输入数据
        
        Returns:
            LRC 校验和
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        lrc = 0
        for byte in data:
            lrc = (lrc + byte) & 0xFF
        return ((~lrc + 1) & 0xFF)


class ChecksumCalculator:
    """
    统一校验和计算接口
    
    提供便捷的静态方法计算各种校验和
    """
    
    @staticmethod
    def crc32(data: Union[bytes, str]) -> int:
        """计算 CRC32 校验和"""
        return CRC32.calculate(data)
    
    @staticmethod
    def crc64(data: Union[bytes, str]) -> int:
        """计算 CRC64 校验和"""
        return CRC64.calculate(data)
    
    @staticmethod
    def adler32(data: Union[bytes, str]) -> int:
        """计算 Adler32 校验和"""
        return Adler32.calculate(data)
    
    @staticmethod
    def fletcher16(data: Union[bytes, str]) -> int:
        """计算 Fletcher-16 校验和"""
        return Fletcher.fletcher16(data)
    
    @staticmethod
    def fletcher32(data: Union[bytes, str]) -> int:
        """计算 Fletcher-32 校验和"""
        return Fletcher.fletcher32(data)
    
    @staticmethod
    def fletcher64(data: Union[bytes, str]) -> int:
        """计算 Fletcher-64 校验和"""
        return Fletcher.fletcher64(data)
    
    @staticmethod
    def internet(data: Union[bytes, str]) -> int:
        """计算 Internet 校验和"""
        return InternetChecksum.calculate(data)
    
    @staticmethod
    def sum8(data: Union[bytes, str]) -> int:
        """计算 8 位求和校验和"""
        return SimpleChecksum.sum8(data)
    
    @staticmethod
    def sum16(data: Union[bytes, str]) -> int:
        """计算 16 位求和校验和"""
        return SimpleChecksum.sum16(data)
    
    @staticmethod
    def sum32(data: Union[bytes, str]) -> int:
        """计算 32 位求和校验和"""
        return SimpleChecksum.sum32(data)
    
    @staticmethod
    def xor8(data: Union[bytes, str]) -> int:
        """计算 8 位异或校验和"""
        return SimpleChecksum.xor8(data)
    
    @staticmethod
    def lrc(data: Union[bytes, str]) -> int:
        """计算 LRC 校验和"""
        return SimpleChecksum.lrc(data)
    
    @staticmethod
    def file_crc32(filepath: str) -> int:
        """计算文件的 CRC32 校验和"""
        return CRC32.calculate_file(filepath)
    
    @staticmethod
    def file_crc64(filepath: str) -> int:
        """计算文件的 CRC64 校验和"""
        return CRC64.calculate_file(filepath)
    
    @staticmethod
    def file_adler32(filepath: str) -> int:
        """计算文件的 Adler32 校验和"""
        return Adler32.calculate_file(filepath)
    
    @staticmethod
    def to_hex(value: int, width: int = 8) -> str:
        """
        将校验和转换为十六进制字符串
        
        Args:
            value: 校验和值
            width: 十六进制宽度
        
        Returns:
            十六进制字符串
        """
        return format(value, f'0{width}x').upper()
    
    @staticmethod
    def calculate_all(data: Union[bytes, str]) -> dict:
        """
        计算所有支持的校验和
        
        Args:
            data: 输入数据
        
        Returns:
            包含所有校验和的字典
        """
        return {
            'crc32': ChecksumCalculator.crc32(data),
            'crc32_hex': ChecksumCalculator.to_hex(ChecksumCalculator.crc32(data), 8),
            'crc64': ChecksumCalculator.crc64(data),
            'crc64_hex': ChecksumCalculator.to_hex(ChecksumCalculator.crc64(data), 16),
            'adler32': ChecksumCalculator.adler32(data),
            'adler32_hex': ChecksumCalculator.to_hex(ChecksumCalculator.adler32(data), 8),
            'fletcher16': ChecksumCalculator.fletcher16(data),
            'fletcher32': ChecksumCalculator.fletcher32(data),
            'fletcher64': ChecksumCalculator.fletcher64(data),
            'internet': ChecksumCalculator.internet(data),
            'sum8': ChecksumCalculator.sum8(data),
            'sum16': ChecksumCalculator.sum16(data),
            'sum32': ChecksumCalculator.sum32(data),
            'xor8': ChecksumCalculator.xor8(data),
            'lrc': ChecksumCalculator.lrc(data),
        }


# 便捷函数
def crc32(data: Union[bytes, str]) -> int:
    """计算 CRC32 校验和"""
    return CRC32.calculate(data)


def crc64(data: Union[bytes, str]) -> int:
    """计算 CRC64 校验和"""
    return CRC64.calculate(data)


def adler32(data: Union[bytes, str]) -> int:
    """计算 Adler32 校验和"""
    return Adler32.calculate(data)


def fletcher16(data: Union[bytes, str]) -> int:
    """计算 Fletcher-16 校验和"""
    return Fletcher.fletcher16(data)


def fletcher32(data: Union[bytes, str]) -> int:
    """计算 Fletcher-32 校验和"""
    return Fletcher.fletcher32(data)


def fletcher64(data: Union[bytes, str]) -> int:
    """计算 Fletcher-64 校验和"""
    return Fletcher.fletcher64(data)


def internet_checksum(data: Union[bytes, str]) -> int:
    """计算 Internet 校验和"""
    return InternetChecksum.calculate(data)


if __name__ == '__main__':
    # 演示用法
    test_data = "Hello, World!"
    
    print(f"测试数据: {test_data}")
    print(f"CRC32: {ChecksumCalculator.to_hex(crc32(test_data), 8)}")
    print(f"CRC64: {ChecksumCalculator.to_hex(crc64(test_data), 16)}")
    print(f"Adler32: {ChecksumCalculator.to_hex(adler32(test_data), 8)}")
    print(f"Fletcher-16: {fletcher16(test_data)}")
    print(f"Fletcher-32: {fletcher32(test_data)}")
    print(f"Internet: {internet_checksum(test_data)}")
    print(f"XOR8: {ChecksumCalculator.xor8(test_data)}")
    print(f"LRC: {ChecksumCalculator.lrc(test_data)}")