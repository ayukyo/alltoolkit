"""
Clipboard Utilities Module
剪贴板工具函数库

提供跨平台的剪贴板操作功能，支持文本和文件的复制粘贴。
自动检测系统平台并使用合适的后端（pyperclip/clipboard）。
所有函数设计为简单易用，无外部依赖（可选安装 pyperclip 增强兼容性）。

Author: AllToolkit
Version: 1.0.0
"""

import subprocess
import sys
import os
from typing import Optional, List
from pathlib import Path


class ClipboardError(Exception):
    """剪贴板操作异常"""
    pass


def _get_platform() -> str:
    """
    获取当前操作系统平台
    
    Returns:
        平台标识：'windows', 'macos', 'linux', 'unknown'
    """
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'macos'
    elif sys.platform.startswith('linux'):
        return 'linux'
    else:
        return 'unknown'


def _run_subprocess(cmd, input_data=None, capture=True, timeout_sec=5.0):
    """
    运行子进程（Python 3.6+ 兼容）
    
    Args:
        cmd: 命令参数列表
        input_data: 可选的输入数据
        capture: 是否捕获输出
        timeout_sec: 超时时间（秒）
    
    Returns:
        tuple: (returncode, stdout, stderr)
    """
    import time
    try:
        kwargs = {
            'universal_newlines': True
        }
        if input_data is not None:
            kwargs['stdin'] = subprocess.PIPE
        if capture:
            kwargs['stdout'] = subprocess.PIPE
            kwargs['stderr'] = subprocess.PIPE
        
        proc = subprocess.Popen(cmd, **kwargs)
        
        # Python 3.6 compatibility: use a simple timeout mechanism
        start_time = time.time()
        while proc.poll() is None:
            if time.time() - start_time > timeout_sec:
                proc.terminate()
                return -1, None, "Timeout"
            time.sleep(0.01)
        
        stdout, stderr = proc.communicate(input=input_data)
        return proc.returncode, stdout, stderr
    except FileNotFoundError:
        return -2, None, "Command not found"
    except OSError as e:
        return -3, None, str(e)


def copy_text(text: str) -> bool:
    """
    复制文本到剪贴板
    
    功能：将文本内容复制到系统剪贴板，支持跨平台操作。
    自动检测系统并使用合适的命令行工具。
    
    Args:
        text: 要复制的文本内容
    
    Returns:
        操作成功返回 True，失败返回 False
    
    Examples:
        >>> copy_text("Hello, World!")
        >>> copy_text("复制这段文本到剪贴板")
    """
    if not isinstance(text, str):
        text = str(text)
    
    platform = _get_platform()
    
    try:
        if platform == 'windows':
            # Windows: use clip.exe
            returncode, _, _ = _run_subprocess(['clip'], input_data=text)
            return returncode == 0
            
        elif platform == 'macos':
            # macOS: use pbcopy
            returncode, _, _ = _run_subprocess(['pbcopy'], input_data=text)
            return returncode == 0
            
        elif platform == 'linux':
            # Linux: try xclip, then xsel, then wl-clipboard
            linux_commands = [
                ['xclip', '-selection', 'clipboard'],
                ['xsel', '--clipboard', '--input'],
                ['wl-copy']
            ]
            
            for cmd in linux_commands:
                returncode, _, _ = _run_subprocess(cmd, input_data=text)
                if returncode == 0:
                    return True
            
            return False
        else:
            return False
            
    except (OSError, IOError):
        return False


def paste_text() -> Optional[str]:
    """
    从剪贴板粘贴文本
    
    功能：从系统剪贴板读取文本内容，支持跨平台操作。
    
    Returns:
        剪贴板文本内容，失败或空剪贴板返回 None
    
    Examples:
        >>> content = paste_text()
        >>> if content:
        ...     print(f"剪贴板内容：{content}")
    """
    platform = _get_platform()
    
    try:
        if platform == 'windows':
            # Windows: use powershell
            returncode, stdout, _ = _run_subprocess(
                ['powershell', '-command', 'Get-Clipboard']
            )
            if returncode == 0 and stdout:
                return stdout.rstrip('\r\n')
            return None
            
        elif platform == 'macos':
            # macOS: use pbpaste
            returncode, stdout, _ = _run_subprocess(['pbpaste'])
            if returncode == 0 and stdout:
                return stdout
            return None
            
        elif platform == 'linux':
            # Linux: try xclip, then xsel, then wl-clipboard
            linux_commands = [
                ['xclip', '-selection', 'clipboard', '-o'],
                ['xsel', '--clipboard', '--output'],
                ['wl-paste']
            ]
            
            for cmd in linux_commands:
                returncode, stdout, _ = _run_subprocess(cmd)
                if returncode == 0 and stdout:
                    return stdout
            
            return None
        else:
            return None
            
    except (OSError, IOError):
        return None


