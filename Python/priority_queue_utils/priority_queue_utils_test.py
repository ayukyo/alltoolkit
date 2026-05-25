"""
优先队列工具测试模块

测试 PriorityQueue, ThreadSafePriorityQueue, BoundedPriorityQueue 的各项功能。
"""

import unittest
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

from mod import (
    PriorityQueue,
    ThreadSafePriorityQueue,
    BoundedPriorityQueue,
    QueueMode,
    create_min_heap,
    create_max_heap,
    merge_queues,
    from_list,
    top_k,
)


class TestPriorityQueue(unittest.TestCase):
    """测试 PriorityQueue 基础功能"""
    
    def test_basic_push_pop(self):
        """测试基本入队出队"""
        pq = create_min_heap()
        
        pq.push("task1", 3)
        pq.push("task2", 1)
        pq.push("task3", 2)
        
        self.assertEqual(len(pq), 3)
        
        result = pq.pop()
        self.assertEqual(result, ("task2", 1))
        
        result = pq.pop()
        self.assertEqual(result, ("task3", 2))
        
        result = pq.pop()
        self.assertEqual(result, ("task1", 3))
        
        self.assertEqual(len(pq), 0)
    
    def test_max_heap(self):
        """测试最大堆模式"""
        pq = create_max_heap()
        
        pq.push("a", 1)
        pq.push("b", 3)
        pq.push("c", 2)
        
        # 最大值先出队
        self.assertEqual(pq.pop(), ("b", 3))
        self.assertEqual(pq.pop(), ("c", 2))
        self.assertEqual(pq.pop(), ("a", 1))
    
    def test_peek(self):
        """测试查看队首"""
        pq = create_min_heap()
        
        pq.push("task", 5)
        
        # peek 不应改变队列
        result = pq.peek()
        self.assertEqual(result, ("task", 5))
        self.assertEqual(len(pq), 1)
        
        # 再次 peek
        result = pq.peek()
        self.assertEqual(result, ("task", 5))
    
    def test_empty_queue(self):
        """测试空队列"""
        pq = create_min_heap()
        
        self.assertEqual(len(pq), 0)
        self.assertFalse(pq)
        self.assertIsNone(pq.pop())
        self.assertIsNone(pq.peek())
    
    def test_stability(self):
        """测试相同优先级的 FIFO 稳定性"""
        pq = create_min_heap()
        
        pq.push("first", 1)
        pq.push("second", 1)
        pq.push("third", 1)
        
        self.assertEqual(pq.pop(), ("first", 1))
        self.assertEqual(pq.pop(), ("second", 1))
        self.assertEqual(pq.pop(), ("third", 1))
    
    def test_update_priority(self):
        """测试更新优先级"""
        pq = create_min_heap()
        
        seq = pq.push("task", 5)
        
        # 更新为更高优先级
        self.assertTrue(pq.update_priority(seq, 1))
        
        result = pq.peek()
        self.assertEqual(result, ("task", 1))
    
    def test_update_priority_by_value(self):
        """测试按值更新优先级"""
        pq = create_min_heap()
        
        pq.push("task1", 5)
        pq.push("task2", 5)
        
        # 更新所有 task1 的优先级
        count = pq.update_priority_by_value("task1", 1)
        self.assertEqual(count, 1)
        
        # task1 应该在队首
        result = pq.peek()
        self.assertEqual(result, ("task1", 1))
    
    def test_remove(self):
        """测试删除元素"""
        pq = create_min_heap()
        
        seq = pq.push("task", 5)
        
        self.assertTrue(pq.remove(seq))
        self.assertEqual(len(pq), 0)
        self.assertIsNone(pq.pop())
    
    def test_remove_by_value(self):
        """测试按值删除"""
        pq = create_min_heap()
        
        pq.push("task1", 1)
        pq.push("task2", 2)
        pq.push("task1", 3)
        
        count = pq.remove_by_value("task1")
        self.assertEqual(count, 2)
        
        # 只有 task2 应该剩余
        result = pq.pop()
        self.assertEqual(result, ("task2", 2))
    
    def test_contains(self):
        """测试包含检查"""
        pq = create_min_heap()
        
        pq.push("task", 1)
        
        self.assertTrue(pq.contains("task"))
        self.assertFalse(pq.contains("not_exist"))
        
        # 使用 in 操作符
        self.assertIn("task", pq)
        self.assertNotIn("not_exist", pq)
    
    def test_get_priority(self):
        """测试获取优先级"""
        pq = create_min_heap()
        
        pq.push("task", 5)
        
        priorities = pq.get_priority("task")
        self.assertEqual(priorities, [5])
        
        priorities = pq.get_priority("not_exist")
        self.assertIsNone(priorities)
    
    def test_extend(self):
        """测试批量入队"""
        pq = create_min_heap()
        
        sequences = pq.extend([("a", 3), ("b", 1), ("c", 2)])
        
        self.assertEqual(len(sequences), 3)
        self.assertEqual(len(pq), 3)
        
        # 按优先级出队
        self.assertEqual(pq.pop(), ("b", 1))
        self.assertEqual(pq.pop(), ("c", 2))
        self.assertEqual(pq.pop(), ("a", 3))
    
    def test_drain(self):
        """测试批量出队"""
        pq = create_min_heap()
        
        pq.extend([("a", 3), ("b", 1), ("c", 2), ("d", 4)])
        
        # 出队前 2 个
        result = pq.drain(2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("b", 1))
        self.assertEqual(result[1], ("c", 2))
        
        # 出队剩余
        result = pq.drain()
        self.assertEqual(len(result), 2)
    
    def test_merge(self):
        """测试队列合并"""
        pq1 = create_min_heap()
        pq2 = create_min_heap()
        
        pq1.push("a", 1)
        pq1.push("c", 3)
        
        pq2.push("b", 2)
        pq2.push("d", 4)
        
        count = pq1.merge(pq2)
        self.assertEqual(count, 2)
        
        # 按优先级出队
        self.assertEqual(pq1.pop(), ("a", 1))
        self.assertEqual(pq1.pop(), ("b", 2))
        self.assertEqual(pq1.pop(), ("c", 3))
        self.assertEqual(pq1.pop(), ("d", 4))
    
    def test_clear(self):
        """测试清空队列"""
        pq = create_min_heap()
        
        pq.extend([("a", 1), ("b", 2), ("c", 3)])
        
        pq.clear()
        
        self.assertEqual(len(pq), 0)
        self.assertFalse(pq)
    
    def test_to_list(self):
        """测试转换为列表"""
        pq = create_min_heap()
        
        pq.extend([("c", 3), ("a", 1), ("b", 2)])
        
        result = pq.to_list()
        
        self.assertEqual(result, [("a", 1), ("b", 2), ("c", 3)])
    
    def test_copy(self):
        """测试复制队列"""
        pq = create_min_heap()
        pq.extend([("a", 1), ("b", 2)])
        
        pq_copy = pq.copy()
        
        # 修改原队列不应影响副本
        pq.pop()
        
        self.assertEqual(len(pq), 1)
        self.assertEqual(len(pq_copy), 2)
    
    def test_iteration(self):
        """测试迭代"""
        pq = create_min_heap()
        pq.extend([("c", 3), ("a", 1), ("b", 2)])
        
        result = list(pq)
        
        self.assertEqual(result, [("a", 1), ("b", 2), ("c", 3)])


