"""
JSON Utilities - JSON 工具集

全面的 JSON 处理工具集，提供格式化、验证、路径查询、差异比较、合并、展平等功能。
零外部依赖，纯 Python 实现。

Author: AllToolkit 自动化开发
Version: 1.0.0 (2026-04-25)
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple, Union, Iterator, Callable
from dataclasses import dataclass, field
from enum import Enum
from copy import deepcopy


# ============================================================================
# 数据类和枚举
# ============================================================================

class JsonType(Enum):
    """JSON 值类型"""
    NULL = "null"
    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"
    ARRAY = "array"
    OBJECT = "object"


@dataclass
class JsonPath:
    """JSON 路径表示"""
    path: str
    value: Any
    
    def __repr__(self):
        return f"JsonPath(path='{self.path}', value={repr(self.value)})"


@dataclass
class JsonDiff:
    """JSON 差异项"""
    path: str
    old_value: Any
    new_value: Any
    change_type: str  # 'added', 'removed', 'changed'
    
    def __repr__(self):
        return f"JsonDiff(path='{self.path}', type='{self.change_type}')"


@dataclass
class ValidationResult:
    """验证结果"""
    valid: bool
    error: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    
    def __bool__(self):
        return self.valid


# ============================================================================
# JSON 类型判断和获取
# ============================================================================

def get_json_type(value: Any) -> JsonType:
    """
    获取 JSON 值的类型。
    
    Args:
        value: 要检查的值
        
    Returns:
        JsonType 枚举值
    """
    if value is None:
        return JsonType.NULL
    elif isinstance(value, bool):
        return JsonType.BOOLEAN
    elif isinstance(value, (int, float)):
        return JsonType.NUMBER
    elif isinstance(value, str):
        return JsonType.STRING
    elif isinstance(value, list):
        return JsonType.ARRAY
    elif isinstance(value, dict):
        return JsonType.OBJECT
    else:
        raise ValueError(f"Invalid JSON type: {type(value)}")


def is_json_serializable(value: Any) -> bool:
    """
    检查值是否可序列化为 JSON。
    
    Args:
        value: 要检查的值
        
    Returns:
        是否可序列化
    """
    try:
        json.dumps(value)
        return True
    except (TypeError, ValueError):
        return False


# ============================================================================
# JSON 验证
# ============================================================================

def validate_json(json_string: str) -> ValidationResult:
    """
    验证 JSON 字符串是否有效。
    
    Args:
        json_string: JSON 字符串
        
    Returns:
        ValidationResult 对象
    """
    try:
        json.loads(json_string)
        return ValidationResult(valid=True)
    except json.JSONDecodeError as e:
        return ValidationResult(
            valid=False,
            error=e.msg,
            line=e.lineno,
            column=e.colno
        )


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    简单的 JSON Schema 验证（基础实现）。
    支持类型检查、必填字段、枚举值、最小/最大值等基本验证。
    
    Args:
        data: 要验证的数据
        schema: JSON Schema（简化版）
        
    Returns:
        (是否有效, 错误消息列表)
    """
    errors = []
    
    def validate_recursive(obj: Any, sch: Dict[str, Any], path: str = ""):
        # 类型检查
        if "type" in sch:
            expected_type = sch["type"]
            type_map = {
                "null": type(None),
                "boolean": bool,
                "integer": int,
                "number": (int, float),
                "string": str,
                "array": list,
                "object": dict
            }
            
            if expected_type in type_map:
                if not isinstance(obj, type_map[expected_type]):
                    if expected_type == "integer" and isinstance(obj, float) and obj.is_integer():
                        pass  # 允许整数浮点数
                    else:
                        errors.append(f"{path}: expected {expected_type}, got {type(obj).__name__}")
        
        # 必填字段
        if "required" in sch and isinstance(obj, dict):
            for field in sch["required"]:
                if field not in obj:
                    errors.append(f"{path}: missing required field '{field}'")
        
        # 枚举值
        if "enum" in sch:
            if obj not in sch["enum"]:
                errors.append(f"{path}: value must be one of {sch['enum']}")
        
        # 最小值/最大值
        if isinstance(obj, (int, float)):
            if "minimum" in sch and obj < sch["minimum"]:
                errors.append(f"{path}: value {obj} is less than minimum {sch['minimum']}")
            if "maximum" in sch and obj > sch["maximum"]:
                errors.append(f"{path}: value {obj} is greater than maximum {sch['maximum']}")
        
        # 字符串长度
        if isinstance(obj, str):
            if "minLength" in sch and len(obj) < sch["minLength"]:
                errors.append(f"{path}: string length {len(obj)} is less than minLength {sch['minLength']}")
            if "maxLength" in sch and len(obj) > sch["maxLength"]:
                errors.append(f"{path}: string length {len(obj)} is greater than maxLength {sch['maxLength']}")
        
        # 数组长度
        if isinstance(obj, list):
            if "minItems" in sch and len(obj) < sch["minItems"]:
                errors.append(f"{path}: array length {len(obj)} is less than minItems {sch['minItems']}")
            if "maxItems" in sch and len(obj) > sch["maxItems"]:
                errors.append(f"{path}: array length {len(obj)} is greater than maxItems {sch['maxItems']}")
            # 数组项验证
            if "items" in sch:
                for i, item in enumerate(obj):
                    validate_recursive(item, sch["items"], f"{path}[{i}]")
        
        # 对象属性验证
        if isinstance(obj, dict):
            if "properties" in sch:
                for prop, prop_schema in sch["properties"].items():
                    if prop in obj:
                        validate_recursive(obj[prop], prop_schema, f"{path}.{prop}" if path else prop)
        
        # 嵌套验证
        if "additionalProperties" in sch and isinstance(obj, dict):
            if isinstance(sch["additionalProperties"], dict):
                for key, val in obj.items():
                    if "properties" not in sch or key not in sch.get("properties", {}):
                        validate_recursive(val, sch["additionalProperties"], f"{path}.{key}" if path else key)
    
    validate_recursive(data, schema)
    return len(errors) == 0, errors


