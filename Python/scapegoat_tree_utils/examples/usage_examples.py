"""
替罪羊树 (Scapegoat Tree) 使用示例

替罪羊树是一种简单高效的自平衡二叉搜索树，适用于需要有序集合的场景。
"""

import sys
sys.path.insert(0, '..')
from mod import ScapegoatTree, ScapegoatTreeSet, ScapegoatTreeMultiSet


def example_basic_operations():
    """基本操作示例"""
    print("=" * 50)
    print("基本操作示例")
    print("=" * 50)
    
    # 创建替罪羊树
    tree = ScapegoatTree[int](alpha=0.7)  # alpha 是平衡因子
    
    # 插入元素
    print("\n插入元素: 5, 3, 7, 1, 9, 2, 8, 4, 6")
    for i in [5, 3, 7, 1, 9, 2, 8, 4, 6]:
        tree.insert(i)
    
    print(f"树大小: {tree.size}")
    print(f"树高度: {tree.height}")
    
    # 查找元素
    print("\n查找元素:")
    print(f"  包含 5: {tree.contains(5)}")
    print(f"  包含 10: {tree.contains(10)}")
    
    # 最值查询
    print("\n最值查询:")
    print(f"  最小值: {tree.min()}")
    print(f"  最大值: {tree.max()}")
    
    # 遍历
    print("\n中序遍历 (升序):")
    print(f"  {list(tree.inorder())}")
    
    # 删除元素
    print("\n删除元素 5:")
    tree.delete(5)
    print(f"  删除后: {list(tree.inorder())}")


def example_range_operations():
    """范围操作示例"""
    print("\n" + "=" * 50)
    print("范围操作示例")
    print("=" * 50)
    
    tree = ScapegoatTree[int]()
    
    # 插入 1-100
    for i in range(1, 101):
        tree.insert(i)
    
    # 范围查询
    print("\n范围查询 [20, 30]:")
    result = tree.range_query(20, 30)
    print(f"  {result}")
    
    # 前驱后继
    print("\n前驱和后继:")
    print(f"  50 的前驱: {tree.predecessor(50)}")
    print(f"  50 的后继: {tree.successor(50)}")
    
    # 计数
    print("\n计数:")
    print(f"  小于 50 的元素数: {tree.count_less_than(50)}")
    print(f"  大于 50 的元素数: {tree.count_greater_than(50)}")
    
    # 排名
    print("\n排名:")
    print(f"  50 的排名: {tree.rank(50)}")
    
    # 第 k 小/大
    print("\n第 k 小/大:")
    print(f"  第 10 小: {tree.kth_smallest(10)}")
    print(f"  第 10 大: {tree.kth_largest(10)}")


def example_set_operations():
    """集合操作示例"""
    print("\n" + "=" * 50)
    print("集合操作示例 (ScapegoatTreeSet)")
    print("=" * 50)
    
    s = ScapegoatTreeSet[str]()
    
    # 添加元素
    fruits = ["apple", "banana", "cherry", "date", "elderberry"]
    print(f"\n添加水果: {fruits}")
    for fruit in fruits:
        s.add(fruit)
    
    print(f"集合大小: {len(s)}")
    print(f"是否包含 'banana': {'banana' in s}")
    print(f"是否包含 'grape': {'grape' in s}")
    
    # 集合遍历
    print(f"\n有序遍历: {list(s)}")
    
    # 删除
    s.remove("banana")
    print(f"\n删除 'banana' 后: {list(s)}")
    
    # 范围查询
    print(f"\n范围查询 ['c', 'e']: {s.range_query('c', 'e')}")


def example_multiset_operations():
    """多重集操作示例"""
    print("\n" + "=" * 50)
    print("多重集操作示例 (ScapegoatTreeMultiSet)")
    print("=" * 50)
    
    ms = ScapegoatTreeMultiSet[str]()
    
    # 添加元素（可重复）
    print("\n添加投票:")
    votes = ["Alice", "Bob", "Alice", "Charlie", "Alice", "Bob"]
    for vote in votes:
        ms.add(vote)
        print(f"  添加 {vote}")
    
    print(f"\n总投票数: {len(ms)}")
    print(f"候选人数量: {ms.unique_size}")
    
    # 计数
    print("\n各候选人得票:")
    for candidate in ms.unique_elements():
        print(f"  {candidate}: {ms.count(candidate)} 票")
    
    # 转换为列表
    print(f"\n所有投票: {ms.to_list()}")


