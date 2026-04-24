#!/usr/bin/env python3
"""
JSON Utilities 测试文件

Author: AllToolkit 自动化开发
Version: 1.0.0 (2026-04-25)
"""

import unittest
from mod import (
    # 类型判断
    get_json_type, is_json_serializable, JsonType,
    # 验证
    validate_json, validate_json_schema, ValidationResult,
    # 格式化
    format_json, minify_json, prettify_json,
    # 路径操作
    get_value, set_value, has_path, delete_value, parse_json_path,
    # 展平和嵌套
    flatten_json, unflatten_json,
    # 搜索
    find_all, find_first, grep_json,
    # 过滤和转换
    filter_json, map_json,
    # 差异比较
    diff_json, diff_summary,
    # 合并
    merge_json,
    # 统计
    json_stats,
    # 提取和选择
    select_keys, omit_keys, pick_path,
    # 遍历
    walk_json, get_all_paths, get_all_values,
    # 克隆和比较
    deep_clone, deep_equals,
    # 安全操作
    safe_get, safe_string,
    # 类和便捷函数
    JsonUtils, loads, dumps, load_file, save_file,
)


class TestJsonType(unittest.TestCase):
    """测试 JSON 类型判断"""
    
    def test_get_json_type(self):
        self.assertEqual(get_json_type(None), JsonType.NULL)
        self.assertEqual(get_json_type(True), JsonType.BOOLEAN)
        self.assertEqual(get_json_type(False), JsonType.BOOLEAN)
        self.assertEqual(get_json_type(42), JsonType.NUMBER)
        self.assertEqual(get_json_type(3.14), JsonType.NUMBER)
        self.assertEqual(get_json_type("hello"), JsonType.STRING)
        self.assertEqual(get_json_type([1, 2, 3]), JsonType.ARRAY)
        self.assertEqual(get_json_type({"a": 1}), JsonType.OBJECT)
    
    def test_is_json_serializable(self):
        self.assertTrue(is_json_serializable({"a": 1}))
        self.assertTrue(is_json_serializable([1, 2, 3]))
        self.assertTrue(is_json_serializable("hello"))
        self.assertFalse(is_json_serializable(set([1, 2, 3])))


