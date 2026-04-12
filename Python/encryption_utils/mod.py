"""
AllToolkit - Python Encryption Utilities

A zero-dependency, production-ready encryption and security utility module.
Supports hashing, HMAC, encryption/decryption, secure random generation, and more.

Author: AllToolkit
License: MIT
"""

import hashlib
import hmac
import secrets
import base64
import os
import struct
import time
from typing import Optional, Union, List, Tuple, Dict, Any
from dataclasses import dataclass


# Type aliases
BytesLike = Union[bytes, bytearray, memoryview]
StringOrBytes = Union[str, bytes]


class EncryptionError(Exception):
    """Base exception for encryption operations."""
    pass


class DecryptionError(EncryptionError):
    """Exception raised when decryption fails."""
    pass


class HashAlgorithm:
    """Supported hash algorithms."""
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"
    SHA3_256 = "sha3_256"
    SHA3_512 = "sha3_512"
    BLAKE2B = "blake2b"
    BLAKE2S = "blake2s"


@dataclass
class HashResult:
    """Result of a hash operation."""
    algorithm: str
    hex_digest: str
    bytes_digest: bytes
    input_length: int
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
    
    def verify(self, data: StringOrBytes) -> bool:
        """Verify that data matches this hash."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hmac.compare_digest(self.bytes_digest, hashlib.new(self.algorithm, data).digest())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'algorithm': self.algorithm,
            'hex': self.hex_digest,
            'input_length': self.input_length,
            'timestamp': self.timestamp,
        }


def _to_bytes(data: StringOrBytes) -> bytes:
    """Convert string or bytes to bytes."""
    if isinstance(data, str):
        return data.encode('utf-8')
    return bytes(data)


def _generate_key(length: int = 32) -> bytes:
    """Generate a cryptographically secure random key."""
    return secrets.token_bytes(length)


# =============================================================================
# Hashing Functions
# =============================================================================

def hash_data(
    data: StringOrBytes,
    algorithm: str = HashAlgorithm.SHA256,
    salt: Optional[StringOrBytes] = None,
) -> HashResult:
    """
    Hash data using specified algorithm.
    
    Args:
        data: Data to hash
        algorithm: Hash algorithm (default: SHA256)
        salt: Optional salt to prepend
        
    Returns:
        HashResult with hash and metadata
    """
    data_bytes = _to_bytes(data)
    
    if salt is not None:
        salt_bytes = _to_bytes(salt)
        data_bytes = salt_bytes + data_bytes
    
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(data_bytes)
    
    return HashResult(
        algorithm=algorithm,
        hex_digest=hash_obj.hexdigest(),
        bytes_digest=hash_obj.digest(),
        input_length=len(data),
    )


def hash_file(
    filepath: str,
    algorithm: str = HashAlgorithm.SHA256,
    chunk_size: int = 8192,
) -> HashResult:
    """
    Hash a file's contents.
    
    Args:
        filepath: Path to file
        algorithm: Hash algorithm (default: SHA256)
        chunk_size: Size of chunks to read
        
    Returns:
        HashResult with hash and metadata
    """
    hash_obj = hashlib.new(algorithm)
    file_size = os.path.getsize(filepath)
    
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hash_obj.update(chunk)
    
    return HashResult(
        algorithm=algorithm,
        hex_digest=hash_obj.hexdigest(),
        bytes_digest=hash_obj.digest(),
        input_length=file_size,
    )


def verify_hash(
    data: StringOrBytes,
    expected_hash: str,
    algorithm: str = HashAlgorithm.SHA256,
    salt: Optional[StringOrBytes] = None,
) -> bool:
    """
    Verify data against expected hash (timing-safe).
    
    Args:
        data: Data to verify
        expected_hash: Expected hex hash
        algorithm: Hash algorithm
        salt: Optional salt
        
    Returns:
        True if hash matches
    """
    result = hash_data(data, algorithm, salt)
    return hmac.compare_digest(result.hex_digest, expected_hash)


def hash_password(
    password: str,
    salt: Optional[bytes] = None,
    iterations: int = 100000,
) -> Dict[str, str]:
    """
    Hash a password securely using PBKDF2.
    
    Args:
        password: Password to hash
        salt: Optional salt (generated if None)
        iterations: Number of iterations (default: 100000)
        
    Returns:
        Dictionary with salt, hash, and algorithm
    """
    if salt is None:
        salt = _generate_key(32)
    else:
        salt = _to_bytes(salt)
    
    password_bytes = _to_bytes(password)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations)
    
    return {
        'algorithm': 'pbkdf2_sha256',
        'iterations': str(iterations),
        'salt': base64.b64encode(salt).decode('ascii'),
        'hash': base64.b64encode(hash_bytes).decode('ascii'),
    }


def verify_password(
    password: str,
    stored_hash: Dict[str, str],
) -> bool:
    """
    Verify password against stored hash.
    
    Args:
        password: Password to verify
        stored_hash: Previously generated hash dict
        
    Returns:
        True if password matches
    """
    if stored_hash.get('algorithm') != 'pbkdf2_sha256':
        raise EncryptionError(f"Unsupported algorithm: {stored_hash.get('algorithm')}")
    
    salt = base64.b64decode(stored_hash['salt'])
    iterations = int(stored_hash['iterations'])
    expected_hash = base64.b64decode(stored_hash['hash'])
    
    password_bytes = _to_bytes(password)
    computed_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations)
    
    return hmac.compare_digest(computed_hash, expected_hash)


# =============================================================================
# HMAC Functions
# =============================================================================

def compute_hmac(
    data: StringOrBytes,
    key: StringOrBytes,
    algorithm: str = "sha256",
) -> str:
    """
    Compute HMAC for data.
    
    Args:
        data: Data to sign
        key: Secret key
        algorithm: Hash algorithm for HMAC
        
    Returns:
        Hex-encoded HMAC
    """
    data_bytes = _to_bytes(data)
    key_bytes = _to_bytes(key)
    
    mac = hmac.new(key_bytes, data_bytes, algorithm)
    return mac.hexdigest()


def verify_hmac(
    data: StringOrBytes,
    signature: str,
    key: StringOrBytes,
    algorithm: str = "sha256",
) -> bool:
    """
    Verify HMAC signature (timing-safe).
    
    Args:
        data: Data that was signed
        signature: Expected signature (hex)
        key: Secret key
        algorithm: Hash algorithm
        
    Returns:
        True if signature is valid
    """
    computed = compute_hmac(data, key, algorithm)
    return hmac.compare_digest(computed, signature)


# =============================================================================
# XOR Encryption (Simple, for educational purposes)
# =============================================================================

def xor_encrypt(data: StringOrBytes, key: StringOrBytes) -> bytes:
    """
    XOR encrypt data with key.
    
    Note: This is NOT secure for production use. Use for educational purposes only.
    For production, use Fernet or AES from cryptography library.
    
    Args:
        data: Data to encrypt
        key: Encryption key
        
    Returns:
        Encrypted bytes
    """
    data_bytes = _to_bytes(data)
    key_bytes = _to_bytes(key)
    
    # Expand key to match data length
    expanded_key = (key_bytes * ((len(data_bytes) // len(key_bytes)) + 1))[:len(data_bytes)]
    
    return bytes(a ^ b for a, b in zip(data_bytes, expanded_key))


def xor_decrypt(encrypted: bytes, key: StringOrBytes) -> bytes:
    """
    XOR decrypt data with key.
    
    Args:
        encrypted: Encrypted data
        key: Decryption key
        
    Returns:
        Decrypted bytes
    """
    return xor_encrypt(encrypted, key)  # XOR is symmetric


# =============================================================================
# Simple Substitution Cipher (Educational)
# =============================================================================

class SubstitutionCipher:
    """
    Simple substitution cipher for educational purposes.
    
    NOT SECURE for production use!
    """
    
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    
    def __init__(self, key: Optional[str] = None):
        """
        Initialize cipher with optional key.
        
        Args:
            key: Seed for shuffle (if None, uses random shuffle)
        """
        if key:
            # Deterministic shuffle based on key
            seed = int(hashlib.sha256(key.encode()).hexdigest(), 16) % (2**32)
            import random
            rng = random.Random(seed)
            self._substitute = list(self.ALPHABET)
            rng.shuffle(self._substitute)
        else:
            self._substitute = list(self.ALPHABET)
            import random
            random.shuffle(self._substitute)
        
        self._substitute_map = dict(zip(self.ALPHABET, self._substitute))
        self._reverse_map = {v: k for k, v in self._substitute_map.items()}
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext."""
        result = []
        for char in plaintext.lower():
            if char in self._substitute_map:
                result.append(self._substitute_map[char])
            else:
                result.append(char)
        return ''.join(result)
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext."""
        result = []
        for char in ciphertext.lower():
            if char in self._reverse_map:
                result.append(self._reverse_map[char])
            else:
                result.append(char)
        return ''.join(result)


# =============================================================================
# Base64 Encoding with Encryption
# =============================================================================

def base64_encode(data: StringOrBytes) -> str:
    """Encode data to base64 string."""
    data_bytes = _to_bytes(data)
    return base64.b64encode(data_bytes).decode('ascii')


def base64_decode(encoded: str) -> bytes:
    """Decode base64 string to bytes."""
    return base64.b64decode(encoded)


def url_safe_encode(data: StringOrBytes) -> str:
    """Encode data to URL-safe base64 string."""
    data_bytes = _to_bytes(data)
    return base64.urlsafe_b64encode(data_bytes).decode('ascii').rstrip('=')


def url_safe_decode(encoded: str) -> bytes:
    """Decode URL-safe base64 string."""
    # Add padding if needed
    padding = 4 - (len(encoded) % 4)
    if padding != 4:
        encoded += '=' * padding
    return base64.urlsafe_b64decode(encoded)


# =============================================================================
# Secure Token Generation
# =============================================================================

def generate_token(
    length: int = 32,
    url_safe: bool = False,
    include_timestamp: bool = False,
) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length: Token length in bytes (default: 32)
        url_safe: Use URL-safe encoding
        include_timestamp: Prepend timestamp
        
    Returns:
        Base64-encoded token string
    """
    token = secrets.token_bytes(length)
    
    if include_timestamp:
        timestamp = struct.pack('>Q', int(time.time() * 1000))
        token = timestamp + token
    
    if url_safe:
        return base64.urlsafe_b64encode(token).decode('ascii').rstrip('=')
    return base64.b64encode(token).decode('ascii')


