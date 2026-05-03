"""
json_flatten_utils - JSON/字典扁平化工具
==========================================

零依赖的字典扁平化和嵌套操作工具库。

功能特性：
- flatten_dict: 将嵌套字典扁平化为单层字典
- unflatten_dict: 将扁平字典还原为嵌套字典
- flatten_list: 将嵌套列表扁平化为一维列表
- deep_merge: 深度合并多个字典
- get_nested_value: 安全获取嵌套值
- set_nested_value: 设置嵌套值
- delete_nested_value: 删除嵌套值
- has_nested_key: 检查嵌套键是否存在
- diff_dicts: 比较两个字典的差异

使用示例：
    >>> from json_flatten_utils import flatten_dict, unflatten_dict
    >>> data = {"a": {"b": {"c": 1}}}
    >>> flat = flatten_dict(data)
    {'a.b.c': 1}
    >>> unflatten_dict(flat)
    {'a': {'b': {'c': 1}}}
"""

import copy
from typing import Any, Dict, List, Optional, Union, Tuple, Set


def flatten_dict(
    data: Dict[str, Any],
    separator: str = ".",
    prefix: str = "",
    max_depth: Optional[int] = None,
    current_depth: int = 0,
    flatten_lists: bool = False,
    list_index_format: str = "[{}]",
) -> Dict[str, Any]:
    """
    将嵌套字典扁平化为单层字典。
    
    Args:
        data: 要扁平化的字典
        separator: 键之间的分隔符，默认为点号
        prefix: 键前缀
        max_depth: 最大扁平化深度，None表示无限制
        current_depth: 当前深度（内部使用）
        flatten_lists: 是否扁平化列表中的字典
        list_index_format: 列表索引格式，例如 "[{}]" 或 ".{}" 或 "_{}"
        
    Returns:
        扁平化后的字典
        
    Examples:
        >>> flatten_dict({"a": {"b": 1}})
        {'a.b': 1}
        >>> flatten_dict({"a": {"b": {"c": 1}}}, max_depth=1)
        {'a.b': {'c': 1}}
        >>> flatten_dict({"a": [{"b": 1}, {"c": 2}]}, flatten_lists=True)
        {'a[0].b': 1, 'a[1].c': 2}
    """
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict, got {type(data).__name__}")
    
    result = {}
    
    for key, value in data.items():
        new_key = f"{prefix}{separator}{key}" if prefix else key
        
        if isinstance(value, dict) and (max_depth is None or current_depth < max_depth):
            # 递归扁平化嵌套字典
            result.update(
                flatten_dict(
                    value,
                    separator=separator,
                    prefix=new_key,
                    max_depth=max_depth,
                    current_depth=current_depth + 1,
                    flatten_lists=flatten_lists,
                    list_index_format=list_index_format,
                )
            )
        elif isinstance(value, list) and flatten_lists and any(isinstance(item, dict) for item in value):
            # 扁平化列表中的字典
            for idx, item in enumerate(value):
                if isinstance(item, dict):
                    list_key = f"{new_key}{list_index_format.format(idx)}"
                    if max_depth is None or current_depth < max_depth:
                        result.update(
                            flatten_dict(
                                item,
                                separator=separator,
                                prefix=list_key,
                                max_depth=max_depth,
                                current_depth=current_depth + 1,
                                flatten_lists=flatten_lists,
                                list_index_format=list_index_format,
                            )
                        )
                    else:
                        result[list_key] = item
                else:
                    list_key = f"{new_key}{list_index_format.format(idx)}"
                    result[list_key] = item
        else:
            result[new_key] = value
    
    return result


