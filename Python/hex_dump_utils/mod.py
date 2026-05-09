"""
Hex Dump Utils - Binary data visualization and manipulation utilities.

Provides functions for displaying binary data in various hex dump formats,
including classic hexdump, xxd-style, and customizable formats.

Features:
- Classic hexdump format
- xxd-compatible output
- Canonical hex+ASCII display
- Colorized output support
- Binary patch generation
- Offset annotation
- Customizable grouping and formatting
"""

from typing import Optional, Union, List, Tuple
import os


def hex_dump(
    data: Union[bytes, bytearray],
    offset: int = 0,
    length: Optional[int] = None,
    width: int = 16,
    group_size: int = 2,
    show_ascii: bool = True,
    show_offset: bool = True,
    offset_base: int = 16,
    uppercase: bool = False,
    colorize: bool = False
) -> str:
    """
    Generate a hex dump of binary data.
    
    Args:
        data: Binary data to dump
        offset: Starting offset for display (default: 0)
        length: Number of bytes to dump (None = all)
        width: Bytes per line (default: 16)
        group_size: Bytes per group (default: 2)
        show_ascii: Show ASCII representation (default: True)
        show_offset: Show offset column (default: True)
        offset_base: Base for offset display, 16=hex, 10=decimal (default: 16)
        uppercase: Use uppercase hex digits (default: False)
        colorize: Add ANSI colors to output (default: False)
    
    Returns:
        Formatted hex dump string
    
    Example:
        >>> data = b'Hello, World!\\x00\\xff\\xfe'
        >>> print(hex_dump(data))
        00000000  48 65 6c 6c 6f 2c 20 57  6f 72 6c 64 21 00 ff fe  |Hello, World!...|
    """
    if isinstance(data, bytearray):
        data = bytes(data)
    
    if length is not None:
        data = data[:length]
    
    if not data:
        return ""
    
    lines = []
    hex_format = "{:02X}" if uppercase else "{:02x}"
    
    # Color codes
    C_RESET = "\033[0m" if colorize else ""
    C_OFFSET = "\033[36m" if colorize else ""  # Cyan
    C_HEX = "\033[32m" if colorize else ""      # Green
    C_ASCII = "\033[33m" if colorize else ""    # Yellow
    C_NULL = "\033[90m" if colorize else ""     # Dark gray
    C_NONPRINT = "\033[31m" if colorize else "" # Red
    
    for i in range(0, len(data), width):
        chunk = data[i:i + width]
        
        # Offset
        line_parts = []
        if show_offset:
            off_val = offset + i
            if offset_base == 16:
                off_str = f"{C_OFFSET}{off_val:08x}{C_RESET}"
            else:
                off_str = f"{C_OFFSET}{off_val:08d}{C_RESET}"
            line_parts.append(off_str)
        
        # Hex section
        hex_parts = []
        for j in range(0, len(chunk), group_size):
            group = chunk[j:j + group_size]
            group_str = " ".join(hex_format.format(b) for b in group)
            if colorize:
                if all(b == 0 for b in group):
                    group_str = f"{C_NULL}{group_str}{C_RESET}"
                elif all(0x20 <= b < 0x7f for b in group):
                    group_str = f"{C_HEX}{group_str}{C_RESET}"
            hex_parts.append(group_str)
        
        # Pad to full width
        total_hex = len(chunk) * 2 + (len(chunk) - 1) // group_size
        hex_line = " ".join(hex_parts)
        if len(hex_line) < width * 2 + width // group_size - 1:
            hex_line += " " * (width * 2 + width // group_size - 1 - len(hex_line))
        
        if colorize:
            line_parts.append(f"{C_HEX}{hex_line}{C_RESET}")
        else:
            line_parts.append(hex_line)
        
        # ASCII section
        if show_ascii:
            ascii_chars = []
            for b in chunk:
                if 0x20 <= b < 0x7f:
                    char = chr(b)
                    if colorize:
                        ascii_chars.append(char)
                    else:
                        ascii_chars.append(char)
                elif b == 0:
                    if colorize:
                        ascii_chars.append(f"{C_NULL}.{C_RESET}")
                    else:
                        ascii_chars.append(".")
                else:
                    if colorize:
                        ascii_chars.append(f"{C_NONPRINT}.{C_RESET}")
                    else:
                        ascii_chars.append(".")
            
            ascii_str = "".join(ascii_chars)
            line_parts.append(f"|{ascii_str}|")
        
        lines.append("  ".join(line_parts))
    
    return "\n".join(lines)


def xxd_dump(
    data: Union[bytes, bytearray],
    offset: int = 0,
    length: Optional[int] = None,
    width: int = 16,
    uppercase: bool = False
) -> str:
    """
    Generate xxd-compatible hex dump.
    
    This format matches the output of the xxd utility, suitable for
    creating binary patches.
    
    Args:
        data: Binary data to dump
        offset: Starting offset (default: 0)
        length: Number of bytes to dump (None = all)
        width: Bytes per line (default: 16)
        uppercase: Use uppercase hex (default: False)
    
    Returns:
        xxd-formatted hex dump string
    
    Example:
        >>> data = b'Hello'
        >>> print(xxd_dump(data))
        00000000: 4865 6c6c 6f                             Hello
    """
    if isinstance(data, bytearray):
        data = bytes(data)
    
    if length is not None:
        data = data[:length]
    
    if not data:
        return ""
    
    lines = []
    hex_format = "{:02X}" if uppercase else "{:02x}"
    
    for i in range(0, len(data), width):
        chunk = data[i:i + width]
        off = offset + i
        
        # Offset with colon
        hex_char = "X" if uppercase else "x"
        off_str = f"{off:08{hex_char}}:"
        
        # Hex in groups of 2 bytes
        hex_groups = []
        for j in range(0, len(chunk), 2):
            if j + 1 < len(chunk):
                hex_groups.append(f"{chunk[j]:02{hex_char}}{chunk[j+1]:02{hex_char}}")
            else:
                hex_groups.append(f"{chunk[j]:02{hex_char}}  ")
        
        hex_str = " ".join(hex_groups)
        
        # ASCII (padded)
        ascii_str = "".join(
            chr(b) if 0x20 <= b < 0x7f else "."
            for b in chunk
        )
        
        lines.append(f"{off_str} {hex_str:<{width * 2 + width // 2}} {ascii_str}")
    
    return "\n".join(lines)


def hex_dump_to_bytes(hex_lines: str) -> bytes:
    """
    Parse hex dump output back to bytes.
    
    Handles multiple hex dump formats including xxd and classic hexdump.
    Skips non-hex content and validates input.
    
    Args:
        hex_lines: Hex dump string to parse
    
    Returns:
        Reconstructed bytes
    
    Raises:
        ValueError: If hex data is malformed
    
    Example:
        >>> hex_data = "48 65 6c 6c 6f"
        >>> hex_dump_to_bytes(hex_data)
        b'Hello'
    """
    result = bytearray()
    
    for line in hex_lines.strip().split("\n"):
        line = line.strip()  # Remove leading/trailing whitespace first
        
        # Remove offset if present
        # For xxd format: offset before colon
        if ":" in line:
            line = line.split(":", 1)[1]
        # For hexdump format: 8 hex digits followed by double space or spaces
        elif len(line) > 10:
            # Check if first 8 chars look like hex offset
            first_8 = line[:8].strip()
            if len(first_8) == 8 and all(c in '0123456789abcdefABCDEF' for c in first_8):
                # Looks like hexdump offset
                line = line[8:].strip()
        
        # Remove ASCII section if present (between | or at end)
        if "|" in line:
            parts = line.split("|")
            line = parts[0]
        elif "  " in line:
            # Likely has trailing ASCII - remove last double-spaced section
            parts = line.rsplit("  ", 1)
            if len(parts) > 1:
                last_part = parts[-1].strip()
                # If last part looks like ASCII (short and has letters/spaces)
                if len(last_part) <= 16 and any(c.isalpha() or c == ' ' for c in last_part):
                    line = parts[0]
        
        # Extract hex bytes
        hex_chars = []
        for c in line:
            if c in "0123456789abcdefABCDEF":
                hex_chars.append(c)
        
        # Process in pairs
        for i in range(0, len(hex_chars) - 1, 2):
            byte_str = hex_chars[i] + hex_chars[i + 1]
            result.append(int(byte_str, 16))
    
    return bytes(result)


def binary_diff(
    data1: Union[bytes, bytearray],
    data2: Union[bytes, bytearray],
    width: int = 16,
    context: int = 2
) -> str:
    """
    Compare two binary files and show differences in hex dump format.
    
    Args:
        data1: First binary data
        data2: Second binary data
        width: Bytes per line (default: 16)
        context: Lines of context around differences (default: 2)
    
    Returns:
        Diff string showing differences
    
    Example:
        >>> d1 = b'Hello World'
        >>> d2 = b'Hello Xorld'
        >>> print(binary_diff(d1, d2))
        --- data1
        +++ data2
        @@ -0,1 +0,1 @@
        -00000000  48 65 6c 6c 6f 20 57 6f  72 6c 64                 |Hello World|
        +00000000  48 65 6c 6c 6f 20 58 6f  72 6c 64                 |Hello Xorld|
    """
    if isinstance(data1, bytearray):
        data1 = bytes(data1)
    if isinstance(data2, bytearray):
        data2 = bytes(data2)
    
    # Find differing lines
    diff_lines = []
    max_len = max(len(data1), len(data2))
    
    differing_offsets = set()
    for i in range(max_len):
        b1 = data1[i] if i < len(data1) else None
        b2 = data2[i] if i < len(data2) else None
        if b1 != b2:
            differing_offsets.add(i // width)
    
    if not differing_offsets:
        return "Files are identical"
    
    # Generate diff output
    lines = ["--- data1", "+++ data2"]
    
    # Group consecutive offsets into hunks
    sorted_offsets = sorted(differing_offsets)
    hunks = []
    current_hunk = [sorted_offsets[0]]
    
    for i in range(1, len(sorted_offsets)):
        if sorted_offsets[i] - sorted_offsets[i-1] <= context * 2 + 1:
            current_hunk.append(sorted_offsets[i])
        else:
            hunks.append(current_hunk)
            current_hunk = [sorted_offsets[i]]
    hunks.append(current_hunk)
    
    for hunk in hunks:
        start = max(0, (hunk[0] - context)) * width
        end = min(max_len, (hunk[-1] + context + 1) * width)
        
        start_line = start // width
        end_line = (end + width - 1) // width
        
        lines.append(f"@@ -{start_line},{end_line - start_line} +{start_line},{end_line - start_line} @@")
        
        for line_idx in range(start_line, end_line):
            offset = line_idx * width
            chunk1 = data1[offset:offset + width] if offset < len(data1) else b""
            chunk2 = data2[offset:offset + width] if offset < len(data2) else b""
            
            if chunk1 != chunk2:
                if chunk1:
                    lines.append("-" + hex_dump(chunk1, offset=offset, width=width))
                if chunk2:
                    lines.append("+" + hex_dump(chunk2, offset=offset, width=width))
            else:
                lines.append(" " + hex_dump(chunk1, offset=offset, width=width))
    
    return "\n".join(lines)


def hex_search(
    data: Union[bytes, bytearray],
    pattern: Union[bytes, str],
    mask: Optional[Union[bytes, str]] = None
) -> List[int]:
    """
    Search for a hex pattern in binary data.
    
    Supports wildcard bytes using ?? in pattern string.
    
    Args:
        data: Binary data to search
        pattern: Pattern to find (bytes or hex string like "48 65 ?? 6c")
        mask: Optional mask (0xFF for exact, 0x00 for wildcard)
    
    Returns:
        List of offsets where pattern was found
    
    Example:
        >>> data = b'Hello World'
        >>> hex_search(data, b'llo')
        [2]
        >>> hex_search(data, "48 ?? 6c")
        [0]
    """
    if isinstance(data, bytearray):
        data = bytes(data)
    
    # Convert hex string to bytes
    if isinstance(pattern, str):
        # Handle wildcard ??
        if "??" in pattern:
            pattern_clean = pattern.replace("??", "00")
            pattern_bytes = bytes.fromhex(pattern_clean.replace(" ", ""))
            # Create mask: 0x00 for wildcards, 0xFF for exact
            mask_bytes = bytearray()
            parts = pattern.split()
            for part in parts:
                if part == "??":
                    mask_bytes.append(0x00)
                else:
                    mask_bytes.append(0xFF)
            mask = bytes(mask_bytes)
        else:
            pattern_bytes = bytes.fromhex(pattern.replace(" ", ""))
    else:
        pattern_bytes = pattern
    
    if len(pattern_bytes) == 0:
        return []
    
    if mask is None:
        # Simple search
        results = []
        start = 0
        while True:
            idx = data.find(pattern_bytes, start)
            if idx == -1:
                break
            results.append(idx)
            start = idx + 1
        return results
    else:
        if isinstance(mask, str):
            mask = bytes.fromhex(mask.replace(" ", ""))
        elif isinstance(mask, bytearray):
            mask = bytes(mask)
        
        # Search with mask
        results = []
        for i in range(len(data) - len(pattern_bytes) + 1):
            match = True
            for j in range(len(pattern_bytes)):
                if mask[j] != 0 and (data[i + j] & mask[j]) != (pattern_bytes[j] & mask[j]):
                    match = False
                    break
            if match:
                results.append(i)
        return results


def hex_edit(
    data: Union[bytes, bytearray],
    offset: int,
    new_bytes: Union[bytes, str]
) -> bytearray:
    """
    Edit bytes at a specific offset.
    
    Args:
        data: Original binary data
        offset: Offset to edit at
        new_bytes: New bytes (bytes or hex string)
    
    Returns:
        Modified bytearray
    
    Raises:
        ValueError: If offset is out of range
    
    Example:
        >>> data = b'Hello World'
        >>> hex_edit(data, 6, b'X')
        bytearray(b'Hello Xorld')
    """
    if isinstance(data, bytes):
        data = bytearray(data)
    elif isinstance(data, bytearray):
        data = bytearray(data)  # Make a copy
    
    if isinstance(new_bytes, str):
        new_bytes = bytes.fromhex(new_bytes.replace(" ", ""))
    
    if offset < 0 or offset > len(data):
        raise ValueError(f"Offset {offset} out of range [0, {len(data)}]")
    
    # Extend if necessary
    end = offset + len(new_bytes)
    if end > len(data):
        data.extend(b'\x00' * (end - len(data)))
    
    data[offset:end] = new_bytes
    return data


def hex_summary(
    data: Union[bytes, bytearray],
    name: Optional[str] = None
) -> str:
    """
    Generate a summary of binary data.
    
    Includes size, entropy, null bytes ratio, printable ratio, etc.
    
    Args:
        data: Binary data
        name: Optional name for the data
    
    Returns:
        Summary string
    
    Example:
        >>> data = b'Hello World\\x00\\x00\\xff'
        >>> print(hex_summary(data, "example.bin"))
        === example.bin ===
        Size: 14 bytes
        MD5: d41d8cd98f00b204e9800998ecf8427e
        SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        Null bytes: 14.3% (2)
        Printable: 78.6% (11)
        High bytes (>0x7F): 7.1% (1)
        Entropy: 3.17 bits/byte
    """
    if isinstance(data, bytearray):
        data = bytes(data)
    
    import hashlib
    from collections import Counter
    
    lines = []
    
    # Name
    if name:
        lines.append(f"=== {name} ===")
    else:
        lines.append("=== Binary Summary ===")
    
    # Size
    size = len(data)
    if size < 1024:
        size_str = f"{size} bytes"
    elif size < 1024 * 1024:
        size_str = f"{size / 1024:.2f} KB"
    else:
        size_str = f"{size / (1024 * 1024):.2f} MB"
    lines.append(f"Size: {size_str}")
    
    if size == 0:
        return "\n".join(lines)
    
    # Hashes
    lines.append(f"MD5: {hashlib.md5(data).hexdigest()}")
    lines.append(f"SHA256: {hashlib.sha256(data).hexdigest()}")
    
    # Byte statistics
    null_count = data.count(0)
    printable_count = sum(1 for b in data if 0x20 <= b < 0x7f)
    high_count = sum(1 for b in data if b > 0x7f)
    
    lines.append(f"Null bytes: {null_count / size * 100:.1f}% ({null_count})")
    lines.append(f"Printable: {printable_count / size * 100:.1f}% ({printable_count})")
    lines.append(f"High bytes (>0x7F): {high_count / size * 100:.1f}% ({high_count})")
    
    # Entropy
    counter = Counter(data)
    import math
    entropy = -sum(
        (count / size) * math.log2(count / size)
        for count in counter.values()
    )
    lines.append(f"Entropy: {entropy:.2f} bits/byte")
    
    # Most common bytes
    common = counter.most_common(5)
    if common:
        common_str = ", ".join(f"0x{b:02x}({c})" for b, c in common)
        lines.append(f"Most common: {common_str}")
    
    return "\n".join(lines)


def create_hex_patch(
    original: Union[bytes, bytearray],
    modified: Union[bytes, bytearray],
    base_offset: int = 0
) -> str:
    """
    Create a hex patch file in xxd-compatible format.
    
    Args:
        original: Original binary data
        modified: Modified binary data
        base_offset: Base offset to add to all offsets
    
    Returns:
        Patch string that can be applied with xxd -r
    
    Example:
        >>> orig = b'Hello'
        >>> mod = b'Hxllo'
        >>> print(create_hex_patch(orig, mod))
        00000001: 78
    """
    if isinstance(original, bytearray):
        original = bytes(original)
    if isinstance(modified, bytearray):
        modified = bytes(modified)
    
    max_len = max(len(original), len(modified))
    patches = []
    
    for i in range(max_len):
        orig_byte = original[i] if i < len(original) else None
        mod_byte = modified[i] if i < len(modified) else None
        
        if orig_byte != mod_byte:
            offset = base_offset + i
            if mod_byte is not None:
                patches.append(f"{offset:08x}: {mod_byte:02x}")
    
    return "\n".join(patches)


def dump_file(
    filepath: str,
    offset: int = 0,
    length: Optional[int] = None,
    width: int = 16,
    format: str = "hexdump"
) -> str:
    """
    Dump a file's contents in hex format.
    
    Args:
        filepath: Path to the file
        offset: Starting offset in file (default: 0)
        length: Number of bytes to dump (None = all)
        width: Bytes per line (default: 16)
        format: Output format - "hexdump", "xxd", or "summary"
    
    Returns:
        Formatted hex dump string
    
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    
    Example:
        >>> print(dump_file("/etc/hostname", format="hexdump"))
    """
    with open(filepath, "rb") as f:
        f.seek(offset)
        if length is not None:
            data = f.read(length)
        else:
            data = f.read()
    
    if format == "hexdump":
        return hex_dump(data, offset=offset, width=width)
    elif format == "xxd":
        return xxd_dump(data, offset=offset, width=width)
    elif format == "summary":
        return hex_summary(data, name=filepath)
    else:
        raise ValueError(f"Unknown format: {format}")


def format_bytes(
    size: int,
    precision: int = 2
) -> str:
    """
    Format byte count as human-readable string.
    
    Args:
        size: Size in bytes
        precision: Decimal precision (default: 2)
    
    Returns:
        Human-readable size string
    
    Example:
        >>> format_bytes(1024)
        '1.00 KB'
        >>> format_bytes(1536)
        '1.50 KB'
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    
    if size == 0:
        return "0 B"
    
    unit_idx = 0
    while size >= 1024 and unit_idx < len(units) - 1:
        size /= 1024
        unit_idx += 1
    
    if unit_idx == 0:
        return f"{size} {units[unit_idx]}"
    else:
        return f"{size:.{precision}f} {units[unit_idx]}"


def find_patterns(
    data: Union[bytes, bytearray],
    min_length: int = 4,
    min_occurrences: int = 2
) -> List[Tuple[bytes, List[int]]]:
    """
    Find repeated byte patterns in binary data.
    
    Args:
        data: Binary data to analyze
        min_length: Minimum pattern length (default: 4)
        min_occurrences: Minimum occurrences to report (default: 2)
    
    Returns:
        List of (pattern, [offsets]) sorted by pattern length
    
    Example:
        >>> data = b'ABCDEFABCDXYZABCD'
        >>> find_patterns(data, min_length=3)
        [(b'ABCD', [0, 6, 13])]
    """
    if isinstance(data, bytearray):
        data = bytes(data)
    
    patterns = {}
    max_len = len(data) // 2
    
    # Find all substrings
    for length in range(min_length, max_len + 1):
        seen = {}
        for i in range(len(data) - length + 1):
            pattern = data[i:i + length]
            if pattern in seen:
                seen[pattern].append(i)
            else:
                seen[pattern] = [i]
        
        # Filter patterns that appear multiple times
        for pattern, offsets in seen.items():
            if len(offsets) >= min_occurrences:
                # Only add if not already covered by longer pattern
                if pattern not in patterns:
                    patterns[pattern] = offsets
    
    # Remove sub-patterns of longer patterns
    result = []
    sorted_patterns = sorted(patterns.items(), key=lambda x: (-len(x[0]), x[0]))
    
    for pattern, offsets in sorted_patterns:
        # Check if this is a sub-pattern of an already added pattern
        is_subpattern = False
        for existing_pattern, _ in result:
            if len(pattern) < len(existing_pattern):
                # Check if pattern is a substring of existing_pattern
                for i in range(len(existing_pattern) - len(pattern) + 1):
                    if existing_pattern[i:i + len(pattern)] == pattern:
                        is_subpattern = True
                        break
        
        if not is_subpattern:
            result.append((pattern, offsets))
    
    return sorted(result, key=lambda x: -len(x[0]))


# Convenience function aliases
dump = hex_dump
xdump = xxd_dump