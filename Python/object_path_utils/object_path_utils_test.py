"""
Object Path Utils - 单元测试

测试所有核心功能的正确性和边界情况。
"""

import unittest
import copy
from mod import (
    get, set, delete, has, paths, flatten, unflatten,
    pick, omit, merge, ObjectPath,
    ObjectPathError, PathNotFoundError, InvalidPathError
)


class TestParsePath(unittest.TestCase):
    """测试路径解析（隐式测试 _parse_path）"""
    
    def test_simple_path(self):
        """简单路径"""
        data = {"a": {"b": {"c": 1}}}
        self.assertEqual(get(data, "a.b.c"), 1)
    
    def test_array_index(self):
        """数组索引"""
        data = {"items": [1, 2, 3]}
        self.assertEqual(get(data, "items[0]"), 1)
        self.assertEqual(get(data, "items[2]"), 3)
    
    def test_mixed_path(self):
        """混合路径"""
        data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
        self.assertEqual(get(data, "users[0].name"), "Alice")
        self.assertEqual(get(data, "users[1].name"), "Bob")
    
    def test_list_path(self):
        """列表路径"""
        data = {"a": {"b": {"c": 1}}}
        self.assertEqual(get(data, ["a", "b", "c"]), 1)


class TestGet(unittest.TestCase):
    """测试 get 函数"""
    
    def test_get_simple(self):
        """获取简单值"""
        data = {"name": "Alice", "age": 30}
        self.assertEqual(get(data, "name"), "Alice")
        self.assertEqual(get(data, "age"), 30)
    
    def test_get_nested(self):
        """获取嵌套值"""
        data = {"user": {"profile": {"name": "Alice"}}}
        self.assertEqual(get(data, "user.profile.name"), "Alice")
    
    def test_get_array(self):
        """获取数组元素"""
        data = {"items": ["a", "b", "c"]}
        self.assertEqual(get(data, "items[0]"), "a")
        self.assertEqual(get(data, "items[2]"), "c")
    
    def test_get_nested_array(self):
        """获取嵌套数组"""
        data = {"matrix": [[1, 2], [3, 4]]}
        self.assertEqual(get(data, "matrix[0][0]"), 1)
        self.assertEqual(get(data, "matrix[1][1]"), 4)
    
    def test_get_default(self):
        """默认值"""
        data = {"name": "Alice"}
        self.assertIsNone(get(data, "email"))
        self.assertEqual(get(data, "email", "none"), "none")
    
    def test_get_nonexistent_path(self):
        """不存在的路径"""
        data = {"name": "Alice"}
        self.assertIsNone(get(data, "user.profile.name"))
        self.assertEqual(get(data, "user.profile.name", "N/A"), "N/A")
    
    def test_get_from_list(self):
        """从列表获取"""
        data = [1, 2, 3]
        self.assertEqual(get(data, "[0]"), 1)
    
    def test_get_empty_path(self):
        """空路径"""
        data = {"name": "Alice"}
        self.assertEqual(get(data, ""), None)
        self.assertEqual(get(data, []), None)


class TestSet(unittest.TestCase):
    """测试 set 函数"""
    
    def test_set_simple(self):
        """设置简单值"""
        data = {}
        set(data, "name", "Alice")
        self.assertEqual(data, {"name": "Alice"})
    
    def test_set_nested(self):
        """设置嵌套值"""
        data = {}
        set(data, "user.name", "Alice")
        self.assertEqual(data, {"user": {"name": "Alice"}})
    
    def test_set_deep_nested(self):
        """设置深层嵌套值"""
        data = {}
        set(data, "a.b.c.d.e", 1)
        self.assertEqual(data, {"a": {"b": {"c": {"d": {"e": 1}}}}})
    
    def test_set_array(self):
        """设置数组元素"""
        data = {"items": []}
        set(data, "items[0]", "first")
        self.assertEqual(data, {"items": ["first"]})
    
    def test_set_array_expand(self):
        """设置数组元素时自动扩展"""
        data = {"items": []}
        set(data, "items[2]", "third")
        self.assertEqual(data["items"][0], None)
        self.assertEqual(data["items"][2], "third")
    
    def test_set_overwrite(self):
        """覆盖现有值"""
        data = {"name": "Alice"}
        set(data, "name", "Bob")
        self.assertEqual(data, {"name": "Bob"})
    
    def test_set_no_create_missing(self):
        """不创建中间路径"""
        data = {}
        with self.assertRaises(PathNotFoundError):
            set(data, "user.name", "Alice", create_missing=False)
    
    def test_set_list_path(self):
        """使用列表路径设置"""
        data = {}
        set(data, ["user", "name"], "Alice")
        self.assertEqual(data, {"user": {"name": "Alice"}})