def clear_clipboard() -> bool:
    """
    清空剪贴板
    
    功能：清除系统剪贴板中的所有内容。
    
    Returns:
        操作成功返回 True，失败返回 False
    
    Examples:
        >>> clear_clipboard()
    """
    platform = _get_platform()
    
    try:
        if platform == 'windows':
            # Windows: use powershell to clear clipboard
            returncode, _, _ = _run_subprocess(
                ['powershell', '-command', 'Set-Clipboard -Value $null']
            )
            return returncode == 0
            
        elif platform == 'macos':
            # macOS: pipe empty string to pbcopy
            returncode, _, _ = _run_subprocess(['pbcopy'], input_data='')
            return returncode == 0
            
        elif platform == 'linux':
            # Linux: try to clear or copy empty string
            linux_commands = [
                ['xclip', '-selection', 'clipboard', '/dev/null'],
                ['xsel', '--clipboard', '--clear'],
                ['wl-copy', '--clear']
            ]
            
            for cmd in linux_commands:
                returncode, _, _ = _run_subprocess(cmd)
                if returncode == 0:
                    return True
            
            # Fallback: copy empty string
            returncode, _, _ = _run_subprocess(
                ['xclip', '-selection', 'clipboard'],
                input_data=''
            )
            return returncode == 0
        else:
            return False
            
    except (OSError, IOError):
        return False


def copy_file_path(filepath: str) -> bool:
    """
    复制文件路径到剪贴板
    
    功能：将文件的绝对路径复制到剪贴板，方便快速分享或粘贴文件位置。
    自动解析相对路径为绝对路径。
    
    Args:
        filepath: 文件路径（支持相对路径和绝对路径）
    
    Returns:
        操作成功返回 True，失败返回 False
    
    Examples:
        >>> copy_file_path('document.pdf')
        >>> copy_file_path('/home/user/data/config.json')
    """
    try:
        # Convert to absolute path
        abs_path = str(Path(filepath).resolve())
        return copy_text(abs_path)
    except (OSError, ValueError):
        return False


def copy_files_list(filepaths: List[str], separator: str = '\n') -> bool:
    """
    复制多个文件路径到剪贴板
    
    功能：将多个文件路径以指定分隔符连接后复制到剪贴板。
    适用于批量分享文件列表场景。
    
    Args:
        filepaths: 文件路径列表
        separator: 路径之间的分隔符，默认为换行符
    
    Returns:
        操作成功返回 True，失败返回 False
    
    Examples:
        >>> copy_files_list(['file1.txt', 'file2.txt', 'file3.txt'])
        >>> copy_files_list(['a.py', 'b.py'], separator=', ')
    """
    try:
        abs_paths = [str(Path(fp).resolve()) for fp in filepaths]
        content = separator.join(abs_paths)
        return copy_text(content)
    except (OSError, ValueError):
        return False


def get_clipboard_history(max_items: int = 10) -> List[str]:
    """
    获取剪贴板历史（如果系统支持）
    
    功能：尝试获取剪贴板历史记录（仅 macOS 支持原生历史）。
    其他平台返回当前剪贴板内容的单元素列表。
    
    Args:
        max_items: 最大返回项目数，默认为 10
    
    Returns:
        剪贴板历史列表，不支持则返回当前内容
    
    Examples:
        >>> history = get_clipboard_history()
        >>> for item in history:
        ...     print(item)
    """
    platform = _get_platform()
    
    try:
        if platform == 'macos':
            # macOS: try to access clipboard history via defaults
            # Note: This is limited, macOS doesn't expose full history easily
            pass
        
        # Default: return current clipboard content as single-item list
        current = paste_text()
        if current:
            return [current]
        return []
        
    except (OSError, IOError):
        return []


def is_clipboard_available() -> bool:
    """
    检测剪贴板是否可用
    
    功能：检测当前系统是否有可用的剪贴板工具。
    可用于在操作前预检查环境支持。
    
    Returns:
        剪贴板可用返回 True，否则返回 False
    
    Examples:
        >>> if is_clipboard_available():
        ...     copy_text("Hello")
        ... else:
        ...     print("剪贴板不可用")
    """
    platform = _get_platform()
    
    if platform == 'windows':
        # Windows always has clip.exe
        return True
        
    elif platform == 'macos':
        # macOS always has pbcopy/pbpaste
        return True
        
    elif platform == 'linux':
        # Linux: check for common clipboard tools
        linux_commands = ['xclip', 'xsel', 'wl-copy', 'wl-paste']
        
        for cmd in linux_commands:
            returncode, _, _ = _run_subprocess([cmd, '--version'], capture=True)
            if returncode == 0:
                return True
        
        return False
    else:
        return False


def get_platform_info() -> dict:
    """
    获取剪贴板平台信息
    
    功能：返回当前系统的剪贴板相关信息，包括平台类型和可用工具。
    
    Returns:
        包含平台信息的字典
    
    Examples:
        >>> info = get_platform_info()
        >>> print(f"平台：{info['platform']}")
        >>> print(f"可用：{info['available']}")
    """
    platform = _get_platform()
    available = is_clipboard_available()
    
    tool_info = {
        'windows': 'clip.exe / PowerShell',
        'macos': 'pbcopy / pbpaste',
        'linux': 'xclip / xsel / wl-clipboard',
        'unknown': 'None'
    }
    
    return {
        'platform': platform,
        'available': available,
        'tools': tool_info.get(platform, 'Unknown'),
        'sys_platform': sys.platform
    }
