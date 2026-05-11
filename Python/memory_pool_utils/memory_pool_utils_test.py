"""
Memory Pool Utils 单元测试
"""

import unittest
import threading
import time
from mod import (
    MemoryPool, ObjectPool, BufferPool, ArenaAllocator,
    FixedSizeAllocator, PooledObject, StringBuilder,
    PoolExhaustedError, InvalidBlockError, with_pool
)


class TestMemoryPool(unittest.TestCase):
    """MemoryPool 测试"""
    
    def test_basic_operations(self):
        """基本操作测试"""
        pool = MemoryPool(256, initial_blocks=4)
        
        # 初始状态
        self.assertEqual(pool.available, 4)
        self.assertEqual(pool.in_use, 0)
        
        # 获取块
        block = pool.acquire()
        self.assertEqual(len(block), 256)
        self.assertEqual(pool.available, 3)
        self.assertEqual(pool.in_use, 1)
        
        # 写入数据
        data = b"Hello, World!"
        block[:len(data)] = data
        self.assertEqual(bytes(block[:len(data)]), data)
        
        # 释放块
        pool.release(block)
        self.assertEqual(pool.available, 4)
        self.assertEqual(pool.in_use, 0)
    
    def test_auto_expand(self):
        """自动扩展测试"""
        pool = MemoryPool(64, initial_blocks=2, max_blocks=10, auto_expand=True)
        
        # 获取超过初始数量的块
        blocks = [pool.acquire() for _ in range(5)]
        self.assertEqual(len(blocks), 5)
        self.assertEqual(pool.in_use, 5)
        
        # 释放
        for block in blocks:
            pool.release(block)
        self.assertEqual(pool.available, 5)
    
    def test_pool_exhausted(self):
        """池耗尽测试"""
        pool = MemoryPool(64, initial_blocks=2, max_blocks=2, auto_expand=False)
        
        blocks = [pool.acquire() for _ in range(2)]
        
        # 应该耗尽
        with self.assertRaises(PoolExhaustedError):
            pool.acquire()
        
        # 释放后可以再获取
        pool.release(blocks[0])
        block = pool.acquire()
        self.assertIsNotNone(block)
    
    def test_thread_safety(self):
        """线程安全测试"""
        pool = MemoryPool(128, initial_blocks=100, max_blocks=100)
        
        results = []
        errors = []
        
        def worker():
            try:
                for _ in range(50):
                    block = pool.acquire()
                    time.sleep(0.001)
                    pool.release(block)
            except PoolExhaustedError:
                errors.append("exhausted")
            except Exception as e:
                errors.append(str(e))
        
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 应该没有错误
        self.assertEqual(len(errors), 0)
        # 所有块应该回到池中
        self.assertEqual(pool.available, 100)
        self.assertEqual(pool.in_use, 0)
    
    def test_utilization(self):
        """利用率测试"""
        pool = MemoryPool(64, initial_blocks=10)
        self.assertEqual(pool.utilization, 0.0)
        
        blocks = [pool.acquire() for _ in range(5)]
        self.assertAlmostEqual(pool.utilization, 0.5)
        
        for block in blocks:
            pool.release(block)
        self.assertEqual(pool.utilization, 0.0)
    
    def test_invalid_release(self):
        """无效释放测试"""
        pool = MemoryPool(64, initial_blocks=2)
        
        # 不是 bytearray
        with self.assertRaises(InvalidBlockError):
            pool.release("not a block")
        
        # 不是池中的块
        foreign_block = bytearray(64)
        with self.assertRaises(InvalidBlockError):
            pool.release(foreign_block)
    
    def test_clear(self):
        """清空测试"""
        pool = MemoryPool(64, initial_blocks=10)
        
        blocks = [pool.acquire() for _ in range(5)]
        
        # 清空未使用的块
        pool.clear()
        self.assertEqual(pool.available, 0)
        self.assertEqual(pool.in_use, 5)
        
        # 释放使用中的块
        for block in blocks:
            pool.release(block)
        self.assertEqual(pool.available, 5)
    
    def test_invalid_parameters(self):
        """无效参数测试"""
        with self.assertRaises(ValueError):
            MemoryPool(0)
        
        with self.assertRaises(ValueError):
            MemoryPool(64, initial_blocks=0)
        
        with self.assertRaises(ValueError):
            MemoryPool(64, initial_blocks=10, max_blocks=5)