def unflatten_dict(
    data: Dict[str, Any],
    separator: str = ".",
    list_index_pattern: str = r"\[(\d+)\]",
) -> Dict[str, Any]:
    """
    将扁平字典还原为嵌套字典。
    
    Args:
        data: 扁平化的字典
        separator: 键分隔符
        list_index_pattern: 列表索引的正则模式
        
    Returns:
        嵌套字典
        
    Examples:
        >>> unflatten_dict({"a.b": 1})
        {'a': {'b': 1}}
        >>> unflatten_dict({"a.b.c": 1, "a.b.d": 2})
        {'a': {'b': {'c': 1, 'd': 2}}}
        >>> unflatten_dict({"a[0]": 1, "a[1]": 2})
        {'a': [1, 2]}
    """
    import re
    
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict, got {type(data).__name__}")
    
    result = {}
    list_pattern = re.compile(f"^(.+){list_index_pattern}$")
    
    # 收集列表索引信息
    list_indices: Dict[str, Dict[int, Any]] = {}
    regular_keys: List[Tuple[str, Any]] = []
    
    for key, value in data.items():
        match = list_pattern.match(key)
        if match:
            list_key = match.group(1)
            idx = int(match.group(2))
            if list_key not in list_indices:
                list_indices[list_key] = {}
            list_indices[list_key][idx] = value
        else:
            regular_keys.append((key, value))
    
    # 处理普通键
    for key, value in regular_keys:
        parts = key.split(separator)
        current = result
        
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                # 检查下一部分是否是数字（列表索引）
                next_part = parts[i + 1]
                if next_part.isdigit():
                    current[part] = []
                else:
                    current[part] = {}
            
            if isinstance(current[part], list):
                # 处理列表索引
                idx = int(parts[i + 1])
                while len(current[part]) <= idx:
                    current[part].append({})
                current = current[part][idx]
            else:
                current = current[part]
        
        # 设置最终值
        final_key = parts[-1]
        if final_key.isdigit():
            # 列表索引作为键
            idx = int(final_key)
            if not isinstance(current, list):
                # 需要转换
                parent = result
                for part in parts[:-2]:
                    parent = parent[part]
                parent_key = parts[-2]
                parent[parent_key] = []
                current = parent[parent_key]
            while len(current) <= idx:
                current.append(None)
            current[idx] = value
        else:
            current[final_key] = value
    
    # 处理收集的列表数据
    for list_key, indices_data in list_indices.items():
        parts = list_key.split(separator)
        current = result
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # 构建列表
        max_idx = max(indices_data.keys())
        list_value = [None] * (max_idx + 1)
        for idx, val in indices_data.items():
            list_value[idx] = val
        
        final_key = parts[-1] if parts else list_key
        current[final_key] = list_value
    
    return result


def flatten_list(
    data: List[Any],
    max_depth: Optional[int] = None,
    current_depth: int = 0,
    preserve_types: bool = False,
) -> List[Any]:
    """
    将嵌套列表扁平化为一维列表。
    
    Args:
        data: 要扁平化的列表
        max_depth: 最大扁平化深度，None表示无限制
        current_depth: 当前深度（内部使用）
        preserve_types: 是否保留非列表的可迭代类型（如元组）
        
    Returns:
        扁平化后的列表
        
    Examples:
        >>> flatten_list([1, [2, [3, 4]]])
        [1, 2, 3, 4]
        >>> flatten_list([1, [2, [3, 4]]], max_depth=1)
        [1, 2, [3, 4]]
        >>> flatten_list([(1, 2), [3, 4]], preserve_types=True)
        [(1, 2), 3, 4]
    """
    if not isinstance(data, list):
        raise TypeError(f"Expected list, got {type(data).__name__}")
    
    result = []
    
    for item in data:
        if (
            isinstance(item, list)
            and (max_depth is None or current_depth < max_depth)
        ):
            result.extend(
                flatten_list(
                    item,
                    max_depth=max_depth,
                    current_depth=current_depth + 1,
                    preserve_types=preserve_types,
                )
            )
        elif (
            preserve_types
            and isinstance(item, (tuple, set))
            and (max_depth is None or current_depth < max_depth)
        ):
            result.extend(
                flatten_list(
                    list(item),
                    max_depth=max_depth,
                    current_depth=current_depth + 1,
                    preserve_types=preserve_types,
                )
            )
        else:
            result.append(item)
    
    return result


