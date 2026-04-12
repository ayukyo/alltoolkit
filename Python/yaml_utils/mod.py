"""
AllToolkit - Python YAML Utilities

功能完整的 YAML 处理工具模块，支持 YAML 文件的读取、写入、验证、
转换、合并、差分比较、安全加载等功能。

使用 PyYAML 库（如果可用），否则优雅降级使用标准库 JSON 作为替代。

Author: AllToolkit
License: MIT
"""

import os
import io
import json
from typing import Union, Optional, Any, Dict, List, Tuple, BinaryIO
from pathlib import Path


# =============================================================================
# PyYAML 检测与导入
# =============================================================================

_PYYAML_AVAILABLE = False
yaml = None

try:
    import yaml
    _PYYAML_AVAILABLE = True
except ImportError:
    pass


# =============================================================================
# 版本信息
# =============================================================================

__version__ = "1.0.0"
__author__ = "AllToolkit"
__license__ = "MIT"


def get_version() -> str:
    """获取模块版本号。"""
    return __version__


def is_pyyaml_available() -> bool:
    """检查 PyYAML 是否可用。"""
    return _PYYAML_AVAILABLE


# =============================================================================
# 异常类
# =============================================================================

class YAMLUtilsError(Exception):
    """YAML 工具基础异常。"""
    pass


class YAMLFileNotFoundError(YAMLUtilsError):
    """YAML 文件未找到异常。"""
    pass


class YAMLValidationError(YAMLUtilsError):
    """YAML 验证失败异常。"""
    pass


class YAMLFormatError(YAMLUtilsError):
    """YAML 格式错误异常。"""
    pass


# =============================================================================
# YAML 读取功能
# =============================================================================

def load_yaml(source: Union[str, Path, BinaryIO], 
              safe: bool = True) -> Any:
    """
    加载 YAML 数据。
    
    Args:
        source: 文件路径、文件对象或 YAML 字符串
        safe: 是否使用安全加载（默认 True，防止任意代码执行）
    
    Returns:
        解析后的 Python 对象（字典、列表等）
    
    Raises:
        YAMLFileNotFoundError: 文件不存在
        YAMLFormatError: YAML 格式错误
    """
    if _PYYAML_AVAILABLE:
        return _load_yaml_pyyaml(source, safe)
    else:
        # 降级：尝试作为 JSON 解析
        return _load_yaml_fallback(source)


def _is_file_path(source: str) -> bool:
    """判断字符串是否是文件路径。"""
    # 检查是否包含路径分隔符或文件扩展名
    if os.sep in source or (os.altsep and os.altsep in source):
        return True
    if source.endswith(('.yaml', '.yml', '.YAML', '.YML')):
        return True
    # 检查是否看起来像路径（包含 / 或 Windows 路径）
    if '/' in source or (len(source) > 2 and source[1] == ':'):
        return True
    return False


def _load_yaml_pyyaml(source: Union[str, Path, BinaryIO], 
                      safe: bool = True) -> Any:
    """使用 PyYAML 加载。"""
    try:
        if isinstance(source, Path):
            # Path 对象
            if not source.exists():
                raise YAMLFileNotFoundError(f"文件不存在：{source}")
            
            with open(source, 'r', encoding='utf-8') as f:
                if safe:
                    return yaml.safe_load(f)
                else:
                    return yaml.unsafe_load(f)
        elif isinstance(source, str):
            # 字符串：判断是文件路径还是 YAML 内容
            if _is_file_path(source):
                path = Path(source)
                if not path.exists():
                    raise YAMLFileNotFoundError(f"文件不存在：{source}")
                
                with open(path, 'r', encoding='utf-8') as f:
                    if safe:
                        return yaml.safe_load(f)
                    else:
                        return yaml.unsafe_load(f)
            else:
                # YAML 字符串内容
                if safe:
                    return yaml.safe_load(source)
                else:
                    return yaml.unsafe_load(source)
        else:
            # 文件对象
            if safe:
                return yaml.safe_load(source)
            else:
                return yaml.unsafe_load(source)
    except yaml.YAMLError as e:
        raise YAMLFormatError(f"YAML 格式错误：{e}")


