"""
AllToolkit - Python AVL Tree Utilities Usage Examples

展示 AVL 树工具模块的各种使用场景

@author AllToolkit
@version 1.0.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    AVLTree, create_avl_tree, from_sorted_list,
    merge_avl_trees, split_avl_tree, avl_tree_to_dict, dict_to_avl_tree,
    find_common_elements, find_difference, validate_avl_tree, get_tree_statistics
)


def example_basic_operations():
    """示例 1: 基本操作"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Operations")
    print("=" * 60)
    
    # 创建 AVL 树
    tree = AVLTree()
    
    # 插入元素
    print("\nInserting elements: 10, 5, 15, 3, 8, 12, 20")
    for key in [10, 5, 15, 3, 8, 12, 20]:
        tree.insert(key)
        print(f"  Inserted {key}, tree size: {tree.size}, height: {tree.height}")
    
    # 查找元素
    print("\nSearching:")
    print(f"  Contains 10: {tree.contains(10)}")
    print(f"  Contains 100: {tree.contains(100)}")
    
    # 最小最大值
    print("\nMin/Max:")
    print(f"  Min: {tree.find_min().key}")
    print(f"  Max: {tree.find_max().key}")
    
    # 删除元素
    print("\nDeleting:")
    print(f"  Delete 10: {tree.delete(10)}")
    print(f"  After delete, size: {tree.size}")
    
    # 转换为列表
    print("\nTree as sorted list:")
    print(f"  {tree.to_list()}")
    
    print("\n✅ Basic operations example completed\n")


def example_with_values():
    """示例 2: 带值的 AVL 树"""
    print("\n" + "=" * 60)
    print("Example 2: AVL Tree with Values (Key-Value Store)")
    print("=" * 60)
    
    # 创建带值的 AVL 树
    tree = AVLTree()
    
    # 插入键值对
    data = {
        "apple": {"color": "red", "price": 1.5},
        "banana": {"color": "yellow", "price": 0.8},
        "cherry": {"color": "red", "price": 2.0},
        "date": {"color": "brown", "price": 3.0},
        "elderberry": {"color": "purple", "price": 5.0},
    }
    
    print("\nInserting fruit data:")
    for key, value in data.items():
        tree.insert(key, value)
        print(f"  {key}: {value}")
    
    # 查找值
    print("\nSearching for values:")
    print(f"  apple: {tree.get_value('apple')}")
    print(f"  banana price: {tree.get_value('banana')['price']}")
    
    # 转换为字典
    print("\nTree as dictionary:")
    d = tree.to_dict()
    for key in sorted(d.keys()):
        print(f"  {key}: {d[key]}")
    
    print("\n✅ Key-value example completed\n")


def example_range_query():
    """示例 3: 范围查询"""
    print("\n" + "=" * 60)
    print("Example 3: Range Queries")
    print("=" * 60)
    
    # 创建树
    tree = create_avl_tree([(i, None) for i in range(1, 21)])
    
    print("\nTree contains 1-20")
    
    # 范围查询
    print("\nRange queries:")
    print(f"  Range [5, 10]: {tree.range_query(5, 10)}")
    print(f"  Range [1, 5]: {tree.range_query(1, 5)}")
    print(f"  Range [15, 20]: {tree.range_query(15, 20)}")
    
    # 范围计数
    print("\nRange counts:")
    print(f"  Count in [5, 15]: {tree.count_range(5, 15)}")
    print(f"  Count in [1, 100]: {tree.count_range(1, 100)}")
    
    # Floor 和 Ceiling
    print("\nFloor and Ceiling:")
    print(f"  Floor of 7: {tree.find_floor(7).key}")
    print(f"  Floor of 7.5: {tree.find_floor(7.5).key}")
    print(f"  Ceiling of 7: {tree.find_ceiling(7).key}")
    print(f"  Ceiling of 7.5: {tree.find_ceiling(7.5).key}")
    
    print("\n✅ Range query example completed\n")


def example_order_statistics():
    """示例 4: 顺序统计"""
    print("\n" + "=" * 60)
    print("Example 4: Order Statistics (K-th Element)")
    print("=" * 60)
    
    # 创建树
    tree = create_avl_tree([(i, None) for i in [10, 5, 15, 3, 8, 12, 20, 1, 7, 14]])
    
    print("\nTree elements (sorted):", tree.to_list())
    
    # 第 k 小
    print("\nK-th smallest elements:")
    for k in range(1, tree.size + 1):
        node = tree.find_kth(k)
        print(f"  {k}-th smallest: {node.key}")
    
    # 排名
    print("\nRank of elements:")
    for key in [1, 5, 10, 15, 20]:
        rank = tree.rank(key)
        print(f"  Rank of {key}: {rank}")
    
    print("\n✅ Order statistics example completed\n")


