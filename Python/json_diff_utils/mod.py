"""
json_diff_utils - JSON 差异比较工具模块

提供深度 JSON 差异比较、JSON Patch (RFC 6902) 生成与应用、
JSON Merge Patch (RFC 7396) 等功能。
零外部依赖，全部使用 Python 标准库实现。

主要功能：
- 深度 JSON 差异比较（支持嵌套对象和数组）
- 路径化差异报告（如 "user.profile.name" 发生变化）
- JSON Patch (RFC 6902) 生成与应用
- JSON Merge Patch (RFC 7396) 支持
- 差异统计与可视化
- 差异过滤与搜索

作者: AllToolkit
日期: 2026-04-20
"""

from typing import Any, Dict, List, Tuple, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from copy import deepcopy
import json
import re


class DiffOperation(Enum):
    """JSON Patch 操作类型 (RFC 6902)"""
    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"
    MOVE = "move"
    COPY = "copy"
    TEST = "test"


class ChangeType(Enum):
    """变更类型"""
    ADDED = "added"        # 新增
    REMOVED = "removed"    # 删除
    MODIFIED = "modified"  # 修改
    UNCHANGED = "unchanged"  # 未变化


@dataclass
class JsonDiff:
    """JSON 差异项"""
    path: str                    # JSON 路径 (如 "user.profile.name")
    change_type: ChangeType      # 变更类型
    old_value: Optional[Any]     # 旧值
    new_value: Optional[Any]     # 新值
    old_type: Optional[str]      # 旧值类型
    new_type: Optional[str]      # 新值类型
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "path": self.path,
            "change_type": self.change_type.value,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "old_type": self.old_type,
            "new_type": self.new_type
        }
    
    def __repr__(self) -> str:
        if self.change_type == ChangeType.ADDED:
            return f"+ {self.path}: {repr(self.new_value)}"
        elif self.change_type == ChangeType.REMOVED:
            return f"- {self.path}: {repr(self.old_value)}"
        else:
            return f"~ {self.path}: {repr(self.old_value)} -> {repr(self.new_value)}"


@dataclass
class JsonPatch:
    """JSON Patch 操作 (RFC 6902)"""
    op: DiffOperation
    path: str
    value: Optional[Any] = None
    from_path: Optional[str] = None  # 用于 move 和 copy
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {"op": self.op.value, "path": self.path}
        if self.value is not None:
            result["value"] = self.value
        if self.from_path is not None:
            result["from"] = self.from_path
        return result
    
    def __repr__(self) -> str:
        if self.op in (DiffOperation.MOVE, DiffOperation.COPY):
            return f"{self.op.value} {self.from_path} -> {self.path}"
        elif self.op == DiffOperation.REMOVE:
            return f"{self.op.value} {self.path}"
        else:
            return f"{self.op.value} {self.path} = {repr(self.value)}"


@dataclass
class DiffResult:
    """差异比较结果"""
    diffs: List[JsonDiff] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        """计算统计信息"""
        self.stats = {
            "added": 0,
            "removed": 0,
            "modified": 0,
            "unchanged": 0,
            "total": len(self.diffs)
        }
        for diff in self.diffs:
            self.stats[diff.change_type.value] += 1
    
    @property
    def has_changes(self) -> bool:
        """是否有变更"""
        return self.stats["added"] > 0 or self.stats["removed"] > 0 or self.stats["modified"] > 0
    
    def filter_by_type(self, change_type: ChangeType) -> List[JsonDiff]:
        """按变更类型过滤"""
        return [d for d in self.diffs if d.change_type == change_type]
    
    def filter_by_path(self, pattern: str) -> List[JsonDiff]:
        """按路径模式过滤（支持正则表达式）"""
        regex = re.compile(pattern)
        return [d for d in self.diffs if regex.search(d.path)]
    
    def get_path(self, path: str) -> Optional[JsonDiff]:
        """获取指定路径的差异"""
        for diff in self.diffs:
            if diff.path == path:
                return diff
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "diffs": [d.to_dict() for d in self.diffs],
            "stats": self.stats,
            "has_changes": self.has_changes
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def __repr__(self) -> str:
        lines = [f"DiffResult({self.stats['total']} changes)"]
        for diff in self.diffs[:20]:  # 最多显示 20 条
            lines.append(f"  {diff}")
        if len(self.diffs) > 20:
            lines.append(f"  ... and {len(self.diffs) - 20} more")
        return "\n".join(lines)