def _load_yaml_fallback(source: Union[str, Path, BinaryIO]) -> Any:
    """降级实现：尝试作为 JSON 解析。"""
    try:
        if isinstance(source, Path):
            # Path 对象
            if not source.exists():
                raise YAMLFileNotFoundError(f"文件不存在：{source}")
            
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
            return json.loads(content)
        elif isinstance(source, str):
            # 字符串：判断是文件路径还是内容
            if _is_file_path(source):
                path = Path(source)
                if not path.exists():
                    raise YAMLFileNotFoundError(f"文件不存在：{source}")
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return json.loads(content)
            else:
                # JSON 字符串内容
                return json.loads(source)
        else:
            # 文件对象
            content = source.read() if hasattr(source, 'read') else str(source)
            return json.loads(content)
    except json.JSONDecodeError as e:
        raise YAMLFormatError(f"无法解析为 JSON（PyYAML 不可用）: {e}")


def load_yaml_string(yaml_string: str, safe: bool = True) -> Any:
    """
    从字符串加载 YAML。
    
    Args:
        yaml_string: YAML 格式的字符串
        safe: 是否使用安全加载
    
    Returns:
        解析后的 Python 对象
    """
    return load_yaml(yaml_string, safe=safe)


def load_yaml_file(file_path: Union[str, Path], 
                   safe: bool = True) -> Any:
    """
    从文件加载 YAML。
    
    Args:
        file_path: YAML 文件路径
        safe: 是否使用安全加载
    
    Returns:
        解析后的 Python 对象
    
    Raises:
        YAMLFileNotFoundError: 文件不存在
    """
    path = Path(file_path)
    if not path.exists():
        raise YAMLFileNotFoundError(f"文件不存在：{file_path}")
    return load_yaml(path, safe=safe)


def load_yaml_all(source: Union[str, Path]) -> List[Any]:
    """
    加载 YAML 中的所有文档（支持多文档 YAML）。
    
    Args:
        source: 文件路径或 YAML 字符串
    
    Returns:
        包含所有文档的列表
    """
    if _PYYAML_AVAILABLE:
        try:
            if isinstance(source, (str, Path)):
                with open(source, 'r', encoding='utf-8') as f:
                    return list(yaml.safe_load_all(f))
            else:
                return list(yaml.safe_load_all(source))
        except yaml.YAMLError as e:
            raise YAMLFormatError(f"YAML 格式错误：{e}")
    else:
        # 降级：返回单个文档
        return [load_yaml(source)]


# =============================================================================
# YAML 写入功能
# =============================================================================

def dump_yaml(data: Any, 
              output: Optional[Union[str, Path]] = None,
              indent: int = 2,
              allow_unicode: bool = True,
              sort_keys: bool = False) -> Optional[str]:
    """
    将数据转储为 YAML 格式。
    
    Args:
        data: 要转储的 Python 对象
        output: 输出文件路径（None 则返回字符串）
        indent: 缩进空格数
        allow_unicode: 是否允许 Unicode 字符
        sort_keys: 是否对键排序
    
    Returns:
        YAML 字符串（如果 output 为 None），否则 None
    
    Raises:
        YAMLFormatError: 序列化失败
    """
    if _PYYAML_AVAILABLE:
        return _dump_yaml_pyyaml(data, output, indent, allow_unicode, sort_keys)
    else:
        return _dump_yaml_fallback(data, output, indent)


def _dump_yaml_pyyaml(data: Any, 
                      output: Optional[Union[str, Path]],
                      indent: int,
                      allow_unicode: bool,
                      sort_keys: bool) -> Optional[str]:
    """使用 PyYAML 转储。"""
    try:
        # 构建兼容的参数（旧版 PyYAML 不支持某些参数）
        dump_kwargs = {
            'default_flow_style': False,
            'indent': indent,
            'allow_unicode': allow_unicode,
        }
        
        # 仅在新版 PyYAML 中添加 sort_keys
        try:
            yaml.dump({}, sort_keys=True)
            dump_kwargs['sort_keys'] = sort_keys
        except TypeError:
            pass
        
        yaml_str = yaml.dump(data, **dump_kwargs)
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(yaml_str)
            return None
        else:
            return yaml_str
    except yaml.YAMLError as e:
        raise YAMLFormatError(f"YAML 序列化失败：{e}")