def example_traversal():
    """示例 5: 遍历"""
    print("\n" + "=" * 60)
    print("Example 5: Tree Traversal")
    print("=" * 60)
    
    # 创建树
    tree = create_avl_tree([(i, None) for i in [10, 5, 15, 3, 8, 12, 20]])
    
    print("\nTree visualization:")
    print(tree.visualize())
    
    print("\nInorder traversal (sorted):")
    print(f"  {list(tree.inorder())}")
    
    print("\nPreorder traversal (root first):")
    print(f"  {list(tree.preorder())}")
    
    print("\nPostorder traversal (root last):")
    print(f"  {list(tree.postorder())}")
    
    print("\nLevel-order traversal (breadth-first):")
    print(f"  {list(tree.level_order())}")
    
    print("\n✅ Traversal example completed\n")


def example_balancing():
    """示例 6: 自动平衡演示"""
    print("\n" + "=" * 60)
    print("Example 6: Self-Balancing Demonstration")
    print("=" * 60)
    
    tree = AVLTree()
    
    print("\nSequential insertion (worst case for BST):")
    print("Inserting: 1, 2, 3, 4, 5, 6, 7")
    
    for i in range(1, 8):
        tree.insert(i)
        print(f"  After insert {i}: height = {tree.height}, balanced = {tree.is_valid_avl()}")
    
    print("\nFinal tree structure:")
    print(tree.visualize())
    
    # 对比理论最大高度
    n = tree.size
    max_height = int(1.44 * math.log2(n + 2))
    print(f"\nTheoretical max height for {n} nodes: ~{max_height}")
    print(f"Actual height: {tree.height}")
    
    print("\n✅ Balancing example completed\n")


def example_merge_split():
    """示例 7: 合并与分割"""
    print("\n" + "=" * 60)
    print("Example 7: Merge and Split Operations")
    print("=" * 60)
    
    # 创建两个树
    tree1 = create_avl_tree([(i, None) for i in [1, 3, 5, 7, 9]])
    tree2 = create_avl_tree([(i, None) for i in [2, 4, 6, 8, 10]])
    
    print("\nTree 1:", tree1.to_list())
    print("Tree 2:", tree2.to_list())
    
    # 合并
    merged = merge_avl_trees(tree1, tree2)
    print("\nMerged tree:", merged.to_list())
    print(f"Merged tree size: {merged.size}, height: {merged.height}")
    
    # 分割
    left, right = split_avl_tree(merged, 5)
    print("\nSplit at key 5:")
    print(f"  Left (< 5): {left.to_list()}")
    print(f"  Right (>= 5): {right.to_list()}")
    
    print("\n✅ Merge/Split example completed\n")


