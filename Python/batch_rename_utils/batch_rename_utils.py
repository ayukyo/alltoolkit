"""
Batch Rename Utilities Module
批量文件重命名工具库

提供多种批量重命名策略，包括序号命名、前缀后缀、正则替换、大小写转换等。
所有功能均为纯 Python 标准库实现，零外部依赖。

Author: AllToolkit
Version: 1.0.0
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Union, List, Tuple, Optional, Callable, Dict


PathLike = Union[str, Path]


class RenameResult:
    """重命名结果类"""
    
    def __init__(self, success: bool, old_path: Path, new_path: Path, error: Optional[str] = None):
        self.success = success
        self.old_path = old_path
        self.new_path = new_path
        self.error = error
    
    def __repr__(self) -> str:
        if self.success:
            return f"RenameResult(success=True, '{self.old_path.name}' -> '{self.new_path.name}')"
        return f"RenameResult(success=False, error='{self.error}')"


class RenamePreview:
    """重命名预览类"""
    
    def __init__(self, old_path: Path, new_path: Path):
        self.old_path = old_path
        self.new_path = new_path
    
    @property
    def old_name(self) -> str:
        return self.old_path.name
    
    @property
    def new_name(self) -> str:
        return self.new_path.name
    
    def __repr__(self) -> str:
        return f"'{self.old_name}' -> '{self.new_name}'"


def _validate_paths(paths: List[PathLike]) -> List[Path]:
    """验证并转换路径列表"""
    return [Path(p) for p in paths]


def _get_unique_path(target_path: Path, existing_paths: set) -> Path:
    """获取唯一路径，避免冲突"""
    if target_path not in existing_paths:
        return target_path
    
    parent = target_path.parent
    stem = target_path.stem
    suffix = target_path.suffix
    
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if new_path not in existing_paths:
            return new_path
        counter += 1


def add_prefix(paths: List[PathLike], prefix: str, preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    为文件名添加前缀
    
    Args:
        paths: 文件路径列表
        prefix: 要添加的前缀
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> add_prefix(['a.txt', 'b.txt'], 'prefix_', preview=True)
        >>> add_prefix([Path('test.txt')], 'new_', preview=False)
    """
    paths = _validate_paths(paths)
    results = []
    
    for path in paths:
        new_name = prefix + path.name
        new_path = path.parent / new_name
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            try:
                path.rename(new_path)
                results.append(RenameResult(True, path, new_path))
            except Exception as e:
                results.append(RenameResult(False, path, new_path, str(e)))
    
    return results


