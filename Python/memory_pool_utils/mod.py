"""
Memory Pool Utils - 内存池工具集

提供高效的内存管理和对象复用工具：
- MemoryPool: 通用内存池，支持块分配和释放
- ObjectPool: 对象池，支持对象复用，减少 GC 压力
- BufferPool: 缓冲区池，适合网络 I/O 场景
- ArenaAllocator: Arena 分配器，批量释放内存
- FixedSizeAllocator: 固定大小块分配器，零碎片

零外部依赖，线程安全。

使用场景：
- 游戏开发中的对象管理
- 网络编程中的缓冲区管理
- 高频创建销毁对象的场景
- 实时系统中的内存管理
"""

import threading
import time
import weakref
from abc import ABC, abstractmethod
from collections import deque
from typing import (
    Any, Callable, Generic, Optional, TypeVar, List,
    Dict, Deque
)


T = TypeVar('T')


class PoolExhaustedError(Exception):
    """内存池耗尽异常"""
    pass


class InvalidBlockError(Exception):
    """无效块异常"""
    pass


class BasePool(ABC, Generic[T]):
    """内存池基类"""
    
    @abstractmethod
    def acquire(self) -> T:
        """获取一个对象"""
        pass
    
    @abstractmethod
    def release(self, obj: T) -> None:
        """释放一个对象"""
        pass
    
    @property
    @abstractmethod
    def available(self) -> int:
        """可用对象数量"""
        pass
    
    @property
    @abstractmethod
    def in_use(self) -> int:
        """正在使用的对象数量"""
        pass


class MemoryPool(BasePool[bytearray]):
    """
    通用内存池
    
    管理固定大小的内存块，支持预分配和动态扩展。
    适合需要频繁分配/释放固定大小内存的场景。
    
    特点：
    - 预分配内存，减少系统调用
    - 支持自动扩展
    - 线程安全
    - 内存复用
    """
    
    def __init__(
        self,
        block_size: int,
        initial_blocks: int = 16,
        max_blocks: int = 1024,
        auto_expand: bool = True
    ):
        """
        初始化内存池
        
        Args:
            block_size: 每个内存块的大小（字节）
            initial_blocks: 初始块数量
            max_blocks: 最大块数量
            auto_expand: 是否自动扩展
        """
        if block_size <= 0:
            raise ValueError("块大小必须为正数")
        if initial_blocks <= 0:
            raise ValueError("初始块数量必须为正数")
        if max_blocks < initial_blocks:
            raise ValueError("最大块数量不能小于初始块数量")
        
        self.block_size = block_size
        self.max_blocks = max_blocks
        self.auto_expand = auto_expand
        
        self._pool: Deque[bytearray] = deque()
        self._in_use: Dict[int, bytearray] = {}
        self._total_allocated = 0
        self._lock = threading.Lock()
        
        # 预分配初始块
        self._allocate_blocks(initial_blocks)
    
    def _allocate_blocks(self, count: int) -> int:
        """分配新的内存块"""
        allocated = 0
        for _ in range(count):
            if self._total_allocated >= self.max_blocks:
                break
            block = bytearray(self.block_size)
            self._pool.append(block)
            self._total_allocated += 1
            allocated += 1
        return allocated
    
    def acquire(self) -> bytearray:
        """获取一个内存块"""
        with self._lock:
            if not self._pool:
                if self.auto_expand and self._total_allocated < self.max_blocks:
                    self._allocate_blocks(1)
                if not self._pool:
                    raise PoolExhaustedError("内存池已耗尽且无法扩展")
            
            block = self._pool.popleft()
            block_id = id(block)
            self._in_use[block_id] = block
            return block
    
    def release(self, obj: bytearray) -> None:
        """释放内存块"""
        if not isinstance(obj, bytearray):
            raise InvalidBlockError("只能释放 bytearray 对象")
        
        with self._lock:
            block_id = id(obj)
            if block_id not in self._in_use:
                raise InvalidBlockError("此内存块不属于此池或已被释放")
            
            # 清零内存块
            obj[:] = b'\x00' * len(obj)
            del self._in_use[block_id]
            self._pool.append(obj)
    
    @property
    def available(self) -> int:
        """可用块数量"""
        with self._lock:
            return len(self._pool)
    
    @property
    def in_use(self) -> int:
        """正在使用的块数量"""
        with self._lock:
            return len(self._in_use)
    
    @property
    def total_allocated(self) -> int:
        """总分配块数"""
        return self._total_allocated
    
    @property
    def utilization(self) -> float:
        """利用率（0-1）"""
        with self._lock:
            if self._total_allocated == 0:
                return 0.0
            return len(self._in_use) / self._total_allocated
    
    def clear(self) -> None:
        """清空池（释放所有未使用的块）"""
        with self._lock:
            self._pool.clear()
            self._total_allocated = len(self._in_use)