class TestObjectPool(unittest.TestCase):
    """ObjectPool 测试"""
    
    def setUp(self):
        self.counter = 0
    
    def _create_object(self):
        self.counter += 1
        return {'id': self.counter, 'value': 0}
    
    def _reset_object(self, obj):
        obj['value'] = 0
    
    def test_basic_operations(self):
        """基本操作测试"""
        pool = ObjectPool(
            factory=self._create_object,
            reset=self._reset_object,
            initial_size=3
        )
        
        self.assertEqual(pool.available, 3)
        self.assertEqual(pool.in_use, 0)
        self.assertEqual(self.counter, 3)  # 预创建了 3 个
        
        # 获取对象
        obj = pool.acquire()
        obj['value'] = 42
        self.assertEqual(pool.available, 2)
        self.assertEqual(pool.in_use, 1)
        
        # 释放并重置
        pool.release(obj)
        self.assertEqual(obj['value'], 0)  # 已重置
        self.assertEqual(pool.available, 3)
    
    def test_factory_creation(self):
        """工厂函数测试"""
        pool = ObjectPool(factory=self._create_object, initial_size=0)
        
        self.assertEqual(self.counter, 0)
        
        # 按需创建
        obj1 = pool.acquire()
        self.assertEqual(self.counter, 1)
        
        obj2 = pool.acquire()
        self.assertEqual(self.counter, 2)
        
        pool.release(obj1)
        pool.release(obj2)
        
        # 再次获取会复用
        obj3 = pool.acquire()
        self.assertEqual(self.counter, 2)  # 没有创建新的
    
    def test_max_size_limit(self):
        """最大大小限制测试"""
        pool = ObjectPool(factory=self._create_object, max_size=3)
        
        # 获取 3 个
        objs = [pool.acquire() for _ in range(3)]
        
        # 第 4 个应该失败
        with self.assertRaises(PoolExhaustedError):
            pool.acquire()
        
        # 释放后可以再获取
        pool.release(objs[0])
        obj = pool.acquire()
        self.assertIsNotNone(obj)
    
    def test_reset_callback_error(self):
        """重置回调错误测试"""
        def bad_reset(obj):
            raise RuntimeError("Reset error")
        
        pool = ObjectPool(
            factory=lambda: {'value': 1},
            reset=bad_reset
        )
        
        obj = pool.acquire()
        obj['value'] = 42
        
        # 重置错误不应该阻止放回池中
        pool.release(obj)
        self.assertEqual(pool.available, 1)
    
    def test_thread_safety(self):
        """线程安全测试"""
        pool = ObjectPool(
            factory=lambda: {'count': 0},
            reset=lambda obj: obj.update({'count': 0}),
            initial_size=50
        )
        
        def worker():
            for _ in range(20):
                obj = pool.acquire()
                obj['count'] += 1
                time.sleep(0.001)
                pool.release(obj)
        
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(pool.available, 50)
        self.assertEqual(pool.in_use, 0)


class TestBufferPool(unittest.TestCase):
    """BufferPool 测试"""
    
    def test_size_selection(self):
        """大小选择测试"""
        pool = BufferPool()
        
        # 小请求
        buf1 = pool.get(50)
        self.assertEqual(len(buf1), 64)  # 第一个等级
        
        # 中等请求
        buf2 = pool.get(500)
        self.assertEqual(len(buf2), 1024)  # 第三个等级
        
        # 大请求
        buf3 = pool.get(5000)
        self.assertEqual(len(buf3), 16384)  # 第五个等级
        
        pool.put(buf1)
        pool.put(buf2)
        pool.put(buf3)
    
    def test_reuse(self):
        """复用测试"""
        pool = BufferPool()
        
        # 第一次获取创建
        buf1 = pool.get(256)
        self.assertEqual(pool.stats['misses'], 1)
        
        pool.put(buf1)
        
        # 第二次获取应该命中（复用）
        buf2 = pool.get(256)
        self.assertEqual(len(buf2), 256)
        self.assertEqual(pool.stats['misses'], 1)  # 没有增加
        
        # 统计
        stats = pool.stats
        self.assertEqual(stats['gets'], 2)
        self.assertEqual(stats['puts'], 1)
    
    def test_custom_size(self):
        """自定义大小测试"""
        pool = BufferPool()
        
        # 超大请求（不在预设等级中）
        buf = pool.get(2000000)
        self.assertEqual(len(buf), 2000000)
        
        pool.put(buf)
    
    def test_stats(self):
        """统计测试"""
        pool = BufferPool()
        
        buf1 = pool.get(100)
        buf2 = pool.get(200)
        buf3 = pool.get(300)
        
        stats = pool.stats
        self.assertEqual(stats['gets'], 3)
        self.assertEqual(stats['creates'], 3)
        
        pool.put(buf1)
        pool.put(buf2)
        
        stats = pool.stats
        self.assertEqual(stats['puts'], 2)
    
    def test_clear(self):
        """清空测试"""
        pool = BufferPool()
        
        # 获取两个不同大小的缓冲区
        buf1 = pool.get(256)
        buf2 = pool.get(512)  # 512 会匹配 1024 等级
        
        pool.put(buf1)
        pool.put(buf2)
        
        # 两个不同等级各有一个缓冲区
        self.assertEqual(pool.total_buffers, 2)
        
        pool.clear()
        self.assertEqual(pool.total_buffers, 0)
    
    def test_invalid_size(self):
        """无效大小测试"""
        pool = BufferPool()
        
        with self.assertRaises(ValueError):
            pool.get(0)
        
        with self.assertRaises(ValueError):
            pool.get(-1)


