#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lazy Utils 测试模块
===================

测试所有惰性求值工具的功能。
"""

import sys
import os
import time
import threading
from typing import List

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Lazy, lazy_property, lazy_class_property, LazySequence,
    Thunk, LazyDict, LazyList, Deferred, lazy, thunk,
    lazy_sequence, lazy_list
)


class TestLazy:
    """Lazy 类测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_basic_lazy_evaluation(self):
        """测试基本惰性求值"""
        call_count = [0]
        
        def factory():
            call_count[0] += 1
            return 42
        
        lazy_val = Lazy(factory)
        
        # 未访问前不应计算
        assert call_count[0] == 0, "Should not compute before access"
        assert not lazy_val.is_computed, "is_computed should be False"
        
        # 首次访问计算
        result = lazy_val.value
        assert result == 42, f"Expected 42, got {result}"
        assert call_count[0] == 1, "Should compute once"
        assert lazy_val.is_computed, "is_computed should be True"
        
        # 再次访问不重复计算
        result2 = lazy_val.value
        assert result2 == 42, f"Expected 42, got {result2}"
        assert call_count[0] == 1, "Should not compute again"
        
        print("  ✓ test_basic_lazy_evaluation")
        self.passed += 1
    
    def test_reset(self):
        """测试重置功能"""
        call_count = [0]
        
        lazy_val = Lazy(lambda: (call_count.__setitem__(0, call_count[0] + 1), call_count[0])[1])
        
        _ = lazy_val.value
        assert call_count[0] == 1
        
        lazy_val.reset()
        assert not lazy_val.is_computed, "Should not be computed after reset"
        
        _ = lazy_val.value
        assert call_count[0] == 2, "Should recompute after reset"
        
        print("  ✓ test_reset")
        self.passed += 1
    
    def test_get_or_else(self):
        """测试 get_or_else"""
        lazy_val = Lazy(lambda: 100)
        
        # 未计算时返回默认值
        default = lazy_val.get_or_else(0)
        assert default == 0, f"Expected 0, got {default}"
        
        # 计算后返回实际值
        _ = lazy_val.value
        actual = lazy_val.get_or_else(0)
        assert actual == 100, f"Expected 100, got {actual}"
        
        print("  ✓ test_get_or_else")
        self.passed += 1
    
    def test_map(self):
        """测试 map 转换"""
        lazy_val = Lazy(lambda: 10)
        mapped = lazy_val.map(lambda x: x * 2)
        
        result = mapped.value
        assert result == 20, f"Expected 20, got {result}"
        
        print("  ✓ test_map")
        self.passed += 1
    
    def test_thread_safety(self):
        """测试线程安全"""
        call_count = [0]
        lazy_val = Lazy(lambda: (call_count.__setitem__(0, call_count[0] + 1), "result")[1])
        
        threads = []
        for _ in range(100):
            t = threading.Thread(target=lambda: lazy_val.value)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        assert call_count[0] == 1, f"Should only compute once, but computed {call_count[0]} times"
        
        print("  ✓ test_thread_safety")
        self.passed += 1
    
    def test_repr(self):
        """测试字符串表示"""
        lazy_val = Lazy(lambda: 42)
        
        repr_before = repr(lazy_val)
        assert "not computed" in repr_before, f"Expected 'not computed' in repr, got {repr_before}"
        
        _ = lazy_val.value
        repr_after = repr(lazy_val)
        assert "42" in repr_after, f"Expected '42' in repr, got {repr_after}"
        
        print("  ✓ test_repr")
        self.passed += 1
    
    def run(self):
        print("\nTesting Lazy:")
        self.test_basic_lazy_evaluation()
        self.test_reset()
        self.test_get_or_else()
        self.test_map()
        self.test_thread_safety()
        self.test_repr()
        return self.passed, self.failed