def _dump_yaml_fallback(data: Any, 
                        output: Optional[Union[str, Path]],
                        indent: int) -> Optional[str]:
    """降级实现：输出为 JSON。"""
    json_str = json.dumps(data, indent=indent, ensure_ascii=False)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(json_str)
        return None
    else:
        return json_str


def dump_yaml_file(data: Any, 
                   file_path: Union[str, Path],
                   indent: int = 2,
                   allow_unicode: bool = True) -> None:
    """
    将数据转储为 YAML 文件。
    
    Args:
        data: 要转储的 Python 对象
        file_path: 输出文件路径
        indent: 缩进空格数
        allow_unicode: 是否允许 Unicode 字符
    """
    dump_yaml(data, output=file_path, indent=indent, allow_unicode=allow_unicode)


def dump_yaml_string(data: Any, 
                     indent: int = 2,
                     allow_unicode: bool = True) -> str:
    """
    将数据转储为 YAML 字符串。
    
    Args:
        data: 要转储的 Python 对象
        indent: 缩进空格数
        allow_unicode: 是否允许 Unicode 字符
    
    Returns:
        YAML 格式的字符串
    """
    result = dump_yaml(data, indent=indent, allow_unicode=allow_unicode)
    return result if result else ""


# =============================================================================
# YAML 验证功能
# =============================================================================

def validate_yaml(source: Union[str, Path], 
                  schema: Optional[Dict] = None) -> Tuple[bool, List[str]]:
    """
    验证 YAML 文件。
    
    Args:
        source: YAML 文件路径或字符串
        schema: 可选的模式字典（简单的类型检查）
    
    Returns:
        (是否有效，错误消息列表)
    """
    errors = []
    
    try:
        data = load_yaml(source)
        
        if schema and isinstance(data, dict):
            _validate_schema(data, schema, "", errors)
        
        return len(errors) == 0, errors
    except YAMLFileNotFoundError as e:
        return False, [str(e)]
    except YAMLFormatError as e:
        return False, [str(e)]


def _validate_schema(data: Any, schema: Dict, path: str, errors: List[str]) -> None:
    """递归验证模式。"""
    if not isinstance(schema, dict):
        return
    
    for key, expected_type in schema.items():
        current_path = f"{path}.{key}" if path else key
        
        if key not in data:
            if expected_type is not None:  # None 表示可选
                errors.append(f"缺少必需字段：{current_path}")
            continue
        
        value = data[key]
        
        if isinstance(expected_type, dict):
            # 嵌套对象
            if not isinstance(value, dict):
                errors.append(f"{current_path} 应该是对象类型")
            else:
                _validate_schema(value, expected_type, current_path, errors)
        elif isinstance(expected_type, list):
            # 数组
            if not isinstance(value, list):
                errors.append(f"{current_path} 应该是数组类型")
        elif expected_type == str and not isinstance(value, str):
            errors.append(f"{current_path} 应该是字符串类型")
        elif expected_type == int and not isinstance(value, int):
            errors.append(f"{current_path} 应该是整数类型")
        elif expected_type == float and not isinstance(value, (int, float)):
            errors.append(f"{current_path} 应该是数字类型")
        elif expected_type == bool and not isinstance(value, bool):
            errors.append(f"{current_path} 应该是布尔类型")


def is_valid_yaml(source: Union[str, Path]) -> bool:
    """
    检查是否为有效的 YAML。
    
    Args:
        source: YAML 文件路径或字符串
    
    Returns:
        是否有效
    """
    valid, _ = validate_yaml(source)
    return valid


# =============================================================================
# YAML 转换功能
# =============================================================================

def yaml_to_json(source: Union[str, Path], 
                 output: Optional[Union[str, Path]] = None,
                 indent: int = 2) -> Optional[str]:
    """
    将 YAML 转换为 JSON。
    
    Args:
        source: YAML 文件路径或字符串
        output: 输出文件路径（None 则返回字符串）
        indent: JSON 缩进空格数
    
    Returns:
        JSON 字符串（如果 output 为 None），否则 None
    """
    data = load_yaml(source)
    json_str = json.dumps(data, indent=indent, ensure_ascii=False)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(json_str)
        return None
    else:
        return json_str


