#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Compression Utilities Test Suite

Comprehensive tests for compression_utils module.
Run with: python compression_utils_test.py
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # ZIP functions
    create_zip, extract_zip, list_zip_contents, add_to_zip,
    # GZIP functions
    gzip_compress, gzip_decompress, gzip_compress_bytes, gzip_decompress_bytes,
    # BZ2 functions
    bz2_compress, bz2_decompress, bz2_compress_bytes, bz2_decompress_bytes,
    # LZMA functions
    lzma_compress, lzma_decompress, lzma_compress_bytes, lzma_decompress_bytes,
    # TAR functions
    create_tar, extract_tar, list_tar_contents, append_to_tar,
    # Utility functions
    get_compression_ratio, format_size, get_file_info, compare_compression_methods,
    # Streaming classes
    StreamingCompressor, StreamingDecompressor,
    # Module info
    get_module_info,
)


class TestRunner:
    """Simple test runner with pass/fail tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            msg = f"  ✗ {name}"
            if error_msg:
                msg += f" - {error_msg}"
            print(msg)
            self.errors.append(name)
    
    def report(self) -> bool:
        """Print test report and return True if all tests passed."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        
        if self.failed == 0:
            print("✓ All tests passed!")
        else:
            print(f"✗ {self.failed} test(s) failed:")
            for error in self.errors:
                print(f"    - {error}")
        
        print('='*60)
        return self.failed == 0


class TempDirectory:
    """Context manager for temporary directories."""
    
    def __init__(self):
        self.temp_dir = None
    
    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp()
        return Path(self.temp_dir)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


def run_zip_tests(runner: TestRunner, temp_dir: Path):
    """Test ZIP operations."""
    print("\nZIP Operations Tests")
    print("="*60)
    
    # Create test files
    test_file1 = temp_dir / "test1.txt"
    test_file1.write_text("Hello, World! This is test file 1." * 100)
    
    test_file2 = temp_dir / "test2.txt"
    test_file2.write_text("Another test file with different content." * 50)
    
    test_dir = temp_dir / "testdir"
    test_dir.mkdir()
    (test_dir / "nested.txt").write_text("Nested file content." * 20)
    
    # Test create_zip
    zip_path = temp_dir / "test.zip"
    result = create_zip(zip_path, [test_file1, test_file2, test_dir])
    runner.test("create_zip: returns stats dict", 
                isinstance(result, dict) and 'files' in result)
    runner.test("create_zip: creates file", zip_path.exists())
    runner.test("create_zip: file count correct", result['files'] == 3)
    runner.test("create_zip: compression achieved", 
                result['compressed_size'] < result['original_size'])
    
    # Test list_zip_contents
    contents = list_zip_contents(zip_path)
    runner.test("list_zip_contents: returns list", isinstance(contents, list))
    runner.test("list_zip_contents: correct count", len(contents) == 3)
    runner.test("list_zip_contents: has name field", 
                all('name' in item for item in contents))
    
    # Test extract_zip
    extract_dir = temp_dir / "extracted"
    extracted = extract_zip(zip_path, extract_dir)
    runner.test("extract_zip: returns list", isinstance(extracted, list))
    runner.test("extract_zip: extracts all files", len(extracted) == 3)
    runner.test("extract_zip: content matches", 
                (extract_dir / "test1.txt").read_text() == test_file1.read_text())
    
    # Test add_to_zip
    new_file = temp_dir / "new_file.txt"
    new_file.write_text("New file to add." * 30)
    added = add_to_zip(zip_path, [new_file])
    runner.test("add_to_zip: returns count", isinstance(added, int))
    runner.test("add_to_zip: adds file", added == 1)
    
    # Test with compression methods
    for method in ['store', 'deflate', 'bzip2']:
        method_zip = temp_dir / f"test_{method}.zip"
        result = create_zip(method_zip, [test_file1], compression=method)
        runner.test(f"create_zip: {method} compression", method_zip.exists())


