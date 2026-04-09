# -*- coding: utf-8 -*-
"""
AllToolkit - Shell Utilities 🐚

零依赖 Shell 命令执行与系统操作工具库。
完全使用 Python 标准库实现（subprocess, os, pathlib, shutil, sys, platform），无需任何外部依赖。

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

import subprocess
import os
import sys
import shutil
import platform
import time
import signal
import tempfile
import stat
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union, List, Callable
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# 常量定义
# =============================================================================

DEFAULT_ENCODING = 'utf-8'
DEFAULT_TIMEOUT = 30  # 默认超时时间（秒）


# =============================================================================
# 枚举与数据类
# =============================================================================

class OSType(Enum):
    """操作系统类型"""
    LINUX = 'linux'
    MACOS = 'macos'
    WINDOWS = 'windows'
    FREEBSD = 'freebsd'
    OTHER = 'other'


@dataclass
class CommandResult:
    """命令执行结果"""
    returncode: int
    stdout: str
    stderr: str
    command: str
    duration: float
    success: bool
    
    def __bool__(self) -> bool:
        return self.success
    
    def __str__(self) -> str:
        status = "✓" if self.success else "✗"
        return f"{status} {self.command} ({self.duration:.2f}s)"


@dataclass
class ProcessInfo:
    """进程信息"""
    pid: int
    name: str
    status: str
    cpu_percent: float
    memory_percent: float
    username: str


# =============================================================================
# 系统信息工具
# =============================================================================

def get_os_type() -> OSType:
    """
    获取操作系统类型
    
    Returns:
        OSType 枚举值
    
    Example:
        >>> get_os_type()
        <OSType.LINUX: 'linux'>
    """
    system = platform.system().lower()
    if 'linux' in system:
        return OSType.LINUX
    elif 'darwin' in system:
        return OSType.MACOS
    elif 'windows' in system:
        return OSType.WINDOWS
    elif 'freebsd' in system:
        return OSType.FREEBSD
    return OSType.OTHER


def is_windows() -> bool:
    """检查是否为 Windows 系统"""
    return get_os_type() == OSType.WINDOWS


def is_unix() -> bool:
    """检查是否为 Unix-like 系统"""
    return get_os_type() in [OSType.LINUX, OSType.MACOS, OSType.FREEBSD]


def get_shell() -> str:
    """
    获取当前系统的默认 Shell
    
    Returns:
        Shell 路径
    """
    if is_windows():
        return os.environ.get('COMSPEC', 'cmd.exe')
    return os.environ.get('SHELL', '/bin/bash')


def get_platform_info() -> Dict[str, Any]:
    """
    获取平台详细信息
    
    Returns:
        包含平台信息的字典
    
    Example:
        >>> info = get_platform_info()
        >>> print(info['os'])
        linux
    """
    return {
        'os': get_os_type().value,
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'architecture': platform.architecture()[0],
    }


# =============================================================================
# 命令执行核心函数
# =============================================================================

def run_command(
    command: Union[str, List[str]],
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = DEFAULT_TIMEOUT,
    shell: Optional[bool] = None,
    capture_output: bool = True,
    text: bool = True,
    encoding: str = DEFAULT_ENCODING,
    check: bool = False,
    stdin_input: Optional[str] = None,
) -> CommandResult:
    """
    执行 Shell 命令
    
    Args:
        command: 命令（字符串或列表）
        cwd: 工作目录
        env: 环境变量
        timeout: 超时时间（秒）
        shell: 是否使用 shell 执行（None 表示自动检测）
        capture_output: 是否捕获输出
        text: 是否以文本模式返回
        encoding: 编码格式
        check: 是否检查返回码（非零则抛异常）
        stdin_input: 标准输入内容
    
    Returns:
        CommandResult 对象
    
    Example:
        >>> result = run_command('ls -la')
        >>> print(result.stdout)
        
        >>> result = run_command(['echo', 'hello'])
        >>> print(result.stdout)
        hello
    """
    # 自动检测 shell 参数
    if shell is None:
        shell = isinstance(command, str)
    
    start_time = time.time()
    
    try:
        # Python 3.6 兼容性：不使用 capture_output 参数
        # 准备 subprocess 参数
        kwargs = {
            'cwd': cwd,
            'env': env,
            'shell': shell,
        }
        
        if capture_output:
            kwargs['stdout'] = subprocess.PIPE
            kwargs['stderr'] = subprocess.PIPE
        
        if text:
            # Python 3.6 使用 universal_newlines 而不是 text
            kwargs['universal_newlines'] = True
            if encoding:
                kwargs['encoding'] = encoding
        
        # 执行命令
        if stdin_input is not None:
            # Python 3.6: input 参数会自动处理 stdin，不需要显式设置 stdin=PIPE
            proc = subprocess.run(command, input=stdin_input, **kwargs)
        else:
            proc = subprocess.run(command, **kwargs)
        
        duration = time.time() - start_time
        
        return CommandResult(
            returncode=proc.returncode,
            stdout=proc.stdout if capture_output else '',
            stderr=proc.stderr if capture_output else '',
            command=command if isinstance(command, str) else ' '.join(command),
            duration=duration,
            success=proc.returncode == 0,
        )
        
    except subprocess.TimeoutExpired as e:
        duration = time.time() - start_time
        return CommandResult(
            returncode=-1,
            stdout=e.stdout.decode(encoding) if e.stdout and capture_output else '',
            stderr=f'Timeout after {timeout}s',
            command=command if isinstance(command, str) else ' '.join(command),
            duration=duration,
            success=False,
        )
    except Exception as e:
        duration = time.time() - start_time
        return CommandResult(
            returncode=-1,
            stdout='',
            stderr=str(e),
            command=command if isinstance(command, str) else ' '.join(command),
            duration=duration,
            success=False,
        )


def run_command_checked(
    command: Union[str, List[str]],
    **kwargs
) -> CommandResult:
    """
    执行命令并检查返回码（非零则抛异常）
    
    Args:
        command: 命令
        **kwargs: 传递给 run_command 的参数
    
    Returns:
        CommandResult 对象
    
    Raises:
        RuntimeError: 命令执行失败
    """
    kwargs['check'] = True
    result = run_command(command, **kwargs)
    
    if not result.success:
        raise RuntimeError(
            f"命令执行失败：{result.command}\n"
            f"返回码：{result.returncode}\n"
            f"错误：{result.stderr}"
        )
    
    return result


def run_command_async(
    command: Union[str, List[str]],
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    shell: Optional[bool] = None,
) -> subprocess.Popen:
    """
    异步执行命令（非阻塞）
    
    Args:
        command: 命令
        cwd: 工作目录
        env: 环境变量
        shell: 是否使用 shell
    
    Returns:
        Popen 对象
    
    Example:
        >>> proc = run_command_async('sleep 10')
        >>> proc.pid
        12345
        >>> proc.terminate()
    """
    if shell is None:
        shell = isinstance(command, str)
    
    return subprocess.Popen(
        command,
        shell=shell,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


# =============================================================================
# 进程管理
# =============================================================================

def kill_process(pid: int, signal_num: int = signal.SIGTERM) -> bool:
    """
    终止进程
    
    Args:
        pid: 进程 ID
        signal_num: 信号类型
    
    Returns:
        是否成功
    """
    try:
        os.kill(pid, signal_num)
        return True
    except (OSError, ProcessLookupError):
        return False


def process_exists(pid: int) -> bool:
    """
    检查进程是否存在
    
    Args:
        pid: 进程 ID
    
    Returns:
        是否存在
    """
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def get_process_count() -> int:
    """
    获取当前系统进程数量
    
    Returns:
        进程数量
    """
    if is_windows():
        result = run_command('tasklist /fo csv')
        if result.success:
            # CSV 格式，减去标题行
            return len(result.stdout.strip().split('\n')) - 1
    else:
        result = run_command('ps aux')
        if result.success:
            # 减去标题行
            return len(result.stdout.strip().split('\n')) - 1
    return -1


def find_processes_by_name(name: str) -> List[int]:
    """
    根据名称查找进程 PID
    
    Args:
        name: 进程名称
    
    Returns:
        PID 列表
    """
    pids = []
    
    if is_windows():
        result = run_command(f'tasklist /fi "IMAGENAME eq {name}" /fo csv')
        if result.success:
            lines = result.stdout.strip().split('\n')[1:]  # 跳过标题
            for line in lines:
                parts = line.split(',')
                if len(parts) >= 2:
                    try:
                        pids.append(int(parts[1].strip('"')))
                    except ValueError:
                        pass
    else:
        result = run_command(f'pgrep -f {name}')
        if result.success:
            for line in result.stdout.strip().split('\n'):
                try:
                    pids.append(int(line.strip()))
                except ValueError:
                    pass
    
    return pids


# =============================================================================
# 文件与路径操作
# =============================================================================

def which(command: str) -> Optional[str]:
    """
    查找命令的完整路径
    
    Args:
        command: 命令名称
    
    Returns:
        完整路径或 None
    """
    return shutil.which(command)


def command_exists(command: str) -> bool:
    """
    检查命令是否存在
    
    Args:
        command: 命令名称
    
    Returns:
        是否存在
    """
    return which(command) is not None


def get_current_directory() -> str:
    """获取当前工作目录"""
    return os.getcwd()


def change_directory(path: str) -> bool:
    """
    切换工作目录
    
    Args:
        path: 目标目录
    
    Returns:
        是否成功
    """
    try:
        os.chdir(path)
        return True
    except (OSError, FileNotFoundError):
        return False


def create_directory(path: str, parents: bool = True, exist_ok: bool = True) -> bool:
    """
    创建目录
    
    Args:
        path: 目录路径
        parents: 是否创建父目录
        exist_ok: 如果目录已存在是否不报错
    
    Returns:
        是否成功
    """
    try:
        Path(path).mkdir(parents=parents, exist_ok=exist_ok)
        return True
    except Exception:
        return False


def remove_directory(path: str, recursive: bool = True) -> bool:
    """
    删除目录
    
    Args:
        path: 目录路径
        recursive: 是否递归删除
    
    Returns:
        是否成功
    """
    try:
        if recursive:
            shutil.rmtree(path)
        else:
            os.rmdir(path)
        return True
    except Exception:
        return False


def file_exists(path: str) -> bool:
    """检查文件是否存在"""
    return os.path.isfile(path)


def directory_exists(path: str) -> bool:
    """检查目录是否存在"""
    return os.path.isdir(path)


def get_file_size(path: str) -> int:
    """
    获取文件大小（字节）
    
    Args:
        path: 文件路径
    
    Returns:
        文件大小，失败返回 -1
    """
    try:
        return os.path.getsize(path)
    except Exception:
        return -1


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
    
    Returns:
        格式化字符串（如 "1.5 MB"）
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def copy_file(src: str, dst: str) -> bool:
    """复制文件"""
    try:
        shutil.copy2(src, dst)
        return True
    except Exception:
        return False


def move_file(src: str, dst: str) -> bool:
    """移动文件"""
    try:
        shutil.move(src, dst)
        return True
    except Exception:
        return False


def delete_file(path: str) -> bool:
    """删除文件"""
    try:
        os.remove(path)
        return True
    except Exception:
        return False


# =============================================================================
# 环境变量
# =============================================================================

def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """获取环境变量"""
    return os.environ.get(name, default)


def set_env_var(name: str, value: str) -> bool:
    """
    设置环境变量（仅当前进程）
    
    Args:
        name: 变量名
        value: 变量值
    
    Returns:
        是否成功
    """
    try:
        os.environ[name] = value
        return True
    except Exception:
        return False


def get_all_env_vars() -> Dict[str, str]:
    """获取所有环境变量"""
    return dict(os.environ)


def load_env_file(path: str) -> Dict[str, str]:
    """
    从 .env 文件加载环境变量
    
    Args:
        path: .env 文件路径
    
    Returns:
        环境变量字典
    """
    env_vars = {}
    
    try:
        with open(path, 'r', encoding=DEFAULT_ENCODING) as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                
                # 解析 KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 处理引号
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    env_vars[key] = value
    except Exception:
        pass
    
    return env_vars


# =============================================================================
# 系统操作
# =============================================================================

def get_hostname() -> str:
    """获取主机名"""
    return platform.node()


def get_username() -> str:
    """获取当前用户名"""
    return get_env_var('USERNAME') or get_env_var('USER') or 'unknown'


def get_home_directory() -> str:
    """获取用户主目录"""
    return os.path.expanduser('~')


def get_temp_directory() -> str:
    """获取临时目录"""
    return tempfile.gettempdir()


def create_temp_file(
    suffix: str = '',
    prefix: str = 'tmp',
    dir: Optional[str] = None,
    text: bool = True,
) -> Tuple[str, int]:
    """
    创建临时文件
    
    Args:
        suffix: 文件后缀
        prefix: 文件前缀
        dir: 目录
        text: 是否文本模式
    
    Returns:
        (文件路径，文件描述符)
    """
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir, text=text)
    return path, fd


def create_temp_directory(
    suffix: str = '',
    prefix: str = 'tmp',
    dir: Optional[str] = None,
) -> str:
    """
    创建临时目录
    
    Args:
        suffix: 目录后缀
        prefix: 目录前缀
        dir: 父目录
    
    Returns:
        目录路径
    """
    return tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)


def get_disk_usage(path: str = '/') -> Dict[str, Any]:
    """
    获取磁盘使用情况
    
    Args:
        path: 路径
    
    Returns:
        包含 total, used, free, percent 的字典
    """
    try:
        usage = shutil.disk_usage(path)
        percent = (usage.used / usage.total) * 100 if usage.total > 0 else 0
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': round(percent, 2),
        }
    except Exception:
        return {'total': 0, 'used': 0, 'free': 0, 'percent': 0}


def get_memory_info() -> Dict[str, Any]:
    """
    获取内存信息
    
    Returns:
        内存信息字典
    """
    info = {'total': 0, 'available': 0, 'used': 0, 'percent': 0}
    
    if is_windows():
        import ctypes
        kernel32 = ctypes.windll.kernel32
        c_ulonglong = ctypes.c_ulonglong
        
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ('dwLength', ctypes.c_ulong),
                ('dwMemoryLoad', ctypes.c_ulong),
                ('dwTotalPhys', c_ulonglong),
                ('dwAvailPhys', c_ulonglong),
                ('dwTotalPageFile', c_ulonglong),
                ('dwAvailPageFile', c_ulonglong),
                ('dwTotalVirtual', c_ulonglong),
                ('dwAvailVirtual', c_ulonglong),
            ]
        
        memory = MEMORYSTATUS()
        memory.dwLength = ctypes.sizeof(memory)
        kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
        
        info['total'] = memory.dwTotalPhys
        info['available'] = memory.dwAvailPhys
        info['used'] = memory.dwTotalPhys - memory.dwAvailPhys
        info['percent'] = memory.dwMemoryLoad
        
    elif is_unix():
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = {}
                for line in f:
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = int(parts[1].strip().split()[0]) * 1024  # KB to bytes
                        meminfo[key] = value
                
                info['total'] = meminfo.get('MemTotal', 0)
                info['available'] = meminfo.get('MemAvailable', meminfo.get('MemFree', 0))
                info['used'] = info['total'] - info['available']
                info['percent'] = round((info['used'] / info['total']) * 100, 2) if info['total'] > 0 else 0
        except Exception:
            pass
    
    return info


# =============================================================================
# 网络工具
# =============================================================================

def ping(host: str, count: int = 4, timeout: int = 5) -> Dict[str, Any]:
    """
    Ping 主机
    
    Args:
        host: 主机名或 IP
        count: 次数
        timeout: 超时时间
    
    Returns:
        包含成功状态的字典
    """
    if is_windows():
        command = f'ping -n {count} -w {timeout * 1000} {host}'
    else:
        command = f'ping -c {count} -W {timeout} {host}'
    
    result = run_command(command)
    
    return {
        'success': result.success,
        'stdout': result.stdout,
        'stderr': result.stderr,
    }


def get_local_ip() -> str:
    """
    获取本地 IP 地址
    
    Returns:
        IP 地址
    """
    import socket
    
    try:
        # 创建一个临时 socket 连接来获取 IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def get_public_ip() -> str:
    """
    获取公网 IP 地址
    
    Returns:
        公网 IP 地址
    """
    services = [
        'https://api.ipify.org',
        'https://ifconfig.me',
        'https://icanhazip.com',
    ]
    
    for service in services:
        try:
            # 使用 curl 获取
            if command_exists('curl'):
                result = run_command(f'curl -s {service}', timeout=5)
                if result.success:
                    return result.stdout.strip()
            # 使用 wget 获取
            elif command_exists('wget'):
                result = run_command(f'wget -qO- {service}', timeout=5)
                if result.success:
                    return result.stdout.strip()
        except Exception:
            continue
    
    return 'unknown'


# =============================================================================
# 快捷命令
# =============================================================================

def ls(path: str = '.', args: str = '') -> CommandResult:
    """列出目录内容"""
    return run_command(f'ls {args} {path}')


def pwd() -> str:
    """获取当前目录"""
    return get_current_directory()


def echo(text: str) -> CommandResult:
    """输出文本"""
    return run_command(['echo', text])


def cat(file_path: str) -> CommandResult:
    """读取文件内容"""
    return run_command(['cat', file_path])


def grep(pattern: str, file_path: str, args: str = '') -> CommandResult:
    """搜索文件内容"""
    return run_command(f'grep {args} "{pattern}" {file_path}')


def find_files(
    path: str = '.',
    name_pattern: str = '*',
    type_filter: Optional[str] = None,
    max_depth: Optional[int] = None,
) -> List[str]:
    """
    查找文件
    
    Args:
        path: 搜索路径
        name_pattern: 名称模式
        type_filter: 类型过滤 (f=文件，d=目录)
        max_depth: 最大深度
    
    Returns:
        文件路径列表
    """
    cmd_parts = ['find', path]
    
    if max_depth is not None:
        cmd_parts.extend(['-maxdepth', str(max_depth)])
    
    if type_filter:
        cmd_parts.extend(['-type', type_filter])
    
    cmd_parts.extend(['-name', name_pattern])
    
    result = run_command(' '.join(cmd_parts))
    
    if result.success:
        return [p.strip() for p in result.stdout.strip().split('\n') if p.strip()]
    return []


def chmod(path: str, mode: Union[str, int]) -> bool:
    """
    修改文件权限（仅 Unix）
    
    Args:
        path: 文件路径
        mode: 权限模式（如 '755' 或 0o755）
    
    Returns:
        是否成功
    """
    if is_windows():
        return False
    
    try:
        if isinstance(mode, str):
            mode = int(mode, 8)
        os.chmod(path, mode)
        return True
    except Exception:
        return False


def mkdir_p(path: str) -> bool:
    """创建目录（包括父目录）"""
    return create_directory(path, parents=True, exist_ok=True)


def rm_rf(path: str) -> bool:
    """递归删除文件或目录"""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    except Exception:
        return False


def cp(src: str, dst: str, recursive: bool = False) -> bool:
    """复制文件或目录"""
    try:
        if recursive:
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
        return True
    except Exception:
        return False


def mv(src: str, dst: str) -> bool:
    """移动文件或目录"""
    return move_file(src, dst)


# =============================================================================
# 批处理与管道
# =============================================================================

def run_commands_sequential(
    commands: List[Union[str, List[str]]],
    stop_on_error: bool = True,
    **kwargs
) -> List[CommandResult]:
    """
    顺序执行多个命令
    
    Args:
        commands: 命令列表
        stop_on_error: 出错时是否停止
        **kwargs: 传递给 run_command 的参数
    
    Returns:
        结果列表
    """
    results = []
    
    for command in commands:
        result = run_command(command, **kwargs)
        results.append(result)
        
        if stop_on_error and not result.success:
            break
    
    return results


def run_commands_parallel(
    commands: List[Union[str, List[str]]],
    max_workers: int = 4,
    **kwargs
) -> List[CommandResult]:
    """
    并行执行多个命令
    
    Args:
        commands: 命令列表
        max_workers: 最大并发数
        **kwargs: 传递给 run_command_async 的参数
    
    Returns:
        结果列表
    """
    import concurrent.futures
    
    results = []
    
    def execute(cmd):
        return run_command(cmd, **kwargs)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(execute, cmd) for cmd in commands]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    return results


def pipe_commands(commands: List[str]) -> CommandResult:
    """
    管道执行多个命令
    
    Args:
        commands: 命令列表
    
    Returns:
        最终结果
    
    Example:
        >>> pipe_commands(['ls -la', 'grep .py', 'wc -l'])
    """
    if is_windows():
        pipe_char = '|'
    else:
        pipe_char = '|'
    
    full_command = f' {pipe_char} '.join(commands)
    return run_command(full_command, shell=True)


# =============================================================================
# 导出所有公共 API
# =============================================================================

__all__ = [
    # 枚举与数据类
    'OSType',
    'CommandResult',
    'ProcessInfo',
    
    # 系统信息
    'get_os_type',
    'is_windows',
    'is_unix',
    'get_shell',
    'get_platform_info',
    
    # 命令执行
    'run_command',
    'run_command_checked',
    'run_command_async',
    
    # 进程管理
    'kill_process',
    'process_exists',
    'get_process_count',
    'find_processes_by_name',
    
    # 文件与路径
    'which',
    'command_exists',
    'get_current_directory',
    'change_directory',
    'create_directory',
    'remove_directory',
    'file_exists',
    'directory_exists',
    'get_file_size',
    'format_file_size',
    'copy_file',
    'move_file',
    'delete_file',
    
    # 环境变量
    'get_env_var',
    'set_env_var',
    'get_all_env_vars',
    'load_env_file',
    
    # 系统操作
    'get_hostname',
    'get_username',
    'get_home_directory',
    'get_temp_directory',
    'create_temp_file',
    'create_temp_directory',
    'get_disk_usage',
    'get_memory_info',
    
    # 网络工具
    'ping',
    'get_local_ip',
    'get_public_ip',
    
    # 快捷命令
    'ls',
    'pwd',
    'echo',
    'cat',
    'grep',
    'find_files',
    'chmod',
    'mkdir_p',
    'rm_rf',
    'cp',
    'mv',
    
    # 批处理
    'run_commands_sequential',
    'run_commands_parallel',
    'pipe_commands',
    
    # 常量
    'DEFAULT_ENCODING',
    'DEFAULT_TIMEOUT',
]