class TestThreadSafePriorityQueue(unittest.TestCase):
    """测试线程安全优先队列"""
    
    def test_concurrent_push(self):
        """测试并发入队"""
        pq = ThreadSafePriorityQueue[str, int]()
        
        def push_items(start: int, count: int):
            for i in range(count):
                pq.push(f"task-{start + i}", start + i)
        
        threads = [
            threading.Thread(target=push_items, args=(i * 100, 100))
            for i in range(10)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(pq), 1000)
    
    def test_concurrent_push_pop(self):
        """测试并发入队出队"""
        pq = ThreadSafePriorityQueue[int, int]()
        results: List[int] = []
        lock = threading.Lock()
        
        def push_items():
            for i in range(100):
                pq.push(i, i)
        
        def pop_items():
            for _ in range(100):
                result = pq.pop()
                if result is not None:
                    with lock:
                        results.append(result[0])
        
        push_thread = threading.Thread(target=push_items)
        pop_thread = threading.Thread(target=pop_items)
        
        push_thread.start()
        pop_thread.start()
        
        push_thread.join()
        pop_thread.join()
        
        # 验证出队的元素是递增顺序
        self.assertEqual(sorted(results), results)
    
    def test_context_manager(self):
        """测试上下文管理器"""
        pq = ThreadSafePriorityQueue[str, int]()
        
        with pq:
            pq.push("task1", 1)
            pq.push("task2", 2)
            # 在上下文内，锁被持有
        
        self.assertEqual(len(pq), 2)


