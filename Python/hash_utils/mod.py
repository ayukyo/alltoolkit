#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Hash Utilities Module

Comprehensive hash utilities for Python with zero external dependencies.
Provides MD5, SHA1, SHA256, SHA512, HMAC, file hashing, and more.

Author: AllToolkit
License: MIT
"""

import hashlib
import hmac
import os
import binascii
import base64
from typing import Union, Optional, List, Dict, Any
from pathlib import Path


# =============================================================================
# Type Aliases
# =============================================================================

HashInput = Union[str, bytes, bytearray, memoryview]
HashAlgorithm = str  # 'md5', 'sha1', 'sha256', 'sha512', etc.


# =============================================================================
# Constants
# =============================================================================

SUPPORTED_ALGORITHMS = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 
                        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
                        'blake2b', 'blake2s']

DEFAULT_CHUNK_SIZE = 8192  # 8KB chunks for file hashing


# =============================================================================
# Basic Hash Functions
# =============================================================================

def md5(data: HashInput, hex_output: bool = True) -> Union[str, bytes]:
    """
    Calculate MD5 hash of input data.
    
    Args:
        data: Input data (string or bytes)
        hex_output: If True, return hex string; otherwise return bytes
        
    Returns:
        Hash digest as hex string or bytes
        
    Example:
        >>> md5("hello")
        '5d41402abc4b2a76b9719d911017c592'
        >>> md5(b"hello", hex_output=False)
        b']\\x41\\x40\\x2a\\xbc\\x4b\\x2a\\x76\\xb9\\x71\\x9d\\x91\\x10\\x17\\xc5\\x92'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    # Use hexdigest() directly for better performance
    if hex_output:
        return hashlib.md5(data).hexdigest()
    return hashlib.md5(data).digest()


def sha1(data: HashInput, hex_output: bool = True) -> Union[str, bytes]:
    """
    Calculate SHA1 hash of input data.
    
    Args:
        data: Input data (string or bytes)
        hex_output: If True, return hex string; otherwise return bytes
        
    Returns:
        Hash digest as hex string or bytes
        
    Example:
        >>> sha1("hello")
        'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    # Use hexdigest() directly for better performance
    if hex_output:
        return hashlib.sha1(data).hexdigest()
    return hashlib.sha1(data).digest()


def sha256(data: HashInput, hex_output: bool = True) -> Union[str, bytes]:
    """
    Calculate SHA256 hash of input data.
    
    Args:
        data: Input data (string or bytes)
        hex_output: If True, return hex string; otherwise return bytes
        
    Returns:
        Hash digest as hex string or bytes
        
    Example:
        >>> sha256("hello")
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    # Use hexdigest() directly for better performance
    if hex_output:
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(data).digest()


def sha512(data: HashInput, hex_output: bool = True) -> Union[str, bytes]:
    """
    Calculate SHA512 hash of input data.
    
    Args:
        data: Input data (string or bytes)
        hex_output: If True, return hex string; otherwise return bytes
        
    Returns:
        Hash digest as hex string or bytes
        
    Example:
        >>> sha512("hello")  # doctest: +SKIP
        '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    # Use hexdigest() directly for better performance
    if hex_output:
        return hashlib.sha512(data).hexdigest()
    return hashlib.sha512(data).digest()


def hash(data: HashInput, algorithm: HashAlgorithm = 'sha256', 
         hex_output: bool = True) -> Union[str, bytes]:
    """
    Calculate hash using specified algorithm.
    
    Args:
        data: Input data (string or bytes)
        algorithm: Hash algorithm name (md5, sha1, sha256, sha512, etc.)
        hex_output: If True, return hex string; otherwise return bytes
        
    Returns:
        Hash digest as hex string or bytes
        
    Raises:
        ValueError: If algorithm is not supported
        
    Example:
        >>> hash("hello", "md5")
        '5d41402abc4b2a76b9719d911017c592'
        >>> hash("hello", "sha256")
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    try:
        hasher = hashlib.new(algorithm)
        hasher.update(data)
        # Use hexdigest() directly for better performance
        if hex_output:
            return hasher.hexdigest()
        return hasher.digest()
    except ValueError as e:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}. "
                        f"Supported: {', '.join(SUPPORTED_ALGORITHMS)}") from e