# ============================================================================
# JSON 格式化
# ============================================================================

def format_json(
    data: Any,
    indent: int = 2,
    ensure_ascii: bool = False,
    sort_keys: bool = False,
    compact: bool = False
) -> str:
    """
    格式化 JSON 数据。
    
    Args:
        data: JSON 数据
        indent: 缩进空格数
        ensure_ascii: 是否转义非 ASCII 字符
        sort_keys: 是否按键排序
        compact: 是否压缩输出
        
    Returns:
        格式化后的 JSON 字符串
    """
    if compact:
        return json.dumps(data, ensure_ascii=ensure_ascii, separators=(',', ':'))
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys)


def minify_json(json_string: str) -> str:
    """
    压缩 JSON 字符串，移除所有空白。
    
    Args:
        json_string: JSON 字符串
        
    Returns:
        压缩后的 JSON 字符串
    """
    data = json.loads(json_string)
    return json.dumps(data, separators=(',', ':'))


def prettify_json(json_string: str, indent: int = 2) -> str:
    """
    美化 JSON 字符串。
    
    Args:
        json_string: JSON 字符串
        indent: 缩进空格数
        
    Returns:
        美化后的 JSON 字符串
    """
    data = json.loads(json_string)
    return json.dumps(data, indent=indent, ensure_ascii=False)


# ============================================================================
# JSON 路径操作
# ============================================================================

def get_value(data: Union[Dict, List], path: str, default: Any = None) -> Any:
    """
    通过路径获取 JSON 值。
    支持路径格式：'a.b.c' 或 'a[0].b' 或 'items[*].name'
    
    Args:
        data: JSON 数据
        path: 路径字符串
        default: 默认值
        
    Returns:
        找到的值或默认值
    """
    try:
        parts = parse_json_path(path)
        current = data
        
        for part in parts:
            if isinstance(current, dict):
                current = current[part]
            elif isinstance(current, list):
                if part == '*':
                    # 通配符：返回所有值
                    return [get_value(item, '.'.join(parts[parts.index(part)+1:]), default) for item in current]
                index = int(part)
                current = current[index]
            else:
                return default
        
        return current
    except (KeyError, IndexError, ValueError, TypeError):
        return default


