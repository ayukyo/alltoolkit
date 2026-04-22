"""
Treap 工具模块使用示例

演示 Treap 和 ImplicitTreap 的主要功能。
"""

import os
import sys
# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import Treap, ImplicitTreap, create_treap, create_implicit_treap


def example_basic_treap():
    """基础 Treap 示例"""
    print("=" * 50)
    print("基础 Treap 示例")
    print("=" * 50)
    
    # 创建 Treap
    treap = Treap()
    
    # 插入元素
    print("\n插入元素: 5, 2, 8, 1, 9, 3, 7")
    for k in [5, 2, 8, 1, 9, 3, 7]:
        treap.insert(k)
    
    print(f"元素数量: {len(treap)}")
    print(f"最小值: {treap.get_min()}")
    print(f"最大值: {treap.get_max()}")
    print(f"排序后列表: {treap.to_sorted_list()}")
    
    # 查找
    print(f"\n查找 5: {treap.contains(5)}")
    print(f"查找 999: {treap.contains(999)}")
    
    # 删除
    print(f"\n删除 5: {treap.delete(5)}")
    print(f"删除后列表: {treap.to_sorted_list()}")


def example_kth_and_rank():
    """第 k 小和排名示例"""
    print("\n" + "=" * 50)
    print("第 k 小元素和排名示例")
    print("=" * 50)
    
    treap = Treap([10, 30, 20, 50, 40])
    print(f"\nTreap 内容: {treap.to_sorted_list()}")
    
    # 第 k 小
    print(f"第 1 小元素: {treap.kth_smallest(1)}")
    print(f"第 3 小元素: {treap.kth_smallest(3)}")
    print(f"第 5 小元素: {treap.kth_smallest(5)}")
    
    # 排名
    print(f"\n10 的排名: {treap.rank(10)}")
    print(f"30 的排名: {treap.rank(30)}")
    print(f"40 的排名: {treap.rank(40)}")


def example_predecessor_successor():
    """前驱后继示例"""
    print("\n" + "=" * 50)
    print("前驱后继示例")
    print("=" * 50)
    
    treap = Treap([1, 3, 5, 7, 9])
    print(f"\nTreap 内容: {treap.to_sorted_list()}")
    
    # 前驱
    print(f"5 的前驱: {treap.predecessor(5)}")
    print(f"7 的前驱: {treap.predecessor(7)}")
    print(f"1 的前驱: {treap.predecessor(1)}")
    print(f"4 的前驱: {treap.predecessor(4)}")
    
    # 后继
    print(f"\n5 的后继: {treap.successor(5)}")
    print(f"3 的后继: {treap.successor(3)}")
    print(f"9 的后继: {treap.successor(9)}")
    print(f"6 的后继: {treap.successor(6)}")


