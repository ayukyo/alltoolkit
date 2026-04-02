"""
File Utilities Test Suite
文件工具函数测试套件

覆盖场景:
- 正常读写操作
- 边界值处理
- 异常情况处理
- 大文件哈希计算
- 并发安全（原子写入）

Author: AllToolkit
Version: 1.0.0
"""

import os
import tempfile
import shutil
from pathlib import Path
import sys
import hashlib

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_utils import (
    safe_read_text,
    safe_write_text,
    get_file_hash,
    get_file_size,
    ensure_dir,
    list_files,
    copy_file,
    move_file,
    delete_file,
    get_unique_filename,
)


def test_safe_read_text_existing_file(tmp_path):
    """测试读取存在的文件"""
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content, encoding='utf-8')
    
    result = safe_read_text(test_file)
    assert result == test_content


def test_safe_read_text_nonexistent_file(tmp_path):
    """测试读取不存在的文件返回默认值"""
    test_file = tmp_path / "nonexistent.txt"
    
    result = safe_read_text(test_file)
    assert result is None
    
    result = safe_read_text(test_file, default="")
    assert result == ""


def test_safe_read_text_unicode_content(tmp_path):
    """测试读取 Unicode 内容（包括 Emoji）"""
    test_file = tmp_path / "test.txt"
    test_content = "Hello 世界 🌍"
    test_file.write_text(test_content, encoding='utf-8')
    
    result = safe_read_text(test_file)
    assert result == test_content


def test_safe_write_text_new_file(tmp_path):
    """测试写入新文件"""
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    
    result = safe_write_text(test_file, test_content)
    assert result is True
    assert test_file.read_text(encoding='utf-8') == test_content


def test_safe_write_text_creates_directories(tmp_path):
    """测试自动创建父目录"""
    test_file = tmp_path / "subdir" / "nested" / "test.txt"
    test_content = "Nested content"
    
    result = safe_write_text(test_file, test_content)
    assert result is True
    assert test_file.exists()
    assert test_file.read_text(encoding='utf-8') == test_content


def test_safe_write_text_atomic(tmp_path):
    """测试原子写入"""
    test_file = tmp_path / "test.txt"
    test_content = "Atomic content"
    
    result = safe_write_text(test_file, test_content, atomic=True)
    assert result is True
    assert test_file.read_text(encoding='utf-8') == test_content


def test_get_file_hash_md5(tmp_path):
    """测试 MD5 哈希计算"""
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content, encoding='utf-8')
    
    result = get_file_hash(test_file, algorithm='md5')
    assert result is not None
    assert len(result) == 32  # MD5 哈希长度为 32 字符
    # Verify hash matches Python's hashlib
    expected_hash = hashlib.md5(test_content.encode('utf-8')).hexdigest()
    assert result == expected_hash


def test_get_file_hash_sha256(tmp_path):
    """测试 SHA256 哈希计算"""
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content, encoding='utf-8')
    
    result = get_file_hash(test_file, algorithm='sha256')
    assert result is not None
    assert len(result) == 64  # SHA256 哈希长度为 64 字符


def test_get_file_hash_nonexistent_file(tmp_path):
    """测试计算不存在文件的哈希返回 None"""
    test_file = tmp_path / "nonexistent.txt"
    
    result = get_file_hash(test_file)
    assert result is None


def test_get_file_hash_invalid_algorithm(tmp_path):
    """测试无效的哈希算法返回 None"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content", encoding='utf-8')
    
    result = get_file_hash(test_file, algorithm='invalid')
    assert result is None


def test_get_file_size_bytes(tmp_path):
    """测试获取字节大小"""
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content, encoding='utf-8')
    
    result = get_file_size(test_file)
    assert result == len(test_content.encode('utf-8'))


def test_get_file_size_human_readable(tmp_path):
    """测试获取人类可读格式大小"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("X" * 1024, encoding='utf-8')  # 1KB
    
    result = get_file_size(test_file, human_readable=True)
    assert isinstance(result, str)
    assert "KB" in result


def test_get_file_size_nonexistent_file(tmp_path):
    """测试获取不存在文件大小返回 None"""
    test_file = tmp_path / "nonexistent.txt"
    
    result = get_file_size(test_file)
    assert result is None


def test_ensure_dir_new_directory(tmp_path):
    """测试创建新目录"""
    test_dir = tmp_path / "newdir"
    
    result = ensure_dir(test_dir)
    assert result is True
    assert test_dir.is_dir()


