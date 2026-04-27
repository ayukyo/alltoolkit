"""
json_diff_utils 单元测试

测试 JSON 差异比较、JSON Patch 生成与应用等功能。
"""

import sys
import os
import unittest
import json

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    JsonDiffer,
    JsonPatcher,
    JsonMergePatch,
    JsonDiffVisualizer,
    DiffResult,
    JsonDiff,
    JsonPatch,
    DiffOperation,
    ChangeType,
    diff,
    diff_strings,
    generate_patch,
    apply_patch,
    generate_merge_patch,
    apply_merge_patch
)


class TestJsonDiffer(unittest.TestCase):
    """测试 JsonDiffer 类"""
    
    def test_empty_objects(self):
        """测试空对象比较"""
        result = diff({}, {})
        self.assertEqual(len(result.diffs), 0)
        self.assertFalse(result.has_changes)
    
    def test_identical_objects(self):
        """测试相同对象比较"""
        obj = {"name": "Alice", "age": 30}
        result = diff(obj, obj)
        self.assertEqual(len(result.diffs), 0)
        self.assertFalse(result.has_changes)
    
    def test_simple_add(self):
        """测试新增字段"""
        old = {"name": "Alice"}
        new = {"name": "Alice", "email": "alice@example.com"}
        result = diff(old, new)
        
        self.assertEqual(len(result.diffs), 1)
        self.assertEqual(result.stats["added"], 1)
        self.assertEqual(result.diffs[0].path, "email")
        self.assertEqual(result.diffs[0].change_type, ChangeType.ADDED)
    
    def test_simple_remove(self):
        """测试删除字段"""
        old = {"name": "Alice", "email": "alice@example.com"}
        new = {"name": "Alice"}
        result = diff(old, new)
        
        self.assertEqual(len(result.diffs), 1)
        self.assertEqual(result.stats["removed"], 1)
        self.assertEqual(result.diffs[0].path, "email")
        self.assertEqual(result.diffs[0].change_type, ChangeType.REMOVED)
    
    def test_simple_modify(self):
        """测试修改字段"""
        old = {"name": "Alice", "age": 30}
        new = {"name": "Alice", "age": 31}
        result = diff(old, new)
        
        self.assertEqual(len(result.diffs), 1)
        self.assertEqual(result.stats["modified"], 1)
        self.assertEqual(result.diffs[0].path, "age")
        self.assertEqual(result.diffs[0].change_type, ChangeType.MODIFIED)
    
    def test_nested_changes(self):
        """测试嵌套对象差异"""
        old = {
            "user": {
                "name": "Alice",
                "address": {"city": "Beijing"}
            }
        }
        new = {
            "user": {
                "name": "Bob",
                "address": {"city": "Shanghai"}
            }
        }
        result = diff(old, new)
        
        self.assertEqual(result.stats["modified"], 2)
        paths = [d.path for d in result.diffs]
        self.assertIn("user.name", paths)
        self.assertIn("user.address.city", paths)
    
    def test_array_changes(self):
        """测试数组差异"""
        old = {"items": [1, 2, 3]}
        new = {"items": [1, 2, 4, 5]}
        result = diff(old, new)
        
        self.assertTrue(result.has_changes)
        # 应该检测到元素变化
    
    def test_ignore_keys(self):
        """测试忽略键"""
        old = {"name": "Alice", "updated_at": "2024-01-01"}
        new = {"name": "Bob", "updated_at": "2024-01-02"}
        result = diff(old, new, ignore_keys=["updated_at"])
        
        # 只检测到 name 变化
        self.assertEqual(result.stats["modified"], 1)
        self.assertEqual(result.diffs[0].path, "name")
    
    def test_float_tolerance(self):
        """测试浮点数容差"""
        old = {"value": 0.1 + 0.2}
        new = {"value": 0.3}
        result = diff(old, new)
        
        # 由于浮点精度，0.1 + 0.2 != 0.3，但默认容差应该处理
        self.assertFalse(result.has_changes)
    
    def test_diff_json_strings(self):
        """测试 JSON 字符串比较"""
        old_str = '{"name": "Alice"}'
        new_str = '{"name": "Bob"}'
        result = diff_strings(old_str, new_str)
        
        self.assertEqual(result.stats["modified"], 1)
    
    def test_type_changes(self):
        """测试类型变化"""
        old = {"value": "123"}
        new = {"value": 123}
        result = diff(old, new)
        
        self.assertEqual(result.stats["modified"], 1)
        self.assertEqual(result.diffs[0].old_type, "string")
        self.assertEqual(result.diffs[0].new_type, "integer")
    
    def test_null_handling(self):
        """测试 null 值处理"""
        old = {"a": None, "b": "value"}
        new = {"a": None, "b": "changed"}
        
        # 默认情况下，null 会被比较
        result = diff(old, new)
        self.assertEqual(result.stats["modified"], 1)
        
        # 忽略 null
        result = diff(old, new, ignore_null=True)
        self.assertEqual(result.stats["modified"], 1)


