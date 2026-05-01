"""
Circular Queue Utils 测试套件

全面测试循环队列模块的所有功能。
"""

import pytest
import threading
import time
from typing import List

# 添加父目录到路径
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circular_queue_utils.mod import (
    CircularQueue,
    create_queue,
    sliding_window,
    recent_buffer
)


class TestCircularQueueBasic:
    """基本功能测试"""
    
    def test_create_queue(self):
        """测试队列创建"""
        queue = CircularQueue[int](capacity=5)
        assert queue.capacity == 5
        assert queue.size == 0
        assert queue.is_empty
        assert not queue.is_full
        assert len(queue) == 0
    
    def test_create_queue_invalid_capacity(self):
        """测试无效容量"""
        with pytest.raises(ValueError):
            CircularQueue[int](capacity=0)
        
        with pytest.raises(ValueError):
            CircularQueue[int](capacity=-1)
    
    def test_enqueue_dequeue(self):
        """测试入队和出队"""
        queue = CircularQueue[int](capacity=3)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        assert len(queue) == 3
        assert queue.is_full
        
        assert queue.dequeue() == 1
        assert queue.dequeue() == 2
        assert queue.dequeue() == 3
        
        assert queue.is_empty
    
    def test_enqueue_multiple(self):
        """测试批量入队"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3, 4, 5)
        
        assert len(queue) == 5
        assert queue.to_list() == [1, 2, 3, 4, 5]
    
    def test_fifo_order(self):
        """测试先进先出顺序"""
        queue = CircularQueue[str](capacity=10)
        items = ["first", "second", "third", "fourth", "fifth"]
        
        for item in items:
            queue.enqueue(item)
        
        for item in items:
            assert queue.dequeue() == item
    
    def test_overflow_error(self):
        """测试溢出错误"""
        queue = CircularQueue[int](capacity=2)
        queue.enqueue(1, 2)
        
        with pytest.raises(OverflowError):
            queue.enqueue(3)
    
    def test_underflow_error(self):
        """测试下溢错误"""
        queue = CircularQueue[int](capacity=5)
        
        with pytest.raises(IndexError):
            queue.dequeue()
    
    def test_peek(self):
        """测试查看队首"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(10, 20, 30)
        
        assert queue.peek() == 10
        assert queue.peek(0) == 10
        assert queue.peek(1) == 20
        assert queue.peek(2) == 30
        assert len(queue) == 3  # peek 不移除元素
    
    def test_peek_last(self):
        """测试查看队尾"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3)
        
        assert queue.peek_last() == 3
    
    def test_peek_empty_queue(self):
        """测试空队列 peek"""
        queue = CircularQueue[int](capacity=5)
        
        with pytest.raises(IndexError):
            queue.peek()
        
        with pytest.raises(IndexError):
            queue.peek_last()
    
    def test_peek_offset_out_of_range(self):
        """测试 peek 偏移越界"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2)
        
        with pytest.raises(IndexError):
            queue.peek(5)


class TestCircularQueueOverwrite:
    """自动覆盖模式测试"""
    
    def test_overwrite_mode(self):
        """测试自动覆盖模式"""
        queue = CircularQueue[int](capacity=3, overwrite=True)
        
        queue.enqueue(1, 2, 3)
        assert queue.to_list() == [1, 2, 3]
        
        queue.enqueue(4)
        assert queue.to_list() == [2, 3, 4]
        
        queue.enqueue(5, 6)
        assert queue.to_list() == [4, 5, 6]
    
    def test_overwrite_statistics(self):
        """测试覆盖统计"""
        queue = CircularQueue[int](capacity=2, overwrite=True)
        
        queue.enqueue(1, 2)
        queue.enqueue(3)
        queue.enqueue(4, 5)
        
        stats = queue.stats
        assert stats['total_enqueued'] == 5
        assert stats['total_overwritten'] == 3


