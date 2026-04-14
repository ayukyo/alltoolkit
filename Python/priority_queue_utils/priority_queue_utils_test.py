"""
优先队列工具模块测试

包含完整的单元测试，验证所有功能：
- PriorityQueue 基本操作
- 最大堆/最小堆模式
- UpdatablePriorityQueue 高效更新
- ThreadSafePriorityQueue 线程安全
- BoundedPriorityQueue 有界队列
- 合并有序列表
- TaskScheduler 任务调度
- top_k 函数

运行方式：
    python priority_queue_utils_test.py
"""

import unittest
import threading
import time
from typing import List, Tuple
from mod import (
    PriorityQueue,
    UpdatablePriorityQueue,
    ThreadSafePriorityQueue,
    BoundedPriorityQueue,
    TaskScheduler,
    PriorityItem,
    merge_sorted_lists,
    top_k,
    create_min_heap,
    create_max_heap,
)


class TestPriorityItem(unittest.TestCase):
    """测试 PriorityItem 类"""
    
    def test_priority_comparison(self):
        """测试优先级比较"""
        item1 = PriorityItem(priority=1, item="a", sequence=0)
        item2 = PriorityItem(priority=2, item="b", sequence=1)
        
        self.assertTrue(item1 < item2)
        self.assertFalse(item2 < item1)
    
    def test_sequence_comparison(self):
        """测试序列号比较（相同优先级时）"""
        item1 = PriorityItem(priority=1, item="a", sequence=0)
        item2 = PriorityItem(priority=1, item="b", sequence=1)
        
        self.assertTrue(item1 < item2)
    
    def test_equality(self):
        """测试相等比较"""
        item1 = PriorityItem(priority=1, item="a", sequence=0)
        item2 = PriorityItem(priority=1, item="a", sequence=1)
        
        self.assertTrue(item1 == item2)


class TestPriorityQueue(unittest.TestCase):
    """测试 PriorityQueue 类"""
    
    def test_basic_push_pop(self):
        """测试基本推入和弹出"""
        pq = PriorityQueue[int]()
        pq.push(5, 5)
        pq.push(1, 1)
        pq.push(3, 3)
        
        self.assertEqual(pq.pop(), 1)
        self.assertEqual(pq.pop(), 3)
        self.assertEqual(pq.pop(), 5)
        self.assertIsNone(pq.pop())
    
    def test_max_heap(self):
        """测试最大堆模式"""
        pq = PriorityQueue[int](max_heap=True)
        pq.push(1, 1)
        pq.push(5, 5)
        pq.push(3, 3)
        
        self.assertEqual(pq.pop(), 5)
        self.assertEqual(pq.pop(), 3)
        self.assertEqual(pq.pop(), 1)
    
    def test_peek(self):
        """测试查看堆顶"""
        pq = PriorityQueue[str]()
        pq.push("a", 2)
        pq.push("b", 1)
        
        self.assertEqual(pq.peek(), "b")
        self.assertEqual(len(pq), 2)
    
    def test_peek_priority(self):
        """测试查看堆顶优先级"""
        pq = PriorityQueue[int]()
        pq.push(10, 5.5)
        
        self.assertEqual(pq.peek_priority(), 5.5)
    
    def test_empty_operations(self):
        """测试空队列操作"""
        pq = PriorityQueue[int]()
        
        self.assertIsNone(pq.pop())
        self.assertIsNone(pq.peek())
        self.assertIsNone(pq.peek_priority())
    
    def test_len_and_bool(self):
        """测试长度和布尔值"""
        pq = PriorityQueue[int]()
        
        self.assertEqual(len(pq), 0)
        self.assertFalse(pq)
        
        pq.push(1, 1)
        self.assertEqual(len(pq), 1)
        self.assertTrue(pq)
    
    def test_contains(self):
        """测试包含检查"""
        pq = PriorityQueue[str]()
        pq.push("hello", 1)
        pq.push("world", 2)
        
        self.assertTrue("hello" in pq)
        self.assertTrue("world" in pq)
        self.assertFalse("foo" in pq)
    
    def test_update_priority(self):
        """测试更新优先级"""
        pq = PriorityQueue[str]()
        pq.push("a", 1)
        pq.push("b", 2)
        
        # 更新 b 的优先级为 0，使其成为最高优先级
        result = pq.update_priority("b", 0)
        self.assertTrue(result)
        self.assertEqual(pq.pop(), "b")
    
    def test_remove(self):
        """测试移除元素"""
        pq = PriorityQueue[int]()
        pq.push(1, 1)
        pq.push(2, 2)
        pq.push(3, 3)
        
        self.assertTrue(pq.remove(2))
        self.assertEqual(len(pq), 2)
        self.assertFalse(2 in pq)
        
        self.assertFalse(pq.remove(100))  # 不存在的元素
    
    def test_merge(self):
        """测试队列合并"""
        pq1 = PriorityQueue[int]()
        pq1.push(1, 1)
        pq1.push(3, 3)
        
        pq2 = PriorityQueue[int]()
        pq2.push(2, 2)
        pq2.push(4, 4)
        
        pq1.merge(pq2)
        
        self.assertEqual(len(pq1), 4)
        # 按优先级弹出
        self.assertEqual(pq1.pop(), 1)
        self.assertEqual(pq1.pop(), 2)
        self.assertEqual(pq1.pop(), 3)
        self.assertEqual(pq1.pop(), 4)
    
    def test_clear(self):
        """测试清空队列"""
        pq = PriorityQueue[int]()
        pq.push(1, 1)
        pq.push(2, 2)
        pq.clear()
        
        self.assertEqual(len(pq), 0)
        self.assertFalse(pq)
    
    def test_to_list(self):
        """测试转换为列表"""
        pq = PriorityQueue[str]()
        pq.push("b", 2)
        pq.push("a", 1)
        pq.push("c", 3)
        
        sorted_list = pq.to_list(sorted_=True)
        self.assertEqual(sorted_list, [("a", 1), ("b", 2), ("c", 3)])
        
        unsorted_list = pq.to_list(sorted_=False)
        self.assertEqual(len(unsorted_list), 3)
    
    def test_from_list(self):
        """测试从列表创建"""
        items = [("a", 2), ("b", 1), ("c", 3)]
        pq = PriorityQueue.from_list(items)
        
        self.assertEqual(pq.pop(), "b")
        self.assertEqual(pq.pop(), "a")
        self.assertEqual(pq.pop(), "c")
    
    def test_stable_sort(self):
        """测试稳定排序（相同优先级时保持插入顺序）"""
        pq = PriorityQueue[str]()
        pq.push("first", 1)
        pq.push("second", 1)
        pq.push("third", 1)
        
        self.assertEqual(pq.pop(), "first")
        self.assertEqual(pq.pop(), "second")
        self.assertEqual(pq.pop(), "third")


