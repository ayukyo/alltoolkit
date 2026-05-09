"""
Hex Dump Utils - Usage Examples

Demonstrates various ways to use the hex_dump_utils module for:
- Displaying binary data in hex format
- Parsing hex dumps back to bytes
- Searching and editing binary data
- Creating diffs and patches
- Analyzing binary files
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    hex_dump, xxd_dump, hex_dump_to_bytes, binary_diff,
    hex_search, hex_edit, hex_summary, create_hex_patch,
    dump_file, format_bytes, find_patterns
)


def example_basic_hex_dump():
    """Example 1: Basic hex dump."""
    print("=" * 60)
    print("Example 1: Basic Hex Dump")
    print("=" * 60)
    
    data = b'Hello, World!\x00\xff\xfe\xab\xcd\xef'
    
    print("\nOriginal data:")
    print(f"  Bytes: {data}")
    print(f"  Length: {len(data)} bytes")
    
    print("\nDefault hex dump:")
    print(hex_dump(data))
    
    print("\nWithout ASCII:")
    print(hex_dump(data, show_ascii=False))
    
    print("\nWithout offset:")
    print(hex_dump(data, show_offset=False))
    
    print("\nWith uppercase hex:")
    print(hex_dump(data, uppercase=True))


def example_xxd_format():
    """Example 2: xxd-compatible output."""
    print("\n" + "=" * 60)
    print("Example 2: xxd-Compatible Output")
    print("=" * 60)
    
    data = b'This is a test string for xxd format output.'
    
    print("\nxxd format:")
    print(xxd_dump(data))
    
    print("\nxxd with uppercase:")
    print(xxd_dump(data, uppercase=True))
    
    print("\nxxd with offset starting at 0x100:")
    print(xxd_dump(data, offset=0x100))


def example_custom_width():
    """Example 3: Custom width and grouping."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Width and Grouping")
    print("=" * 60)
    
    data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    print("\nWidth 8 bytes per line:")
    print(hex_dump(data, width=8))
    
    print("\nWidth 32 bytes per line:")
    print(hex_dump(data, width=32))
    
    print("\nGroup size 4 bytes:")
    print(hex_dump(data, width=16, group_size=4))


def example_parse_hex():
    """Example 4: Parsing hex dump back to bytes."""
    print("\n" + "=" * 60)
    print("Example 4: Parsing Hex Dump Back to Bytes")
    print("=" * 60)
    
    # From hex dump output
    hexdump_output = """
    00000000  48 65 6c 6c 6f 2c 20 57  6f 72 6c 64 21 00 ff fe  |Hello, World!...|
    """
    
    print("\nParsing hexdump output:")
    print(hexdump_output.strip())
    result = hex_dump_to_bytes(hexdump_output)
    print(f"\nRecovered bytes: {result}")
    print(f"As string: {result.decode('ascii', errors='replace')}")
    
    # From xxd output
    xxd_output = "00000000: 4865 6c6c 6f                            Hello"
    
    print("\nParsing xxd output:")
    print(xxd_output)
    result = hex_dump_to_bytes(xxd_output)
    print(f"Recovered: {result}")
    
    # From plain hex string
    plain_hex = "48 65 6c 6c 6f 20 57 6f 72 6c 64"
    
    print("\nParsing plain hex:")
    print(f"  Input: {plain_hex}")
    result = hex_dump_to_bytes(plain_hex)
    print(f"  Result: {result}")


def example_hex_search():
    """Example 5: Searching in binary data."""
    print("\n" + "=" * 60)
    print("Example 5: Searching in Binary Data")
    print("=" * 60)
    
    data = b'Hello World! Hello Universe! Hello Galaxy!'
    
    print(f"\nData: {data}")
    print(f"Length: {len(data)} bytes")
    
    # Simple search
    pattern = b'Hello'
    positions = hex_search(data, pattern)
    print(f"\nSearching for '{pattern.decode()}':")
    print(f"  Found at offsets: {positions}")
    
    # Hex string search
    pattern_hex = "48 65 6c 6c"  # 'Hell'
    positions = hex_search(data, pattern_hex)
    print(f"\nSearching for hex pattern '{pattern_hex}':")
    print(f"  Found at offsets: {positions}")
    
    # Wildcard search
    wildcard_pattern = "48 ?? 6c 6c"  # 'H?ll'
    positions = hex_search(data, wildcard_pattern)
    print(f"\nSearching with wildcard '48 ?? 6c 6c':")
    print(f"  Found at offsets: {positions}")