class TestValidation(unittest.TestCase):
    """测试 JSON 验证"""
    
    def test_validate_json_valid(self):
        result = validate_json('{"name": "test", "value": 123}')
        self.assertTrue(result.valid)
        self.assertIsNone(result.error)
    
    def test_validate_json_invalid(self):
        result = validate_json('{"name": "test"')
        self.assertFalse(result.valid)
        self.assertIsNotNone(result.error)
        self.assertEqual(result.line, 1)
    
    def test_validate_json_schema_type(self):
        data = {"name": "test", "age": 25}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        valid, errors = validate_json_schema(data, schema)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_json_schema_required(self):
        data = {"name": "test"}
        schema = {
            "type": "object",
            "required": ["name", "age"],
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        valid, errors = validate_json_schema(data, schema)
        self.assertFalse(valid)
        self.assertIn("missing required field 'age'", errors[0])
    
    def test_validate_json_schema_enum(self):
        data = {"status": "active"}
        schema = {
            "type": "object",
            "properties": {
                "status": {"enum": ["active", "inactive", "pending"]}
            }
        }
        valid, errors = validate_json_schema(data, schema)
        self.assertTrue(valid)
    
    def test_validate_json_schema_range(self):
        data = {"age": 150}
        schema = {
            "type": "object",
            "properties": {
                "age": {"type": "integer", "minimum": 0, "maximum": 120}
            }
        }
        valid, errors = validate_json_schema(data, schema)
        self.assertFalse(valid)


class TestFormatting(unittest.TestCase):
    """测试 JSON 格式化"""
    
    def test_format_json(self):
        data = {"name": "测试", "value": 123}
        result = format_json(data)
        self.assertIn('"name"', result)
        self.assertIn('"测试"', result)
    
    def test_format_json_compact(self):
        data = {"name": "test", "value": 123}
        result = format_json(data, compact=True)
        self.assertEqual(result, '{"name":"test","value":123}')
    
    def test_format_json_sort_keys(self):
        data = {"z": 1, "a": 2}
        result = format_json(data, sort_keys=True)
        self.assertTrue(result.index('"a"') < result.index('"z"'))
    
    def test_minify_json(self):
        json_string = '''
        {
            "name": "test",
            "value": 123
        }
        '''
        result = minify_json(json_string)
        self.assertEqual(result, '{"name":"test","value":123}')
    
    def test_prettify_json(self):
        json_string = '{"name":"test","value":123}'
        result = prettify_json(json_string)
        self.assertIn('\n', result)
        self.assertIn('  "name"', result)


class TestPathOperations(unittest.TestCase):
    """测试路径操作"""
    
    def setUp(self):
        self.data = {
            "name": "test",
            "user": {
                "id": 1,
                "profile": {
                    "email": "test@example.com"
                }
            },
            "items": [
                {"id": 1, "name": "item1"},
                {"id": 2, "name": "item2"}
            ]
        }
    
    def test_get_value_simple(self):
        self.assertEqual(get_value(self.data, "name"), "test")
    
    def test_get_value_nested(self):
        self.assertEqual(get_value(self.data, "user.id"), 1)
        self.assertEqual(get_value(self.data, "user.profile.email"), "test@example.com")
    
    def test_get_value_array(self):
        self.assertEqual(get_value(self.data, "items[0].name"), "item1")
        self.assertEqual(get_value(self.data, "items[1].id"), 2)
    
    def test_get_value_default(self):
        self.assertIsNone(get_value(self.data, "notexist"))
        self.assertEqual(get_value(self.data, "notexist", "default"), "default")
    
    def test_set_value_simple(self):
        data = {"a": 1}
        set_value(data, "a", 2)
        self.assertEqual(data["a"], 2)
    
    def test_set_value_nested(self):
        data = {"a": {}}
        set_value(data, "a.b.c", "value")
        self.assertEqual(data["a"]["b"]["c"], "value")
    
    def test_set_value_create(self):
        data = {}
        set_value(data, "x.y.z", "new")
        self.assertEqual(data["x"]["y"]["z"], "new")
    
    def test_has_path(self):
        self.assertTrue(has_path(self.data, "name"))
        self.assertTrue(has_path(self.data, "user.id"))
        self.assertTrue(has_path(self.data, "items[0].name"))
        self.assertFalse(has_path(self.data, "notexist"))
    
    def test_delete_value(self):
        data = {"a": {"b": 1, "c": 2}}
        self.assertTrue(delete_value(data, "a.b"))
        self.assertNotIn("b", data["a"])
        self.assertIn("c", data["a"])
    
    def test_parse_json_path(self):
        self.assertEqual(parse_json_path("a.b.c"), ["a", "b", "c"])
        self.assertEqual(parse_json_path("items[0].name"), ["items", "0", "name"])
        self.assertEqual(parse_json_path("a.b[2].c"), ["a", "b", "2", "c"])
        self.assertEqual(parse_json_path("$.a.b"), ["a", "b"])


class TestFlattenUnflatten(unittest.TestCase):
    """测试展平和嵌套"""
    
    def test_flatten_simple(self):
        data = {"a": {"b": {"c": 1}}}
        result = flatten_json(data)
        self.assertEqual(result, {"a.b.c": 1})
    
    def test_flatten_with_arrays(self):
        data = {"items": [{"id": 1}, {"id": 2}]}
        result = flatten_json(data)
        self.assertEqual(result, {"items[0].id": 1, "items[1].id": 2})
    
    def test_flatten_preserve_arrays(self):
        data = {"items": [1, 2, 3]}
        result = flatten_json(data, preserve_arrays=True)
        self.assertEqual(result, {"items": [1, 2, 3]})
    
    def test_unflatten_simple(self):
        data = {"a.b.c": 1}
        result = unflatten_json(data)
        self.assertEqual(result, {"a": {"b": {"c": 1}}})
    
    def test_unflatten_with_arrays(self):
        data = {"items[0]": "a", "items[1]": "b"}
        result = unflatten_json(data)
        self.assertEqual(result, {"items": ["a", "b"]})
    
    def test_flatten_unflatten_roundtrip(self):
        original = {
            "name": "test",
            "user": {
                "id": 1,
                "tags": ["a", "b"]
            }
        }
        flattened = flatten_json(original)
        restored = unflatten_json(flattened)
        self.assertEqual(restored["name"], "test")
        self.assertEqual(restored["user"]["id"], 1)


class TestSearch(unittest.TestCase):
    """测试 JSON 搜索"""
    
    def setUp(self):
        self.data = {
            "name": "test",
            "user": {
                "name": "John",
                "email": "john@example.com"
            },
            "items": [
                {"name": "item1", "value": 100},
                {"name": "item2", "value": 200}
            ]
        }
    
    def test_find_all_by_key(self):
        results = find_all(self.data, key="name")
        names = [r.value for r in results]
        self.assertIn("test", names)
        self.assertIn("John", names)
        self.assertIn("item1", names)
    
    def test_find_all_by_value(self):
        results = find_all(self.data, value="item1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].value, "item1")
    
    def test_find_first(self):
        result = find_first(self.data, key="name")
        self.assertIsNotNone(result)
        self.assertEqual(result.value, "test")
    
    def test_grep_json(self):
        results = grep_json(self.data, r"example\.com")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].value, "john@example.com")
    
    def test_grep_json_keys(self):
        # grep_json 会搜索匹配键名对应的值（值也必须是字符串且匹配）
        # item1, item2 是键名匹配，但值也是字符串所以会被找到
        results = grep_json(self.data, r"item\d", search_keys=True, search_values=True)
        self.assertGreaterEqual(len(results), 2)