class TestDiffResult(unittest.TestCase):
    """测试 DiffResult 类"""
    
    def test_filter_by_type(self):
        """测试按类型过滤"""
        diffs = [
            JsonDiff("a", ChangeType.ADDED, None, 1, None, "integer"),
            JsonDiff("b", ChangeType.REMOVED, 2, None, "integer", None),
            JsonDiff("c", ChangeType.MODIFIED, 3, 4, "integer", "integer")
        ]
        result = DiffResult(diffs=diffs)
        
        added = result.filter_by_type(ChangeType.ADDED)
        self.assertEqual(len(added), 1)
        self.assertEqual(added[0].path, "a")
        
        removed = result.filter_by_type(ChangeType.REMOVED)
        self.assertEqual(len(removed), 1)
    
    def test_filter_by_path(self):
        """测试按路径过滤"""
        diffs = [
            JsonDiff("user.name", ChangeType.MODIFIED, "A", "B", "string", "string"),
            JsonDiff("user.age", ChangeType.MODIFIED, 1, 2, "integer", "integer"),
            JsonDiff("config.debug", ChangeType.ADDED, None, True, None, "boolean")
        ]
        result = DiffResult(diffs=diffs)
        
        user_diffs = result.filter_by_path(r"user\.")
        self.assertEqual(len(user_diffs), 2)
    
    def test_to_dict(self):
        """测试转换为字典"""
        diffs = [
            JsonDiff("a", ChangeType.ADDED, None, 1, None, "integer")
        ]
        result = DiffResult(diffs=diffs)
        
        d = result.to_dict()
        self.assertIn("diffs", d)
        self.assertIn("stats", d)
        self.assertEqual(d["stats"]["added"], 1)
    
    def test_to_json(self):
        """测试转换为 JSON"""
        diffs = [
            JsonDiff("a", ChangeType.ADDED, None, 1, None, "integer")
        ]
        result = DiffResult(diffs=diffs)
        
        json_str = result.to_json()
        parsed = json.loads(json_str)
        self.assertIn("diffs", parsed)


class TestJsonPatcher(unittest.TestCase):
    """测试 JsonPatcher 类"""
    
    def test_add_operation(self):
        """测试添加操作"""
        obj = {"name": "Alice"}
        patches = [{"op": "add", "path": "/age", "value": 30}]
        result = apply_patch(obj, patches)
        
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(result["age"], 30)
    
    def test_remove_operation(self):
        """测试删除操作"""
        obj = {"name": "Alice", "age": 30}
        patches = [{"op": "remove", "path": "/age"}]
        result = apply_patch(obj, patches)
        
        self.assertEqual(result, {"name": "Alice"})
    
    def test_replace_operation(self):
        """测试替换操作"""
        obj = {"name": "Alice", "age": 30}
        patches = [{"op": "replace", "path": "/age", "value": 31}]
        result = apply_patch(obj, patches)
        
        self.assertEqual(result["age"], 31)
    
    def test_move_operation(self):
        """测试移动操作"""
        obj = {"name": "Alice", "old_name": "Bob"}
        patches = [{"op": "move", "from": "/old_name", "path": "/alias"}]
        result = apply_patch(obj, patches)
        
        self.assertNotIn("old_name", result)
        self.assertEqual(result["alias"], "Bob")
    
    def test_copy_operation(self):
        """测试复制操作"""
        obj = {"name": "Alice"}
        patches = [{"op": "copy", "from": "/name", "path": "/alias"}]
        result = apply_patch(obj, patches)
        
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(result["alias"], "Alice")
    
    def test_test_operation(self):
        """测试测试操作"""
        obj = {"name": "Alice"}
        
        # 应该成功
        patches = [{"op": "test", "path": "/name", "value": "Alice"}]
        result = apply_patch(obj, patches)
        self.assertEqual(result, obj)
        
        # 应该失败
        patches = [{"op": "test", "path": "/name", "value": "Bob"}]
        with self.assertRaises(ValueError):
            apply_patch(obj, patches)
    
    def test_nested_path(self):
        """测试嵌套路径"""
        obj = {"user": {"name": "Alice"}}
        patches = [{"op": "add", "path": "/user/age", "value": 30}]
        result = apply_patch(obj, patches)
        
        self.assertEqual(result["user"]["name"], "Alice")
        self.assertEqual(result["user"]["age"], 30)
    
    def test_array_operations(self):
        """测试数组操作"""
        obj = {"items": [1, 2, 3]}
        
        # 添加到数组
        patches = [{"op": "add", "path": "/items/3", "value": 4}]
        result = apply_patch(obj, patches)
        self.assertEqual(result["items"], [1, 2, 3, 4])
        
        # 替换数组元素
        patches = [{"op": "replace", "path": "/items/1", "value": 10}]
        result = apply_patch(obj, patches)
        self.assertEqual(result["items"][1], 10)
        
        # 删除数组元素
        patches = [{"op": "remove", "path": "/items/1"}]
        result = apply_patch(obj, patches)
        self.assertEqual(result["items"], [1, 3])
    
    def test_generate_patch(self):
        """测试生成 JSON Patch"""
        old = {"name": "Alice", "age": 30}
        new = {"name": "Alice", "age": 31, "email": "alice@example.com"}
        
        patches = generate_patch(old, new)
        patch_dicts = [p.to_dict() for p in patches]
        
        # 应该包含 age 替换和 email 添加
        ops = [p["op"] for p in patch_dicts]
        self.assertIn("replace", ops)
        self.assertIn("add", ops)
    
    def test_apply_generated_patch(self):
        """测试应用生成的补丁"""
        old = {"name": "Alice", "age": 30}
        new = {"name": "Alice", "age": 31, "email": "alice@example.com"}
        
        patches = generate_patch(old, new)
        result = apply_patch(old, patches)
        
        self.assertEqual(result, new)


