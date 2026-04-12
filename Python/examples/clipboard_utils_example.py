"""
Clipboard Utils 使用示例

演示 clipboard_utils.py 中各函数的使用方法
直接运行：python examples/clipboard_utils_example.py

注意：部分功能需要图形界面环境才能正常工作
在无头服务器或 Docker 容器中可能受限
"""

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clipboard_utils import (
    copy_text,
    paste_text,
    clear_clipboard,
    copy_file_path,
    copy_files_list,
    get_clipboard_history,
    is_clipboard_available,
    get_platform_info
)
import tempfile
import os


def demo_platform_info():
    """演示平台信息获取"""
    print("=" * 50)
    print("演示：获取平台信息")
    print("=" * 50)
    
    info = get_platform_info()
    print("操作系统：{}".format(info['platform']))
    print("系统平台：{}".format(info['sys_platform']))
    print("剪贴板工具：{}".format(info['tools']))
    print("是否可用：{}".format('是' if info['available'] else '否'))
    print()


def demo_basic_copy_paste():
    """演示基本复制粘贴功能"""
    print("=" * 50)
    print("演示：基本复制粘贴")
    print("=" * 50)
    
    if not is_clipboard_available():
        print("⚠ 剪贴板不可用，跳过此演示")
        print("提示：在 Linux 上安装 xclip: sudo apt install xclip")
        return
    
    # 复制文本
    text = "Hello, AllToolkit! 你好，世界！"
    print("准备复制：{}".format(text))
    
    success = copy_text(text)
    print("复制结果：{}".format('成功' if success else '失败'))
    
    # 粘贴文本
    if success:
        pasted = paste_text()
        if pasted:
            print("粘贴内容：{}".format(pasted))
            print("内容匹配：{}".format('是' if pasted == text else '否'))
        else:
            print("粘贴返回空值（可能是空剪贴板）")
    print()


def demo_clear_clipboard():
    """演示清空剪贴板"""
    print("=" * 50)
    print("演示：清空剪贴板")
    print("=" * 50)
    
    if not is_clipboard_available():
        print("⚠ 剪贴板不可用，跳过此演示")
        return
    
    # 先复制一些内容
    copy_text("这是将要被清空的内容")
    print("已复制：'这是将要被清空的内容'")
    
    # 清空剪贴板
    clear_result = clear_clipboard()
    print("清空结果：{}".format('成功' if clear_result else '失败'))
    
    # 验证是否清空
    pasted = paste_text()
    if pasted is None or pasted == "":
        print("✓ 剪贴板已清空")
    else:
        print("⚠ 剪贴板可能未完全清空：'{}'".format(pasted))
    print()


def demo_unicode_content():
    """演示 Unicode 和 Emoji 内容"""
    print("=" * 50)
    print("演示：Unicode 和 Emoji 内容")
    print("=" * 50)
    
    if not is_clipboard_available():
        print("⚠ 剪贴板不可用，跳过此演示")
        return
    
    # 多语言文本
    texts = [
        "中文：你好世界",
        "日本語：こんにちは世界",
        "한국어: 안녕하세요 세계",
        "Русский: Привет мир",
        "العربية: مرحبا بالعالم",
        "Emoji: 🌍🚀💻🎉🔥"
    ]
    
    for text in texts:
        copy_text(text)
        pasted = paste_text()
        match = "✓" if pasted == text else "✗"
        print("{} {}".format(match, text))
    print()


def demo_file_path():
    """演示文件路径复制"""
    print("=" * 50)
    print("演示：文件路径复制")
    print("=" * 50)
    
    if not is_clipboard_available():
        print("⚠ 剪贴板不可用，跳过此演示")
        return
    
    # 创建临时文件
    fd, temp_path = tempfile.mkstemp(suffix='.txt')
    try:
        os.write(fd, "示例文件内容".encode('utf-8'))
        os.close(fd)
        
        print("临时文件：{}".format(temp_path))
        
        # 复制文件路径
        result = copy_file_path(temp_path)
        print("复制路径：{}".format('成功' if result else '失败'))
        
        # 验证粘贴内容
        pasted = paste_text()
        if pasted:
            print("粘贴的路径：{}".format(pasted))
            print("是绝对路径：{}".format('是' if os.path.isabs(pasted) else '否'))
            print("文件存在：{}".format('是' if os.path.exists(pasted) else '否'))
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_path)
        except:
            pass
    print()