class TestFilterAndMap(unittest.TestCase):
    """测试过滤和映射"""
    
    def test_filter_json(self):
        data = {
            "keep": 1,
            "remove": 2,
            "nested": {
                "keep": 3,
                "remove": 4
            }
        }
        result = filter_json(data, lambda path, value: "remove" not in path)
        self.assertEqual(result["keep"], 1)
        self.assertNotIn("remove", result)
        self.assertEqual(result["nested"]["keep"], 3)
    
    def test_map_json(self):
        data = {"a": 1, "b": 2, "c": 3}
        result = map_json(data, lambda path, value: value * 2 if isinstance(value, (int, float)) else value)
        self.assertEqual(result, {"a": 2, "b": 4, "c": 6})


class TestDiff(unittest.TestCase):
    """测试差异比较"""
    
    def test_diff_added(self):
        old = {"a": 1}
        new = {"a": 1, "b": 2}
        diffs = diff_json(old, new)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].change_type, "added")
        self.assertEqual(diffs[0].new_value, 2)
    
    def test_diff_removed(self):
        old = {"a": 1, "b": 2}
        new = {"a": 1}
        diffs = diff_json(old, new)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].change_type, "removed")
    
    def test_diff_changed(self):
        old = {"a": 1}
        new = {"a": 2}
        diffs = diff_json(old, new)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].change_type, "changed")
    
    def test_diff_nested(self):
        old = {"user": {"name": "John", "age": 25}}
        new = {"user": {"name": "Jane", "age": 25}}
        diffs = diff_json(old, new)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].path, "user.name")
    
    def test_diff_arrays(self):
        old = {"items": [1, 2, 3]}
        new = {"items": [1, 4, 3]}
        diffs = diff_json(old, new)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].path, "items[1]")
    
    def test_diff_summary(self):
        old = {"a": 1, "b": 2, "c": 3}
        new = {"a": 1, "b": 20, "d": 4}
        diffs = diff_json(old, new)
        summary = diff_summary(diffs)
        self.assertEqual(summary["added"], 1)
        self.assertEqual(summary["removed"], 1)
        self.assertEqual(summary["changed"], 1)