class TestLazyProperty:
    """lazy_property 装饰器测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_lazy_property(self):
        """测试惰性属性"""
        call_count = [0]
        
        class MyClass:
            @lazy_property
            def expensive(self):
                call_count[0] += 1
                return "computed"
        
        obj = MyClass()
        
        # 首次访问
        result1 = obj.expensive
        assert result1 == "computed"
        assert call_count[0] == 1
        
        # 后续访问
        result2 = obj.expensive
        assert result2 == "computed"
        assert call_count[0] == 1, "Should not recompute"
        
        print("  ✓ test_lazy_property")
        self.passed += 1
    
    def test_lazy_property_reset(self):
        """测试惰性属性重置"""
        call_count = [0]
        
        class MyClass:
            @lazy_property
            def value(self):
                call_count[0] += 1
                return call_count[0]
        
        obj = MyClass()
        assert obj.value == 1
        
        # 删除属性后重置
        del obj.value
        assert obj.value == 2, "Should recompute after delete"
        
        print("  ✓ test_lazy_property_reset")
        self.passed += 1
    
    def run(self):
        print("\nTesting lazy_property:")
        self.test_lazy_property()
        self.test_lazy_property_reset()
        return self.passed, self.failed


class TestLazyClassProperty:
    """lazy_class_property 装饰器测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_lazy_class_property(self):
        """测试类级别惰性属性"""
        call_count = [0]
        
        class MyClass:
            @lazy_class_property
            def class_value(cls):
                call_count[0] += 1
                return "class_computed"
        
        # 首次访问
        result1 = MyClass.class_value
        assert result1 == "class_computed"
        assert call_count[0] == 1
        
        # 后续访问
        result2 = MyClass.class_value
        assert result2 == "class_computed"
        assert call_count[0] == 1, "Should not recompute"
        
        print("  ✓ test_lazy_class_property")
        self.passed += 1
    
    def run(self):
        print("\nTesting lazy_class_property:")
        self.test_lazy_class_property()
        return self.passed, self.failed


class TestLazySequence:
    """LazySequence 类测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_basic_iteration(self):
        """测试基本迭代"""
        def counter():
            for i in range(5):
                yield i
        
        seq = LazySequence(counter)
        result = list(seq)
        assert result == [0, 1, 2, 3, 4], f"Expected [0,1,2,3,4], got {result}"
        
        print("  ✓ test_basic_iteration")
        self.passed += 1
    
    def test_indexing(self):
        """测试索引访问"""
        def fib():
            a, b = 0, 1
            while True:
                yield a
                a, b = b, a + b
        
        seq = LazySequence(fib)
        
        assert seq[0] == 0
        assert seq[1] == 1
        assert seq[2] == 1
        assert seq[10] == 55
        
        print("  ✓ test_indexing")
        self.passed += 1
    
    def test_slicing(self):
        """测试切片"""
        def counter():
            for i in range(100):
                yield i
        
        seq = LazySequence(counter)
        
        result = seq[:5]
        assert result == [0, 1, 2, 3, 4], f"Expected [0,1,2,3,4], got {result}"
        
        result2 = seq[10:15]
        assert result2 == [10, 11, 12, 13, 14], f"Expected [10,11,12,13,14], got {result2}"
        
        print("  ✓ test_slicing")
        self.passed += 1
    
    def test_take(self):
        """测试 take 方法"""
        def counter():
            for i in range(100):
                yield i
        
        seq = LazySequence(counter)
        result = seq.take(5)
        assert result == [0, 1, 2, 3, 4], f"Expected [0,1,2,3,4], got {result}"
        
        print("  ✓ test_take")
        self.passed += 1
    
    def test_take_while(self):
        """测试 take_while 方法"""
        def counter():
            for i in range(100):
                yield i
        
        seq = LazySequence(counter)
        result = seq.take_while(lambda x: x < 5)
        assert result == [0, 1, 2, 3, 4], f"Expected [0,1,2,3,4], got {result}"
        
        print("  ✓ test_take_while")
        self.passed += 1
    
    def test_no_cache(self):
        """测试无缓存模式"""
        call_count = [0]
        
        def counter():
            for i in range(5):
                call_count[0] += 1
                yield i
        
        seq = LazySequence(counter, cache=False)
        
        # 无缓存模式下，迭代不会缓存元素
        _ = list(seq)
        assert call_count[0] == 5, "Should generate each element once"
        
        print("  ✓ test_no_cache")
        self.passed += 1
    
    def run(self):
        print("\nTesting LazySequence:")
        self.test_basic_iteration()
        self.test_indexing()
        self.test_slicing()
        self.test_take()
        self.test_take_while()
        self.test_no_cache()
        return self.passed, self.failed


class TestThunk:
    """Thunk 类测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_basic_thunk(self):
        """测试基本 Thunk"""
        call_count = [0]
        
        t = Thunk(lambda: (call_count.__setitem__(0, call_count[0] + 1), 42)[1])
        
        assert not t.is_forced, "Should not be forced initially"
        
        result = t.force()
        assert result == 42
        assert call_count[0] == 1
        assert t.is_forced
        
        # 再次强制不重复计算
        result2 = t.value
        assert result2 == 42
        assert call_count[0] == 1
        
        print("  ✓ test_basic_thunk")
        self.passed += 1
    
    def test_thunk_composition(self):
        """测试 Thunk 组合"""
        x = Thunk(lambda: 10)
        y = Thunk(lambda: 20)
        z = Thunk(lambda: x.value + y.value)
        
        assert z.force() == 30
        
        print("  ✓ test_thunk_composition")
        self.passed += 1
    
    def run(self):
        print("\nTesting Thunk:")
        self.test_basic_thunk()
        self.test_thunk_composition()
        return self.passed, self.failed