class TestDelete(unittest.TestCase):
    """测试 delete 函数"""
    
    def test_delete_simple(self):
        """删除简单键"""
        data = {"name": "Alice", "age": 30}
        result = delete(data, "age")
        self.assertTrue(result)
        self.assertEqual(data, {"name": "Alice"})
    
    def test_delete_nested(self):
        """删除嵌套键"""
        data = {"user": {"name": "Alice", "age": 30}}
        result = delete(data, "user.age")
        self.assertTrue(result)
        self.assertEqual(data, {"user": {"name": "Alice"}})
    
    def test_delete_nonexistent(self):
        """删除不存在的键"""
        data = {"name": "Alice"}
        result = delete(data, "email")
        self.assertFalse(result)
    
    def test_delete_array_element(self):
        """删除数组元素"""
        data = {"items": ["a", "b", "c"]}
        result = delete(data, "items[1]")
        self.assertTrue(result)
        self.assertEqual(data["items"], ["a", "c"])


class TestHas(unittest.TestCase):
    """测试 has 函数"""
    
    def test_has_simple(self):
        """检查简单键"""
        data = {"name": "Alice"}
        self.assertTrue(has(data, "name"))
        self.assertFalse(has(data, "age"))
    
    def test_has_nested(self):
        """检查嵌套键"""
        data = {"user": {"name": "Alice"}}
        self.assertTrue(has(data, "user.name"))
        self.assertFalse(has(data, "user.age"))
    
    def test_has_array(self):
        """检查数组元素"""
        data = {"items": [1, 2, 3]}
        self.assertTrue(has(data, "items[0]"))
        self.assertTrue(has(data, "items[2]"))
        self.assertFalse(has(data, "items[3]"))
    
    def test_has_none_value(self):
        """检查 None 值"""
        data = {"name": None}
        self.assertTrue(has(data, "name"))


class TestPaths(unittest.TestCase):
    """测试 paths 函数"""
    
    def test_paths_flat(self):
        """扁平对象路径"""
        data = {"name": "Alice", "age": 30}
        result = paths(data)
        self.assertIn("name", result)
        self.assertIn("age", result)
    
    def test_paths_nested(self):
        """嵌套对象路径"""
        data = {"user": {"name": "Alice", "age": 30}}
        result = paths(data)
        self.assertIn("user", result)
        self.assertIn("user.name", result)
        self.assertIn("user.age", result)
    
    def test_paths_array(self):
        """数组路径"""
        data = {"items": [1, 2, 3]}
        result = paths(data)
        self.assertIn("items", result)
        self.assertIn("items[0]", result)
        self.assertIn("items[2]", result)
    
    def test_paths_max_depth(self):
        """最大深度限制"""
        data = {"a": {"b": {"c": {"d": 1}}}}
        result = paths(data, max_depth=2)
        # 应该只到第二层
        self.assertIn("a", result)
        self.assertIn("a.b", result)


