#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Splay Tree 工具模块使用示例

展示如何使用伸展树的各种功能：
1. 基本操作
2. 范围查询
3. 排名和选择
4. 序列操作
5. 实际应用场景
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SplayTree, 
    IndexedSplayTree,
    create_splay_tree,
    merge_splay_trees
)


def example_basic_operations():
    """基本操作示例"""
    print("\n" + "=" * 50)
    print("示例 1: 基本操作")
    print("=" * 50)
    
    # 创建伸展树
    tree = SplayTree[int]()
    
    # 插入元素
    print("\n插入元素: 5, 3, 7, 1, 9, 4, 6, 8, 2")
    for x in [5, 3, 7, 1, 9, 4, 6, 8, 2]:
        tree.insert(x)
    
    print(f"树大小: {tree.size}")
    print(f"最小值: {tree.min()}")
    print(f"最大值: {tree.max()}")
    print(f"有序遍历: {tree.to_sorted_list()}")
    
    # 查找
    print(f"\n查找 5: {tree.search(5)}")
    print(f"查找 10: {tree.search(10)}")
    
    # 删除
    print(f"\n删除 5: {tree.delete(5)}")
    print(f"删除后有序遍历: {tree.to_sorted_list()}")


def example_with_values():
    """带值的伸展树示例"""
    print("\n" + "=" * 50)
    print("示例 2: 带值的伸展树（键值对存储）")
    print("=" * 50)
    
    # 创建存储学生信息的伸展树
    students = SplayTree[int]()
    
    # 插入学生数据（学号 -> 姓名）
    students.insert(1001, "张三")
    students.insert(1002, "李四")
    students.insert(1003, "王五")
    students.insert(1005, "赵六")
    students.insert(1008, "钱七")
    
    print("\n学生信息:")
    for sid, name in students.items():
        print(f"  学号 {sid}: {name}")
    
    # 查找学生
    print(f"\n查找学号 1002: {students.get(1002)}")
    print(f"查找学号 1004: {students.get(1004)}")
    
    # 更新学生姓名
    students.insert(1002, "李四（已改名）")
    print(f"\n更新后学号 1002: {students.get(1002)}")


def example_range_query():
    """范围查询示例"""
    print("\n" + "=" * 50)
    print("示例 3: 范围查询")
    print("=" * 50)
    
    # 创建伸展树存储分数
    scores = SplayTree[int]()
    
    # 插入分数
    scores_list = [78, 92, 85, 67, 88, 95, 72, 81, 90, 76]
    for s in scores_list:
        scores.insert(s)
    
    print(f"所有分数（升序）: {scores.to_sorted_list()}")
    
    # 查询 80-90 分的分数
    result = scores.range_query(80, 90)
    print(f"\n80-90 分区间: {[k for k, v in result]}")
    
    # 查询 90 分以上
    high_scores = scores.range_query(lower=90)
    print(f"90 分以上: {[k for k, v in high_scores]}")
    
    # 查询 70 分以下
    low_scores = scores.range_query(upper=70)
    print(f"70 分以下: {[k for k, v in low_scores]}")


def example_rank_and_select():
    """排名和选择示例"""
    print("\n" + "=" * 50)
    print("示例 4: 排名和选择（Kth 元素）")
    print("=" * 50)
    
    # 创建伸展树
    tree = create_splay_tree([5, 2, 8, 1, 9, 3, 7, 4, 6])
    
    print(f"有序序列: {tree.to_sorted_list()}")
    
    # 找第 k 小的元素
    print("\n第 k 小的元素:")
    for k in [1, 3, 5, 9]:
        print(f"  第 {k} 小: {tree.kth(k)}")
    
    # 查找元素的排名
    print("\n元素的排名:")
    for x in [1, 5, 9, 6]:
        print(f"  {x} 的排名: {tree.rank(x)}")
    
    # 统计小于某个值的元素数量
    print("\n小于某值的元素数量:")
    for x in [1, 5, 10]:
        print(f"  小于 {x}: {tree.count_less_than(x)}")


def example_predecessor_successor():
    """前驱和后继示例"""
    print("\n" + "=" * 50)
    print("示例 5: 前驱和后继")
    print("=" * 50)
    
    tree = create_splay_tree([10, 5, 15, 3, 7, 12, 20])
    
    print(f"有序序列: {tree.to_sorted_list()}")
    
    print("\n前驱（小于某值的最大值）:")
    for x in [5, 10, 15, 20]:
        pred = tree.predecessor(x)
        print(f"  {x} 的前驱: {pred}")
    
    print("\n后继（大于某值的最小值）:")
    for x in [5, 10, 15, 20]:
        succ = tree.successor(x)
        print(f"  {x} 的后继: {succ}")


def example_merge_trees():
    """合并树示例"""
    print("\n" + "=" * 50)
    print("示例 6: 合并两棵树")
    print("=" * 50)
    
    # 创建两棵树
    tree1 = create_splay_tree([1, 2, 3, 4, 5])
    tree2 = create_splay_tree([6, 7, 8, 9, 10])
    
    print(f"树1: {tree1.to_sorted_list()}")
    print(f"树2: {tree2.to_sorted_list()}")
    
    # 合并（要求 tree1 所有元素小于 tree2）
    merged = merge_splay_trees(tree1, tree2)
    print(f"合并后: {merged.to_sorted_list()}")


