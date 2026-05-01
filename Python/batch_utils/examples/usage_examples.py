"""
batch_utils 使用示例

演示批处理工具模块的各种用法。
"""

import time
from typing import List

# 导入模块
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from batch_utils.mod import (
    batched, chunked, sliding_window,
    BatchProcessor, TimeWindowBatcher,
    ParallelBatchProcessor, BatchAggregator,
    AdaptiveBatcher, process_in_batches, batch_by_key
)


def example_1_basic_batching():
    """示例1：基本分批操作"""
    print("=" * 60)
    print("示例1：基本分批操作")
    print("=" * 60)
    
    data = list(range(1, 11))  # [1, 2, 3, ..., 10]
    print(f"原始数据: {data}")
    
    # 基本分批 - 每批3个元素
    print("\n--- batched (固定大小分批) ---")
    for i, batch in enumerate(batched(data, 3)):
        print(f"批次 {i + 1}: {batch}")
    
    # 分块 - 分成3块
    print("\n--- chunked (分块) ---")
    for i, chunk in enumerate(chunked(data, 3)):
        print(f"块 {i + 1}: {chunk}")
    
    # 滑动窗口 - 窗口大小3
    print("\n--- sliding_window (滑动窗口) ---")
    for i, window in enumerate(sliding_window(data, 3)):
        print(f"窗口 {i + 1}: {window}")
    
    # 滑动窗口 - 步长2
    print("\n--- sliding_window (步长2) ---")
    for i, window in enumerate(sliding_window(data, 3, step=2)):
        print(f"窗口 {i + 1}: {window}")


def example_2_batch_processor():
    """示例2：批处理器"""
    print("\n" + "=" * 60)
    print("示例2：BatchProcessor - 批处理器")
    print("=" * 60)
    
    # 模拟数据库批量插入
    def insert_to_database(records: List[dict]) -> int:
        """模拟批量插入数据库"""
        print(f"  插入 {len(records)} 条记录: {[r['id'] for r in records]}")
        time.sleep(0.05)  # 模拟数据库操作
        return len(records)
    
    # 创建批处理器
    processor = BatchProcessor(
        handler=insert_to_database,
        batch_size=3,
        auto_flush=True,  # 达到批次大小时自动刷新
        on_batch_complete=lambda result: print(
            f"  ✓ 批次完成: {result.result} 条记录, 耗时 {result.duration:.3f}s"
        )
    )
    
    # 添加数据
    print("\n添加数据 (batch_size=3):")
    for i in range(10):
        processor.add({"id": i, "name": f"item_{i}"})
    
    # 手动刷新剩余数据
    if processor.pending_count > 0:
        print(f"\n刷新剩余 {processor.pending_count} 条数据...")
        processor.flush()
    
    print(f"\n总处理: {sum(r.result for r in processor.results)} 条记录")


def example_3_time_window_batcher():
    """示例3：时间窗口批处理器"""
    print("\n" + "=" * 60)
    print("示例3：TimeWindowBatcher - 时间窗口批处理器")
    print("=" * 60)
    
    events = []
    
    def process_events(batch: List[dict]) -> int:
        """处理事件批次"""
        print(f"  处理 {len(batch)} 个事件: {[e['type'] for e in batch]}")
        events.append(len(batch))
        return len(batch)
    
    # 创建时间窗口批处理器
    batcher = TimeWindowBatcher(
        handler=process_events,
        window_seconds=0.3,  # 0.3秒窗口
        max_size=5,  # 最大5个事件
        on_batch=lambda result: print(
            f"  ✓ 窗口触发: {result.result} 个事件"
        )
    )
    
    print("\n启动批处理器 (窗口=0.3s, 最大=5):")
    batcher.start()
    
    # 快速添加事件
    print("快速添加事件...")
    for i in range(8):
        batcher.add({"type": f"event_{i}", "timestamp": time.time()})
        time.sleep(0.05)
    
    # 等待窗口触发
    print("等待窗口触发...")
    time.sleep(0.4)
    
    # 添加更多事件触发最大大小
    print("\n添加5个事件触发最大大小:")
    for i in range(5):
        batcher.add({"type": f"burst_{i}", "timestamp": time.time()})
    time.sleep(0.1)
    
    batcher.stop()
    print(f"\n总事件数: {sum(events)}")