class TestJsonMergePatch(unittest.TestCase):
    """测试 JsonMergePatch 类"""
    
    def test_simple_merge(self):
        """测试简单合并"""
        target = {"a": "b"}
        patch = {"a": "c"}
        result = apply_merge_patch(target, patch)
        
        self.assertEqual(result, {"a": "c"})
    
    def test_add_field(self):
        """测试添加字段"""
        target = {"a": "b"}
        patch = {"c": "d"}
        result = apply_merge_patch(target, patch)
        
        self.assertEqual(result, {"a": "b", "c": "d"})
    
    def test_remove_field(self):
        """测试删除字段（null 值）"""
        target = {"a": "b", "c": "d"}
        patch = {"c": None}
        result = apply_merge_patch(target, patch)
        
        self.assertEqual(result, {"a": "b"})
    
    def test_nested_merge(self):
        """测试嵌套合并"""
        target = {"a": {"b": "c", "d": "e"}}
        patch = {"a": {"b": "x"}}
        result = apply_merge_patch(target, patch)
        
        self.assertEqual(result, {"a": {"b": "x", "d": "e"}})
    
    def test_generate_merge_patch(self):
        """测试生成 Merge Patch"""
        old = {"a": "b", "c": "d"}
        new = {"a": "z", "c": "d"}
        
        patch = generate_merge_patch(old, new)
        self.assertEqual(patch, {"a": "z"})
        
        # 验证可以应用
        result = apply_merge_patch(old, patch)
        self.assertEqual(result, new)
    
    def test_replace_value(self):
        """测试替换整个值"""
        target = {"a": "b"}
        patch = "c"
        result = apply_merge_patch(target, patch)
        
        self.assertEqual(result, "c")


class TestJsonDiffVisualizer(unittest.TestCase):
    """测试 JsonDiffVisualizer 类"""
    
    def test_to_colored_text(self):
        """测试彩色文本输出"""
        diffs = [
            JsonDiff("a", ChangeType.ADDED, None, 1, None, "integer"),
            JsonDiff("b", ChangeType.REMOVED, 2, None, "integer", None),
            JsonDiff("c", ChangeType.MODIFIED, 3, 4, "integer", "integer")
        ]
        result = DiffResult(diffs=diffs)
        
        text = JsonDiffVisualizer.to_colored_text(result)
        self.assertIn("a", text)
        self.assertIn("b", text)
        self.assertIn("c", text)
    
    def test_to_markdown(self):
        """测试 Markdown 输出"""
        diffs = [
            JsonDiff("name", ChangeType.MODIFIED, "Alice", "Bob", "string", "string")
        ]
        result = DiffResult(diffs=diffs)
        
        md = JsonDiffVisualizer.to_markdown(result)
        self.assertIn("# JSON 差异报告", md)
        self.assertIn("name", md)
        self.assertIn("Alice", md)
        self.assertIn("Bob", md)
    
    def test_to_html(self):
        """测试 HTML 输出"""
        diffs = [
            JsonDiff("a", ChangeType.ADDED, None, 1, None, "integer")
        ]
        result = DiffResult(diffs=diffs)
        
        html = JsonDiffVisualizer.to_html(result)
        self.assertIn("<div", html)
        self.assertIn("diff-added", html)