def hash_algorithms() -> List[str]:
    """
    Get list of supported hash algorithms.
    
    Returns:
        List of algorithm names
        
    Example:
        >>> 'sha256' in hash_algorithms()
        True
    """
    return SUPPORTED_ALGORITHMS.copy()


# =============================================================================
# HMAC Functions
# =============================================================================

def hmac_hash(data: HashInput, key: HashInput, 
              algorithm: HashAlgorithm = 'sha256',
              hex_output: bool = True) -> Union[str, bytes]:
    """
    Calculate HMAC (Hash-based Message Authentication Code).
    
    Args:
        data: Input data (string or bytes)
        key: Secret key (string or bytes)
        algorithm: Hash algorithm to use
        hex_output: If True, return hex string; otherwise return bytes
        
    Returns:
        HMAC digest as hex string or bytes
        
    Raises:
        ValueError: If algorithm is not supported
        
    Example:
        >>> hmac_hash("message", "secret_key")  # doctest: +SKIP
        'c955b7f8e1c4e8f4c8e8f4c8e8f4c8e8f4c8e8f4c8e8f4c8e8f4c8e8f4c8e8'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    try:
        mac = hmac.new(key, data, algorithm)
        # Use hexdigest() directly for better performance
        if hex_output:
            return mac.hexdigest()
        return mac.digest()
    except ValueError as e:
        raise ValueError(f"Unsupported HMAC algorithm: {algorithm}") from e


def hmac_verify(data: HashInput, key: HashInput, signature: Union[str, bytes],
                algorithm: HashAlgorithm = 'sha256') -> bool:
    """
    Verify HMAC signature.
    
    Args:
        data: Input data (string or bytes)
        key: Secret key (string or bytes)
        signature: Expected signature (hex string or bytes)
        algorithm: Hash algorithm used
        
    Returns:
        True if signature is valid, False otherwise
        
    Example:
        >>> key = "secret"
        >>> sig = hmac_hash("message", key)
        >>> hmac_verify("message", key, sig)
        True
        >>> hmac_verify("tampered", key, sig)
        False
    """
    if isinstance(signature, str):
        signature = bytes.fromhex(signature)
    
    expected = hmac_hash(data, key, algorithm, hex_output=False)
    return hmac.compare_digest(expected, signature)


# =============================================================================
# File Hashing
# =============================================================================

def hash_file(filepath: Union[str, Path], algorithm: HashAlgorithm = 'sha256',
               hex_output: bool = True, chunk_size: int = DEFAULT_CHUNK_SIZE) -> Union[str, bytes]:
    """
    Calculate hash of a file.
    
    Args:
        filepath: Path to the file
        algorithm: Hash algorithm to use
        hex_output: If True, return hex string; otherwise return bytes
        chunk_size: Size of chunks to read (default 8KB, minimum 512 for efficiency)
        
    Returns:
        Hash digest as hex string or bytes
        
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read due to permissions
        ValueError: If algorithm is not supported
        
    Example:
        >>> # Create a temp file for testing
        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        ...     _ = f.write("hello")
        ...     temp_path = f.name
        >>> hash_file(temp_path)  # doctest: +SKIP
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        >>> import os; os.unlink(temp_path)
    
    Note:
        Optimized version:
        - Single-pass algorithm validation using hashlib.new()
        - Adaptive chunk size based on file size for optimal I/O
        - Direct read for small files (< chunk_size)
        - Better error messages with file info
    """
    filepath = Path(filepath)
    
    # 边界处理：快速验证文件存在性和可读性
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if not filepath.is_file():
        raise ValueError(f"Path is not a file: {filepath}")
    
    # 获取文件大小用于优化决策
    try:
        file_size = filepath.stat().st_size
    except OSError as e:
        raise PermissionError(f"Cannot access file stats: {filepath}") from e
    
    # 优化：单次算法验证，避免重复调用 hashlib.new()
    try:
        hasher = hashlib.new(algorithm)
    except ValueError as e:
        raise ValueError(f"Unsupported hash algorithm '{algorithm}'. "
                        f"Supported: {', '.join(SUPPORTED_ALGORITHMS)}") from e
    
    # 优化：自适应 chunk size
    # 小文件直接读取，避免多次 I/O
    # 中等文件使用默认 chunk size
    # 大文件使用更大的 chunk size 提升效率
    if file_size <= 0:
        # 空文件直接返回空数据的哈希
        pass
    elif file_size <= chunk_size:
        # 小文件：直接读取，单次 I/O
        try:
            content = filepath.read_bytes()
            hasher.update(content)
        except PermissionError as e:
            raise PermissionError(f"Permission denied reading file: {filepath}") from e
    else:
        # 大文件：分块读取
        # 对于大文件（>1MB），使用更大的 chunk size
        actual_chunk_size = chunk_size
        if file_size > 1024 * 1024:  # > 1MB
            actual_chunk_size = max(chunk_size, 64 * 1024)  # 至少 64KB
        
        try:
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(actual_chunk_size)
                    if not chunk:
                        break
                    hasher.update(chunk)
        except PermissionError as e:
            raise PermissionError(f"Permission denied reading file: {filepath}") from e
    
    # 优化：直接调用 hexdigest() 或 digest()，避免中间变量
    return hasher.hexdigest() if hex_output else hasher.digest()


def hash_directory(dirpath: Union[str, Path], algorithm: HashAlgorithm = 'sha256',
                   recursive: bool = True, 
                   ignore_patterns: Optional[List[str]] = None) -> Dict[str, str]:
    """
    Calculate hashes for all files in a directory.
    
    Args:
        dirpath: Path to the directory
        algorithm: Hash algorithm to use
        recursive: If True, process subdirectories
        ignore_patterns: List of filename patterns to ignore (e.g., ['*.pyc', '__pycache__'])
        
    Returns:
        Dictionary mapping relative file paths to their hash values
        
    Example:
        >>> # This would hash all files in a directory
        >>> # hashes = hash_directory("/path/to/dir")
        >>> # print(hashes)  # {'file1.txt': 'abc123...', 'subdir/file2.txt': 'def456...'}
    
    Note:
        优化版本（v3）：
        - 提前验证算法避免在文件处理时重复检查
        - 使用 fnmatch 替代简单的模式匹配，支持更复杂的模式
        - 边界处理：空目录、无权限文件
        - 批量预获取文件列表减少迭代器开销
        - 使用生成器表达式优化内存使用
        - 错误信息标准化，便于调试
    """
    import fnmatch
    
    dirpath = Path(dirpath)
    
    # 边界处理：提前验证路径
    if not dirpath.exists():
        raise FileNotFoundError(f"Directory not found: {dirpath}")
    if not dirpath.is_dir():
        raise NotADirectoryError(f"Not a directory: {dirpath}")
    
    # 提前验证算法有效性，避免在文件处理时重复检查
    try:
        # 预创建一个 hasher 用于验证算法有效性
        hashlib.new(algorithm)
    except ValueError as e:
        raise ValueError(f"Unsupported hash algorithm '{algorithm}'. "
                        f"Supported: {', '.join(SUPPORTED_ALGORITHMS)}") from e
    
    ignore_patterns = ignore_patterns or []
    result = {}
    
    # 优化：预编译忽略模式匹配函数
    def should_ignore(filename: str, rel_path: str) -> bool:
        """检查文件是否应该被忽略"""
        # 检查文件名匹配
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(filename, pattern):
                return True
            # 也检查相对路径（支持目录级忽略）
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        return False
    
    # 优化：批量获取文件列表，减少迭代器开销
    if recursive:
        all_files = list(dirpath.rglob('*'))
    else:
        all_files = list(dirpath.glob('*'))
    
    # 边界处理：空目录快速返回
    if not all_files:
        return result
    
    # 批量处理文件，使用生成器优化内存
    file_count = 0
    error_count = 0
    
    for filepath in all_files:
        if not filepath.is_file():
            continue
        
        rel_path = str(filepath.relative_to(dirpath))
        filename = filepath.name
        
        if should_ignore(filename, rel_path):
            continue
        
        file_count += 1
        try:
            result[rel_path] = hash_file(filepath, algorithm)
        except PermissionError:
            # 边界处理：记录权限错误而非跳过
            result[rel_path] = "<error: permission denied>"
            error_count += 1
        except IOError as e:
            # 边界处理：记录IO错误
            result[rel_path] = f"<error: {str(e)[:50]}>"
            error_count += 1
    
    # 返回结果，包含处理统计（可选：用于调试）
    # result['_stats'] = {'files': file_count, 'errors': error_count}
    
    return result


def verify_file_hash(filepath: Union[str, Path], expected_hash: str,
                     algorithm: HashAlgorithm = 'sha256') -> bool:
    """
    Verify that a file matches an expected hash.
    
    Args:
        filepath: Path to the file
        expected_hash: Expected hash value (hex string)
        algorithm: Hash algorithm used
        
    Returns:
        True if hash matches, False otherwise
        
    Example:
        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        ...     _ = f.write("hello")
        ...     temp_path = f.name
        >>> expected = hash_file(temp_path)
        >>> verify_file_hash(temp_path, expected)
        True
        >>> verify_file_hash(temp_path, "wrong_hash")
        False
        >>> import os; os.unlink(temp_path)
    """
    try:
        actual_hash = hash_file(filepath, algorithm)
        return actual_hash == expected_hash
    except (FileNotFoundError, IOError):
        return False


# =============================================================================
# Hash Comparison and Utilities
# =============================================================================

def compare_hashes(hash1: str, hash2: str, case_sensitive: bool = False) -> bool:
    """
    Safely compare two hash values.
    
    Args:
        hash1: First hash value
        hash2: Second hash value
        case_sensitive: If True, compare case-sensitively
        
    Returns:
        True if hashes match, False otherwise
        
    Example:
        >>> compare_hashes("ABC123", "abc123")
        True
        >>> compare_hashes("ABC123", "abc123", case_sensitive=True)
        False
    """
    if not case_sensitive:
        hash1 = hash1.lower()
        hash2 = hash2.lower()
    return hmac.compare_digest(hash1, hash2)


def hash_diff(hash1: str, hash2: str) -> Dict[str, Any]:
    """
    Compare two hashes and return detailed difference info.
    
    Args:
        hash1: First hash value
        hash2: Second hash value
        
    Returns:
        Dictionary with comparison results
        
    Example:
        >>> result = hash_diff("abc123", "abc456")
        >>> result['match']
        False
        >>> result['length_match']
        True
    """
    hash1_lower = hash1.lower()
    hash2_lower = hash2.lower()
    
    return {
        'match': hash1_lower == hash2_lower,
        'length_match': len(hash1) == len(hash2),
        'hash1_length': len(hash1),
        'hash2_length': len(hash2),
        'hash1': hash1,
        'hash2': hash2,
        'differ_at': [i for i, (a, b) in enumerate(zip(hash1_lower, hash2_lower)) if a != b][:10]
    }


# =============================================================================
# Encoding Utilities
# =============================================================================

def hex_to_base64(hex_string: str) -> str:
    """
    Convert hex string to base64.
    
    Args:
        hex_string: Hex-encoded string
        
    Returns:
        Base64-encoded string
        
    Example:
        >>> hex_to_base64("48656c6c6f")  # "Hello" in hex
        'SGVsbG8='
    
    Note:
        优化版本：添加空输入快速返回，
        使用链式调用减少中间变量。
    """
    # 边界处理：空字符串快速返回
    if not hex_string:
        return ''
    
    try:
        # 优化：链式调用，减少中间变量
        return base64.b64encode(bytes.fromhex(hex_string)).decode('ascii')
    except ValueError as e:
        raise ValueError(f"Invalid hex string: {hex_string}") from e


def base64_to_hex(base64_string: str) -> str:
    """
    Convert base64 string to hex.
    
    Args:
        base64_string: Base64-encoded string
        
    Returns:
        Hex-encoded string
        
    Example:
        >>> base64_to_hex("SGVsbG8=")
        '48656c6c6f'
    """
    try:
        binary_data = base64.b64decode(base64_string)
        return binary_data.hex()
    except (binascii.Error, ValueError) as e:
        raise ValueError(f"Invalid base64 string: {base64_string}") from e


def bytes_to_hex(data: Union[bytes, bytearray]) -> str:
    """
    Convert bytes to hex string.
    
    Args:
        data: Bytes or bytearray
        
    Returns:
        Hex-encoded string
        
    Example:
        >>> bytes_to_hex(b"Hello")
        '48656c6c6f'
    """
    return data.hex()


def hex_to_bytes(hex_string: str) -> bytes:
    """
    Convert hex string to bytes.
    
    Args:
        hex_string: Hex-encoded string
        
    Returns:
        Bytes object
        
    Example:
        >>> hex_to_bytes("48656c6c6f")
        b'Hello'
    """
    return bytes.fromhex(hex_string)


# =============================================================================
# Incremental Hashing
# =============================================================================

class IncrementalHasher:
    """
    Incremental hasher for streaming data.
    
    Example:
        >>> hasher = IncrementalHasher('sha256')
        >>> hasher.update("Hello ")
        >>> hasher.update("World")
        >>> hasher.hexdigest()
        'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
    """
    
    def __init__(self, algorithm: HashAlgorithm = 'sha256'):
        """
        Initialize incremental hasher.
        
        Args:
            algorithm: Hash algorithm to use
        """
        self.algorithm = algorithm
        self._hasher = hashlib.new(algorithm)
    
    def update(self, data: HashInput) -> 'IncrementalHasher':
        """
        Update hash with more data.
        
        Args:
            data: Data to add
            
        Returns:
            Self for chaining
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._hasher.update(data)
        return self
    
    def digest(self) -> bytes:
        """
        Get hash digest as bytes.
        
        Returns:
            Hash digest bytes
        """
        return self._hasher.digest()
    
    def hexdigest(self) -> str:
        """
        Get hash digest as hex string.
        
        Returns:
            Hash digest hex string
        """
        return self._hasher.hexdigest()
    
    def reset(self) -> 'IncrementalHasher':
        """
        Reset hasher to initial state.
        
        Returns:
            Self for chaining
        """
        self._hasher = hashlib.new(self.algorithm)
        return self
    
    def copy(self) -> 'IncrementalHasher':
        """
        Create a copy of the current hasher state.
        
        Returns:
            New IncrementalHasher with same state
        """
        new_hasher = IncrementalHasher(self.algorithm)
        new_hasher._hasher = self._hasher.copy()
        return new_hasher


