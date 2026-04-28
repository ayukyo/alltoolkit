"""
Hamming Code Utilities - Error Detection and Correction

Implements Hamming codes for error detection and correction in data transmission.
Supports Hamming(7,4) and extended Hamming(8,4) codes.

Features:
- Encode 4-bit data into 7-bit Hamming code
- Detect and correct single-bit errors
- Extended Hamming code with overall parity for double-error detection
- Zero external dependencies
"""

from typing import Tuple, List, Optional


class HammingCode:
    """
    Hamming Code encoder/decoder for error detection and correction.
    
    Hamming(7,4) encodes 4 data bits into 7 bits (3 parity bits).
    Extended Hamming(8,4) adds an overall parity bit for double-error detection.
    """
    
    # Parity bit positions (1-indexed): 1, 2, 4 (powers of 2)
    PARITY_POSITIONS = [0, 1, 3]  # 0-indexed positions for parity bits
    
    # Data bit positions (1-indexed): 3, 5, 6, 7
    DATA_POSITIONS = [2, 4, 5, 6]  # 0-indexed positions for data bits
    
    def __init__(self, extended: bool = False):
        """
        Initialize Hamming Code encoder/decoder.
        
        Args:
            extended: If True, use extended Hamming(8,4) with overall parity.
                     If False, use standard Hamming(7,4).
        """
        self.extended = extended
        self.code_length = 8 if extended else 7
    
    @staticmethod
    def _calculate_parity(bits: List[int], parity_index: int) -> int:
        """
        Calculate a parity bit value.
        
        The parity bit at position 2^n checks all bits whose position
        has bit n set in its binary representation.
        
        Args:
            bits: List of bit values (0 or 1)
            parity_index: Index of the parity bit (0, 1, or 2)
            
        Returns:
            Parity bit value (0 or 1)
        """
        position = 1 << parity_index  # 1, 2, or 4 for parity bits
        parity = 0
        
        for i, bit in enumerate(bits):
            bit_position = i + 1  # 1-indexed position
            if bit_position & position and bit_position != position:
                parity ^= bit
        
        return parity
    
    def encode(self, data: int) -> int:
        """
        Encode 4-bit data into Hamming code.
        
        Args:
            data: Integer value 0-15 (4 bits)
            
        Returns:
            Encoded Hamming code as integer
            
        Raises:
            ValueError: If data is not in range 0-15
        """
        if not 0 <= data <= 15:
            raise ValueError(f"Data must be 4 bits (0-15), got {data}")
        
        # Extract data bits
        data_bits = [
            (data >> 3) & 1,  # D1 (MSB)
            (data >> 2) & 1,  # D2
            (data >> 1) & 1,  # D3
            (data >> 0) & 1,  # D4 (LSB)
        ]
        
        # Initialize code with zeros
        code = [0] * self.code_length
        
        # Place data bits in their positions
        for i, pos in enumerate(self.DATA_POSITIONS):
            code[pos] = data_bits[i]
        
        # Calculate and place parity bits
        for i, pos in enumerate(self.PARITY_POSITIONS):
            code[pos] = self._calculate_parity(code, i)
        
        # Add overall parity for extended Hamming code
        if self.extended:
            overall_parity = sum(code[:7]) % 2
            code[7] = overall_parity
        
        # Convert to integer
        result = 0
        for i, bit in enumerate(code):
            result |= (bit << (self.code_length - 1 - i))
        
        return result
    
    def encode_bits(self, data_bits: List[int]) -> List[int]:
        """
        Encode 4 data bits into Hamming code bits.
        
        Args:
            data_bits: List of 4 bits [D1, D2, D3, D4]
            
        Returns:
            List of Hamming code bits
            
        Raises:
            ValueError: If data_bits is not a list of 4 bits
        """
        if len(data_bits) != 4:
            raise ValueError(f"Expected 4 data bits, got {len(data_bits)}")
        
        if not all(b in (0, 1) for b in data_bits):
            raise ValueError("All bits must be 0 or 1")
        
        data = (data_bits[0] << 3) | (data_bits[1] << 2) | (data_bits[2] << 1) | data_bits[3]
        code = self.encode(data)
        
        return [(code >> (self.code_length - 1 - i)) & 1 for i in range(self.code_length)]
    
    def decode(self, code: int) -> Tuple[int, Optional[int]]:
        """
        Decode Hamming code, detecting and correcting errors.
        
        Args:
            code: Hamming code as integer
            
        Returns:
            Tuple of (decoded_data, error_position)
            - decoded_data: The corrected 4-bit data (0-15)
            - error_position: Position of detected error (0-indexed), or None if no error
            
        Raises:
            ValueError: If code has invalid bit length
        """
        max_code = (1 << self.code_length) - 1
        if not 0 <= code <= max_code:
            raise ValueError(f"Code must be {self.code_length} bits (0-{max_code}), got {code}")
        
        # Extract code bits
        code_bits = [(code >> (self.code_length - 1 - i)) & 1 for i in range(self.code_length)]
        
        # For extended code, check overall parity first
        double_error = False
        if self.extended:
            overall_parity = sum(code_bits) % 2
            if overall_parity != 0:
                # Odd parity means single error or triple error
                # We'll handle single error correction
                pass
        
        # Calculate syndrome (error position)
        syndrome = 0
        for i in range(3):  # 3 parity checks for Hamming(7,4)
            parity = self._calculate_parity(code_bits[:7], i)
            expected_parity = code_bits[self.PARITY_POSITIONS[i]]
            if parity != expected_parity:
                syndrome |= (1 << i)
        
        error_position = syndrome - 1 if syndrome > 0 else None  # 0-indexed
        
        # Check for double error in extended code
        if self.extended:
            overall_parity = sum(code_bits) % 2
            if syndrome == 0 and overall_parity == 1:
                # Error in overall parity bit (position 7)
                error_position = 7
            elif syndrome > 0 and overall_parity == 0:
                # Double error detected (even parity but syndrome indicates error)
                # Cannot correct, return original data with indication
                double_error = True
        
        # Correct error if detected
        corrected_bits = code_bits.copy()
        if error_position is not None and error_position < 7:
            corrected_bits[error_position] ^= 1  # Flip the erroneous bit
        
        # Extract data bits
        data_bits = [corrected_bits[pos] for pos in self.DATA_POSITIONS]
        data = (data_bits[0] << 3) | (data_bits[1] << 2) | (data_bits[2] << 1) | data_bits[3]
        
        # For double error, we still return the data but mark it
        if double_error:
            return (data, -1)  # -1 indicates uncorrectable double error
        
        return (data, error_position)
    
    def decode_bits(self, code_bits: List[int]) -> Tuple[List[int], Optional[int]]:
        """
        Decode Hamming code bits into data bits.
        
        Args:
            code_bits: List of Hamming code bits
            
        Returns:
            Tuple of (data_bits, error_position)
            - data_bits: List of 4 corrected data bits [D1, D2, D3, D4]
            - error_position: Position of detected error, or None if no error
        """
        if len(code_bits) != self.code_length:
            raise ValueError(f"Expected {self.code_length} code bits, got {len(code_bits)}")
        
        code = 0
        for i, bit in enumerate(code_bits):
            code |= (bit << (self.code_length - 1 - i))
        
        data, error_pos = self.decode(code)
        data_bits = [(data >> (3 - i)) & 1 for i in range(4)]
        
        return (data_bits, error_pos)
    
    def is_valid(self, code: int) -> Tuple[bool, Optional[int]]:
        """
        Check if a Hamming code is valid (no errors).
        
        Args:
            code: Hamming code as integer
            
        Returns:
            Tuple of (is_valid, error_position)
            - is_valid: True if no errors detected
            - error_position: Position of error if detected, None otherwise
        """
        _, error_pos = self.decode(code)
        return (error_pos is None, error_pos)
    
    def introduce_error(self, code: int, position: int) -> int:
        """
        Introduce a single-bit error at specified position.
        
        Args:
            code: Hamming code as integer
            position: 0-indexed position to flip
            
        Returns:
            Corrupted code with bit flipped at position
        """
        if not 0 <= position < self.code_length:
            raise ValueError(f"Position must be 0-{self.code_length-1}, got {position}")
        
        return code ^ (1 << (self.code_length - 1 - position))