def example_hex_edit():
    """Example 6: Editing binary data."""
    print("\n" + "=" * 60)
    print("Example 6: Editing Binary Data")
    print("=" * 60)
    
    original = b'Hello World!'
    
    print(f"\nOriginal: {original}")
    
    # Edit single byte
    edited = hex_edit(original, 6, b'X')
    print(f"\nEdit at offset 6, replace with 'X':")
    print(f"  Result: {bytes(edited)}")
    
    # Edit multiple bytes
    edited = hex_edit(original, 0, b'Goodbye')
    print(f"\nEdit at offset 0, replace with 'Goodbye':")
    print(f"  Result: {bytes(edited)}")
    
    # Edit with hex string
    edited = hex_edit(original, 7, '4f 4f')  # 'OO'
    print(f"\nEdit at offset 7 with hex '4f 4f':")
    print(f"  Result: {bytes(edited)}")


def example_binary_diff():
    """Example 7: Comparing binary data."""
    print("\n" + "=" * 60)
    print("Example 7: Comparing Binary Data")
    print("=" * 60)
    
    original = b'Hello World! This is original data.'
    modified = b'Hello Xorld! This is modified data.'
    
    print(f"\nOriginal: {original}")
    print(f"Modified: {modified}")
    
    print("\nDiff:")
    print(binary_diff(original, modified))
    
    # Different sizes
    short = b'Hello'
    long = b'Hello World'
    
    print("\n" + "-" * 40)
    print(f"Comparing different sizes:")
    print(f"  Data1: {short}")
    print(f"  Data2: {long}")
    print("\nDiff:")
    print(binary_diff(short, long))


def example_hex_summary():
    """Example 8: Binary data summary."""
    print("\n" + "=" * 60)
    print("Example 8: Binary Data Summary")
    print("=" * 60)
    
    data = b'Hello World!\x00\x00\xff\xfe\xab\xcd\xef\x01\x02\x03'
    
    print("\nData summary:")
    print(hex_summary(data, name='sample.bin'))
    
    # Mostly null bytes
    null_data = b'\x00' * 100 + b'\xff\xff\xff'
    
    print("\n" + "-" * 40)
    print("\nNull-heavy data summary:")
    print(hex_summary(null_data, name='nulls.bin'))
    
    # Random-like data
    import random
    random.seed(42)
    random_data = bytes([random.randint(0, 255) for _ in range(1000)])
    
    print("\n" + "-" * 40)
    print("\nHigh-entropy data summary:")
    print(hex_summary(random_data, name='random.bin'))


def example_create_patch():
    """Example 9: Creating hex patches."""
    print("\n" + "=" * 60)
    print("Example 9: Creating Hex Patches")
    print("=" * 60)
    
    original = b'Original binary data for patching'
    modified = b'Original xinary data for matching'
    
    print(f"\nOriginal: {original}")
    print(f"Modified: {modified}")
    
    print("\nPatch (xxd -r format):")
    patch = create_hex_patch(original, modified)
    print(patch)
    
    # Apply patch simulation
    print("\nVerifying patch offsets:")
    for line in patch.split('\n'):
        if line:
            offset_hex, byte_hex = line.split(':')
            offset = int(offset_hex, 16)
            byte_val = int(byte_hex.strip(), 16)
            print(f"  Offset {offset} ({offset_hex}): byte changed to {byte_hex} ('{chr(byte_val) if 32 <= byte_val < 127 else '.'}')")


def example_format_bytes():
    """Example 10: Human-readable byte formatting."""
    print("\n" + "=" * 60)
    print("Example 10: Human-Readable Byte Formatting")
    print("=" * 60)
    
    sizes = [0, 100, 1024, 1500, 1024*1024, 5*1024*1024, 
             1024*1024*1024, 2.5*1024*1024*1024]
    
    print("\nFormatting various sizes:")
    for size in sizes:
        formatted = format_bytes(int(size))
        print(f"  {int(size):>15} bytes = {formatted}")
    
    print("\nWith different precision:")
    size = 1234567
    for precision in range(4):
        print(f"  Precision {precision}: {format_bytes(size, precision=precision)}")


