"""
Bitmask Utils - A comprehensive bitmask manipulation library

Provides utilities for creating, manipulating, and querying bitmasks.
Useful for permission systems, flag management, state machines, and bit operations.
"""

from typing import List, Optional, Set, Dict, Any


class Bitmask:
    """
    A class for managing bitmask operations with a clean API.
    
    Example:
        >>> mask = Bitmask()
        >>> mask.set(0).set(1).set(2)  # Set bits 0, 1, 2
        >>> mask.has(1)  # True
        >>> mask.toggle(3)  # Toggle bit 3
        >>> mask.clear(0)  # Clear bit 0
    """
    
    def __init__(self, value: int = 0, bits: int = 32):
        """
        Initialize a bitmask.
        
        Args:
            value: Initial bitmask value (default: 0)
            bits: Number of bits in the mask (default: 32)
        """
        if bits <= 0:
            raise ValueError("Number of bits must be positive")
        self._bits = bits
        self._mask = value & self._full_mask()
    
    def _full_mask(self) -> int:
        """Get the full mask for all bits."""
        return (1 << self._bits) - 1
    
    def _validate_bit(self, bit: int) -> None:
        """Validate that a bit position is within range."""
        if bit < 0 or bit >= self._bits:
            raise ValueError(f"Bit position {bit} out of range [0, {self._bits - 1}]")
    
    # ========== Basic Operations ==========
    
    def set(self, bit: int) -> 'Bitmask':
        """
        Set a bit to 1.
        
        Args:
            bit: Bit position to set
            
        Returns:
            Self for method chaining
        """
        self._validate_bit(bit)
        self._mask |= (1 << bit)
        return self
    
    def clear(self, bit: int) -> 'Bitmask':
        """
        Clear a bit to 0.
        
        Args:
            bit: Bit position to clear
            
        Returns:
            Self for method chaining
        """
        self._validate_bit(bit)
        self._mask &= ~(1 << bit)
        return self
    
    def toggle(self, bit: int) -> 'Bitmask':
        """
        Toggle a bit (0 -> 1 or 1 -> 0).
        
        Args:
            bit: Bit position to toggle
            
        Returns:
            Self for method chaining
        """
        self._validate_bit(bit)
        self._mask ^= (1 << bit)
        return self
    
    def has(self, bit: int) -> bool:
        """
        Check if a bit is set.
        
        Args:
            bit: Bit position to check
            
        Returns:
            True if the bit is 1, False otherwise
        """
        self._validate_bit(bit)
        return bool(self._mask & (1 << bit))
    
    def get(self, bit: int) -> int:
        """
        Get the value of a single bit (0 or 1).
        
        Args:
            bit: Bit position to get
            
        Returns:
            0 or 1
        """
        return 1 if self.has(bit) else 0
    
    # ========== Multi-bit Operations ==========
    
    def set_all(self, bits: List[int]) -> 'Bitmask':
        """
        Set multiple bits at once.
        
        Args:
            bits: List of bit positions to set
            
        Returns:
            Self for method chaining
        """
        for bit in bits:
            self.set(bit)
        return self
    
    def clear_all(self, bits: List[int]) -> 'Bitmask':
        """
        Clear multiple bits at once.
        
        Args:
            bits: List of bit positions to clear
            
        Returns:
            Self for method chaining
        """
        for bit in bits:
            self.clear(bit)
        return self
    
    def toggle_all(self, bits: List[int]) -> 'Bitmask':
        """
        Toggle multiple bits at once.
        
        Args:
            bits: List of bit positions to toggle
            
        Returns:
            Self for method chaining
        """
        for bit in bits:
            self.toggle(bit)
        return self
    
    def has_all(self, bits: List[int]) -> bool:
        """
        Check if all specified bits are set.
        
        Args:
            bits: List of bit positions to check
            
        Returns:
            True if all bits are 1
        """
        return all(self.has(bit) for bit in bits)
    
    def has_any(self, bits: List[int]) -> bool:
        """
        Check if any of the specified bits are set.
        
        Args:
            bits: List of bit positions to check
            
        Returns:
            True if any bit is 1
        """
        return any(self.has(bit) for bit in bits)
    
    def has_none(self, bits: List[int]) -> bool:
        """
        Check if none of the specified bits are set.
        
        Args:
            bits: List of bit positions to check
            
        Returns:
            True if all bits are 0
        """
        return not self.has_any(bits)
    
    # ========== Range Operations ==========
    
    def set_range(self, start: int, end: int) -> 'Bitmask':
        """
        Set a range of bits.
        
        Args:
            start: Starting bit position (inclusive)
            end: Ending bit position (inclusive)
            
        Returns:
            Self for method chaining
        """
        self._validate_bit(start)
        self._validate_bit(end)
        if start > end:
            raise ValueError(f"Start {start} cannot be greater than end {end}")
        
        range_mask = ((1 << (end - start + 1)) - 1) << start
        self._mask |= range_mask
        return self
    
    def clear_range(self, start: int, end: int) -> 'Bitmask':
        """
        Clear a range of bits.
        
        Args:
            start: Starting bit position (inclusive)
            end: Ending bit position (inclusive)
            
        Returns:
            Self for method chaining
        """
        self._validate_bit(start)
        self._validate_bit(end)
        if start > end:
            raise ValueError(f"Start {start} cannot be greater than end {end}")
        
        range_mask = ((1 << (end - start + 1)) - 1) << start
        self._mask &= ~range_mask
        return self
    
    # ========== Query Operations ==========
    
    def count_set(self) -> int:
        """
        Count the number of set bits (population count).
        
        Returns:
            Number of bits set to 1
        """
        count = 0
        value = self._mask
        while value:
            count += value & 1
            value >>= 1
        return count
    
    def count_clear(self) -> int:
        """
        Count the number of cleared bits.
        
        Returns:
            Number of bits set to 0
        """
        return self._bits - self.count_set()
    
    def first_set(self) -> Optional[int]:
        """
        Find the position of the first set bit (least significant).
        
        Returns:
            Position of first 1 bit, or None if no bits are set
        """
        if self._mask == 0:
            return None
        position = 0
        value = self._mask
        while (value & 1) == 0:
            value >>= 1
            position += 1
        return position
    
    def last_set(self) -> Optional[int]:
        """
        Find the position of the last set bit (most significant).
        
        Returns:
            Position of last 1 bit, or None if no bits are set
        """
        if self._mask == 0:
            return None
        position = self._bits - 1
        while position >= 0 and not self.has(position):
            position -= 1
        return position
    
    def get_set_bits(self) -> List[int]:
        """
        Get a list of all set bit positions.
        
        Returns:
            List of positions where bits are 1
        """
        return [i for i in range(self._bits) if self.has(i)]
    
    def get_clear_bits(self) -> List[int]:
        """
        Get a list of all cleared bit positions.
        
        Returns:
            List of positions where bits are 0
        """
        return [i for i in range(self._bits) if not self.has(i)]
    
    # ========== Manipulation Operations ==========
    
    def invert(self) -> 'Bitmask':
        """
        Invert all bits (bitwise NOT).
        
        Returns:
            Self for method chaining
        """
        self._mask = (~self._mask) & self._full_mask()
        return self
    
    def shift_left(self, n: int) -> 'Bitmask':
        """
        Shift all bits left by n positions.
        
        Args:
            n: Number of positions to shift
            
        Returns:
            Self for method chaining
        """
        if n < 0:
            return self.shift_right(-n)
        self._mask = (self._mask << n) & self._full_mask()
        return self
    
    def shift_right(self, n: int) -> 'Bitmask':
        """
        Shift all bits right by n positions.
        
        Args:
            n: Number of positions to shift
            
        Returns:
            Self for method chaining
        """
        if n < 0:
            return self.shift_left(-n)
        self._mask = self._mask >> n
        return self
    
    def rotate_left(self, n: int) -> 'Bitmask':
        """
        Rotate bits left by n positions (circular shift).
        
        Args:
            n: Number of positions to rotate
            
        Returns:
            Self for method chaining
        """
        n = n % self._bits
        if n == 0:
            return self
        self._mask = ((self._mask << n) | (self._mask >> (self._bits - n))) & self._full_mask()
        return self
    
    def rotate_right(self, n: int) -> 'Bitmask':
        """
        Rotate bits right by n positions (circular shift).
        
        Args:
            n: Number of positions to rotate
            
        Returns:
            Self for method chaining
        """
        n = n % self._bits
        if n == 0:
            return self
        return self.rotate_left(self._bits - n)
    
    # ========== Logical Operations ==========
    
    def and_with(self, other: 'Bitmask') -> 'Bitmask':
        """
        Perform bitwise AND with another bitmask.
        
        Args:
            other: Another Bitmask
            
        Returns:
            Self for method chaining
        """
        self._mask &= other._mask
        return self
    
    def or_with(self, other: 'Bitmask') -> 'Bitmask':
        """
        Perform bitwise OR with another bitmask.
        
        Args:
            other: Another Bitmask
            
        Returns:
            Self for method chaining
        """
        self._mask |= other._mask
        return self
    
    def xor_with(self, other: 'Bitmask') -> 'Bitmask':
        """
        Perform bitwise XOR with another bitmask.
        
        Args:
            other: Another Bitmask
            
        Returns:
            Self for method chaining
        """
        self._mask ^= other._mask
        return self
    
    # ========== Comparison Operations ==========
    
    def is_subset(self, other: 'Bitmask') -> bool:
        """
        Check if this mask is a subset of another (all our bits are set in other).
        
        Args:
            other: Another Bitmask
            
        Returns:
            True if this is a subset of other
        """
        return (self._mask & other._mask) == self._mask
    
    def is_superset(self, other: 'Bitmask') -> bool:
        """
        Check if this mask is a superset of another (all other's bits are set in us).
        
        Args:
            other: Another Bitmask
            
        Returns:
            True if this is a superset of other
        """
        return (self._mask & other._mask) == other._mask
    
    def overlaps(self, other: 'Bitmask') -> bool:
        """
        Check if this mask has any bits in common with another.
        
        Args:
            other: Another Bitmask
            
        Returns:
            True if any bits overlap
        """
        return bool(self._mask & other._mask)
    
    def is_disjoint(self, other: 'Bitmask') -> bool:
        """
        Check if this mask has no bits in common with another.
        
        Args:
            other: Another Bitmask
            
        Returns:
            True if no bits overlap
        """
        return not self.overlaps(other)
    
    # ========== Conversion Operations ==========
    
    def to_int(self) -> int:
        """
        Get the integer value of the bitmask.
        
        Returns:
            Integer representation
        """
        return self._mask
    
    def to_bin(self, prefix: str = '0b', pad: bool = True) -> str:
        """
        Get the binary string representation.
        
        Args:
            prefix: Prefix to add (default: '0b')
            pad: Whether to pad to full bit width
            
        Returns:
            Binary string representation
        """
        if pad:
            return f"{prefix}{self._mask:0{self._bits}b}"
        return f"{prefix}{self._mask:b}"
    
    def to_hex(self, prefix: str = '0x', pad: bool = True) -> str:
        """
        Get the hexadecimal string representation.
        
        Args:
            prefix: Prefix to add (default: '0x')
            pad: Whether to pad to full bit width
            
        Returns:
            Hexadecimal string representation
        """
        hex_digits = (self._bits + 3) // 4
        if pad:
            return f"{prefix}{self._mask:0{hex_digits}x}"
        return f"{prefix}{self._mask:x}"
    
    def to_list(self) -> List[int]:
        """
        Get a list of bit values.
        
        Returns:
            List of 0s and 1s (LSB first)
        """
        return [(self._mask >> i) & 1 for i in range(self._bits)]
    
    def to_set(self) -> Set[int]:
        """
        Get a set of set bit positions.
        
        Returns:
            Set of positions where bits are 1
        """
        return set(self.get_set_bits())
    
    def copy(self) -> 'Bitmask':
        """
        Create a copy of this bitmask.
        
        Returns:
            A new Bitmask with the same value
        """
        return Bitmask(self._mask, self._bits)
    
    def reset(self) -> 'Bitmask':
        """
        Reset all bits to 0.
        
        Returns:
            Self for method chaining
        """
        self._mask = 0
        return self
    
    def fill(self) -> 'Bitmask':
        """
        Set all bits to 1.
        
        Returns:
            Self for method chaining
        """
        self._mask = self._full_mask()
        return self
    
    # ========== Magic Methods ==========
    
    def __int__(self) -> int:
        return self._mask
    
    def __str__(self) -> str:
        return self.to_bin()
    
    def __repr__(self) -> str:
        return f"Bitmask({self._mask}, bits={self._bits})"
    
    def __len__(self) -> int:
        return self._bits
    
    def __getitem__(self, bit: int) -> int:
        return self.get(bit)
    
    def __setitem__(self, bit: int, value: int) -> None:
        if value:
            self.set(bit)
        else:
            self.clear(bit)
    
    def __contains__(self, bit: int) -> bool:
        return self.has(bit)
    
    def __and__(self, other: 'Bitmask') -> 'Bitmask':
        return self.copy().and_with(other)
    
    def __or__(self, other: 'Bitmask') -> 'Bitmask':
        return self.copy().or_with(other)
    
    def __xor__(self, other: 'Bitmask') -> 'Bitmask':
        return self.copy().xor_with(other)
    
    def __invert__(self) -> 'Bitmask':
        return self.copy().invert()
    
    def __lshift__(self, n: int) -> 'Bitmask':
        return self.copy().shift_left(n)
    
    def __rshift__(self, n: int) -> 'Bitmask':
        return self.copy().shift_right(n)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bitmask):
            return self._mask == other._mask and self._bits == other._bits
        return False
    
    def __hash__(self) -> int:
        return hash((self._mask, self._bits))
    
    def __bool__(self) -> bool:
        return self._mask != 0


