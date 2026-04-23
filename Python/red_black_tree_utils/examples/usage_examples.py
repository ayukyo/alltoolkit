"""
Red-Black Tree Utils - 使用示例

本示例展示红黑树的各种使用场景：
1. 基本操作（插入、删除、查找）
2. 范围查询
3. 集合操作
4. 有序映射
5. 实际应用场景
"""

import sys
import os
import time
import random

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    RedBlackTree, RedBlackTreeSet, RedBlackTreeMap,
    create_tree, create_set, create_map
)


def example_basic_operations():
    """示例1: 基本操作"""
    print("=" * 50)
    print("示例1: 红黑树基本操作")
    print("=" * 50)
    
    # 创建红黑树
    tree = RedBlackTree[int]()
    
    # 插入数据
    print("\n插入数据: 50, 30, 70, 20, 40, 60, 80")
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key, f"value_{key}")
    
    print(f"树大小: {tree.size}")
    print(f"树高度: {tree.height()}")
    print(f"黑高度: {tree.black_height()}")
    print(f"是否合法: {tree.is_valid()}")
    
    # 查找
    print(f"\n查找 40: {tree.search(40)}")
    print(f"查找 100: {tree.search(100)}")
    print(f"40 in tree: {40 in tree}")
    
    # 最小最大
    print(f"\n最小值: {tree.minimum()}")
    print(f"最大值: {tree.maximum()}")
    
    # 中序遍历（有序）
    print(f"\n中序遍历: {[k for k, _ in tree.inorder()]}")
    
    # 删除
    print("\n删除 30...")
    tree.delete(30)
    print(f"删除后中序遍历: {[k for k, _ in tree.inorder()]}")
    print(f"删除后是否合法: {tree.is_valid()}")
    print()


def example_range_query():
    """示例2: 范围查询"""
    print("=" * 50)
    print("示例2: 范围查询")
    print("=" * 50)
    
    # 创建树并插入数据
    tree = RedBlackTree[int]()
    data = [15, 10, 20, 8, 12, 17, 25, 6, 11, 13, 16, 19, 22, 30]
    
    for key in data:
        tree.insert(key)
    
    print(f"树数据: {sorted(data)}")
    
    # 范围查询
    print(f"\n范围 [10, 20]: {[k for k, _ in tree.range_query(10, 20)]}")
    print(f"范围 [15, 25]: {[k for k, _ in tree.range_query(15, 25)]}")
    print(f"范围 [1, 5]: {[k for k, _ in tree.range_query(1, 5)]}")
    print()


def example_successor_predecessor():
    """示例3: 前驱和后继"""
    print("=" * 50)
    print("示例3: 前驱和后继")
    print("=" * 50)
    
    tree = RedBlackTree[int]()
    for key in [10, 5, 15, 3, 7, 12, 18]:
        tree.insert(key)
    
    print("树数据: [3, 5, 7, 10, 12, 15, 18]")
    
    # 后继
    print("\n后继查询:")
    for key in [3, 5, 7, 10, 12, 15, 18]:
        succ = tree.successor(key)
        print(f"  {key} 的后继: {succ}")
    
    # 前驱
    print("\n前驱查询:")
    for key in [3, 5, 7, 10, 12, 15, 18]:
        pred = tree.predecessor(key)
        print(f"  {key} 的前驱: {pred}")
    print()


def example_set_operations():
    """示例4: 集合操作"""
    print("=" * 50)
    print("示例4: 红黑树集合")
    print("=" * 50)
    
    # 创建集合
    s = create_set([30, 10, 50, 20, 40])
    
    print(f"集合内容: {list(s)}")
    print(f"最小元素: {s.minimum()}")
    print(f"最大元素: {s.maximum()}")
    
    # 添加和删除
    s.add(25)
    print(f"\n添加 25 后: {list(s)}")
    
    s.remove(30)
    print(f"删除 30 后: {list(s)}")
    
    # 包含测试
    print(f"\n包含 20: {20 in s}")
    print(f"包含 100: {100 in s}")
    
    # 范围查询
    print(f"\n范围 [15, 35]: {s.range_query(15, 35)}")
    print()