def deep_merge(
    *dicts: Dict[str, Any],
    overwrite: bool = True,
    merge_lists: bool = False,
    unique_lists: bool = True,
) -> Dict[str, Any]:
    """
    深度合并多个字典。
    
    Args:
        *dicts: 要合并的字典（按顺序合并，后面的覆盖前面的）
        overwrite: 是否覆盖已存在的键
        merge_lists: 是否合并列表
        unique_lists: 合并列表时是否去重
        
    Returns:
        合并后的字典
        
    Examples:
        >>> deep_merge({"a": 1}, {"b": 2})
        {'a': 1, 'b': 2}
        >>> deep_merge({"a": {"b": 1}}, {"a": {"c": 2}})
        {'a': {'b': 1, 'c': 2}}
        >>> deep_merge({"a": [1, 2]}, {"a": [3, 4]}, merge_lists=True)
        {'a': [1, 2, 3, 4]}
    """
    if not dicts:
        return {}
    
    result = {}
    
    for d in dicts:
        if not isinstance(d, dict):
            continue
        
        for key, value in d.items():
            if key not in result:
                result[key] = copy.deepcopy(value)
            elif isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(
                    result[key],
                    value,
                    overwrite=overwrite,
                    merge_lists=merge_lists,
                    unique_lists=unique_lists,
                )
            elif merge_lists and isinstance(result[key], list) and isinstance(value, list):
                if unique_lists:
                    # 去重合并
                    seen = set()
                    merged = []
                    for item in result[key] + value:
                        item_key = str(item) if not isinstance(item, (int, str, float, bool, type(None))) else item
                        if item_key not in seen:
                            seen.add(item_key)
                            merged.append(item)
                    result[key] = merged
                else:
                    result[key] = result[key] + value
            elif overwrite:
                result[key] = copy.deepcopy(value)
    
    return result


def get_nested_value(
    data: Dict[str, Any],
    key_path: Union[str, List[str]],
    separator: str = ".",
    default: Any = None,
    raise_error: bool = False,
) -> Any:
    """
    安全获取嵌套字典中的值。
    
    Args:
        data: 字典数据
        key_path: 键路径，可以是字符串或列表
        separator: 键路径分隔符（当key_path为字符串时使用）
        default: 键不存在时的默认值
        raise_error: 键不存在时是否抛出错误
        
    Returns:
        找到的值或默认值
        
    Examples:
        >>> get_nested_value({"a": {"b": {"c": 1}}}, "a.b.c")
        1
        >>> get_nested_value({"a": {"b": 1}}, ["a", "b"])
        1
        >>> get_nested_value({"a": {"b": 1}}, "a.x", default="N/A")
        'N/A'
    """
    if isinstance(key_path, str):
        keys = key_path.split(separator)
    else:
        keys = list(key_path)
    
    current = data
    
    for key in keys:
        if isinstance(current, dict):
            if key not in current:
                if raise_error:
                    raise KeyError(f"Key '{key}' not found in path '{separator.join(keys)}'")
                return default
            current = current[key]
        elif isinstance(current, list):
            try:
                idx = int(key)
                current = current[idx]
            except (ValueError, IndexError) as e:
                if raise_error:
                    raise KeyError(f"Invalid index '{key}' in path") from e
                return default
        else:
            if raise_error:
                raise KeyError(f"Cannot access key '{key}' on non-dict/list value")
            return default
    
    return current


def set_nested_value(
    data: Dict[str, Any],
    key_path: Union[str, List[str]],
    value: Any,
    separator: str = ".",
    create_parents: bool = True,
) -> Dict[str, Any]:
    """
    设置嵌套字典中的值。
    
    Args:
        data: 字典数据
        key_path: 键路径
        value: 要设置的值
        separator: 键路径分隔符
        create_parents: 是否自动创建父级字典
        
    Returns:
        修改后的字典
        
    Examples:
        >>> set_nested_value({}, "a.b.c", 1)
        {'a': {'b': {'c': 1}}}
        >>> set_nested_value({"a": {}}, ["a", "b"], 2)
        {'a': {'b': 2}}
    """
    if isinstance(key_path, str):
        keys = key_path.split(separator)
    else:
        keys = list(key_path)
    
    if not keys:
        return data
    
    current = data
    
    for i, key in enumerate(keys[:-1]):
        if key not in current:
            if create_parents:
                current[key] = {}
            else:
                raise KeyError(f"Parent key '{key}' does not exist")
        elif not isinstance(current[key], dict):
            if create_parents:
                current[key] = {}
            else:
                raise TypeError(f"Parent key '{key}' is not a dict")
        current = current[key]
    
    current[keys[-1]] = value
    return data


