"""
B+树工具使用示例
B+ Tree Utilities Usage Examples

演示 B+ 树的各种用法：
1. 基本增删改查
2. 范围查询
3. 批量操作
4. 序列化
5. 数据库索引模拟
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    BPlusTree, bulk_load, merge_trees, get_tree_stats
)


def example_basic_operations():
    """示例1: 基本增删改查"""
    print("=" * 60)
    print("示例1: 基本增删改查")
    print("=" * 60)
    
    # 创建B+树（阶数4，每个节点最多3个键）
    tree = BPlusTree(order=4)
    
    # 插入数据
    print("\n插入数据:")
    data = [
        (10, "Alice"),
        (5, "Bob"),
        (20, "Charlie"),
        (15, "David"),
        (25, "Eve"),
    ]
    
    for key, value in data:
        tree.insert(key, value)
        print(f"  插入 ({key}, {value})")
    
    # 查询
    print("\n精确查询:")
    print(f"  get(10) = {tree.get(10)}")
    print(f"  get(20) = {tree.get(20)}")
    print(f"  get(999) = {tree.get(999)}")  # 不存在的键
    
    # 使用 [] 操作符
    print("\n使用 [] 操作符:")
    tree[30] = "Frank"
    print(f"  tree[30] = {tree[30]}")
    print(f"  10 in tree = {10 in tree}")
    
    # 更新
    print("\n更新数据:")
    tree.insert(10, "Alice Updated")
    print(f"  更新后 get(10) = {tree.get(10)}")
    
    # 删除
    print("\n删除数据:")
    print(f"  删除前 contains(5) = {tree.contains(5)}")
    tree.delete(5)
    print(f"  删除后 contains(5) = {tree.contains(5)}")
    
    # 统计
    print("\n树统计:")
    print(f"  大小: {tree.size}")
    print(f"  高度: {tree.height}")
    print(f"  最小键值: {tree.get_min()}")
    print(f"  最大键值: {tree.get_max()}")


def example_range_query():
    """示例2: 范围查询"""
    print("\n" + "=" * 60)
    print("示例2: 范围查询")
    print("=" * 60)
    
    tree = BPlusTree(order=8)
    
    # 插入数据
    for i in range(1, 101):
        tree.insert(i, f"Item_{i:03d}")
    
    print(f"\n树中已插入 {tree.size} 条数据")
    
    # 基本范围查询
    print("\n范围查询 [10, 20]:")
    results = tree.range_query(10, 20)
    for key, value in results[:5]:
        print(f"  {key}: {value}")
    if len(results) > 5:
        print(f"  ... 共 {len(results)} 条结果")
    
    # 排除边界
    print("\n范围查询 (10, 20) - 排除边界:")
    results = tree.range_query(10, 20, include_start=False, include_end=False)
    print(f"  {[(k, v) for k, v in results]}")
    
    # 单点查询
    print("\n单点查询 [50, 50]:")
    results = tree.range_query(50, 50)
    print(f"  {results}")
    
    # 获取所有数据
    print(f"\n获取所有键: {len(tree.get_keys())} 个")
    print(f"获取所有值: {len(tree.get_values())} 个")


def example_bulk_operations():
    """示例3: 批量操作"""
    print("\n" + "=" * 60)
    print("示例3: 批量操作")
    print("=" * 60)
    
    # 批量加载
    print("\n批量加载 1000 条数据:")
    items = [(i, f"value_{i}") for i in range(1000)]
    tree = bulk_load(items)
    print(f"  加载完成: {tree.size} 条数据")
    
    # 获取统计信息
    stats = get_tree_stats(tree)
    print("\n树统计信息:")
    print(f"  大小: {stats['size']}")
    print(f"  高度: {stats['height']}")
    print(f"  阶数: {stats['order']}")
    print(f"  叶节点数: {stats['leaf_count']}")
    print(f"  内部节点数: {stats['internal_count']}")
    print(f"  平均叶节点填充: {stats['avg_leaf_fill']:.2f}")
    
    # 合并树
    print("\n合并两棵树:")
    tree1 = BPlusTree(order=4)
    tree2 = BPlusTree(order=4)
    
    for i in range(10):
        tree1.insert(i, f"tree1_{i}")
    
    for i in range(5, 15):
        tree2.insert(i, f"tree2_{i}")
    
    merged = merge_trees(tree1, tree2)
    print(f"  树1大小: {tree1.size}")
    print(f"  树2大小: {tree2.size}")
    print(f"  合并后大小: {merged.size}")


def example_serialization():
    """示例4: 序列化"""
    print("\n" + "=" * 60)
    print("示例4: 序列化")
    print("=" * 60)
    
    # 创建树并插入数据
    tree = BPlusTree(order=4)
    for i in range(20):
        tree.insert(i, f"value_{i}")
    
    print(f"\n原始树: {tree.size} 条数据")
    
    # JSON 序列化
    print("\nJSON 序列化:")
    json_str = tree.to_json()
    print(f"  JSON 长度: {len(json_str)} 字符")
    
    restored = BPlusTree.from_json(json_str)
    print(f"  恢复后大小: {restored.size}")
    print(f"  验证数据: get(10) = {restored.get(10)}")
    
    # Pickle 序列化
    print("\nPickle 序列化:")
    pickle_data = tree.to_pickle()
    print(f"  Pickle 大小: {len(pickle_data)} 字节")
    
    restored = BPlusTree.from_pickle(pickle_data)
    print(f"  恢复后大小: {restored.size}")
    
    # 字典转换
    print("\n字典转换:")
    data_dict = tree.to_dict()
    print(f"  字典键: {list(data_dict.keys())}")
    print(f"  数据项数: {len(data_dict['items'])}")


def example_database_index():
    """示例5: 模拟数据库索引"""
    print("\n" + "=" * 60)
    print("示例5: 模拟数据库索引")
    print("=" * 60)
    
    # 模拟用户表
    users = [
        (1, {"name": "Alice", "age": 30, "city": "Beijing"}),
        (2, {"name": "Bob", "age": 25, "city": "Shanghai"}),
        (3, {"name": "Charlie", "age": 35, "city": "Guangzhou"}),
        (4, {"name": "David", "age": 28, "city": "Shenzhen"}),
        (5, {"name": "Eve", "age": 32, "city": "Hangzhou"}),
    ]
    
    # 创建主键索引
    print("\n创建主键索引 (user_id):")
    primary_index = BPlusTree(order=4)
    for user_id, user_data in users:
        primary_index.insert(user_id, user_data)
    
    print(f"  索引大小: {primary_index.size}")
    print(f"  查找 user_id=3: {primary_index.get(3)}")
    
    # 创建年龄索引（模拟二级索引）
    print("\n创建年龄索引 (age):")
    age_index = BPlusTree(order=4)
    for user_id, user_data in users:
        # 在二级索引中，值是主键
        age_index.insert(user_data["age"], user_id)
    
    print(f"  索引大小: {age_index.size}")
    
    # 年龄范围查询
    print("\n查询年龄 28-32 的用户:")
    age_range = age_index.range_query(28, 32)
    for age, user_id in age_range:
        user = primary_index.get(user_id)
        print(f"  {user['name']}: age={age}, city={user['city']}")
    
    # 验证树结构
    print(f"\n验证索引完整性:")
    print(f"  主键索引: {primary_index.validate()}")
    print(f"  年龄索引: {age_index.validate()}")


def example_iterators():
    """示例6: 迭代器使用"""
    print("\n" + "=" * 60)
    print("示例6: 迭代器使用")
    print("=" * 60)
    
    tree = BPlusTree(order=4)
    
    # 插入一些数据（无序）
    keys = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0]
    for k in keys:
        tree.insert(k, f"val_{k}")
    
    print(f"\n插入了 {tree.size} 条数据（乱序插入）")
    
    # 迭代所有键值对（自动排序）
    print("\n迭代所有键值对（自动排序）:")
    for key, value in tree:
        print(f"  {key}: {value}")
    
    # 仅迭代键
    print("\n仅迭代键:")
    keys_list = list(tree.iterate_keys())
    print(f"  {keys_list}")
    
    # 仅迭代值
    print("\n仅迭代值:")
    values_list = list(tree.iterate_values())
    print(f"  {values_list}")
    
    # 使用列表推导
    print("\n列表推导筛选:")
    filtered = [(k, v) for k, v in tree if k >= 5]
    print(f"  键 >= 5: {filtered}")


def example_print_tree_structure():
    """示例7: 打印树结构"""
    print("\n" + "=" * 60)
    print("示例7: 打印树结构")
    print("=" * 60)
    
    # 使用小阶数以展示分裂
    tree = BPlusTree(order=3)
    
    print("\n插入数据 1-10:")
    for i in range(1, 11):
        tree.insert(i, f"v{i}")
    
    print(f"\n树高度: {tree.height}")
    print(f"树大小: {tree.size}")
    
    print("\n树结构:")
    tree.print_tree()


def main():
    """运行所有示例"""
    example_basic_operations()
    example_range_query()
    example_bulk_operations()
    example_serialization()
    example_database_index()
    example_iterators()
    example_print_tree_structure()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()