class JsonDiffer:
    """JSON 差异比较器"""
    
    def __init__(
        self,
        ignore_keys: Optional[List[str]] = None,
        ignore_null: bool = False,
        array_id_field: Optional[str] = None,
        float_tolerance: float = 1e-9
    ):
        """
        初始化差异比较器
        
        Args:
            ignore_keys: 忽略的键列表
            ignore_null: 是否忽略 None 值的比较
            array_id_field: 数组元素用于匹配的 ID 字段名
            float_tolerance: 浮点数比较容差
        """
        self.ignore_keys = set(ignore_keys or [])
        self.ignore_null = ignore_null
        self.array_id_field = array_id_field
        self.float_tolerance = float_tolerance
    
    def _get_type_name(self, value: Any) -> str:
        """获取值类型名称"""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return type(value).__name__
    
    def _values_equal(self, v1: Any, v2: Any) -> bool:
        """比较两个值是否相等"""
        if self.ignore_null and (v1 is None or v2 is None):
            return True
        
        if type(v1) != type(v2):
            if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                return abs(v1 - v2) < self.float_tolerance
            return False
        
        if isinstance(v1, float):
            return abs(v1 - v2) < self.float_tolerance
        
        return v1 == v2
    
    def _build_path(self, base: str, key: Union[str, int]) -> str:
        """构建 JSON 路径"""
        if isinstance(key, int):
            return f"{base}[{key}]"
        elif base == "":
            return str(key)
        else:
            return f"{base}.{key}"
    
    def _get_array_element_id(self, item: Any) -> Optional[Any]:
        """获取数组元素的 ID"""
        if self.array_id_field and isinstance(item, dict):
            return item.get(self.array_id_field)
        return None
    
    def _diff_arrays(
        self,
        old_arr: List[Any],
        new_arr: List[Any],
        path: str,
        diffs: List[JsonDiff]
    ):
        """比较数组差异"""
        if self.array_id_field:
            # 基于 ID 的数组比较
            old_map = {}
            for i, item in enumerate(old_arr):
                item_id = self._get_array_element_id(item)
                if item_id is not None:
                    old_map[item_id] = (i, item)
            
            new_map = {}
            for i, item in enumerate(new_arr):
                item_id = self._get_array_element_id(item)
                if item_id is not None:
                    new_map[item_id] = (i, item)
            
            old_ids = set(old_map.keys())
            new_ids = set(new_map.keys())
            
            # 删除的元素
            for item_id in old_ids - new_ids:
                idx, item = old_map[item_id]
                diffs.append(JsonDiff(
                    path=self._build_path(path, idx),
                    change_type=ChangeType.REMOVED,
                    old_value=item,
                    new_value=None,
                    old_type=self._get_type_name(item),
                    new_type=None
                ))
            
            # 新增的元素
            for item_id in new_ids - old_ids:
                idx, item = new_map[item_id]
                diffs.append(JsonDiff(
                    path=self._build_path(path, idx),
                    change_type=ChangeType.ADDED,
                    old_value=None,
                    new_value=item,
                    old_type=None,
                    new_type=self._get_type_name(item)
                ))
            
            # 修改的元素
            for item_id in old_ids & new_ids:
                old_idx, old_item = old_map[item_id]
                new_idx, new_item = new_map[item_id]
                self._diff_values(
                    old_item, new_item,
                    self._build_path(path, old_idx),
                    diffs
                )
        else:
            # 基于索引的数组比较（LCS 算法简化版）
            old_len = len(old_arr)
            new_len = len(new_arr)
            max_len = max(old_len, new_len)
            
            for i in range(max_len):
                item_path = self._build_path(path, i)
                if i >= old_len:
                    # 新增
                    diffs.append(JsonDiff(
                        path=item_path,
                        change_type=ChangeType.ADDED,
                        old_value=None,
                        new_value=new_arr[i],
                        old_type=None,
                        new_type=self._get_type_name(new_arr[i])
                    ))
                elif i >= new_len:
                    # 删除
                    diffs.append(JsonDiff(
                        path=item_path,
                        change_type=ChangeType.REMOVED,
                        old_value=old_arr[i],
                        new_value=None,
                        old_type=self._get_type_name(old_arr[i]),
                        new_type=None
                    ))
                else:
                    # 比较元素
                    self._diff_values(old_arr[i], new_arr[i], item_path, diffs)
    
    def _diff_objects(
        self,
        old_obj: Dict[str, Any],
        new_obj: Dict[str, Any],
        path: str,
        diffs: List[JsonDiff]
    ):
        """比较对象差异"""
        old_keys = set(old_obj.keys()) - self.ignore_keys
        new_keys = set(new_obj.keys()) - self.ignore_keys
        
        all_keys = old_keys | new_keys
        
        for key in all_keys:
            if key in self.ignore_keys:
                continue
            
            key_path = self._build_path(path, key)
            
            if key not in old_keys:
                # 新增
                diffs.append(JsonDiff(
                    path=key_path,
                    change_type=ChangeType.ADDED,
                    old_value=None,
                    new_value=new_obj[key],
                    old_type=None,
                    new_type=self._get_type_name(new_obj[key])
                ))
            elif key not in new_keys:
                # 删除
                diffs.append(JsonDiff(
                    path=key_path,
                    change_type=ChangeType.REMOVED,
                    old_value=old_obj[key],
                    new_value=None,
                    old_type=self._get_type_name(old_obj[key]),
                    new_type=None
                ))
            else:
                # 比较
                self._diff_values(old_obj[key], new_obj[key], key_path, diffs)
    
    def _diff_values(
        self,
        old_val: Any,
        new_val: Any,
        path: str,
        diffs: List[JsonDiff]
    ):
        """比较两个值的差异"""
        if self._values_equal(old_val, new_val):
            return
        
        old_type = self._get_type_name(old_val)
        new_type = self._get_type_name(new_val)
        
        # 两者都是对象
        if isinstance(old_val, dict) and isinstance(new_val, dict):
            self._diff_objects(old_val, new_val, path, diffs)
        # 两者都是数组
        elif isinstance(old_val, list) and isinstance(new_val, list):
            self._diff_arrays(old_val, new_val, path, diffs)
        # 其他情况：类型不同或基本类型值不同
        else:
            diffs.append(JsonDiff(
                path=path,
                change_type=ChangeType.MODIFIED,
                old_value=old_val,
                new_value=new_val,
                old_type=old_type,
                new_type=new_type
            ))
    
    def diff(self, old_json: Any, new_json: Any) -> DiffResult:
        """
        比较两个 JSON 对象的差异
        
        Args:
            old_json: 旧 JSON 对象
            new_json: 新 JSON 对象
        
        Returns:
            DiffResult: 差异结果
        """
        diffs: List[JsonDiff] = []
        self._diff_values(old_json, new_json, "", diffs)
        return DiffResult(diffs=diffs)
    
    def diff_json_strings(self, old_str: str, new_str: str) -> DiffResult:
        """
        比较两个 JSON 字符串的差异
        
        Args:
            old_str: 旧 JSON 字符串
            new_str: 新 JSON 字符串
        
        Returns:
            DiffResult: 差异结果
        """
        old_json = json.loads(old_str)
        new_json = json.loads(new_str)
        return self.diff(old_json, new_json)