def json_to_yaml(source: Union[str, Path], 
                 output: Optional[Union[str, Path]] = None,
                 indent: int = 2) -> Optional[str]:
    """
    将 JSON 转换为 YAML。
    
    Args:
        source: JSON 文件路径或字符串
        output: 输出文件路径（None 则返回字符串）
        indent: YAML 缩进空格数
    
    Returns:
        YAML 字符串（如果 output 为 None），否则 None
    """
    # 加载 JSON
    if isinstance(source, (str, Path)):
        path = Path(source)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.loads(source)
    else:
        data = json.loads(source)
    
    # 转储为 YAML
    return dump_yaml(data, output=output, indent=indent)


def yaml_to_dict(source: Union[str, Path]) -> Dict:
    """
    将 YAML 转换为字典。
    
    Args:
        source: YAML 文件路径或字符串
    
    Returns:
        字典对象
    """
    result = load_yaml(source)
    return result if isinstance(result, dict) else {}


# =============================================================================
# YAML 合并功能
# =============================================================================

def merge_yaml(sources: List[Union[str, Path]], 
               output: Optional[Union[str, Path]] = None,
               deep: bool = True) -> Optional[Dict]:
    """
    合并多个 YAML 文件/数据。
    
    Args:
        sources: 源文件路径列表
        output: 输出文件路径（None 则返回合并后的字典）
        deep: 是否深度合并（True 递归合并嵌套对象）
    
    Returns:
        合并后的字典（如果 output 为 None），否则 None
    """
    result = {}
    
    for source in sources:
        data = load_yaml(source)
        if isinstance(data, dict):
            if deep:
                result = _deep_merge(result, data)
            else:
                result.update(data)
    
    if output:
        dump_yaml(result, output=output)
        return None
    else:
        return result


def _deep_merge(base: Dict, override: Dict) -> Dict:
    """深度合并两个字典。"""
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


# =============================================================================
# YAML 差分功能
# =============================================================================

def diff_yaml(source1: Union[str, Path], 
              source2: Union[str, Path]) -> Dict[str, Any]:
    """
    比较两个 YAML 文件的差异。
    
    Args:
        source1: 第一个 YAML 文件路径
        source2: 第二个 YAML 文件路径
    
    Returns:
        包含 added、removed、modified 键的字典
    """
    data1 = load_yaml(source1)
    data2 = load_yaml(source2)
    
    added = {}
    removed = {}
    modified = {}
    
    if isinstance(data1, dict) and isinstance(data2, dict):
        all_keys = set(data1.keys()) | set(data2.keys())
        
        for key in all_keys:
            if key not in data1:
                added[key] = data2[key]
            elif key not in data2:
                removed[key] = data1[key]
            elif data1[key] != data2[key]:
                modified[key] = {"old": data1[key], "new": data2[key]}
    
    return {
        "added": added,
        "removed": removed,
        "modified": modified
    }


# =============================================================================
# 便捷功能
# =============================================================================

def get_yaml_value(source: Union[str, Path], 
                   key_path: str, 
                   default: Any = None) -> Any:
    """
    获取 YAML 中指定路径的值。
    
    Args:
        source: YAML 文件路径
        key_path: 点分隔的键路径（如 "database.host"）
        default: 默认值（如果路径不存在）
    
    Returns:
        对应的值或默认值
    """
    data = load_yaml(source)
    
    if not isinstance(data, dict):
        return default
    
    keys = key_path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def set_yaml_value(source: Union[str, Path], 
                   key_path: str, 
                   value: Any,
                   output: Optional[Union[str, Path]] = None) -> None:
    """
    设置 YAML 中指定路径的值。
    
    Args:
        source: YAML 文件路径
        key_path: 点分隔的键路径
        value: 要设置的值
        output: 输出文件路径（None 则覆盖原文件）
    """
    data = load_yaml(source)
    
    if not isinstance(data, dict):
        data = {}
    
    keys = key_path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value
    
    dump_yaml(data, output=output or source)


