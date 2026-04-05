"""
AllToolkit - Python Base64 Utilities

A zero-dependency, production-ready Base64 encoding/decoding utility module.
Supports standard Base64, URL-safe Base64 (RFC 4648), and binary data handling.

Author: AllToolkit
License: MIT
"""

import base64
import re
from typing import Union, Optional


class Base64Utils:
    """
    Base64 encoding and decoding utilities.
    
    Provides functions for:
    - Standard Base64 encoding/decoding
    - URL-safe Base64 encoding/decoding (RFC 4648)
    - Binary data handling
    - Input validation
    - Length calculations
    """

    @staticmethod
    def encode(input_data: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """
        Encode string or bytes to Base64.

        Args:
            input_data: The data to encode (string or bytes)
            encoding: Character encoding for string input (default: 'utf-8')

        Returns:
            Base64 encoded string

        Raises:
            TypeError: If input_data is neither str nor bytes

        Example:
            >>> Base64Utils.encode("Hello, World!")
            'SGVsbG8sIFdvcmxkIQ=='
        """
        if isinstance(input_data, str):
            input_bytes = input_data.encode(encoding)
        elif isinstance(input_data, bytes):
            input_bytes = input_data
        else:
            raise TypeError("Input must be str or bytes")
        
        return base64.b64encode(input_bytes).decode('ascii')

    @staticmethod
    def decode(base64_string: str, encoding: str = 'utf-8') -> str:
        """
        Decode Base64 string to regular string.

        Args:
            base64_string: The Base64 encoded string
            encoding: Character encoding for output (default: 'utf-8')

        Returns:
            Decoded string

        Raises:
            ValueError: If input is not valid Base64

        Example:
            >>> Base64Utils.decode("SGVsbG8sIFdvcmxkIQ==")
            'Hello, World!'
        """
        decoded_bytes = base64.b64decode(base64_string)
        return decoded_bytes.decode(encoding)

    @staticmethod
    def decode_to_bytes(base64_string: str) -> bytes:
        """
        Decode Base64 string to bytes.

        Args:
            base64_string: The Base64 encoded string

        Returns:
            Decoded bytes

        Raises:
            ValueError: If input is not valid Base64

        Example:
            >>> Base64Utils.decode_to_bytes("SGVsbG8=")
            b'Hello'
        """
        return base64.b64decode(base64_string)

    @staticmethod
    def encode_urlsafe(input_data: Union[str, bytes], encoding: str = 'utf-8', padding: bool = True) -> str:
        """
        Encode to URL-safe Base64 (RFC 4648).
        
        Replaces '+' with '-' and '/' with '_'.

        Args:
            input_data: The data to encode (string or bytes)
            encoding: Character encoding for string input (default: 'utf-8')
            padding: Whether to include padding characters '=' (default: True)

        Returns:
            URL-safe Base64 encoded string

        Example:
            >>> Base64Utils.encode_urlsafe("hello+world/test")
            'aGVsbG8rd29ybGQvdGVzdA=='
        """
        if isinstance(input_data, str):
            input_bytes = input_data.encode(encoding)
        elif isinstance(input_data, bytes):
            input_bytes = input_data
        else:
            raise TypeError("Input must be str or bytes")
        
        encoded = base64.urlsafe_b64encode(input_bytes).decode('ascii')
        if not padding:
            encoded = encoded.rstrip('=')
        return encoded

    @staticmethod
    def decode_urlsafe(base64_url_string: str, encoding: str = 'utf-8') -> str:
        """
        Decode URL-safe Base64 string to regular string.

        Args:
            base64_url_string: The URL-safe Base64 encoded string
            encoding: Character encoding for output (default: 'utf-8')

        Returns:
            Decoded string

        Raises:
            ValueError: If input is not valid Base64

        Example:
            >>> Base64Utils.decode_urlsafe("aGVsbG8rd29ybGQvdGVzdA==")
            'hello+world/test'
        """
        # Add padding if missing
        padding_needed = 4 - (len(base64_url_string) % 4)
        if padding_needed != 4:
            base64_url_string += '=' * padding_needed
        
        decoded_bytes = base64.urlsafe_b64decode(base64_url_string)
        return decoded_bytes.decode(encoding)

    @staticmethod
    def decode_urlsafe_to_bytes(base64_url_string: str) -> bytes:
        """
        Decode URL-safe Base64 string to bytes.

        Args:
            base64_url_string: The URL-safe Base64 encoded string

        Returns:
            Decoded bytes

        Raises:
            ValueError: If input is not valid Base64

        Example:
            >>> Base64Utils.decode_urlsafe_to_bytes("aGVsbG8-")
            b'hello\xfb'
        """
        # Add padding if missing
        padding_needed = 4 - (len(base64_url_string) % 4)
        if padding_needed != 4:
            base64_url_string += '=' * padding_needed
        
        return base64.urlsafe_b64decode(base64_url_string)

    @staticmethod
    def to_urlsafe(standard_base64: str, padding: bool = True) -> str:
        """
        Convert standard Base64 to URL-safe Base64.

        Args:
            standard_base64: Standard Base64 encoded string
            padding: Whether to include padding characters '=' (default: True)

        Returns:
            URL-safe Base64 string

        Example:
            >>> Base64Utils.to_urlsafe("aGVsbG8+/test=")
            'aGVsbG8-_test='
        """
        urlsafe = standard_base64.replace('+', '-').replace('/', '_')
        if not padding:
            urlsafe = urlsafe.rstrip('=')
        return urlsafe

    @staticmethod
    def from_urlsafe(base64_url_string: str) -> str:
        """
        Convert URL-safe Base64 to standard Base64.

        Args:
            base64_url_string: URL-safe Base64 encoded string

        Returns:
            Standard Base64 string

        Example:
            >>> Base64Utils.from_urlsafe("aGVsbG8-_test=")
            'aGVsbG8+/test='
        """
        standard = base64_url_string.replace('-', '+').replace('_', '/')
        # Add padding if missing
        padding_needed = 4 - (len(standard) % 4)
        if padding_needed != 4:
            standard += '=' * padding_needed
        return standard

    @staticmethod
    def is_valid(base64_string: str, urlsafe: bool = False) -> bool:
        """
        Check if a string is valid Base64.

        Args:
            base64_string: The string to validate
            urlsafe: Whether to validate as URL-safe Base64 (default: False)

        Returns:
            True if valid Base64, False otherwise

        Example:
            >>> Base64Utils.is_valid("SGVsbG8=")
            True
            >>> Base64Utils.is_valid("Invalid!", urlsafe=True)
            False
        """
        if not isinstance(base64_string, str):
            return False
        
        if not base64_string:
            return True  # Empty string is valid Base64
        
        # Fast path: check length constraints
        # Base64 length must be multiple of 4 (or 2/3 for unpadded data)
        length = len(base64_string)
        remainder = length % 4
        
        # 1 mod 4 is always invalid
        if remainder == 1:
            return False
        
        # Define valid character sets
        if urlsafe:
            valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')
        else:
            valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')
        
        # Check all characters before padding
        padding_started = False
        padding_count = 0
        
        for i, char in enumerate(base64_string):
            if char == '=':
                padding_started = True
                padding_count += 1
                # Padding can only appear at the end, max 2 padding chars
                if padding_count > 2:
                    return False
                continue
            
            if padding_started:
                # Non-padding char after padding is invalid
                return False
            
            if char not in valid_chars:
                return False
        
        # Validate by actual decoding (handles all edge cases correctly)
        # Add padding for validation if missing
        try:
            test_string = base64_string
            padding_needed = 4 - (len(test_string) % 4)
            if padding_needed != 4:
                test_string += '=' * padding_needed
            
            if urlsafe:
                base64.urlsafe_b64decode(test_string)
            else:
                base64.b64decode(test_string)
            return True
        except Exception:
            return False

    @staticmethod
    def encoded_length(input_length: int, padding: bool = True) -> int:
        """
        Calculate the length of Base64 encoded output.

        Args:
            input_length: Length of input data in bytes
            padding: Whether padding is included (default: True)

        Returns:
            Length of Base64 encoded string

        Example:
            >>> Base64Utils.encoded_length(100)
            136
            >>> Base64Utils.encoded_length(100, padding=False)
            135
        """
        if input_length == 0:
            return 0
        
        # Base64 uses 4 bytes for every 3 bytes of input
        encoded_len = ((input_length + 2) // 3) * 4
        
        if not padding:
            # Calculate exact length without padding
            remainder = input_length % 3
            if remainder == 1:
                encoded_len -= 2
            elif remainder == 2:
                encoded_len -= 1
        
        return encoded_len

    @staticmethod
    def decoded_max_length(base64_length: int) -> int:
        """
        Calculate the maximum possible decoded length.

        Args:
            base64_length: Length of Base64 string

        Returns:
            Maximum possible decoded length in bytes

        Example:
            >>> Base64Utils.decoded_max_length(136)
            102
        """
        if base64_length == 0:
            return 0
        
        # Each 4 Base64 chars decode to 3 bytes
        return (base64_length // 4) * 3


# Convenience functions for direct import

def encode(input_data: Union[str, bytes], encoding: str = 'utf-8') -> str:
    """Encode string or bytes to Base64."""
    return Base64Utils.encode(input_data, encoding)


def decode(base64_string: str, encoding: str = 'utf-8') -> str:
    """Decode Base64 string to regular string."""
    return Base64Utils.decode(base64_string, encoding)


def decode_to_bytes(base64_string: str) -> bytes:
    """Decode Base64 string to bytes."""
    return Base64Utils.decode_to_bytes(base64_string)


def encode_urlsafe(input_data: Union[str, bytes], encoding: str = 'utf-8', padding: bool = True) -> str:
    """Encode to URL-safe Base64 (RFC 4648)."""
    return Base64Utils.encode_urlsafe(input_data, encoding, padding)


def decode_urlsafe(base64_url_string: str, encoding: str = 'utf-8') -> str:
    """Decode URL-safe Base64 string to regular string."""
    return Base64Utils.decode_urlsafe(base64_url_string, encoding)


def decode_urlsafe_to_bytes(base64_url_string: str) -> bytes:
    """Decode URL-safe Base64 string to bytes."""
    return Base64Utils.decode_urlsafe_to_bytes(base64_url_string)


def to_urlsafe(standard_base64: str, padding: bool = True) -> str:
    """Convert standard Base64 to URL-safe Base64."""
    return Base64Utils.to_urlsafe(standard_base64, padding)


def from_urlsafe(base64_url_string: str) -> str:
    """Convert URL-safe Base64 to standard Base64."""
    return Base64Utils.from_urlsafe(base64_url_string)


def is_valid(base64_string: str, urlsafe: bool = False) -> bool:
    """Check if a string is valid Base64."""
    return Base64Utils.is_valid(base64_string, urlsafe)


def encoded_length(input_length: int, padding: bool = True) -> int:
    """Calculate the length of Base64 encoded output."""
    return Base64Utils.encoded_length(input_length, padding)


def decoded_max_length(base64_length: int) -> int:
    """Calculate the maximum possible decoded length."""
    return Base64Utils.decoded_max_length(base64_length)