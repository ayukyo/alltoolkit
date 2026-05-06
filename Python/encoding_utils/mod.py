"""
Encoding Utilities - 编码处理工具集

提供多种编码格式的转换功能。零外部依赖，纯 Python 实现（兼容 Python 3.6+）。

支持的编码格式：
- Base64 (标准/URL-safe)
- Base32 (标准)
- Base58 (Bitcoin)
- URL 编码
- Hex 编码
- Quoted-printable
- Unicode 规范化

Author: AllToolkit
Version: 1.0.0
"""

import base64
import binascii
import quopri
import urllib.parse
import unicodedata
import re
from typing import Union, Optional, Tuple, List


# ============================================================================
# Base64 编码
# ============================================================================

def base64_encode(data: Union[str, bytes], url_safe: bool = False) -> str:
    """
    Base64 编码
    
    Args:
        data: 输入数据（字符串或字节）
        url_safe: 是否使用 URL-safe 编码（替换 +/ 为 -_）
        
    Returns:
        Base64 编码字符串
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    encoded = base64.b64encode(data).decode('ascii')
    
    if url_safe:
        encoded = encoded.replace('+', '-').replace('/', '_')
    
    return encoded.rstrip('=')


def base64_decode(encoded: str, url_safe: bool = False) -> bytes:
    """
    Base64 解码
    
    Args:
        encoded: Base64 编码字符串
        url_safe: 是否是 URL-safe 编码
        
    Returns:
        解码后的字节
        
    Raises:
        ValueError: 无效的 Base64 数据
    """
    # 恢复 URL-safe 字符
    if url_safe:
        encoded = encoded.replace('-', '+').replace('_', '/')
    
    # 补齐 padding
    padding = 4 - (len(encoded) % 4)
    if padding != 4:
        encoded += '=' * padding
    
    try:
        return base64.b64decode(encoded)
    except binascii.Error as e:
        raise ValueError(f"无效的 Base64 数据: {e}")


def base64_encode_json(obj: dict) -> str:
    """
    将 JSON 对象编码为 Base64
    
    Args:
        obj: JSON 对象
        
    Returns:
        Base64 编码字符串
    """
    import json
    json_str = json.dumps(obj, separators=(',', ':'))
    return base64_encode(json_str)


def base64_decode_json(encoded: str) -> dict:
    """
    从 Base64 解码 JSON 对象
    
    Args:
        encoded: Base64 编码字符串
        
    Returns:
        JSON 对象
        
    Raises:
        ValueError: 无效的数据或 JSON
    """
    import json
    try:
        json_bytes = base64_decode(encoded)
        return json.loads(json_bytes.decode('utf-8'))
    except json.JSONDecodeError as e:
        raise ValueError(f"无效的 JSON 数据: {e}")


# ============================================================================
# Base32 编码
# ============================================================================

def base32_encode(data: Union[str, bytes]) -> str:
    """
    Base32 编码
    
    Args:
        data: 输入数据
        
    Returns:
        Base32 编码字符串（无 padding）
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    encoded = base64.b32encode(data).decode('ascii')
    return encoded.rstrip('=')


def base32_decode(encoded: str) -> bytes:
    """
    Base32 解码
    
    Args:
        encoded: Base32 编码字符串
        
    Returns:
        解码后的字节
        
    Raises:
        ValueError: 无效的 Base32 数据
    """
    # 补齐 padding
    padding = 8 - (len(encoded) % 8)
    if padding != 8:
        encoded += '=' * padding
    
    try:
        return base64.b32decode(encoded.upper())  # Base32 要求大写
    except binascii.Error as e:
        raise ValueError(f"无效的 Base32 数据: {e}")