class JsonPatcher:
    """JSON Patch 操作器 (RFC 6902)"""
    
    @staticmethod
    def _parse_pointer(pointer: str) -> List[str]:
        """解析 JSON Pointer"""
        if not pointer:
            return []
        
        if pointer.startswith("/"):
            pointer = pointer[1:]
        
        if not pointer:
            return []
        
        parts = pointer.split("/")
        # 处理转义字符
        result = []
        for part in parts:
            part = part.replace("~1", "/")
            part = part.replace("~0", "~")
            result.append(part)
        
        return result
    
    @staticmethod
    def _to_pointer(path_parts: List[Union[str, int]]) -> str:
        """将路径部分转换为 JSON Pointer"""
        if not path_parts:
            return ""
        
        result = []
        for part in path_parts:
            if isinstance(part, int):
                result.append(str(part))
            else:
                part = str(part).replace("~", "~0").replace("/", "~1")
                result.append(part)
        
        return "/" + "/".join(result)
    
    @staticmethod
    def _get_value(obj: Any, path: str) -> Any:
        """根据路径获取值"""
        parts = JsonPatcher._parse_pointer(path)
        current = obj
        
        for part in parts:
            if isinstance(current, dict):
                if part not in current:
                    raise KeyError(f"Path not found: {path}")
                current = current[part]
            elif isinstance(current, list):
                try:
                    idx = int(part)
                    current = current[idx]
                except (ValueError, IndexError):
                    raise KeyError(f"Invalid array index: {part}")
            else:
                raise KeyError(f"Cannot navigate into non-container: {type(current)}")
        
        return current
    
    @staticmethod
    def _set_value(obj: Any, path: str, value: Any, create_parents: bool = False):
        """设置指定路径的值"""
        parts = JsonPatcher._parse_pointer(path)
        
        if not parts:
            # 替换根对象
            return value
        
        current = obj
        for i, part in enumerate(parts[:-1]):
            next_part = parts[i + 1]
            
            if isinstance(current, dict):
                if part not in current:
                    if create_parents:
                        current[part] = {} if not next_part.isdigit() else []
                    else:
                        raise KeyError(f"Path not found: {'/'.join(parts[:i+1])}")
                current = current[part]
            elif isinstance(current, list):
                try:
                    idx = int(part)
                    current = current[idx]
                except (ValueError, IndexError):
                    raise KeyError(f"Invalid array index: {part}")
            else:
                raise KeyError(f"Cannot navigate into non-container")
        
        # 设置最终值
        last_part = parts[-1]
        if isinstance(current, dict):
            current[last_part] = value
        elif isinstance(current, list):
            try:
                idx = int(last_part)
                if idx == len(current):
                    current.append(value)  # 允许添加到数组末尾
                elif 0 <= idx < len(current):
                    current[idx] = value
                else:
                    raise IndexError(f"Array index out of range: {idx}")
            except ValueError:
                raise KeyError(f"Invalid array index: {last_part}")
        
        return obj
    
    @staticmethod
    def _remove_value(obj: Any, path: str) -> Any:
        """删除指定路径的值"""
        parts = JsonPatcher._parse_pointer(path)
        
        if not parts:
            raise ValueError("Cannot remove root object")
        
        current = obj
        for part in parts[:-1]:
            if isinstance(current, dict):
                current = current[part]
            elif isinstance(current, list):
                idx = int(part)
                current = current[idx]
        
        last_part = parts[-1]
        if isinstance(current, dict):
            return current.pop(last_part)
        elif isinstance(current, list):
            idx = int(last_part)
            return current.pop(idx)
        
        return None
    
    @staticmethod
    def apply_patch(obj: Any, patches: List[Union[JsonPatch, Dict[str, Any]]]) -> Any:
        """
        应用 JSON Patch
        
        Args:
            obj: 原始对象
            patches: 补丁列表
        
        Returns:
            应用补丁后的对象
        """
        result = deepcopy(obj)
        
        for patch in patches:
            if isinstance(patch, JsonPatch):
                patch_dict = patch.to_dict()
            else:
                patch_dict = patch
            
            op = DiffOperation(patch_dict["op"])
            path = patch_dict["path"]
            value = patch_dict.get("value")
            from_path = patch_dict.get("from")
            
            if op == DiffOperation.ADD:
                JsonPatcher._set_value(result, path, value, create_parents=True)
            
            elif op == DiffOperation.REMOVE:
                JsonPatcher._remove_value(result, path)
            
            elif op == DiffOperation.REPLACE:
                JsonPatcher._set_value(result, path, value)
            
            elif op == DiffOperation.MOVE:
                if from_path is None:
                    raise ValueError("Move operation requires 'from' path")
                moved_value = JsonPatcher._get_value(result, from_path)
                JsonPatcher._remove_value(result, from_path)
                JsonPatcher._set_value(result, path, moved_value, create_parents=True)
            
            elif op == DiffOperation.COPY:
                if from_path is None:
                    raise ValueError("Copy operation requires 'from' path")
                copied_value = deepcopy(JsonPatcher._get_value(result, from_path))
                JsonPatcher._set_value(result, path, copied_value, create_parents=True)
            
            elif op == DiffOperation.TEST:
                current_value = JsonPatcher._get_value(result, path)
                if current_value != value:
                    raise ValueError(f"Test failed: {path} has value {current_value}, expected {value}")
        
        return result
    
    @staticmethod
    def generate_patch(
        old_json: Any,
        new_json: Any,
        differ: Optional[JsonDiffer] = None
    ) -> List[JsonPatch]:
        """
        从差异生成 JSON Patch
        
        Args:
            old_json: 旧 JSON 对象
            new_json: 新 JSON 对象
            differ: 可选的差异比较器
        
        Returns:
            List[JsonPatch]: JSON Patch 操作列表
        """
        if differ is None:
            differ = JsonDiffer()
        
        diff_result = differ.diff(old_json, new_json)
        patches: List[JsonPatch] = []
        
        for diff in diff_result.diffs:
            # 转换路径格式（JSON Pointer 格式）
            path = "/" + diff.path.replace(".", "/").replace("[", "/").replace("]", "") if diff.path else ""
            path = path.replace("//", "/")  # 清理双斜杠
            
            if diff.change_type == ChangeType.ADDED:
                patches.append(JsonPatch(
                    op=DiffOperation.ADD,
                    path=path,
                    value=diff.new_value
                ))
            elif diff.change_type == ChangeType.REMOVED:
                patches.append(JsonPatch(
                    op=DiffOperation.REMOVE,
                    path=path
                ))
            elif diff.change_type == ChangeType.MODIFIED:
                patches.append(JsonPatch(
                    op=DiffOperation.REPLACE,
                    path=path,
                    value=diff.new_value
                ))
        
        return patches