def example_map_operations():
    """示例5: 有序映射"""
    print("=" * 50)
    print("示例5: 红黑树映射（有序字典）")
    print("=" * 50)
    
    # 创建映射
    scores = RedBlackTreeMap[str]()
    
    # 添加数据
    scores["Alice"] = 95
    scores["Bob"] = 87
    scores["Charlie"] = 92
    scores["David"] = 78
    scores["Eve"] = 88
    
    print(f"学生成绩（按名字排序）:")
    for name, score in scores.items():
        print(f"  {name}: {score}")
    
    # 字典式操作
    print(f"\nAlice 的成绩: {scores['Alice']}")
    print(f"Frank 的成绩: {scores.get('Frank', '未找到')}")
    
    # 更新
    scores["Alice"] = 98
    print(f"\n更新后 Alice 的成绩: {scores['Alice']}")
    
    # floor 和 ceiling
    print("\n按成绩查找:")
    ages = create_map({20: "二十", 30: "三十", 40: "四十", 50: "五十"})
    print(f"  小于等于 35 的最大键: {ages.floor_key(35)} -> {ages.get(ages.floor_key(35))}")
    print(f"  大于等于 35 的最小键: {ages.ceiling_key(35)} -> {ages.get(ages.ceiling_key(35))}")
    print()


def example_event_scheduler():
    """示例6: 事件调度器"""
    print("=" * 50)
    print("示例6: 事件调度器（实际应用）")
    print("=" * 50)
    
    class EventScheduler:
        """使用红黑树实现的事件调度器"""
        
        def __init__(self):
            self._events = RedBlackTreeMap[int]()
        
        def schedule(self, timestamp: int, event: str):
            """安排事件"""
            if timestamp in self._events:
                self._events[timestamp].append(event)
            else:
                self._events[timestamp] = [event]
        
        def cancel(self, timestamp: int, event: str = None):
            """取消事件"""
            if timestamp in self._events:
                if event:
                    events = self._events[timestamp]
                    if event in events:
                        events.remove(event)
                        if not events:
                            del self._events[timestamp]
                else:
                    del self._events[timestamp]
        
        def get_events_in_range(self, start: int, end: int):
            """获取时间范围内的事件"""
            result = []
            for ts, events in self._events.range_query(start, end):
                for event in events:
                    result.append((ts, event))
            return result
        
        def get_next_event(self, timestamp: int):
            """获取下一个事件"""
            key = self._events.ceiling_key(timestamp)
            if key:
                events = self._events[key]
                return (key, events[0]) if events else None
            return None
        
        def show_all(self):
            """显示所有事件"""
            return list(self._events.items())
    
    # 使用事件调度器
    scheduler = EventScheduler()
    
    # 安排事件
    scheduler.schedule(1000, "会议开始")
    scheduler.schedule(1500, "午休")
    scheduler.schedule(2000, "项目评审")
    scheduler.schedule(2500, "下班")
    scheduler.schedule(1000, "签到")
    
    print("所有事件:")
    for timestamp, events in scheduler.show_all():
        print(f"  {timestamp}: {events}")
    
    print(f"\n时间范围 [1200, 2200] 的事件:")
    for ts, event in scheduler.get_events_in_range(1200, 2200):
        print(f"  {ts}: {event}")
    
    print(f"\n从时间 1300 开始的下一个事件:")
    next_event = scheduler.get_next_event(1300)
    if next_event:
        print(f"  {next_event[0]}: {next_event[1]}")
    
    # 取消事件
    scheduler.cancel(1500)
    print(f"\n取消 1500 午休后的事件:")
    for timestamp, events in scheduler.show_all():
        print(f"  {timestamp}: {events}")
    print()