class TestUpdatablePriorityQueue(unittest.TestCase):
    """测试 UpdatablePriorityQueue 类"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        pq = UpdatablePriorityQueue[int]()
        pq.push(1, 3)
        pq.push(2, 1)
        pq.push(3, 2)
        
        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 3)
        self.assertEqual(pq.pop(), 1)
    
    def test_update_priority_efficient(self):
        """测试高效更新优先级"""
        pq = UpdatablePriorityQueue[str]()
        pq.push("a", 1)
        pq.push("b", 2)
        pq.push("c", 3)
        
        # 更新 c 的优先级为 0
        result = pq.update_priority("c", 0)
        self.assertTrue(result)
        self.assertEqual(pq.pop(), "c")
    
    def test_push_existing_updates(self):
        """测试推入已存在元素时更新优先级"""
        pq = UpdatablePriorityQueue[str]()
        pq.push("item", 5)
        pq.push("item", 1)  # 更新优先级
        
        self.assertEqual(len(pq), 1)
        self.assertEqual(pq.pop(), "item")
    
    def test_contains_and_get_priority(self):
        """测试包含检查和获取优先级"""
        pq = UpdatablePriorityQueue[str]()
        pq.push("hello", 3.5)
        
        self.assertTrue(pq.contains("hello"))
        self.assertFalse(pq.contains("world"))
        self.assertEqual(pq.get_priority("hello"), 3.5)
        self.assertIsNone(pq.get_priority("world"))
    
    def test_remove(self):
        """测试移除元素"""
        pq = UpdatablePriorityQueue[int]()
        pq.push(1, 1)
        pq.push(2, 2)
        
        self.assertTrue(pq.remove(1))
        self.assertEqual(len(pq), 1)
        self.assertFalse(pq.contains(1))
    
    def test_max_heap_mode(self):
        """测试最大堆模式"""
        pq = UpdatablePriorityQueue[int](max_heap=True)
        pq.push(1, 1)
        pq.push(5, 5)
        pq.push(3, 3)
        
        self.assertEqual(pq.pop(), 5)
        self.assertEqual(pq.pop(), 3)
        self.assertEqual(pq.pop(), 1)


class TestThreadSafePriorityQueue(unittest.TestCase):
    """测试 ThreadSafePriorityQueue 类"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        pq = ThreadSafePriorityQueue[int]()
        pq.push(1, 1)
        pq.push(2, 2)
        
        self.assertEqual(pq.pop(), 1)
        self.assertEqual(pq.pop(), 2)
    
    def test_concurrent_push_pop(self):
        """测试并发推入和弹出"""
        pq = ThreadSafePriorityQueue[int]()
        results = []
        errors = []
        
        def producer(start: int, count: int):
            try:
                for i in range(count):
                    pq.push(start + i, start + i)
            except Exception as e:
                errors.append(e)
        
        def consumer(count: int):
            try:
                for _ in range(count):
                    item = pq.try_pop()
                    if item is not None:
                        results.append(item)
            except Exception as e:
                errors.append(e)
        
        # 启动生产者和消费者线程
        threads = []
        for i in range(3):
            threads.append(threading.Thread(target=producer, args=(i * 100, 50)))
        for i in range(2):
            threads.append(threading.Thread(target=consumer, args=(75,)))
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 验证没有错误
        self.assertEqual(len(errors), 0)
        
        # 验证所有元素都被消费
        remaining = pq.try_pop()
        while remaining is not None:
            results.append(remaining)
            remaining = pq.try_pop()
        
        self.assertEqual(len(results), 150)  # 3 * 50
    
    def test_pop_timeout(self):
        """测试弹出超时"""
        pq = ThreadSafePriorityQueue[int]()
        
        start_time = time.time()
        result = pq.pop(timeout=0.1)
        elapsed = time.time() - start_time
        
        self.assertIsNone(result)
        self.assertGreaterEqual(elapsed, 0.1)