def generate_api_key(prefix: str = "ak") -> str:
    """
    Generate an API key with prefix.
    
    Args:
        prefix: Key prefix (default: "ak")
        
    Returns:
        API key string like "ak_xxxxxxxxxxxxx"
    """
    token = secrets.token_urlsafe(24)
    return f"{prefix}_{token}"


def generate_session_id() -> str:
    """Generate a session ID."""
    return secrets.token_hex(32)


# =============================================================================
# Checksum Functions
# =============================================================================

def compute_checksum(data: StringOrBytes, algorithm: str = "crc32") -> int:
    """
    Compute checksum for data.
    
    Args:
        data: Data to checksum
        algorithm: Checksum algorithm (crc32, adler32)
        
    Returns:
        Checksum value
    """
    data_bytes = _to_bytes(data)
    
    if algorithm == "crc32":
        import zlib
        return zlib.crc32(data_bytes) & 0xffffffff
    elif algorithm == "adler32":
        import zlib
        return zlib.adler32(data_bytes) & 0xffffffff
    else:
        raise EncryptionError(f"Unsupported checksum algorithm: {algorithm}")


def verify_checksum(data: StringOrBytes, expected: int, algorithm: str = "crc32") -> bool:
    """Verify checksum."""
    return compute_checksum(data, algorithm) == expected