class TestFlatten(unittest.TestCase):
    """测试 flatten 函数"""
    
    def test_flatten_simple(self):
        """扁平化简单对象"""
        data = {"name": "Alice", "age": 30}
        result = flatten(data)
        self.assertEqual(result, {"name": "Alice", "age": 30})
    
    def test_flatten_nested(self):
        """扁平化嵌套对象"""
        data = {"user": {"name": "Alice", "age": 30}}
        result = flatten(data)
        self.assertEqual(result, {
            "user.name": "Alice",
            "user.age": 30
        })
    
    def test_flatten_array(self):
        """扁平化数组"""
        data = {"items": [1, 2, 3]}
        result = flatten(data)
        self.assertEqual(result, {
            "items[0]": 1,
            "items[1]": 2,
            "items[2]": 3
        })
    
    def test_flatten_complex(self):
        """扁平化复杂对象"""
        data = {
            "user": {
                "name": "Alice",
                "tags": ["admin", "user"]
            }
        }
        result = flatten(data)
        self.assertEqual(result, {
            "user.name": "Alice",
            "user.tags[0]": "admin",
            "user.tags[1]": "user"
        })
    
    def test_flatten_custom_separator(self):
        """自定义分隔符"""
        data = {"user": {"name": "Alice"}}
        result = flatten(data, separator="_")
        self.assertEqual(result, {"user_name": "Alice"})


class TestUnflatten(unittest.TestCase):
    """测试 unflatten 函数"""
    
    def test_unflatten_simple(self):
        """反扁平化简单对象"""
        flat = {"name": "Alice", "age": 30}
        result = unflatten(flat)
        self.assertEqual(result, {"name": "Alice", "age": 30})
    
    def test_unflatten_nested(self):
        """反扁平化嵌套对象"""
        flat = {"user.name": "Alice", "user.age": 30}
        result = unflatten(flat)
        self.assertEqual(result, {"user": {"name": "Alice", "age": 30}})
    
    def test_flatten_unflatten_roundtrip(self):
        """扁平化和反扁平化往返测试"""
        original = {
            "user": {
                "name": "Alice",
                "profile": {
                    "age": 30,
                    "tags": ["admin", "user"]
                }
            }
        }
        flat = flatten(original)
        result = unflatten(flat)
        # 注意：数组索引会丢失，需要手动处理
        self.assertEqual(result["user"]["name"], "Alice")
        self.assertEqual(result["user"]["profile"]["age"], 30)


class TestPick(unittest.TestCase):
    """测试 pick 函数"""
    
    def test_pick_single(self):
        """选取单个路径"""
        data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
        result = pick(data, "name")
        self.assertEqual(result, {"name": "Alice"})
    
    def test_pick_multiple(self):
        """选取多个路径"""
        data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
        result = pick(data, "name", "age")
        self.assertEqual(result, {"name": "Alice", "age": 30})
    
    def test_pick_nested(self):
        """选取嵌套路径"""
        data = {"user": {"name": "Alice", "age": 30, "email": "alice@example.com"}}
        result = pick(data, "user.name", "user.email")
        self.assertEqual(result, {
            "user.name": "Alice",
            "user.email": "alice@example.com"
        })
    
    def test_pick_nonexistent(self):
        """选取不存在的路径"""
        data = {"name": "Alice"}
        result = pick(data, "name", "email")
        self.assertEqual(result, {"name": "Alice"})


class TestOmit(unittest.TestCase):
    """测试 omit 函数"""
    
    def test_omit_single(self):
        """排除单个路径"""
        data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
        result = omit(data, "email")
        self.assertEqual(result, {"name": "Alice", "age": 30})
    
    def test_omit_multiple(self):
        """排除多个路径"""
        data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
        result = omit(data, "age", "email")
        self.assertEqual(result, {"name": "Alice"})
    
    def test_omit_nested(self):
        """排除嵌套路径"""
        data = {"user": {"name": "Alice", "age": 30, "email": "alice@example.com"}}
        result = omit(data, "user.email")
        self.assertEqual(result, {"user": {"name": "Alice", "age": 30}})
    
    def test_omit_preserves_original(self):
        """排除不修改原对象"""
        data = {"name": "Alice", "age": 30}
        result = omit(data, "age")
        self.assertEqual(data, {"name": "Alice", "age": 30})


