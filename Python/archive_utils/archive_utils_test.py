"""
AllToolkit - Python Archive Utilities Test Suite

Comprehensive test suite for archive_utils module.
Covers normal scenarios, edge cases, and error conditions.

Run: python archive_utils_test.py
"""

import sys
import os
import tempfile
import shutil
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    ArchiveUtils,
    ArchiveFormat,
    CompressionLevel,
    ArchiveInfo,
    ArchiveMember,
    ArchiveOperationResult,
    detect_format,
    create_archive,
    extract_archive,
    list_archive,
    get_archive_info,
    verify_archive,
    calculate_checksum,
)


class TestResult:
    """Simple test result tracker."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name: str):
        self.passed += 1
        print(f"  ✓ {name}")
    
    def add_fail(self, name: str, expected: Any, actual: Any):
        self.failed += 1
        self.errors.append((name, expected, actual))
        print(f"  ✗ {name}")
        print(f"    Expected: {expected}")
        print(f"    Actual: {actual}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"Failed: {self.failed}")
            print(f"\nFailures:")
            for name, expected, actual in self.errors:
                print(f"  - {name}: expected {expected}, got {actual}")
        else:
            print("All tests passed! ✓")
        print(f"{'='*60}")
        return self.failed == 0


class ArchiveTestContext:
    """Context manager for test files and directories."""
    
    def __init__(self):
        self.temp_dir = None
        self.test_files = []
    
    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='archive_test_')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_file(self, name: str, content: str = "test content") -> str:
        """Create a test file."""
        path = os.path.join(self.temp_dir, name)
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else self.temp_dir, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        self.test_files.append(path)
        return path
    
    def create_dir(self, name: str) -> str:
        """Create a test directory."""
        path = os.path.join(self.temp_dir, name)
        os.makedirs(path, exist_ok=True)
        return path
    
    @property
    def path(self) -> str:
        """Get temp directory path."""
        return self.temp_dir


def run_tests():
    """Run all tests."""
    result = TestResult()
    utils = ArchiveUtils()
    
    print("=" * 60)
    print("Archive Utils Test Suite")
    print("=" * 60)
    
    # ===== Format Detection Tests =====
    print("\n[1] Format Detection Tests")
    print("-" * 40)
    
    # Test ZIP detection
    test_name = "detect_zip"
    expected = ArchiveFormat.ZIP
    actual = utils.detect_format("archive.zip")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test TAR.GZ detection
    test_name = "detect_tar_gz"
    expected = ArchiveFormat.TAR_GZ
    actual = utils.detect_format("backup.tar.gz")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test TAR.BZ2 detection
    test_name = "detect_tar_bz2"
    expected = ArchiveFormat.TAR_BZ2
    actual = utils.detect_format("data.tar.bz2")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test TAR.XZ detection
    test_name = "detect_tar_xz"
    expected = ArchiveFormat.TAR_XZ
    actual = utils.detect_format("archive.tar.xz")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test GZ detection
    test_name = "detect_gz"
    expected = ArchiveFormat.GZ
    actual = utils.detect_format("file.txt.gz")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test BZ2 detection
    test_name = "detect_bz2"
    expected = ArchiveFormat.BZ2
    actual = utils.detect_format("file.bz2")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test XZ detection
    test_name = "detect_xz"
    expected = ArchiveFormat.XZ
    actual = utils.detect_format("file.xz")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test unknown format
    test_name = "detect_unknown"
    expected = None
    actual = utils.detect_format("unknown.xyz")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test case insensitivity
    test_name = "detect_case_insensitive"
    expected = ArchiveFormat.ZIP
    actual = utils.detect_format("ARCHIVE.ZIP")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test .tgz alias
    test_name = "detect_tgz_alias"
    expected = ArchiveFormat.TAR_GZ
    actual = utils.detect_format("backup.tgz")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # ===== ZIP Archive Tests =====
    print("\n[2] ZIP Archive Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        # Create test files
        file1 = ctx.create_file("test1.txt", "Hello World 1")
        file2 = ctx.create_file("test2.txt", "Hello World 2")
        subdir = ctx.create_dir("subdir")
        file3 = ctx.create_file("subdir/test3.txt", "Hello World 3")
        
        zip_path = os.path.join(ctx.path, "test.zip")
        
        # Test create ZIP
        test_name = "create_zip"
        zip_result = utils.create_archive(zip_path, [file1, file2, subdir])
        if zip_result.success and os.path.exists(zip_path):
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "success=True", zip_result.success)
        
        # Test list ZIP contents
        test_name = "list_zip"
        if zip_result.success:
            members = utils.list_archive(zip_path)
            member_names = [m.name for m in members]
            expected_count = 3  # test1.txt, test2.txt, subdir/test3.txt
            if len(members) == expected_count:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, f"{expected_count} members", len(members))
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test extract ZIP
        test_name = "extract_zip"
        if zip_result.success:
            extract_dir = os.path.join(ctx.path, "extracted")
            extract_result = utils.extract_archive(zip_path, extract_dir)
            if extract_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", extract_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test verify ZIP
        test_name = "verify_zip"
        if zip_result.success:
            verify_result = utils.verify_archive(zip_path)
            if verify_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", verify_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test get archive info
        test_name = "get_zip_info"
        if zip_result.success:
            info = utils.get_archive_info(zip_path)
            if info.format == ArchiveFormat.ZIP and info.file_count > 0:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "valid info", info.to_dict())
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test checksum
        test_name = "zip_checksum"
        if zip_result.success:
            checksum = utils.calculate_checksum(zip_path)
            if len(checksum) == 64:  # SHA256 hex length
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "64 char hex", len(checksum))
        else:
            result.add_fail(test_name, "archive created", "archive not created")
    
    # ===== TAR.GZ Archive Tests =====
    print("\n[3] TAR.GZ Archive Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        # Create test files
        file1 = ctx.create_file("data1.txt", "Data content 1")
        file2 = ctx.create_file("data2.txt", "Data content 2")
        
        targz_path = os.path.join(ctx.path, "test.tar.gz")
        
        # Test create TAR.GZ
        test_name = "create_tar_gz"
        result_op = utils.create_archive(targz_path, [file1, file2])
        if result_op.success and os.path.exists(targz_path):
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "success=True", result_op.success)
        
        # Test extract TAR.GZ
        test_name = "extract_tar_gz"
        if result_op.success:
            extract_dir = os.path.join(ctx.path, "extracted_targz")
            extract_result = utils.extract_archive(targz_path, extract_dir)
            if extract_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", extract_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test verify TAR.GZ
        test_name = "verify_tar_gz"
        if result_op.success:
            verify_result = utils.verify_archive(targz_path)
            if verify_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", verify_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
    
    # ===== TAR.BZ2 Archive Tests =====
    print("\n[4] TAR.BZ2 Archive Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        file1 = ctx.create_file("bz2test.txt", "BZ2 test content")
        tarbz2_path = os.path.join(ctx.path, "test.tar.bz2")
        
        # Test create TAR.BZ2
        test_name = "create_tar_bz2"
        result_op = utils.create_archive(tarbz2_path, [file1])
        if result_op.success:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "success=True", result_op.success)
        
        # Test extract TAR.BZ2
        test_name = "extract_tar_bz2"
        if result_op.success:
            extract_dir = os.path.join(ctx.path, "extracted_tarbz2")
            extract_result = utils.extract_archive(tarbz2_path, extract_dir)
            if extract_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", extract_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
    
    # ===== GZIP Tests =====
    print("\n[5] GZIP Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        file1 = ctx.create_file("original.txt", "This is original content for gzip test")
        gz_path = os.path.join(ctx.path, "original.txt.gz")
        
        # Test create GZ
        test_name = "create_gz"
        result_op = utils.create_archive(gz_path, [file1])
        if result_op.success and os.path.exists(gz_path):
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "success=True", result_op.success)
        
        # Test extract GZ
        test_name = "extract_gz"
        if result_op.success:
            extract_dir = ctx.path
            extract_result = utils.extract_archive(gz_path, extract_dir)
            if extract_result.success:
                # Check if original file was restored
                restored_path = os.path.join(extract_dir, "original.txt")
                if os.path.exists(restored_path):
                    result.add_pass(test_name)
                else:
                    result.add_fail(test_name, "file restored", "file not found")
            else:
                result.add_fail(test_name, "success=True", extract_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
    
    # ===== BZ2 Tests =====
    print("\n[6] BZ2 Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        file1 = ctx.create_file("bz2original.txt", "Content for BZ2 compression")
        bz2_path = os.path.join(ctx.path, "bz2original.txt.bz2")
        
        # Test create BZ2
        test_name = "create_bz2"
        result_op = utils.create_archive(bz2_path, [file1])
        if result_op.success:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "success=True", result_op.success)
        
        # Test extract BZ2
        test_name = "extract_bz2"
        if result_op.success:
            extract_result = utils.extract_archive(bz2_path, ctx.path)
            if extract_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", extract_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
    
    # ===== XZ Tests =====
    print("\n[7] XZ Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        file1 = ctx.create_file("xzoriginal.txt", "Content for XZ compression test")
        xz_path = os.path.join(ctx.path, "xzoriginal.txt.xz")
        
        # Test create XZ
        test_name = "create_xz"
        result_op = utils.create_archive(xz_path, [file1])
        if result_op.success:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "success=True", result_op.success)
        
        # Test extract XZ
        test_name = "extract_xz"
        if result_op.success:
            extract_result = utils.extract_archive(xz_path, ctx.path)
            if extract_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", extract_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
    
    # ===== Error Handling Tests =====
    print("\n[8] Error Handling Tests")
    print("-" * 40)
    
    # Test extract non-existent file
    test_name = "extract_nonexistent"
    result_op = utils.extract_archive("/nonexistent/path/archive.zip", ctx.path if 'ctx' in dir() else "/tmp")
    if not result_op.success and len(result_op.errors) > 0:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "success=False with errors", result_op.success)
    
    # Test list non-existent file
    test_name = "list_nonexistent"
    try:
        utils.list_archive("/nonexistent/path/archive.zip")
        result.add_fail(test_name, "FileNotFoundError", "no exception")
    except FileNotFoundError:
        result.add_pass(test_name)
    except Exception as e:
        result.add_fail(test_name, "FileNotFoundError", type(e).__name__)
    
    # Test unknown format
    test_name = "unknown_format_error"
    try:
        utils.list_archive("/tmp/test.unknown")
        result.add_fail(test_name, "ValueError", "no exception")
    except ValueError as e:
        if "Unknown archive format" in str(e):
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "Unknown archive format", str(e))
    except Exception as e:
        result.add_fail(test_name, "ValueError", type(e).__name__)
    
    # Test invalid checksum algorithm
    test_name = "invalid_checksum_algo"
    with ArchiveTestContext() as ctx:
        file1 = ctx.create_file("test.txt", "test")
        zip_path = os.path.join(ctx.path, "test.zip")
        utils.create_archive(zip_path, [file1])
        
        try:
            utils.calculate_checksum(zip_path, "invalid_algo")
            result.add_fail(test_name, "ValueError", "no exception")
        except ValueError:
            result.add_pass(test_name)
        except Exception as e:
            result.add_fail(test_name, "ValueError", type(e).__name__)
    
    # ===== Module-level Function Tests =====
    print("\n[9] Module-level Function Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        file1 = ctx.create_file("modtest.txt", "Module test content")
        
        # Test module-level detect_format
        test_name = "mod_detect_format"
        fmt = detect_format("test.zip")
        if fmt == ArchiveFormat.ZIP:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, ArchiveFormat.ZIP, fmt)
        
        # Test module-level create_archive
        test_name = "mod_create_archive"
        zip_path = os.path.join(ctx.path, "modtest.zip")
        result_op = create_archive(zip_path, [file1])
        if result_op.success:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "success=True", result_op.success)
        
        # Test module-level extract_archive
        test_name = "mod_extract_archive"
        if result_op.success:
            extract_result = extract_archive(zip_path, ctx.path)
            if extract_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", extract_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test module-level list_archive
        test_name = "mod_list_archive"
        if result_op.success:
            members = list_archive(zip_path)
            if len(members) > 0:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, ">0 members", len(members))
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test module-level get_archive_info
        test_name = "mod_get_info"
        if result_op.success:
            info = get_archive_info(zip_path)
            if isinstance(info, ArchiveInfo):
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "ArchiveInfo", type(info).__name__)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test module-level verify_archive
        test_name = "mod_verify"
        if result_op.success:
            verify_result = verify_archive(zip_path)
            if verify_result.success:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", verify_result.success)
        else:
            result.add_fail(test_name, "archive created", "archive not created")
        
        # Test module-level calculate_checksum
        test_name = "mod_checksum"
        if result_op.success:
            checksum = calculate_checksum(zip_path)
            if len(checksum) == 64:
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "64 char hex", len(checksum))
        else:
            result.add_fail(test_name, "archive created", "archive not created")
    
    # ===== ArchiveInfo Tests =====
    print("\n[10] ArchiveInfo Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        file1 = ctx.create_file("infotest.txt", "Info test content for compression ratio")
        zip_path = os.path.join(ctx.path, "infotest.zip")
        utils.create_archive(zip_path, [file1])
        
        test_name = "archive_info_format"
        info = utils.get_archive_info(zip_path)
        if info.format == ArchiveFormat.ZIP:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, ArchiveFormat.ZIP, info.format)
        
        test_name = "archive_info_file_count"
        if info.file_count >= 1:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, ">=1", info.file_count)
        
        test_name = "archive_info_to_dict"
        info_dict = info.to_dict()
        if 'path' in info_dict and 'format' in info_dict and 'file_count' in info_dict:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "dict with keys", info_dict.keys())
    
    # ===== Compression Level Tests =====
    print("\n[11] Compression Level Tests")
    print("-" * 40)
    
    with ArchiveTestContext() as ctx:
        # Create a larger file for compression testing
        large_content = "x" * 10000  # 10KB of repetitive content
        file1 = ctx.create_file("compressible.txt", large_content)
        
        # Test different compression levels
        for level in [CompressionLevel.FASTEST, CompressionLevel.DEFAULT, CompressionLevel.BEST]:
            test_name = f"compression_{level.name.lower()}"
            zip_path = os.path.join(ctx.path, f"compress_{level.name}.zip")
            result_op = utils.create_archive(zip_path, [file1], compression=level)
            if result_op.success and os.path.exists(zip_path):
                result.add_pass(test_name)
            else:
                result.add_fail(test_name, "success=True", result_op.success)
    
    # Summary
    result.summary()
    return result.failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
