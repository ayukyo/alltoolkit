"""
红黑树工具模块测试

测试覆盖：
- 基本操作（插入、删除、查找）
- 红黑树性质验证
- 范围查询
- 前驱后继
- Set 和 Map 实现
"""

import sys
import os
import random
import time

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from red_black_tree_utils.mod import (
    RedBlackTree, RedBlackTreeSet, RedBlackTreeMap,
    Color, create_tree, create_set, create_map
)


class TestRedBlackTree:
    """红黑树测试"""
    
    def test_empty_tree(self):
        """测试空树"""
        tree = RedBlackTree[int]()
        assert tree.size == 0
        assert tree.is_empty
        assert tree.minimum() is None
        assert tree.maximum() is None
        assert tree.height() == 0
        assert tree.is_valid()
        print("✓ 空树测试通过")
    
    def test_single_insert(self):
        """测试单节点插入"""
        tree = RedBlackTree[int]()
        assert tree.insert(10, "ten")
        assert tree.size == 1
        assert not tree.is_empty
        assert tree.search(10) == "ten"
        assert tree.minimum() == 10
        assert tree.maximum() == 10
        assert tree.is_valid()
        print("✓ 单节点插入测试通过")
    
    def test_insert_duplicate(self):
        """测试重复插入"""
        tree = RedBlackTree[int]()
        assert tree.insert(10, "first")
        assert not tree.insert(10, "second")  # 更新，返回 False
        assert tree.size == 1
        assert tree.search(10) == "second"
        assert tree.is_valid()
        print("✓ 重复插入测试通过")
    
    def test_multiple_inserts(self):
        """测试多次插入"""
        tree = RedBlackTree[int]()
        data = [7, 3, 18, 10, 22, 8, 11, 26]
        
        for key in data:
            tree.insert(key)
            assert tree.is_valid(), f"插入 {key} 后树不合法"
        
        assert tree.size == len(data)
        assert tree.inorder() == [(k, None) for k in sorted(data)]
        print("✓ 多次插入测试通过")
    
    def test_delete_leaf(self):
        """测试删除叶子节点"""
        tree = RedBlackTree[int]()
        for key in [10, 5, 15, 3]:
            tree.insert(key)
        
        assert tree.delete(3)  # 叶子节点
        assert tree.size == 3
        assert tree.search(3) is None
        assert tree.is_valid()
        print("✓ 删除叶子节点测试通过")
    
    def test_delete_node_with_one_child(self):
        """测试删除有一个子节点的节点"""
        tree = RedBlackTree[int]()
        for key in [10, 5, 15, 12]:
            tree.insert(key)
        
        # 删除 15（有一个子节点 12）
        assert tree.delete(15)
        assert tree.size == 3
        assert 15 not in tree  # 使用 in 操作符检查是否存在
        assert 12 in tree  # 12 应该仍然存在
        assert tree.is_valid()
        print("✓ 删除单子节点测试通过")
    
    def test_delete_node_with_two_children(self):
        """测试删除有两个子节点的节点"""
        tree = RedBlackTree[int]()
        for key in [10, 5, 15, 3, 7, 12, 18]:
            tree.insert(key)
        
        # 删除根节点（有两个子节点）
        assert tree.delete(10)
        assert tree.size == 6
        assert tree.search(10) is None
        assert tree.is_valid()
        print("✓ 删除双子节点测试通过")
    
    def test_delete_nonexistent(self):
        """测试删除不存在的键"""
        tree = RedBlackTree[int]()
        for key in [10, 5, 15]:
            tree.insert(key)
        
        assert not tree.delete(100)
        assert tree.size == 3
        print("✓ 删除不存在键测试通过")
    
    def test_search(self):
        """测试查找"""
        tree = RedBlackTree[int]()
        data = [50, 30, 70, 20, 40, 60, 80]
        
        for key in data:
            tree.insert(key, f"value_{key}")
        
        for key in data:
            assert tree.search(key) == f"value_{key}"
        
        assert tree.search(25) is None
        assert tree.search(100) is None
        print("✓ 查找测试通过")
    
    def test_contains(self):
        """测试 in 操作符"""
        tree = RedBlackTree[str]()
        for key in ["apple", "banana", "cherry"]:
            tree.insert(key)
        
        assert "apple" in tree
        assert "banana" in tree
        assert "grape" not in tree
        print("✓ in 操作符测试通过")
    
    def test_minimum_maximum(self):
        """测试最小最大值"""
        tree = RedBlackTree[int]()
        data = [50, 30, 70, 20, 40, 60, 80]
        
        for key in data:
            tree.insert(key)
        
        assert tree.minimum() == 20
        assert tree.maximum() == 80
        
        # 测试空树
        empty_tree = RedBlackTree[int]()
        assert empty_tree.minimum() is None
        assert empty_tree.maximum() is None
        print("✓ 最小最大值测试通过")
    
    def test_traversals(self):
        """测试遍历"""
        tree = RedBlackTree[int]()
        data = [4, 2, 6, 1, 3, 5, 7]
        
        for key in data:
            tree.insert(key)
        
        # 中序（应该是有序的）
        inorder = tree.inorder()
        assert [k for k, _ in inorder] == [1, 2, 3, 4, 5, 6, 7]
        
        # 前序
        preorder = tree.preorder()
        assert len(preorder) == 7
        assert preorder[0][0] in [4, 2, 3, 6]  # 根可能因为旋转而变化
        
        # 后序
        postorder = tree.postorder()
        assert len(postorder) == 7
        
        print("✓ 遍历测试通过")
    
    def test_range_query(self):
        """测试范围查询"""
        tree = RedBlackTree[int]()
        data = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        for key in data:
            tree.insert(key)
        
        # 范围查询 [25, 65]
        result = tree.range_query(25, 65)
        assert [k for k, _ in result] == [30, 40, 50, 60]
        
        # 范围查询 [10, 90]
        result = tree.range_query(10, 90)
        assert [k for k, _ in result] == data
        
        # 范围查询 [100, 200]（无结果）
        result = tree.range_query(100, 200)
        assert result == []
        
        print("✓ 范围查询测试通过")
    
    def test_successor_predecessor(self):
        """测试后继和前驱"""
        tree = RedBlackTree[int]()
        data = [20, 10, 30, 5, 15, 25, 35]
        
        for key in data:
            tree.insert(key)
        
        # 后继测试
        assert tree.successor(20) == 25
        assert tree.successor(10) == 15
        assert tree.successor(35) is None  # 最大元素无后继
        
        # 前驱测试
        assert tree.predecessor(20) == 15
        assert tree.predecessor(25) == 20
        assert tree.predecessor(5) is None  # 最小元素无前驱
        
        print("✓ 后继前驱测试通过")
    
    def test_rank(self):
        """测试排名"""
        tree = RedBlackTree[int]()
        data = [50, 30, 70, 20, 40, 60, 80]
        
        for key in data:
            tree.insert(key)
        
        # 排名测试（1-based）
        sorted_data = sorted(data)
        for i, key in enumerate(sorted_data, 1):
            assert tree.rank(key) == i, f"Key {key} rank should be {i}, got {tree.rank(key)}"
        
        # 不存在的键
        assert tree.rank(100) == -1
        
        print("✓ 排名测试通过")
    
    def test_height_and_black_height(self):
        """测试高度和黑高度"""
        tree = RedBlackTree[int]()
        
        # 空树
        assert tree.height() == 0
        assert tree.black_height() == 0
        
        # 插入后
        for key in range(1, 100):
            tree.insert(key)
        
        # 红黑树高度不超过 2*log2(n+1)
        import math
        max_height = 2 * math.log2(tree.size + 1)
        assert tree.height() <= max_height
        
        # 黑高度应该合理
        assert tree.black_height() >= 1
        
        print("✓ 高度测试通过")
    
    def test_large_scale_random(self):
        """大规模随机测试"""
        tree = RedBlackTree[int]()
        n = 1000
        
        # 随机插入
        data = list(range(n))
        random.shuffle(data)
        
        for key in data:
            tree.insert(key)
            assert tree.is_valid(), f"插入 {key} 后树不合法"
        
        assert tree.size == n
        
        # 验证中序遍历有序
        inorder = [k for k, _ in tree.inorder()]
        assert inorder == list(range(n))
        
        # 随机删除
        random.shuffle(data)
        for key in data[:500]:  # 删除一半
            tree.delete(key)
            assert tree.is_valid(), f"删除 {key} 后树不合法"
        
        assert tree.size == n - 500
        
        # 验证剩余数据
        remaining = set(data[500:])
        for key in remaining:
            assert key in tree
        
        print("✓ 大规模随机测试通过")
    
    def test_clear(self):
        """测试清空"""
        tree = RedBlackTree[int]()
        for key in range(100):
            tree.insert(key)
        
        tree.clear()
        assert tree.size == 0
        assert tree.is_empty
        assert tree.is_valid()
        print("✓ 清空测试通过")
    
    def test_string_keys(self):
        """测试字符串键"""
        tree = RedBlackTree[str]()
        words = ["apple", "banana", "cherry", "date", "elderberry"]
        
        for word in words:
            tree.insert(word, len(word))
        
        assert tree.size == 5
        assert tree.search("banana") == 6
        assert tree.minimum() == "apple"
        assert tree.maximum() == "elderberry"
        assert tree.is_valid()
        print("✓ 字符串键测试通过")
    
    def test_custom_objects(self):
        """测试自定义对象"""
        class Person:
            def __init__(self, name: str, age: int):
                self.name = name
                self.age = age
            
            def __lt__(self, other):
                return self.age < other.age
            
            def __eq__(self, other):
                return self.age == other.age
            
            def __hash__(self):
                return hash(self.age)
        
        tree = RedBlackTree[Person]()
        people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35)]
        
        for p in people:
            tree.insert(p, p.name)
        
        assert tree.size == 3
        assert tree.is_valid()
        print("✓ 自定义对象测试通过")


