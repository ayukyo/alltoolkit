"""
Clipboard Utilities Test Suite
剪贴板工具函数测试套件

覆盖场景:
- 文本复制粘贴基本功能
- 跨平台兼容性
- 异常情况处理
- 文件路径操作
- 剪贴板清空
- 平台检测

Author: AllToolkit
Version: 1.0.0
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clipboard_utils import (
    ClipboardError,
    _get_platform,
    copy_text,
    paste_text,
    clear_clipboard,
    copy_file_path,
    copy_files_list,
    get_clipboard_history,
    is_clipboard_available,
    get_platform_info
)


def test_get_platform():
    """测试平台检测功能"""
    print("测试：平台检测")
    platform = _get_platform()
    assert platform in ['windows', 'macos', 'linux', 'unknown']
    print("  当前平台：{}".format(platform))


def test_get_platform_info():
    """测试平台信息获取"""
    print("测试：平台信息获取")
    info = get_platform_info()
    assert 'platform' in info
    assert 'available' in info
    assert 'tools' in info
    assert 'sys_platform' in info
    print("  平台：{}".format(info['platform']))
    print("  可用：{}".format(info['available']))
    print("  工具：{}".format(info['tools']))


def test_is_clipboard_available():
    """测试剪贴板可用性检测"""
    print("测试：剪贴板可用性检测")
    available = is_clipboard_available()
    print("  剪贴板可用：{}".format(available))
    # Note: This might be False in headless environments


def test_copy_and_paste_text():
    """测试文本复制粘贴"""
    print("测试：文本复制粘贴")
    test_text = "Hello, AllToolkit! 测试内容 123"
    
    # Copy text
    copy_result = copy_text(test_text)
    
    # Only test paste if copy succeeded and clipboard is available
    if copy_result and is_clipboard_available():
        pasted = paste_text()
        if pasted is not None:
            assert pasted == test_text, "Expected '{}', got '{}'".format(test_text, pasted)
            print("  ✓ 复制粘贴成功")
        else:
            print("  ⚠ 粘贴返回 None (可能是 headless 环境)")
    else:
        print("  ⚠ 剪贴板不可用，跳过复制粘贴测试")


def test_copy_text_empty():
    """测试复制空文本"""
    print("测试：复制空文本")
    result = copy_text("")
    # Should succeed even with empty string
    print("  复制空文本结果：{}".format(result))


def test_copy_text_non_string():
    """测试复制非字符串内容（自动转换）"""
    print("测试：复制非字符串内容")
    result = copy_text(12345)
    if result and is_clipboard_available():
        pasted = paste_text()
        if pasted:
            assert pasted == "12345"
            print("  ✓ 数字自动转换为字符串")
    else:
        print("  ⚠ 剪贴板不可用，跳过测试")


def test_copy_text_unicode():
    """测试复制 Unicode 内容（包括 Emoji）"""
    print("测试：复制 Unicode 内容")
    test_text = "Hello 世界 🌍 Привет мир"
    
    result = copy_text(test_text)
    if result and is_clipboard_available():
        pasted = paste_text()
        if pasted:
            assert pasted == test_text
            print("  ✓ Unicode 内容复制成功")
    else:
        print("  ⚠ 剪贴板不可用，跳过测试")


def test_paste_empty_clipboard():
    """测试粘贴空剪贴板"""
    print("测试：粘贴空剪贴板")
    # Clear clipboard first
    clear_clipboard()
    
    result = paste_text()
    # May return None or empty string depending on platform
    print("  空剪贴板粘贴结果：{}".format(result))


def test_clear_clipboard():
    """测试清空剪贴板"""
    print("测试：清空剪贴板")
    # First copy something
    copy_text("Test content to clear")
    
    # Then clear
    clear_result = clear_clipboard()
    print("  清空结果：{}".format(clear_result))
    
    # Verify it's cleared (if clipboard available)
    if is_clipboard_available():
        pasted = paste_text()
        if pasted is None or pasted == "":
            print("  ✓ 剪贴板已清空")
        else:
            print("  ⚠ 剪贴板可能未完全清空：'{}'".format(pasted))


def test_copy_file_path():
    """测试复制文件路径"""
    print("测试：复制文件路径")
    
    # Create a temporary file
    fd, tmp_path = tempfile.mkstemp(suffix='.txt')
    try:
        os.write(fd, b"test content")
        os.close(fd)
        
        # Copy the file path
        result = copy_file_path(tmp_path)
        
        if result and is_clipboard_available():
            pasted = paste_text()
            if pasted:
                # Verify it's the absolute path
                assert Path(pasted).is_absolute()
                assert Path(pasted).exists()
                print("  ✓ 文件路径复制成功")
                print("  路径：{}".format(pasted))
        else:
            print("  ⚠ 剪贴板不可用，跳过测试")
    finally:
        # Cleanup
        try:
            os.unlink(tmp_path)
        except:
            pass


def test_copy_file_path_relative():
    """测试复制相对路径（应转换为绝对路径）"""
    print("测试：复制相对路径")
    
    # Use a relative path
    relative_path = "test_relative_file.txt"
    
    result = copy_file_path(relative_path)
    if result and is_clipboard_available():
        pasted = paste_text()
        if pasted:
            # Should be converted to absolute path
            assert Path(pasted).is_absolute()
            print("  ✓ 相对路径已转换为绝对路径")
            print("  绝对路径：{}".format(pasted))
    else:
        print("  ⚠ 剪贴板不可用，跳过测试")


def test_copy_files_list():
    """测试复制多个文件路径"""
    print("测试：复制多个文件路径")
    
    # Create temporary files
    temp_files = []
    try:
        for i in range(3):
            fd, tmp_path = tempfile.mkstemp(suffix='_{0}.txt'.format(i))
            os.write(fd, "content {0}".format(i).encode('utf-8'))
            os.close(fd)
            temp_files.append(tmp_path)
        
        # Copy list of file paths
        result = copy_files_list(temp_files)
        
        if result and is_clipboard_available():
            pasted = paste_text()
            if pasted:
                # Verify all paths are in the clipboard
                lines = pasted.split('\n')
                assert len(lines) == 3
                print("  ✓ 多个文件路径复制成功")
                print("  文件数：{}".format(len(lines)))
        else:
            print("  ⚠ 剪贴板不可用，跳过测试")
    finally:
        # Cleanup
        for f in temp_files:
            try:
                os.unlink(f)
            except:
                pass


def test_copy_files_list_custom_separator():
    """测试使用自定义分隔符复制文件列表"""
    print("测试：自定义分隔符复制文件列表")
    
    # Create temporary files
    temp_files = []
    try:
        for i in range(2):
            fd, tmp_path = tempfile.mkstemp(suffix='_{0}.txt'.format(i))
            os.write(fd, "content {0}".format(i).encode('utf-8'))
            os.close(fd)
            temp_files.append(tmp_path)
        
        # Copy with custom separator
        result = copy_files_list(temp_files, separator=', ')
        
        if result and is_clipboard_available():
            pasted = paste_text()
            if pasted:
                # Should be comma-separated
                assert ', ' in pasted
                print("  ✓ 自定义分隔符生效")
                print("  内容：{}".format(pasted))
        else:
            print("  ⚠ 剪贴板不可用，跳过测试")
    finally:
        # Cleanup
        for f in temp_files:
            try:
                os.unlink(f)
            except:
                pass


def test_get_clipboard_history():
    """测试获取剪贴板历史"""
    print("测试：获取剪贴板历史")
    
    # Copy something first
    copy_text("Test history item")
    
    history = get_clipboard_history()
    print("  历史项目数：{}".format(len(history)))
    
    # Should at least return current content
    if len(history) > 0:
        print("  ✓ 获取剪贴板历史成功")
    else:
        print("  ⚠ 剪贴板历史为空")


def test_get_clipboard_history_max_items():
    """测试剪贴板历史最大项目数"""
    print("测试：剪贴板历史最大项目数")
    
    history = get_clipboard_history(max_items=5)
    assert len(history) <= 5
    print("  返回项目数：{} (max: 5)".format(len(history)))


def test_clipboard_error_exception():
    """测试 ClipboardError 异常"""
    print("测试：ClipboardError 异常")
    try:
        raise ClipboardError("Test error message")
    except ClipboardError as e:
        assert str(e) == "Test error message"
        print("  ✓ ClipboardError 异常正常工作")


def test_platform_specific_behavior():
    """测试不同平台的行为"""
    print("测试：平台特定行为")
    platform = _get_platform()
    
    if platform == 'windows':
        print("  运行于 Windows 环境")
        # Windows uses clip.exe and PowerShell
    elif platform == 'macos':
        print("  运行于 macOS 环境")
        # macOS uses pbcopy/pbpaste
    elif platform == 'linux':
        print("  运行于 Linux 环境")
        # Linux uses xclip/xsel/wl-clipboard
    else:
        print("  运行于未知平台")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AllToolkit - Python Clipboard Utils 测试套件")
    print("=" * 60 + "\n")
    
    tests = [
        test_get_platform,
        test_get_platform_info,
        test_is_clipboard_available,
        test_copy_and_paste_text,
        test_copy_text_empty,
        test_copy_text_non_string,
        test_copy_text_unicode,
        test_paste_empty_clipboard,
        test_clear_clipboard,
        test_copy_file_path,
        test_copy_file_path_relative,
        test_copy_files_list,
        test_copy_files_list_custom_separator,
        test_get_clipboard_history,
        test_get_clipboard_history_max_items,
        test_clipboard_error_exception,
        test_platform_specific_behavior,
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test in tests:
        try:
            print("\n运行：{}".format(test.__name__))
            print("-" * 60)
            test()
            passed += 1
        except AssertionError as e:
            print("  ✗ 断言失败：{}".format(e))
            failed += 1
        except Exception as e:
            print("  ✗ 异常：{}: {}".format(type(e).__name__, e))
            failed += 1
    
    print("\n" + "=" * 60)
    print("测试结果：{} 通过，{} 失败".format(passed, failed))
    print("=" * 60)
    
    if failed > 0:
        sys.exit(1)