def example_custom_objects():
    """自定义对象示例"""
    print("\n" + "=" * 50)
    print("自定义对象示例")
    print("=" * 50)
    
    # 定义学生类
    class Student:
        def __init__(self, id: int, name: str, score: float):
            self.id = id
            self.name = name
            self.score = score
        
        def __repr__(self):
            return f"Student({self.id}, {self.name}, {self.score})"
    
    # 按分数排序的比较器
    def compare_by_score(a: Student, b: Student) -> int:
        if a.score < b.score:
            return -1
        elif a.score > b.score:
            return 1
        return 0
    
    tree = ScapegoatTree[Student](comparator=compare_by_score)
    
    # 添加学生
    students = [
        Student(1, "Alice", 85.5),
        Student(2, "Bob", 92.0),
        Student(3, "Charlie", 78.5),
        Student(4, "Diana", 95.0),
        Student(5, "Eve", 88.0),
    ]
    
    print("\n添加学生:")
    for s in students:
        tree.insert(s)
        print(f"  {s}")
    
    # 按分数排序
    print("\n按分数排序:")
    for s in tree.inorder():
        print(f"  {s.name}: {s.score}")
    
    # 查找最高分和最低分
    print(f"\n最低分: {tree.min()}")
    print(f"最高分: {tree.max()}")


def example_balance_property():
    """平衡性质示例"""
    print("\n" + "=" * 50)
    print("平衡性质示例")
    print("=" * 50)
    
    import math
    
    # 测试不同 alpha 值
    for alpha in [0.55, 0.6, 0.7, 0.8]:
        tree = ScapegoatTree[int](alpha=alpha)
        
        # 顺序插入（最坏情况）
        for i in range(100):
            tree.insert(i)
        
        # 检查平衡
        is_balanced = tree.is_balanced()
        height = tree.height
        max_expected = math.log(tree.size, 1 / alpha)
        
        print(f"\nalpha = {alpha}:")
        print(f"  大小: {tree.size}")
        print(f"  高度: {height}")
        print(f"  理论最大高度: {max_expected:.2f}")
        print(f"  是否平衡: {is_balanced}")


def example_tree_visualization():
    """树可视化示例"""
    print("\n" + "=" * 50)
    print("树可视化示例")
    print("=" * 50)
    
    tree = ScapegoatTree[int]()
    
    # 插入一些元素
    for i in [5, 3, 7, 1, 9, 2, 8]:
        tree.insert(i)
    
    print("\n树结构:")
    print(tree.to_tree_string())


def example_performance():
    """性能示例"""
    print("\n" + "=" * 50)
    print("性能示例")
    print("=" * 50)
    
    import time
    import random
    
    n = 10000
    
    # 插入性能
    tree = ScapegoatTree[int]()
    data = list(range(n))
    random.shuffle(data)
    
    start = time.time()
    for x in data:
        tree.insert(x)
    insert_time = time.time() - start
    
    print(f"\n插入 {n} 个随机元素:")
    print(f"  时间: {insert_time:.4f}s")
    print(f"  树大小: {tree.size}")
    print(f"  树高度: {tree.height}")
    print(f"  是否平衡: {tree.is_balanced()}")
    
    # 查找性能
    random.shuffle(data)
    start = time.time()
    for x in data[:1000]:
        tree.contains(x)
    search_time = time.time() - start
    
    print(f"\n查找 1000 个元素:")
    print(f"  时间: {search_time:.4f}s")
    
    # 范围查询性能
    start = time.time()
    result = tree.range_query(1000, 2000)
    range_time = time.time() - start
    
    print(f"\n范围查询 [1000, 2000]:")
    print(f"  结果数量: {len(result)}")
    print(f"  时间: {range_time:.4f}s")
    
    # 删除性能
    random.shuffle(data)
    start = time.time()
    for x in data[:5000]:
        tree.delete(x)
    delete_time = time.time() - start
    
    print(f"\n删除 5000 个元素:")
    print(f"  时间: {delete_time:.4f}s")
    print(f"  剩余大小: {tree.size}")
    print(f"  是否平衡: {tree.is_balanced()}")


def main():
    """运行所有示例"""
    example_basic_operations()
    example_range_operations()
    example_set_operations()
    example_multiset_operations()
    example_custom_objects()
    example_balance_property()
    example_tree_visualization()
    example_performance()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()