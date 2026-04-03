#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - JSON Utilities Test Suite"""

import sys
import os
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    safe_loads, safe_load, dumps_compact, dumps_pretty, save,
    get_path, set_path, has_path, delete_path,
    merge, flatten, unflatten, filter_by_key, filter_by_value, pick, omit,
    is_valid, is_json_object, is_json_array, is_json_primitive,
    clone, diff, size, sort_keys, find_all, find_first, map_values, map_keys,
    equals, hash_code
)


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test(self, name, condition):
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}")
    
    def report(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.failed == 0:
            print("All tests passed!")
        else:
            print(f"{self.failed} test(s) failed.")
        print('='*50)
        return self.failed == 0


def run_tests():
    runner = TestRunner()
    
    print("\nSafe Parsing Tests")
    print("="*50)
    runner.test("safe_loads parses valid JSON", safe_loads('{"name": "John"}') == {'name': 'John'})
    runner.test("safe_loads returns default on invalid JSON", safe_loads('invalid', default={}) == {})
    runner.test("safe_loads returns default on None", safe_loads(None, default={}) == {})
    runner.test("safe_loads handles bytes", safe_loads(b'{"key": "value"}') == {'key': 'value'})
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"test": "data"}')
        temp_path = f.name
    try:
        runner.test("safe_load reads valid JSON file", safe_load(temp_path) == {'test': 'data'})
        runner.test("safe_load returns default for missing file", safe_load('/nonexistent/file.json', default={}) == {})
    finally:
        os.unlink(temp_path)
    
    print("\nSerialization Tests")
    print("="*50)
    runner.test("dumps_compact produces compact output", dumps_compact({'a': 1, 'b': 2}) == '{"a":1,"b":2}')
    runner.test("dumps_compact handles unicode", '你好' in dumps_compact({'msg': '你好'}))
    pretty = dumps_pretty({'a': 1})
    runner.test("dumps_pretty includes newlines", '\n' in pretty)
    runner.test("dumps_pretty uses specified indent", '  "a"' in pretty)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    os.unlink(temp_path)
    try:
        runner.test("save returns True on success", save({'key': 'value'}, temp_path) == True)
        runner.test("save creates file", os.path.exists(temp_path))
        runner.test("save writes valid JSON", json.load(open(temp_path)) == {'key': 'value'})
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    print("\nQuery and Navigation Tests")
    print("="*50)
    data = {'user': {'name': 'John', 'address': {'city': 'NYC'}}, 'items': ['a', 'b', 'c']}
    runner.test("get_path gets nested value", get_path(data, 'user.name') == 'John')
    runner.test("get_path gets deeply nested value", get_path(data, 'user.address.city') == 'NYC')
    runner.test("get_path returns default for missing path", get_path(data, 'user.phone', 'N/A') == 'N/A')
    runner.test("get_path handles array indices", get_path(data, 'items.0') == 'a')
    runner.test("get_path returns default for out of bounds index", get_path(data, 'items.10', 'default') == 'default')
    
    data = {'user': {'name': 'John'}}
    set_path(data, 'user.age', 30)
    runner.test("set_path sets value at existing path", data['user']['age'] == 30)
    data = {}
    set_path(data, 'a.b.c', 'value')
    runner.test("set_path creates intermediate dicts", data == {'a': {'b': {'c': 'value'}}})
    
    data = {'user': {'name': 'John'}}
    runner.test("has_path returns True for existing path", has_path(data, 'user.name') == True)
    runner.test("has_path returns False for missing path", has_path(data, 'user.age') == False)
    
    data = {'user': {'name': 'John', 'age': 30}}
    runner.test("delete_path returns True on success", delete_path(data, 'user.age') == True)
    runner.test("delete_path removes key", 'age' not in data['user'])
    runner.test("delete_path returns False for missing path", delete_path(data, 'user.phone') == False)
    
    print("\nMerge and Manipulation Tests")
    print("="*50)
    base = {'a': 1, 'b': {'c': 2}}
    update = {'b': {'d': 3}, 'e': 4}
    merged = merge(base, update)
    runner.test("merge combines dictionaries", merged['a'] == 1 and merged['e'] == 4)
    runner.test("merge does deep merge by default", merged['b'] == {'c': 2, 'd': 3})
    runner.test("merge doesn't modify original", base['b'] == {'c': 2})
    
    data = {'user': {'name': 'John', 'address': {'city': 'NYC'}}}
    flat = flatten(data)
    runner.test("flatten creates flat keys", 'user.name' in flat and 'user.address.city' in flat)
    runner.test("flatten preserves values", flat['user.name'] == 'John')
    
    flat = {'user.name': 'John', 'user.age': 30}
    nested = unflatten(flat)
    runner.test("unflatten creates nested structure", nested == {'user': {'name': 'John', 'age': 30}})
    
    data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
    filtered = filter_by_key(data, lambda k: k.startswith('a'))
    runner.test("filter_by_key filters by key predicate", filtered == {'age': 30})
    
    data = {'a': 1, 'b': 2, 'c': 3}
    filtered = filter_by_value(data, lambda v: v > 1)
    runner.test("filter_by_value filters by value predicate", filtered == {'b': 2, 'c': 3})
    
    data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
    picked = pick(data, ['name', 'email'])
    runner.test("pick selects specified keys", picked == {'name': 'John', 'email': 'john@example.com'})
    omitted = omit(data, ['age'])
    runner.test("omit excludes specified keys", 'age' not in omitted)
    runner.test("omit preserves other keys", 'name' in omitted and 'email' in omitted)
    
    print("\nValidation Tests")
    print("="*50)
    runner.test("is_valid returns True for valid JSON", is_valid('{"key": "value"}') == True)
    runner.test("is_valid returns False for invalid JSON", is_valid('invalid') == False)
    
    print("\nType Checking Tests")
    print("="*50)
    runner.test("is_json_object returns True for dict", is_json_object({'a': 1}) == True)
    runner.test("is_json_object returns False for list", is_json_object([1, 2]) == False)
    runner.test("is_json_array returns True for list", is_json_array([1, 2]) == True)
    runner.test("is_json_array returns False for dict", is_json_array({'a': 1}) == False)
    runner.test("is_json_primitive returns True for string", is_json_primitive("hello") == True)
    runner.test("is_json_primitive returns True for number", is_json_primitive(42) == True)
    runner.test("is_json_primitive returns True for bool", is_json_primitive(True) == True)
    runner.test("is_json_primitive returns True for null", is_json_primitive(None) == True)
    runner.test("is_json_primitive returns False for dict", is_json_primitive({'a': 1}) == False)
    
    print("\nUtility Tests")
    print("="*50)
    data = {'user': {'name': 'John'}}
    cloned = clone(data)
    runner.test("clone creates independent copy", cloned == data)
    cloned['user']['name'] = 'Jane'
    runner.test("clone is deep copy", data['user']['name'] == 'John