# ========== Functional API ==========

def create_bitmask(value: int = 0, bits: int = 32) -> Bitmask:
    """Create a new Bitmask instance."""
    return Bitmask(value, bits)


def from_bits(bits: List[int], total_bits: int = 32) -> Bitmask:
    """
    Create a bitmask from a list of bit positions.
    
    Args:
        bits: List of bit positions to set
        total_bits: Total number of bits
        
    Returns:
        New Bitmask with specified bits set
    """
    return Bitmask(0, total_bits).set_all(bits)


def from_binary(binary_str: str, total_bits: Optional[int] = None) -> Bitmask:
    """
    Create a bitmask from a binary string.
    
    Args:
        binary_str: Binary string (with or without '0b' prefix)
        total_bits: Total number of bits (default: auto)
        
    Returns:
        New Bitmask
    """
    # Remove prefix if present
    if binary_str.startswith('0b'):
        binary_str = binary_str[2:]
    
    value = int(binary_str, 2)
    if total_bits is None:
        total_bits = max(len(binary_str), 1)
    
    return Bitmask(value, total_bits)


def from_hex(hex_str: str, total_bits: Optional[int] = None) -> Bitmask:
    """
    Create a bitmask from a hexadecimal string.
    
    Args:
        hex_str: Hex string (with or without '0x' prefix)
        total_bits: Total number of bits (default: auto)
        
    Returns:
        New Bitmask
    """
    # Remove prefix if present
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]
    
    value = int(hex_str, 16)
    if total_bits is None:
        total_bits = len(hex_str) * 4
    
    return Bitmask(value, total_bits)