class TestCircularQueueIteration:
    """迭代测试"""
    
    def test_iterator(self):
        """测试迭代器"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3, 4, 5)
        
        result = list(queue)
        assert result == [1, 2, 3, 4, 5]
    
    def test_reversed_iterator(self):
        """测试反向迭代器"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3, 4, 5)
        
        result = list(reversed(queue))
        assert result == [5, 4, 3, 2, 1]
    
    def test_iteration_after_wrap_around(self):
        """测试环绕后的迭代"""
        queue = CircularQueue[int](capacity=3)
        
        # 填满队列
        queue.enqueue(1, 2, 3)
        # 出队一些
        queue.dequeue()
        queue.dequeue()
        # 再入队
        queue.enqueue(4, 5)
        
        result = list(queue)
        assert result == [3, 4, 5]


class TestCircularQueueIndexing:
    """索引和切片测试"""
    
    def test_positive_index(self):
        """测试正索引"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(10, 20, 30, 40, 50)
        
        assert queue[0] == 10
        assert queue[2] == 30
        assert queue[4] == 50
    
    def test_negative_index(self):
        """测试负索引"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(10, 20, 30, 40, 50)
        
        assert queue[-1] == 50
        assert queue[-2] == 40
        assert queue[-5] == 10
    
    def test_slice(self):
        """测试切片"""
        queue = CircularQueue[int](capacity=10)
        queue.enqueue(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        
        assert queue[0:3] == [0, 1, 2]
        assert queue[2:5] == [2, 3, 4]
        assert queue[::2] == [0, 2, 4, 6, 8]
        assert queue[::-1] == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    
    def test_contains(self):
        """测试包含检查"""
        queue = CircularQueue[str](capacity=5)
        queue.enqueue("a", "b", "c")
        
        assert "a" in queue
        assert "b" in queue
        assert "c" in queue
        assert "d" not in queue


class TestCircularQueueOperations:
    """操作方法测试"""
    
    def test_clear(self):
        """测试清空队列"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3, 4, 5)
        
        result = queue.clear()
        
        assert queue.is_empty
        assert len(queue) == 0
        assert result is queue  # 返回 self
    
    def test_to_list(self):
        """测试转换为列表"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3)
        
        result = queue.to_list()
        assert result == [1, 2, 3]
        
        # 确保是副本而非引用
        result.append(4)
        assert len(queue) == 3
    
    def test_copy(self):
        """测试拷贝"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3)
        
        new_queue = queue.copy()
        
        assert new_queue.to_list() == queue.to_list()
        assert new_queue.capacity == queue.capacity
        
        # 确保是独立副本
        new_queue.enqueue(4)
        assert len(queue) == 3
        assert len(new_queue) == 4
    
    def test_extend(self):
        """测试扩展"""
        queue = CircularQueue[int](capacity=10)
        queue.enqueue(1, 2)
        queue.extend([3, 4, 5])
        
        assert queue.to_list() == [1, 2, 3, 4, 5]
    
    def test_count(self):
        """测试计数"""
        queue = CircularQueue[int](capacity=10)
        queue.enqueue(1, 2, 3, 2, 2, 4)
        
        assert queue.count(1) == 1
        assert queue.count(2) == 3
        assert queue.count(5) == 0
    
    def test_index(self):
        """测试查找索引"""
        queue = CircularQueue[str](capacity=10)
        queue.enqueue("a", "b", "c", "b", "d")
        
        assert queue.index("a") == 0
        assert queue.index("b") == 1  # 第一个
        assert queue.index("c") == 2
        assert queue.index("b", 2) == 3  # 从位置 2 开始
        
        with pytest.raises(ValueError):
            queue.index("z")
    
    def test_find(self):
        """测试条件查找"""
        queue = CircularQueue[int](capacity=10)
        queue.enqueue(1, 2, 3, 4, 5)
        
        result = queue.find(lambda x: x > 3)
        assert result == 4
        
        result = queue.find(lambda x: x > 10)
        assert result is None
    
    def test_find_all(self):
        """测试条件查找所有"""
        queue = CircularQueue[int](capacity=10)
        queue.enqueue(1, 2, 3, 4, 5, 6)
        
        result = queue.find_all(lambda x: x % 2 == 0)
        assert result == [2, 4, 6]
    
    def test_map(self):
        """测试映射"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3)
        
        result = queue.map(lambda x: x * 2)
        assert result == [2, 4, 6]
    
    def test_filter(self):
        """测试过滤"""
        queue = CircularQueue[int](capacity=10)
        queue.enqueue(1, 2, 3, 4, 5, 6)
        
        result = queue.filter(lambda x: x % 2 == 0)
        assert result == [2, 4, 6]
    
    def test_reduce(self):
        """测试归约"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3, 4, 5)
        
        result = queue.reduce(lambda acc, x: acc + x, 0)
        assert result == 15
        
        result = queue.reduce(lambda acc, x: acc * x, 1)
        assert result == 120


class TestCircularQueueChaining:
    """链式调用测试"""
    
    def test_method_chaining(self):
        """测试方法链式调用"""
        queue = CircularQueue[int](capacity=10)
        
        result = (
            queue
            .enqueue(1, 2, 3)
            .enqueue(4)
            .extend([5, 6])
        )
        
        assert result is queue
        assert queue.to_list() == [1, 2, 3, 4, 5, 6]


class TestCircularQueueThreadSafe:
    """线程安全测试"""
    
    def test_thread_safe_creation(self):
        """测试线程安全队列创建"""
        queue = CircularQueue[int](capacity=10, thread_safe=True)
        assert queue.thread_safe
    
    def test_concurrent_enqueue_dequeue(self):
        """测试并发入队出队"""
        queue = CircularQueue[int](capacity=100, thread_safe=True)
        errors: List[Exception] = []
        
        def producer(start: int, count: int):
            try:
                for i in range(start, start + count):
                    queue.enqueue(i)
            except Exception as e:
                errors.append(e)
        
        def consumer(count: int, results: List[int]):
            try:
                for _ in range(count):
                    item = queue.blocking_dequeue(timeout=5)
                    if item is not None:
                        results.append(item)
            except Exception as e:
                errors.append(e)
        
        # 启动生产者和消费者
        results: List[int] = []
        threads = [
            threading.Thread(target=producer, args=(0, 50)),
            threading.Thread(target=producer, args=(50, 50)),
            threading.Thread(target=consumer, args=(100, results)),
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join(timeout=10)
        
        assert len(errors) == 0
        assert len(results) == 100
    
    def test_blocking_enqueue_timeout(self):
        """测试阻塞入队超时"""
        queue = CircularQueue[int](capacity=2, thread_safe=True)
        queue.enqueue(1, 2)
        
        start = time.time()
        result = queue.blocking_enqueue(3, timeout=0.5)
        elapsed = time.time() - start
        
        assert result is False
        assert elapsed >= 0.4
    
    def test_blocking_dequeue_timeout(self):
        """测试阻塞出队超时"""
        queue = CircularQueue[int](capacity=5, thread_safe=True)
        
        start = time.time()
        result = queue.blocking_dequeue(timeout=0.5)
        elapsed = time.time() - start
        
        assert result is None
        assert elapsed >= 0.4
    
    def test_blocking_without_thread_safe(self):
        """测试非线程安全模式的阻塞操作"""
        queue = CircularQueue[int](capacity=5, thread_safe=False)
        
        with pytest.raises(RuntimeError):
            queue.blocking_enqueue(1)
        
        with pytest.raises(RuntimeError):
            queue.blocking_dequeue()


class TestCircularQueueStatistics:
    """统计信息测试"""
    
    def test_stats(self):
        """测试统计信息"""
        queue = CircularQueue[int](capacity=5)
        
        stats = queue.stats
        assert stats['capacity'] == 5
        assert stats['size'] == 0
        assert stats['is_empty'] is True
        assert stats['is_full'] is False
        assert stats['utilization'] == 0
        
        queue.enqueue(1, 2, 3)
        stats = queue.stats
        assert stats['size'] == 3
        assert stats['total_enqueued'] == 3
        assert stats['utilization'] == 0.6
    
    def test_operations_tracking(self):
        """测试操作跟踪"""
        queue = CircularQueue[int](capacity=3, overwrite=True)
        
        queue.enqueue(1, 2, 3)
        queue.dequeue()
        queue.enqueue(4, 5, 6)
        
        stats = queue.stats
        assert stats['total_enqueued'] == 6
        assert stats['total_dequeued'] == 1
        # enqueue(4, 5, 6) in overwrite mode:
        # - enqueue(4): queue was [2, 3], becomes [2, 3, 4] (no overwrite)
        # - enqueue(5): queue was [2, 3, 4], overwrites 2, becomes [3, 4, 5]
        # - enqueue(6): queue was [3, 4, 5], overwrites 3, becomes [4, 5, 6]
        assert stats['total_overwritten'] == 2


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_create_queue(self):
        """测试创建队列便捷函数"""
        queue = create_queue(5, [1, 2, 3])
        
        assert len(queue) == 3
        assert queue.capacity == 5
    
    def test_sliding_window(self):
        """测试滑动窗口"""
        data = [1, 2, 3, 4, 5]
        windows = list(sliding_window(data, 3))
        
        assert windows == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    
    def test_sliding_window_string(self):
        """测试字符串滑动窗口"""
        data = "abcdef"
        windows = list(sliding_window(data, 2))
        
        assert windows == [['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'e'], ['e', 'f']]
    
    def test_sliding_window_empty(self):
        """测试空数据滑动窗口"""
        windows = list(sliding_window([], 3))
        assert windows == []
    
    def test_sliding_window_data_smaller_than_window(self):
        """测试数据小于窗口"""
        windows = list(sliding_window([1, 2], 5))
        assert windows == []
    
    def test_sliding_window_invalid_size(self):
        """测试无效窗口大小"""
        with pytest.raises(ValueError):
            list(sliding_window([1, 2, 3], 0))
        
        with pytest.raises(ValueError):
            list(sliding_window([1, 2, 3], -1))
    
    def test_recent_buffer(self):
        """测试最近缓冲区"""
        buffer = recent_buffer(10)
        
        assert buffer.capacity == 10
        assert buffer.overwrite is True


class TestCircularQueueEdgeCases:
    """边界情况测试"""
    
    def test_single_capacity(self):
        """测试容量为 1 的队列"""
        queue = CircularQueue[int](capacity=1)
        
        queue.enqueue(42)
        assert queue.is_full
        assert queue.peek() == 42
        assert queue.dequeue() == 42
        assert queue.is_empty
    
    def test_large_capacity(self):
        """测试大容量队列"""
        capacity = 10000
        queue = CircularQueue[int](capacity=capacity)
        
        for i in range(capacity):
            queue.enqueue(i)
        
        assert queue.is_full
        assert queue[0] == 0
        assert queue[-1] == capacity - 1
    
    def test_different_types(self):
        """测试不同数据类型"""
        # 字符串
        str_queue = CircularQueue[str](capacity=3)
        str_queue.enqueue("a", "b", "c")
        assert str_queue.to_list() == ["a", "b", "c"]
        
        # 浮点数
        float_queue = CircularQueue[float](capacity=3)
        float_queue.enqueue(1.1, 2.2, 3.3)
        assert float_queue.to_list() == [1.1, 2.2, 3.3]
        
        # 自定义对象
        obj_queue = CircularQueue[dict](capacity=3)
        obj_queue.enqueue({"a": 1}, {"b": 2})
        assert obj_queue.to_list() == [{"a": 1}, {"b": 2}]
    
    def test_wrap_around_behavior(self):
        """测试环绕行为"""
        queue = CircularQueue[int](capacity=3)
        
        # 入队并部分出队
        queue.enqueue(1, 2, 3)
        queue.dequeue()  # 移除 1
        queue.dequeue()  # 移除 2
        
        # 继续入队，触发环绕
        queue.enqueue(4, 5)
        
        assert queue.to_list() == [3, 4, 5]
        assert queue.is_full
    
    def test_string_representation(self):
        """测试字符串表示"""
        queue = CircularQueue[int](capacity=5)
        queue.enqueue(1, 2, 3)
        
        assert "CircularQueue" in repr(queue)
        assert "capacity=5" in repr(queue)
        assert "size=3" in repr(queue)
        
        str_repr = str(queue)
        assert "1" in str_repr
        assert "2" in str_repr
        assert "3" in str_repr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])