def example_find_patterns():
    """Example 11: Finding repeated patterns."""
    print("\n" + "=" * 60)
    print("Example 11: Finding Repeated Patterns")
    print("=" * 60)
    
    data = b'HEADERdataHEADERmoreHEADERend'
    
    print(f"\nData: {data}")
    
    patterns = find_patterns(data, min_length=4)
    
    print("\nFound patterns:")
    for pattern, offsets in patterns:
        try:
            pattern_str = pattern.decode('ascii')
        except:
            pattern_str = pattern.hex()
        print(f"  '{pattern_str}' at offsets: {offsets}")
    
    # More complex data
    complex_data = b'ABCDEFABCDEFXYZABCDEFABCDEF123ABCDEF'
    
    print("\n" + "-" * 40)
    print(f"\nComplex data: {complex_data}")
    
    patterns = find_patterns(complex_data, min_length=4)
    
    print("\nFound patterns:")
    for pattern, offsets in patterns:
        try:
            pattern_str = pattern.decode('ascii')
        except:
            pattern_str = pattern.hex()
        print(f"  '{pattern_str}' (len={len(pattern)}) at offsets: {offsets}")


def example_colorized_output():
    """Example 12: Colorized hex dump (requires terminal)."""
    print("\n" + "=" * 60)
    print("Example 12: Colorized Hex Dump")
    print("=" * 60)
    
    data = b'Text\x00Null\xfe\xabHigh bytes\x7fDEL'
    
    print("\nNormal output:")
    print(hex_dump(data))
    
    print("\nColorized output (ANSI colors):")
    print(hex_dump(data, colorize=True))
    
    print("\nNote: Colors are visible in terminal:")
    print("  Cyan: Offset")
    print("  Green: Printable bytes")
    print("  Dark gray: Null bytes (0x00)")
    print("  Red dots: Non-printable bytes in ASCII")


def example_full_workflow():
    """Example 13: Complete workflow."""
    print("\n" + "=" * 60)
    print("Example 13: Complete Analysis Workflow")
    print("=" * 60)
    
    # Simulate a binary file with some structure
    header = b'MAGIC\x00\x01\x02'  # Magic header
    version = b'\x01\x00'          # Version 1.0
    payload = b'Hello World Data ' * 5
    footer = b'END\x00\xff'
    
    file_data = header + version + payload + footer
    
    print(f"\nSimulated file ({len(file_data)} bytes):")
    
    # Summary
    print("\n--- File Summary ---")
    print(hex_summary(file_data, name='structured.bin'))
    
    # Dump with offset starting at header
    print("\n--- Header Section (offset 0-8) ---")
    print(hex_dump(file_data[:8]))
    
    # Search for patterns
    print("\n--- Pattern Analysis ---")
    patterns = find_patterns(file_data, min_length=5)
    for pattern, offsets in patterns:
        try:
            pattern_str = pattern.decode('ascii', errors='replace')
        except:
            pattern_str = pattern.hex()
        print(f"  Found '{pattern_str}' {len(offsets)} times")
    
    # Edit and create patch
    print("\n--- Modification Example ---")
    modified = hex_edit(file_data, 5, b'\x10\x20')
    patch = create_hex_patch(file_data, bytes(modified))
    print(f"Patch for modification:")
    print(patch)
    
    # Diff
    print("\n--- Diff View ---")
    diff = binary_diff(file_data[:20], bytes(modified)[:20])
    print(diff)


def main():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# Hex Dump Utils - Usage Examples")
    print("#" * 60)
    
    example_basic_hex_dump()
    example_xxd_format()
    example_custom_width()
    example_parse_hex()
    example_hex_search()
    example_hex_edit()
    example_binary_diff()
    example_hex_summary()
    example_create_patch()
    example_format_bytes()
    example_find_patterns()
    example_colorized_output()
    example_full_workflow()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()