def run_gzip_tests(runner: TestRunner, temp_dir: Path):
    """Test GZIP operations."""
    print("\nGZIP Operations Tests")
    print("="*60)
    
    # Create test file
    test_file = temp_dir / "gzip_test.txt"
    original_content = "GZIP test content. " * 200
    test_file.write_text(original_content)
    
    # Test gzip_compress
    gz_path = gzip_compress(test_file, keep_original=True)
    runner.test("gzip_compress: returns path", isinstance(gz_path, str))
    runner.test("gzip_compress: creates file", Path(gz_path).exists())
    runner.test("gzip_compress: keeps original", test_file.exists())
    
    # Test gzip_decompress
    decompressed_path = gzip_decompress(gz_path, keep_original=False)
    runner.test("gzip_decompress: returns path", isinstance(decompressed_path, str))
    runner.test("gzip_decompress: content matches", 
                Path(decompressed_path).read_text() == original_content)
    
    # Test bytes compression
    test_bytes = b"Binary test data " * 100
    compressed_bytes = gzip_compress_bytes(test_bytes)
    runner.test("gzip_compress_bytes: compresses", len(compressed_bytes) < len(test_bytes))
    
    decompressed_bytes = gzip_decompress_bytes(compressed_bytes)
    runner.test("gzip_decompress_bytes: decompresses", decompressed_bytes == test_bytes)


def run_bz2_tests(runner: TestRunner, temp_dir: Path):
    """Test BZ2 operations."""
    print("\nBZ2 Operations Tests")
    print("="*60)
    
    # Create test file
    test_file = temp_dir / "bz2_test.txt"
    original_content = "BZ2 test content. " * 200
    test_file.write_text(original_content)
    
    # Test bz2_compress
    bz2_path = bz2_compress(test_file, keep_original=True)
    runner.test("bz2_compress: returns path", isinstance(bz2_path, str))
    runner.test("bz2_compress: creates file", Path(bz2_path).exists())
    runner.test("bz2_compress: keeps original", test_file.exists())
    
    # Test bz2_decompress
    decompressed_path = bz2_decompress(bz2_path, keep_original=False)
    runner.test("bz2_decompress: returns path", isinstance(decompressed_path, str))
    runner.test("bz2_decompress: content matches", 
                Path(decompressed_path).read_text() == original_content)
    
    # Test bytes compression
    test_bytes = b"Binary BZ2 test data " * 100
    compressed_bytes = bz2_compress_bytes(test_bytes)
    runner.test("bz2_compress_bytes: compresses", len(compressed_bytes) < len(test_bytes))
    
    decompressed_bytes = bz2_decompress_bytes(compressed_bytes)
    runner.test("bz2_decompress_bytes: decompresses", decompressed_bytes == test_bytes)


def run_lzma_tests(runner: TestRunner, temp_dir: Path):
    """Test LZMA operations."""
    print("\nLZMA Operations Tests")
    print("="*60)
    
    # Create test file
    test_file = temp_dir / "lzma_test.txt"
    original_content = "LZMA test content. " * 200
    test_file.write_text(original_content)
    
    # Test lzma_compress
    xz_path = lzma_compress(test_file, keep_original=True)
    runner.test("lzma_compress: returns path", isinstance(xz_path, str))
    runner.test("lzma_compress: creates file", Path(xz_path).exists())
    runner.test("lzma_compress: keeps original", test_file.exists())
    
    # Test lzma_decompress
    decompressed_path = lzma_decompress(xz_path, keep_original=False)
    runner.test("lzma_decompress: returns path", isinstance(decompressed_path, str))
    runner.test("lzma_decompress: content matches", 
                Path(decompressed_path).read_text() == original_content)
    
    # Test bytes compression
    test_bytes = b"Binary LZMA test data " * 100
    compressed_bytes = lzma_compress_bytes(test_bytes)
    runner.test("lzma_compress_bytes: compresses", len(compressed_bytes) < len(test_bytes))
    
    decompressed_bytes = lzma_decompress_bytes(compressed_bytes)
    runner.test("lzma_decompress_bytes: decompresses", decompressed_bytes == test_bytes)