def combine_bitmasks(*masks: Bitmask) -> Bitmask:
    """
    Combine multiple bitmasks with OR operation.
    
    Args:
        *masks: Bitmasks to combine
        
    Returns:
        New combined Bitmask
    """
    if not masks:
        return Bitmask()
    
    result = masks[0].copy()
    for mask in masks[1:]:
        result.or_with(mask)
    
    return result


def intersect_bitmasks(*masks: Bitmask) -> Bitmask:
    """
    Intersect multiple bitmasks with AND operation.
    
    Args:
        *masks: Bitmasks to intersect
        
    Returns:
        New intersected Bitmask
    """
    if not masks:
        return Bitmask()
    
    result = masks[0].copy()
    for mask in masks[1:]:
        result.and_with(mask)
    
    return result


# ========== Utility Functions ==========

def count_bits(value: int) -> int:
    """
    Count the number of set bits in an integer.
    
    Args:
        value: Integer value
        
    Returns:
        Number of 1 bits
    """
    count = 0
    while value:
        count += value & 1
        value >>= 1
    return count


def parity(value: int) -> int:
    """
    Calculate the parity of an integer (XOR of all bits).
    
    Args:
        value: Integer value
        
    Returns:
        0 or 1
    """
    result = 0
    while value:
        result ^= (value & 1)
        value >>= 1
    return result