def set_value(data: Union[Dict, List], path: str, value: Any) -> Union[Dict, List]:
    """
    通过路径设置 JSON 值。
    
    Args:
        data: JSON 数据
        path: 路径字符串
        value: 要设置的值
        
    Returns:
        修改后的数据（原地修改）
    """
    parts = parse_json_path(path)
    current = data
    
    for i, part in enumerate(parts[:-1]):
        next_part = parts[i + 1]
        
        if isinstance(current, dict):
            if part not in current:
                # 创建中间结构
                current[part] = [] if next_part.isdigit() or next_part == '*' else {}
            current = current[part]
        elif isinstance(current, list):
            index = int(part)
            while len(current) <= index:
                current.append(None)
            if current[index] is None:
                current[index] = [] if next_part.isdigit() or next_part == '*' else {}
            current = current[index]
    
    # 设置最终值
    last_part = parts[-1]
    if isinstance(current, dict):
        current[last_part] = value
    elif isinstance(current, list):
        index = int(last_part)
        while len(current) <= index:
            current.append(None)
        current[index] = value
    
    return data


def has_path(data: Union[Dict, List], path: str) -> bool:
    """
    检查路径是否存在。
    
    Args:
        data: JSON 数据
        path: 路径字符串
        
    Returns:
        路径是否存在
    """
    try:
        parts = parse_json_path(path)
        current = data
        
        for part in parts:
            if isinstance(current, dict):
                if part not in current:
                    return False
                current = current[part]
            elif isinstance(current, list):
                if part == '*':
                    return True
                index = int(part)
                if index < 0 or index >= len(current):
                    return False
                current = current[index]
            else:
                return False
        
        return True
    except (KeyError, IndexError, ValueError, TypeError):
        return False


def delete_value(data: Union[Dict, List], path: str) -> bool:
    """
    删除指定路径的值。
    
    Args:
        data: JSON 数据
        path: 路径字符串
        
    Returns:
        是否成功删除
    """
    try:
        parts = parse_json_path(path)
        current = data
        
        for part in parts[:-1]:
            if isinstance(current, dict):
                current = current[part]
            elif isinstance(current, list):
                index = int(part)
                current = current[index]
        
        last_part = parts[-1]
        if isinstance(current, dict):
            del current[last_part]
        elif isinstance(current, list):
            index = int(last_part)
            del current[index]
        
        return True
    except (KeyError, IndexError, ValueError, TypeError):
        return False


def parse_json_path(path: str) -> List[str]:
    """
    解析 JSON 路径字符串为部分列表。
    支持：'a.b.c', 'a[0].b', 'a.b[2]', 'items[*].name'
    
    Args:
        path: 路径字符串
        
    Returns:
        路径部分列表
    """
    if not path or path == '$':
        return []
    
    # 移除开头的 $
    if path.startswith('$.'):
        path = path[2:]
    elif path.startswith('$'):
        path = path[1:]
    
    parts = []
    current = ""
    i = 0
    
    while i < len(path):
        char = path[i]
        
        if char == '.':
            if current:
                parts.append(current)
                current = ""
            i += 1
        elif char == '[':
            if current:
                parts.append(current)
                current = ""
            # 找到对应的 ]
            j = i + 1
            while j < len(path) and path[j] != ']':
                j += 1
            bracket_content = path[i+1:j]
            parts.append(bracket_content.strip("'\"") if bracket_content not in ('*', '') else bracket_content)
            i = j + 1
        else:
            current += char
            i += 1
    
    if current:
        parts.append(current)
    
    return parts


# ============================================================================
# JSON 展平和嵌套
# ============================================================================