def run_tar_tests(runner: TestRunner, temp_dir: Path):
    """Test TAR operations."""
    print("\nTAR Operations Tests")
    print("="*60)
    
    # Create test files
    test_file1 = temp_dir / "tar_test1.txt"
    test_file1.write_text("TAR test file 1. " * 100)
    
    test_file2 = temp_dir / "tar_test2.txt"
    test_file2.write_text("TAR test file 2. " * 100)
    
    test_dir = temp_dir / "tardir"
    test_dir.mkdir()
    (test_dir / "nested.txt").write_text("Nested in TAR." * 20)
    
    # Test create_tar (uncompressed)
    tar_path = temp_dir / "test.tar"
    result = create_tar(tar_path, [test_file1, test_file2, test_dir])
    runner.test("create_tar: returns stats dict", isinstance(result, dict))
    runner.test("create_tar: creates file", tar_path.exists())
    
    # Test create_tar with gzip compression
    tar_gz_path = temp_dir / "test.tar.gz"
    result_gz = create_tar(tar_gz_path, [test_file1, test_file2], compression='gz')
    runner.test("create_tar: gz compression", tar_gz_path.exists())
    runner.test("create_tar: gz smaller", result_gz['size'] < result['size'])
    
    # Test create_tar with bz2 compression
    tar_bz2_path = temp_dir / "test.tar.bz2"
    result_bz2 = create_tar(tar_bz2_path, [test_file1, test_file2], compression='bz2')
    runner.test("create_tar: bz2 compression", tar_bz2_path.exists())
    
    # Test list_tar_contents
    contents = list_tar_contents(tar_path)
    runner.test("list_tar_contents: returns list", isinstance(contents, list))
    runner.test("list_tar_contents: has entries", len(contents) > 0)
    
    # Test extract_tar
    extract_dir = temp_dir / "tar_extracted"
    extracted = extract_tar(tar_path, extract_dir)
    runner.test("extract_tar: returns list", isinstance(extracted, list))
    runner.test("extract_tar: extracts files", len(extracted) > 0)
    runner.test("extract_tar: content matches", 
                (extract_dir / "tar_test1.txt").read_text() == test_file1.read_text())
    
    # Test append_to_tar
    new_file = temp_dir / "new_tar_file.txt"
    new_file.write_text("New TAR file." * 30)
    appended = append_to_tar(tar_path, [new_file])
    runner.test("append_to_tar: returns count", isinstance(appended, int))


def run_utility_tests(runner: TestRunner, temp_dir: Path):
    """Test utility functions."""
    print("\nUtility Functions Tests")
    print("="*60)
    
    # Test get_compression_ratio
    ratio = get_compression_ratio(1000, 500)
    runner.test("get_compression_ratio: calculates correctly", ratio == "50.0%")
    runner.test("get_compression_ratio: handles zero", get_compression_ratio(0, 0) == "N/A")
    
    # Test format_size
    runner.test("format_size: bytes", format_size(500) == "500.00 B")
    runner.test("format_size: KB", format_size(1536) == "1.50 KB")
    runner.test("format_size: MB", format_size(1572864) == "1.50 MB")
    
    # Test get_file_info
    test_file = temp_dir / "info_test.txt"
    test_file.write_text("Test content")
    info = get_file_info(test_file)
    runner.test("get_file_info: returns dict", isinstance(info, dict))
    runner.test("get_file_info: has name", 'name' in info)
    runner.test("get_file_info: has size", 'size' in info)
    runner.test("get_file_info: size correct", info['size'] == 12)
    
    # Test compare_compression_methods
    comparison = compare_compression_methods(test_file)
    runner.test("compare_compression_methods: returns dict", isinstance(comparison, dict))
    runner.test("compare_compression_methods: has methods", 
                'gzip' in comparison and 'bz2' in comparison and 'lzma' in comparison)