class JsonMergePatch:
    """JSON Merge Patch (RFC 7396) 实现"""
    
    @staticmethod
    def apply_patch(target: Any, patch: Any) -> Any:
        """
        应用 JSON Merge Patch
        
        Args:
            target: 目标对象
            patch: 补丁对象
        
        Returns:
            应用补丁后的对象
        """
        if not isinstance(patch, dict):
            return deepcopy(patch)
        
        result = deepcopy(target) if isinstance(target, dict) else {}
        
        for key, value in patch.items():
            if value is None:
                # null 值表示删除
                result.pop(key, None)
            elif isinstance(value, dict):
                # 递归合并
                if key not in result or not isinstance(result.get(key), dict):
                    result[key] = {}
                result[key] = JsonMergePatch.apply_patch(result[key], value)
            else:
                result[key] = deepcopy(value)
        
        return result
    
    @staticmethod
    def generate_patch(old_json: Any, new_json: Any) -> Dict[str, Any]:
        """
        生成 JSON Merge Patch
        
        Args:
            old_json: 旧 JSON 对象
            new_json: 新 JSON 对象
        
        Returns:
            Dict: Merge Patch 对象
        """
        if new_json is None:
            return None
        
        if not isinstance(old_json, dict) or not isinstance(new_json, dict):
            return deepcopy(new_json)
        
        patch: Dict[str, Any] = {}
        
        # 检查删除的键
        for key in old_json:
            if key not in new_json:
                patch[key] = None
        
        # 检查新增或修改的键
        for key, value in new_json.items():
            if key not in old_json:
                patch[key] = deepcopy(value)
            elif isinstance(value, dict) and isinstance(old_json[key], dict):
                nested_patch = JsonMergePatch.generate_patch(old_json[key], value)
                if nested_patch:  # 只添加非空补丁
                    patch[key] = nested_patch
            elif old_json[key] != value:
                patch[key] = deepcopy(value)
        
        return patch