def example_range_operations():
    """区间操作示例"""
    print("\n" + "=" * 50)
    print("区间操作示例")
    print("=" * 50)
    
    treap = Treap([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"\nTreap 内容: {treap.to_sorted_list()}")
    
    # 区间计数
    print(f"\n[1, 10] 内元素数量: {treap.count_range(1, 10)}")
    print(f"[3, 7] 内元素数量: {treap.count_range(3, 7)}")
    
    # 区间查询
    print(f"\n[3, 7] 内元素: {treap.range_query(3, 7)}")
    print(f"[1, 5] 内元素: {treap.range_query(1, 5)}")


def example_split_merge():
    """分裂合并示例"""
    print("\n" + "=" * 50)
    print("分裂合并示例")
    print("=" * 50)
    
    treap = Treap([1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(f"\n原始 Treap: {treap.to_sorted_list()}")
    
    # 分裂
    left, right = treap.split(5)
    print(f"按 5 分裂后:")
    print(f"  左边 (< 5): {left.to_sorted_list()}")
    print(f"  右边 (>= 5): {right.to_sorted_list()}")
    
    # 合并
    merged = left.merge(right)
    print(f"\n合并后: {merged.to_sorted_list()}")


def example_duplicates():
    """重复元素示例"""
    print("\n" + "=" * 50)
    print("重复元素示例")
    print("=" * 50)
    
    treap = Treap()
    keys = [5, 3, 5, 3, 5, 3, 3, 5]
    
    print(f"\n插入元素: {keys}")
    for k in keys:
        treap.insert(k)
    
    print(f"元素总数: {len(treap)}")
    print(f"5 的数量: {treap.search(5)}")
    print(f"3 的数量: {treap.search(3)}")
    print(f"排序后列表: {treap.to_sorted_list()}")
    
    # 删除重复元素
    print(f"\n删除一个 5...")
    treap.delete(5)
    print(f"5 的数量: {treap.search(5)}")
    print(f"元素总数: {len(treap)}")


def example_custom_key():
    """自定义键函数示例"""
    print("\n" + "=" * 50)
    print("自定义键函数示例")
    print("=" * 50)
    
    # 按字符串长度排序
    treap = Treap(key_func=len)
    words = ["a", "bb", "ccc", "dddd", "ee", "f", "ggggg"]
    
    print(f"\n插入单词: {words}")
    for w in words:
        treap.insert(w)
    
    print(f"按长度排序: {treap.to_sorted_list()}")
    print(f"最短的单词: {treap.get_min()}")
    print(f"最长的单词: {treap.get_max()}")


def example_implicit_treap():
    """隐式 Treap 示例"""
    print("\n" + "=" * 50)
    print("隐式 Treap 示例")
    print("=" * 50)
    
    # 初始化
    treap = ImplicitTreap([1, 2, 3, 4, 5])
    print(f"\n初始序列: {treap.to_list()}")
    
    # 位置访问
    print(f"\n索引 0: {treap[0]}")
    print(f"索引 2: {treap[2]}")
    print(f"索引 4: {treap[4]}")
    
    # 位置插入
    print(f"\n在位置 2 插入 99")
    treap.insert_at(2, 99)
    print(f"插入后: {treap.to_list()}")
    
    # 位置删除
    print(f"\n删除位置 0 的元素")
    deleted = treap.delete_at(0)
    print(f"删除的元素: {deleted}")
    print(f"删除后: {treap.to_list()}")
    
    # 区间反转
    print(f"\n反转 [1, 4) 区间")
    treap.reverse_range(1, 4)
    print(f"反转后: {treap.to_list()}")


def example_implicit_treap_operations():
    """隐式 Treap 高级操作示例"""
    print("\n" + "=" * 50)
    print("隐式 Treap 高级操作示例")
    print("=" * 50)
    
    # 构建序列
    treap = ImplicitTreap(list(range(1, 11)))
    print(f"\n原始序列: {treap.to_list()}")
    
    # 完全反转
    print("\n完全反转")
    treap.reverse_range(0, len(treap))
    print(f"反转后: {treap.to_list()}")
    
    # 反转回来
    treap.reverse_range(0, len(treap))
    print(f"再次反转: {treap.to_list()}")
    
    # 多次操作
    print("\n多次操作:")
    treap.insert_at(5, 999)
    print(f"在位置 5 插入 999: {treap.to_list()}")
    
    treap.set_at(0, -1)
    print(f"设置位置 0 为 -1: {treap.to_list()}")
    
    treap.delete_at(len(treap) - 1)
    print(f"删除最后一个元素: {treap.to_list()}")


def example_performance():
    """性能示例"""
    print("\n" + "=" * 50)
    print("性能示例")
    print("=" * 50)
    
    import time
    
    # 大规模插入
    n = 10000
    print(f"\n插入 {n} 个元素...")
    treap = Treap()
    
    start = time.time()
    for i in range(n):
        treap.insert(i)
    insert_time = time.time() - start
    print(f"插入耗时: {insert_time:.3f}s")
    
    # 查找
    print(f"\n查找 {n} 个元素...")
    start = time.time()
    for i in range(n):
        treap.contains(i)
    search_time = time.time() - start
    print(f"查找耗时: {search_time:.3f}s")
    
    # 删除
    print(f"\n删除 {n//2} 个元素...")
    start = time.time()
    for i in range(0, n, 2):
        treap.delete(i)
    delete_time = time.time() - start
    print(f"删除耗时: {delete_time:.3f}s")
    
    print(f"\n最终元素数量: {len(treap)}")
    print(f"树高度: {treap.get_height()} (理论期望约 {n//2 ** 0.5:.1f})")


def example_real_world_usage():
    """实际应用示例"""
    print("\n" + "=" * 50)
    print("实际应用示例 - 动态排名系统")
    print("=" * 50)
    
    # 模拟游戏排行榜
    scores = Treap()
    
    # 玩家得分
    player_scores = [
        1500, 2000, 1800, 1500, 2200,
        1700, 1900, 2100, 1600, 1800
    ]
    
    print("\n玩家得分记录:")
    for i, score in enumerate(player_scores, 1):
        scores.insert(score)
        print(f"  玩家 {i}: {score} 分")
    
    print(f"\n当前排行榜:")
    print(f"  最高分: {scores.get_max()}")
    print(f"  最低分: {scores.get_min()}")
    print(f"  参与人数: {len(scores)}")
    
    # 分数段查询
    print(f"\n分数段统计:")
    print(f"  1500-1600 分: {scores.count_range(1500, 1600)} 人")
    print(f"  1601-1800 分: {scores.count_range(1601, 1800)} 人")
    print(f"  1801-2000 分: {scores.count_range(1801, 2000)} 人")
    print(f"  2001+ 分: {scores.count_range(2001, 9999)} 人")
    
    # 排名查询
    print(f"\n排名查询:")
    print(f"  1800 分的排名: 第 {scores.rank(1800)} 名")
    print(f"  第 3 名的分数: {scores.kth_smallest(len(scores) - 3 + 1)} 分")
    
    # 前驱后继
    print(f"\n目标分数指导:")
    target = 1800
    print(f"  当前分数: {target}")
    print(f"  下一个目标: {scores.successor(target)} 分")
    print(f"  上一个分数: {scores.predecessor(target)} 分")


if __name__ == "__main__":
    example_basic_treap()
    example_kth_and_rank()
    example_predecessor_successor()
    example_range_operations()
    example_split_merge()
    example_duplicates()
    example_custom_key()
    example_implicit_treap()
    example_implicit_treap_operations()
    example_performance()
    example_real_world_usage()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)