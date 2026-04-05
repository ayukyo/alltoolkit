"""
AllToolkit - Python QR Code Utilities Examples

Demonstrates various use cases for the QR Code generation module.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from qr_code_utils.mod import (
    QRCodeUtils, QRCode, ErrorCorrectionLevel, QRMode,
    encode, validate, get_capacity
)


def example_1_basic_encoding():
    """Example 1: Basic QR Code encoding and display."""
    print("=" * 60)
    print("Example 1: Basic QR Code Encoding")
    print("=" * 60)
    
    # Encode a simple message
    qr = QRCodeUtils.encode("Hello, World!")
    
    print("\nData: Hello, World!")
    print(f"Version: {qr.version}")
    print(f"Size: {qr.size}x{qr.size} modules")
    print(f"Error Correction: {qr.ec_level.name}")
    print(f"Mode: {qr.mode.name}")
    
    print("\nQR Code (ASCII):")
    print(qr.to_ascii())


def example_2_different_data_types():
    """Example 2: Encoding different types of data."""
    print("\n" + "=" * 60)
    print("Example 2: Different Data Types")
    print("=" * 60)
    
    # Numeric data
    print("\n1. Numeric Data:")
    qr_num = QRCodeUtils.encode("1234567890")
    print(f"   Data: 1234567890")
    print(f"   Mode: {qr_num.mode.name}")
    print(qr_num.to_compact_ascii())
    
    # Alphanumeric data
    print("\n2. Alphanumeric Data:")
    qr_alpha = QRCodeUtils.encode("HTTPS://EXAMPLE.COM")
    print(f"   Data: HTTPS://EXAMPLE.COM")
    print(f"   Mode: {qr_alpha.mode.name}")
    print(qr_alpha.to_compact_ascii())
    
    # Binary/Byte data
    print("\n3. Binary Data (with special characters):")
    qr_byte = QRCodeUtils.encode("Hello! 你好世界 🌍")
    print(f"   Data: Hello! 你好世界 🌍")
    print(f"   Mode: {qr_byte.mode.name}")
    print(qr_byte.to_compact_ascii())


def example_3_error_correction_levels():
    """Example 3: Different error correction levels."""
    print("\n" + "=" * 60)
    print("Example 3: Error Correction Levels")
    print("=" * 60)
    
    data = "Test Data"
    
    for ec in [ErrorCorrectionLevel.L, ErrorCorrectionLevel.M, 
               ErrorCorrectionLevel.Q, ErrorCorrectionLevel.H]:
        qr = QRCodeUtils.encode(data, ec_level=ec)
        print(f"\n{ec.name} Level (~{[7, 15, 25, 30][ec]}% recovery):")
        print(f"  Version: {qr.version}")
        print(f"  Capacity: {get_capacity(qr.version, ec)} bytes")
        print(qr.to_compact_ascii())


def example_4_svg_generation():
    """Example 4: Generate SVG for web use."""
    print("\n" + "=" * 60)
    print("Example 4: SVG Generation")
    print("=" * 60)
    
    qr = QRCodeUtils.encode("https://github.com/ayukyo/alltoolkit")
    svg = qr.to_svg(module_size=8)
    
    # Save to file
    output_path = "/tmp/alltoolkit_qr.svg"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    
    print(f"\nQR Code for: https://github.com/ayukyo/alltoolkit")
    print(f"SVG saved to: {output_path}")
    print(f"SVG size: {len(svg)} characters")
    print("\nFirst 500 characters of SVG:")
    print(svg[:500] + "...")


def example_5_wifi_qr_code():
    """Example 5: Create a WiFi connection QR Code."""
    print("\n" + "=" * 60)
    print("Example 5: WiFi Connection QR Code")
    print("=" * 60)
    
    # WiFi QR format: WIFI:S:<SSID>;T:<WPA|WEP|nopass>;P:<PASSWORD>;H:<true|false>;
    ssid = "MyHomeWiFi"
    password = "SecurePass123"
    wifi_string = f"WIFI:S:{ssid};T:WPA;P:{password};;"
    
    print(f"\nWiFi Network: {ssid}")
    print(f"Password: {password}")
    print("\nScan this QR code to connect:")
    
    qr = QRCodeUtils.encode(wifi_string)
    print(qr.to_ascii(border=2))


def example_6_vcard_qr_code():
    """Example 6: Create a vCard QR Code."""
    print("\n" + "=" * 60)
    print("Example 6: vCard QR Code")
    print("=" * 60)
    
    # Simple vCard format
    vcard = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
TEL:+1234567890
EMAIL:john@example.com
END:VCARD"""
    
    print("\nvCard Data:")
    print(vcard)
    print("\nQR Code:")
    
    qr = QRCodeUtils.encode(vcard)
    print(qr.to_compact_ascii())