class JsonDiffVisualizer:
    """JSON 差异可视化工具"""
    
    @staticmethod
    def to_colored_text(diff_result: DiffResult) -> str:
        """
        生成彩色文本输出
        
        Args:
            diff_result: 差异结果
        
        Returns:
            str: 彩色文本
        """
        lines = []
        
        # ANSI 颜色代码
        GREEN = "\033[92m"    # 新增
        RED = "\033[91m"      # 删除
        YELLOW = "\033[93m"   # 修改
        RESET = "\033[0m"
        
        for diff in diff_result.diffs:
            if diff.change_type == ChangeType.ADDED:
                lines.append(f"{GREEN}+ {diff.path}: {repr(diff.new_value)}{RESET}")
            elif diff.change_type == ChangeType.REMOVED:
                lines.append(f"{RED}- {diff.path}: {repr(diff.old_value)}{RESET}")
            elif diff.change_type == ChangeType.MODIFIED:
                lines.append(f"{YELLOW}~ {diff.path}:{RESET}")
                lines.append(f"{RED}  - {repr(diff.old_value)}{RESET}")
                lines.append(f"{GREEN}  + {repr(diff.new_value)}{RESET}")
        
        # 添加统计信息
        stats = diff_result.stats
        lines.append("")
        lines.append(f"统计: +{stats['added']} -{stats['removed']} ~{stats['modified']}")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_markdown(diff_result: DiffResult) -> str:
        """
        生成 Markdown 格式输出
        
        Args:
            diff_result: 差异结果
        
        Returns:
            str: Markdown 文本
        """
        lines = ["# JSON 差异报告\n"]
        
        # 统计信息
        stats = diff_result.stats
        lines.append("## 统计信息\n")
        lines.append(f"- 新增: **{stats['added']}**")
        lines.append(f"- 删除: **{stats['removed']}**")
        lines.append(f"- 修改: **{stats['modified']}**")
        lines.append(f"- 总计: **{stats['total']}**\n")
        
        if diff_result.has_changes:
            # 新增项
            added = diff_result.filter_by_type(ChangeType.ADDED)
            if added:
                lines.append("## 新增项\n")
                for diff in added:
                    lines.append(f"- `{diff.path}`: `{repr(diff.new_value)}`")
                lines.append("")
            
            # 删除项
            removed = diff_result.filter_by_type(ChangeType.REMOVED)
            if removed:
                lines.append("## 删除项\n")
                for diff in removed:
                    lines.append(f"- `{diff.path}`: `{repr(diff.old_value)}`")
                lines.append("")
            
            # 修改项
            modified = diff_result.filter_by_type(ChangeType.MODIFIED)
            if modified:
                lines.append("## 修改项\n")
                lines.append("| 路径 | 旧值 | 新值 |")
                lines.append("|------|------|------|")
                for diff in modified:
                    lines.append(f"| `{diff.path}` | `{repr(diff.old_value)}` | `{repr(diff.new_value)}` |")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_html(diff_result: DiffResult) -> str:
        """
        生成 HTML 格式输出
        
        Args:
            diff_result: 差异结果
        
        Returns:
            str: HTML 文本
        """
        html = ['<div class="json-diff">']
        
        for diff in diff_result.diffs:
            if diff.change_type == ChangeType.ADDED:
                html.append(f'<div class="diff-added">+ {diff.path}: {repr(diff.new_value)}</div>')
            elif diff.change_type == ChangeType.REMOVED:
                html.append(f'<div class="diff-removed">- {diff.path}: {repr(diff.old_value)}</div>')
            elif diff.change_type == ChangeType.MODIFIED:
                html.append(f'<div class="diff-modified">~ {diff.path}:')
                html.append(f'  <span class="old">{repr(diff.old_value)}</span>')
                html.append(f'  <span class="new">{repr(diff.new_value)}</span>')
                html.append('</div>')
        
        stats = diff_result.stats
        html.append('<div class="stats">')
        html.append(f'统计: +{stats["added"]} -{stats["removed"]} ~{stats["modified"]}')
        html.append('</div>')
        html.append('</div>')
        
        return "\n".join(html)


