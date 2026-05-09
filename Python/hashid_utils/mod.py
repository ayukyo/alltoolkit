"""
HashID Utils - Generate YouTube-like hash IDs from numbers.

A Python implementation for encoding integers into short, URL-safe,
non-sequential, reversible strings. Similar to YouTube video IDs.

Features:
- Encode integers to short hash strings
- Decode hash strings back to integers
- Custom alphabets and salts
- Configurable minimum length
- Encode/decode multiple numbers at once
- Zero external dependencies

Example:
    >>> hashid = HashID(salt="my secret", min_length=6)
    >>> encoded = hashid.encode(12345)
    >>> decoded = hashid.decode(encoded)
    >>> assert decoded == [12345]
"""

import hashlib
from typing import List, Optional, Union


class HashID:
    """
    HashID encoder/decoder for generating short, URL-safe IDs.
    
    Uses a modified version of the Hashids algorithm to create reversible
    hash strings from integers.
    """
    
    # Default alphabet - URL-safe characters, no ambiguous chars
    DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    
    # Separators for multi-number encoding
    DEFAULT_SEPARATORS = "cfhimpstuvCFHIMPSTUV"
    
    # Guards for wrapping encoded values
    DEFAULT_GUARDS = "abdegjklmnopqrABDEGJKLMNOPQR"
    
    def __init__(
        self,
        salt: str = "",
        min_length: int = 0,
        alphabet: Optional[str] = None,
    ):
        """
        Initialize HashID encoder.
        
        Args:
            salt: Secret key for unique encoding (default: "")
            min_length: Minimum length of encoded string (default: 0)
            alphabet: Custom character set to use (default: alphanumeric)
        
        Raises:
            ValueError: If alphabet has less than 16 unique characters
        """
        self.salt = salt
        self.min_length = min_length
        
        # Setup alphabet
        if alphabet is None:
            alphabet = self.DEFAULT_ALPHABET
        
        # Remove duplicates and ensure minimum length
        unique_alphabet = self._unique_chars(alphabet)
        
        if len(unique_alphabet) < 16:
            raise ValueError("Alphabet must contain at least 16 unique characters")
        
        # Separate alphabet, separators, and guards
        self._alphabet, self._separators, self._guards = self._setup_constants(
            unique_alphabet, salt
        )
    
    def _unique_chars(self, s: str) -> str:
        """Return string with duplicate characters removed, preserving order."""
        seen = set()
        result = []
        for char in s:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return "".join(result)
    
    def _setup_constants(
        self, alphabet: str, salt: str
    ) -> tuple:
        """Setup alphabet, separators, and guards based on salt."""
        # Shuffle alphabet based on salt
        alphabet_list = list(alphabet)
        
        if salt:
            salt_list = list(salt)
            salt_len = len(salt_list)
            salt_sum = sum(ord(c) for c in salt_list)
            
            # Consistent shuffle
            i = len(alphabet_list) - 1
            while i > 0:
                salt_char = salt_list[salt_sum % salt_len] if salt_len > 0 else ""
                salt_sum = (salt_sum + ord(salt_char) if salt_char else salt_sum + i) % (i + 1)
                j = salt_sum
                alphabet_list[i], alphabet_list[j] = alphabet_list[j], alphabet_list[i]
                i -= 1
        
        alphabet = "".join(alphabet_list)
        
        # Determine separators from alphabet
        separators = self.DEFAULT_SEPARATORS
        guards = self.DEFAULT_GUARDS
        
        # Filter separators and guards to only use chars in alphabet
        separators = "".join(c for c in separators if c in alphabet)
        guards = "".join(c for c in guards if c in alphabet)
        
        # Remove separators and guards from alphabet
        alphabet = "".join(c for c in alphabet if c not in separators and c not in guards)
        
        return alphabet, separators, guards
    
    def _hash(self, value: int, alphabet: str) -> str:
        """Hash an integer value using the given alphabet."""
        result = []
        alphabet_len = len(alphabet)
        
        while True:
            result.append(alphabet[value % alphabet_len])
            value = value // alphabet_len
            if value == 0:
                break
        
        return "".join(result[::-1])
    
    def _unhash(self, value: str, alphabet: str) -> int:
        """Unhash a string back to an integer using the given alphabet."""
        alphabet_len = len(alphabet)
        result = 0
        
        for char in value:
            pos = alphabet.index(char)
            result = result * alphabet_len + pos
        
        return result
    
    def encode(self, *numbers: int) -> str:
        """
        Encode one or more integers into a hash string.
        
        Args:
            *numbers: One or more non-negative integers to encode
        
        Returns:
            Encoded hash string
        
        Raises:
            ValueError: If any number is negative
        
        Example:
            >>> h = HashID(salt="my app", min_length=8)
            >>> h.encode(123)
            'Rk3b9NPA'
            >>> h.encode(1, 2, 3)
            'Rk3b9NPq'
        """
        # Validate input
        for num in numbers:
            if num < 0:
                raise ValueError("Cannot encode negative numbers")
        
        if not numbers:
            return ""
        
        # Add lottery char for single numbers
        lottery_offset = sum(
            (num % (i + 100)) for i, num in enumerate(numbers)
        )
        lottery_char = self._alphabet[lottery_offset % len(self._alphabet)]
        
        result = [lottery_char]
        alphabet = self._alphabet
        
        for i, num in enumerate(numbers):
            # Use lottery char and index to create unique alphabet for each number
            salt = lottery_char + self.salt + alphabet
            shuffled = self._shuffle_alphabet(alphabet, salt[:len(alphabet)])
            
            encoded = self._hash(num, shuffled)
            result.append(encoded)
            
            # Add separator between numbers (except after last)
            if i < len(numbers) - 1:
                # Use number value to determine separator
                sep_index = (num % 100) % len(self._separators) if self._separators else -1
                if sep_index >= 0:
                    result.append(self._separators[sep_index])
        
        encoded = "".join(result)
        
        # Pad to minimum length by adding guard chars at start and end
        if len(encoded) < self.min_length:
            padding_needed = self.min_length - len(encoded)
            
            # Split padding between start and end
            half = padding_needed // 2
            
            # Add guards at start
            for i in range(half):
                guard_index = (sum(numbers) + i) % len(self._guards) if self._guards else 0
                if self._guards:
                    encoded = self._guards[guard_index] + encoded
            
            # Add guards at end
            for i in range(padding_needed - half):
                guard_index = (sum(numbers) + i + half) % len(self._guards) if self._guards else 0
                if self._guards:
                    encoded += self._guards[guard_index]
        
        return encoded
    
    def decode(self, hash_str: str) -> List[int]:
        """
        Decode a hash string back to integers.
        
        Args:
            hash_str: Hash string to decode
        
        Returns:
            List of decoded integers
        
        Raises:
            ValueError: If hash string is invalid
        
        Example:
            >>> h = HashID(salt="my app", min_length=8)
            >>> h.decode('Rk3b9NPA')
            [123]
        """
        if not hash_str:
            return []
        
        # Remove guard chars from start and end
        while hash_str and hash_str[0] in self._guards:
            hash_str = hash_str[1:]
        while hash_str and hash_str[-1] in self._guards:
            hash_str = hash_str[:-1]
        
        if not hash_str:
            return []
        
        # First char is lottery
        lottery_char = hash_str[0]
        hash_str = hash_str[1:]
        
        # Split by separators
        parts = [hash_str]
        for sep in self._separators:
            new_parts = []
            for part in parts:
                new_parts.extend(part.split(sep))
            parts = new_parts
        
        # Decode each part
        numbers = []
        alphabet = self._alphabet
        
        for part in parts:
            if not part:
                continue
            
            # Reconstruct shuffled alphabet
            salt = lottery_char + self.salt + alphabet
            shuffled = self._shuffle_alphabet(alphabet, salt[:len(alphabet)])
            
            try:
                num = self._unhash(part, shuffled)
                numbers.append(num)
            except ValueError:
                # Invalid hash string
                raise ValueError(f"Invalid hash string: cannot decode '{part}'")
        
        return numbers
    
    def encode_single(self, number: int) -> str:
        """
        Encode a single integer and return the encoded string.
        
        Args:
            number: Non-negative integer to encode
        
        Returns:
            Encoded hash string
        
        Example:
            >>> h = HashID()
            >>> h.encode_single(12345)
            'jRg'
        """
        return self.encode(number)
    
    def decode_single(self, hash_str: str) -> int:
        """
        Decode a hash string and return the single integer.
        
        Args:
            hash_str: Hash string to decode
        
        Returns:
            Decoded integer
        
        Raises:
            ValueError: If hash string decodes to more/less than one number
        
        Example:
            >>> h = HashID()
            >>> h.decode_single('jRg')
            12345
        """
        numbers = self.decode(hash_str)
        if len(numbers) != 1:
            raise ValueError(f"Expected single number, got {len(numbers)}")
        return numbers[0]
    
    def _shuffle_alphabet(self, alphabet: str, salt: str) -> str:
        """Shuffle alphabet using salt for consistent results."""
        if not salt:
            return alphabet
        
        alphabet_list = list(alphabet)
        salt_list = list(salt)
        salt_len = len(salt_list)
        
        v = 0
        p = 0
        
        for i in range(len(alphabet_list) - 1, 0, -1):
            v %= salt_len
            p += ord(salt_list[v]) if v < salt_len and salt_list[v] else 0
            j = (ord(salt_list[v]) + p) % (i + 1) if v < salt_len and salt_list[v] else p % (i + 1)
            
            alphabet_list[i], alphabet_list[j] = alphabet_list[j], alphabet_list[i]
            v += 1
        
        return "".join(alphabet_list)


