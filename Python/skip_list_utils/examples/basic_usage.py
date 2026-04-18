"""
Skip List 基础用法示例

演示跳表的基本操作：插入、查找、删除、范围查询等。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SkipList, ConcurrentSkipList, SkipListSet,
    create_skip_list, create_sorted_dict
)


def basic_operations():
    """基础操作示例"""
    print("=" * 60)
    print("基础操作示例")
    print("=" * 60)
    
    # 创建跳表
    sl = SkipList[int]()
    
    # 插入元素
    sl.insert(5, "five")
    sl.insert(2, "two")
    sl.insert(8, "eight")
    sl.insert(1, "one")
    sl.insert(9, "nine")
    
    print(f"插入 5 个元素后，大小: {sl.size}")
    print(f"元素（按 key 排序）: {sl.to_list()}")
    
    # 查找
    print(f"\n查找 key=5: {sl.search(5)}")
    print(f"查找 key=10（不存在）: {sl.search(10)}")
    print(f"key=8 存在吗? {8 in sl}")
    
    # 使用 [] 运算符
    print(f"\n使用 [] 获取 key=2: {sl[2]}")
    sl[2] = "TWO"  # 更新
    print(f"更新 key=2 后: {sl[2]}")
    
    # 删除
    print(f"\n删除 key=5: {sl.delete(5)}")
    print(f"删除后大小: {sl.size}")
    print(f"元素: {sl.to_list()}")


def range_queries():
    """范围查询示例"""
    print("\n" + "=" * 60)
    print("范围查询示例")
    print("=" * 60)
    
    sl = SkipList[int]()
    for i in range(1, 21):
        sl.insert(i, i * 10)
    
    print(f"插入了 1-20 的元素")
    
    # 范围查询
    print(f"\n范围 [5, 10]: {list(sl.range(5, 10))}")
    print(f"范围 (5, 10)（不含边界）: {list(sl.range(5, 10, inclusive=False))}")
    print(f"从 15 开始: {list(sl.range(start_key=15))}")
    print(f"到 5 为止: {list(sl.range(end_key=5))}")
    
    # 计数
    print(f"\n[5, 10] 范围内元素数量: {sl.count_range(5, 10)}")


def navigation_methods():
    """导航方法示例"""
    print("\n" + "=" * 60)
    print("导航方法示例")
    print("=" * 60)
    
    sl = SkipList[int]()
    for i in [5, 2, 8, 1, 9, 3, 7]:
        sl.insert(i, str(i))
    
    print(f"元素: {sl.to_list()}")
    
    # 最小/最大
    print(f"\n最小元素: {sl.first()}")
    print(f"最大元素: {sl.last()}")
    print(f"最小 key: {sl.min_key()}")
    print(f"最大 key: {sl.max_key()}")
    
    # 前驱/后继
    print(f"\nkey=5 的前驱: {sl.predecessor(5)}")
    print(f"key=5 的后继: {sl.successor(5)}")
    print(f"key=4（不存在）的前驱: {sl.predecessor(4)}")
    print(f"key=4（不存在）的后继: {sl.successor(4)}")


def skip_list_set_example():
    """SkipListSet 示例"""
    print("\n" + "=" * 60)
    print("SkipListSet 示例")
    print("=" * 60)
    
    s1 = SkipListSet[int].from_iterable([5, 2, 8, 1, 9])
    s2 = SkipListSet[int].from_iterable([8, 9, 10, 11])
    
    print(f"s1: {s1.to_list()}")
    print(f"s2: {s2.to_list()}")
    
    # 集合操作
    print(f"\n并集: {s1.union(s2).to_list()}")
    print(f"交集: {s1.intersection(s2).to_list()}")
    print(f"差集 (s1 - s2): {s1.difference(s2).to_list()}")
    
    # 子集判断
    s3 = SkipListSet[int].from_iterable([2, 5])
    print(f"\n{list(s3)} 是 {list(s1)} 的子集? {s3.issubset(s1)}")
    
    # 范围查询
    print(f"\ns1 中 [2, 8] 范围内的元素: {list(s1.range(2, 8))}")


def concurrent_example():
    """并发跳表示例"""
    print("\n" + "=" * 60)
    print("并发跳表示例")
    print("=" * 60)
    
    import threading
    
    sl = ConcurrentSkipList[int]()
    
    def insert_range(start, count):
        for i in range(start, start + count):
            sl.insert(i, f"value_{i}")
    
    # 创建多个线程并发插入
    threads = []
    for i in range(3):
        t = threading.Thread(target=insert_range, args=(i * 100, 100))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"并发插入后大小: {sl.size}")
    print(f"最小 key: {sl.min_key()}")
    print(f"最大 key: {sl.max_key()}")


def utility_functions():
    """工具函数示例"""
    print("\n" + "=" * 60)
    print("工具函数示例")
    print("=" * 60)
    
    # 从列表创建
    items = [(3, "c"), (1, "a"), (2, "b")]
    sl = create_skip_list(items)
    print(f"从列表创建: {sl.to_list()}")
    
    # 从字典创建有序字典
    d = {"z": 26, "a": 1, "m": 13}
    sorted_dict = create_sorted_dict(d)
    print(f"从字典创建有序字典: {sorted_dict.to_dict()}")


def visualization():
    """可视化示例"""
    print("\n" + "=" * 60)
    print("跳表结构可视化")
    print("=" * 60)
    
    sl = SkipList[int]()
    sl.seed(42)  # 固定随机种子以获得确定性结构
    
    for i in [5, 2, 8, 1, 9, 3, 7]:
        sl.insert(i, i)
    
    print(sl.visualize())


def string_keys_example():
    """字符串 key 示例"""
    print("\n" + "=" * 60)
    print("字符串 Key 示例")
    print("=" * 60)
    
    # 字符串按字典序排序
    sl = SkipList[str]()
    
    words = ["banana", "apple", "cherry", "date", "elderberry"]
    for word in words:
        sl.insert(word, len(word))
    
    print("单词按字典序排序:")
    for word, length in sl:
        print(f"  {word}: {length}")


def time_series_example():
    """时间序列示例"""
    print("\n" + "=" * 60)
    print("时间序列示例（使用元组作为 key）")
    print("=" * 60)
    
    # 使用元组作为复合 key： (日期, 时间)
    sl = SkipList[tuple]()
    
    events = [
        ((2024, 1, 15, 10, 30), "会议开始"),
        ((2024, 1, 15, 9, 0), "到达办公室"),
        ((2024, 1, 15, 12, 0), "午餐"),
        ((2024, 1, 15, 11, 0), "代码审查"),
        ((2024, 1, 15, 14, 0), "项目讨论"),
    ]
    
    for time_key, event in events:
        sl.insert(time_key, event)
    
    print("按时间顺序的事件:")
    for time_key, event in sl:
        print(f"  {time_key}: {event}")
    
    # 范围查询：10点到14点之间的事件
    print("\n10:00-14:00 之间的事件:")
    start = (2024, 1, 15, 10, 0)
    end = (2024, 1, 15, 14, 0)
    for time_key, event in sl.range(start, end):
        print(f"  {time_key}: {event}")


if __name__ == "__main__":
    basic_operations()
    range_queries()
    navigation_methods()
    skip_list_set_example()
    concurrent_example()
    utility_functions()
    visualization()
    string_keys_example()
    time_series_example()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)