# =============================================================================
# Hash-based Data Structures
# =============================================================================

def hash_key(key: Any, algorithm: HashAlgorithm = 'sha256') -> str:
    """
    Create a hash-based key from any Python object.
    
    Args:
        key: Any hashable Python object
        algorithm: Hash algorithm to use
        
    Returns:
        Hex-encoded hash string
        
    Example:
        >>> hash_key(("user", 123))  # doctest: +SKIP
        'abc123...'
    """
    import pickle
    serialized = pickle.dumps(key, protocol=pickle.HIGHEST_PROTOCOL)
    return hash(serialized, algorithm)


def consistent_hash(data: HashInput, num_buckets: int) -> int:
    """
    Calculate consistent hash for bucket assignment.
    
    Args:
        data: Input data
        num_buckets: Number of buckets
        
    Returns:
        Bucket index (0 to num_buckets-1)
        
    Example:
        >>> bucket = consistent_hash("user123", 10)
        >>> 0 <= bucket < 10
        True
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    hash_value = int(hashlib.md5(data).hexdigest(), 16)
    return hash_value % num_buckets


# =============================================================================
# Password Hashing Utilities (Simple, for non-critical use)
# =============================================================================

def simple_hash_password(password: str, salt: Optional[str] = None) -> Dict[str, str]:
    """
    Create a simple salted password hash.
    
    Note: For production use, use bcrypt, argon2, or scrypt instead.
    This is provided for educational purposes and non-critical applications.
    
    Args:
        password: Plain text password
        salt: Optional salt (generated if not provided)
        
    Returns:
        Dictionary with 'hash', 'salt', and 'algorithm' keys
        
    Example:
        >>> result = simple_hash_password("mypassword")
        >>> 'hash' in result and 'salt' in result
        True
    """
    import secrets
    
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Combine salt and password
    salted = f"{salt}{password}"
    password_hash = sha256(salted)
    
    return {
        'hash': password_hash,
        'salt': salt,
        'algorithm': 'sha256'
    }


def verify_password(password: str, stored_hash: str, salt: str,
                    algorithm: HashAlgorithm = 'sha256') -> bool:
    """
    Verify a password against a stored hash.
    
    Args:
        password: Plain text password to verify
        stored_hash: Previously stored hash
        salt: Salt used for hashing
        algorithm: Hash algorithm used
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> result = simple_hash_password("mypassword")
        >>> verify_password("mypassword", result['hash'], result['salt'])
        True
        >>> verify_password("wrongpassword", result['hash'], result['salt'])
        False
    """
    salted = f"{salt}{password}"
    computed_hash = hash(salted, algorithm)
    return hmac.compare_digest(computed_hash, stored_hash)


# =============================================================================
# Checksum Utilities
# =============================================================================

def crc32(data: HashInput) -> int:
    """
    Calculate CRC32 checksum.
    
    Args:
        data: Input data
        
    Returns:
        CRC32 checksum as unsigned integer
        
    Example:
        >>> crc32("hello")
        907060870
    """
    import zlib
    if isinstance(data, str):
        data = data.encode('utf-8')
    return zlib.crc32(data) & 0xffffffff


def crc32_hex(data: HashInput) -> str:
    """
    Calculate CRC32 checksum as hex string.
    
    Args:
        data: Input data
        
    Returns:
        CRC32 checksum as 8-character hex string
        
    Example:
        >>> crc32_hex("hello")
        '3610a686'
    """
    return format(crc32(data), '08x')


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    # Demo usage
    print("Hash Utilities Demo")
    print("=" * 50)
    
    test_data = "Hello, AllToolkit!"
    print(f"Input: {test_data}")
    print()
    
    print("Basic Hashes:")
    print(f"  MD5:    {md5(test_data)}")
    print(f"  SHA1:   {sha1(test_data)}")
    print(f"  SHA256: {sha256(test_data)}")
    print(f"  SHA512: {sha512(test_data)[:64]}...")
    print()
    
    print("HMAC:")
    secret = "my-secret-key"
    mac = hmac_hash(test_data, secret)
    print(f"  HMAC-SHA256: {mac}")
    print(f"  Verified: {hmac_verify(test_data, secret, mac)}")
    print()
    
    print("Encoding:")
    print(f"  Hex to Base64: {hex_to_base64('48656c6c6f')}")
    print(f"  Base64 to Hex: {base64_to_hex('SGVsbG8=')}")
    print()
    
    print("CRC32:")
    print(f"  CRC32: {crc32(test_data)}")
    print(f"  CRC32 Hex: {crc32_hex(test_data)}")
    print()
    
    print("Incremental Hashing:")
    hasher = IncrementalHasher('sha256')
    hasher.update("Hello, ")
    hasher.update("AllToolkit!")
    print(f"  Result: {hasher.hexdigest()}")
    print()
    
    print("Supported Algorithms:")
    for algo in hash_algorithms():
        print(f"  - {algo}")