# ============================================================================
# Base58 编码
# ============================================================================

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def base58_encode(data: Union[str, bytes]) -> str:
    """
    Base58 编码（Bitcoin 标准）
    
    Args:
        data: 输入数据
        
    Returns:
        Base58 编码字符串
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # 统计前导零字节
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    # 转换为整数（忽略前导零）
    num = int.from_bytes(data, 'big')
    
    # 编码
    result = []
    while num > 0:
        num, remainder = divmod(num, 58)
        result.append(BASE58_ALPHABET[remainder])
    
    # 添加前导 '1' 字符（对应零字节）
    return '1' * leading_zeros + ''.join(reversed(result))


def base58_decode(encoded: str) -> bytes:
    """
    Base58 解码
    
    Args:
        encoded: Base58 编码字符串
        
    Returns:
        解码后的字节
        
    Raises:
        ValueError: 无效的 Base58 数据
    """
    # 检查有效字符
    for char in encoded:
        if char not in BASE58_ALPHABET:
            raise ValueError(f"无效的 Base58 字符: {char}")
    
    # 统计前导 '1' 字符（对应零字节）
    leading_zeros = 0
    for char in encoded:
        if char == '1':
            leading_zeros += 1
        else:
            break
    
    # 解码为整数
    num = 0
    for char in encoded:
        num = num * 58 + BASE58_ALPHABET.index(char)
    
    # 转换为字节
    if num == 0:
        return bytes(leading_zeros)
    
    # 计算需要的字节数
    hex_str = hex(num)[2:]  # 移除 '0x'
    if len(hex_str) % 2:
        hex_str = '0' + hex_str
    
    result = bytes.fromhex(hex_str)
    
    return bytes(leading_zeros) + result


# ============================================================================
# URL 编码
# ============================================================================

def url_encode(data: str, safe: str = '', encoding: str = 'utf-8') -> str:
    """
    URL 编码
    
    Args:
        data: 输入字符串
        safe: 不编码的安全字符
        encoding: 编码方式
        
    Returns:
        URL 编码字符串
    """
    return urllib.parse.quote(data, safe=safe, encoding=encoding)


def url_decode(encoded: str, encoding: str = 'utf-8') -> str:
    """
    URL 解码
    
    Args:
        encoded: URL 编码字符串
        encoding: 编码方式
        
    Returns:
        解码后的字符串
    """
    return urllib.parse.unquote(encoded, encoding=encoding)


def url_encode_query(params: dict) -> str:
    """
    编码 URL 查询参数
    
    Args:
        params: 参数字典
        
    Returns:
        URL 查询字符串
    """
    return urllib.parse.urlencode(params)


def url_decode_query(query: str) -> dict:
    """
    解码 URL 查询参数
    
    Args:
        query: URL 查询字符串
        
    Returns:
        参数字典
    """
    return dict(urllib.parse.parse_qsl(query))


def url_encode_all(data: str) -> str:
    """
    编码所有字符（包括字母）
    
    Args:
        data: 输入字符串
        
    Returns:
        全编码字符串
    """
    return ''.join(f'%{ord(c):02x}' for c in data)


# ============================================================================
# Hex 编码
# ============================================================================

def hex_encode(data: Union[str, bytes]) -> str:
    """
    Hex（十六进制）编码
    
    Args:
        data: 输入数据
        
    Returns:
        Hex 编码字符串
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return binascii.hexlify(data).decode('ascii')


def hex_decode(encoded: str) -> bytes:
    """
    Hex 解码
    
    Args:
        encoded: Hex 编码字符串
        
    Returns:
        解码后的字节
        
    Raises:
        ValueError: 无效的 Hex 数据
    """
    try:
        return binascii.unhexlify(encoded)
    except binascii.Error as e:
        raise ValueError(f"无效的 Hex 数据: {e}")


def hex_encode_with_prefix(data: Union[str, bytes]) -> str:
    """
    Hex 编码（带 0x 前缀）
    """
    return '0x' + hex_encode(data)


def hex_decode_with_prefix(encoded: str) -> bytes:
    """
    Hex 解码（支持 0x 前缀）
    """
    if encoded.startswith('0x') or encoded.startswith('0X'):
        encoded = encoded[2:]
    return hex_decode(encoded)


# ============================================================================
# Quoted-printable 编码
# ============================================================================