class ObjectPool(BasePool[T]):
    """
    对象池
    
    管理可复用对象，通过工厂函数创建新对象。
    支持对象重置和生命周期回调。
    
    特点：
    - 减少对象创建开销
    - 降低 GC 压力
    - 支持对象初始化/重置回调
    - 线程安全
    
    用法：
        pool = ObjectPool(
            factory=lambda: MyObject(),
            reset=lambda obj: obj.reset(),
            initial_size=10
        )
        
        obj = pool.acquire()
        try:
            # 使用对象
            obj.do_something()
        finally:
            pool.release(obj)
    """
    
    def __init__(
        self,
        factory: Callable[[], T],
        reset: Optional[Callable[[T], None]] = None,
        initial_size: int = 0,
        max_size: int = 1024
    ):
        """
        初始化对象池
        
        Args:
            factory: 对象工厂函数
            reset: 对象重置函数（释放时调用）
            initial_size: 初始对象数量
            max_size: 最大对象数量
        """
        if initial_size < 0:
            raise ValueError("初始对象数量不能为负数")
        if max_size < initial_size:
            raise ValueError("最大对象数量不能小于初始对象数量")
        
        self._factory = factory
        self._reset = reset
        self.max_size = max_size
        
        self._pool: Deque[T] = deque()
        self._in_use: Dict[int, T] = {}
        self._lock = threading.Lock()
        
        # 预创建对象
        for _ in range(initial_size):
            obj = self._factory()
            self._pool.append(obj)
    
    def acquire(self) -> T:
        """获取一个对象"""
        with self._lock:
            if self._pool:
                obj = self._pool.popleft()
            elif len(self._in_use) < self.max_size:
                obj = self._factory()
            else:
                raise PoolExhaustedError("对象池已耗尽")
            
            self._in_use[id(obj)] = obj
            return obj
    
    def release(self, obj: T) -> None:
        """释放对象"""
        with self._lock:
            obj_id = id(obj)
            if obj_id not in self._in_use:
                raise InvalidBlockError("此对象不属于此池或已被释放")
            
            del self._in_use[obj_id]
            
            # 调用重置函数
            if self._reset:
                try:
                    self._reset(obj)
                except Exception:
                    pass  # 重置失败不影响放回池中
            
            self._pool.append(obj)
    
    @property
    def available(self) -> int:
        """可用对象数量"""
        with self._lock:
            return len(self._pool)
    
    @property
    def in_use(self) -> int:
        """正在使用的对象数量"""
        with self._lock:
            return len(self._in_use)
    
    @property
    def total_objects(self) -> int:
        """总对象数量"""
        with self._lock:
            return len(self._pool) + len(self._in_use)