# =============================================================================
# One-Time Pad (Theoretically Unbreakable)
# =============================================================================

def generate_otp(length: int) -> bytes:
    """
    Generate a one-time pad.
    
    Args:
        length: Length of pad in bytes
        
    Returns:
        Random bytes for OTP
    """
    return secrets.token_bytes(length)


def otp_encrypt(data: StringOrBytes, otp: bytes) -> bytes:
    """
    Encrypt with one-time pad.
    
    Args:
        data: Data to encrypt
        otp: One-time pad (must be >= data length)
        
    Returns:
        Encrypted bytes
    """
    data_bytes = _to_bytes(data)
    
    if len(otp) < len(data_bytes):
        raise EncryptionError("OTP must be at least as long as data")
    
    return bytes(a ^ b for a, b in zip(data_bytes, otp))


def otp_decrypt(encrypted: bytes, otp: bytes) -> bytes:
    """Decrypt with one-time pad."""
    return otp_encrypt(encrypted, otp)  # OTP is symmetric


# =============================================================================
# Secure Comparison
# =============================================================================

def secure_compare(a: StringOrBytes, b: StringOrBytes) -> bool:
    """
    Timing-safe comparison of two values.
    
    Args:
        a: First value
        b: Second value
        
    Returns:
        True if equal
    """
    a_bytes = _to_bytes(a) if isinstance(a, str) else bytes(a)
    b_bytes = _to_bytes(b) if isinstance(b, str) else bytes(b)
    return hmac.compare_digest(a_bytes, b_bytes)