def reverse_bits(value: int, bits: int = 32) -> int:
    """
    Reverse the bits in an integer.
    
    Args:
        value: Integer value
        bits: Number of bits to consider
        
    Returns:
        Integer with reversed bits
    """
    result = 0
    for i in range(bits):
        if value & (1 << i):
            result |= 1 << (bits - 1 - i)
    return result


def next_power_of_2(value: int) -> int:
    """
    Find the next power of 2 greater than or equal to value.
    
    Args:
        value: Integer value
        
    Returns:
        Next power of 2
    """
    if value <= 0:
        return 1
    value -= 1
    value |= value >> 1
    value |= value >> 2
    value |= value >> 4
    value |= value >> 8
    value |= value >> 16
    return value + 1


def is_power_of_2(value: int) -> bool:
    """
    Check if a value is a power of 2.
    
    Args:
        value: Integer value
        
    Returns:
        True if value is a power of 2
    """
    return value > 0 and (value & (value - 1)) == 0


def get_lsb(value: int) -> int:
    """
    Get the least significant bit position.
    
    Args:
        value: Integer value
        
    Returns:
        Position of LSB, or -1 if value is 0
    """
    if value == 0:
        return -1
    position = 0
    while (value & 1) == 0:
        value >>= 1
        position += 1
    return position