def flatten_json(
    data: Dict[str, Any],
    separator: str = '.',
    array_separator: str = '[',
    array_end: str = ']',
    preserve_arrays: bool = False
) -> Dict[str, Any]:
    """
    将嵌套 JSON 展平为单层字典。
    
    Args:
        data: 嵌套的 JSON 对象
        separator: 键分隔符
        array_separator: 数组分隔符开始
        array_end: 数组分隔符结束
        preserve_arrays: 是否保留数组为整体
        
    Returns:
        展平后的字典
    """
    result = {}
    
    def flatten(obj: Any, prefix: str = ""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{prefix}{separator}{key}" if prefix else key
                flatten(value, new_key)
        elif isinstance(obj, list) and not preserve_arrays:
            for i, value in enumerate(obj):
                new_key = f"{prefix}{array_separator}{i}{array_end}"
                flatten(value, new_key)
        else:
            result[prefix] = obj
    
    flatten(data)
    return result


def unflatten_json(
    data: Dict[str, Any],
    separator: str = '.',
    array_pattern: str = r'\[(\d+)\]'
) -> Dict[str, Any]:
    """
    将展平的字典还原为嵌套 JSON 对象。
    
    Args:
        data: 展平的字典
        separator: 键分隔符
        array_pattern: 数组索引匹配模式
        
    Returns:
        嵌套的 JSON 对象
    """
    result = {}
    
    for key, value in data.items():
        parts = []
        current = ""
        i = 0
        
        while i < len(key):
            char = key[i]
            
            if char == separator:
                if current:
                    parts.append(current)
                    current = ""
                i += 1
            elif char == '[':
                if current:
                    parts.append(current)
                    current = ""
                # 找到对应的 ]
                j = i + 1
                while j < len(key) and key[j] != ']':
                    j += 1
                index_str = key[i+1:j]
                if index_str.isdigit():
                    parts.append(int(index_str))
                i = j + 1
            else:
                current += char
                i += 1
        
        if current:
            parts.append(current)
        
        # 构建嵌套结构
        current_obj = result
        for i, part in enumerate(parts[:-1]):
            next_part = parts[i + 1]
            
            if isinstance(part, int):
                # 数组索引
                if not isinstance(current_obj, list):
                    current_obj = []
                while len(current_obj) <= part:
                    current_obj.append(None)
                if current_obj[part] is None:
                    current_obj[part] = [] if isinstance(next_part, int) else {}
                current_obj = current_obj[part]
            else:
                # 字典键
                if part not in current_obj:
                    current_obj[part] = [] if isinstance(next_part, int) else {}
                current_obj = current_obj[part]
        
        # 设置最终值
        last_part = parts[-1]
        if isinstance(last_part, int):
            while len(current_obj) <= last_part:
                current_obj.append(None)
            current_obj[last_part] = value
        else:
            current_obj[last_part] = value
    
    return result


# ============================================================================
# JSON 搜索
# ============================================================================

def find_all(
    data: Any,
    key: Optional[str] = None,
    value: Any = None,
    path_prefix: str = ""
) -> List[JsonPath]:
    """
    在 JSON 中查找所有匹配的键或值。
    
    Args:
        data: JSON 数据
        key: 要查找的键名（可选）
        value: 要查找的值（可选）
        path_prefix: 路径前缀
        
    Returns:
        匹配的 JsonPath 列表
    """
    results = []
    
    def search(obj: Any, path: str):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}.{k}" if path else k
                if key is not None and k == key:
                    results.append(JsonPath(path=new_path, value=v))
                if value is not None and v == value:
                    results.append(JsonPath(path=new_path, value=v))
                search(v, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                if value is not None and item == value:
                    results.append(JsonPath(path=new_path, value=item))
                search(item, new_path)
    
    search(data, path_prefix)
    return results


def find_first(
    data: Any,
    key: Optional[str] = None,
    value: Any = None,
    path_prefix: str = ""
) -> Optional[JsonPath]:
    """
    在 JSON 中查找第一个匹配的键或值。
    
    Args:
        data: JSON 数据
        key: 要查找的键名（可选）
        value: 要查找的值（可选）
        path_prefix: 路径前缀
        
    Returns:
        匹配的 JsonPath 或 None
    """
    def search(obj: Any, path: str) -> Optional[JsonPath]:
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}.{k}" if path else k
                if key is not None and k == key:
                    return JsonPath(path=new_path, value=v)
                if value is not None and v == value:
                    return JsonPath(path=new_path, value=v)
                result = search(v, new_path)
                if result:
                    return result
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                if value is not None and item == value:
                    return JsonPath(path=new_path, value=item)
                result = search(item, new_path)
                if result:
                    return result
        return None
    
    return search(data, path_prefix)