class HammingStream:
    """
    Stream-based Hamming code encoder/decoder for multi-byte data.
    """
    
    def __init__(self, extended: bool = False):
        """
        Initialize stream encoder/decoder.
        
        Args:
            extended: If True, use extended Hamming(8,4) code
        """
        self.hamming = HammingCode(extended=extended)
        self.code_length = 8 if extended else 7
    
    def encode_bytes(self, data: bytes) -> List[int]:
        """
        Encode bytes into Hamming codes.
        
        Each byte is split into two 4-bit nibbles, each encoded separately.
        
        Args:
            data: Input bytes
            
        Returns:
            List of Hamming codes
        """
        codes = []
        for byte in data:
            # High nibble
            high = (byte >> 4) & 0x0F
            codes.append(self.hamming.encode(high))
            # Low nibble
            low = byte & 0x0F
            codes.append(self.hamming.encode(low))
        return codes
    
    def decode_bytes(self, codes: List[int]) -> Tuple[bytes, List[Optional[int]]]:
        """
        Decode Hamming codes back to bytes.
        
        Args:
            codes: List of Hamming codes (must be even length)
            
        Returns:
            Tuple of (decoded_bytes, error_positions)
        """
        if len(codes) % 2 != 0:
            raise ValueError(f"Expected even number of codes, got {len(codes)}")
        
        result = bytearray()
        error_positions = []
        
        for i in range(0, len(codes), 2):
            high, err1 = self.hamming.decode(codes[i])
            low, err2 = self.hamming.decode(codes[i + 1])
            
            byte = (high << 4) | low
            result.append(byte)
            error_positions.extend([err1, err2])
        
        return (bytes(result), error_positions)
    
    def encode_to_bits(self, data: bytes) -> List[int]:
        """
        Encode bytes into a flat list of Hamming code bits.
        
        Args:
            data: Input bytes
            
        Returns:
            Flat list of bits
        """
        codes = self.encode_bytes(data)
        bits = []
        for code in codes:
            for i in range(self.code_length):
                bits.append((code >> (self.code_length - 1 - i)) & 1)
        return bits
    
    def decode_from_bits(self, bits: List[int]) -> Tuple[bytes, List[Optional[int]]]:
        """
        Decode a flat list of bits back to bytes.
        
        Args:
            bits: Flat list of Hamming code bits
            
        Returns:
            Tuple of (decoded_bytes, error_positions)
        """
        bits_per_byte = self.code_length * 2
        if len(bits) % bits_per_byte != 0:
            raise ValueError(f"Bit count must be multiple of {bits_per_byte}, got {len(bits)}")
        
        codes = []
        for i in range(0, len(bits), self.code_length):
            code = 0
            for j in range(self.code_length):
                code |= (bits[i + j] << (self.code_length - 1 - j))
            codes.append(code)
        
        return self.decode_bytes(codes)