# 便捷函数
def diff(
    old_json: Any,
    new_json: Any,
    ignore_keys: Optional[List[str]] = None,
    ignore_null: bool = False,
    array_id_field: Optional[str] = None
) -> DiffResult:
    """
    比较两个 JSON 对象的差异（便捷函数）
    
    Args:
        old_json: 旧 JSON 对象
        new_json: 新 JSON 对象
        ignore_keys: 忽略的键列表
        ignore_null: 是否忽略 None 值
        array_id_field: 数组元素匹配 ID 字段
    
    Returns:
        DiffResult: 差异结果
    """
    differ = JsonDiffer(
        ignore_keys=ignore_keys,
        ignore_null=ignore_null,
        array_id_field=array_id_field
    )
    return differ.diff(old_json, new_json)


def diff_strings(old_str: str, new_str: str, **kwargs) -> DiffResult:
    """
    比较两个 JSON 字符串的差异（便捷函数）
    
    Args:
        old_str: 旧 JSON 字符串
        new_str: 新 JSON 字符串
        **kwargs: 传递给 JsonDiffer 的参数
    
    Returns:
        DiffResult: 差异结果
    """
    differ = JsonDiffer(**kwargs)
    return differ.diff_json_strings(old_str, new_str)


def generate_patch(old_json: Any, new_json: Any) -> List[JsonPatch]:
    """
    生成 JSON Patch（便捷函数）
    
    Args:
        old_json: 旧 JSON 对象
        new_json: 新 JSON 对象
    
    Returns:
        List[JsonPatch]: JSON Patch 操作列表
    """
    return JsonPatcher.generate_patch(old_json, new_json)