class TestLazyDict:
    """LazyDict 类测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_lazy_dict(self):
        """测试延迟字典"""
        call_count = {}
        
        def factory(key):
            call_count[key] = call_count.get(key, 0) + 1
            return f"value-{key}"
        
        d = LazyDict(factory)
        
        # 首次访问计算
        result1 = d['a']
        assert result1 == "value-a"
        assert call_count['a'] == 1
        
        # 再次访问缓存
        result2 = d['a']
        assert result2 == "value-a"
        assert call_count['a'] == 1, "Should not recompute"
        
        print("  ✓ test_lazy_dict")
        self.passed += 1
    
    def test_prefetch(self):
        """测试预取"""
        call_count = [0]
        
        def factory(key):
            call_count[0] += 1
            return key * 2
        
        d = LazyDict(factory)
        d.prefetch('a', 'b', 'c')
        
        assert call_count[0] == 3, "Should prefetch 3 keys"
        
        # 后续访问不重复计算
        _ = d['a']
        assert call_count[0] == 3, "Should not recompute"
        
        print("  ✓ test_prefetch")
        self.passed += 1
    
    def test_get_or_compute(self):
        """测试 get_or_compute"""
        d = LazyDict()
        
        result = d.get_or_compute('x', lambda k: k.upper())
        assert result == 'X'
        assert d['x'] == 'X'
        
        print("  ✓ test_get_or_compute")
        self.passed += 1
    
    def run(self):
        print("\nTesting LazyDict:")
        self.test_lazy_dict()
        self.test_prefetch()
        self.test_get_or_compute()
        return self.passed, self.failed


class TestLazyList:
    """LazyList 类测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_basic_lazy_list(self):
        """测试基本惰性列表"""
        call_count = [0]
        
        def factory(i):
            call_count[0] += 1
            return i * 2
        
        lst = LazyList(factory)
        
        # 首次访问
        assert lst[5] == 10
        assert call_count[0] == 6, "Should generate elements 0-5"
        
        # 再次访问已计算的
        assert lst[3] == 6
        assert call_count[0] == 6, "Should not regenerate"
        
        print("  ✓ test_basic_lazy_list")
        self.passed += 1
    
    def test_slice(self):
        """测试切片"""
        lst = LazyList(lambda i: i * 2)
        
        result = lst[:5]
        assert result == [0, 2, 4, 6, 8], f"Expected [0,2,4,6,8], got {result}"
        
        print("  ✓ test_slice")
        self.passed += 1
    
    def test_append_extend(self):
        """测试追加和扩展"""
        lst = LazyList(lambda i: 0)
        
        lst.append(100)
        assert lst[0] == 100
        
        lst.extend([200, 300])
        assert lst[1] == 200
        assert lst[2] == 300
        
        print("  ✓ test_append_extend")
        self.passed += 1
    
    def test_iteration(self):
        """测试迭代"""
        lst = LazyList(lambda i: i + 1)
        lst._ensure_size(5)
        
        result = list(lst.to_list())[:5]
        assert result == [1, 2, 3, 4, 5], f"Expected [1,2,3,4,5], got {result}"
        
        print("  ✓ test_iteration")
        self.passed += 1
    
    def run(self):
        print("\nTesting LazyList:")
        self.test_basic_lazy_list()
        self.test_slice()
        self.test_append_extend()
        self.test_iteration()
        return self.passed, self.failed