class TestMerge(unittest.TestCase):
    """测试合并"""
    
    def test_merge_simple(self):
        base = {"a": 1}
        overlay = {"b": 2}
        result = merge_json(base, overlay)
        self.assertEqual(result, {"a": 1, "b": 2})
    
    def test_merge_override(self):
        base = {"a": 1, "b": 2}
        overlay = {"b": 3, "c": 4}
        result = merge_json(base, overlay)
        self.assertEqual(result, {"a": 1, "b": 3, "c": 4})
    
    def test_merge_deep(self):
        base = {"user": {"name": "John", "age": 25}}
        overlay = {"user": {"email": "john@example.com"}}
        result = merge_json(base, overlay, deep=True)
        self.assertEqual(result["user"]["name"], "John")
        self.assertEqual(result["user"]["email"], "john@example.com")
    
    def test_merge_arrays_replace(self):
        base = {"items": [1, 2, 3]}
        overlay = {"items": [4, 5]}
        result = merge_json(base, overlay, arrays='replace')
        self.assertEqual(result["items"], [4, 5])
    
    def test_merge_arrays_concat(self):
        base = {"items": [1, 2, 3]}
        overlay = {"items": [4, 5]}
        result = merge_json(base, overlay, arrays='concat')
        self.assertEqual(result["items"], [1, 2, 3, 4, 5])
    
    def test_merge_multiple(self):
        base = {"a": 1}
        result = merge_json(base, {"b": 2}, {"c": 3}, {"d": 4})
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3, "d": 4})


class TestStats(unittest.TestCase):
    """测试统计"""
    
    def test_json_stats(self):
        data = {
            "name": "test",
            "items": [1, 2, 3],
            "nested": {
                "a": 1,
                "b": 2
            }
        }
        stats = json_stats(data)
        # total_keys 计算所有对象的键（包括嵌套）：name, items, nested, a, b = 5
        self.assertEqual(stats["total_keys"], 5)
        self.assertGreater(stats["max_depth"], 1)
        self.assertEqual(stats["types"]["string"], 1)
        self.assertEqual(stats["types"]["array"], 1)
        self.assertEqual(stats["types"]["object"], 2)


class TestSelectOmit(unittest.TestCase):
    """测试选择和排除"""
    
    def test_select_keys(self):
        data = {"a": 1, "b": 2, "c": 3}
        result = select_keys(data, ["a", "c"])
        self.assertEqual(result, {"a": 1, "c": 3})
    
    def test_omit_keys(self):
        data = {"a": 1, "b": 2, "c": 3}
        result = omit_keys(data, ["b"])
        self.assertEqual(result, {"a": 1, "c": 3})
    
    def test_pick_path(self):
        data = {"user": {"name": "John", "age": 25}}
        result = pick_path(data, ["user.name", "user.age"])
        self.assertEqual(result, {"user.name": "John", "user.age": 25})


class TestWalk(unittest.TestCase):
    """测试遍历"""
    
    def test_walk_json(self):
        data = {"a": {"b": 1, "c": 2}}
        paths = list(walk_json(data))
        path_values = {p: v for p, v in paths}
        self.assertIn("a.b", path_values)
        self.assertIn("a.c", path_values)
    
    def test_get_all_paths(self):
        data = {"a": {"b": 1}, "c": [1, 2]}
        paths = get_all_paths(data)
        self.assertIn("a.b", paths)
        self.assertIn("c[0]", paths)
        self.assertIn("c[1]", paths)
    
    def test_get_all_values(self):
        data = {"a": 1, "b": [2, 3]}
        values = get_all_values(data)
        self.assertIn(1, values)
        self.assertIn(2, values)
        self.assertIn(3, values)


class TestCloneEquals(unittest.TestCase):
    """测试克隆和比较"""
    
    def test_deep_clone(self):
        data = {"a": {"b": [1, 2, 3]}}
        cloned = deep_clone(data)
        self.assertEqual(cloned, data)
        cloned["a"]["b"][0] = 100
        self.assertNotEqual(cloned, data)
        self.assertEqual(data["a"]["b"][0], 1)
    
    def test_deep_equals_same(self):
        a = {"x": [1, 2, {"y": 3}]}
        b = {"x": [1, 2, {"y": 3}]}
        self.assertTrue(deep_equals(a, b))
    
    def test_deep_equals_different(self):
        a = {"x": [1, 2, 3]}
        b = {"x": [1, 2, 4]}
        self.assertFalse(deep_equals(a, b))
    
    def test_deep_equals_different_types(self):
        self.assertFalse(deep_equals([1, 2], {"0": 1, "1": 2}))