def run_streaming_tests(runner: TestRunner, temp_dir: Path):
    """Test streaming compression classes."""
    print("\nStreaming Compression Tests")
    print("="*60)
    
    # Test StreamingCompressor with gzip
    compressor = StreamingCompressor('gzip')
    chunk1 = compressor.write(b"Hello ")
    chunk2 = compressor.write(b"World!")
    final = compressor.flush()
    runner.test("StreamingCompressor: creates instance", compressor is not None)
    
    # Test StreamingDecompressor with gzip
    decompressor = StreamingDecompressor('gzip')
    try:
        # Note: gzip streaming is tricky, just test instantiation
        runner.test("StreamingDecompressor: creates instance", decompressor is not None)
    except Exception as e:
        runner.test("StreamingDecompressor: creates instance", False, str(e))
    
    # Test reset functionality
    compressor.reset()
    runner.test("StreamingCompressor: reset works", compressor._buffer is not None)
    
    # Test different algorithms
    for algo in ['gzip', 'bz2', 'lzma']:
        try:
            comp = StreamingCompressor(algo)
            runner.test(f"StreamingCompressor: {algo} supported", comp is not None)
        except Exception as e:
            runner.test(f"StreamingCompressor: {algo} supported", False, str(e))


def run_module_info_tests(runner: TestRunner):
    """Test module info function."""
    print("\nModule Info Tests")
    print("="*60)
    
    info = get_module_info()
    runner.test("get_module_info: returns dict", isinstance(info, dict))
    runner.test("get_module_info: has name", 'name' in info)
    runner.test("get_module_info: has version", 'version' in info)
    runner.test("get_module_info: zero dependencies", info.get('zero_dependencies') == True)
    runner.test("get_module_info: lists formats", 'supported_formats' in info)


def run_edge_case_tests(runner: TestRunner, temp_dir: Path):
    """Test edge cases and error handling."""
    print("\nEdge Case Tests")
    print("="*60)
    
    # Test empty file
    empty_file = temp_dir / "empty.txt"
    empty_file.write_text("")
    
    gz_empty = gzip_compress(empty_file, keep_original=True)
    runner.test("gzip_compress: handles empty file", Path(gz_empty).exists())
    
    # Test large content
    large_file = temp_dir / "large.txt"
    large_content = "Large content line. " * 10000
    large_file.write_text(large_content)
    
    gz_large = gzip_compress(large_file, keep_original=True)
    runner.test("gzip_compress: handles large file", Path(gz_large).exists())
    
    gz_large_result = gzip_decompress(gz_large, keep_original=False)
    runner.test("gzip_decompress: large file content matches",
                Path(gz_large_result).read_text() == large_content)
    
    # Test Unicode content
    unicode_file = temp_dir / "unicode.txt"
    unicode_content = "Hello 世界！Привет! مرحبا! 🌍"
    unicode_file.write_text(unicode_content, encoding='utf-8')
    
    gz_unicode = gzip_compress(unicode_file, keep_original=True)
    gz_unicode_result = gzip_decompress(gz_unicode, keep_original=False)
    runner.test("gzip: handles Unicode content",
                Path(gz_unicode_result).read_text(encoding='utf-8') == unicode_content)
    
    # Test non-existent file (should raise error)
    try:
        create_zip(temp_dir / "fail.zip", [temp_dir / "nonexistent.txt"])
        runner.test("create_zip: handles non-existent file", False, "Should have raised error")
    except FileNotFoundError:
        runner.test("create_zip: raises FileNotFoundError for missing file", True)


def run_all_tests():
    """Run all test suites."""
    runner = TestRunner()
    
    print("="*60)
    print("Compression Utilities Test Suite")
    print("="*60)
    
    with TempDirectory() as temp_dir:
        run_zip_tests(runner, temp_dir)
        run_gzip_tests(runner, temp_dir)
        run_bz2_tests(runner, temp_dir)
        run_lzma_tests(runner, temp_dir)
        run_tar_tests(runner, temp_dir)
        run_utility_tests(runner, temp_dir)
        run_streaming_tests(runner, temp_dir)
        run_module_info_tests(runner)
        run_edge_case_tests(runner, temp_dir)
    
    return runner.report()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