def demo_multiple_files():
    """演示多个文件路径复制"""
    print("=" * 50)
    print("演示：多个文件路径复制")
    print("=" * 50)
    
    if not is_clipboard_available():
        print("⚠ 剪贴板不可用，跳过此演示")
        return
    
    # 创建多个临时文件
    temp_files = []
    try:
        for i in range(3):
            fd, tmp_path = tempfile.mkstemp(suffix='_file{}.txt'.format(i))
            os.write(fd, "文件 {} 的内容".format(i).encode('utf-8'))
            os.close(fd)
            temp_files.append(tmp_path)
        
        print("创建 {} 个临时文件".format(len(temp_files)))
        
        # 复制文件列表（默认换行分隔）
        result = copy_files_list(temp_files)
        print("复制文件列表：{}".format('成功' if result else '失败'))
        
        # 验证粘贴内容
        pasted = paste_text()
        if pasted:
            lines = pasted.strip().split('\n')
            print("粘贴的行数：{}".format(len(lines)))
            print("文件路径列表:")
            for i, line in enumerate(lines, 1):
                print("  {}. {}".format(i, os.path.basename(line)))
        
        # 使用自定义分隔符
        print("\n使用逗号分隔:")
        copy_files_list(temp_files, separator=', ')
        pasted = paste_text()
        if pasted:
            print("{}...".format(pasted[:80]))
            
    finally:
        # 清理临时文件
        for f in temp_files:
            try:
                os.unlink(f)
            except:
                pass
    print()


def demo_clipboard_history():
    """演示剪贴板历史"""
    print("=" * 50)
    print("演示：剪贴板历史")
    print("=" * 50)
    
    if not is_clipboard_available():
        print("⚠ 剪贴板不可用，跳过此演示")
        return
    
    # 复制一些内容
    test_items = ["项目 1", "项目 2", "项目 3"]
    for item in test_items:
        copy_text(item)
    
    # 获取历史
    history = get_clipboard_history(max_items=10)
    print("剪贴板历史项目数：{}".format(len(history)))
    
    if history:
        print("历史内容:")
        for i, item in enumerate(history, 1):
            preview = item[:50] + "..." if len(item) > 50 else item
            print("  {}. {}".format(i, preview))
    else:
        print("（当前平台不支持剪贴板历史或历史为空）")
    print()


def demo_practical_scenarios():
    """演示实际应用场景"""
    print("=" * 50)
    print("演示：实际应用场景")
    print("=" * 50)
    
    if not is_clipboard_available():
        print("⚠ 剪贴板不可用，跳过此演示")
        return
    
    # 场景 1: 快速复制代码片段
    print("场景 1: 复制代码片段")
    code_snippet = """
def hello_world():
    print("Hello, World!")
    return True
""".strip()
    copy_text(code_snippet)
    print("✓ 代码片段已复制到剪贴板")
    
    # 场景 2: 复制配置信息
    print("\n场景 2: 复制配置信息")
    config = """
Server: production.example.com
Port: 443
Protocol: HTTPS
Timeout: 30s
""".strip()
    copy_text(config)
    print("✓ 配置信息已复制到剪贴板")
    
    # 场景 3: 复制日志错误
    print("\n场景 3: 复制错误日志")
    error_log = """
[ERROR] 2024-01-15 10:30:45
Module: database.connection
Message: Connection timeout after 30s
Stack trace: ...
""".strip()
    copy_text(error_log)
    print("✓ 错误日志已复制到剪贴板")
    
    # 场景 4: 分享文件列表
    print("\n场景 4: 分享项目文件列表")
    project_files = [
        "src/main.py",
        "src/utils.py", 
        "tests/test_main.py",
        "README.md",
        "requirements.txt"
    ]
    copy_files_list(project_files)
    print("✓ 文件列表已复制到剪贴板")
    pasted = paste_text()
    if pasted:
        print("内容预览:\n{}".format(pasted))
    
    print()


def demo_error_handling():
    """演示错误处理"""
    print("=" * 50)
    print("演示：错误处理")
    print("=" * 50)
    
    # 检查剪贴板可用性
    available = is_clipboard_available()
    print("剪贴板可用性：{}".format(available))
    
    if not available:
        print("\n建议:")
        platform = get_platform_info()['platform']
        if platform == 'linux':
            print("  Linux: 安装 xclip 或 xsel")
            print("    sudo apt install xclip")
            print("    或：sudo apt install xsel")
        elif platform == 'windows':
            print("  Windows: 确保 clip.exe 可用")
        elif platform == 'macos':
            print("  macOS: pbcopy/pbpaste 应该默认可用")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("AllToolkit - Python Clipboard Utils 示例")
    print("=" * 50 + "\n")
    
    demos = [
        demo_platform_info,
        demo_basic_copy_paste,
        demo_clear_clipboard,
        demo_unicode_content,
        demo_file_path,
        demo_multiple_files,
        demo_clipboard_history,
        demo_practical_scenarios,
        demo_error_handling,
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print("演示中出现错误：{}: {}\n".format(type(e).__name__, e))
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)