class BufferPool:
    """
    缓冲区池
    
    管理不同大小的缓冲区，适合网络 I/O 场景。
    支持多种大小的缓冲区池。
    
    特点：
    - 多大小支持
    - 按需创建
    - 自动选择合适大小
    - 统计信息
    
    用法：
        pool = BufferPool()
        
        buf = pool.get(1024)  # 获取至少 1024 字节的缓冲区
        try:
            # 使用缓冲区
            n = socket.recv_into(buf)
            data = bytes(buf[:n])
        finally:
            pool.put(buf)
    """
    
    # 预定义的缓冲区大小等级
    SIZE_TIERS = [64, 256, 1024, 4096, 16384, 65536, 262144, 1048576]
    
    def __init__(self, max_buffers_per_tier: int = 32):
        """
        初始化缓冲区池
        
        Args:
            max_buffers_per_tier: 每个大小等级的最大缓冲区数量
        """
        self.max_buffers_per_tier = max_buffers_per_tier
        
        # 每个大小等级一个池
        self._pools: Dict[int, Deque[bytearray]] = {
            size: deque() for size in self.SIZE_TIERS
        }
        self._stats = {
            'gets': 0,
            'puts': 0,
            'creates': 0,
            'misses': 0
        }
        self._lock = threading.Lock()
    
    def _find_tier(self, size: int) -> int:
        """找到适合大小的等级"""
        for tier_size in self.SIZE_TIERS:
            if tier_size >= size:
                return tier_size
        # 超出最大等级，返回原大小
        return size
    
    def get(self, size: int) -> bytearray:
        """
        获取缓冲区
        
        Args:
            size: 需要的缓冲区大小
            
        Returns:
            至少包含 size 字节的缓冲区
        """
        if size <= 0:
            raise ValueError("大小必须为正数")
        
        tier = self._find_tier(size)
        
        with self._lock:
            self._stats['gets'] += 1
            
            if tier in self._pools and self._pools[tier]:
                # 命中现有池
                return self._pools[tier].popleft()
            
            # 没有可用缓冲区，创建新的
            self._stats['creates'] += 1
            self._stats['misses'] += 1
            
            # 如果不在预定义等级中，添加新等级
            if tier not in self._pools:
                self._pools[tier] = deque()
            
            return bytearray(tier)
    
    def put(self, buffer: bytearray) -> None:
        """
        放回缓冲区
        
        Args:
            buffer: 要放回的缓冲区
        """
        size = len(buffer)
        tier = self._find_tier(size)
        
        # 如果缓冲区大小不在等级中，找对应等级
        if size not in self._pools:
            tier = size
        
        with self._lock:
            self._stats['puts'] += 1
            
            # 只有在层级内且有对应池时才放回
            if tier in self._pools:
                pool = self._pools[tier]
                if len(pool) < self.max_buffers_per_tier:
                    # 清零后放回
                    buffer[:] = b'\x00' * len(buffer)
                    pool.append(buffer)
    
    @property
    def stats(self) -> Dict[str, int]:
        """获取统计信息"""
        with self._lock:
            return dict(self._stats)
    
    @property
    def total_buffers(self) -> int:
        """总缓冲区数量"""
        with self._lock:
            return sum(len(pool) for pool in self._pools.values())
    
    def clear(self) -> None:
        """清空所有缓冲区"""
        with self._lock:
            for pool in self._pools.values():
                pool.clear()


class ArenaAllocator:
    """
    Arena 分配器
    
    从大块内存中分配小块，支持批量释放。
    适合短生命周期对象的场景。
    
    特点：
    - 批量释放
    - 零碎片
    - 极快分配
    - 不支持单独释放
    
    用法：
        arena = ArenaAllocator(1024 * 1024)  # 1MB arena
        
        buf1 = arena.alloc(256)
        buf2 = arena.alloc(512)
        
        # 所有分配一起释放
        arena.reset()
    """
    
    def __init__(self, arena_size: int = 1024 * 1024):
        """
        初始化 Arena 分配器
        
        Args:
            arena_size: Arena 大小（字节）
        """
        if arena_size <= 0:
            raise ValueError("Arena 大小必须为正数")
        
        self.arena_size = arena_size
        self._arena = bytearray(arena_size)
        self._offset = 0
        self._allocations = 0
        self._lock = threading.Lock()
    
    def alloc(self, size: int, align: int = 1) -> bytearray:
        """
        分配内存
        
        Args:
            size: 需要的字节数
            align: 对齐字节数（默认 1）
            
        Returns:
            分配的内存视图
            
        Raises:
            MemoryError: Arena 空间不足
        """
        if size <= 0:
            raise ValueError("分配大小必须为正数")
        if align <= 0:
            raise ValueError("对齐必须为正数")
        
        with self._lock:
            # 计算对齐后的偏移
            aligned_offset = (self._offset + align - 1) // align * align
            
            if aligned_offset + size > self.arena_size:
                raise MemoryError(f"Arena 空间不足: 需要 {size} 字节，剩余 {self.arena_size - aligned_offset} 字节")
            
            self._offset = aligned_offset + size
            self._allocations += 1
            
            # 返回内存视图
            return memoryview(self._arena)[aligned_offset:self._offset]
    
    def reset(self) -> None:
        """重置 Arena，释放所有分配"""
        with self._lock:
            # 可选：清零内存
            # self._arena[:self._offset] = b'\x00' * self._offset
            self._offset = 0
            self._allocations = 0
    
    @property
    def used(self) -> int:
        """已使用字节数"""
        with self._lock:
            return self._offset
    
    @property
    def available(self) -> int:
        """可用字节数"""
        with self._lock:
            return self.arena_size - self._offset
    
    @property
    def utilization(self) -> float:
        """利用率（0-1）"""
        with self._lock:
            if self.arena_size == 0:
                return 0.0
            return self._offset / self.arena_size
    
    @property
    def allocations(self) -> int:
        """分配次数"""
        with self._lock:
            return self._allocations