class TestDeferred:
    """Deferred 类测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_basic_deferred(self):
        """测试基本延迟值"""
        d = Deferred(lambda: 42)
        
        assert d.is_pending
        assert not d.is_computing
        assert not d.is_completed
        
        result = d.get()
        assert result == 42
        assert d.is_completed
        assert not d.is_pending
        
        print("  ✓ test_basic_deferred")
        self.passed += 1
    
    def test_callbacks(self):
        """测试回调"""
        results = []
        errors = []
        
        d = Deferred(lambda: 100)
        d.on_complete(lambda v: results.append(v))
        d.on_error(lambda e: errors.append(e))
        
        d.get()
        
        assert results == [100], f"Expected [100], got {results}"
        assert errors == [], "Should not have errors"
        
        print("  ✓ test_callbacks")
        self.passed += 1
    
    def test_error_handling(self):
        """测试错误处理"""
        d = Deferred(lambda: 1/0)
        
        try:
            d.get()
            assert False, "Should raise exception"
        except ZeroDivisionError:
            pass
        
        assert d.is_failed
        
        print("  ✓ test_error_handling")
        self.passed += 1
    
    def test_cancel(self):
        """测试取消"""
        d = Deferred(lambda: 42)
        
        cancelled = d.cancel()
        assert cancelled, "Should cancel successfully"
        assert d.is_cancelled
        
        print("  ✓ test_cancel")
        self.passed += 1
    
    def run(self):
        print("\nTesting Deferred:")
        self.test_basic_deferred()
        self.test_callbacks()
        self.test_error_handling()
        self.test_cancel()
        return self.passed, self.failed


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_lazy_function(self):
        """测试 lazy 便捷函数"""
        lazy_val = lazy(lambda: 42)
        assert isinstance(lazy_val, Lazy)
        assert lazy_val.value == 42
        
        print("  ✓ test_lazy_function")
        self.passed += 1
    
    def test_thunk_function(self):
        """测试 thunk 便捷函数"""
        t = thunk(lambda: 100)
        assert isinstance(t, Thunk)
        assert t.force() == 100
        
        print("  ✓ test_thunk_function")
        self.passed += 1
    
    def test_lazy_sequence_function(self):
        """测试 lazy_sequence 便捷函数"""
        seq = lazy_sequence(lambda: (x for x in range(5)))
        result = seq.take(3)
        assert result == [0, 1, 2]
        
        print("  ✓ test_lazy_sequence_function")
        self.passed += 1
    
    def test_lazy_list_function(self):
        """测试 lazy_list 便捷函数"""
        lst = lazy_list(lambda i: i + 1)
        assert lst[0] == 1
        assert lst[4] == 5
        
        print("  ✓ test_lazy_list_function")
        self.passed += 1
    
    def run(self):
        print("\nTesting Convenience Functions:")
        self.test_lazy_function()
        self.test_thunk_function()
        self.test_lazy_sequence_function()
        self.test_lazy_list_function()
        return self.passed, self.failed


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Lazy Utils - 测试套件")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    test_classes = [
        TestLazy(),
        TestLazyProperty(),
        TestLazyClassProperty(),
        TestLazySequence(),
        TestThunk(),
        TestLazyDict(),
        TestLazyList(),
        TestDeferred(),
        TestConvenienceFunctions(),
    ]
    
    for test_class in test_classes:
        passed, failed = test_class.run()
        total_passed += passed
        total_failed += failed
    
    print("\n" + "=" * 60)
    print(f"测试结果: {total_passed} 通过, {total_failed} 失败")
    print("=" * 60)
    
    if total_failed == 0:
        print("✅ 所有测试通过!")
    else:
        print("❌ 存在失败的测试")
        sys.exit(1)
    
    return total_passed, total_failed


if __name__ == "__main__":
    run_all_tests()