"""
batch_utils 单元测试

测试覆盖：
- batched: 固定大小分批
- chunked: 分块
- sliding_window: 滑动窗口
- BatchProcessor: 批处理器
- TimeWindowBatcher: 时间窗口批处理器
- ParallelBatchProcessor: 并行批处理器
- BatchAggregator: 结果聚合器
- AdaptiveBatcher: 自适应批处理器
- 便捷函数
"""

import unittest
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

# 导入被测模块
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from batch_utils.mod import (
    batched, chunked, sliding_window,
    BatchProcessor, BatchResult, TimeWindowBatcher,
    ParallelBatchProcessor, BatchAggregator, AdaptiveBatcher,
    process_in_batches, batch_by_key
)


class TestBatched(unittest.TestCase):
    """测试 batched 函数"""
    
    def test_basic_batching(self):
        """测试基本分批"""
        result = list(batched([1, 2, 3, 4, 5], 2))
        self.assertEqual(result, [[1, 2], [3, 4], [5]])
    
    def test_exact_division(self):
        """测试正好整除的情况"""
        result = list(batched([1, 2, 3, 4], 2))
        self.assertEqual(result, [[1, 2], [3, 4]])
    
    def test_single_batch(self):
        """测试单个批次"""
        result = list(batched([1, 2], 5))
        self.assertEqual(result, [[1, 2]])
    
    def test_empty_input(self):
        """测试空输入"""
        result = list(batched([], 3))
        self.assertEqual(result, [])
    
    def test_drop_last(self):
        """测试丢弃最后不完整批次"""
        result = list(batched([1, 2, 3, 4, 5], 2, drop_last=True))
        self.assertEqual(result, [[1, 2], [3, 4]])
    
    def test_drop_last_complete(self):
        """测试丢弃最后（但数据完整）"""
        result = list(batched([1, 2, 3, 4], 2, drop_last=True))
        self.assertEqual(result, [[1, 2], [3, 4]])
    
    def test_size_one(self):
        """测试批次大小为1"""
        result = list(batched([1, 2, 3], 1))
        self.assertEqual(result, [[1], [2], [3]])
    
    def test_invalid_size(self):
        """测试无效批次大小"""
        with self.assertRaises(ValueError):
            list(batched([1, 2, 3], 0))
        with self.assertRaises(ValueError):
            list(batched([1, 2, 3], -1))
    
    def test_with_generator(self):
        """测试使用生成器输入"""
        def gen():
            yield 1
            yield 2
            yield 3
        result = list(batched(gen(), 2))
        self.assertEqual(result, [[1, 2], [3]])


class TestChunked(unittest.TestCase):
    """测试 chunked 函数"""
    
    def test_basic_chunking(self):
        """测试基本分块"""
        result = list(chunked([1, 2, 3, 4, 5], 2))
        self.assertEqual(result, [[1, 2, 3], [4, 5]])
    
    def test_even_distribution(self):
        """测试均匀分布"""
        result = list(chunked([1, 2, 3, 4, 5, 6], 3))
        self.assertEqual(result, [[1, 2], [3, 4], [5, 6]])
    
    def test_more_chunks_than_items(self):
        """测试块数多于元素数"""
        result = list(chunked([1, 2], 5))
        self.assertEqual(result, [[1], [2]])
    
    def test_single_chunk(self):
        """测试单块"""
        result = list(chunked([1, 2, 3, 4, 5], 1))
        self.assertEqual(result, [[1, 2, 3, 4, 5]])
    
    def test_empty_input(self):
        """测试空输入"""
        result = list(chunked([], 3))
        self.assertEqual(result, [])
    
    def test_invalid_chunks(self):
        """测试无效块数"""
        with self.assertRaises(ValueError):
            list(chunked([1, 2, 3], 0))
        with self.assertRaises(ValueError):
            list(chunked([1, 2, 3], -1))