class TestArenaAllocator(unittest.TestCase):
    """ArenaAllocator 测试"""
    
    def test_basic_allocation(self):
        """基本分配测试"""
        arena = ArenaAllocator(1024)
        
        buf1 = arena.alloc(100)
        self.assertEqual(len(buf1), 100)
        
        buf2 = arena.alloc(200)
        self.assertEqual(len(buf2), 200)
        
        self.assertEqual(arena.used, 300)
        self.assertEqual(arena.available, 724)
        self.assertEqual(arena.allocations, 2)
    
    def test_alignment(self):
        """对齐测试"""
        arena = ArenaAllocator(1024)
        
        # 不对齐
        buf1 = arena.alloc(7)
        self.assertEqual(arena.used, 7)
        
        # 4 字节对齐
        buf2 = arena.alloc(10, align=4)
        # 应该从 8 开始（下一个 4 字节对齐位置）
        self.assertEqual(arena.used, 8 + 10)
    
    def test_reset(self):
        """重置测试"""
        arena = ArenaAllocator(1024)
        
        arena.alloc(100)
        arena.alloc(200)
        arena.alloc(300)
        
        self.assertEqual(arena.used, 600)
        
        arena.reset()
        
        self.assertEqual(arena.used, 0)
        self.assertEqual(arena.available, 1024)
        self.assertEqual(arena.allocations, 0)
    
    def test_memory_exhaustion(self):
        """内存耗尽测试"""
        arena = ArenaAllocator(100)
        
        arena.alloc(50)
        arena.alloc(40)
        
        # 只有 10 字节剩余
        arena.alloc(10)
        
        # 应该失败
        with self.assertRaises(MemoryError):
            arena.alloc(1)
    
    def test_utilization(self):
        """利用率测试"""
        arena = ArenaAllocator(1000)
        
        self.assertEqual(arena.utilization, 0.0)
        
        arena.alloc(250)
        self.assertAlmostEqual(arena.utilization, 0.25)
        
        arena.alloc(250)
        self.assertAlmostEqual(arena.utilization, 0.5)
        
        arena.reset()
        self.assertEqual(arena.utilization, 0.0)
    
    def test_invalid_parameters(self):
        """无效参数测试"""
        arena = ArenaAllocator(1000)
        
        with self.assertRaises(ValueError):
            arena.alloc(0)
        
        with self.assertRaises(ValueError):
            arena.alloc(100, align=0)
        
        with self.assertRaises(ValueError):
            ArenaAllocator(0)
    
    def test_thread_safety(self):
        """线程安全测试"""
        arena = ArenaAllocator(10000)
        
        def worker():
            for _ in range(10):
                buf = arena.alloc(50)
                time.sleep(0.001)
        
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(arena.allocations, 100)
        self.assertEqual(arena.used, 5000)