def example_4_parallel_processing():
    """示例4：并行批处理"""
    print("\n" + "=" * 60)
    print("示例4：ParallelBatchProcessor - 并行批处理")
    print("=" * 60)
    
    def slow_process(batch: List[int]) -> int:
        """模拟耗时处理"""
        time.sleep(0.1)  # 模拟IO操作
        return sum(batch)
    
    # 创建并行批处理器
    processor = ParallelBatchProcessor(
        handler=slow_process,
        batch_size=20,
        max_workers=4,
        ordered=True  # 保持结果顺序
    )
    
    # 处理100个数字
    print("并行处理 100 个数字 (批次=20, 工作线程=4):")
    
    start = time.time()
    results = processor.process_all(range(100))
    duration = time.time() - start
    
    print(f"处理 {len(results)} 个批次")
    print(f"总耗时: {duration:.3f}s (串行需要约 {0.1 * len(results):.1f}s)")
    print(f"结果总和: {sum(r.result for r in results)}")
    print(f"结果顺序: {'正确' if [r.batch[0] for r in results] == list(range(0, 100, 20)) else '错误'}")


def example_5_adaptive_batcher():
    """示例5：自适应批处理器"""
    print("\n" + "=" * 60)
    print("示例5：AdaptiveBatcher - 自适应批处理器")
    print("=" * 60)
    
    call_history = []
    
    def adaptive_process(batch: List[int]) -> int:
        """模拟处理时间随批次大小变化"""
        # 处理时间与批次大小成正比
        process_time = len(batch) * 0.01
        time.sleep(process_time)
        call_history.append(len(batch))
        return sum(batch)
    
    # 创建自适应批处理器
    batcher = AdaptiveBatcher(
        handler=adaptive_process,
        initial_size=5,
        min_size=3,
        max_size=30,
        target_duration=0.1,  # 目标处理时间0.1秒
        adjustment_factor=0.2
    )
    
    print("处理 200 个数字 (初始批次=5, 目标时间=0.1s):")
    print("根据处理时间动态调整批次大小...\n")
    
    for result in batcher.process(range(200)):
        print(
            f"  批次大小: {len(result.batch):2d}, "
            f"耗时: {result.duration:.3f}s, "
            f"结果: {result.result}"
        )
    
    print(f"\n最终批次大小: {batcher.current_size}")
    print(f"批次大小变化: {call_history[:5]} ... {call_history[-5:]}")


def example_6_batch_aggregator():
    """示例6：批处理结果聚合"""
    print("\n" + "=" * 60)
    print("示例6：BatchAggregator - 批处理结果聚合")
    print("=" * 60)
    
    # 创建聚合器 - 计算总和
    sum_aggregator = BatchAggregator(
        initial_value=0,
        aggregate_func=lambda acc, r: acc + (r.result if r.success else 0)
    )
    
    # 创建聚合器 - 收集所有元素
    collect_aggregator = BatchAggregator(
        initial_value=[],
        aggregate_func=lambda acc, r: acc + r.batch
    )
    
    # 模拟处理结果
    from batch_utils.mod import BatchResult
    
    results = [
        BatchResult(batch=[1, 2, 3], result=6, success=True),
        BatchResult(batch=[4, 5, 6], result=15, success=True),
        BatchResult(batch=[7, 8, 9], result=24, success=True),
    ]
    
    print("处理结果:")
    for result in results:
        print(f"  批次 {result.batch} -> 结果: {result.result}")
        sum_aggregator.add(result)
        collect_aggregator.add(result)
    
    print(f"\n总和聚合: {sum_aggregator.value}")
    print(f"收集聚合: {collect_aggregator.value}")
    print(f"成功率: {sum_aggregator.success_count}/{sum_aggregator.count}")


def example_7_convenience_functions():
    """示例7：便捷函数"""
    print("\n" + "=" * 60)
    print("示例7：便捷函数")
    print("=" * 60)
    
    # process_in_batches - 串行处理
    print("\n--- process_in_batches (串行) ---")
    results = process_in_batches(
        range(20),
        handler=lambda b: sum(b),
        batch_size=5
    )
    print(f"结果: {[r.result for r in results]}")
    print(f"总和: {sum(r.result for r in results)}")
    
    # process_in_batches - 并行处理
    print("\n--- process_in_batches (并行) ---")
    
    def slow_sum(batch):
        time.sleep(0.02)
        return sum(batch)
    
    start = time.time()
    results = process_in_batches(
        range(50),
        handler=slow_sum,
        batch_size=10,
        parallel=True,
        max_workers=5
    )
    print(f"耗时: {time.time() - start:.3f}s")
    print(f"结果: {[r.result for r in results]}")
    
    # batch_by_key - 按键分组
    print("\n--- batch_by_key ---")
    items = ['apple', 'ant', 'banana', 'blue', 'cat', 'cherry', 'date']
    grouped = batch_by_key(items, lambda x: x[0])
    print(f"原始数据: {items}")
    print(f"按键分组: {dict(grouped)}")