class TestSlidingWindow(unittest.TestCase):
    """测试 sliding_window 函数"""
    
    def test_basic_window(self):
        """测试基本滑动窗口"""
        result = list(sliding_window([1, 2, 3, 4, 5], 3))
        self.assertEqual(result, [[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    
    def test_with_step(self):
        """测试带步长的滑动窗口"""
        result = list(sliding_window([1, 2, 3, 4, 5], 3, step=2))
        self.assertEqual(result, [[1, 2, 3], [3, 4, 5]])
    
    def test_window_size_one(self):
        """测试窗口大小为1"""
        result = list(sliding_window([1, 2, 3], 1))
        self.assertEqual(result, [[1], [2], [3]])
    
    def test_window_equals_length(self):
        """测试窗口大小等于数组长度"""
        result = list(sliding_window([1, 2, 3], 3))
        self.assertEqual(result, [[1, 2, 3]])
    
    def test_window_larger_than_length(self):
        """测试窗口大于数组长度"""
        result = list(sliding_window([1, 2], 5))
        self.assertEqual(result, [])
    
    def test_empty_input(self):
        """测试空输入"""
        result = list(sliding_window([], 3))
        self.assertEqual(result, [])
    
    def test_invalid_window_size(self):
        """测试无效窗口大小"""
        with self.assertRaises(ValueError):
            list(sliding_window([1, 2, 3], 0))
    
    def test_invalid_step(self):
        """测试无效步长"""
        with self.assertRaises(ValueError):
            list(sliding_window([1, 2, 3], 2, step=0))


class TestBatchProcessor(unittest.TestCase):
    """测试 BatchProcessor 类"""
    
    def test_basic_processing(self):
        """测试基本批处理"""
        processed = []
        
        def handler(batch):
            processed.append(batch)
            return sum(batch)
        
        processor = BatchProcessor(handler=handler, batch_size=3)
        processor.add_many([1, 2, 3, 4, 5])
        result = processor.flush()
        
        self.assertEqual(result.result, 15)
        self.assertEqual(len(processed), 1)
    
    def test_auto_flush(self):
        """测试自动刷新"""
        processed = []
        
        def handler(batch):
            processed.append(batch)
            return sum(batch)
        
        processor = BatchProcessor(
            handler=handler,
            batch_size=3,
            auto_flush=True
        )
        
        processor.add(1)
        processor.add(2)
        processor.add(3)  # 触发自动刷新
        processor.add(4)
        processor.flush()
        
        self.assertEqual(len(processed), 2)
    
    def test_context_manager(self):
        """测试上下文管理器"""
        processed = []
        
        def handler(batch):
            processed.append(batch)
            return sum(batch)
        
        with BatchProcessor(handler=handler, batch_size=2, auto_flush=True) as processor:
            processor.add_many([1, 2, 3, 4, 5])
        
        self.assertEqual(len(processed), 3)  # [1,2], [3,4], [5]
    
    def test_error_handling(self):
        """测试错误处理"""
        errors = []
        
        def handler(batch):
            raise ValueError("Test error")
        
        def on_error(batch, exc):
            errors.append((batch, exc))
        
        processor = BatchProcessor(
            handler=handler,
            on_error=on_error,
            max_retries=2,
            retry_delay=0.01
        )
        processor.add_many([1, 2, 3])
        result = processor.flush()
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertEqual(len(errors), 3)  # 1 initial + 2 retries
    
    def test_callback(self):
        """测试完成回调"""
        completed = []
        
        def handler(batch):
            return sum(batch)
        
        def on_complete(result):
            completed.append(result)
        
        processor = BatchProcessor(
            handler=handler,
            batch_size=2,
            auto_flush=True,
            on_batch_complete=on_complete
        )
        processor.add_many([1, 2, 3, 4])
        processor.flush()  # 处理剩余数据
        
        self.assertEqual(len(completed), 2)  # [1,2], [3,4]
    
    def test_buffer_operations(self):
        """测试缓冲区操作"""
        def handler(batch):
            return sum(batch)
        
        processor = BatchProcessor(handler=handler, batch_size=10)
        processor.add_many([1, 2, 3])
        
        self.assertEqual(processor.buffer_size, 3)
        self.assertEqual(processor.pending_count, 3)
        
        cleared = processor.clear_buffer()
        self.assertEqual(cleared, [1, 2, 3])
        self.assertEqual(processor.buffer_size, 0)


class TestTimeWindowBatcher(unittest.TestCase):
    """测试 TimeWindowBatcher 类"""
    
    def test_basic_window(self):
        """测试基本时间窗口"""
        processed = []
        
        def handler(batch):
            processed.append(batch.copy())
            return len(batch)
        
        batcher = TimeWindowBatcher(
            handler=handler,
            window_seconds=0.1,
            max_size=100
        )
        
        batcher.start()
        batcher.add_many([1, 2, 3, 4, 5])
        time.sleep(0.2)  # 等待窗口触发
        batcher.stop(flush=False)
        
        self.assertEqual(len(processed), 1)
        self.assertEqual(processed[0], [1, 2, 3, 4, 5])
    
    def test_max_size_trigger(self):
        """测试最大大小触发"""
        processed = []
        
        def handler(batch):
            processed.append(batch.copy())
            return len(batch)
        
        batcher = TimeWindowBatcher(
            handler=handler,
            window_seconds=10,  # 长时间窗口
            max_size=3
        )
        
        batcher.start()
        batcher.add(1)
        batcher.add(2)
        batcher.add(3)  # 触发最大大小
        time.sleep(0.05)
        batcher.stop(flush=False)
        
        self.assertEqual(len(processed), 1)
        self.assertEqual(processed[0], [1, 2, 3])
    
    def test_context_manager(self):
        """测试上下文管理器"""
        processed = []
        
        def handler(batch):
            processed.append(batch)
            return len(batch)
        
        with TimeWindowBatcher(handler=handler, window_seconds=0.1) as batcher:
            batcher.add_many([1, 2, 3])
            time.sleep(0.15)
        
        self.assertGreaterEqual(len(processed), 1)
    
    def test_stop_with_flush(self):
        """测试停止时刷新"""
        processed = []
        
        def handler(batch):
            processed.append(batch)
            return len(batch)
        
        batcher = TimeWindowBatcher(
            handler=handler,
            window_seconds=10  # 长时间，不会自动触发
        )
        batcher.start()
        batcher.add_many([1, 2, 3])
        batcher.stop(flush=True)
        
        self.assertEqual(len(processed), 1)


class TestParallelBatchProcessor(unittest.TestCase):
    """测试 ParallelBatchProcessor 类"""
    
    def test_basic_parallel(self):
        """测试基本并行处理"""
        def handler(batch):
            time.sleep(0.01)
            return sum(batch)
        
        processor = ParallelBatchProcessor(
            handler=handler,
            batch_size=10,
            max_workers=4
        )
        
        start = time.time()
        results = processor.process_all(range(100))
        duration = time.time() - start
        
        # 100个元素，批次大小10，共10批
        self.assertEqual(len(results), 10)
        # 并行处理应该比串行快
        self.assertLess(duration, 0.2)  # 串行需要0.1秒
        
        total = sum(r.result for r in results if r.success)
        self.assertEqual(total, 4950)
    
    def test_ordered_results(self):
        """测试结果顺序"""
        def handler(batch):
            return batch[0]  # 返回第一个元素
        
        processor = ParallelBatchProcessor(
            handler=handler,
            batch_size=1,
            max_workers=4,
            ordered=True
        )
        
        results = processor.process_all(range(10))
        values = [r.result for r in results]
        
        self.assertEqual(values, list(range(10)))
    
    def test_unordered_results(self):
        """测试无序结果"""
        def handler(batch):
            time.sleep(0.01)
            return batch[0]
        
        processor = ParallelBatchProcessor(
            handler=handler,
            batch_size=1,
            max_workers=4,
            ordered=False
        )
        
        results = processor.process_all(range(10))
        
        # 无序时，所有值应该存在，但顺序可能不同
        values = set(r.result for r in results)
        self.assertEqual(values, set(range(10)))
    
    def test_error_handling(self):
        """测试错误处理"""
        def handler(batch):
            if 5 in batch:
                raise ValueError("Found 5")
            return sum(batch)
        
        processor = ParallelBatchProcessor(
            handler=handler,
            batch_size=5,
            max_workers=2
        )
        
        results = processor.process_all(range(10))
        
        # 10个元素，批次大小5，共2批
        # 其中一批包含5，应该失败
        success_count = sum(1 for r in results if r.success)
        fail_count = sum(1 for r in results if not r.success)
        
        self.assertEqual(success_count, 1)
        self.assertEqual(fail_count, 1)


class TestBatchAggregator(unittest.TestCase):
    """测试 BatchAggregator 类"""
    
    def test_basic_aggregation(self):
        """测试基本聚合"""
        aggregator = BatchAggregator(
            initial_value=0,
            aggregate_func=lambda acc, r: acc + (r.result if r.success else 0)
        )
        
        results = [
            BatchResult(batch=[1, 2], result=3, success=True),
            BatchResult(batch=[3, 4], result=7, success=True),
            BatchResult(batch=[5, 6], result=11, success=True),
        ]
        
        for result in results:
            aggregator.add(result)
        
        self.assertEqual(aggregator.value, 21)
        self.assertEqual(aggregator.count, 3)
        self.assertEqual(aggregator.success_count, 3)
    
    def test_with_errors(self):
        """测试包含错误"""
        aggregator = BatchAggregator(
            initial_value=0,
            aggregate_func=lambda acc, r: acc + (r.result if r.success else 0)
        )
        
        results = [
            BatchResult(batch=[1, 2], result=3, success=True),
            BatchResult(batch=[3, 4], result=None, success=False, error=Exception()),
            BatchResult(batch=[5, 6], result=11, success=True),
        ]
        
        for result in results:
            aggregator.add(result)
        
        self.assertEqual(aggregator.value, 14)
        self.assertEqual(aggregator.success_count, 2)
        self.assertEqual(aggregator.error_count, 1)
    
    def test_reset(self):
        """测试重置"""
        aggregator = BatchAggregator(
            initial_value=0,
            aggregate_func=lambda acc, r: acc + r.result
        )
        
        aggregator.add(BatchResult(batch=[1, 2], result=3, success=True))
        aggregator.reset()
        
        self.assertEqual(aggregator.value, 0)
        self.assertEqual(aggregator.count, 0)
    
    def test_custom_aggregation(self):
        """测试自定义聚合"""
        aggregator = BatchAggregator(
            initial_value=[],
            aggregate_func=lambda acc, r: acc + r.batch
        )
        
        results = [
            BatchResult(batch=[1, 2], result=None, success=True),
            BatchResult(batch=[3, 4], result=None, success=True),
        ]
        
        for result in results:
            aggregator.add(result)
        
        self.assertEqual(aggregator.value, [1, 2, 3, 4])


class TestAdaptiveBatcher(unittest.TestCase):
    """测试 AdaptiveBatcher 类"""
    
    def test_basic_processing(self):
        """测试基本处理"""
        def handler(batch):
            return sum(batch)
        
        batcher = AdaptiveBatcher(
            handler=handler,
            initial_size=5,
            min_size=1,
            max_size=100
        )
        
        results = list(batcher.process(range(20)))
        
        self.assertEqual(len(results), 4)  # 20/5 = 4 batches
        total = sum(r.result for r in results if r.success)
        self.assertEqual(total, 190)
    
    def test_size_adaptation(self):
        """测试批次大小自适应"""
        call_sizes = []
        
        def handler(batch):
            call_sizes.append(len(batch))
            # 模拟处理时间与批次大小成正比
            time.sleep(len(batch) * 0.001)
            return sum(batch)
        
        batcher = AdaptiveBatcher(
            handler=handler,
            initial_size=10,
            min_size=5,
            max_size=50,
            target_duration=0.02,
            adjustment_factor=0.3
        )
        
        list(batcher.process(range(100)))
        
        # 批次大小应该会调整
        self.assertGreater(len(call_sizes), 1)
        # 初始大小应该包含在调用中
        self.assertIn(10, call_sizes)
    
    def test_size_limits(self):
        """测试批次大小限制"""
        def handler(batch):
            time.sleep(0.1)  # 非常慢
            return sum(batch)
        
        batcher = AdaptiveBatcher(
            handler=handler,
            initial_size=10,
            min_size=5,
            max_size=20,
            target_duration=0.001  # 很短的目标时间
        )
        
        list(batcher.process(range(30)))
        
        # 批次大小应该在限制范围内
        self.assertGreaterEqual(batcher.current_size, batcher.min_size)
        self.assertLessEqual(batcher.current_size, batcher.max_size)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_process_in_batches(self):
        """测试 process_in_batches"""
        results = process_in_batches(
            range(20),
            handler=lambda b: sum(b),
            batch_size=5
        )
        
        self.assertEqual(len(results), 4)
        self.assertTrue(all(r.success for r in results))
        self.assertEqual(sum(r.result for r in results), 190)
    
    def test_process_in_batches_parallel(self):
        """测试并行 process_in_batches"""
        def slow_sum(batch):
            time.sleep(0.01)
            return sum(batch)
        
        start = time.time()
        results = process_in_batches(
            range(50),
            handler=slow_sum,
            batch_size=10,
            parallel=True,
            max_workers=5
        )
        duration = time.time() - start
        
        self.assertEqual(len(results), 5)
        self.assertLess(duration, 0.1)  # 并行应该更快
    
    def test_batch_by_key(self):
        """测试 batch_by_key"""
        items = [1, 2, 3, 4, 5, 6]
        result = batch_by_key(items, lambda x: x % 2)
        
        self.assertEqual(result[0], [2, 4, 6])
        self.assertEqual(result[1], [1, 3, 5])
    
    def test_batch_by_key_string_key(self):
        """测试字符串键的 batch_by_key"""
        items = ['apple', 'ant', 'banana', 'cat', 'avocado']
        result = batch_by_key(items, lambda x: x[0])
        
        self.assertEqual(set(result.keys()), {'a', 'b', 'c'})
        self.assertEqual(result['a'], ['apple', 'ant', 'avocado'])
        self.assertEqual(result['b'], ['banana'])
        self.assertEqual(result['c'], ['cat'])


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_inputs(self):
        """测试空输入"""
        # batched
        self.assertEqual(list(batched([], 5)), [])
        
        # chunked
        self.assertEqual(list(chunked([], 3)), [])
        
        # sliding_window
        self.assertEqual(list(sliding_window([], 3)), [])
        
        # BatchProcessor
        processor = BatchProcessor(handler=lambda b: sum(b))
        self.assertIsNone(processor.flush())
        
        # process_in_batches
        self.assertEqual(process_in_batches([], lambda b: sum(b)), [])
    
    def test_single_element(self):
        """测试单个元素"""
        self.assertEqual(list(batched([1], 5)), [[1]])
        self.assertEqual(list(chunked([1], 1)), [[1]])
        self.assertEqual(list(sliding_window([1], 1)), [[1]])
    
    def test_large_batch_size(self):
        """测试大批次大小"""
        result = list(batched([1, 2, 3], 1000))
        self.assertEqual(result, [[1, 2, 3]])


class TestBatchResult(unittest.TestCase):
    """测试 BatchResult 数据类"""
    
    def test_default_values(self):
        """测试默认值"""
        result = BatchResult(batch=[1, 2, 3], result=6)
        
        self.assertEqual(result.batch, [1, 2, 3])
        self.assertEqual(result.result, 6)
        self.assertTrue(result.success)
        self.assertIsNone(result.error)
        self.assertEqual(result.duration, 0.0)
        self.assertGreater(result.timestamp, 0)
    
    def test_with_error(self):
        """测试带错误"""
        error = ValueError("test")
        result = BatchResult(
            batch=[1, 2, 3],
            result=None,
            success=False,
            error=error
        )
        
        self.assertFalse(result.success)
        self.assertEqual(result.error, error)


if __name__ == "__main__":
    unittest.main(verbosity=2)