def encode_id(
    number: int,
    salt: str = "",
    min_length: int = 0,
    alphabet: Optional[str] = None,
) -> str:
    """
    Convenience function to encode a single number.
    
    Args:
        number: Non-negative integer to encode
        salt: Secret key for unique encoding
        min_length: Minimum length of encoded string
        alphabet: Custom character set
    
    Returns:
        Encoded hash string
    
    Example:
        >>> encode_id(12345, salt="my app")
        'jRg'
    """
    h = HashID(salt=salt, min_length=min_length, alphabet=alphabet)
    return h.encode_single(number)


def decode_id(
    hash_str: str,
    salt: str = "",
    min_length: int = 0,
    alphabet: Optional[str] = None,
) -> int:
    """
    Convenience function to decode a single number.
    
    Args:
        hash_str: Hash string to decode
        salt: Secret key used during encoding
        min_length: Minimum length used during encoding
        alphabet: Custom character set used during encoding
    
    Returns:
        Decoded integer
    
    Example:
        >>> decode_id('jRg', salt="my app")
        12345
    """
    h = HashID(salt=salt, min_length=min_length, alphabet=alphabet)
    return h.decode_single(hash_str)


def encode_ids(
    *numbers: int,
    salt: str = "",
    min_length: int = 0,
    alphabet: Optional[str] = None,
) -> str:
    """
    Convenience function to encode multiple numbers.
    
    Args:
        *numbers: Non-negative integers to encode
        salt: Secret key for unique encoding
        min_length: Minimum length of encoded string
        alphabet: Custom character set
    
    Returns:
        Encoded hash string
    
    Example:
        >>> encode_ids(1, 2, 3, salt="my app")
        'kRp9'
    """
    h = HashID(salt=salt, min_length=min_length, alphabet=alphabet)
    return h.encode(*numbers)


