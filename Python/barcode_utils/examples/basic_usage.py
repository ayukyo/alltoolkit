#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Barcode Utils Examples

Basic usage examples for barcode generation.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    generate_code39, generate_code128, generate_ean13,
    generate_ean8, generate_upca, generate_itf, generate_matrix,
    generate_barcode, save_barcode, BarcodeConfig, get_supported_formats
)


def example_basic_code128():
    """Basic Code 128 example."""
    print("=" * 50)
    print("Example 1: Basic Code 128")
    print("=" * 50)
    
    result = generate_code128("Hello World")
    print(f"Data: {result.data}")
    print(f"Format: {result.format}")
    print(f"Size: {result.width}x{result.height}")
    print(f"SVG length: {len(result.svg)} chars")
    
    save_barcode(result, "examples/code128_basic.svg")
    print("Saved to: examples/code128_basic.svg\n")


def example_custom_config():
    """Custom configuration example."""
    print("=" * 50)
    print("Example 2: Custom Configuration")
    print("=" * 50)
    
    config = BarcodeConfig(
        width=3,
        height=120,
        margin=15,
        foreground="#0066CC",
        background="#F0F0F0",
        text_size=16
    )
    
    result = generate_code128("CUSTOM-STYLE", config)
    save_barcode(result, "examples/code128_custom.svg")
    print(f"Custom style barcode saved to: examples/code128_custom.svg\n")


def example_ean13():
    """EAN-13 product barcode example."""
    print("=" * 50)
    print("Example 3: EAN-13 Product Barcode")
    print("=" * 50)
    
    # Common country prefixes:
    # 00-09: USA/Canada
    # 30-37: France
    # 400-440: Germany
    # 45-49: Japan
    # 690-695: China
    # 590: Poland
    
    result = generate_ean13("590123412345")  # Polish product
    print(f"Data: {result.data}")
    print(f"Format: {result.format}")
    
    save_barcode(result, "examples/ean13_product.svg")
    print("Saved to: examples/ean13_product.svg\n")


def example_multiple_formats():
    """Generate multiple barcode formats."""
    print("=" * 50)
    print("Example 4: Multiple Formats")
    print("=" * 50)
    
    formats_data = {
        'code39': 'ABC-123',
        'code128': 'Universal-128',
        'ean13': '590123412345',
        'ean8': '1234567',
        'upca': '01234567890',
        'itf': '12345678',
    }
    
    for fmt, data in formats_data.items():
        result = generate_barcode(data, format=fmt)
        filename = f"examples/{fmt}_example.svg"
        save_barcode(result, filename)
        print(f"  {fmt}: {filename}")
    
    print()


def example_batch_generation():
    """Batch barcode generation."""
    print("=" * 50)
    print("Example 5: Batch Generation")
    print("=" * 50)
    
    products = [
        ("PROD-001", "Product Alpha"),
        ("PROD-002", "Product Beta"),
        ("PROD-003", "Product Gamma"),
    ]
    
    for sku, name in products:
        result = generate_code128(f"{sku}-{name}")
        filename = f"examples/batch_{sku}.svg"
        save_barcode(result, filename)
        print(f"  Generated: {filename}")
    
    print()


def example_print_ready():
    """High-resolution print-ready barcode."""
    print("=" * 50)
    print("Example 6: Print-Ready Barcode")
    print("=" * 50)
    
    config = BarcodeConfig(
        width=4,
        height=150,
        margin=20,
        scale=2.0,
        text_size=18,
        foreground="#000000",
        background="#FFFFFF"
    )
    
    result = generate_code128("PRINT-2024-XYZ", config)
    save_barcode(result, "examples/print_ready.svg")
    print(f"High-res barcode: {result.width}x{result.height}")
    print("Saved to: examples/print_ready.svg\n")


def example_no_text():
    """Barcode without text label."""
    print("=" * 50)
    print("Example 7: No Text Label")
    print("=" * 50)
    
    config = BarcodeConfig(show_text=False)
    result = generate_code128("HIDDEN-TEXT", config)
    save_barcode(result, "examples/no_text.svg")
    print("Barcode without text saved to: examples/no_text.svg\n")


def example_matrix_code():
    """Matrix code example."""
    print("=" * 50)
    print("Example 8: Matrix Code")
    print("=" * 50)
    
    result = generate_matrix("https://example.com/product/123", size=25)
    save_barcode(result, "examples/matrix_code.svg")
    print(f"Matrix code: {result.width}x{result.height}")
    print("Saved to: examples/matrix_code.svg\n")


def example_color_themes():
    """Different color themes."""
    print("=" * 50)
    print("Example 9: Color Themes")
    print("=" * 50)
    
    themes = [
        ("classic", "#000000", "#FFFFFF"),
        ("blue", "#0066CC", "#FFFFFF"),
        ("green", "#006600", "#FFFFFF"),
        ("red", "#CC0000", "#FFFFFF"),
        ("dark", "#FFFFFF", "#000000"),
    ]
    
    for name, fg, bg in themes:
        config = BarcodeConfig(foreground=fg, background=bg)
        result = generate_code128("THEME", config)
        save_barcode(result, f"examples/theme_{name}.svg")
        print(f"  {name}: examples/theme_{name}.svg")
    
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 50)
    print("AllToolkit Barcode Utils - Examples")
    print("=" * 50)
    print(f"Supported formats: {get_supported_formats()}\n")
    
    # Ensure examples directory exists
    os.makedirs("examples", exist_ok=True)
    
    # Run examples
    example_basic_code128()
    example_custom_config()
    example_ean13()
    example_multiple_formats()
    example_batch_generation()
    example_print_ready()
    example_no_text()
    example_matrix_code()
    example_color_themes()
    
    print("=" * 50)
    print("All examples completed!")
    print("=" * 50)


if __name__ == '__main__':
    main()