def add_suffix(paths: List[PathLike], suffix: str, before_ext: bool = True, 
               preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    为文件名添加后缀
    
    Args:
        paths: 文件路径列表
        suffix: 要添加的后缀
        before_ext: 是否添加在扩展名之前，默认 True
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> add_suffix(['a.txt'], '_backup', preview=True)
        >>> add_suffix(['photo.jpg'], '_small', before_ext=True, preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    for path in paths:
        if before_ext:
            new_name = f"{path.stem}{suffix}{path.suffix}"
        else:
            new_name = f"{path.name}{suffix}"
        new_path = path.parent / new_name
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            try:
                path.rename(new_path)
                results.append(RenameResult(True, path, new_path))
            except Exception as e:
                results.append(RenameResult(False, path, new_path, str(e)))
    
    return results


def remove_prefix(paths: List[PathLike], prefix: str, preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    移除文件名前缀
    
    Args:
        paths: 文件路径列表
        prefix: 要移除的前缀
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> remove_prefix(['prefix_a.txt'], 'prefix_', preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    for path in paths:
        if path.name.startswith(prefix):
            new_name = path.name[len(prefix):]
            new_path = path.parent / new_name
        else:
            new_path = path  # 无变化
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            if new_path != path:
                try:
                    path.rename(new_path)
                    results.append(RenameResult(True, path, new_path))
                except Exception as e:
                    results.append(RenameResult(False, path, new_path, str(e)))
            else:
                results.append(RenameResult(True, path, new_path))
    
    return results


def remove_suffix(paths: List[PathLike], suffix: str, before_ext: bool = True,
                  preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    移除文件名后缀
    
    Args:
        paths: 文件路径列表
        suffix: 要移除的后缀
        before_ext: 是否从扩展名之前移除，默认 True
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> remove_suffix(['a_backup.txt'], '_backup', preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    for path in paths:
        if before_ext:
            stem = path.stem
            if stem.endswith(suffix):
                new_name = f"{stem[:-len(suffix)]}{path.suffix}"
                new_path = path.parent / new_name
            else:
                new_path = path
        else:
            if path.name.endswith(suffix):
                new_name = path.name[:-len(suffix)]
                new_path = path.parent / new_name
            else:
                new_path = path
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            if new_path != path:
                try:
                    path.rename(new_path)
                    results.append(RenameResult(True, path, new_path))
                except Exception as e:
                    results.append(RenameResult(False, path, new_path, str(e)))
            else:
                results.append(RenameResult(True, path, new_path))
    
    return results


def replace_text(paths: List[PathLike], old_text: str, new_text: str, 
                 preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    替换文件名中的文本
    
    Args:
        paths: 文件路径列表
        old_text: 要替换的文本
        new_text: 替换后的文本
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> replace_text(['old_file.txt'], 'old', 'new', preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    for path in paths:
        new_name = path.name.replace(old_text, new_text)
        new_path = path.parent / new_name
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            if new_path != path:
                try:
                    path.rename(new_path)
                    results.append(RenameResult(True, path, new_path))
                except Exception as e:
                    results.append(RenameResult(False, path, new_path, str(e)))
            else:
                results.append(RenameResult(True, path, new_path))
    
    return results


def regex_replace(paths: List[PathLike], pattern: str, replacement: str,
                  flags: int = 0, preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    使用正则表达式替换文件名
    
    Args:
        paths: 文件路径列表
        pattern: 正则表达式模式
        replacement: 替换文本（支持反向引用）
        flags: 正则表达式标志（如 re.IGNORECASE）
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> regex_replace(['IMG_1234.jpg'], r'IMG_(\\d+)', r'Photo_\\1', preview=True)
        >>> regex_replace(['test.txt'], r'\\.txt$', '.md', preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        for path in paths:
            results.append(RenameResult(False, path, path, f"Invalid regex: {e}"))
        return results
    
    for path in paths:
        try:
            new_name = compiled.sub(replacement, path.name)
            new_path = path.parent / new_name
            
            if preview:
                results.append(RenamePreview(path, new_path))
            else:
                if new_path != path:
                    try:
                        path.rename(new_path)
                        results.append(RenameResult(True, path, new_path))
                    except Exception as e:
                        results.append(RenameResult(False, path, new_path, str(e)))
                else:
                    results.append(RenameResult(True, path, new_path))
        except Exception as e:
            if preview:
                results.append(RenamePreview(path, path))
            else:
                results.append(RenameResult(False, path, path, str(e)))
    
    return results


def change_case(paths: List[PathLike], case_mode: str = 'lower',
                preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    更改文件名大小写
    
    Args:
        paths: 文件路径列表
        case_mode: 大小写模式，可选 'lower', 'upper', 'title', 'capitalize', 'swap'
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> change_case(['HELLO.txt'], 'lower', preview=True)
        >>> change_case(['hello world.txt'], 'title', preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    case_functions = {
        'lower': str.lower,
        'upper': str.upper,
        'title': str.title,
        'capitalize': str.capitalize,
        'swap': str.swapcase,
    }
    
    if case_mode not in case_functions:
        for path in paths:
            results.append(RenameResult(False, path, path, f"Invalid case_mode: {case_mode}"))
        return results
    
    case_func = case_functions[case_mode]
    
    for path in paths:
        new_name = case_func(path.name)
        new_path = path.parent / new_name
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            if new_path != path:
                try:
                    path.rename(new_path)
                    results.append(RenameResult(True, path, new_path))
                except Exception as e:
                    results.append(RenameResult(False, path, new_path, str(e)))
            else:
                results.append(RenameResult(True, path, new_path))
    
    return results


def sequential_rename(paths: List[PathLike], base_name: str, start: int = 1, 
                      digits: int = 3, separator: str = '_', 
                      keep_ext: bool = True, preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    序号重命名文件
    
    Args:
        paths: 文件路径列表
        base_name: 基础文件名
        start: 起始序号，默认 1
        digits: 序号位数，默认 3（如 001, 002）
        separator: 分隔符，默认 '_'
        keep_ext: 是否保留原扩展名，默认 True
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> sequential_rename(['a.txt', 'b.txt'], 'photo', start=1, preview=True)
        >>> sequential_rename(['img.jpg'], 'IMG', digits=4, preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    # 构建已存在的路径集合（用于预览和避免冲突）
    existing_paths = set()
    for p in paths:
        existing_paths.add(p)
    
    used_paths = set()
    
    for i, path in enumerate(paths):
        num = start + i
        num_str = str(num).zfill(digits)
        
        if keep_ext:
            ext = path.suffix
            new_name = f"{base_name}{separator}{num_str}{ext}"
        else:
            new_name = f"{base_name}{separator}{num_str}"
        
        new_path = path.parent / new_name
        
        # 检查冲突并获取唯一路径
        if new_path in used_paths or (new_path.exists() and new_path not in existing_paths):
            new_path = _get_unique_path(new_path, used_paths | existing_paths)
        
        used_paths.add(new_path)
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            try:
                path.rename(new_path)
                results.append(RenameResult(True, path, new_path))
            except Exception as e:
                results.append(RenameResult(False, path, new_path, str(e)))
    
    return results


def datetime_rename(paths: List[PathLike], format_str: str = '%Y%m%d_%H%M%S',
                    prefix: str = '', suffix: str = '', 
                    keep_ext: bool = True, preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    使用日期时间重命名文件
    
    Args:
        paths: 文件路径列表
        format_str: 日期时间格式字符串，默认 '%Y%m%d_%H%M%S'
        prefix: 文件名前缀
        suffix: 文件名后缀（扩展名之前）
        keep_ext: 是否保留原扩展名，默认 True
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> datetime_rename(['photo.jpg'], format_str='%Y-%m-%d', prefix='IMG_', preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    used_paths = set()
    existing_paths = set(paths)
    
    for path in paths:
        dt_str = datetime.now().strftime(format_str)
        
        if keep_ext:
            ext = path.suffix
            name_parts = [prefix, dt_str, suffix]
            name = ''.join(p for p in name_parts if p) + ext
        else:
            name_parts = [prefix, dt_str, suffix]
            name = ''.join(p for p in name_parts if p)
        
        new_path = path.parent / name
        
        # 避免冲突
        if new_path in used_paths or (new_path.exists() and new_path not in existing_paths):
            new_path = _get_unique_path(new_path, used_paths | existing_paths)
        
        used_paths.add(new_path)
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            try:
                path.rename(new_path)
                results.append(RenameResult(True, path, new_path))
            except Exception as e:
                results.append(RenameResult(False, path, new_path, str(e)))
    
    return results


def change_extension(paths: List[PathLike], new_ext: str, 
                      preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    更改文件扩展名
    
    Args:
        paths: 文件路径列表
        new_ext: 新扩展名（可带或不带点，如 '.txt' 或 'txt'）
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> change_extension(['data.txt'], 'md', preview=True)
        >>> change_extension(['image.jpeg'], '.jpg', preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    # 确保扩展名以点开头
    if new_ext and not new_ext.startswith('.'):
        new_ext = '.' + new_ext
    
    for path in paths:
        new_name = path.stem + new_ext
        new_path = path.parent / new_name
        
        if preview:
            results.append(RenamePreview(path, new_path))
        else:
            if new_path != path:
                try:
                    path.rename(new_path)
                    results.append(RenameResult(True, path, new_path))
                except Exception as e:
                    results.append(RenameResult(False, path, new_path, str(e)))
            else:
                results.append(RenameResult(True, path, new_path))
    
    return results


def custom_rename(paths: List[PathLike], rename_func: Callable[[Path], str],
                  preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    自定义重命名函数
    
    Args:
        paths: 文件路径列表
        rename_func: 自定义重命名函数，接收 Path 对象，返回新文件名
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> def my_rename(p):
        ...     return p.stem.upper() + p.suffix
        >>> custom_rename(['a.txt'], my_rename, preview=True)
    """
    paths = _validate_paths(paths)
    results = []
    
    used_paths = set()
    existing_paths = set(paths)
    
    for path in paths:
        try:
            new_name = rename_func(path)
            new_path = path.parent / new_name
            
            # 避免冲突
            if new_path in used_paths or (new_path.exists() and new_path not in existing_paths):
                new_path = _get_unique_path(new_path, used_paths | existing_paths)
            
            used_paths.add(new_path)
            
            if preview:
                results.append(RenamePreview(path, new_path))
            else:
                try:
                    path.rename(new_path)
                    results.append(RenameResult(True, path, new_path))
                except Exception as e:
                    results.append(RenameResult(False, path, new_path, str(e)))
        except Exception as e:
            if preview:
                results.append(RenamePreview(path, path))
            else:
                results.append(RenameResult(False, path, path, str(e)))
    
    return results


def undo_rename(results: List[RenameResult]) -> List[RenameResult]:
    """
    撤销重命名操作
    
    Args:
        results: 之前的 RenameResult 列表
    
    Returns:
        撤销操作的 RenameResult 列表
    
    Examples:
        >>> results = add_prefix(['a.txt'], 'new_')
        >>> undo_results = undo_rename(results)
    """
    undo_results = []
    
    for result in reversed(results):
        if result.success and result.old_path != result.new_path:
            try:
                # 检查新路径是否还存在
                if result.new_path.exists():
                    result.new_path.rename(result.old_path)
                    undo_results.append(RenameResult(True, result.new_path, result.old_path))
                else:
                    undo_results.append(RenameResult(False, result.new_path, result.old_path, "File not found"))
            except Exception as e:
                undo_results.append(RenameResult(False, result.new_path, result.old_path, str(e)))
        else:
            undo_results.append(RenameResult(True, result.new_path, result.old_path))
    
    return undo_results


def batch_rename(paths: List[PathLike], operations: List[Dict],
                 preview: bool = False) -> Union[List[RenamePreview], List[RenameResult]]:
    """
    批量执行多个重命名操作
    
    Args:
        paths: 文件路径列表
        operations: 操作列表，每个操作是一个字典
            - {'type': 'prefix', 'value': 'new_'}
            - {'type': 'suffix', 'value': '_bak'}
            - {'type': 'replace', 'old': 'old', 'new': 'new'}
            - {'type': 'regex', 'pattern': r'\\d+', 'replacement': 'NUM'}
            - {'type': 'case', 'mode': 'lower'}
            - {'type': 'extension', 'value': '.md'}
        preview: 是否只预览不执行，默认 False
    
    Returns:
        preview=True 返回 RenamePreview 列表
        preview=False 返回 RenameResult 列表
    
    Examples:
        >>> ops = [
        ...     {'type': 'prefix', 'value': 'IMG_'},
        ...     {'type': 'case', 'mode': 'lower'}
        ... ]
        >>> batch_rename(['TEST.txt'], ops, preview=True)
    """
    paths = _validate_paths(paths)
    
    # 预览模式：计算最终结果
    if preview:
        current_names = [p.name for p in paths]
        parents = [p.parent for p in paths]
        
        for op in operations:
            op_type = op.get('type')
            
            if op_type == 'prefix':
                prefix = op.get('value', '')
                current_names = [prefix + name for name in current_names]
            elif op_type == 'suffix':
                suffix = op.get('value', '')
                before_ext = op.get('before_ext', True)
                if before_ext:
                    current_names = [Path(name).stem + suffix + Path(name).suffix for name in current_names]
                else:
                    current_names = [name + suffix for name in current_names]
            elif op_type == 'replace':
                old = op.get('old', '')
                new = op.get('new', '')
                current_names = [name.replace(old, new) for name in current_names]
            elif op_type == 'regex':
                pattern = op.get('pattern', '')
                replacement = op.get('replacement', '')
                flags = op.get('flags', 0)
                try:
                    current_names = [re.sub(pattern, replacement, name, flags=flags) for name in current_names]
                except re.error:
                    pass
            elif op_type == 'case':
                mode = op.get('mode', 'lower')
                case_funcs = {
                    'lower': str.lower,
                    'upper': str.upper,
                    'title': str.title,
                    'capitalize': str.capitalize,
                    'swap': str.swapcase,
                }
                if mode in case_funcs:
                    current_names = [case_funcs[mode](name) for name in current_names]
            elif op_type == 'extension':
                new_ext = op.get('value', '')
                if new_ext and not new_ext.startswith('.'):
                    new_ext = '.' + new_ext
                current_names = [Path(name).stem + new_ext for name in current_names]
        
        previews = []
        for old_path, new_name, parent in zip(paths, current_names, parents):
            previews.append(RenamePreview(old_path, parent / new_name))
        return previews
    
    # 执行模式：按顺序执行每个操作
    for op in operations:
        op_type = op.get('type')
        
        if op_type == 'prefix':
            results = add_prefix(paths, op.get('value', ''), preview=False)
        elif op_type == 'suffix':
            results = add_suffix(paths, op.get('value', ''), 
                                before_ext=op.get('before_ext', True), preview=False)
        elif op_type == 'replace':
            results = replace_text(paths, op.get('old', ''), op.get('new', ''), preview=False)
        elif op_type == 'regex':
            results = regex_replace(paths, op.get('pattern', ''), op.get('replacement', ''),
                                   flags=op.get('flags', 0), preview=False)
        elif op_type == 'case':
            results = change_case(paths, op.get('mode', 'lower'), preview=False)
        elif op_type == 'extension':
            results = change_extension(paths, op.get('value', ''), preview=False)
        else:
            continue
        
        # 更新路径列表为重命名后的路径
        paths = [r.new_path for r in results]
    
    return results


def get_files_by_pattern(directory: PathLike, pattern: str = '*',
                         recursive: bool = False) -> List[Path]:
    """
    按模式获取文件列表
    
    Args:
        directory: 目录路径
        pattern: 文件名模式（支持通配符），默认 '*'
        recursive: 是否递归子目录，默认 False
    
    Returns:
        匹配的文件路径列表
    
    Examples:
        >>> get_files_by_pattern('.', '*.txt')
        >>> get_files_by_pattern('./photos', 'IMG_*.jpg', recursive=True)
    """
    directory = Path(directory)
    
    if not directory.is_dir():
        return []
    
    if recursive:
        return list(directory.rglob(pattern))
    else:
        return list(directory.glob(pattern))


# 便捷函数别名
def rename_with_sequence(paths: List[PathLike], base_name: str, **kwargs):
    """sequential_rename 的便捷别名"""
    return sequential_rename(paths, base_name, **kwargs)


def rename_with_datetime(paths: List[PathLike], **kwargs):
    """datetime_rename 的便捷别名"""
    return datetime_rename(paths, **kwargs)


if __name__ == '__main__':
    # 简单演示
    import tempfile
    import shutil
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # 创建测试文件
        test_files = []
        for name in ['test1.txt', 'test2.txt', 'TEST3.TXT']:
            f = tmpdir / name
            f.write_text('content')
            test_files.append(f)
        
        print("=== 批量重命名工具演示 ===\n")
        
        # 1. 添加前缀预览
        print("1. 添加前缀 'prefix_' (预览):")
        for p in add_prefix(test_files, 'prefix_', preview=True):
            print(f"   {p}")
        
        # 2. 序号重命名预览
        print("\n2. 序号重命名 'file_' (预览):")
        for p in sequential_rename(test_files, 'file', preview=True):
            print(f"   {p}")
        
        # 3. 大小写转换预览
        print("\n3. 转换为小写 (预览):")
        for p in change_case(test_files, 'lower', preview=True):
            print(f"   {p}")
        
        # 4. 正则替换预览
        print("\n4. 正则替换 'test' -> 'demo' (预览):")
        for p in regex_replace(test_files, r'test', 'demo', preview=True):
            print(f"   {p}")
        
        # 5. 批量操作预览
        print("\n5. 批量操作: 添加前缀 + 转小写 (预览):")
        ops = [
            {'type': 'prefix', 'value': 'new_'},
            {'type': 'case', 'mode': 'lower'}
        ]
        for p in batch_rename(test_files, ops, preview=True):
            print(f"   {p}")
        
        print("\n=== 演示完成 ===")