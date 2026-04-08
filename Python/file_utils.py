"""
File Utilities Module
通用文件处理工具函数库

提供常用的文件操作功能，包括安全读写、路径处理、文件类型检测等。
所有函数均为纯函数设计，无外部依赖，可直接复用。

Author: AllToolkit
Version: 1.0.0
"""

import os
import hashlib
import shutil
from pathlib import Path
from typing import Union, Optional, List


PathLike = Union[str, Path]


def safe_read_text(filepath: PathLike, encoding: str = 'utf-8', default: Optional[str] = None) -> Optional[str]:
    """
    安全读取文本文件内容
    
    功能：以安全方式读取文本文件，自动处理文件不存在、权限错误等异常情况。
    
    Args:
        filepath: 文件路径，支持 str 或 Path 对象
        encoding: 文件编码，默认为 'utf-8'
        default: 读取失败时返回的默认值，默认为 None
    
    Returns:
        文件内容字符串，读取失败时返回 default 值
    
    Examples:
        >>> content = safe_read_text('config.json')
        >>> content = safe_read_text('data.txt', encoding='gbk', default='')
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, IOError):
        return default


def safe_write_text(filepath: PathLike, content: str, encoding: str = 'utf-8', 
                    create_dirs: bool = True, atomic: bool = False) -> bool:
    """
    安全写入文本文件内容
    
    功能：以安全方式写入文本文件，支持自动创建目录和原子写入。
    
    Args:
        filepath: 文件路径，支持 str 或 Path 对象
        content: 要写入的文本内容
        encoding: 文件编码，默认为 'utf-8'
        create_dirs: 是否自动创建父目录，默认为 True
        atomic: 是否使用原子写入（先写临时文件再重命名），默认为 False
    
    Returns:
        写入成功返回 True，失败返回 False
    
    Examples:
        >>> safe_write_text('output.txt', 'Hello World')
        >>> safe_write_text('data/config.json', json_data, atomic=True)
    """
    try:
        path = Path(filepath)
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        if atomic:
            temp_path = path.with_suffix(path.suffix + '.tmp')
            try:
                with open(temp_path, 'w', encoding=encoding) as f:
                    f.write(content)
                temp_path.replace(path)
            except Exception:
                if temp_path.exists():
                    temp_path.unlink(missing_ok=True)
                raise
        else:
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
        return True
    except (PermissionError, IOError, OSError):
        return False


def get_file_hash(filepath: PathLike, algorithm: str = 'md5', chunk_size: int = 8192) -> Optional[str]:
    """
    计算文件哈希值
    
    功能：计算文件的哈希值，支持大文件分块读取，内存友好。
    
    Args:
        filepath: 文件路径，支持 str 或 Path 对象
        algorithm: 哈希算法，可选 'md5', 'sha1', 'sha256', 'sha512'，默认为 'md5'
        chunk_size: 分块读取大小（字节），默认为 8192
    
    Returns:
        文件哈希值字符串（小写十六进制），失败返回 None
    
    Examples:
        >>> hash_md5 = get_file_hash('document.pdf')
        >>> hash_sha256 = get_file_hash('installer.exe', algorithm='sha256')
    """
    hash_algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
    if algorithm not in hash_algorithms:
        return None
    
    try:
        hasher = hash_algorithms[algorithm]()
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except (FileNotFoundError, PermissionError, IOError):
        return None


def get_file_size(filepath: PathLike, human_readable: bool = False, decimal_places: int = 2) -> Union[int, str, None]:
    """
    获取文件大小
    
    功能：获取文件大小，支持返回原始字节数或人类可读格式。
    
    Args:
        filepath: 文件路径，支持 str 或 Path 对象
        human_readable: 是否返回人类可读格式（如 '1.5 MB'），默认为 False
        decimal_places: 小数位数，默认为 2
    
    Returns:
        文件大小（字节整数或格式化字符串），失败返回 None
    
    Examples:
        >>> size = get_file_size('video.mp4')  # 返回: 15728640
        >>> size = get_file_size('video.mp4', human_readable=True)  # 返回: '15.0 MB'
    """
    try:
        size = os.path.getsize(filepath)
        if not human_readable:
            return size
        
        # Handle zero size edge case
        if size == 0:
            return "0 B"
        
        # Handle negative size (shouldn't happen but be defensive)
        if size < 0:
            return None
        
        # Optimized: Use logarithm for O(1) unit selection
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
        
        # Calculate appropriate unit using logarithm
        # Avoid log(0) as we already handled size == 0
        import math
        unit_index = min(int(math.log2(size) / 10), len(units) - 1)
        
        # Calculate final value with proper division
        divisor = 1024.0 ** unit_index
        size_float = size / divisor
        
        # Format based on magnitude for cleaner output
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        
        # Dynamic precision based on value magnitude
        if size_float >= 100:
            fmt = f"{{:.0f}} {units[unit_index]}"
        elif size_float >= 10:
            fmt = f"{{:.1f}} {units[unit_index]}"
        else:
            fmt = f"{{:.{decimal_places}f}} {units[unit_index]}"
        
        return fmt.format(size_float)
    except (FileNotFoundError, PermissionError, OSError, OverflowError, ValueError):
        return None


def ensure_dir(directory: PathLike, mode: int = 0o755) -> bool:
    """
    确保目录存在
    
    功能：检查目录是否存在，不存在则创建，支持设置权限模式。
    
    Args:
        directory: 目录路径，支持 str 或 Path 对象
        mode: 目录权限模式（八进制），默认为 0o755
    
    Returns:
        目录已存在或创建成功返回 True，失败返回 False
    
    Examples:
        >>> ensure_dir('/tmp/myapp/logs')
        >>> ensure_dir('data/cache', mode=0o700)
    """
    try:
        path = Path(directory)
        if path.exists():
            # Check if it's actually a directory (not a file)
            return path.is_dir()
        
        # Create directory with parents, handle race condition
        path.mkdir(parents=True, exist_ok=True, mode=mode)
        
        # Verify creation succeeded
        return path.exists() and path.is_dir()
    except (PermissionError, OSError, FileExistsError):
        # FileExistsError: path exists but is a file
        return False


def list_files(directory: PathLike, pattern: str = '*', recursive: bool = False,
               include_dirs: bool = False, sort_by: str = 'name') -> List[Path]:
    """
    列出目录中的文件
    
    功能：列出目录中的文件，支持通配符匹配、递归遍历和排序。
    
    Args:
        directory: 目录路径，支持 str 或 Path 对象
        pattern: 文件名匹配模式，支持通配符，默认为 '*'（所有文件）
        recursive: 是否递归遍历子目录，默认为 False
        include_dirs: 结果是否包含目录，默认为 False
        sort_by: 排序方式，可选 'name', 'size', 'mtime'，默认为 'name'
    
    Returns:
        Path 对象列表，失败返回空列表
    
    Examples:
        >>> files = list_files('/home/user/docs', pattern='*.pdf')
        >>> files = list_files('src', recursive=True, sort_by='mtime')
    """
    try:
        path = Path(directory)
        if not path.is_dir():
            return []
        
        # Validate sort_by parameter
        valid_sort_options = {'name', 'size', 'mtime'}
        if sort_by not in valid_sort_options:
            sort_by = 'name'
        
        if recursive:
            items = list(path.rglob(pattern))
        else:
            items = list(path.glob(pattern))
        
        if not include_dirs:
            items = [f for f in items if f.is_file()]
        
        # Optimized sorting with cached stat calls for size/mtime
        if sort_by == 'name':
            items.sort(key=lambda x: x.name.lower())
        elif sort_by == 'size':
            # Cache stat results to avoid multiple system calls
            items.sort(key=lambda x: x.stat().st_size if x.exists() else 0)
        elif sort_by == 'mtime':
            items.sort(key=lambda x: x.stat().st_mtime if x.exists() else 0, reverse=True)
        
        return items
    except (PermissionError, OSError):
        return []


def copy_file(src: PathLike, dst: PathLike, overwrite: bool = False, 
              preserve_metadata: bool = True) -> bool:
    """
    复制文件
    
    功能：安全复制文件，支持覆盖控制和元数据保留。
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
        overwrite: 是否覆盖已存在的目标文件，默认为 False
        preserve_metadata: 是否保留文件元数据（时间戳、权限等），默认为 True
    
    Returns:
        复制成功返回 True，失败返回 False
    
    Examples:
        >>> copy_file('source.txt', 'backup/source.txt')
        >>> copy_file('data.json', 'data.json.bak', overwrite=True)
    """
    try:
        src_path = Path(src)
        dst_path = Path(dst)
        
        if not src_path.is_file():
            return False
        if dst_path.exists() and not overwrite:
            return False
        
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        if preserve_metadata:
            shutil.copy2(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
        return True
    except (PermissionError, OSError, IOError):
        return False


def move_file(src: PathLike, dst: PathLike, overwrite: bool = False) -> bool:
    """
    移动文件或目录
    
    功能：安全移动文件或目录，支持覆盖控制。
    
    Args:
        src: 源路径
        dst: 目标路径
        overwrite: 是否覆盖已存在的目标，默认为 False
    
    Returns:
        移动成功返回 True，失败返回 False
    
    Examples:
        >>> move_file('temp.txt', 'archive/temp.txt')
        >>> move_file('old_name.txt', 'new_name.txt', overwrite=True)
    """
    try:
        src_path = Path(src)
        dst_path = Path(dst)
        
        if not src_path.exists():
            return False
        if dst_path.exists() and not overwrite:
            return False
        
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dst_path))
        return True
    except (PermissionError, OSError, IOError):
        return False


def delete_file(filepath: PathLike, missing_ok: bool = True) -> bool:
    """
    删除文件
    
    功能：安全删除文件，支持忽略不存在的情况。
    
    Args:
        filepath: 文件路径
        missing_ok: 文件不存在时是否视为成功，默认为 True
    
    Returns:
        删除成功返回 True，失败返回 False
    
    Examples:
        >>> delete_file('temp.txt')
        >>> delete_file('cache.tmp', missing_ok=False)
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return missing_ok
        if not path.is_file():
            return False
        path.unlink()
        return True
    except (PermissionError, OSError, IOError):
        return False


def get_unique_filename(filepath: PathLike, suffix_format: str = '_{}') -> Path:
    """
    获取唯一文件名
    
    功能：当目标文件已存在时，自动生成带序号的唯一文件名。
    
    Args:
        filepath: 原始文件路径
        suffix_format: 序号格式化字符串，默认为 '_{}'
    
    Returns:
        唯一的文件路径（Path 对象）
    
    Examples:
        >>> get_unique_filename('report.pdf')  # 如果存在返回 'report_1.pdf'
        >>> get_unique_filename('data.txt', suffix_format='({})')  # 返回 'data(1).txt'
    """
    path = Path(filepath)
    if not path.exists():
        return path
    
    parent = path.parent
    stem = path.stem
    suffix = path.suffix
    counter = 1
    
    while True:
        new_name = f"{stem}{suffix_format.format(counter)}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1