def example_8_context_manager():
    """示例8：上下文管理器用法"""
    print("\n" + "=" * 60)
    print("示例8：上下文管理器用法")
    print("=" * 60)
    
    processed = []
    
    def handler(batch):
        processed.append(batch)
        return sum(batch)
    
    # BatchProcessor 上下文管理器
    print("\n--- BatchProcessor ---")
    with BatchProcessor(handler=handler, batch_size=3) as processor:
        for i in range(10):
            processor.add(i)
        # 自动刷新
    
    print(f"处理批次: {processed}")
    
    # TimeWindowBatcher 上下文管理器
    processed.clear()
    print("\n--- TimeWindowBatcher ---")
    
    with TimeWindowBatcher(handler=handler, window_seconds=0.1) as batcher:
        for i in range(10):
            batcher.add(i)
        time.sleep(0.15)
        # 自动停止并刷新
    
    print(f"处理批次: {processed}")


def example_9_error_handling():
    """示例9：错误处理"""
    print("\n" + "=" * 60)
    print("示例9：错误处理")
    print("=" * 60)
    
    errors = []
    
    def risky_handler(batch):
        """可能失败的处理函数"""
        if 5 in batch:
            raise ValueError(f"批次包含敏感数字 5: {batch}")
        return sum(batch)
    
    def on_error(batch, exc):
        errors.append((batch, str(exc)))
        print(f"  ⚠ 错误: {exc}")
    
    processor = BatchProcessor(
        handler=risky_handler,
        batch_size=3,
        on_error=on_error,
        max_retries=1,  # 重试1次
        retry_delay=0.01
    )
    
    print("处理数据 (包含敏感数字 5):")
    processor.add_many([1, 2, 3])  # 正常
    processor.flush()
    processor.add_many([4, 5, 6])  # 会失败
    processor.flush()
    processor.add_many([7, 8, 9])  # 正常
    processor.flush()
    
    print(f"\n成功批次: {sum(1 for r in processor.results if r.success)}")
    print(f"失败批次: {sum(1 for r in processor.results if not r.success)}")
    print(f"错误记录: {len(errors)}")


def example_10_real_world_scenario():
    """示例10：实际应用场景"""
    print("\n" + "=" * 60)
    print("示例10：实际应用场景 - 批量API请求")
    print("=" * 60)
    
    class BatchAPI:
        """模拟批量API客户端"""
        
        def __init__(self):
            self.request_count = 0
            self.total_items = 0
        
        def process_batch(self, items: List[dict]) -> dict:
            """处理一批请求"""
            self.request_count += 1
            self.total_items += len(items)
            # 模拟API延迟
            time.sleep(0.05)
            return {
                "success": True,
                "processed": len(items),
                "request_id": f"req_{self.request_count}"
            }
    
    api = BatchAPI()
    
    # 创建批处理器
    processor = BatchProcessor(
        handler=api.process_batch,
        batch_size=10,
        auto_flush=True,
        on_batch_complete=lambda r: print(
            f"  请求 {r.result['request_id']}: "
            f"处理 {r.result['processed']} 项, "
            f"耗时 {r.duration*1000:.1f}ms"
        )
    )
    
    # 模拟批量发送用户更新
    print("模拟批量发送用户更新:")
    users = [{"id": i, "name": f"user_{i}"} for i in range(35)]
    
    for user in users:
        processor.add(user)
    
    # 确保所有数据已处理
    if processor.pending_count > 0:
        processor.flush()
    
    print(f"\n统计:")
    print(f"  总用户: {len(users)}")
    print(f"  API请求数: {api.request_count}")
    print(f"  平均批次大小: {api.total_items / api.request_count:.1f}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("batch_utils 使用示例集合")
    print("=" * 60)
    
    example_1_basic_batching()
    example_2_batch_processor()
    example_3_time_window_batcher()
    example_4_parallel_processing()
    example_5_adaptive_batcher()
    example_6_batch_aggregator()
    example_7_convenience_functions()
    example_8_context_manager()
    example_9_error_handling()
    example_10_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()