class FixedSizeAllocator(BasePool[bytearray]):
    """
    固定大小块分配器
    
    管理固定大小的内存块，无碎片分配。
    适合需要频繁分配释放相同大小内存的场景。
    
    特点：
    - 零内存碎片
    - O(1) 分配和释放
    - 线程安全
    - 支持预分配
    
    用法：
        allocator = FixedSizeAllocator(256, 100)
        
        block = allocator.acquire()
        try:
            block[:] = data
            # 使用 block...
        finally:
            allocator.release(block)
    """
    
    def __init__(
        self,
        block_size: int,
        block_count: int,
        auto_expand: bool = False
    ):
        """
        初始化固定大小分配器
        
        Args:
            block_size: 每个块的大小（字节）
            block_count: 块数量
            auto_expand: 是否自动扩展
        """
        if block_size <= 0:
            raise ValueError("块大小必须为正数")
        if block_count <= 0:
            raise ValueError("块数量必须为正数")
        
        self.block_size = block_size
        self._auto_expand = auto_expand
        
        # 预分配独立的内存块，便于追踪
        self._blocks: List[bytearray] = [bytearray(block_size) for _ in range(block_count)]
        self._total_blocks = block_count
        
        # 空闲块索引
        self._free_blocks: Deque[int] = deque(range(block_count))
        self._allocated: Dict[int, int] = {}  # block_id -> block_index
        self._lock = threading.Lock()
    
    def acquire(self) -> bytearray:
        """获取一个内存块"""
        with self._lock:
            if not self._free_blocks:
                if self._auto_expand:
                    # 创建新块
                    block_index = self._total_blocks
                    self._blocks.append(bytearray(self.block_size))
                    self._total_blocks += 1
                else:
                    raise PoolExhaustedError("没有可用内存块")
            else:
                block_index = self._free_blocks.popleft()
            
            block = self._blocks[block_index]
            block_id = id(block)
            self._allocated[block_id] = block_index
            
            return block
    
    def release(self, obj: bytearray) -> None:
        """释放内存块"""
        with self._lock:
            block_id = id(obj)
            if block_id not in self._allocated:
                raise InvalidBlockError("此块不属于此分配器")
            
            block_index = self._allocated.pop(block_id)
            # 清零后放回
            obj[:] = b'\x00' * len(obj)
            self._free_blocks.append(block_index)
    
    @property
    def available(self) -> int:
        """可用块数量"""
        with self._lock:
            return len(self._free_blocks)
    
    @property
    def in_use(self) -> int:
        """正在使用的块数量"""
        with self._lock:
            return self._total_blocks - len(self._free_blocks)
    
    @property
    def total_blocks(self) -> int:
        """总块数量"""
        return self._total_blocks
    
    @property
    def utilization(self) -> float:
        """利用率（0-1）"""
        with self._lock:
            if self._total_blocks == 0:
                return 0.0
            return (self._total_blocks - len(self._free_blocks)) / self._total_blocks


class PooledObject(Generic[T]):
    """
    池化对象包装器
    
    自动管理对象的生命周期，支持上下文管理器。
    
    用法：
        with pool.pooled() as obj:
            obj.do_something()
        # 自动放回池中
    """
    
    def __init__(self, pool: ObjectPool[T], obj: T):
        self._pool = pool
        self._obj = obj
        self._released = False
    
    def __enter__(self) -> T:
        return self._obj
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
    
    def release(self) -> None:
        """手动释放对象"""
        if not self._released:
            self._pool.release(self._obj)
            self._released = True
    
    @property
    def obj(self) -> T:
        """获取原始对象"""
        if self._released:
            raise InvalidBlockError("对象已被释放")
        return self._obj


def with_pool(pool: ObjectPool[T]) -> PooledObject[T]:
    """
    创建池化对象的便捷函数
    
    用法：
        with with_pool(pool) as obj:
            obj.do_something()
    """
    return PooledObject(pool, pool.acquire())