class TestBoundedPriorityQueue(unittest.TestCase):
    """测试有界优先队列"""
    
    def test_max_size(self):
        """测试最大容量"""
        pq = BoundedPriorityQueue[str, int](max_size=3)
        
        success, evicted = pq.push("a", 1)
        self.assertTrue(success)
        self.assertIsNone(evicted)
        
        success, evicted = pq.push("b", 2)
        self.assertTrue(success)
        self.assertIsNone(evicted)
        
        success, evicted = pq.push("c", 3)
        self.assertTrue(success)
        self.assertIsNone(evicted)
        
        # 队列已满
        self.assertTrue(pq.is_full)
        
        # 再添加一个，应该弹出优先级最低的
        success, evicted = pq.push("d", 0)
        self.assertTrue(success)
        self.assertEqual(evicted, ("a", 1))
    
    def test_evicted_tracking(self):
        """测试被弹出元素追踪"""
        pq = BoundedPriorityQueue[str, int](max_size=2)
        
        pq.push("a", 1)
        pq.push("b", 2)
        pq.push("c", 3)  # 弹出 a
        pq.push("d", 4)  # 弹出 b
        
        evicted = pq.get_evicted()
        self.assertEqual(len(evicted), 2)
        self.assertIn(("a", 1), evicted)
        self.assertIn(("b", 2), evicted)
        
        pq.clear_evicted()
        self.assertEqual(len(pq.get_evicted()), 0)
    
    def test_pop_from_bounded(self):
        """测试从有界队列出队"""
        pq = BoundedPriorityQueue[str, int](max_size=3)
        
        pq.push("a", 1)
        pq.push("b", 2)
        pq.push("c", 3)
        
        result = pq.pop()
        self.assertEqual(result, ("a", 1))
        
        self.assertEqual(len(pq), 2)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_min_heap(self):
        """测试创建最小堆"""
        pq = create_min_heap()
        
        pq.push("a", 3)
        pq.push("b", 1)
        pq.push("c", 2)
        
        self.assertEqual(pq.pop(), ("b", 1))
    
    def test_create_max_heap(self):
        """测试创建最大堆"""
        pq = create_max_heap()
        
        pq.push("a", 1)
        pq.push("b", 3)
        pq.push("c", 2)
        
        self.assertEqual(pq.pop(), ("b", 3))
    
    def test_merge_queues(self):
        """测试合并队列函数"""
        pq1 = create_min_heap()
        pq2 = create_min_heap()
        
        pq1.push("a", 1)
        pq2.push("b", 2)
        
        merged = merge_queues(pq1, pq2)
        
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged.pop(), ("a", 1))
        self.assertEqual(merged.pop(), ("b", 2))
    
    def test_from_list(self):
        """测试从列表创建队列"""
        items = [("a", 3), ("b", 1), ("c", 2)]
        
        pq = from_list(items)
        
        self.assertEqual(pq.pop(), ("b", 1))
        self.assertEqual(pq.pop(), ("c", 2))
        self.assertEqual(pq.pop(), ("a", 3))
    
    def test_top_k_smallest(self):
        """测试获取最小的 K 个元素"""
        items = [(f"item{i}", i) for i in range(100)]
        
        result = top_k(items, k=5)
        
        self.assertEqual(len(result), 5)
        # 应该是最小的 5 个
        for i, (value, priority) in enumerate(result):
            self.assertEqual(priority, i)
    
    def test_top_k_largest(self):
        """测试获取最大的 K 个元素"""
        items = [(f"item{i}", i) for i in range(100)]
        
        result = top_k(items, k=5, largest=True)
        
        self.assertEqual(len(result), 5)
        # 应该是最大的 5 个
        expected = [(f"item{99-i}", 99-i) for i in range(5)]
        # 注意：结果顺序可能不同，但应该包含相同的元素
        result_values = {v for v, p in result}
        expected_values = {v for v, p in expected}
        self.assertEqual(result_values, expected_values)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_negative_priority(self):
        """测试负优先级"""
        pq = create_min_heap()
        
        pq.push("a", -1)
        pq.push("b", 1)
        pq.push("c", 0)
        
        # -1 应该最先出队
        self.assertEqual(pq.pop(), ("a", -1))
        self.assertEqual(pq.pop(), ("c", 0))
        self.assertEqual(pq.pop(), ("b", 1))
    
    def test_float_priority(self):
        """测试浮点优先级"""
        pq = create_min_heap()
        
        pq.push("a", 1.5)
        pq.push("b", 0.5)
        pq.push("c", 1.0)
        
        self.assertEqual(pq.pop(), ("b", 0.5))
        self.assertEqual(pq.pop(), ("c", 1.0))
        self.assertEqual(pq.pop(), ("a", 1.5))
    
    def test_duplicate_values(self):
        """测试重复值"""
        pq = create_min_heap()
        
        pq.push("same", 1)
        pq.push("same", 2)
        pq.push("same", 3)
        
        self.assertEqual(len(pq), 3)
        
        # 所有三个都应该能出队
        self.assertEqual(pq.pop(), ("same", 1))
        self.assertEqual(pq.pop(), ("same", 2))
        self.assertEqual(pq.pop(), ("same", 3))
    
    def test_large_queue(self):
        """测试大队列"""
        pq = create_min_heap()
        
        # 入队 10000 个元素
        for i in range(10000):
            pq.push(f"item{i}", i)
        
        self.assertEqual(len(pq), 10000)
        
        # 出队应该按顺序
        for i in range(10000):
            result = pq.pop()
            self.assertEqual(result, (f"item{i}", i))
        
        self.assertEqual(len(pq), 0)
    
    def test_none_value(self):
        """测试 None 值"""
        pq = create_min_heap()
        
        pq.push(None, 1)
        pq.push("not_none", 2)
        
        self.assertEqual(pq.pop(), (None, 1))
        self.assertEqual(pq.pop(), ("not_none", 2))
    
    def test_string_priority(self):
        """测试字符串优先级（字典序）"""
        pq = PriorityQueue[str, str](mode=QueueMode.MIN_HEAP)
        
        pq.push("task1", "c")
        pq.push("task2", "a")
        pq.push("task3", "b")
        
        # 按字典序
        self.assertEqual(pq.pop(), ("task2", "a"))
        self.assertEqual(pq.pop(), ("task3", "b"))
        self.assertEqual(pq.pop(), ("task1", "c"))


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_push_performance(self):
        """测试入队性能"""
        pq = create_min_heap()
        
        start = time.time()
        for i in range(10000):
            pq.push(f"item{i}", i)
        elapsed = time.time() - start
        
        # 10000 次入队应该在 1 秒内完成
        self.assertLess(elapsed, 1.0, "Push performance too slow")
    
    def test_pop_performance(self):
        """测试出队性能"""
        pq = create_min_heap()
        
        for i in range(10000):
            pq.push(f"item{i}", i)
        
        start = time.time()
        for i in range(10000):
            pq.pop()
        elapsed = time.time() - start
        
        # 10000 次出队应该在 1 秒内完成
        self.assertLess(elapsed, 1.0, "Pop performance too slow")
    
    def test_mixed_operations(self):
        """测试混合操作性能"""
        pq = create_min_heap()
        
        start = time.time()
        for i in range(5000):
            pq.push(f"item{i}", i)
            if i % 3 == 0:
                pq.pop()
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 1.0, "Mixed operations too slow")


if __name__ == "__main__":
    unittest.main(verbosity=2)