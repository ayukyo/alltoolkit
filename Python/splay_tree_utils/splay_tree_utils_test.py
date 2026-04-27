#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Splay Tree 工具模块测试

测试所有核心功能：
- 基本操作（插入、查找、删除）
- 范围查询
- 排名和选择
- 边界情况
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SplayTree, 
    IndexedSplayTree,
    create_splay_tree,
    merge_splay_trees
)


def test_basic_operations():
    """测试基本操作"""
    print("测试基本操作...")
    
    tree = SplayTree[int]()
    
    # 测试空树
    assert tree.is_empty
    assert tree.size == 0
    assert tree.min() is None
    assert tree.max() is None
    
    # 插入
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    tree.insert(1)
    tree.insert(9)
    
    assert not tree.is_empty
    assert tree.size == 5
    
    # 查找
    assert tree.search(5)
    assert tree.search(3)
    assert tree.search(7)
    assert not tree.search(4)
    assert not tree.search(0)
    
    # min/max
    assert tree.min() == 1
    assert tree.max() == 9
    
    print("  ✓ 基本操作测试通过")


def test_delete():
    """测试删除操作"""
    print("测试删除操作...")
    
    tree = SplayTree[int]()
    
    # 删除不存在的元素
    assert not tree.delete(5)
    
    # 插入元素
    for i in [5, 3, 7, 2, 4, 6, 8]:
        tree.insert(i)
    
    assert tree.size == 7
    
    # 删除叶子节点
    assert tree.delete(2)
    assert tree.size == 6
    assert not tree.search(2)
    
    # 删除有一个子节点的节点
    assert tree.delete(3)  # 删除后 4 应该替代它
    assert not tree.search(3)
    
    # 删除有两个子节点的节点
    assert tree.delete(7)
    assert not tree.search(7)
    
    # 验证其他元素仍然存在
    assert tree.search(5)
    assert tree.search(4)
    assert tree.search(6)
    assert tree.search(8)
    
    print("  ✓ 删除操作测试通过")


def test_rank_and_select():
    """测试排名和选择操作"""
    print("测试排名和选择操作...")
    
    tree = SplayTree[int]()
    
    # 插入元素
    for i in [5, 3, 7, 1, 9, 2, 8]:
        tree.insert(i)
    # 有序: [1, 2, 3, 5, 7, 8, 9]
    
    # 测试 kth
    assert tree.kth(1) == 1
    assert tree.kth(2) == 2
    assert tree.kth(3) == 3
    assert tree.kth(4) == 5
    assert tree.kth(5) == 7
    assert tree.kth(6) == 8
    assert tree.kth(7) == 9
    assert tree.kth(0) is None  # 无效
    assert tree.kth(8) is None  # 超出范围
    
    # 测试 rank
    assert tree.rank(1) == 1
    assert tree.rank(2) == 2
    assert tree.rank(3) == 3
    assert tree.rank(5) == 4
    assert tree.rank(9) == 7
    assert tree.rank(4) == 0  # 不存在
    
    # 测试 count_less_than
    assert tree.count_less_than(1) == 0
    assert tree.count_less_than(5) == 3
    assert tree.count_less_than(9) == 6
    assert tree.count_less_than(10) == 7
    
    print("  ✓ 排名和选择测试通过")


def test_predecessor_successor():
    """测试前驱和后继"""
    print("测试前驱和后继...")
    
    tree = SplayTree[int]()
    
    for i in [5, 3, 7, 1, 9]:
        tree.insert(i)
    # 有序: [1, 3, 5, 7, 9]
    
    # 测试前驱
    assert tree.predecessor(5) == 3
    assert tree.predecessor(3) == 1
    assert tree.predecessor(1) is None  # 没有前驱
    assert tree.predecessor(7) == 5
    assert tree.predecessor(4) == 3  # 不存在的元素
    
    # 测试后继
    assert tree.successor(5) == 7
    assert tree.successor(7) == 9
    assert tree.successor(9) is None  # 没有后继
    assert tree.successor(1) == 3
    assert tree.successor(4) == 5  # 不存在的元素
    
    print("  ✓ 前驱和后继测试通过")


def test_range_query():
    """测试范围查询"""
    print("测试范围查询...")
    
    tree = SplayTree[int]()
    
    for i in range(1, 11):
        tree.insert(i, f"value_{i}")
    
    # 范围查询
    result = tree.range_query(3, 7)
    assert len(result) == 5
    keys = [k for k, v in result]
    assert keys == [3, 4, 5, 6, 7]
    
    # 只有下界
    result = tree.range_query(lower=8)
    assert len(result) == 3
    
    # 只有上界
    result = tree.range_query(upper=2)
    assert len(result) == 2
    
    # 无界
    result = tree.range_query()
    assert len(result) == 10
    
    print("  ✓ 范围查询测试通过")


def test_iteration():
    """测试迭代功能"""
    print("测试迭代功能...")
    
    tree = SplayTree[int]()
    
    for i in [5, 3, 7, 1, 9, 2, 8]:
        tree.insert(i)
    
    # 测试有序遍历
    keys = list(tree.keys())
    assert keys == [1, 2, 3, 5, 7, 8, 9]
    
    # 测试 to_sorted_list
    assert tree.to_sorted_list() == [1, 2, 3, 5, 7, 8, 9]
    
    # 测试 in 操作符
    assert 5 in tree
    assert 4 not in tree
    
    # 测试 len
    assert len(tree) == 7
    
    print("  ✓ 迭代功能测试通过")