def example_7_validation_and_info():
    """Example 7: Validate data and get QR info."""
    print("\n" + "=" * 60)
    print("Example 7: Validation and Information")
    print("=" * 60)
    
    # Test various data
    test_cases = [
        "Short text",
        "A" * 100,
        "A" * 501,  # Too long
        123,  # Invalid type
    ]
    
    print("\nValidation Tests:")
    for data in test_cases:
        result = validate(data)
        data_str = str(data)[:30] + "..." if len(str(data)) > 30 else str(data)
        print(f"  '{data_str}': {'✓ Valid' if result else '✗ Invalid'}")
    
    # Get QR info
    print("\nQR Code Information:")
    qr = QRCodeUtils.encode("https://example.com/page?id=123", 
                             version=3, 
                             ec_level=ErrorCorrectionLevel.M)
    info = qr.get_info()
    for key, value in info.items():
        print(f"  {key}: {value}")


def example_8_custom_styling():
    """Example 8: Custom ASCII styling."""
    print("\n" + "=" * 60)
    print("Example 8: Custom Styling")
    print("=" * 60)
    
    qr = QRCodeUtils.encode("Styled QR")
    
    print("\n1. Default styling:")
    print(qr.to_ascii())
    
    print("\n2. Custom characters (blocks):")
    print(qr.to_ascii(black='█', white='░'))
    
    print("\n3. Custom characters (braille):")
    print(qr.to_ascii(black='⣿', white='⠀'))


def example_9_save_to_file():
    """Example 9: Save QR Code to file."""
    print("\n" + "=" * 60)
    print("Example 9: Save to File")
    print("=" * 60)
    
    qr = QRCodeUtils.encode("Save me to a file!")
    
    # Save as ASCII
    ascii_path = "/tmp/qr_ascii.txt"
    qr.save_to_file(ascii_path, format='ascii')
    print(f"\nASCII QR saved to: {ascii_path}")
    
    # Save as SVG
    svg_path = "/tmp/qr_image.svg"
    qr.save_to_file(svg_path, format='svg')
    print(f"SVG QR saved to: {svg_path}")


def example_10_bitmap_access():
    """Example 10: Access raw bitmap data."""
    print("\n" + "=" * 60)
    print("Example 10: Raw Bitmap Access")
    print("=" * 60)
    
    qr = QRCodeUtils.encode("Bitmap")
    bitmap = qr.to_bitmap()
    
    print(f"\nQR Code size: {qr.size}x{qr.size}")
    print(f"Total modules: {qr.size * qr.size}")
    
    # Count black and white modules
    black_count = sum(sum(row) for row in bitmap)
    white_count = qr.size * qr.size - black_count
    
    print(f"Black modules: {black_count}")
    print(f"White modules: {white_count}")
    print(f"Fill ratio: {black_count / (qr.size * qr.size) * 100:.1f}%")
    
    # Print first few rows
    print("\nFirst 5 rows of bitmap:")
    for i, row in enumerate(bitmap[:5]):
        print(f"  Row {i}: {row[:10]}...")


def example_11_convenience_functions():
    """Example 11: Using convenience functions."""
    print("\n" + "=" * 60)
    print("Example 11: Convenience Functions")
    print("=" * 60)
    
    # Direct encode
    qr = encode("Convenience!")
    print(f"\nEncoded: {qr.data}")
    print(qr.to_compact_ascii())
    
    # Check capacity
    print("\nCapacity by version and error correction:")
    for version in [1, 2, 3]:
        for ec in [ErrorCorrectionLevel.L, ErrorCorrectionLevel.M]:
            cap = get_capacity(version, ec)
            print(f"  Version {version}, {ec.name}: {cap} bytes")


def main():
    """Run all examples."""
    examples = [
        example_1_basic_encoding,
        example_2_different_data_types,
        example_3_error_correction_levels,
        example_4_svg_generation,
        example_5_wifi_qr_code,
        example_6_vcard_qr_code,
        example_7_validation_and_info,
        example_8_custom_styling,
        example_9_save_to_file,
        example_10_bitmap_access,
        example_11_convenience_functions,
    ]
    
    print("\n" + "=" * 60)
    print("AllToolkit - Python QR Code Utilities Examples")
    print("=" * 60)
    
    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"\nError in example {i}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