def delete_yaml_key(source: Union[str, Path], 
                    key_path: str,
                    output: Optional[Union[str, Path]] = None) -> None:
    """
    删除 YAML 中指定路径的键。
    
    Args:
        source: YAML 文件路径
        key_path: 点分隔的键路径
        output: 输出文件路径（None 则覆盖原文件）
    """
    data = load_yaml(source)
    
    if not isinstance(data, dict):
        return
    
    keys = key_path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            return
        current = current[key]
    
    if keys[-1] in current:
        del current[keys[-1]]
    
    dump_yaml(data, output=output or source)


# =============================================================================
# 安全功能
# =============================================================================

def safe_load_yaml(source: Union[str, Path]) -> Any:
    """
    安全加载 YAML（防止任意代码执行）。
    
    这是 load_yaml 的别名，始终使用安全模式。
    
    Args:
        source: YAML 文件路径或字符串
    
    Returns:
        解析后的 Python 对象
    """
    return load_yaml(source, safe=True)


def contains_unsafe_tags(source: Union[str, Path]) -> bool:
    """
    检查 YAML 是否包含不安全标签。
    
    Args:
        source: YAML 文件路径或字符串
    
    Returns:
        是否包含不安全标签
    """
    unsafe_tags = ['!!python', '!!ruby', '!!perl', '!!java']
    
    try:
        if isinstance(source, (str, Path)):
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = str(source)
        
        return any(tag in content for tag in unsafe_tags)
    except Exception:
        return False


# =============================================================================
# 工具功能
# =============================================================================

def get_supported_formats() -> List[str]:
    """获取支持的格式列表。"""
    formats = ["YAML", "JSON"]
    if _PYYAML_AVAILABLE:
        formats.append("YAML (full)")
    return formats


def get_yaml_info(source: Union[str, Path]) -> Dict[str, Any]:
    """
    获取 YAML 文件信息。
    
    Args:
        source: YAML 文件路径
    
    Returns:
        包含文件信息的字典
    """
    path = Path(source)
    
    info = {
        "path": str(path.absolute()),
        "exists": path.exists(),
        "size": path.stat().st_size if path.exists() else 0,
        "valid": False,
        "type": "unknown",
        "keys": []
    }
    
    if path.exists():
        try:
            data = load_yaml(source)
            info["valid"] = True
            
            if isinstance(data, dict):
                info["type"] = "object"
                info["keys"] = list(data.keys())
            elif isinstance(data, list):
                info["type"] = "array"
                info["length"] = len(data)
            else:
                info["type"] = type(data).__name__
        except Exception:
            info["valid"] = False
    
    return info


# =============================================================================
# 模块信息
# =============================================================================

def get_module_info() -> Dict[str, Any]:
    """获取模块信息。"""
    return {
        "name": "yaml_utils",
        "version": __version__,
        "author": __author__,
        "license": __license__,
        "pyyaml_available": _PYYAML_AVAILABLE,
        "supported_formats": get_supported_formats()
    }


# 导出所有公共 API
__all__ = [
    # 版本信息
    'get_version',
    'is_pyyaml_available',
    'get_module_info',
    
    # 异常类
    'YAMLUtilsError',
    'YAMLFileNotFoundError',
    'YAMLValidationError',
    'YAMLFormatError',
    
    # 读取功能
    'load_yaml',
    'load_yaml_string',
    'load_yaml_file',
    'load_yaml_all',
    'safe_load_yaml',
    
    # 写入功能
    'dump_yaml',
    'dump_yaml_file',
    'dump_yaml_string',
    
    # 验证功能
    'validate_yaml',
    'is_valid_yaml',
    
    # 转换功能
    'yaml_to_json',
    'json_to_yaml',
    'yaml_to_dict',
    
    # 合并功能
    'merge_yaml',
    
    # 差分功能
    'diff_yaml',
    
    # 便捷功能
    'get_yaml_value',
    'set_yaml_value',
    'delete_yaml_key',
    
    # 安全功能
    'contains_unsafe_tags',
    
    # 工具功能
    'get_supported_formats',
    'get_yaml_info',
]