def example_application_cache():
    """应用示例: 最近访问缓存"""
    print("\n" + "=" * 50)
    print("示例 7: 应用 - 最近访问缓存（LRU 风格）")
    print("=" * 50)
    
    class RecentCache:
        """利用伸展树实现最近访问缓存"""
        
        def __init__(self):
            self.tree = SplayTree[int]()
            self.access_time = 0
        
        def access(self, key: int):
            """访问一个键"""
            self.access_time += 1
            # 使用 (key, access_time) 作为复合键
            # 最近访问的会被伸展到根部
            self.tree.insert(key, self.access_time)
            print(f"访问 {key}，时间戳: {self.access_time}")
        
        def get_recent(self):
            """获取最近访问的键（根节点）"""
            if self.tree.root:
                return self.tree.root.key
            return None
    
    cache = RecentCache()
    
    print("访问顺序: 1 -> 2 -> 3 -> 1 -> 4 -> 1")
    cache.access(1)
    cache.access(2)
    cache.access(3)
    cache.access(1)  # 再次访问 1
    cache.access(4)
    cache.access(1)  # 再次访问 1
    
    print(f"\n最近访问的键: {cache.get_recent()}")
    print("伸展树的特性：最近访问的元素更靠近根节点")


def example_application_leaderboard():
    """应用示例: 排行榜"""
    print("\n" + "=" * 50)
    print("示例 8: 应用 - 游戏排行榜")
    print("=" * 50)
    
    # 使用伸展树存储玩家分数
    leaderboard = SplayTree[int]()
    
    # 添加玩家分数
    players = [
        (1500, "玩家A"),
        (2000, "玩家B"),
        (1800, "玩家C"),
        (1200, "玩家D"),
        (2500, "玩家E"),
        (1700, "玩家F"),
    ]
    
    for score, name in players:
        leaderboard.insert(score, name)
    
    print("所有玩家（按分数升序）:")
    for score, name in leaderboard.items():
        print(f"  分数 {score}: {name}")
    
    # 查询高分玩家（前3名）
    print("\n前3名玩家:")
    total = leaderboard.size
    for i in range(3):
        rank = total - i
        score = leaderboard.kth(rank)
        if score:
            name = leaderboard.get(score)
            print(f"  第 {i+1} 名: {name} (分数: {score})")
    
    # 查询分数在 1500-2000 之间的玩家
    print("\n分数在 1500-2000 之间的玩家:")
    for score, name in leaderboard.range_query(1500, 2000):
        print(f"  {name}: {score}")


def example_application_time_series():
    """应用示例: 时间序列数据"""
    print("\n" + "=" * 50)
    print("示例 9: 应用 - 时间序列数据存储")
    print("=" * 50)
    
    # 使用伸展树存储时间戳 -> 数据
    time_series = SplayTree[int]()
    
    # 添加数据点
    data = [
        (1000, "事件A"),
        (1010, "事件B"),
        (1020, "事件C"),
        (1030, "事件D"),
        (1040, "事件E"),
        (1050, "事件F"),
    ]
    
    for timestamp, event in data:
        time_series.insert(timestamp, event)
    
    print("时间序列数据:")
    for ts, event in time_series.items():
        print(f"  {ts}: {event}")
    
    # 查询时间范围
    print("\n1015-1045 时间段的事件:")
    for ts, event in time_series.range_query(1015, 1045):
        print(f"  {ts}: {event}")
    
    # 查找最接近的时间戳
    query_time = 1025
    pred = time_series.predecessor(query_time)
    succ = time_series.successor(query_time)
    print(f"\n最接近 {query_time} 的:")
    print(f"  前一个: {pred} ({time_series.get(pred)})")
    print(f"  后一个: {succ} ({time_series.get(succ)})")


def example_indexed_tree():
    """索引伸展树示例"""
    print("\n" + "=" * 50)
    print("示例 10: 索引伸展树（序列操作）")
    print("=" * 50)
    
    # 创建序列
    seq = IndexedSplayTree[str](["A", "B", "C", "D", "E"])
    
    print(f"初始序列: {list(seq._tree.values())}")
    
    # 按索引访问
    print(f"\n按索引访问:")
    print(f"  seq[0] = {seq[0]}")
    print(f"  seq[2] = {seq[2]}")
    print(f"  seq[-1] = {seq[-1]}")
    
    # 修改元素
    seq[2] = "X"
    print(f"\n修改 seq[2] = 'X' 后: {list(seq._tree.values())}")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("Splay Tree (伸展树) 工具模块 - 使用示例")
    print("=" * 50)
    
    example_basic_operations()
    example_with_values()
    example_range_query()
    example_rank_and_select()
    example_predecessor_successor()
    example_merge_trees()
    example_application_cache()
    example_application_leaderboard()
    example_application_time_series()
    example_indexed_tree()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()