def delete_nested_value(
    data: Dict[str, Any],
    key_path: Union[str, List[str]],
    separator: str = ".",
    raise_error: bool = False,
) -> Dict[str, Any]:
    """
    删除嵌套字典中的值。
    
    Args:
        data: 字典数据
        key_path: 键路径
        separator: 键路径分隔符
        raise_error: 键不存在时是否抛出错误
        
    Returns:
        修改后的字典
        
    Examples:
        >>> delete_nested_value({"a": {"b": 1}}, "a.b")
        {'a': {}}
        >>> delete_nested_value({"a": {"b": 1}}, "a.x")
        {'a': {'b': 1}}
    """
    if isinstance(key_path, str):
        keys = key_path.split(separator)
    else:
        keys = list(key_path)
    
    if not keys:
        return data
    
    current = data
    path = []
    
    for key in keys[:-1]:
        if not isinstance(current, dict) or key not in current:
            if raise_error:
                raise KeyError(f"Key '{key}' not found in path")
            return data
        path.append((current, key))
        current = current[key]
    
    if isinstance(current, dict) and keys[-1] in current:
        del current[keys[-1]]
        
        # 清理空的父级字典
        for parent, key in reversed(path):
            if isinstance(parent[key], dict) and not parent[key]:
                del parent[key]
            else:
                break
    elif raise_error:
        raise KeyError(f"Key '{keys[-1]}' not found")
    
    return data


def has_nested_key(
    data: Dict[str, Any],
    key_path: Union[str, List[str]],
    separator: str = ".",
) -> bool:
    """
    检查嵌套键是否存在。
    
    Args:
        data: 字典数据
        key_path: 键路径
        separator: 键路径分隔符
        
    Returns:
        键是否存在
        
    Examples:
        >>> has_nested_key({"a": {"b": 1}}, "a.b")
        True
        >>> has_nested_key({"a": {"b": 1}}, "a.c")
        False
    """
    try:
        get_nested_value(data, key_path, separator=separator, raise_error=True)
        return True
    except KeyError:
        return False


