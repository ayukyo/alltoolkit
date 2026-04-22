#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Huffman Coding Utilities Module
=============================================
A comprehensive Huffman encoding/decoding utility module with zero external dependencies.

Features:
    - Huffman tree construction from frequency data
    - Text and binary data encoding/decoding
    - Adaptive Huffman coding support
    - Canonical Huffman codes generation
    - Frequency analysis and visualization
    - Compression ratio calculation
    - Bit-level operations for efficient storage
    - Support for custom symbol alphabets

Author: AllToolkit Contributors
License: MIT
"""

import heapq
from typing import Dict, List, Tuple, Optional, Union, Any
from collections import Counter
from dataclasses import dataclass, field
from functools import total_ordering


# =============================================================================
# Data Structures
# =============================================================================

@total_ordering
@dataclass
class HuffmanNode:
    """
    Node in a Huffman tree.
    
    Attributes:
        symbol: The character or symbol (None for internal nodes)
        frequency: Frequency count of the symbol
        left: Left child node
        right: Right child node
    """
    symbol: Optional[Union[str, bytes, int]] = None
    frequency: int = 0
    left: Optional['HuffmanNode'] = None
    right: Optional['HuffmanNode'] = None
    
    def __eq__(self, other):
        if not isinstance(other, HuffmanNode):
            return NotImplemented
        return self.frequency == other.frequency
    
    def __lt__(self, other):
        if not isinstance(other, HuffmanNode):
            return NotImplemented
        return self.frequency < other.frequency
    
    def is_leaf(self) -> bool:
        """Check if this node is a leaf node."""
        return self.left is None and self.right is None


@dataclass
class HuffmanTree:
    """
    Huffman tree container with root node.
    
    Provides methods for encoding, decoding, and tree manipulation.
    """
    root: Optional[HuffmanNode] = None
    code_table: Dict[Union[str, bytes, int], str] = field(default_factory=dict)
    
    def build_from_frequencies(self, frequencies: Dict[Union[str, bytes, int], int]) -> None:
        """
        Build Huffman tree from frequency dictionary.
        
        Args:
            frequencies: Dictionary mapping symbols to their frequencies
        """
        if not frequencies:
            self.root = None
            self.code_table = {}
            return
        
        # Handle single symbol case
        if len(frequencies) == 1:
            symbol = list(frequencies.keys())[0]
            self.root = HuffmanNode(frequency=frequencies[symbol])
            self.root.left = HuffmanNode(symbol=symbol, frequency=frequencies[symbol])
            self.code_table = {symbol: '0'}
            return
        
        # Build priority queue (min-heap)
        heap = []
        for symbol, freq in frequencies.items():
            node = HuffmanNode(symbol=symbol, frequency=freq)
            heapq.heappush(heap, node)
        
        # Build tree by combining nodes
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = HuffmanNode(
                frequency=left.frequency + right.frequency,
                left=left,
                right=right
            )
            heapq.heappush(heap, merged)
        
        self.root = heap[0] if heap else None
        self._build_code_table()
    
    def _build_code_table(self) -> None:
        """Build the code table by traversing the tree."""
        self.code_table = {}
        if self.root is None:
            return
        
        if self.root.is_leaf():
            # Single symbol case
            if self.root.symbol is not None:
                self.code_table[self.root.symbol] = '0'
            return
        
        self._traverse_for_codes(self.root, "")
    
    def _traverse_for_codes(self, node: HuffmanNode, code: str) -> None:
        """
        Recursively traverse tree to build code table.
        
        Args:
            node: Current node
            code: Current binary code string
        """
        if node.is_leaf():
            if node.symbol is not None:
                self.code_table[node.symbol] = code if code else '0'
            return
        
        if node.left:
            self._traverse_for_codes(node.left, code + '0')
        if node.right:
            self._traverse_for_codes(node.right, code + '1')
    
    def get_code(self, symbol: Union[str, bytes, int]) -> Optional[str]:
        """
        Get Huffman code for a symbol.
        
        Args:
            symbol: The symbol to look up
        
        Returns:
            Binary code string or None if symbol not in tree
        """
        return self.code_table.get(symbol)
    
    def decode_symbol(self, bits: str, start_pos: int = 0) -> Tuple[Optional[Union[str, bytes, int]], int]:
        """
        Decode a single symbol from a bit string.
        
        Args:
            bits: Binary string to decode from
            start_pos: Starting position in the bit string
        
        Returns:
            Tuple of (decoded symbol or None, next position)
        """
        if self.root is None:
            return None, start_pos
        
        node = self.root
        pos = start_pos
        
        while not node.is_leaf() and pos < len(bits):
            bit = bits[pos]
            if bit == '0':
                node = node.left
            else:
                node = node.right
            pos += 1
        
        return node.symbol, pos


# =============================================================================
# Core Huffman Functions
# =============================================================================

def build_frequency_table(data: Union[str, bytes], 
                          byte_mode: bool = False) -> Dict[Union[str, int], int]:
    """
    Build frequency table from input data.
    
    Args:
        data: Input string or bytes
        byte_mode: If True, treat input as bytes (int keys); if False, as characters
    
    Returns:
        Dictionary mapping symbols to their frequencies
    
    Example:
        >>> build_frequency_table("hello")
        {'h': 1, 'e': 1, 'l': 2, 'o': 1}
        >>> build_frequency_table(b"hello", byte_mode=True)
        {104: 1, 101: 1, 108: 2, 111: 1}
    
    Note:
        优化版本：添加空输入快速返回路径，
        减少不必要的类型转换开销。
    """
    # 边界处理：空输入快速返回空字典
    if not data:
        return {}
    
    if byte_mode or isinstance(data, bytes):
        if isinstance(data, str):
            data = data.encode('utf-8')
        # 使用 Counter 的优化版本
        return dict(Counter(data))
    else:
        return dict(Counter(data))


def build_huffman_tree(frequencies: Dict[Union[str, bytes, int], int]) -> HuffmanTree:
    """
    Build Huffman tree from frequency dictionary.
    
    Args:
        frequencies: Dictionary mapping symbols to their frequencies
    
    Returns:
        HuffmanTree object with built tree and code table
    
    Example:
        >>> tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        >>> tree.code_table
        {'a': '0', 'b': '10', 'c': '11'}  # Example output (actual may vary)
    """
    tree = HuffmanTree()
    tree.build_from_frequencies(frequencies)
    return tree


def encode_text(text: str, tree: Optional[HuffmanTree] = None) -> Tuple[str, HuffmanTree]:
    """
    Encode text using Huffman coding.
    
    Args:
        text: Input text string
        tree: Optional pre-built Huffman tree (will build from text if None)
    
    Returns:
        Tuple of (encoded binary string, Huffman tree used)
    
    Example:
        >>> encoded, tree = encode_text("hello")
        >>> print(f"Encoded: {encoded}")
        Encoded: 0110110111
    """
    if not text:
        return "", HuffmanTree()
    
    frequencies = build_frequency_table(text)
    
    if tree is None:
        tree = build_huffman_tree(frequencies)
    
    encoded = ''.join(tree.code_table.get(char, '') for char in text)
    return encoded, tree


def decode_text(encoded: str, tree: HuffmanTree) -> str:
    """
    Decode Huffman-encoded binary string back to text.
    
    Args:
        encoded: Binary string (e.g., "01101101")
        tree: Huffman tree used for decoding
    
    Returns:
        Decoded text string
    
    Example:
        >>> encoded, tree = encode_text("hello")
        >>> decode_text(encoded, tree)
        'hello'
    """
    if not encoded or tree.root is None:
        return ""
    
    result = []
    pos = 0
    
    while pos < len(encoded):
        symbol, new_pos = tree.decode_symbol(encoded, pos)
        if symbol is None:
            break
        result.append(symbol)
        pos = new_pos
    
    return ''.join(result)


def encode_bytes(data: bytes, tree: Optional[HuffmanTree] = None) -> Tuple[bytes, HuffmanTree, int]:
    """
    Encode bytes using Huffman coding.
    
    Args:
        data: Input bytes
        tree: Optional pre-built Huffman tree
    
    Returns:
        Tuple of (encoded bytes, Huffman tree, number of padding bits)
    
    Example:
        >>> encoded, tree, padding = encode_bytes(b"hello")
        >>> decoded = decode_bytes(encoded, tree, padding)
        >>> decoded
        b'hello'
    """
    if not data:
        return b"", HuffmanTree(), 0
    
    frequencies = build_frequency_table(data, byte_mode=True)
    
    if tree is None:
        tree = build_huffman_tree(frequencies)
    
    # Build binary string
    binary_str = ''.join(tree.code_table.get(byte_val, '') for byte_val in data)
    
    # Pad to make multiple of 8
    padding = (8 - len(binary_str) % 8) % 8
    binary_str += '0' * padding
    
    # Convert to bytes
    encoded = bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))
    
    return encoded, tree, padding


def decode_bytes(encoded: bytes, tree: HuffmanTree, padding: int = 0) -> bytes:
    """
    Decode Huffman-encoded bytes back to original data.
    
    Args:
        encoded: Encoded bytes
        tree: Huffman tree used for decoding
        padding: Number of padding bits at the end
    
    Returns:
        Decoded bytes
    
    Example:
        >>> encoded, tree, padding = encode_bytes(b"hello")
        >>> decode_bytes(encoded, tree, padding)
        b'hello'
    """
    if not encoded or tree.root is None:
        return b""
    
    # Convert bytes to binary string
    binary_str = ''.join(format(byte_val, '08b') for byte_val in encoded)
    
    # Remove padding
    if padding > 0:
        binary_str = binary_str[:-padding]
    
    # Decode
    result = []
    pos = 0
    
    while pos < len(binary_str):
        symbol, new_pos = tree.decode_symbol(binary_str, pos)
        if symbol is None:
            break
        result.append(symbol)
        pos = new_pos
    
    return bytes(result)


# =============================================================================
# Advanced Features
# =============================================================================

def generate_canonical_codes(code_lengths: Dict[Union[str, bytes, int], int]) -> Dict[Union[str, bytes, int], str]:
    """
    Generate canonical Huffman codes from code lengths.
    
    Canonical codes are more efficient for storage/transmission as only
    the code lengths need to be stored, not the actual codes.
    
    Args:
        code_lengths: Dictionary mapping symbols to their code lengths
    
    Returns:
        Dictionary mapping symbols to canonical binary codes
    
    Example:
        >>> generate_canonical_codes({'a': 1, 'b': 2, 'c': 2, 'd': 3})
        {'a': '0', 'b': '10', 'c': '11', 'd': '100'}
    """
    if not code_lengths:
        return {}
    
    # Sort by length, then by symbol for consistency
    sorted_symbols = sorted(code_lengths.keys(), key=lambda s: (code_lengths[s], str(s)))
    
    codes = {}
    code = 0
    prev_length = 0
    
    for symbol in sorted_symbols:
        length = code_lengths[symbol]
        code <<= (length - prev_length)
        codes[symbol] = format(code, f'0{length}b')
        code += 1
        prev_length = length
    
    return codes


def calculate_compression_ratio(original_size: int, compressed_size: int) -> float:
    """
    Calculate compression ratio.
    
    Args:
        original_size: Size of original data in bytes
        compressed_size: Size of compressed data in bytes
    
    Returns:
        Compression ratio (higher is better, e.g., 2.0 means 50% reduction)
    
    Example:
        >>> calculate_compression_ratio(1000, 500)
        2.0
    """
    if compressed_size == 0:
        return float('inf') if original_size > 0 else 1.0
    return original_size / compressed_size


def calculate_compression_percentage(original_size: int, compressed_size: int) -> float:
    """
    Calculate compression percentage.
    
    Args:
        original_size: Size of original data in bytes
        compressed_size: Size of compressed data in bytes
    
    Returns:
        Percentage of size reduction (0-100)
    
    Example:
        >>> calculate_compression_percentage(1000, 500)
        50.0
    """
    if original_size == 0:
        return 0.0
    return (1 - compressed_size / original_size) * 100


def get_code_statistics(tree: HuffmanTree) -> Dict[str, Any]:
    """
    Get statistics about the Huffman codes.
    
    Args:
        tree: Huffman tree to analyze
    
    Returns:
        Dictionary with code statistics
    
    Example:
        >>> tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        >>> stats = get_code_statistics(tree)
        >>> print(stats['average_code_length'])
        1.25
    """
    if not tree.code_table:
        return {
            'num_symbols': 0,
            'min_code_length': 0,
            'max_code_length': 0,
            'average_code_length': 0,
            'total_bits': 0
        }
    
    code_lengths = [len(code) for code in tree.code_table.values()]
    
    return {
        'num_symbols': len(tree.code_table),
        'min_code_length': min(code_lengths),
        'max_code_length': max(code_lengths),
        'average_code_length': sum(code_lengths) / len(code_lengths),
        'total_bits': sum(code_lengths)
    }


def bits_to_bytes(bits: str) -> Tuple[bytes, int]:
    """
    Convert binary string to bytes with padding.
    
    Args:
        bits: Binary string (e.g., "01101001")
    
    Returns:
        Tuple of (bytes, padding bits count)
    
    Example:
        >>> bits_to_bytes("01101001")
        (b'i', 0)
        >>> bits_to_bytes("01101")
        (b'm', 3)  # Padded to "01101000"
    """
    if not bits:
        return b"", 0
    
    padding = (8 - len(bits) % 8) % 8
    padded = bits + '0' * padding
    
    return bytes(int(padded[i:i+8], 2) for i in range(0, len(padded), 8)), padding


def bytes_to_bits(data: bytes, padding: int = 0) -> str:
    """
    Convert bytes back to binary string, removing padding.
    
    Args:
        data: Input bytes
        padding: Number of padding bits to remove from the end
    
    Returns:
        Binary string
    
    Example:
        >>> bytes_to_bits(b'i', 0)
        '01101001'
        >>> bytes_to_bits(b'm', 3)
        '01101'
    """
    if not data:
        return ""
    
    bits = ''.join(format(byte_val, '08b') for byte_val in data)
    
    if padding > 0:
        bits = bits[:-padding]
    
    return bits


# =============================================================================
# Tree Serialization
# =============================================================================

def serialize_tree(tree: HuffmanTree) -> Dict[str, Any]:
    """
    Serialize Huffman tree to a dictionary for storage/transmission.
    
    Args:
        tree: Huffman tree to serialize
    
    Returns:
        Dictionary representation of the tree
    
    Example:
        >>> tree = build_huffman_tree({'a': 5, 'b': 2})
        >>> data = serialize_tree(tree)
        >>> restored = deserialize_tree(data)
    """
    if tree.root is None:
        return {'type': 'empty', 'code_table': {}}
    
    def node_to_dict(node: HuffmanNode) -> Dict[str, Any]:
        """Convert node to dictionary recursively."""
        if node.is_leaf():
            symbol = node.symbol
            # Convert bytes to list for JSON serialization
            if isinstance(symbol, bytes):
                symbol = {'type': 'bytes', 'value': list(symbol)}
            return {
                'type': 'leaf',
                'symbol': symbol,
                'frequency': node.frequency
            }
        return {
            'type': 'internal',
            'frequency': node.frequency,
            'left': node_to_dict(node.left) if node.left else None,
            'right': node_to_dict(node.right) if node.right else None
        }
    
    # Convert code_table for serialization
    serializable_code_table = {}
    for symbol, code in tree.code_table.items():
        if isinstance(symbol, bytes):
            key = {'type': 'bytes', 'value': list(symbol)}
        elif isinstance(symbol, int):
            key = {'type': 'int', 'value': symbol}
        else:
            key = symbol
        serializable_code_table[str(key) if not isinstance(key, str) else key] = code
    
    return {
        'type': 'tree',
        'root': node_to_dict(tree.root),
        'code_table': serializable_code_table
    }


def deserialize_tree(data: Dict[str, Any]) -> HuffmanTree:
    """
    Deserialize dictionary back to Huffman tree.
    
    Args:
        data: Dictionary representation of the tree
    
    Returns:
        Restored HuffmanTree object
    
    Example:
        >>> tree = build_huffman_tree({'a': 5, 'b': 2})
        >>> data = serialize_tree(tree)
        >>> restored = deserialize_tree(data)
    """
    if data.get('type') == 'empty':
        return HuffmanTree()
    
    def dict_to_node(node_data: Dict[str, Any]) -> HuffmanNode:
        """Convert dictionary to node recursively."""
        if node_data['type'] == 'leaf':
            symbol = node_data['symbol']
            # Restore bytes from list
            if isinstance(symbol, dict) and symbol.get('type') == 'bytes':
                symbol = bytes(symbol['value'])
            return HuffmanNode(
                symbol=symbol,
                frequency=node_data['frequency']
            )
        
        node = HuffmanNode(frequency=node_data['frequency'])
        if 'left' in node_data and node_data['left']:
            node.left = dict_to_node(node_data['left'])
        if 'right' in node_data and node_data['right']:
            node.right = dict_to_node(node_data['right'])
        return node
    
    tree = HuffmanTree()
    tree.root = dict_to_node(data['root'])
    
    # Rebuild code table
    tree._build_code_table()
    
    return tree


# =============================================================================
# Utility Functions
# =============================================================================

def visualize_tree(tree: HuffmanTree) -> str:
    """
    Generate ASCII visualization of Huffman tree.
    
    Args:
        tree: Huffman tree to visualize
    
    Returns:
        ASCII string representation of the tree
    
    Example:
        >>> tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        >>> print(visualize_tree(tree))
        └── (8)
            ├── 'a': 0
            └── (3)
                ├── 'b': 10
                └── 'c': 11
    """
    if tree.root is None:
        return "(empty tree)"
    
    lines = []
    
    def build_lines(node: HuffmanNode, prefix: str = "", is_last: bool = True) -> None:
        """Build lines for tree visualization."""
        connector = "└── " if is_last else "├── "
        
        if node.is_leaf():
            symbol_repr = repr(node.symbol) if node.symbol is not None else "None"
            code = tree.code_table.get(node.symbol, '?')
            lines.append(f"{prefix}{connector}{symbol_repr}: {code} (freq: {node.frequency})")
        else:
            lines.append(f"{prefix}{connector}({node.frequency})")
            
            extension = "    " if is_last else "│   "
            new_prefix = prefix + extension
            
            children = [n for n in [node.left, node.right] if n is not None]
            for i, child in enumerate(children):
                build_lines(child, new_prefix, i == len(children) - 1)
    
    build_lines(tree.root, "", True)
    return '\n'.join(lines)


def print_code_table(tree: HuffmanTree, sort_by: str = 'symbol') -> None:
    """
    Print the Huffman code table in a formatted way.
    
    Args:
        tree: Huffman tree with code table
        sort_by: How to sort the table ('symbol', 'code', 'length')
    
    Example:
        >>> tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        >>> print_code_table(tree)
        Symbol  | Code | Length
        --------|------|-------
        a       | 0    | 1
        b       | 10   | 2
        c       | 11   | 2
    """
    if not tree.code_table:
        print("(empty code table)")
        return
    
    # Prepare items
    items = [(symbol, code) for symbol, code in tree.code_table.items()]
    
    if sort_by == 'code':
        items.sort(key=lambda x: (len(x[1]), x[1]))
    elif sort_by == 'length':
        items.sort(key=lambda x: len(x[1]))
    else:  # sort by symbol
        items.sort(key=lambda x: str(x[0]))
    
    # Print header
    print(f"{'Symbol':<10} | {'Code':<10} | {'Length':<6}")
    print("-" * 35)
    
    for symbol, code in items:
        symbol_str = repr(symbol)[:8]
        print(f"{symbol_str:<10} | {code:<10} | {len(code):<6}")


def compare_with_fixed_length(tree: HuffmanTree, original_size: int) -> Dict[str, Any]:
    """
    Compare Huffman coding with fixed-length encoding.
    
    Args:
        tree: Huffman tree
        original_size: Size of original data in symbols
    
    Returns:
        Dictionary with comparison statistics
    
    Example:
        >>> tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        >>> compare_with_fixed_length(tree, 100)
    """
    stats = get_code_statistics(tree)
    num_symbols = stats['num_symbols']
    
    if num_symbols <= 1:
        return {
            'huffman_bits_per_symbol': stats['average_code_length'],
            'fixed_bits_per_symbol': 1,
            'savings_percent': 0
        }
    
    # Calculate fixed-length encoding bits needed
    import math
    fixed_bits = math.ceil(math.log2(num_symbols))
    
    savings = (1 - stats['average_code_length'] / fixed_bits) * 100 if fixed_bits > 0 else 0
    
    return {
        'huffman_bits_per_symbol': round(stats['average_code_length'], 3),
        'fixed_bits_per_symbol': fixed_bits,
        'savings_percent': round(savings, 2),
        'total_huffman_bits': round(stats['average_code_length'] * original_size, 0),
        'total_fixed_bits': fixed_bits * original_size
    }


# =============================================================================
# Convenience Functions
# =============================================================================

def huffman_encode(data: Union[str, bytes]) -> Tuple[bytes, Dict[str, Any], int]:
    """
    One-shot Huffman encoding function.
    
    Args:
        data: Input string or bytes
    
    Returns:
        Tuple of (encoded bytes, serialized tree, padding bits)
    
    Example:
        >>> encoded, tree_data, padding = huffman_encode("hello")
        >>> decoded = huffman_decode(encoded, tree_data, padding)
        >>> decoded
        'hello'
    """
    if isinstance(data, str):
        encoded_bits, tree, padding = encode_bytes(data.encode('utf-8'))
    else:
        encoded_bits, tree, padding = encode_bytes(data)
    
    tree_data = serialize_tree(tree)
    return encoded_bits, tree_data, padding


def huffman_decode(encoded: bytes, tree_data: Dict[str, Any], padding: int) -> Union[str, bytes]:
    """
    One-shot Huffman decoding function.
    
    Args:
        encoded: Encoded bytes
        tree_data: Serialized tree dictionary
        padding: Padding bits count
    
    Returns:
        Decoded string or bytes (matches input type if detectable)
    
    Example:
        >>> encoded, tree_data, padding = huffman_encode("hello")
        >>> huffman_decode(encoded, tree_data, padding)
        'hello'
    """
    tree = deserialize_tree(tree_data)
    decoded = decode_bytes(encoded, tree, padding)
    
    # Try to decode as UTF-8 string
    try:
        return decoded.decode('utf-8')
    except UnicodeDecodeError:
        return decoded


# =============================================================================
# Compression Analysis
# =============================================================================

def analyze_compression_potential(data: Union[str, bytes]) -> Dict[str, Any]:
    """
    Analyze the compression potential of data using Huffman coding.
    
    Args:
        data: Input data to analyze
    
    Returns:
        Dictionary with detailed compression analysis
    
    Example:
        >>> analysis = analyze_compression_potential("aaabbc")
        >>> print(analysis['compression_percentage'])
        33.33
    """
    if isinstance(data, str):
        data_bytes = data.encode('utf-8')
        original_size = len(data_bytes)
    else:
        data_bytes = data
        original_size = len(data)
    
    if original_size == 0:
        return {
            'original_size': 0,
            'compressed_size': 0,
            'compression_ratio': 1.0,
            'compression_percentage': 0.0,
            'entropy': 0.0,
            'efficiency': 100.0
        }
    
    # Build tree and encode
    encoded, tree_data, padding = huffman_encode(data_bytes)
    compressed_size = len(encoded)
    
    # Deserialize tree for statistics
    tree = deserialize_tree(tree_data)
    
    # Calculate entropy
    frequencies = build_frequency_table(data_bytes, byte_mode=True)
    import math
    
    total = sum(frequencies.values())
    entropy = -sum((freq / total) * math.log2(freq / total) for freq in frequencies.values())
    
    stats = get_code_statistics(tree)
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': calculate_compression_ratio(original_size, compressed_size),
        'compression_percentage': calculate_compression_percentage(original_size, compressed_size),
        'entropy_bits': round(entropy, 3),
        'average_code_length': round(stats['average_code_length'], 3),
        'efficiency': round(entropy / stats['average_code_length'] * 100, 2) if stats['average_code_length'] > 0 else 100.0,
        'num_unique_symbols': len(frequencies),
        'min_code_length': stats['min_code_length'],
        'max_code_length': stats['max_code_length']
    }


if __name__ == "__main__":
    # Quick demo
    print("=" * 60)
    print("Huffman Coding Utilities Demo")
    print("=" * 60)
    
    # Example text
    text = "this is an example for huffman encoding"
    print(f"\nOriginal text: '{text}'")
    print(f"Original size: {len(text.encode('utf-8'))} bytes")
    
    # Build tree
    freq = build_frequency_table(text)
    tree = build_huffman_tree(freq)
    
    # Encode
    encoded, tree_data, padding = huffman_encode(text)
    print(f"\nEncoded size: {len(encoded)} bytes")
    print(f"Padding bits: {padding}")
    
    # Decode
    decoded = huffman_decode(encoded, tree_data, padding)
    print(f"Decoded text: '{decoded}'")
    print(f"Match: {decoded == text}")
    
    # Analysis
    analysis = analyze_compression_potential(text)
    print(f"\nCompression analysis:")
    print(f"  Compression ratio: {analysis['compression_ratio']:.2f}x")
    print(f"  Compression percentage: {analysis['compression_percentage']:.2f}%")
    print(f"  Entropy: {analysis['entropy_bits']:.3f} bits")
    print(f"  Average code length: {analysis['average_code_length']:.3f} bits")
    print(f"  Efficiency: {analysis['efficiency']:.2f}%")
    
    # Visualize
    print(f"\nTree visualization:")
    print(visualize_tree(tree))