class TestBoundedPriorityQueue(unittest.TestCase):
    """测试 BoundedPriorityQueue 类"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        pq = BoundedPriorityQueue[int](max_size=3)
        
        self.assertTrue(pq.push(1, 1))
        self.assertTrue(pq.push(2, 2))
        self.assertTrue(pq.push(3, 3))
        self.assertEqual(len(pq), 3)
    
    def test_max_size_limit(self):
        """测试最大容量限制"""
        pq = BoundedPriorityQueue[int](max_size=2)
        
        self.assertTrue(pq.push(1, 1))
        self.assertTrue(pq.push(2, 2))
        self.assertTrue(pq.is_full())
        
        # 低优先级元素应该被拒绝
        self.assertFalse(pq.push(0, 3))  # 优先级 3 比队列中的都低
    
    def test_replacement_on_higher_priority(self):
        """测试高优先级元素替换"""
        pq = BoundedPriorityQueue[int](max_size=2)
        pq.push(1, 1)
        pq.push(2, 2)
        
        # 高优先级元素应该替换低优先级元素
        self.assertTrue(pq.push(0, 0))
        
        # 验证低优先级元素被移除
        items = []
        while pq:
            item = pq.pop()
            if item is not None:
                items.append(item)
        
        self.assertNotIn(2, items)  # 优先级为 2 的应该被移除
        self.assertIn(0, items)
        self.assertIn(1, items)
    
    def test_max_heap_mode(self):
        """测试最大堆模式"""
        pq = BoundedPriorityQueue[int](max_size=2, max_heap=True)
        
        pq.push(1, 1)
        pq.push(2, 2)
        
        # 在最大堆模式，优先级高的先出
        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 1)
    
    def test_invalid_max_size(self):
        """测试无效的最大容量"""
        with self.assertRaises(ValueError):
            BoundedPriorityQueue[int](max_size=0)
        
        with self.assertRaises(ValueError):
            BoundedPriorityQueue[int](max_size=-1)


class TestMergeSortedLists(unittest.TestCase):
    """测试 merge_sorted_lists 函数"""
    
    def test_merge_two_lists(self):
        """测试合并两个列表"""
        list1 = [("a", 1), ("c", 3)]
        list2 = [("b", 2), ("d", 4)]
        
        result = merge_sorted_lists([list1, list2])
        
        self.assertEqual(result, [("a", 1), ("b", 2), ("c", 3), ("d", 4)])
    
    def test_merge_multiple_lists(self):
        """测试合并多个列表"""
        list1 = [("a", 1)]
        list2 = [("b", 2)]
        list3 = [("c", 0)]
        
        result = merge_sorted_lists([list1, list2, list3])
        
        self.assertEqual(result, [("c", 0), ("a", 1), ("b", 2)])
    
    def test_empty_lists(self):
        """测试空列表"""
        self.assertEqual(merge_sorted_lists([]), [])
        self.assertEqual(merge_sorted_lists([[], []]), [])
    
    def test_single_list(self):
        """测试单个列表"""
        lst = [("a", 1), ("b", 2)]
        result = merge_sorted_lists([lst])
        self.assertEqual(result, [("a", 1), ("b", 2)])


class TestTaskScheduler(unittest.TestCase):
    """测试 TaskScheduler 类"""
    
    def test_basic_scheduling(self):
        """测试基本调度"""
        scheduler = TaskScheduler()
        scheduler.add_task("low", 3)
        scheduler.add_task("high", 1)
        scheduler.add_task("medium", 2)
        
        self.assertEqual(scheduler.get_next_task(), "high")
        self.assertEqual(scheduler.get_next_task(), "medium")
        self.assertEqual(scheduler.get_next_task(), "low")
    
    def test_task_with_data(self):
        """测试带数据的任务"""
        scheduler = TaskScheduler()
        scheduler.add_task("task1", 1, data={"type": "urgent"})
        scheduler.add_task("task2", 2, data={"type": "normal"})
        
        self.assertEqual(scheduler.get_task_data("task1"), {"type": "urgent"})
        self.assertEqual(scheduler.get_task_data("task2"), {"type": "normal"})
    
    def test_update_priority(self):
        """测试更新任务优先级"""
        scheduler = TaskScheduler()
        scheduler.add_task("task", 5)
        
        scheduler.update_task_priority("task", 1)
        
        self.assertEqual(scheduler.peek_next_task(), "task")
    
    def test_cancel_task(self):
        """测试取消任务"""
        scheduler = TaskScheduler()
        scheduler.add_task("task1", 1)
        scheduler.add_task("task2", 2)
        
        scheduler.cancel_task("task1")
        
        self.assertFalse(scheduler.has_task("task1"))
        self.assertEqual(len(scheduler), 1)
    
    def test_clear(self):
        """测试清空调度器"""
        scheduler = TaskScheduler()
        scheduler.add_task("task1", 1)
        scheduler.add_task("task2", 2)
        
        scheduler.clear()
        
        self.assertEqual(len(scheduler), 0)
        self.assertFalse(scheduler)
    
    def test_max_heap_mode(self):
        """测试最大堆模式"""
        scheduler = TaskScheduler(max_heap=True)
        scheduler.add_task("low", 1)
        scheduler.add_task("high", 5)
        scheduler.add_task("medium", 3)
        
        # 最大堆模式，优先级高的先出
        self.assertEqual(scheduler.get_next_task(), "high")


class TestTopK(unittest.TestCase):
    """测试 top_k 函数"""
    
    def test_top_k_largest(self):
        """测试最大的 K 个元素"""
        items = [("a", 1), ("b", 5), ("c", 3), ("d", 2), ("e", 4)]
        result = top_k(items, 3, largest=True)
        
        # 应该返回优先级最大的 3 个
        priorities = [p for _, p in result]
        self.assertEqual(sorted(priorities, reverse=True), [5, 4, 3])
    
    def test_top_k_smallest(self):
        """测试最小的 K 个元素"""
        items = [("a", 1), ("b", 5), ("c", 3), ("d", 2), ("e", 4)]
        result = top_k(items, 3, largest=False)
        
        # 应该返回优先级最小的 3 个
        priorities = [p for _, p in result]
        self.assertEqual(sorted(priorities), [1, 2, 3])
    
    def test_top_k_empty(self):
        """测试空列表"""
        result = top_k([], 3)
        self.assertEqual(result, [])
    
    def test_top_k_zero(self):
        """测试 K=0"""
        items = [("a", 1), ("b", 2)]
        result = top_k(items, 0)
        self.assertEqual(result, [])
    
    def test_top_k_larger_than_size(self):
        """测试 K 大于列表大小"""
        items = [("a", 1), ("b", 2)]
        result = top_k(items, 10)
        
        self.assertEqual(len(result), 2)


class TestFactoryFunctions(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_min_heap(self):
        """测试创建最小堆"""
        pq = create_min_heap()
        pq.push(3, 3)
        pq.push(1, 1)
        pq.push(2, 2)
        
        self.assertEqual(pq.pop(), 1)
        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 3)
    
    def test_create_max_heap(self):
        """测试创建最大堆"""
        pq = create_max_heap()
        pq.push(1, 1)
        pq.push(3, 3)
        pq.push(2, 2)
        
        self.assertEqual(pq.pop(), 3)
        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)