class TestSafeOperations(unittest.TestCase):
    """测试安全操作"""
    
    def test_safe_get_success(self):
        data = {"a": {"b": {"c": 1}}}
        result = safe_get(data, "a", "b", "c")
        self.assertEqual(result, 1)
    
    def test_safe_get_default(self):
        data = {"a": {"b": 1}}
        result = safe_get(data, "a", "x", "y", default="default")
        self.assertEqual(result, "default")
    
    def test_safe_get_array(self):
        data = {"items": [{"id": 1}, {"id": 2}]}
        result = safe_get(data, "items", 1, "id")
        self.assertEqual(result, 2)
    
    def test_safe_string_valid(self):
        success, data = safe_string('{"name": "test"}')
        self.assertTrue(success)
        self.assertEqual(data, {"name": "test"})
    
    def test_safe_string_invalid(self):
        success, error = safe_string('{"name": invalid}')
        self.assertFalse(success)
        self.assertIn("解析错误", error)


class TestJsonUtilsClass(unittest.TestCase):
    """测试 JsonUtils 类"""
    
    def test_from_string(self):
        jutil = JsonUtils.from_string('{"a": 1, "b": 2}')
        self.assertEqual(jutil.get("a"), 1)
    
    def test_to_string(self):
        jutil = JsonUtils({"a": 1})
        result = jutil.to_string()
        self.assertIn('"a"', result)
    
    def test_get_set(self):
        jutil = JsonUtils({})
        jutil.set("a.b.c", "value")
        self.assertEqual(jutil.get("a.b.c"), "value")
    
    def test_has_delete(self):
        jutil = JsonUtils({"a": {"b": 1}})
        self.assertTrue(jutil.has("a.b"))
        jutil.delete("a.b")
        self.assertFalse(jutil.has("a.b"))
    
    def test_find(self):
        jutil = JsonUtils({"name": "test", "user": {"name": "John"}})
        results = jutil.find(key="name")
        self.assertEqual(len(results), 2)
    
    def test_flatten(self):
        jutil = JsonUtils({"a": {"b": {"c": 1}}})
        result = jutil.flatten()
        self.assertEqual(result, {"a.b.c": 1})
    
    def test_diff(self):
        jutil = JsonUtils({"a": 1, "b": 2})
        diffs = jutil.diff({"a": 1, "b": 3})
        self.assertEqual(len(diffs), 1)
    
    def test_merge(self):
        jutil = JsonUtils({"a": 1})
        jutil.merge({"b": 2})
        self.assertEqual(jutil.get("b"), 2)
    
    def test_stats(self):
        jutil = JsonUtils({"name": "test", "items": [1, 2, 3]})
        stats = jutil.stats()
        self.assertIn("total_keys", stats)
    
    def test_clone(self):
        jutil = JsonUtils({"a": {"b": 1}})
        cloned = jutil.clone()
        cloned.set("a.b", 2)
        self.assertEqual(jutil.get("a.b"), 1)
        self.assertEqual(cloned.get("a.b"),  2)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_loads(self):
        result = loads('{"a": 1}')
        self.assertEqual(result, {"a": 1})
    
    def test_loads_invalid(self):
        result = loads('invalid', default={})
        self.assertEqual(result, {})
    
    def test_dumps(self):
        result = dumps({"a": 1})
        self.assertIn('"a"', result)
    
    def test_load_file(self):
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"test": 123}')
            f.flush()
            result = load_file(f.name)
            os.unlink(f.name)
        self.assertEqual(result, {"test": 123})
    
    def test_save_file(self):
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        success = save_file({"test": 123}, filepath)
        self.assertTrue(success)
        
        with open(filepath, 'r') as f:
            content = f.read()
        os.unlink(filepath)
        
        self.assertIn('"test"', content)


if __name__ == '__main__':
    unittest.main(verbosity=2)