def apply_patch(obj: Any, patches: List[Union[JsonPatch, Dict[str, Any]]]) -> Any:
    """
    应用 JSON Patch（便捷函数）
    
    Args:
        obj: 原始对象
        patches: 补丁列表
    
    Returns:
        Any: 应用补丁后的对象
    """
    return JsonPatcher.apply_patch(obj, patches)


def generate_merge_patch(old_json: Any, new_json: Any) -> Dict[str, Any]:
    """
    生成 JSON Merge Patch（便捷函数）
    
    Args:
        old_json: 旧 JSON 对象
        new_json: 新 JSON 对象
    
    Returns:
        Dict: Merge Patch 对象
    """
    return JsonMergePatch.generate_patch(old_json, new_json)


def apply_merge_patch(target: Any, patch: Dict[str, Any]) -> Any:
    """
    应用 JSON Merge Patch（便捷函数）
    
    Args:
        target: 目标对象
        patch: 补丁对象
    
    Returns:
        Any: 应用补丁后的对象
    """
    return JsonMergePatch.apply_patch(target, patch)


if __name__ == "__main__":
    # 简单示例
    old = {
        "name": "Alice",
        "age": 30,
        "hobbies": ["reading", "gaming"],
        "address": {
            "city": "Beijing",
            "zip": "100000"
        }
    }
    
    new = {
        "name": "Alice",
        "age": 31,
        "hobbies": ["reading", "traveling", "coding"],
        "address": {
            "city": "Shanghai",
            "zip": "200000"
        },
        "email": "alice@example.com"
    }
    
    result = diff(old, new)
    print("差异结果:")
    print(result)
    print()
    
    print("JSON Patch:")
    patches = generate_patch(old, new)
    for p in patches:
        print(f"  {p}")