class TestRedBlackTreeSet:
    """红黑树集合测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        s = RedBlackTreeSet[int]()
        
        assert s.add(10)
        assert s.add(20)
        assert not s.add(10)  # 已存在
        
        assert len(s) == 2
        assert s.contains(10)
        assert s.contains(20)
        assert not s.contains(30)
        
        assert s.remove(10)
        assert not s.contains(10)
        assert not s.remove(100)  # 不存在
        
        print("✓ Set 基本操作测试通过")
    
    def test_iteration(self):
        """测试迭代"""
        s = create_set([3, 1, 4, 1, 5, 9, 2, 6])
        
        result = list(s)
        assert result == sorted(set([3, 1, 4, 1, 5, 9, 2, 6]))
        print("✓ Set 迭代测试通过")
    
    def test_range_query(self):
        """测试范围查询"""
        s = create_set([10, 20, 30, 40, 50])
        
        result = s.range_query(15, 45)
        assert result == [20, 30, 40]
        print("✓ Set 范围查询测试通过")


class TestRedBlackTreeMap:
    """红黑树映射测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        m = RedBlackTreeMap[str]()
        
        assert m.put("one", 1) is None
        assert m.put("two", 2) is None
        assert m.put("one", 1) == 1  # 更新
        
        assert len(m) == 2
        assert m.get("one") == 1
        assert m.get("two") == 2
        assert m.get("three", 0) == 0  # 默认值
        
        assert m.remove("one") == 1
        assert m.get("one") is None
        
        print("✓ Map 基本操作测试通过")
    
    def test_dict_interface(self):
        """测试字典接口"""
        m = RedBlackTreeMap[str]()
        
        m["a"] = 1
        m["b"] = 2
        m["c"] = 3
        
        assert m["a"] == 1
        assert m["b"] == 2
        
        del m["b"]
        assert "b" not in m
        
        try:
            _ = m["b"]
            assert False, "应该抛出 KeyError"
        except KeyError:
            pass
        
        print("✓ Map 字典接口测试通过")
    
    def test_keys_values_items(self):
        """测试键值对获取"""
        m = create_map({"c": 3, "a": 1, "b": 2})
        
        keys = m.keys()
        assert keys == ["a", "b", "c"]  # 有序
        
        values = m.values()
        assert values == [1, 2, 3]
        
        items = m.items()
        assert items == [("a", 1), ("b", 2), ("c", 3)]
        
        print("✓ Map 键值对测试通过")
    
    def test_floor_ceiling(self):
        """测试 floor 和 ceiling"""
        m = create_map({10: "a", 20: "b", 30: "c", 40: "d", 50: "e"})
        
        assert m.floor_key(25) == 20  # 小于等于的最大
        assert m.floor_key(20) == 20  # 正好等于
        assert m.floor_key(5) is None  # 没有更小的
        
        assert m.ceiling_key(25) == 30  # 大于等于的最小
        assert m.ceiling_key(30) == 30  # 正好等于
        assert m.ceiling_key(60) is None  # 没有更大的
        
        print("✓ floor/ceiling 测试通过")