# =============================================================================
# Key Derivation
# =============================================================================

def derive_key(
    password: StringOrBytes,
    salt: Optional[bytes] = None,
    length: int = 32,
    algorithm: str = "pbkdf2",
    iterations: int = 100000,
) -> Tuple[bytes, bytes]:
    """
    Derive a key from password.
    
    Args:
        password: Password or passphrase
        salt: Optional salt (generated if None)
        length: Key length in bytes
        algorithm: KDF algorithm (pbkdf2)
        iterations: Iterations for PBKDF2
        
    Returns:
        Tuple of (derived_key, salt)
    """
    password_bytes = _to_bytes(password)
    
    if salt is None:
        salt = secrets.token_bytes(32)
    
    if algorithm == "pbkdf2":
        key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, length)
    else:
        raise EncryptionError(f"Unsupported KDF: {algorithm}")
    
    return key, salt


# =============================================================================
# Utility Classes
# =============================================================================

class SecureString:
    """
    A string that attempts to clear itself from memory.
    
    Note: Python's memory management makes true secure strings difficult.
    This is a best-effort implementation.
    """
    
    def __init__(self, value: str):
        self._value = value
        self._consumed = False
    
    def get(self) -> str:
        """Get the string value."""
        if self._consumed:
            raise EncryptionError("SecureString already consumed")
        return self._value
    
    def consume(self) -> str:
        """Get and mark as consumed."""
        value = self._value
        self._consumed = True
        self._value = None
        return value
    
    def clear(self) -> None:
        """Attempt to clear the value."""
        self._value = None
        self._consumed = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()
    
    def __str__(self):
        if self._consumed:
            return "<consumed>"
        return "<secure>"
    
    def __repr__(self):
        return f"SecureString(consumed={self._consumed})"


class HashChain:
    """
    Create a hash chain for data integrity verification.
    """
    
    def __init__(self, algorithm: str = HashAlgorithm.SHA256):
        self._algorithm = algorithm
        self._chain: List[HashResult] = []
    
    def add(self, data: StringOrBytes) -> 'HashChain':
        """Add data to chain."""
        if self._chain:
            # Include previous hash
            prev_hash = self._chain[-1].bytes_digest
            result = hash_data(prev_hash + _to_bytes(data), self._algorithm)
        else:
            result = hash_data(data, self._algorithm)
        
        self._chain.append(result)
        return self
    
    def get_chain_hash(self) -> str:
        """Get final chain hash."""
        if not self._chain:
            return ""
        return self._chain[-1].hex_digest
    
    def verify(self, data_list: List[StringOrBytes], expected_chain_hash: str) -> bool:
        """Verify a chain of data."""
        chain = HashChain(self._algorithm)
        for data in data_list:
            chain.add(data)
        return secure_compare(chain.get_chain_hash(), expected_chain_hash)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export chain."""
        return {
            'algorithm': self._algorithm,
            'length': len(self._chain),
            'chain_hash': self.get_chain_hash(),
            'entries': [entry.to_dict() for entry in self._chain],
        }


# =============================================================================
# Module-level Convenience
# =============================================================================

def quick_hash(data: StringOrBytes) -> str:
    """Quick SHA256 hash."""
    return hash_data(data).hex_digest


def quick_encrypt(data: StringOrBytes, key: StringOrBytes) -> str:
    """Quick XOR encrypt and base64 encode."""
    encrypted = xor_encrypt(data, key)
    return base64_encode(encrypted)


def quick_decrypt(encoded: str, key: StringOrBytes) -> bytes:
    """Quick base64 decode and XOR decrypt."""
    encrypted = base64_decode(encoded)
    return xor_decrypt(encrypted, key)