def get_msb(value: int, bits: int = 32) -> int:
    """
    Get the most significant bit position.
    
    Args:
        value: Integer value
        bits: Maximum number of bits
        
    Returns:
        Position of MSB, or -1 if value is 0
    """
    if value == 0:
        return -1
    position = bits - 1
    while position >= 0 and (value & (1 << position)) == 0:
        position -= 1
    return position


def gray_code(value: int) -> int:
    """
    Convert an integer to Gray code.
    
    Args:
        value: Integer value
        
    Returns:
        Gray code representation
    """
    return value ^ (value >> 1)


def from_gray_code(gray: int) -> int:
    """
    Convert Gray code back to binary.
    
    Args:
        gray: Gray code value
        
    Returns:
        Binary representation
    """
    value = gray
    mask = gray >> 1
    while mask:
        value ^= mask
        mask >>= 1
    return value


if __name__ == "__main__":
    # Demo
    print("=== Bitmask Utils Demo ===\n")
    
    # Create a bitmask
    mask = Bitmask(bits=8)
    mask.set(0).set(2).set(4).set(6)
    print(f"Set bits 0, 2, 4, 6: {mask.to_bin()}")
    print(f"Integer value: {mask.to_int()}")
    print(f"Set bits: {mask.get_set_bits()}")
    
    # Toggle some bits
    mask.toggle(1).toggle(2)
    print(f"After toggling bits 1, 2: {mask.to_bin()}")
    
    # Range operations
    mask.set_range(0, 3)
    print(f"After setting range 0-3: {mask.to_bin()}")
    
    # Count and find
    print(f"Number of set bits: {mask.count_set()}")
    print(f"First set bit: {mask.first_set()}")
    print(f"Last set bit: {mask.last_set()}")
    
    # Rotate
    mask.rotate_left(2)
    print(f"After rotating left by 2: {mask.to_bin()}")
    
    # Functional API
    print("\n=== Functional API ===")
    mask2 = from_bits([1, 3, 5], total_bits=8)
    print(f"From bits [1, 3, 5]: {mask2.to_bin()}")
    
    mask3 = from_binary("10101010")
    print(f"From binary '10101010': {mask3.to_bin()}")
    
    combined = combine_bitmasks(mask2, mask3)
    print(f"Combined: {combined.to_bin()}")
    
    # Utility functions
    print("\n=== Utility Functions ===")
    print(f"count_bits(255): {count_bits(255)}")
    print(f"is_power_of_2(16): {is_power_of_2(16)}")
    print(f"is_power_of_2(15): {is_power_of_2(15)}")
    print(f"next_power_of_2(10): {next_power_of_2(10)}")
    print(f"parity(7): {parity(7)}")
    print(f"reverse_bits(0b11010010, 8): {bin(reverse_bits(0b11010010, 8))}")
    print(f"gray_code(5): {gray_code(5)} (binary: {bin(gray_code(5))})")
    print(f"from_gray_code({gray_code(5)}): {from_gray_code(gray_code(5))}")