def example_statistics():
    """示例 8: 统计信息"""
    print("\n" + "=" * 60)
    print("Example 8: Tree Statistics")
    print("=" * 60)
    
    # 创建大树
    tree = create_avl_tree([(i, None) for i in range(1, 51)])
    
    stats = get_tree_statistics(tree)
    
    print("\nTree statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 验证
    valid, msg = validate_avl_tree(tree)
    print(f"\nTree validation: {valid}")
    print(f"  Message: {msg}")
    
    print("\n✅ Statistics example completed\n")


def example_predecessor_successor():
    """示例 9: 前驱和后继"""
    print("\n" + "=" * 60)
    print("Example 9: Predecessor and Successor")
    print("=" * 60)
    
    tree = create_avl_tree([(i, None) for i in [1, 3, 5, 7, 9, 11, 13]])
    
    print("\nTree elements:", tree.to_list())
    
    print("\nPredecessors and Successors:")
    for key in [1, 5, 7, 13]:
        pred = tree.predecessor(key)
        succ = tree.successor(key)
        print(f"  Key {key}: predecessor = {pred}, successor = {succ}")
    
    print("\n✅ Predecessor/Successor example completed\n")


def example_path_depth():
    """示例 10: 路径和深度"""
    print("\n" + "=" * 60)
    print("Example 10: Path and Depth")
    print("=" * 60)
    
    tree = create_avl_tree([(i, None) for i in [10, 5, 15, 3, 8, 12, 20]])
    
    print("\nTree visualization:")
    print(tree.visualize())
    
    print("\nDepth of elements:")
    for key in [10, 5, 15, 3, 8, 12, 20]:
        depth = tree.depth(key)
        print(f"  Depth of {key}: {depth}")
    
    print("\nPath to elements:")
    for key in [3, 8, 12, 20]:
        path = tree.path_to(key)
        print(f"  Path to {key}: {path}")
    
    print("\n✅ Path/Depth example completed\n")


def example_dictionary_operations():
    """示例 11: 字典操作"""
    print("\n" + "=" * 60)
    print("Example 11: Dictionary Operations")
    print("=" * 60)
    
    # 从字典创建
    d = {"apple": 1, "banana": 2, "cherry": 3, "date": 4}
    
    print("\nOriginal dictionary:")
    print(f"  {d}")
    
    tree = dict_to_avl_tree(d)
    print("\nConverted to AVL tree:")
    print(f"  Keys (sorted): {tree.keys()}")
    print(f"  Values: {tree.values()}")
    
    # 转回字典
    back_to_dict = avl_tree_to_dict(tree)
    print("\nConverted back to dictionary:")
    print(f"  {back_to_dict}")
    
    print("\n✅ Dictionary operations example completed\n")


def example_common_elements():
    """示例 12: 公共元素和差集"""
    print("\n" + "=" * 60)
    print("Example 12: Set Operations on AVL Trees")
    print("=" * 60)
    
    tree1 = create_avl_tree([(i, None) for i in [1, 2, 3, 4, 5]])
    tree2 = create_avl_tree([(i, None) for i in [3, 4, 5, 6, 7]])
    
    print("\nTree 1:", tree1.to_list())
    print("Tree 2:", tree2.to_list())
    
    # 公共元素
    common = find_common_elements(tree1, tree2)
    print("\nCommon elements:", common)
    
    # 差集
    diff1, diff2 = find_difference(tree1, tree2)
    print("\nDifferences:")
    print(f"  Tree1 only: {diff1}")
    print(f"  Tree2 only: {diff2}")
    
    print("\n✅ Set operations example completed\n")


def example_optimal_building():
    """示例 13: 最优构建"""
    print("\n" + "=" * 60)
    print("Example 13: Optimal Tree Building from Sorted List")
    print("=" * 60)
    
    keys = list(range(1, 16))
    
    print(f"\nBuilding tree from sorted list: {keys}")
    
    # 从有序列表构建（最优）
    optimal_tree = from_sorted_list(keys)
    
    print(f"\nOptimal tree:")
    print(f"  Size: {optimal_tree.size}")
    print(f"  Height: {optimal_tree.height}")
    print(f"  Valid AVL: {optimal_tree.is_valid_avl()}")
    
    print("\nTree structure:")
    print(optimal_tree.visualize())
    
    # 对比顺序插入
    sequential_tree = AVLTree()
    for key in keys:
        sequential_tree.insert(key)
    
    print(f"\nSequential insertion comparison:")
    print(f"  Optimal height: {optimal_tree.height}")
    print(f"  Sequential height: {sequential_tree.height}")
    
    print("\n✅ Optimal building example completed\n")


def example_duplicates():
    """示例 14: 允许重复"""
    print("\n" + "=" * 60)
    print("Example 14: AVL Tree with Duplicate Keys")
    print("=" * 60)
    
    # 创建允许重复的树
    tree = AVLTree(allow_duplicates=True)
    
    print("\nInserting duplicates: 5, 5, 5, 10, 10, 3")
    for key in [5, 5, 5, 10, 10, 3]:
        tree.insert(key)
        print(f"  Inserted {key}, size: {tree.size}")
    
    print(f"\nFinal tree size: {tree.size}")
    print(f"Tree elements: {tree.to_list()}")
    
    # 删除一个重复
    print("\nDeleting one '5':")
    tree.delete(5)
    print(f"  After delete, size: {tree.size}")
    print(f"  Tree elements: {tree.to_list()}")
    
    print("\n✅ Duplicates example completed\n")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("AllToolkit - Python AVL Tree Utilities Examples")
    print("=" * 60)
    
    example_basic_operations()
    example_with_values()
    example_range_query()
    example_order_statistics()
    example_traversal()
    example_balancing()
    example_merge_split()
    example_statistics()
    example_predecessor_successor()
    example_path_depth()
    example_dictionary_operations()
    example_common_elements()
    example_optimal_building()
    example_duplicates()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    import math
    main()