def test_value_storage():
    """测试值存储"""
    print("测试值存储...")
    
    tree = SplayTree[str]()
    
    # 插入带值的节点
    tree.insert("apple", 1)
    tree.insert("banana", 2)
    tree.insert("cherry", 3)
    
    # 获取值
    assert tree.get("apple") == 1
    assert tree.get("banana") == 2
    assert tree.get("cherry") == 3
    assert tree.get("grape") is None
    
    # 更新值
    tree.insert("apple", 10)
    assert tree.get("apple") == 10
    
    print("  ✓ 值存储测试通过")


def test_clear():
    """测试清空操作"""
    print("测试清空操作...")
    
    tree = SplayTree[int]()
    
    for i in range(10):
        tree.insert(i)
    
    assert tree.size == 10
    
    tree.clear()
    
    assert tree.is_empty
    assert tree.size == 0
    assert tree.min() is None
    assert tree.max() is None
    
    print("  ✓ 清空操作测试通过")


def test_duplicated_keys():
    """测试重复键"""
    print("测试重复键...")
    
    tree = SplayTree[int]()
    
    # 插入相同键（应该更新值）
    tree.insert(5, "first")
    tree.insert(5, "second")
    tree.insert(5, "third")
    
    assert tree.size == 1
    assert tree.get(5) == "third"
    
    print("  ✓ 重复键测试通过")


def test_create_from_list():
    """测试从列表创建"""
    print("测试从列表创建...")
    
    # 注意：SplayTree 作为字典使用，重复键会覆盖
    tree = create_splay_tree([3, 1, 4, 5, 9, 2, 6, 8])
    
    assert tree.size == 8
    assert tree.to_sorted_list() == [1, 2, 3, 4, 5, 6, 8, 9]
    
    # 测试带键函数（使用不同长度的字符串）
    items = ["a", "bb", "ccc", "dddd"]
    tree2 = create_splay_tree(items, key_func=lambda x: len(x))
    assert tree2.size == 4
    assert tree2.to_sorted_list() == [1, 2, 3, 4]
    
    print("  ✓ 从列表创建测试通过")


def test_merge_trees():
    """测试合并树"""
    print("测试合并树...")
    
    tree1 = create_splay_tree([1, 2, 3])
    tree2 = create_splay_tree([4, 5, 6])
    
    merged = merge_splay_trees(tree1, tree2)
    
    assert merged.size == 6
    assert merged.to_sorted_list() == [1, 2, 3, 4, 5, 6]
    
    print("  ✓ 合并树测试通过")


def test_large_dataset():
    """测试大数据集"""
    print("测试大数据集...")
    
    import random
    
    tree = SplayTree[int]()
    data = list(range(1000))
    random.shuffle(data)
    
    # 插入
    for x in data:
        tree.insert(x)
    
    assert tree.size == 1000
    
    # 查找
    for x in range(1000):
        assert tree.search(x)
    
    # 排名
    for i in range(1000):
        assert tree.rank(i) == i + 1
        assert tree.kth(i + 1) == i
    
    # 删除一半
    for x in range(0, 1000, 2):
        assert tree.delete(x)
    
    assert tree.size == 500
    
    # 验证奇数仍然存在
    for x in range(1, 1000, 2):
        assert tree.search(x)
    
    print("  ✓ 大数据集测试通过")


def test_indexed_splay_tree():
    """测试索引伸展树"""
    print("测试索引伸展树...")
    
    seq = IndexedSplayTree[int]()
    
    # 追加元素
    seq.append(1)
    seq.append(2)
    seq.append(3)
    
    assert len(seq) == 3
    assert seq[0] == 1
    assert seq[1] == 2
    assert seq[2] == 3
    
    # 负索引
    assert seq[-1] == 3
    assert seq[-2] == 2
    
    # 修改
    seq[1] = 10
    assert seq[1] == 10
    
    print("  ✓ 索引伸展树测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    tree = SplayTree[int]()
    
    # 单元素操作
    tree.insert(42)
    assert tree.size == 1
    assert tree.min() == 42
    assert tree.max() == 42
    assert tree.predecessor(42) is None
    assert tree.successor(42) is None
    assert tree.delete(42)
    assert tree.is_empty
    
    # 删除后重新插入
    tree.insert(10)
    tree.insert(20)
    tree.delete(10)
    assert tree.size == 1
    assert tree.search(20)
    
    print("  ✓ 边界情况测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Splay Tree 工具模块测试")
    print("=" * 50)
    
    test_basic_operations()
    test_delete()
    test_rank_and_select()
    test_predecessor_successor()
    test_range_query()
    test_iteration()
    test_value_storage()
    test_clear()
    test_duplicated_keys()
    test_create_from_list()
    test_merge_trees()
    test_large_dataset()
    test_indexed_splay_tree()
    test_edge_cases()
    
    print("=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()