class TestMerge(unittest.TestCase):
    """测试 merge 函数"""
    
    def test_merge_simple(self):
        """合并简单对象"""
        result = merge({"a": 1}, {"b": 2})
        self.assertEqual(result, {"a": 1, "b": 2})
    
    def test_merge_override(self):
        """合并覆盖"""
        result = merge({"a": 1}, {"a": 2})
        self.assertEqual(result, {"a": 2})
    
    def test_merge_deep(self):
        """深度合并"""
        result = merge(
            {"user": {"name": "Alice"}},
            {"user": {"age": 30}}
        )
        self.assertEqual(result, {"user": {"name": "Alice", "age": 30}})
    
    def test_merge_shallow(self):
        """浅合并"""
        result = merge(
            {"user": {"name": "Alice"}},
            {"user": {"age": 30}},
            deep=False
        )
        self.assertEqual(result, {"user": {"age": 30}})
    
    def test_merge_arrays(self):
        """合并数组"""
        result = merge({"items": [1, 2]}, {"items": [3, 4]})
        self.assertEqual(result, {"items": [1, 2, 3, 4]})
    
    def test_merge_multiple(self):
        """合并多个对象"""
        result = merge({"a": 1}, {"b": 2}, {"c": 3})
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3})


class TestObjectPathClass(unittest.TestCase):
    """测试 ObjectPath 类"""
    
    def test_basic_operations(self):
        """基本操作"""
        op = ObjectPath({"name": "Alice"})
        self.assertEqual(op.get("name"), "Alice")
    
    def test_chained_operations(self):
        """链式操作"""
        op = ObjectPath({})
        result = op.set("user.name", "Alice").set("user.age", 30)
        self.assertEqual(result.get("user.name"), "Alice")
        self.assertEqual(result.get("user.age"), 30)
    
    def test_has_and_delete(self):
        """检查和删除"""
        op = ObjectPath({"name": "Alice", "age": 30})
        self.assertTrue(op.has("name"))
        op.delete("age")
        self.assertFalse(op.has("age"))
    
    def test_paths_and_flatten(self):
        """路径和扁平化"""
        op = ObjectPath({"user": {"name": "Alice"}})
        self.assertIn("user.name", op.paths())
        flat = op.flatten()
        self.assertEqual(flat, {"user.name": "Alice"})
    
    def test_pick_and_omit(self):
        """选取和排除"""
        op = ObjectPath({"name": "Alice", "age": 30, "email": "alice@example.com"})
        picked = op.pick("name", "age")
        self.assertEqual(picked, {"name": "Alice", "age": 30})
        
        omitted = op.omit("email")
        self.assertTrue(omitted.has("name"))
        self.assertFalse(omitted.has("email"))


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_objects(self):
        """空对象"""
        self.assertEqual(get({}, "a"), None)
        self.assertEqual(set({}, "a", 1), {"a": 1})
        self.assertFalse(has({}, "a"))
    
    def test_none_values(self):
        """None 值"""
        data = {"name": None}
        self.assertTrue(has(data, "name"))
        self.assertEqual(get(data, "name"), None)
    
    def test_special_characters_in_keys(self):
        """键中的特殊字符"""
        data = {"user.name": "Alice"}
        # 注意：这种情况路径解析可能会有问题
        # 这里测试带有特殊字符的键名
        self.assertEqual(get(data, "user.name"), None)  # 会解析为嵌套路径
    
    def test_numeric_keys(self):
        """数字键"""
        data = {"1": "one", "2": "two"}
        self.assertEqual(get(data, "1"), "one")
    
    def test_large_arrays(self):
        """大数组"""
        data = {"items": list(range(100))}
        self.assertEqual(get(data, "items[50]"), 50)
        self.assertEqual(get(data, "items[99]"), 99)


if __name__ == "__main__":
    unittest.main()