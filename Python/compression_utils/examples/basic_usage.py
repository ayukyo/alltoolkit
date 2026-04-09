#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compression Utils - Basic Usage Examples

Demonstrates common compression operations.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path (compression_utils folder)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    create_zip, extract_zip, list_zip_contents,
    gzip_compress, gzip_decompress,
    bz2_compress, bz2_decompress,
    lzma_compress, lzma_decompress,
    create_tar, extract_tar, list_tar_contents,
    format_size, get_compression_ratio, compare_compression_methods,
)


def demo_zip_operations():
    """Demonstrate ZIP operations."""
    print("\n" + "="*60)
    print("ZIP Operations Demo")
    print("="*60)
    
    # Create some test files
    test_dir = Path("demo_temp")
    test_dir.mkdir(exist_ok=True)
    
    (test_dir / "file1.txt").write_text("Hello, World! " * 100)
    (test_dir / "file2.txt").write_text("Another file with content. " * 50)
    
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "nested.txt").write_text("Nested file content. " * 30)
    
    # Create ZIP archive
    print("\n1. Creating ZIP archive...")
    result = create_zip(
        test_dir / "archive.zip",
        [test_dir / "file1.txt", test_dir / "file2.txt", sub_dir],
        compression='deflate',
        compression_level=6,
    )
    print(f"   Files: {result['files']}")
    print(f"   Original size: {format_size(result['original_size'])}")
    print(f"   Compressed size: {format_size(result['compressed_size'])}")
    print(f"   Compression ratio: {result['ratio']}")
    
    # List contents
    print("\n2. Listing ZIP contents...")
    contents = list_zip_contents(test_dir / "archive.zip")
    for item in contents:
        print(f"   - {item['name']}: {format_size(item['size'])}")
    
    # Extract
    print("\n3. Extracting ZIP...")
    extract_dir = test_dir / "extracted"
    extracted = extract_zip(test_dir / "archive.zip", extract_dir)
    print(f"   Extracted {len(extracted)} files to {extract_dir}")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    print("\n   Cleanup complete.")


def demo_gzip_operations():
    """Demonstrate GZIP operations."""
    print("\n" + "="*60)
    print("GZIP Operations Demo")
    print("="*60)
    
    # Create test file
    test_file = Path("demo_temp.txt")
    test_file.write_text("GZIP test content. " * 500)
    original_size = test_file.stat().st_size
    
    print(f"\n1. Original file: {format_size(original_size)}")
    
    # Compress
    print("\n2. Compressing with GZIP...")
    gz_path = gzip_compress(test_file, keep_original=True)
    gz_size = Path(gz_path).stat().st_size
    print(f"   Compressed to: {format_size(gz_size)}")
    print(f"   Ratio: {get_compression_ratio(original_size, gz_size)}")
    
    # Decompress
    print("\n3. Decompressing...")
    decompressed = gzip_decompress(gz_path, keep_original=False)
    print(f"   Decompressed to: {decompressed}")
    
    # Verify
    original_content = "GZIP test content. " * 500
    decompressed_content = Path(decompressed).read_text()
    match = original_content == decompressed_content
    print(f"   Content verified: {'✓' if match else '✗'}")
    
    # Cleanup
    Path(decompressed).unlink()
    print("\n   Cleanup complete.")


def demo_tar_operations():
    """Demonstrate TAR operations."""
    print("\n" + "="*60)
    print("TAR Operations Demo")
    print("="*60)
    
    # Create test directory
    test_dir = Path("demo_tar")
    test_dir.mkdir(exist_ok=True)
    
    for i in range(5):
        (test_dir / f"file{i}.txt").write_text(f"File {i} content. " * 100)
    
    # Create different TAR formats
    print("\n1. Creating TAR archives with different compression...")
    
    formats = [
        ('archive.tar', None),
        ('archive.tar.gz', 'gz'),
        ('archive.tar.bz2', 'bz2'),
        ('archive.tar.xz', 'xz'),
    ]
    
    sizes = {}
    for filename, compression in formats:
        result = create_tar(test_dir / filename, list(test_dir.glob("*.txt")), compression=compression)
        sizes[filename] = result['size']
        print(f"   {filename}: {format_size(result['size'])}")
    
    # Find best compression
    best = min(sizes.items(), key=lambda x: x[1])
    print(f"\n   Best compression: {best[0]} ({format_size(best[1])})")
    
    # List contents
    print("\n2. Listing TAR.GZ contents...")
    contents = list_tar_contents(test_dir / "archive.tar.gz")
    for item in contents[:3]:  # Show first 3
        print(f"   - {item['name']}: {format_size(item['size'])}")
    
    # Extract
    print("\n3. Extracting TAR.GZ...")
    extract_dir = test_dir / "extracted"
    extracted = extract_tar(test_dir / "archive.tar.gz", extract_dir)
    print(f"   Extracted {len(extracted)} files")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    print("\n   Cleanup complete.")


def demo_comparison():
    """Compare different compression methods."""
    print("\n" + "="*60)
    print("Compression Method Comparison")
    print("="*60)
    
    # Create test file with repetitive content (compresses well)
    test_file = Path("demo_compare.txt")
    test_file.write_text("This is repetitive content for compression testing. " * 1000)
    
    # compare_compression_methods is already imported at the top
    
    print("\nComparing compression methods on test file...")
    results = compare_compression_methods(test_file)
    
    print(f"\nOriginal: {results['original']['size_formatted']}")
    print("\nCompressed sizes:")
    for method in ['gzip', 'bz2', 'lzma']:
        r = results[method]
        print(f"   {method.upper():6}: {r['size_formatted']:>10} ({r['ratio']:>6} reduction)")
    
    # Cleanup
    test_file.unlink()
    print("\n   Cleanup complete.")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("Compression Utils - Basic Usage Examples")
    print("="*60)
    
    demo_zip_operations()
    demo_gzip_operations()
    demo_tar_operations()
    demo_comparison()
    
    print("\n" + "="*60)
    print("All demos completed!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