class TestFactoryFunctions:
    """工厂函数测试"""
    
    def test_create_tree(self):
        """测试 create_tree"""
        tree = create_tree([(3, "three"), (1, "one"), (2, "two")])
        
        assert tree.size == 3
        assert tree.search(2) == "two"
        assert tree.is_valid()
        print("✓ create_tree 测试通过")
    
    def test_create_set(self):
        """测试 create_set"""
        s = create_set([3, 1, 4, 1, 5])
        
        assert len(s) == 4  # 去重
        assert s.is_valid()
        print("✓ create_set 测试通过")
    
    def test_create_map(self):
        """测试 create_map"""
        m = create_map({"a": 1, "b": 2, "c": 3})
        
        assert len(m) == 3
        assert m["b"] == 2
        assert m.is_valid()
        print("✓ create_map 测试通过")


class TestPerformance:
    """性能测试"""
    
    def test_insert_performance(self):
        """插入性能测试"""
        tree = RedBlackTree[int]()
        n = 10000
        
        start = time.time()
        for i in range(n):
            tree.insert(i)
        elapsed = time.time() - start
        
        assert tree.size == n
        assert tree.is_valid()
        print(f"✓ 插入 {n} 个元素: {elapsed:.4f}s")
    
    def test_search_performance(self):
        """查找性能测试"""
        tree = RedBlackTree[int]()
        n = 10000
        
        for i in range(n):
            tree.insert(i)
        
        start = time.time()
        for i in range(n):
            tree.search(i)
        elapsed = time.time() - start
        
        print(f"✓ 查找 {n} 次: {elapsed:.4f}s")
    
    def test_delete_performance(self):
        """删除性能测试"""
        tree = RedBlackTree[int]()
        n = 10000
        
        for i in range(n):
            tree.insert(i)
        
        start = time.time()
        for i in range(n // 2):
            tree.delete(i)
        elapsed = time.time() - start
        
        assert tree.size == n // 2
        assert tree.is_valid()
        print(f"✓ 删除 {n // 2} 个元素: {elapsed:.4f}s")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("红黑树工具模块测试")
    print("=" * 50)
    
    # 红黑树测试
    print("\n--- RedBlackTree Tests ---")
    test_tree = TestRedBlackTree()
    test_tree.test_empty_tree()
    test_tree.test_single_insert()
    test_tree.test_insert_duplicate()
    test_tree.test_multiple_inserts()
    test_tree.test_delete_leaf()
    test_tree.test_delete_node_with_one_child()
    test_tree.test_delete_node_with_two_children()
    test_tree.test_delete_nonexistent()
    test_tree.test_search()
    test_tree.test_contains()
    test_tree.test_minimum_maximum()
    test_tree.test_traversals()
    test_tree.test_range_query()
    test_tree.test_successor_predecessor()
    test_tree.test_rank()
    test_tree.test_height_and_black_height()
    test_tree.test_large_scale_random()
    test_tree.test_clear()
    test_tree.test_string_keys()
    test_tree.test_custom_objects()
    
    # Set 测试
    print("\n--- RedBlackTreeSet Tests ---")
    test_set = TestRedBlackTreeSet()
    test_set.test_basic_operations()
    test_set.test_iteration()
    test_set.test_range_query()
    
    # Map 测试
    print("\n--- RedBlackTreeMap Tests ---")
    test_map = TestRedBlackTreeMap()
    test_map.test_basic_operations()
    test_map.test_dict_interface()
    test_map.test_keys_values_items()
    test_map.test_floor_ceiling()
    
    # 工厂函数测试
    print("\n--- Factory Functions Tests ---")
    test_factory = TestFactoryFunctions()
    test_factory.test_create_tree()
    test_factory.test_create_set()
    test_factory.test_create_map()
    
    # 性能测试
    print("\n--- Performance Tests ---")
    test_perf = TestPerformance()
    test_perf.test_insert_performance()
    test_perf.test_search_performance()
    test_perf.test_delete_performance()
    
    print("\n" + "=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()