def test_ensure_dir_existing_directory(tmp_path):
    """测试已存在目录返回 True"""
    test_dir = tmp_path / "existing"
    test_dir.mkdir()
    
    result = ensure_dir(test_dir)
    assert result is True


def test_ensure_dir_nested_directories(tmp_path):
    """测试创建嵌套目录"""
    test_dir = tmp_path / "a" / "b" / "c"
    
    result = ensure_dir(test_dir)
    assert result is True
    assert test_dir.is_dir()


def test_list_files_all_files(tmp_path):
    """测试列出所有文件"""
    (tmp_path / "file1.txt").write_text("content1")
    (tmp_path / "file2.txt").write_text("content2")
    (tmp_path / "file3.py").write_text("content3")
    
    result = list_files(tmp_path)
    assert len(result) == 3


def test_list_files_with_pattern(tmp_path):
    """测试使用通配符模式"""
    (tmp_path / "file1.txt").write_text("content1")
    (tmp_path / "file2.txt").write_text("content2")
    (tmp_path / "script.py").write_text("content3")
    
    result = list_files(tmp_path, pattern="*.txt")
    assert len(result) == 2


def test_list_files_nonexistent_directory(tmp_path):
    """测试列出不存在目录返回空列表"""
    result = list_files(tmp_path / "nonexistent")
    assert result == []


def test_copy_file_success(tmp_path):
    """测试成功复制文件"""
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("content", encoding='utf-8')
    
    result = copy_file(src, dst)
    assert result is True
    assert dst.exists()
    assert dst.read_text(encoding='utf-8') == "content"


def test_copy_file_no_overwrite(tmp_path):
    """测试不覆盖已存在文件"""
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("new content", encoding='utf-8')
    dst.write_text("old content", encoding='utf-8')
    
    result = copy_file(src, dst, overwrite=False)
    assert result is False
    assert dst.read_text(encoding='utf-8') == "old content"


def test_copy_file_overwrite(tmp_path):
    """测试覆盖已存在文件"""
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("new content", encoding='utf-8')
    dst.write_text("old content", encoding='utf-8')
    
    result = copy_file(src, dst, overwrite=True)
    assert result is True
    assert dst.read_text(encoding='utf-8') == "new content"


def test_move_file_success(tmp_path):
    """测试成功移动文件"""
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("content", encoding='utf-8')
    
    result = move_file(src, dst)
    assert result is True
    assert not src.exists()
    assert dst.exists()
    assert dst.read_text(encoding='utf-8') == "content"


def test_move_file_nonexistent_source(tmp_path):
    """测试移动不存在的文件返回 False"""
    src = tmp_path / "nonexistent.txt"
    dst = tmp_path / "dest.txt"
    
    result = move_file(src, dst)
    assert result is False


def test_delete_file_success(tmp_path):
    """测试成功删除文件"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content", encoding='utf-8')
    
    result = delete_file(test_file)
    assert result is True
    assert not test_file.exists()


def test_delete_file_missing_ok(tmp_path):
    """测试删除不存在的文件（missing_ok=True）"""
    test_file = tmp_path / "nonexistent.txt"
    
    result = delete_file(test_file, missing_ok=True)
    assert result is True


def test_delete_file_missing_not_ok(tmp_path):
    """测试删除不存在的文件（missing_ok=False）"""
    test_file = tmp_path / "nonexistent.txt"
    
    result = delete_file(test_file, missing_ok=False)
    assert result is False


def test_get_unique_filename_new_file(tmp_path):
    """测试获取不存在的文件的文件名"""
    test_file = tmp_path / "test.txt"
    
    result = get_unique_filename(test_file)
    assert result == test_file


def test_get_unique_filename_existing_file(tmp_path):
    """测试获取已存在文件的唯一文件名"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content", encoding='utf-8')
    
    result = get_unique_filename(test_file)
    assert result.name == "test_1.txt"


def test_get_unique_filename_multiple_existing(tmp_path):
    """测试获取多个已存在文件的唯一文件名"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content", encoding='utf-8')
    (tmp_path / "test_1.txt").write_text("content", encoding='utf-8')
    (tmp_path / "test_2.txt").write_text("content", encoding='utf-8')
    
    result = get_unique_filename(test_file)
    assert result.name == "test_3.txt"


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise print message
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("Tests require pytest. Install with: pip install pytest")
        print("Or run with: python -m pytest file_utils_test.py -v")