# 示例类
class StringBuilder:
    """
    使用内存池的字符串构建器
    
    高效构建大量字符串。
    """
    
    def __init__(self, pool: Optional[MemoryPool] = None, chunk_size: int = 1024):
        self._pool = pool or MemoryPool(chunk_size)
        self._chunks: List[bytearray] = []
        self._current_chunk: Optional[bytearray] = None
        self._position = 0
    
    def append(self, text: str) -> 'StringBuilder':
        """追加文本"""
        data = text.encode('utf-8')
        remaining = len(data)
        offset = 0
        
        while remaining > 0:
            if self._current_chunk is None or self._position >= len(self._current_chunk):
                self._current_chunk = self._pool.acquire()
                self._chunks.append(self._current_chunk)
                self._position = 0
            
            chunk_remaining = len(self._current_chunk) - self._position
            copy_len = min(remaining, chunk_remaining)
            
            self._current_chunk[self._position:self._position + copy_len] = data[offset:offset + copy_len]
            
            self._position += copy_len
            offset += copy_len
            remaining -= copy_len
        
        return self
    
    def build(self) -> str:
        """构建最终字符串"""
        parts = []
        for chunk in self._chunks:
            if chunk is self._current_chunk:
                parts.append(chunk[:self._position].decode('utf-8'))
            else:
                parts.append(chunk.decode('utf-8'))
        return ''.join(parts)
    
    def clear(self) -> None:
        """清空并释放所有块"""
        for chunk in self._chunks:
            self._pool.release(chunk)
        self._chunks.clear()
        self._current_chunk = None
        self._position = 0
    
    def __str__(self) -> str:
        return self.build()


if __name__ == '__main__':
    # 简单演示
    print("=== MemoryPool 演示 ===")
    pool = MemoryPool(256, initial_blocks=4, max_blocks=8)
    print(f"初始状态: 可用={pool.available}, 使用中={pool.in_use}")
    
    blocks = []
    for i in range(5):
        block = pool.acquire()
        block[:10] = f"Block {i}".encode()
        blocks.append(block)
        print(f"获取块 {i}: 可用={pool.available}, 使用中={pool.in_use}")
    
    for i, block in enumerate(blocks):
        pool.release(block)
        print(f"释放块 {i}: 可用={pool.available}, 使用中={pool.in_use}")
    
    print("\n=== ObjectPool 演示 ===")
    
    class DemoObject:
        def __init__(self):
            self.value = 0
        
        def reset(self):
            self.value = 0
        
        def __repr__(self):
            return f"DemoObject(value={self.value})"
    
    obj_pool = ObjectPool(
        factory=DemoObject,
        reset=lambda obj: obj.reset(),
        initial_size=3
    )
    
    print(f"初始状态: 可用={obj_pool.available}, 使用中={obj_pool.in_use}")
    
    objs = [obj_pool.acquire() for _ in range(3)]
    print(f"获取 3 个对象: 可用={obj_pool.available}, 使用中={obj_pool.in_use}")
    
    for obj in objs:
        obj_pool.release(obj)
    print(f"释放所有对象: 可用={obj_pool.available}, 使用中={obj_pool.in_use}")
    
    print("\n=== BufferPool 演示 ===")
    buf_pool = BufferPool()
    buf = buf_pool.get(500)
    print(f"获取 500 字节缓冲区，实际大小: {len(buf)} 字节")
    buf_pool.put(buf)
    print(f"统计: {buf_pool.stats}")
    
    print("\n=== ArenaAllocator 演示 ===")
    arena = ArenaAllocator(1024)
    buf1 = arena.alloc(100)
    buf2 = arena.alloc(200)
    print(f"分配 100 + 200 字节: 已用={arena.used}, 可用={arena.available}, 分配次数={arena.allocations}")
    arena.reset()
    print(f"重置后: 已用={arena.used}, 可用={arena.available}")
    
    print("\n=== FixedSizeAllocator 演示 ===")
    allocator = FixedSizeAllocator(64, 5)
    blocks = [allocator.acquire() for _ in range(3)]
    print(f"获取 3 块: 可用={allocator.available}, 使用中={allocator.in_use}, 利用率={allocator.utilization:.2f}")
    for b in blocks:
        allocator.release(b)
    print(f"释放所有: 可用={allocator.available}, 使用中={allocator.in_use}")