class TestFixedSizeAllocator(unittest.TestCase):
    """FixedSizeAllocator 测试"""
    
    def test_basic_operations(self):
        """基本操作测试"""
        allocator = FixedSizeAllocator(64, 10)
        
        self.assertEqual(allocator.available, 10)
        self.assertEqual(allocator.in_use, 0)
        
        blocks = [allocator.acquire() for _ in range(5)]
        
        self.assertEqual(allocator.available, 5)
        self.assertEqual(allocator.in_use, 5)
        self.assertEqual(allocator.total_blocks, 10)
        
        for block in blocks:
            allocator.release(block)
        
        self.assertEqual(allocator.available, 10)
        self.assertEqual(allocator.in_use, 0)
    
    def test_auto_expand(self):
        """自动扩展测试"""
        allocator = FixedSizeAllocator(64, 5, auto_expand=True)
        
        # 获取超过初始数量的块
        blocks = [allocator.acquire() for _ in range(10)]
        self.assertEqual(len(blocks), 10)
        self.assertEqual(allocator.total_blocks, 10)
        
        for block in blocks:
            allocator.release(block)
        
        self.assertEqual(allocator.available, 10)
    
    def test_exhaustion(self):
        """耗尽测试"""
        allocator = FixedSizeAllocator(64, 5, auto_expand=False)
        
        blocks = [allocator.acquire() for _ in range(5)]
        
        with self.assertRaises(PoolExhaustedError):
            allocator.acquire()
        
        allocator.release(blocks[0])
        block = allocator.acquire()
        self.assertIsNotNone(block)
    
    def test_block_size(self):
        """块大小测试"""
        allocator = FixedSizeAllocator(128, 5)
        
        block = allocator.acquire()
        self.assertEqual(len(block), 128)
        
        allocator.release(block)
    
    def test_invalid_release(self):
        """无效释放测试"""
        allocator = FixedSizeAllocator(64, 5)
        
        foreign_block = bytearray(64)
        with self.assertRaises(InvalidBlockError):
            allocator.release(foreign_block)
    
    def test_utilization(self):
        """利用率测试"""
        allocator = FixedSizeAllocator(64, 10)
        
        self.assertEqual(allocator.utilization, 0.0)
        
        blocks = [allocator.acquire() for _ in range(4)]
        self.assertAlmostEqual(allocator.utilization, 0.4)
        
        for block in blocks:
            allocator.release(block)
        self.assertEqual(allocator.utilization, 0.0)


class TestPooledObject(unittest.TestCase):
    """PooledObject 测试"""
    
    def test_context_manager(self):
        """上下文管理器测试"""
        pool = ObjectPool(factory=lambda: {'value': 0})
        
        with PooledObject(pool, pool.acquire()) as obj:
            obj['value'] = 42
            self.assertEqual(obj['value'], 42)
        
        # 应该已放回池中
        self.assertEqual(pool.available, 1)
    
    def test_manual_release(self):
        """手动释放测试"""
        pool = ObjectPool(factory=lambda: {'value': 0})
        
        wrapped = PooledObject(pool, pool.acquire())
        wrapped.obj['value'] = 42
        
        self.assertEqual(pool.available, 0)
        
        wrapped.release()
        self.assertEqual(pool.available, 1)
        
        # 重复释放应该被忽略
        wrapped.release()
        self.assertEqual(pool.available, 1)
    
    def test_access_after_release(self):
        """释放后访问测试"""
        pool = ObjectPool(factory=lambda: {'value': 0})
        
        wrapped = PooledObject(pool, pool.acquire())
        wrapped.release()
        
        with self.assertRaises(InvalidBlockError):
            wrapped.obj
    
    def test_with_pool_function(self):
        """with_pool 函数测试"""
        pool = ObjectPool(factory=lambda: {'count': 0})
        
        with with_pool(pool) as obj:
            obj['count'] = 5
        
        self.assertEqual(pool.available, 1)


class TestStringBuilder(unittest.TestCase):
    """StringBuilder 测试"""
    
    def test_basic_usage(self):
        """基本使用测试"""
        pool = MemoryPool(64)
        sb = StringBuilder(pool)
        
        sb.append("Hello")
        sb.append(", ")
        sb.append("World!")
        
        result = sb.build()
        self.assertEqual(result, "Hello, World!")
    
    def test_large_text(self):
        """大文本测试"""
        pool = MemoryPool(128)
        sb = StringBuilder(pool)
        
        # 构建超过单个块大小的文本
        for i in range(100):
            sb.append(f"Line {i}\n")
        
        result = sb.build()
        lines = result.split('\n')
        self.assertEqual(len(lines), 101)  # 100 行 + 最后空行
    
    def test_unicode(self):
        """Unicode 测试"""
        pool = MemoryPool(256)
        sb = StringBuilder(pool)
        
        sb.append("你好")
        sb.append(", ")
        sb.append("世界!")
        
        result = sb.build()
        self.assertEqual(result, "你好, 世界!")
    
    def test_clear(self):
        """清空测试"""
        pool = MemoryPool(256, initial_blocks=5)  # 更大的块避免使用多个
        sb = StringBuilder(pool)
        
        sb.append("Test data")
        # 确保只使用了 1 个块（数据小于块大小）
        self.assertEqual(pool.in_use, 1)
        
        sb.clear()
        self.assertEqual(pool.available, 5)  # 回到初始状态
        self.assertEqual(sb.build(), "")
    
    def test_chain_append(self):
        """链式追加测试"""
        pool = MemoryPool(256)
        sb = StringBuilder(pool)
        
        sb.append("A").append("B").append("C")
        
        self.assertEqual(sb.build(), "ABC")


if __name__ == '__main__':
    unittest.main(verbosity=2)