def diff_dicts(
    dict1: Dict[str, Any],
    dict2: Dict[str, Any],
    separator: str = ".",
    ignore_keys: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """
    比较两个字典的差异。
    
    Args:
        dict1: 第一个字典（基准）
        dict2: 第二个字典（比较）
        separator: 输出键分隔符
        ignore_keys: 要忽略的键集合
        
    Returns:
        包含差异的字典：
        - added: dict2 中新增的键
        - removed: dict2 中移除的键
        - changed: 值不同的键（包含 old 和 new）
        - unchanged: 值相同的键
        
    Examples:
        >>> diff_dicts({"a": 1}, {"a": 1, "b": 2})
        {'added': {'b': 2}, 'removed': {}, 'changed': {}, 'unchanged': {'a': 1}}
        >>> diff_dicts({"a": 1}, {"a": 2})
        {'added': {}, 'removed': {}, 'changed': {'a': {'old': 1, 'new': 2}}, 'unchanged': {}}
    """
    ignore_keys = ignore_keys or set()
    
    def _get_all_keys(d: Dict[str, Any], prefix: str = "") -> Set[str]:
        keys = set()
        for key, value in d.items():
            full_key = f"{prefix}{separator}{key}" if prefix else key
            if full_key not in ignore_keys:
                keys.add(full_key)
                if isinstance(value, dict):
                    keys.update(_get_all_keys(value, full_key))
        return keys
    
    flat1 = flatten_dict(dict1, separator=separator)
    flat2 = flatten_dict(dict2, separator=separator)
    
    keys1 = set(flat1.keys()) - ignore_keys
    keys2 = set(flat2.keys()) - ignore_keys
    
    added_keys = keys2 - keys1
    removed_keys = keys1 - keys2
    common_keys = keys1 & keys2
    
    result = {
        "added": {k: flat2[k] for k in sorted(added_keys)},
        "removed": {k: flat1[k] for k in sorted(removed_keys)},
        "changed": {},
        "unchanged": {},
    }
    
    for key in sorted(common_keys):
        val1 = flat1[key]
        val2 = flat2[key]
        if val1 == val2:
            result["unchanged"][key] = val1
        else:
            result["changed"][key] = {"old": val1, "new": val2}
    
    return result


def dict_paths(
    data: Dict[str, Any],
    separator: str = ".",
    include_values: bool = False,
) -> Union[List[str], Dict[str, Any]]:
    """
    获取字典中所有键的路径列表。
    
    Args:
        data: 字典数据
        separator: 路径分隔符
        include_values: 是否包含值
        
    Returns:
        键路径列表或键值对字典
        
    Examples:
        >>> dict_paths({"a": {"b": 1, "c": 2}})
        ['a.b', 'a.c']
        >>> dict_paths({"a": {"b": 1}}, include_values=True)
        {'a.b': 1}
    """
    flat = flatten_dict(data, separator=separator)
    
    if include_values:
        return flat
    return list(flat.keys())


def dict_depth(data: Dict[str, Any]) -> int:
    """
    计算字典的最大嵌套深度。
    
    Args:
        data: 字典数据
        
    Returns:
        最大深度（从1开始）
        
    Examples:
        >>> dict_depth({"a": 1})
        1
        >>> dict_depth({"a": {"b": {"c": 1}}})
        3
    """
    if not isinstance(data, dict) or not data:
        return 0
    
    max_depth = 1
    for value in data.values():
        if isinstance(value, dict):
            depth = dict_depth(value) + 1
            max_depth = max(max_depth, depth)
    
    return max_depth


def dict_to_tuples(
    data: Dict[str, Any],
    separator: str = ".",
) -> List[Tuple[str, Any]]:
    """
    将字典转换为键值对元组列表。
    
    Args:
        data: 字典数据
        separator: 路径分隔符
        
    Returns:
        键值对元组列表
        
    Examples:
        >>> dict_to_tuples({"a": {"b": 1}})
        [('a.b', 1)]
    """
    flat = flatten_dict(data, separator=separator)
    return list(flat.items())


def tuples_to_dict(
    tuples: List[Tuple[str, Any]],
    separator: str = ".",
) -> Dict[str, Any]:
    """
    将键值对元组列表转换回嵌套字典。
    
    Args:
        tuples: 键值对元组列表
        separator: 路径分隔符
        
    Returns:
        嵌套字典
        
    Examples:
        >>> tuples_to_dict([('a.b', 1)])
        {'a': {'b': 1}}
    """
    return unflatten_dict(dict(tuples), separator=separator)


def pick_keys(
    data: Dict[str, Any],
    keys: List[str],
    separator: str = ".",
) -> Dict[str, Any]:
    """
    从字典中选取指定的键，返回新的嵌套字典。
    
    Args:
        data: 字典数据
        keys: 要选取的键路径列表
        separator: 路径分隔符
        
    Returns:
        包含选取键的新字典
        
    Examples:
        >>> pick_keys({"a": {"b": 1, "c": 2}}, ["a.b"])
        {'a': {'b': 1}}
    """
    result = {}
    for key in keys:
        if has_nested_key(data, key, separator):
            value = get_nested_value(data, key, separator)
            set_nested_value(result, key, value, separator)
    return result


def omit_keys(
    data: Dict[str, Any],
    keys: List[str],
    separator: str = ".",
) -> Dict[str, Any]:
    """
    从字典中排除指定的键，返回新的嵌套字典。
    
    Args:
        data: 字典数据
        keys: 要排除的键路径列表
        separator: 路径分隔符
        
    Returns:
        排除指定键后的新字典
        
    Examples:
        >>> omit_keys({"a": {"b": 1, "c": 2}}, ["a.c"])
        {'a': {'b': 1}}
    """
    result = copy.deepcopy(data)
    for key in keys:
        delete_nested_value(result, key, separator, raise_error=False)
    return result


# 版本信息
__version__ = '1.0.0'
__author__ = 'AllToolkit'
__all__ = [
    'flatten_dict',
    'unflatten_dict',
    'flatten_list',
    'deep_merge',
    'get_nested_value',
    'set_nested_value',
    'delete_nested_value',
    'has_nested_key',
    'diff_dicts',
    'dict_paths',
    'dict_depth',
    'dict_to_tuples',
    'tuples_to_dict',
    'pick_keys',
    'omit_keys',
]