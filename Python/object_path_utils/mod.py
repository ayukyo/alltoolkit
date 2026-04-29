"""
Object Path Utils - 对象路径操作工具

通过路径字符串访问和操作嵌套对象，支持字典、列表、对象属性。

功能:
- get: 通过路径获取值
- set: 通过路径设置值
- delete: 通过路径删除值
- has: 检查路径是否存在
- paths: 列出所有路径
- flatten: 扁平化对象
- unflatten: 反扁平化对象

零外部依赖，仅使用 Python 标准库。
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import re


class ObjectPathError(Exception):
    """对象路径操作错误基类"""
    pass


class PathNotFoundError(ObjectPathError):
    """路径不存在错误"""
    pass


class InvalidPathError(ObjectPathError):
    """无效路径错误"""
    pass


def _parse_path(path: Union[str, List[str]]) -> List[Union[str, int]]:
    """
    解析路径字符串为路径段列表
    
    Args:
        path: 路径字符串，如 "user.profile.name" 或 "users[0].name"
              也可以是已解析的路径段列表
    
    Returns:
        路径段列表，如 ['user', 'profile', 'name'] 或 ['users', 0, 'name']
    
    Examples:
        >>> _parse_path("user.name")
        ['user', 'name']
        >>> _parse_path("users[0].name")
        ['users', 0, 'name']
        >>> _parse_path("data.items[2].value")
        ['data', 'items', 2, 'value']
    """
    if isinstance(path, list):
        return path
    
    if not path or not isinstance(path, str):
        return []
    
    segments = []
    # 匹配路径段: name 或 [index] 或 .name
    pattern = r'([^.[\]]+)|\[(\d+)\]'
    
    for match in re.finditer(pattern, path):
        if match.group(1) is not None:
            # 属性名
            segments.append(match.group(1))
        elif match.group(2) is not None:
            # 数组索引
            segments.append(int(match.group(2)))
    
    return segments


def _get_value(obj: Any, key: Union[str, int]) -> Any:
    """
    从对象中获取值
    
    Args:
        obj: 源对象
        key: 键名或索引
    
    Returns:
        对应的值
    
    Raises:
        KeyError: 字典键不存在
        IndexError: 列表索引越界
        AttributeError: 属性不存在
    """
    if isinstance(obj, dict):
        return obj[key]
    elif isinstance(obj, list):
        return obj[key]
    elif isinstance(obj, (tuple,)):
        return obj[key]
    else:
        return getattr(obj, str(key))


def _set_value(obj: Any, key: Union[str, int], value: Any) -> None:
    """
    在对象中设置值
    
    Args:
        obj: 目标对象
        key: 键名或索引
        value: 要设置的值
    
    Raises:
        KeyError: 字典键不存在（严格模式）
        IndexError: 列表索引越界
    """
    if isinstance(obj, dict):
        obj[key] = value
    elif isinstance(obj, list):
        if isinstance(key, int):
            # 扩展列表以适应索引
            while len(obj) <= key:
                obj.append(None)
            obj[key] = value
        else:
            raise InvalidPathError(f"Cannot use string key '{key}' on list")
    elif isinstance(obj, tuple):
        raise InvalidPathError("Cannot modify tuple")
    else:
        setattr(obj, str(key), value)


def _delete_value(obj: Any, key: Union[str, int]) -> bool:
    """
    从对象中删除值
    
    Args:
        obj: 源对象
        key: 键名或索引
    
    Returns:
        是否成功删除
    """
    try:
        if isinstance(obj, dict):
            del obj[key]
            return True
        elif isinstance(obj, list):
            if isinstance(key, int) and 0 <= key < len(obj):
                obj.pop(key)
                return True
        elif hasattr(obj, str(key)):
            delattr(obj, str(key))
            return True
    except (KeyError, IndexError, AttributeError):
        pass
    return False


def _has_key(obj: Any, key: Union[str, int]) -> bool:
    """
    检查对象是否包含键
    
    Args:
        obj: 源对象
        key: 键名或索引
    
    Returns:
        是否包含键
    """
    if isinstance(obj, dict):
        return key in obj
    elif isinstance(obj, (list, tuple)):
        return isinstance(key, int) and 0 <= key < len(obj)
    else:
        return hasattr(obj, str(key))


def get(obj: Any, path: Union[str, List[str]], default: Any = None) -> Any:
    """
    通过路径获取对象中的值
    
    Args:
        obj: 源对象（字典、列表、对象）
        path: 路径字符串或路径段列表
              格式: "a.b.c" 或 "items[0].name"
        default: 路径不存在时的默认值
    
    Returns:
        找到的值或默认值
    
    Examples:
        >>> data = {"user": {"name": "Alice", "age": 30}}
        >>> get(data, "user.name")
        'Alice'
        >>> get(data, "user.email", "unknown@example.com")
        'unknown@example.com'
        >>> get(data, ["user", "name"])
        'Alice'
    """
    segments = _parse_path(path)
    
    # 空路径返回默认值
    if not segments:
        return default
    
    current = obj
    for segment in segments:
        try:
            current = _get_value(current, segment)
        except (KeyError, IndexError, AttributeError, TypeError):
            return default
    
    return current


def set(obj: Any, path: Union[str, List[str]], value: Any, 
        create_missing: bool = True) -> Any:
    """
    通过路径设置对象中的值
    
    Args:
        obj: 目标对象
        path: 路径字符串或路径段列表
        value: 要设置的值
        create_missing: 是否创建不存在的中间路径
    
    Returns:
        修改后的对象
    
    Raises:
        PathNotFoundError: 路径不存在且 create_missing=False
    
    Examples:
        >>> data = {}
        >>> set(data, "user.name", "Alice")
        {'user': {'name': 'Alice'}}
        >>> set(data, "items[0].value", 100)
        {'user': {'name': 'Alice'}, 'items': [{'value': 100}]}
    """
    segments = _parse_path(path)
    
    if not segments:
        return obj
    
    current = obj
    for i, segment in enumerate(segments[:-1]):
        next_segment = segments[i + 1]
        
        if not _has_key(current, segment):
            if create_missing:
                # 创建中间对象
                if isinstance(next_segment, int):
                    new_value = []
                else:
                    new_value = {}
                _set_value(current, segment, new_value)
                current = new_value
            else:
                raise PathNotFoundError(f"Path segment '{segment}' not found")
        else:
            current = _get_value(current, segment)
    
    # 设置最终值
    final_key = segments[-1]
    _set_value(current, final_key, value)
    
    return obj


def delete(obj: Any, path: Union[str, List[str]]) -> bool:
    """
    通过路径删除对象中的值
    
    Args:
        obj: 源对象
        path: 路径字符串或路径段列表
    
    Returns:
        是否成功删除
    
    Examples:
        >>> data = {"user": {"name": "Alice", "age": 30}}
        >>> delete(data, "user.age")
        True
        >>> data
        {'user': {'name': 'Alice'}}
        >>> delete(data, "user.email")
        False
    """
    segments = _parse_path(path)
    
    if not segments:
        return False
    
    # 导航到父对象
    current = obj
    for segment in segments[:-1]:
        try:
            current = _get_value(current, segment)
        except (KeyError, IndexError, AttributeError, TypeError):
            return False
    
    # 删除最后的键
    final_key = segments[-1]
    return _delete_value(current, final_key)


def has(obj: Any, path: Union[str, List[str]]) -> bool:
    """
    检查路径是否存在
    
    Args:
        obj: 源对象
        path: 路径字符串或路径段列表
    
    Returns:
        路径是否存在
    
    Examples:
        >>> data = {"user": {"name": "Alice"}}
        >>> has(data, "user.name")
        True
        >>> has(data, "user.age")
        False
    """
    segments = _parse_path(path)
    
    current = obj
    for segment in segments:
        if not _has_key(current, segment):
            return False
        try:
            current = _get_value(current, segment)
        except (KeyError, IndexError, AttributeError, TypeError):
            return False
    
    return True


def paths(obj: Any, parent: str = "", max_depth: int = 10) -> List[str]:
    """
    列出对象中的所有路径
    
    Args:
        obj: 源对象
        parent: 父路径前缀
        max_depth: 最大递归深度（防止循环引用）
    
    Returns:
        所有路径的列表
    
    Examples:
        >>> data = {"user": {"name": "Alice", "age": 30}}
        >>> paths(data)
        ['user', 'user.name', 'user.age']
    """
    if max_depth <= 0:
        return [parent] if parent else []
    
    result = []
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{parent}.{key}" if parent else key
            result.append(path)
            if isinstance(value, (dict, list)) and value:
                result.extend(paths(value, path, max_depth - 1))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            path = f"{parent}[{i}]"
            result.append(path)
            if isinstance(value, (dict, list)) and value:
                result.extend(paths(value, path, max_depth - 1))
    
    return result


def flatten(obj: Any, separator: str = ".", prefix: str = "") -> Dict[str, Any]:
    """
    将嵌套对象扁平化为单层字典
    
    Args:
        obj: 源对象
        separator: 路径分隔符
        prefix: 键前缀
    
    Returns:
        扁平化后的字典
    
    Examples:
        >>> data = {"user": {"name": "Alice", "age": 30}}
        >>> flatten(data)
        {'user.name': 'Alice', 'user.age': 30}
    """
    result = {}
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            if isinstance(value, dict) and value:
                result.update(flatten(value, separator, new_key))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    item_key = f"{new_key}[{i}]"
                    if isinstance(item, (dict, list)) and item:
                        result.update(flatten(item, separator, item_key))
                    else:
                        result[item_key] = item
            else:
                result[new_key] = value
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_key = f"{prefix}[{i}]"
            if isinstance(item, (dict, list)) and item:
                result.update(flatten(item, separator, new_key))
            else:
                result[new_key] = item
    else:
        result[prefix] = obj
    
    return result


def unflatten(obj: Dict[str, Any], separator: str = ".") -> Dict[str, Any]:
    """
    将扁平化字典还原为嵌套对象
    
    Args:
        obj: 扁平化的字典
        separator: 路径分隔符
    
    Returns:
        嵌套对象
    
    Examples:
        >>> flat = {"user.name": "Alice", "user.age": 30}
        >>> unflatten(flat)
        {'user': {'name': 'Alice', 'age': 30}}
    """
    result = {}
    
    for key, value in obj.items():
        set(result, key.replace(separator, "."), value)
    
    return result


def pick(obj: Any, *paths: Union[str, List[str]]) -> Dict[str, Any]:
    """
    从对象中选取指定路径的值
    
    Args:
        obj: 源对象
        *paths: 要选取的路径
    
    Returns:
        包含选取路径和值的字典
    
    Examples:
        >>> data = {"user": {"name": "Alice", "age": 30, "email": "alice@example.com"}}
        >>> pick(data, "user.name", "user.age")
        {'user.name': 'Alice', 'user.age': 30}
    """
    result = {}
    for path in paths:
        path_str = path if isinstance(path, str) else ".".join(str(p) for p in path)
        if has(obj, path):
            result[path_str] = get(obj, path)
    return result


def omit(obj: Any, *paths: Union[str, List[str]]) -> Any:
    """
    从对象中排除指定路径的值
    
    Args:
        obj: 源对象
        *paths: 要排除的路径
    
    Returns:
        排除后的新对象（深拷贝）
    
    Examples:
        >>> data = {"user": {"name": "Alice", "age": 30, "email": "alice@example.com"}}
        >>> omit(data, "user.email")
        {'user': {'name': 'Alice', 'age': 30}}
    """
    import copy
    
    # 深拷贝对象
    result = copy.deepcopy(obj)
    
    for path in paths:
        delete(result, path)
    
    return result


def merge(*objects: Any, deep: bool = True) -> Any:
    """
    合并多个对象
    
    Args:
        *objects: 要合并的对象
        deep: 是否深度合并
    
    Returns:
        合并后的对象
    
    Examples:
        >>> merge({"a": 1}, {"b": 2})
        {'a': 1, 'b': 2}
        >>> merge({"user": {"name": "Alice"}}, {"user": {"age": 30}})
        {'user': {'name': 'Alice', 'age': 30}}
    """
    import copy
    
    if not objects:
        return {}
    
    result = copy.deepcopy(objects[0]) if objects else {}
    
    for obj in objects[1:]:
        if deep:
            _deep_merge(result, obj)
        else:
            if isinstance(result, dict) and isinstance(obj, dict):
                result.update(obj)
    
    return result


def _deep_merge(target: Any, source: Any) -> Any:
    """深度合并辅助函数"""
    import copy
    
    if isinstance(target, dict) and isinstance(source, dict):
        for key, value in source.items():
            if key in target:
                # 目标中已有此键，根据类型决定合并策略
                target_value = target[key]
                if isinstance(target_value, dict) and isinstance(value, dict):
                    # 都是字典，深度合并
                    _deep_merge(target_value, value)
                elif isinstance(target_value, list) and isinstance(value, list):
                    # 都是列表，合并列表
                    target_value.extend(copy.deepcopy(value))
                else:
                    # 其他情况，直接覆盖
                    target[key] = copy.deepcopy(value)
            else:
                # 目标中没有此键，直接添加
                target[key] = copy.deepcopy(value)
    elif isinstance(target, list) and isinstance(source, list):
        target.extend(copy.deepcopy(source))
    
    return target


# 便捷类
class ObjectPath:
    """
    对象路径操作类，支持链式调用
    
    Examples:
        >>> op = ObjectPath({"user": {"name": "Alice"}})
        >>> op.get("user.name")
        'Alice'
        >>> op.set("user.age", 30).get("user")
        {'name': 'Alice', 'age': 30}
    """
    
    def __init__(self, obj: Any):
        """初始化"""
        self._obj = obj
    
    def get(self, path: Union[str, List[str]], default: Any = None) -> Any:
        """获取值"""
        return get(self._obj, path, default)
    
    def set(self, path: Union[str, List[str]], value: Any, 
            create_missing: bool = True) -> 'ObjectPath':
        """设置值（返回自身以支持链式调用）"""
        set(self._obj, path, value, create_missing)
        return self
    
    def delete(self, path: Union[str, List[str]]) -> 'ObjectPath':
        """删除值"""
        delete(self._obj, path)
        return self
    
    def has(self, path: Union[str, List[str]]) -> bool:
        """检查路径是否存在"""
        return has(self._obj, path)
    
    def paths(self) -> List[str]:
        """列出所有路径"""
        return paths(self._obj)
    
    def flatten(self, separator: str = ".") -> Dict[str, Any]:
        """扁平化"""
        return flatten(self._obj, separator)
    
    def pick(self, *paths: Union[str, List[str]]) -> Dict[str, Any]:
        """选取路径"""
        return pick(self._obj, *paths)
    
    def omit(self, *paths: Union[str, List[str]]) -> 'ObjectPath':
        """排除路径"""
        return ObjectPath(omit(self._obj, *paths))
    
    @property
    def obj(self) -> Any:
        """获取原始对象"""
        return self._obj
    
    def __repr__(self) -> str:
        return f"ObjectPath({self._obj!r})"


# 导出公共 API
__all__ = [
    'get',
    'set',
    'delete',
    'has',
    'paths',
    'flatten',
    'unflatten',
    'pick',
    'omit',
    'merge',
    'ObjectPath',
    'ObjectPathError',
    'PathNotFoundError',
    'InvalidPathError',
]