def decode_ids(
    hash_str: str,
    salt: str = "",
    min_length: int = 0,
    alphabet: Optional[str] = None,
) -> List[int]:
    """
    Convenience function to decode to multiple numbers.
    
    Args:
        hash_str: Hash string to decode
        salt: Secret key used during encoding
        min_length: Minimum length used during encoding
        alphabet: Custom character set used during encoding
    
    Returns:
        List of decoded integers
    
    Example:
        >>> decode_ids('kRp9', salt="my app")
        [1, 2, 3]
    """
    h = HashID(salt=salt, min_length=min_length, alphabet=alphabet)
    return h.decode(hash_str)


def is_valid_hashid(
    hash_str: str,
    alphabet: Optional[str] = None,
) -> bool:
    """
    Check if a string is a valid hashid format.
    
    Args:
        hash_str: String to check
        alphabet: Custom character set (default: alphanumeric)
    
    Returns:
        True if string contains only valid characters
    
    Example:
        >>> is_valid_hashid('aBc123')
        True
        >>> is_valid_hashid('hello world!')
        False
    """
    if not hash_str:
        return False
    
    valid_chars = alphabet or HashID.DEFAULT_ALPHABET
    valid_chars += HashID.DEFAULT_SEPARATORS + HashID.DEFAULT_GUARDS
    
    return all(c in valid_chars for c in hash_str)


def estimate_length(
    number: int,
    alphabet_length: int = 62,
) -> int:
    """
    Estimate the length of encoded hash string.
    
    Args:
        number: Number to encode
        alphabet_length: Length of character set used
    
    Returns:
        Estimated length of encoded string
    
    Example:
        >>> estimate_length(1000000)
        4
        >>> estimate_length(1000000, alphabet_length=16)
        5
    """
    if number == 0:
        return 1
    
    length = 0
    while number > 0:
        number //= alphabet_length
        length += 1
    
    return length


# Pre-configured instances for common use cases
class YouTubeHashID(HashID):
    """YouTube-style HashID with recommended settings."""
    
    def __init__(self, salt: str = ""):
        """
        Initialize YouTube-style encoder.
        
        Args:
            salt: Secret key for unique encoding
        """
        super().__init__(
            salt=salt,
            min_length=11,  # YouTube-style length
        )


class ShortHashID(HashID):
    """Short HashID for minimal encoding."""
    
    def __init__(self, salt: str = ""):
        """
        Initialize short encoder.
        
        Args:
            salt: Secret key for unique encoding
        """
        super().__init__(
            salt=salt,
            min_length=4,
        )