class TestComplexScenarios(unittest.TestCase):
    """测试复杂场景"""
    
    def test_deep_nested_structure(self):
        """测试深度嵌套结构"""
        old = {
            "company": {
                "departments": [
                    {
                        "name": "Engineering",
                        "employees": [
                            {"id": 1, "name": "Alice", "salary": 100000},
                            {"id": 2, "name": "Bob", "salary": 90000}
                        ]
                    }
                ]
            }
        }
        
        new = {
            "company": {
                "departments": [
                    {
                        "name": "Engineering",
                        "employees": [
                            {"id": 1, "name": "Alice", "salary": 110000},  # 加薪
                            {"id": 2, "name": "Bob", "salary": 95000}     # 加薪
                        ]
                    }
                ]
            }
        }
        
        result = diff(old, new)
        self.assertTrue(result.has_changes)
        self.assertEqual(result.stats["modified"], 2)
    
    def test_array_with_id_field(self):
        """测试基于 ID 字段的数组比较"""
        old = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
        
        new = {
            "users": [
                {"id": 1, "name": "Alice Updated"},  # 修改
                {"id": 3, "name": "Charlie"}          # 新增
            ]
        }
        
        differ = JsonDiffer(array_id_field="id")
        result = differ.diff(old, new)
        
        # 应该检测到 Bob 删除，Alice 修改，Charlie 新增
        self.assertTrue(result.has_changes)
    
    def test_large_structure_performance(self):
        """测试大型结构性能"""
        # 创建大型结构
        old = {"items": [{"id": i, "value": f"old_{i}"} for i in range(100)]}
        new = {"items": [{"id": i, "value": f"new_{i}"} for i in range(100)]}
        
        import time
        start = time.time()
        result = diff(old, new)
        elapsed = time.time() - start
        
        # 应该在合理时间内完成
        self.assertLess(elapsed, 1.0)  # 1秒内
        self.assertTrue(result.has_changes)
    
    def test_round_trip_patch(self):
        """测试补丁往返"""
        original = {
            "name": "Alice",
            "age": 30,
            "hobbies": ["reading", "gaming"],
            "address": {
                "city": "Beijing",
                "zip": "100000"
            }
        }
        
        modified = {
            "name": "Alice",
            "age": 31,
            "hobbies": ["reading", "traveling"],
            "address": {
                "city": "Shanghai",
                "zip": "200000"
            },
            "email": "alice@example.com"
        }
        
        # 生成补丁
        patches = generate_patch(original, modified)
        
        # 应用补丁
        result = apply_patch(original, patches)
        
        # 验证结果
        self.assertEqual(result["age"], 31)
        self.assertEqual(result["email"], "alice@example.com")
        self.assertEqual(result["address"]["city"], "Shanghai")


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_values(self):
        """测试空值"""
        old = {"a": "", "b": [], "c": {}}
        new = {"a": "x", "b": [1], "c": {"d": 1}}
        result = diff(old, new)
        
        # 空字符串变为非空: modified
        # 空数组变为非空: 由于是数组，会递归比较，新增元素是 added
        # 空对象变为非空: 由于是对象，会递归比较，新增键是 added
        self.assertTrue(result.has_changes)
        self.assertEqual(result.stats["modified"], 1)  # "a" 字符串变更
        self.assertEqual(result.stats["added"], 2)    # "b" 和 "c" 内部新增
    
    def test_special_characters_in_keys(self):
        """测试键中的特殊字符"""
        old = {"a/b": 1, "c~d": 2}
        new = {"a/b": 10, "c~d": 20}
        result = diff(old, new)
        
        self.assertEqual(result.stats["modified"], 2)
    
    def test_unicode_values(self):
        """测试 Unicode 值"""
        old = {"name": "中文", "emoji": "😀"}
        new = {"name": "日本語", "emoji": "🎉"}
        result = diff(old, new)
        
        self.assertEqual(result.stats["modified"], 2)
    
    def test_very_large_numbers(self):
        """测试大数字"""
        old = {"value": 10**100}
        new = {"value": 10**100 + 1}
        result = diff(old, new)
        
        self.assertEqual(result.stats["modified"], 1)
    
    def test_boolean_vs_integer(self):
        """测试布尔值与整数"""
        old = {"value": True}
        new = {"value": 1}
        result = diff(old, new)
        
        # Python 中 bool 是 int 子类，True == 1
        # 默认行为：值相等则无差异
        # 如果需要区分 bool 和 int，可以使用类型严格比较
        self.assertFalse(result.has_changes)
        
        # 测试实际布尔值差异
        old2 = {"value": True}
        new2 = {"value": False}
        result2 = diff(old2, new2)
        self.assertEqual(result2.stats["modified"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)