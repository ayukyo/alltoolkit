"""
Ring Buffer Utils 测试套件

测试循环缓冲区的各项功能。
"""

import unittest
import threading
import time
from collections.abc import Sequence
from mod import (
    RingBuffer, NumericRingBuffer, EventBuffer,
    create_ring_buffer, create_numeric_buffer,
    sliding_window, batch_process
)


class TestRingBuffer(unittest.TestCase):
    """RingBuffer 基础测试"""
    
    def test_init(self):
        """测试初始化"""
        rb = RingBuffer[int](5)
        self.assertEqual(len(rb), 0)
        self.assertEqual(rb.capacity, 5)
        self.assertTrue(rb.is_empty)
        self.assertFalse(rb.is_full)
    
    def test_init_invalid_capacity(self):
        """测试无效容量"""
        with self.assertRaises(ValueError):
            RingBuffer[int](0)
        with self.assertRaises(ValueError):
            RingBuffer[int](-5)
    
    def test_append(self):
        """测试添加元素"""
        rb = RingBuffer[int](3)
        rb.append(1)
        rb.append(2)
        rb.append(3)
        
        self.assertEqual(len(rb), 3)
        self.assertTrue(rb.is_full)
        self.assertEqual(list(rb), [1, 2, 3])
    
    def test_overflow(self):
        """测试溢出覆盖"""
        rb = RingBuffer[int](3)
        rb.extend([1, 2, 3, 4, 5])  # 添加 5 个元素，容量只有 3
        
        self.assertEqual(len(rb), 3)
        self.assertEqual(list(rb), [3, 4, 5])  # 最新的 3 个
    
    def test_getitem(self):
        """测试索引访问"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3, 4, 5])
        
        self.assertEqual(rb[0], 1)
        self.assertEqual(rb[2], 3)
        self.assertEqual(rb[-1], 5)
        self.assertEqual(rb[-2], 4)
    
    def test_getitem_out_of_range(self):
        """测试索引越界"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        
        with self.assertRaises(IndexError):
            _ = rb[5]
        with self.assertRaises(IndexError):
            _ = rb[-5]
    
    def test_iteration(self):
        """测试迭代"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3, 4, 5])
        
        result = list(rb)
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_reversed(self):
        """测试反向迭代"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3, 4, 5])
        
        result = list(reversed(rb))
        self.assertEqual(result, [5, 4, 3, 2, 1])
    
    def test_contains(self):
        """测试包含检查"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3, 4, 5])
        
        self.assertIn(3, rb)
        self.assertNotIn(10, rb)
    
    def test_extend(self):
        """测试批量添加"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        
        self.assertEqual(len(rb), 3)
        self.assertEqual(list(rb), [1, 2, 3])
    
    def test_pop(self):
        """测试弹出最新元素"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        
        self.assertEqual(rb.pop(), 3)
        self.assertEqual(rb.pop(), 2)
        self.assertEqual(len(rb), 1)
    
    def test_popleft(self):
        """测试弹出最旧元素"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        
        self.assertEqual(rb.popleft(), 1)
        self.assertEqual(rb.popleft(), 2)
        self.assertEqual(len(rb), 1)
    
    def test_pop_empty(self):
        """测试空缓冲区弹出"""
        rb = RingBuffer[int](5)
        
        with self.assertRaises(IndexError):
            rb.pop()
        with self.assertRaises(IndexError):
            rb.popleft()
    
    def test_peek(self):
        """测试查看元素"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        
        self.assertEqual(rb.peek(), 3)  # 最新
        self.assertEqual(rb.peekleft(), 1)  # 最旧
        self.assertEqual(len(rb), 3)  # 不删除
    
    def test_clear(self):
        """测试清空"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        rb.clear()
        
        self.assertEqual(len(rb), 0)
        self.assertTrue(rb.is_empty)
    
    def test_rotate(self):
        """测试旋转"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3, 4, 5])
        
        rb.rotate(1)
        self.assertEqual(list(rb), [5, 1, 2, 3, 4])
        
        rb.rotate(-1)
        self.assertEqual(list(rb), [1, 2, 3, 4, 5])
    
    def test_copy(self):
        """测试复制"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        
        rb2 = rb.copy()
        self.assertEqual(list(rb2), [1, 2, 3])
        
        rb2.append(4)
        self.assertEqual(len(rb), 3)
        self.assertEqual(len(rb2), 4)
    
    def test_to_list(self):
        """测试转换为列表"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        
        self.assertEqual(rb.to_list(), [1, 2, 3])
    
    def test_repr(self):
        """测试字符串表示"""
        rb = RingBuffer[int](5)
        rb.extend([1, 2, 3])
        
        self.assertIn("RingBuffer", repr(rb))
        self.assertEqual(str(rb), "[1, 2, 3]")
    
    def test_bool(self):
        """测试布尔值"""
        rb = RingBuffer[int](5)
        self.assertFalse(bool(rb))
        
        rb.append(1)
        self.assertTrue(bool(rb))


class TestRingBufferThreadSafe(unittest.TestCase):
    """线程安全测试"""
    
    def test_concurrent_append(self):
        """测试并发添加"""
        rb = RingBuffer[int](1000, thread_safe=True)
        
        def append_values(start: int, count: int):
            for i in range(count):
                rb.append(start + i)
        
        threads = [
            threading.Thread(target=append_values, args=(i * 1000, 500))
            for i in range(4)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(rb), 1000)
    
    def test_concurrent_read_write(self):
        """测试并发读写"""
        rb = RingBuffer[int](100, thread_safe=True)
        
        def writer():
            for i in range(1000):
                rb.append(i)
        
        def reader():
            for _ in range(1000):
                _ = list(rb)
        
        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=reader),
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 不应该有异常


class TestNumericRingBuffer(unittest.TestCase):
    """NumericRingBuffer 测试"""
    
    def test_mean(self):
        """测试均值计算"""
        rb = NumericRingBuffer(5)
        rb.extend([1, 2, 3, 4, 5])
        
        self.assertEqual(rb.mean, 3.0)
    
    def test_mean_empty(self):
        """测试空缓冲区均值"""
        rb = NumericRingBuffer(5)
        
        with self.assertRaises(ValueError):
            _ = rb.mean
    
    def test_variance(self):
        """测试方差计算"""
        rb = NumericRingBuffer(10)
        rb.extend([2, 4, 4, 4, 5, 5, 7, 9])
        
        # 验证方差计算 (样本方差)
        # 手动计算: mean = 5, variance = sum((x-mean)^2)/(n-1)
        import math
        expected_var = sum((x - 5)**2 for x in [2, 4, 4, 4, 5, 5, 7, 9]) / 7
        self.assertAlmostEqual(rb.variance, expected_var, places=2)
    
    def test_std_dev(self):
        """测试标准差计算"""
        rb = NumericRingBuffer(10)
        rb.extend([2, 4, 4, 4, 5, 5, 7, 9])
        
        # 验证标准差计算
        import math
        expected_var = sum((x - 5)**2 for x in [2, 4, 4, 4, 5, 5, 7, 9]) / 7
        expected_std = math.sqrt(expected_var)
        self.assertAlmostEqual(rb.std_dev, expected_std, places=2)
    
    def test_min_max(self):
        """测试最小最大值"""
        rb = NumericRingBuffer(5)
        rb.extend([1, 2, 3, 4, 5])
        
        self.assertEqual(rb.min_value, 1)
        self.assertEqual(rb.max_value, 5)
        self.assertEqual(rb.range, 4)
    
    def test_sum(self):
        """测试求和"""
        rb = NumericRingBuffer(5)
        rb.extend([1, 2, 3, 4, 5])
        
        self.assertEqual(rb.sum, 15)
    
    def test_moving_average(self):
        """测试移动平均"""
        rb = NumericRingBuffer(10)
        rb.extend([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
        ma = rb.moving_average(3)
        
        self.assertEqual(len(ma), 8)
        self.assertEqual(ma[0], 2.0)  # (1+2+3)/3
        self.assertEqual(ma[1], 3.0)  # (2+3+4)/3
    
    def test_overflow_updates_stats(self):
        """测试溢出时更新统计"""
        rb = NumericRingBuffer(3)
        rb.extend([1, 2, 3, 4, 5])  # 只保留 3, 4, 5
        
        self.assertEqual(rb.mean, 4.0)  # (3+4+5)/3
        self.assertEqual(rb.sum, 12)
    
    def test_clear_resets_stats(self):
        """测试清空重置统计"""
        rb = NumericRingBuffer(5)
        rb.extend([1, 2, 3, 4, 5])
        rb.clear()
        
        with self.assertRaises(ValueError):
            _ = rb.mean


class TestEventBuffer(unittest.TestCase):
    """EventBuffer 测试"""
    
    def test_add_event(self):
        """测试添加事件"""
        eb = EventBuffer[str](10)
        eb.add("event1", 1000.0)
        eb.add("event2", 1001.0)
        
        self.assertEqual(len(eb), 2)
    
    def test_add_event_auto_timestamp(self):
        """测试自动时间戳"""
        eb = EventBuffer[str](10)
        eb.add("event1")
        
        events = list(eb)
        self.assertEqual(len(events), 1)
        self.assertTrue(events[0][0] > 0)
    
    def test_get_events_time_range(self):
        """测试时间范围查询"""
        eb = EventBuffer[str](10)
        eb.add("event1", 1000.0)
        eb.add("event2", 1001.0)
        eb.add("event3", 1002.0)
        eb.add("event4", 1003.0)
        
        # 查询范围
        events = eb.get_events(since=1001.0, until=1003.0)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0][1], "event2")
        self.assertEqual(events[1][1], "event3")
    
    def test_get_event_data(self):
        """测试获取事件数据"""
        eb = EventBuffer[str](10)
        eb.add("event1", 1000.0)
        eb.add("event2", 1001.0)
        
        data = eb.get_event_data()
        self.assertEqual(data, ["event1", "event2"])
    
    def test_count(self):
        """测试事件计数"""
        eb = EventBuffer[str](10)
        eb.add("event1", 1000.0)
        eb.add("event2", 1001.0)
        eb.add("event3", 1002.0)
        
        self.assertEqual(eb.count(), 3)
        self.assertEqual(eb.count(since=1001.0), 2)
    
    def test_capacity_overflow(self):
        """测试容量溢出"""
        eb = EventBuffer[int](3)
        eb.add(1, 1000.0)
        eb.add(2, 1001.0)
        eb.add(3, 1002.0)
        eb.add(4, 1003.0)  # 应该覆盖 1
        
        self.assertEqual(len(eb), 3)
        data = eb.get_event_data()
        self.assertEqual(data, [2, 3, 4])


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_create_ring_buffer(self):
        """测试创建缓冲区"""
        rb = create_ring_buffer(5, [1, 2, 3])
        
        self.assertEqual(len(rb), 3)
        self.assertEqual(list(rb), [1, 2, 3])
    
    def test_create_numeric_buffer(self):
        """测试创建数值缓冲区"""
        rb = create_numeric_buffer(5, [1.0, 2.0, 3.0])
        
        self.assertEqual(rb.mean, 2.0)
    
    def test_sliding_window(self):
        """测试滑动窗口"""
        data = [1, 2, 3, 4, 5]
        windows = list(sliding_window(data, 3))
        
        self.assertEqual(len(windows), 3)
        self.assertEqual(windows[0], [1, 2, 3])
        self.assertEqual(windows[1], [2, 3, 4])
        self.assertEqual(windows[2], [3, 4, 5])
    
    def test_sliding_window_small_data(self):
        """测试小数据滑动窗口"""
        data = [1, 2]
        windows = list(sliding_window(data, 3))
        
        self.assertEqual(len(windows), 0)
    
    def test_sliding_window_invalid_size(self):
        """测试无效窗口大小"""
        with self.assertRaises(ValueError):
            list(sliding_window([1, 2, 3], 0))
    
    def test_batch_process(self):
        """测试批量处理"""
        data = [1, 2, 3, 4, 5, 6, 7]
        results = batch_process(data, 3, sum)
        
        self.assertEqual(results, [6, 15, 7])  # [1+2+3, 4+5+6, 7]


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_capacity(self):
        """测试容量为 1"""
        rb = RingBuffer[int](1)
        rb.append(1)
        self.assertEqual(list(rb), [1])
        
        rb.append(2)
        self.assertEqual(list(rb), [2])
    
    def test_large_capacity(self):
        """测试大容量"""
        rb = RingBuffer[int](10000)
        for i in range(10000):
            rb.append(i)
        
        self.assertEqual(len(rb), 10000)
        self.assertEqual(rb[0], 0)
        self.assertEqual(rb[-1], 9999)
    
    def test_string_elements(self):
        """测试字符串元素"""
        rb = RingBuffer[str](5)
        rb.extend(["a", "b", "c"])
        
        self.assertEqual(list(rb), ["a", "b", "c"])
    
    def test_mixed_types(self):
        """测试混合类型"""
        rb = RingBuffer[object](5)
        rb.extend([1, "a", 3.14, [1, 2], {"key": "value"}])
        
        self.assertEqual(rb[0], 1)
        self.assertEqual(rb[1], "a")
        self.assertEqual(rb[2], 3.14)
    
    def test_nested_ring_buffer(self):
        """测试嵌套缓冲区"""
        rb1 = RingBuffer[int](3)
        rb1.extend([1, 2, 3])
        
        rb2 = RingBuffer[RingBuffer[int]](2)
        rb2.append(rb1)
        
        self.assertEqual(len(rb2), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)