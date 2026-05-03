#!/usr/bin/env python3
"""
json_flatten_utils 测试文件
===========================

测试所有功能的正确性和边界情况。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    flatten_dict,
    unflatten_dict,
    flatten_list,
    deep_merge,
    get_nested_value,
    set_nested_value,
    delete_nested_value,
    has_nested_key,
    diff_dicts,
    dict_paths,
    dict_depth,
    dict_to_tuples,
    tuples_to_dict,
    pick_keys,
    omit_keys,
)


def test_flatten_dict():
    """测试字典扁平化"""
    print("测试 flatten_dict...")
    
    # 基本测试
    data = {"a": {"b": {"c": 1}}}
    result = flatten_dict(data)
    assert result == {"a.b.c": 1}, f"Expected {{'a.b.c': 1}}, got {result}"
    
    # 多个键
    data = {"a": {"b": 1, "c": 2}}
    result = flatten_dict(data)
    assert result == {"a.b": 1, "a.c": 2}, f"Expected {{'a.b': 1, 'a.c': 2}}, got {result}"
    
    # 不同分隔符
    data = {"a": {"b": 1}}
    result = flatten_dict(data, separator="_")
    assert result == {"a_b": 1}, f"Expected {{'a_b': 1}}, got {result}"
    
    # 深度限制
    data = {"a": {"b": {"c": {"d": 1}}}}
    result = flatten_dict(data, max_depth=2)
    assert result == {"a.b.c": {"d": 1}}, f"Expected nested dict, got {result}"
    
    # 空字典
    assert flatten_dict({}) == {}
    
    # 单层字典
    assert flatten_dict({"a": 1}) == {"a": 1}
    
    # 列表中的字典
    data = {"items": [{"name": "a"}, {"name": "b"}]}
    result = flatten_dict(data, flatten_lists=True)
    assert "items[0].name" in result
    assert result["items[0].name"] == "a"
    
    print("  ✓ flatten_dict 所有测试通过")


def test_unflatten_dict():
    """测试字典反扁平化"""
    print("测试 unflatten_dict...")
    
    # 基本测试
    data = {"a.b.c": 1}
    result = unflatten_dict(data)
    assert result == {"a": {"b": {"c": 1}}}, f"Got {result}"
    
    # 多个键
    data = {"a.b": 1, "a.c": 2}
    result = unflatten_dict(data)
    assert result == {"a": {"b": 1, "c": 2}}, f"Got {result}"
    
    # 不同分隔符
    data = {"a_b": 1}
    result = unflatten_dict(data, separator="_")
    assert result == {"a": {"b": 1}}, f"Got {result}"
    
    # 空字典
    assert unflatten_dict({}) == {}
    
    # 单层字典
    assert unflatten_dict({"a": 1}) == {"a": 1}
    
    # 列表索引
    data = {"a[0]": 1, "a[1]": 2}
    result = unflatten_dict(data)
    assert "a" in result
    assert isinstance(result["a"], list)
    
    print("  ✓ unflatten_dict 所有测试通过")


def test_flatten_list():
    """测试列表扁平化"""
    print("测试 flatten_list...")
    
    # 基本测试
    data = [1, [2, [3, [4]]]]
    result = flatten_list(data)
    assert result == [1, 2, 3, 4], f"Got {result}"
    
    # 深度限制
    data = [1, [2, [3, [4]]]]
    result = flatten_list(data, max_depth=1)
    assert result == [1, 2, [3, [4]]], f"Got {result}"
    
    # 空列表
    assert flatten_list([]) == []
    
    # 无嵌套
    assert flatten_list([1, 2, 3]) == [1, 2, 3]
    
    # 保留类型
    data = [(1, 2), [3, 4]]
    result = flatten_list(data, preserve_types=True)
    assert 1 in result and 2 in result and 3 in result and 4 in result
    
    print("  ✓ flatten_list 所有测试通过")


def test_deep_merge():
    """测试深度合并"""
    print("测试 deep_merge...")
    
    # 基本合并
    result = deep_merge({"a": 1}, {"b": 2})
    assert result == {"a": 1, "b": 2}, f"Got {result}"
    
    # 嵌套合并
    result = deep_merge({"a": {"b": 1}}, {"a": {"c": 2}})
    assert result == {"a": {"b": 1, "c": 2}}, f"Got {result}"
    
    # 覆盖
    result = deep_merge({"a": 1}, {"a": 2}, overwrite=True)
    assert result == {"a": 2}, f"Got {result}"
    
    # 不覆盖
    result = deep_merge({"a": 1}, {"a": 2}, overwrite=False)
    assert result == {"a": 1}, f"Got {result}"
    
    # 列表合并
    result = deep_merge({"a": [1, 2]}, {"a": [3, 4]}, merge_lists=True)
    assert result == {"a": [1, 2, 3, 4]}, f"Got {result}"
    
    # 空输入
    assert deep_merge() == {}
    assert deep_merge({"a": 1}) == {"a": 1}
    
    print("  ✓ deep_merge 所有测试通过")


def test_get_nested_value():
    """测试获取嵌套值"""
    print("测试 get_nested_value...")
    
    data = {"a": {"b": {"c": 1}}}
    
    # 字符串路径
    result = get_nested_value(data, "a.b.c")
    assert result == 1, f"Got {result}"
    
    # 列表路径
    result = get_nested_value(data, ["a", "b", "c"])
    assert result == 1, f"Got {result}"
    
    # 默认值
    result = get_nested_value(data, "a.x.y", default="N/A")
    assert result == "N/A", f"Got {result}"
    
    # 抛出错误
    try:
        get_nested_value(data, "a.x.y", raise_error=True)
        assert False, "Should raise KeyError"
    except KeyError:
        pass
    
    # 列表索引
    data = {"a": [{"b": 1}, {"b": 2}]}
    result = get_nested_value(data, "a.0.b")
    assert result == 1, f"Got {result}"
    
    print("  ✓ get_nested_value 所有测试通过")


def test_set_nested_value():
    """测试设置嵌套值"""
    print("测试 set_nested_value...")
    
    # 创建嵌套结构
    result = set_nested_value({}, "a.b.c", 1)
    assert result == {"a": {"b": {"c": 1}}}, f"Got {result}"
    
    # 更新现有值
    result = set_nested_value({"a": {"b": 1}}, "a.b", 2)
    assert result == {"a": {"b": 2}}, f"Got {result}"
    
    # 不创建父级
    try:
        set_nested_value({}, "a.b.c", 1, create_parents=False)
        assert False, "Should raise KeyError"
    except KeyError:
        pass
    
    # 列表路径
    result = set_nested_value({}, ["a", "b", "c"], 1)
    assert result == {"a": {"b": {"c": 1}}}, f"Got {result}"
    
    print("  ✓ set_nested_value 所有测试通过")


def test_delete_nested_value():
    """测试删除嵌套值"""
    print("测试 delete_nested_value...")
    
    # 基本删除（会清理空父级）
    result = delete_nested_value({"a": {"b": 1}}, "a.b")
    assert result == {}, f"Got {result}"  # a 变成空字典后被清理
    
    # 删除不存在的键
    result = delete_nested_value({"a": 1}, "b")
    assert result == {"a": 1}, f"Got {result}"
    
    # 清理空父级（深度删除）
    result = delete_nested_value({"a": {"b": {"c": 1}}}, "a.b.c")
    assert result == {}, f"Got {result}"  # 空父级被完全清理
    
    # 删除后保留其他键
    result = delete_nested_value({"a": {"b": 1, "c": 2}}, "a.b")
    assert result == {"a": {"c": 2}}, f"Got {result}"  # a.c 存在，a 不被清理
    
    # 抛出错误
    try:
        delete_nested_value({"a": 1}, "b", raise_error=True)
        assert False, "Should raise KeyError"
    except KeyError:
        pass
    
    print("  ✓ delete_nested_value 所有测试通过")


def test_has_nested_key():
    """测试检查嵌套键"""
    print("测试 has_nested_key...")
    
    data = {"a": {"b": {"c": 1}}}
    
    assert has_nested_key(data, "a.b.c") == True
    assert has_nested_key(data, "a.b") == True
    assert has_nested_key(data, "a.x") == False
    assert has_nested_key(data, ["a", "b", "c"]) == True
    assert has_nested_key(data, ["a", "x"]) == False
    # 空路径返回 True（指向根数据本身）
    assert has_nested_key(data, []) == True
    
    print("  ✓ has_nested_key 所有测试通过")


def test_diff_dicts():
    """测试字典比较"""
    print("测试 diff_dicts...")
    
    # 基本比较
    dict1 = {"a": 1, "b": 2}
    dict2 = {"a": 1, "c": 3}
    result = diff_dicts(dict1, dict2)
    
    assert "added" in result
    assert "removed" in result
    assert "changed" in result
    assert "unchanged" in result
    assert result["added"] == {"c": 3}
    assert result["removed"] == {"b": 2}
    assert result["unchanged"] == {"a": 1}
    
    # 值变化
    dict1 = {"a": 1}
    dict2 = {"a": 2}
    result = diff_dicts(dict1, dict2)
    assert result["changed"] == {"a": {"old": 1, "new": 2}}
    
    # 嵌套比较
    dict1 = {"a": {"b": 1}}
    dict2 = {"a": {"b": 2}}
    result = diff_dicts(dict1, dict2)
    assert "a.b" in result["changed"]
    
    # 忽略键
    dict1 = {"a": 1, "b": 2}
    dict2 = {"a": 1, "b": 3}
    result = diff_dicts(dict1, dict2, ignore_keys={"b"})
    assert result["unchanged"] == {"a": 1}
    
    print("  ✓ diff_dicts 所有测试通过")


def test_dict_paths():
    """测试获取字典路径"""
    print("测试 dict_paths...")
    
    data = {"a": {"b": 1, "c": 2}}
    
    # 只返回路径
    result = dict_paths(data)
    assert "a.b" in result
    assert "a.c" in result
    
    # 返回路径和值
    result = dict_paths(data, include_values=True)
    assert result["a.b"] == 1
    assert result["a.c"] == 2
    
    print("  ✓ dict_paths 所有测试通过")


def test_dict_depth():
    """测试字典深度"""
    print("测试 dict_depth...")
    
    assert dict_depth({}) == 0
    assert dict_depth({"a": 1}) == 1
    assert dict_depth({"a": {"b": 1}}) == 2
    assert dict_depth({"a": {"b": {"c": 1}}}) == 3
    
    # 混合深度
    data = {"a": 1, "b": {"c": {"d": 1}}}
    assert dict_depth(data) == 3
    
    print("  ✓ dict_depth 所有测试通过")


def test_dict_to_tuples():
    """测试字典转元组"""
    print("测试 dict_to_tuples...")
    
    data = {"a": {"b": 1, "c": 2}}
    result = dict_to_tuples(data)
    
    assert ("a.b", 1) in result
    assert ("a.c", 2) in result
    assert len(result) == 2
    
    print("  ✓ dict_to_tuples 所有测试通过")


def test_tuples_to_dict():
    """测试元组转字典"""
    print("测试 tuples_to_dict...")
    
    tuples = [("a.b", 1), ("a.c", 2)]
    result = tuples_to_dict(tuples)
    
    assert result == {"a": {"b": 1, "c": 2}}, f"Got {result}"
    
    print("  ✓ tuples_to_dict 所有测试通过")


def test_pick_keys():
    """测试选取键"""
    print("测试 pick_keys...")
    
    data = {"a": {"b": 1, "c": 2}, "d": 3}
    result = pick_keys(data, ["a.b", "d"])
    
    assert result == {"a": {"b": 1}, "d": 3}, f"Got {result}"
    
    # 空选择
    assert pick_keys(data, []) == {}
    
    # 不存在的键
    assert pick_keys(data, ["x.y"]) == {}
    
    print("  ✓ pick_keys 所有测试通过")


def test_omit_keys():
    """测试排除键"""
    print("测试 omit_keys...")
    
    data = {"a": {"b": 1, "c": 2}, "d": 3}
    result = omit_keys(data, ["a.c"])
    
    assert result == {"a": {"b": 1}, "d": 3}, f"Got {result}"
    
    # 排除不存在的键
    result = omit_keys(data, ["x.y"])
    assert "a" in result and "d" in result
    
    print("  ✓ omit_keys 所有测试通过")


def test_roundtrip():
    """测试扁平化和反扁平化的往返转换"""
    print("测试往返转换...")
    
    # 复杂嵌套结构
    original = {
        "user": {
            "name": "Alice",
            "age": 30,
            "address": {
                "city": "Beijing",
                "zip": "100000"
            }
        },
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"}
        ]
    }
    
    # 扁平化
    flat = flatten_dict(original, flatten_lists=True)
    
    # 反扁平化
    restored = unflatten_dict(flat)
    
    # 验证核心数据（列表结构可能有差异）
    assert restored["user"]["name"] == original["user"]["name"]
    assert restored["user"]["age"] == original["user"]["age"]
    assert restored["user"]["address"]["city"] == original["user"]["address"]["city"]
    
    print("  ✓ 往返转换测试通过")


def test_type_errors():
    """测试类型错误"""
    print("测试类型错误...")
    
    # flatten_dict 非字典
    try:
        flatten_dict([1, 2, 3])
        assert False, "Should raise TypeError"
    except TypeError:
        pass
    
    # flatten_list 非列表
    try:
        flatten_list({"a": 1})
        assert False, "Should raise TypeError"
    except TypeError:
        pass
    
    # unflatten_dict 非字典
    try:
        unflatten_dict([1, 2, 3])
        assert False, "Should raise TypeError"
    except TypeError:
        pass
    
    print("  ✓ 类型错误测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("json_flatten_utils 测试套件")
    print("="*50 + "\n")
    
    tests = [
        test_flatten_dict,
        test_unflatten_dict,
        test_flatten_list,
        test_deep_merge,
        test_get_nested_value,
        test_set_nested_value,
        test_delete_nested_value,
        test_has_nested_key,
        test_diff_dicts,
        test_dict_paths,
        test_dict_depth,
        test_dict_to_tuples,
        test_tuples_to_dict,
        test_pick_keys,
        test_omit_keys,
        test_roundtrip,
        test_type_errors,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)