def quoted_printable_encode(data: Union[str, bytes]) -> str:
    """
    Quoted-printable 编码
    
    Args:
        data: 输入数据
        
    Returns:
        Quoted-printable 编码字符串
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    return quopri.encodestring(data).decode('ascii')


def quoted_printable_decode(encoded: str) -> bytes:
    """
    Quoted-printable 解码
    
    Args:
        encoded: Quoted-printable 编码字符串
        
    Returns:
        解码后的字节
    """
    return quopri.decodestring(encoded.encode('ascii'))


# ============================================================================
# Unicode 规范化
# ============================================================================

def unicode_normalize_nfc(text: str) -> str:
    """
    Unicode NFC 规范化（规范化形式 C）
    """
    return unicodedata.normalize('NFC', text)


def unicode_normalize_nfd(text: str) -> str:
    """
    Unicode NFD 规范化（规范化形式 D）
    """
    return unicodedata.normalize('NFD', text)


def unicode_normalize_nfkc(text: str) -> str:
    """
    Unicode NFKC 规范化（规范化形式 KC）
    """
    return unicodedata.normalize('NFKC', text)


def unicode_normalize_nfkd(text: str) -> str:
    """
    Unicode NFKD 规范化（规范化形式 KD）
    """
    return unicodedata.normalize('NFKD', text)


def unicode_remove_accents(text: str) -> str:
    """
    移除重音符号
    
    Args:
        text: 输入文本
        
    Returns:
        移除重音后的文本
    """
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')


# ============================================================================
# 编码检测
# ============================================================================

def detect_base64(s: str) -> bool:
    """
    检测字符串是否可能是 Base64 编码
    """
    if len(s) < 4:
        return False
    
    pattern = r'^[A-Za-z0-9+/]+=*$'
    if not re.match(pattern, s):
        return False
    
    try:
        base64_decode(s)
        return True
    except ValueError:
        return False


def detect_hex(s: str) -> bool:
    """
    检测字符串是否可能是 Hex 编码
    """
    if s.startswith('0x') or s.startswith('0X'):
        s = s[2:]
    
    if len(s) < 4 or len(s) % 2 != 0:
        return False
    
    return bool(re.match(r'^[0-9a-fA-F]+$', s))


def detect_url_encoded(s: str) -> bool:
    """
    检测字符串是否包含 URL 编码
    """
    return bool(re.search(r'%[0-9A-Fa-f]{2}', s))


def detect_encoding(s: str) -> Optional[str]:
    """
    尝试检测字符串的编码类型
    """
    # 按顺序检测，优先检测更严格的格式
    if detect_hex(s) and len(s) >= 8:  # Hex 通常较长
        return 'hex'
    
    if detect_base64(s):
        return 'base64'
    
    if detect_url_encoded(s):
        return 'url'
    
    return None


def auto_decode(s: str) -> Tuple[str, Optional[str]]:
    """
    自动检测并解码字符串
    
    Returns:
        (解码后的字符串, 使用的编码类型)
    """
    encoding = detect_encoding(s)
    
    if encoding == 'base64':
        try:
            return base64_decode(s).decode('utf-8'), 'base64'
        except UnicodeDecodeError:
            pass
    
    if encoding == 'hex':
        try:
            return hex_decode(s).decode('utf-8'), 'hex'
        except UnicodeDecodeError:
            pass
    
    if encoding == 'url':
        return url_decode(s), 'url'
    
    return s, None


# ============================================================================
# 编码信息
# ============================================================================

def count_bytes(s: str, encoding: str = 'utf-8') -> int:
    """
    计算字符串的字节数
    """
    return len(s.encode(encoding))


def get_unicode_name(char: str) -> Optional[str]:
    """
    获取 Unicode 字符的名称
    """
    try:
        return unicodedata.name(char)
    except ValueError:
        return None


def get_unicode_category(char: str) -> str:
    """
    获取 Unicode 字符的分类
    """
    return unicodedata.category(char)


# ============================================================================
# 批量操作
# ============================================================================

def batch_encode(items: List[str], encoding: str = 'base64') -> List[str]:
    """
    批量编码字符串列表
    """
    encoders = {
        'base64': base64_encode,
        'base32': base32_encode,
        'base58': base58_encode,
        'hex': hex_encode,
        'url': url_encode,
    }
    
    encoder = encoders.get(encoding)
    if not encoder:
        raise ValueError(f"不支持的编码类型: {encoding}")
    
    return [encoder(item) for item in items]


def batch_decode(items: List[str], encoding: str = 'base64') -> List[str]:
    """
    批量解码字符串列表
    """
    decoders = {
        'base64': lambda x: base64_decode(x).decode('utf-8'),
        'base32': lambda x: base32_decode(x).decode('utf-8'),
        'base58': lambda x: base58_decode(x).decode('utf-8'),
        'hex': lambda x: hex_decode(x).decode('utf-8'),
        'url': url_decode,
    }
    
    decoder = decoders.get(encoding)
    if not decoder:
        raise ValueError(f"不支持的编码类型: {encoding}")
    
    return [decoder(item) for item in items]


def convert_encoding(encoded: str, from_encoding: str, to_encoding: str) -> str:
    """
    将一种编码转换为另一种编码
    """
    decoders = {
        'base64': lambda x: base64_decode(x).decode('utf-8'),
        'base32': lambda x: base32_decode(x).decode('utf-8'),
        'base58': lambda x: base58_decode(x).decode('utf-8'),
        'hex': lambda x: hex_decode(x).decode('utf-8'),
        'url': url_decode,
    }
    
    encoders = {
        'base64': base64_encode,
        'base32': base32_encode,
        'base58': base58_encode,
        'hex': hex_encode,
        'url': url_encode,
    }
    
    if from_encoding not in decoders:
        raise ValueError(f"不支持的源编码类型: {from_encoding}")
    
    if to_encoding not in encoders:
        raise ValueError(f"不支持的目标编码类型: {to_encoding}")
    
    decoded = decoders[from_encoding](encoded)
    return encoders[to_encoding](decoded)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # Base64
    'base64_encode', 'base64_decode', 'base64_encode_json', 'base64_decode_json',
    
    # Base32
    'base32_encode', 'base32_decode',
    
    # Base58
    'base58_encode', 'base58_decode', 'BASE58_ALPHABET',
    
    # URL
    'url_encode', 'url_decode', 'url_encode_query', 'url_decode_query', 'url_encode_all',
    
    # Hex
    'hex_encode', 'hex_decode', 'hex_encode_with_prefix', 'hex_decode_with_prefix',
    
    # Quoted-printable
    'quoted_printable_encode', 'quoted_printable_decode',
    
    # Unicode
    'unicode_normalize_nfc', 'unicode_normalize_nfd', 'unicode_normalize_nfkc',
    'unicode_normalize_nfkd', 'unicode_remove_accents',
    
    # 检测
    'detect_base64', 'detect_hex', 'detect_url_encoded', 'detect_encoding', 'auto_decode',
    
    # 信息
    'count_bytes', 'get_unicode_name', 'get_unicode_category',
    
    # 批量操作
    'batch_encode', 'batch_decode',
    
    # 转换
    'convert_encoding',
]