def grep_json(
    data: Any,
    pattern: str,
    ignore_case: bool = False,
    search_keys: bool = True,
    search_values: bool = True
) -> List[JsonPath]:
    """
    使用正则表达式搜索 JSON。
    
    Args:
        data: JSON 数据
        pattern: 正则表达式模式
        ignore_case: 是否忽略大小写
        search_keys: 是否搜索键
        search_values: 是否搜索值
        
    Returns:
        匹配的 JsonPath 列表
    """
    results = []
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    
    def search(obj: Any, path: str):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}.{k}" if path else k
                if search_keys and regex.search(k):
                    results.append(JsonPath(path=new_path, value=v))
                if search_values and isinstance(v, str) and regex.search(v):
                    results.append(JsonPath(path=new_path, value=v))
                if not isinstance(v, str):
                    search(v, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                if search_values and isinstance(item, str) and regex.search(item):
                    results.append(JsonPath(path=new_path, value=item))
                elif not isinstance(item, str):
                    search(item, new_path)
    
    search(data, "")
    return results


# ============================================================================
# JSON 过滤和转换
# ============================================================================

def filter_json(
    data: Any,
    predicate: Callable[[str, Any], bool],
    path: str = ""
) -> Any:
    """
    过滤 JSON 数据，保留满足条件的键值对。
    
    Args:
        data: JSON 数据
        predicate: 过滤函数 (path, value) -> bool
        path: 当前路径
        
    Returns:
        过滤后的数据
    """
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            new_path = f"{path}.{k}" if path else k
            if predicate(new_path, v):
                filtered_value = filter_json(v, predicate, new_path)
                result[k] = filtered_value
        return result
    elif isinstance(data, list):
        result = []
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            if predicate(new_path, item):
                filtered_item = filter_json(item, predicate, new_path)
                result.append(filtered_item)
        return result
    else:
        return data


def map_json(
    data: Any,
    mapper: Callable[[str, Any], Any],
    path: str = ""
) -> Any:
    """
    映射转换 JSON 数据中的每个值。
    
    Args:
        data: JSON 数据
        mapper: 转换函数 (path, value) -> new_value
        path: 当前路径
        
    Returns:
        转换后的数据
    """
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            new_path = f"{path}.{k}" if path else k
            if isinstance(v, (dict, list)):
                result[k] = map_json(v, mapper, new_path)
            else:
                result[k] = mapper(new_path, v)
        return result
    elif isinstance(data, list):
        result = []
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            if isinstance(item, (dict, list)):
                result.append(map_json(item, mapper, new_path))
            else:
                result.append(mapper(new_path, item))
        return result
    else:
        return mapper(path, data)


# ============================================================================
# JSON 差异比较
# ============================================================================

def diff_json(
    old_data: Any,
    new_data: Any,
    path: str = ""
) -> List[JsonDiff]:
    """
    比较两个 JSON 的差异。
    
    Args:
        old_data: 原始 JSON 数据
        new_data: 新的 JSON 数据
        path: 当前路径
        
    Returns:
        差异列表
    """
    diffs = []
    
    # 类型不同
    if type(old_data) != type(new_data):
        diffs.append(JsonDiff(
            path=path,
            old_value=old_data,
            new_value=new_data,
            change_type='changed'
        ))
        return diffs
    
    # 字典比较
    if isinstance(old_data, dict):
        all_keys = set(old_data.keys()) | set(new_data.keys())
        for key in all_keys:
            new_path = f"{path}.{key}" if path else key
            if key not in old_data:
                diffs.append(JsonDiff(
                    path=new_path,
                    old_value=None,
                    new_value=new_data[key],
                    change_type='added'
                ))
            elif key not in new_data:
                diffs.append(JsonDiff(
                    path=new_path,
                    old_value=old_data[key],
                    new_value=None,
                    change_type='removed'
                ))
            else:
                diffs.extend(diff_json(old_data[key], new_data[key], new_path))
    
    # 列表比较
    elif isinstance(old_data, list):
        max_len = max(len(old_data), len(new_data))
        for i in range(max_len):
            new_path = f"{path}[{i}]"
            if i >= len(old_data):
                diffs.append(JsonDiff(
                    path=new_path,
                    old_value=None,
                    new_value=new_data[i],
                    change_type='added'
                ))
            elif i >= len(new_data):
                diffs.append(JsonDiff(
                    path=new_path,
                    old_value=old_data[i],
                    new_value=None,
                    change_type='removed'
                ))
            else:
                diffs.extend(diff_json(old_data[i], new_data[i], new_path))
    
    # 基本类型比较
    elif old_data != new_data:
        diffs.append(JsonDiff(
            path=path,
            old_value=old_data,
            new_value=new_data,
            change_type='changed'
        ))
    
    return diffs


def diff_summary(diffs: List[JsonDiff]) -> Dict[str, int]:
    """
    生成差异摘要统计。
    
    Args:
        diffs: 差异列表
        
    Returns:
        统计字典
    """
    summary = {'added': 0, 'removed': 0, 'changed': 0}
    for diff in diffs:
        summary[diff.change_type] = summary.get(diff.change_type, 0) + 1
    return summary


# ============================================================================
# JSON 合并
# ============================================================================

def merge_json(
    base: Dict[str, Any],
    *overlays: Dict[str, Any],
    deep: bool = True,
    arrays: str = 'replace'  # 'replace', 'concat', 'merge'
) -> Dict[str, Any]:
    """
    合并多个 JSON 对象。
    
    Args:
        base: 基础对象
        overlays: 要覆盖的对象
        deep: 是否深度合并
        arrays: 数组合并策略
        
    Returns:
        合并后的对象
    """
    result = deepcopy(base)
    
    for overlay in overlays:
        result = _merge_two(result, overlay, deep, arrays)
    
    return result


def _merge_two(
    base: Dict[str, Any],
    overlay: Dict[str, Any],
    deep: bool,
    arrays: str
) -> Dict[str, Any]:
    """合并两个对象"""
    result = deepcopy(base)
    
    for key, value in overlay.items():
        if key in result and deep:
            base_value = result[key]
            
            if isinstance(base_value, dict) and isinstance(value, dict):
                result[key] = _merge_two(base_value, value, deep, arrays)
            elif isinstance(base_value, list) and isinstance(value, list):
                if arrays == 'concat':
                    result[key] = base_value + value
                elif arrays == 'merge':
                    max_len = max(len(base_value), len(value))
                    merged = []
                    for i in range(max_len):
                        if i < len(base_value) and i < len(value):
                            if isinstance(base_value[i], dict) and isinstance(value[i], dict):
                                merged.append(_merge_two(base_value[i], value[i], deep, arrays))
                            else:
                                merged.append(value[i])
                        elif i < len(value):
                            merged.append(value[i])
                        else:
                            merged.append(base_value[i])
                    result[key] = merged
                else:  # replace
                    result[key] = deepcopy(value)
            else:
                result[key] = deepcopy(value)
        else:
            result[key] = deepcopy(value)
    
    return result


# ============================================================================
# JSON 统计
# ============================================================================

def json_stats(data: Any) -> Dict[str, Any]:
    """
    统计 JSON 数据的信息。
    
    Args:
        data: JSON 数据
        
    Returns:
        统计信息字典
    """
    stats = {
        'total_keys': 0,
        'total_values': 0,
        'max_depth': 0,
        'types': {t.value: 0 for t in JsonType},
        'size_bytes': len(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    }
    
    def count(obj: Any, depth: int):
        stats['max_depth'] = max(stats['max_depth'], depth)
        stats['types'][get_json_type(obj).value] += 1
        
        if isinstance(obj, dict):
            stats['total_keys'] += len(obj)
            stats['total_values'] += len(obj)
            for v in obj.values():
                count(v, depth + 1)
        elif isinstance(obj, list):
            stats['total_values'] += len(obj)
            for item in obj:
                count(item, depth + 1)
    
    count(data, 1)
    return stats


# ============================================================================
# JSON 提取和选择
# ============================================================================

def select_keys(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    从 JSON 对象中选择指定的键。
    
    Args:
        data: JSON 对象
        keys: 要选择的键列表
        
    Returns:
        只包含指定键的新对象
    """
    return {k: deepcopy(v) for k, v in data.items() if k in keys}


def omit_keys(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    从 JSON 对象中排除指定的键。
    
    Args:
        data: JSON 对象
        keys: 要排除的键列表
        
    Returns:
        不包含指定键的新对象
    """
    return {k: deepcopy(v) for k, v in data.items() if k not in keys}


def pick_path(data: Any, paths: List[str]) -> Dict[str, Any]:
    """
    选择多个路径的值。
    
    Args:
        data: JSON 数据
        paths: 路径列表
        
    Returns:
        路径到值的映射
    """
    return {path: get_value(data, path) for path in paths}


# ============================================================================
# JSON 遍历
# ============================================================================

def walk_json(data: Any) -> Iterator[Tuple[str, Any]]:
    """
    遍历 JSON 中的所有值。
    
    Args:
        data: JSON 数据
        
    Yields:
        (path, value) 元组
    """
    def walk(obj: Any, path: str):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}.{k}" if path else k
                yield new_path, v
                yield from walk(v, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                yield new_path, item
                yield from walk(item, new_path)
    
    yield from walk(data, "")


def get_all_paths(data: Any) -> List[str]:
    """
    获取 JSON 中所有路径列表。
    
    Args:
        data: JSON 数据
        
    Returns:
        路径列表
    """
    return [path for path, _ in walk_json(data)]


def get_all_values(data: Any) -> List[Any]:
    """
    获取 JSON 中所有值列表。
    
    Args:
        data: JSON 数据
        
    Returns:
        值列表
    """
    return [value for _, value in walk_json(data)]


# ============================================================================
# JSON 克隆和深拷贝
# ============================================================================

def deep_clone(data: Any) -> Any:
    """
    深度克隆 JSON 数据。
    
    Args:
        data: JSON 数据
        
    Returns:
        克隆后的数据
    """
    return deepcopy(data)


def deep_equals(a: Any, b: Any) -> bool:
    """
    深度比较两个 JSON 值是否相等。
    
    Args:
        a: 第一个值
        b: 第二个值
        
    Returns:
        是否相等
    """
    if type(a) != type(b):
        return False
    
    if isinstance(a, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(deep_equals(a[k], b[k]) for k in a)
    elif isinstance(a, list):
        if len(a) != len(b):
            return False
        return all(deep_equals(x, y) for x, y in zip(a, b))
    else:
        return a == b


# ============================================================================
# JSON 安全操作
# ============================================================================

def safe_get(data: Any, *keys, default: Any = None) -> Any:
    """
    安全获取嵌套值，避免 KeyError/IndexError。
    
    Args:
        data: JSON 数据
        *keys: 键序列
        default: 默认值
        
    Returns:
        找到的值或默认值
    """
    current = data
    for key in keys:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return default
    return current


def safe_string(json_string: str) -> Tuple[bool, Any]:
    """
    安全解析 JSON 字符串。
    
    Args:
        json_string: JSON 字符串
        
    Returns:
        (是否成功, 数据或错误消息)
    """
    try:
        data = json.loads(json_string)
        return True, data
    except json.JSONDecodeError as e:
        return False, f"JSON 解析错误: {e.msg} (行 {e.lineno}, 列 {e.colno})"


# ============================================================================
# JsonUtils 类 - 面向对象接口
# ============================================================================

class JsonUtils:
    """
    JSON 工具类，提供面向对象的接口。
    
    使用示例:
        jutil = JsonUtils(data)
        value = jutil.get('a.b.c')
        jutil.set('a.b.d', 'new value')
        flat = jutil.flatten()
    """
    
    def __init__(self, data: Any = None):
        """初始化"""
        self._data = data if data is not None else {}
    
    @property
    def data(self) -> Any:
        """获取数据"""
        return self._data
    
    @data.setter
    def data(self, value: Any):
        """设置数据"""
        self._data = value
    
    @classmethod
    def from_string(cls, json_string: str) -> 'JsonUtils':
        """从 JSON 字符串创建"""
        return cls(json.loads(json_string))
    
    @classmethod
    def from_file(cls, filepath: str, encoding: str = 'utf-8') -> 'JsonUtils':
        """从文件创建"""
        with open(filepath, 'r', encoding=encoding) as f:
            return cls(json.load(f))
    
    def to_string(self, indent: int = 2, ensure_ascii: bool = False) -> str:
        """转换为 JSON 字符串"""
        return format_json(self._data, indent=indent, ensure_ascii=ensure_ascii)
    
    def to_file(self, filepath: str, indent: int = 2, encoding: str = 'utf-8'):
        """保存到文件"""
        with open(filepath, 'w', encoding=encoding) as f:
            json.dump(self._data, f, indent=indent, ensure_ascii=False)
    
    def get(self, path: str, default: Any = None) -> Any:
        """获取路径值"""
        return get_value(self._data, path, default)
    
    def set(self, path: str, value: Any) -> 'JsonUtils':
        """设置路径值"""
        set_value(self._data, path, value)
        return self
    
    def has(self, path: str) -> bool:
        """检查路径是否存在"""
        return has_path(self._data, path)
    
    def delete(self, path: str) -> bool:
        """删除路径值"""
        return delete_value(self._data, path)
    
    def find(self, key: str = None, value: Any = None) -> List[JsonPath]:
        """查找键或值"""
        return find_all(self._data, key, value)
    
    def grep(self, pattern: str, ignore_case: bool = False) -> List[JsonPath]:
        """正则搜索"""
        return grep_json(self._data, pattern, ignore_case)
    
    def flatten(self, separator: str = '.') -> Dict[str, Any]:
        """展平"""
        return flatten_json(self._data, separator) if isinstance(self._data, dict) else {}
    
    def diff(self, other: Any) -> List[JsonDiff]:
        """比较差异"""
        return diff_json(self._data, other)
    
    def merge(self, *others: Dict[str, Any], deep: bool = True) -> 'JsonUtils':
        """合并"""
        self._data = merge_json(self._data, *others, deep=deep)
        return self
    
    def stats(self) -> Dict[str, Any]:
        """统计信息"""
        return json_stats(self._data)
    
    def walk(self) -> Iterator[Tuple[str, Any]]:
        """遍历"""
        return walk_json(self._data)
    
    def paths(self) -> List[str]:
        """所有路径"""
        return get_all_paths(self._data)
    
    def clone(self) -> 'JsonUtils':
        """克隆"""
        return JsonUtils(deep_clone(self._data))
    
    def __repr__(self):
        return f"JsonUtils({self.to_string()[:100]}...)"
    
    def __str__(self):
        return self.to_string()


# ============================================================================
# 便捷函数
# ============================================================================

def loads(json_string: str, default: Any = None) -> Any:
    """
    安全的 JSON 解析，失败返回默认值。
    
    Args:
        json_string: JSON 字符串
        default: 默认值
        
    Returns:
        解析后的数据或默认值
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return default


def dumps(data: Any, indent: int = 2, ensure_ascii: bool = False) -> str:
    """
    格式化 JSON 数据为字符串。
    
    Args:
        data: JSON 数据
        indent: 缩进空格数
        ensure_ascii: 是否转义非 ASCII 字符
        
    Returns:
        JSON 字符串
    """
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)


def load_file(filepath: str, encoding: str = 'utf-8', default: Any = None) -> Any:
    """
    从文件加载 JSON。
    
    Args:
        filepath: 文件路径
        encoding: 文件编码
        default: 默认值
        
    Returns:
        解析后的数据或默认值
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_file(
    data: Any,
    filepath: str,
    indent: int = 2,
    encoding: str = 'utf-8',
    ensure_ascii: bool = False
) -> bool:
    """
    保存 JSON 到文件。
    
    Args:
        data: JSON 数据
        filepath: 文件路径
        indent: 缩进空格数
        encoding: 文件编码
        ensure_ascii: 是否转义非 ASCII 字符
        
    Returns:
        是否成功
    """
    try:
        with open(filepath, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
        return True
    except (IOError, TypeError):
        return False