def hamming_distance(code1: int, code2: int, bits: int = 7) -> int:
    """
    Calculate Hamming distance between two codes.
    
    Args:
        code1: First code
        code2: Second code
        bits: Number of bits to compare
        
    Returns:
        Number of differing bits
    """
    xor = code1 ^ code2
    distance = 0
    while xor:
        distance += xor & 1
        xor >>= 1
    return distance


def generate_hamming_table(extended: bool = False) -> dict:
    """
    Generate encoding table for all 4-bit values.
    
    Args:
        extended: If True, generate extended Hamming(8,4) table
        
    Returns:
        Dictionary mapping data value to Hamming code
    """
    encoder = HammingCode(extended=extended)
    return {data: encoder.encode(data) for data in range(16)}


def calculate_code_rate(extended: bool = False) -> float:
    """
    Calculate the code rate (efficiency) of Hamming code.
    
    Args:
        extended: If True, calculate for extended Hamming(8,4)
        
    Returns:
        Code rate as ratio of data bits to total bits
    """
    if extended:
        return 4 / 8  # 4 data bits in 8 total bits
    return 4 / 7  # 4 data bits in 7 total bits


# Convenience functions
def encode(data: int, extended: bool = False) -> int:
    """Convenience function to encode 4-bit data."""
    return HammingCode(extended=extended).encode(data)


def decode(code: int, extended: bool = False) -> Tuple[int, Optional[int]]:
    """Convenience function to decode Hamming code."""
    return HammingCode(extended=extended).decode(code)


if __name__ == "__main__":
    # Quick demonstration
    print("Hamming Code Utilities Demo")
    print("=" * 40)
    
    # Standard Hamming(7,4)
    hamming = HammingCode(extended=False)
    print("\nStandard Hamming(7,4):")
    for data in range(16):
        code = hamming.encode(data)
        print(f"  Data: {data:2d} ({data:04b}) -> Code: {code:07b} ({code:3d})")
    
    # Error correction demo
    print("\nError Correction Demo:")
    original_data = 10  # 1010
    code = hamming.encode(original_data)
    print(f"  Original data: {original_data} ({original_data:04b})")
    print(f"  Encoded code: {code:07b}")
    
    # Introduce error at position 2
    corrupted = hamming.introduce_error(code, 2)
    print(f"  Corrupted code (error at pos 2): {corrupted:07b}")
    
    decoded, error_pos = hamming.decode(corrupted)
    print(f"  Decoded data: {decoded} ({decoded:04b})")
    print(f"  Error detected at position: {error_pos}")
    print(f"  Correction successful: {decoded == original_data}")
    
    # Extended Hamming(8,4)
    print("\nExtended Hamming(8,4):")
    hamming_ext = HammingCode(extended=True)
    code_ext = hamming_ext.encode(original_data)
    print(f"  Data: {original_data} ({original_data:04b}) -> Code: {code_ext:08b}")