def example_database_index():
    """示例7: 数据库索引模拟"""
    print("=" * 50)
    print("示例7: 数据库索引模拟")
    print("=" * 50)
    
    class TableIndex:
        """使用红黑树实现的表索引"""
        
        def __init__(self, key_field: str):
            self._index = RedBlackTreeMap[int]()
            self._key_field = key_field
        
        def insert(self, record: dict):
            """插入记录"""
            key = record[self._key_field]
            record_id = id(record)
            if key in self._index:
                self._index[key].append(record)
            else:
                self._index[key] = [record]
        
        def find(self, key: int):
            """精确查找"""
            return self._index.get(key, [])
        
        def find_range(self, low: int, high: int):
            """范围查找"""
            result = []
            for key, records in self._index.range_query(low, high):
                for record in records:
                    result.append(record)
            return result
        
        def find_less_than(self, key: int):
            """查找小于指定键的记录"""
            if self._index.is_empty:
                return []
            min_key = self._index.first_key()
            return self.find_range(min_key, key - 1)
        
        def find_greater_than(self, key: int):
            """查找大于指定键的记录"""
            if self._index.is_empty:
                return []
            max_key = self._index.last_key()
            return self.find_range(key + 1, max_key)
        
        def stats(self):
            """索引统计"""
            if self._index.is_empty:
                return {"records": 0, "unique_keys": 0}
            records = sum(len(v) for v in self._index.values())
            return {"records": records, "unique_keys": len(self._index)}
    
    # 创建用户表索引
    user_index = TableIndex("age")
    
    # 插入用户记录
    users = [
        {"id": 1, "name": "Alice", "age": 25},
        {"id": 2, "name": "Bob", "age": 30},
        {"id": 3, "name": "Charlie", "age": 25},
        {"id": 4, "name": "David", "age": 35},
        {"id": 5, "name": "Eve", "age": 28},
        {"id": 6, "name": "Frank", "age": 30},
    ]
    
    for user in users:
        user_index.insert(user)
    
    print("索引统计:", user_index.stats())
    
    print("\n查找年龄为 25 的用户:")
    for user in user_index.find(25):
        print(f"  {user['name']}: {user['age']}岁")
    
    print("\n查找年龄在 [28, 35] 范围的用户:")
    for user in user_index.find_range(28, 35):
        print(f"  {user['name']}: {user['age']}岁")
    print()


def example_performance_comparison():
    """示例8: 性能对比"""
    print("=" * 50)
    print("示例8: 性能对比（红黑树 vs 列表）")
    print("=" * 50)
    
    import bisect
    
    n = 10000
    
    # 准备数据
    data = list(range(n))
    random.shuffle(data)
    
    # 红黑树
    tree = RedBlackTree[int]()
    
    start = time.time()
    for key in data:
        tree.insert(key)
    tree_insert_time = time.time() - start
    
    start = time.time()
    for key in range(n):
        tree.search(key)
    tree_search_time = time.time() - start
    
    start = time.time()
    for key in range(n // 2):
        tree.delete(key)
    tree_delete_time = time.time() - start
    
    # 列表 + bisect
    lst = []
    
    start = time.time()
    for key in data:
        bisect.insort(lst, key)
    list_insert_time = time.time() - start
    
    start = time.time()
    for key in range(n):
        idx = bisect.bisect_left(lst, key)
        if idx < len(lst) and lst[idx] == key:
            pass  # 找到
    list_search_time = time.time() - start
    
    start = time.time()
    for key in range(n // 2):
        try:
            lst.remove(key)
        except ValueError:
            pass
    list_delete_time = time.time() - start
    
    print(f"操作次数: {n}")
    print(f"\n红黑树:")
    print(f"  插入: {tree_insert_time:.4f}s")
    print(f"  查找: {tree_search_time:.4f}s")
    print(f"  删除: {tree_delete_time:.4f}s")
    
    print(f"\n列表 + bisect:")
    print(f"  插入: {list_insert_time:.4f}s")
    print(f"  查找: {list_search_time:.4f}s")
    print(f"  删除: {list_delete_time:.4f}s")
    
    print(f"\n性能比（红黑树/列表）:")
    print(f"  插入: {tree_insert_time / list_insert_time:.2f}x")
    print(f"  查找: {tree_search_time / list_search_time:.2f}x")
    print(f"  删除: {tree_delete_time / list_delete_time:.2f}x")
    print()
    
    # 说明
    print("注：红黑树的时间复杂度为 O(log n)，而列表操作为 O(n)。")
    print("对于大规模数据，红黑树性能优势更明显。")


def main():
    """运行所有示例"""
    example_basic_operations()
    example_range_query()
    example_successor_predecessor()
    example_set_operations()
    example_map_operations()
    example_event_scheduler()
    example_database_index()
    example_performance_comparison()
    
    print("=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()