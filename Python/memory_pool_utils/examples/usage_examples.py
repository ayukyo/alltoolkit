"""
Memory Pool Utils 使用示例

展示各种内存池工具的实际应用场景。
"""

import time
import threading
from typing import List

# 导入模块
import sys
sys.path.insert(0, '..')
from mod import (
    MemoryPool, ObjectPool, BufferPool, ArenaAllocator,
    FixedSizeAllocator, PooledObject, StringBuilder,
    PoolExhaustedError, with_pool
)


def example_memory_pool_basic():
    """
    MemoryPool 基本用法示例
    
    展示如何创建、使用和回收内存块。
    """
    print("=== MemoryPool 基本用法 ===\n")
    
    # 创建一个管理 256 字节块的内存池
    pool = MemoryPool(
        block_size=256,
        initial_blocks=10,
        max_blocks=100,
        auto_expand=True
    )
    
    print(f"初始状态: 可用={pool.available}, 使用中={pool.in_use}")
    print(f"总分配: {pool.total_allocated}, 利用率: {pool.utilization:.2%}")
    
    # 获取内存块
    blocks = []
    for i in range(5):
        block = pool.acquire()
        # 写入数据
        message = f"Block {i}: Hello, World!".encode()
        block[:len(message)] = message
        blocks.append(block)
        print(f"获取块 {i}: 写入 {len(message)} 字节")
    
    print(f"\n使用后: 可用={pool.available}, 使用中={pool.in_use}")
    
    # 读取数据
    for i, block in enumerate(blocks):
        # 找到数据长度（假设以空字节结束）
        data = bytes(block).rstrip(b'\x00')
        print(f"块 {i} 数据: {data.decode()}")
    
    # 释放内存块
    for block in blocks:
        pool.release(block)
    
    print(f"\n释放后: 可用={pool.available}, 使用中={pool.in_use}")
    print()


def example_object_pool_game():
    """
    ObjectPool 游戏开发示例
    
    展示如何在游戏开发中使用对象池管理游戏对象。
    """
    print("=== ObjectPool 游戏开发示例 ===\n")
    
    class Bullet:
        """子弹类"""
        def __init__(self):
            self.x = 0
            self.y = 0
            self.vx = 0
            self.vy = 0
            self.active = False
        
        def reset(self):
            """重置子弹状态"""
            self.x = 0
            self.y = 0
            self.vx = 0
            self.vy = 0
            self.active = False
        
        def fire(self, x: float, y: float, vx: float, vy: float):
            """发射子弹"""
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.active = True
        
        def update(self):
            """更新位置"""
            if self.active:
                self.x += self.vx
                self.y += self.vy
        
        def __repr__(self):
            status = "活跃" if self.active else "待机"
            return f"Bullet({status}) at ({self.x:.1f}, {self.y:.1f})"
    
    # 创建子弹池
    bullet_pool = ObjectPool(
        factory=Bullet,
        reset=lambda b: b.reset(),
        initial_size=20,
        max_size=50
    )
    
    print(f"子弹池初始状态: 可用={bullet_pool.available}")
    
    # 发射子弹
    active_bullets = []
    for i in range(5):
        bullet = bullet_pool.acquire()
        bullet.fire(0, 0, 10, 5 * i)
        active_bullets.append(bullet)
        print(f"发射子弹 {i}: {bullet}")
    
    print(f"\n发射后: 可用={bullet_pool.available}, 使用中={bullet_pool.in_use}")
    
    # 模拟游戏循环
    print("\n模拟 5 帧更新:")
    for frame in range(5):
        print(f"帧 {frame}:")
        for bullet in active_bullets:
            bullet.update()
            print(f"  {bullet}")
    
    # 子弹超出屏幕，回收
    print("\n回收子弹:")
    for bullet in active_bullets:
        print(f"  回收: {bullet}")
        bullet_pool.release(bullet)
    
    print(f"\n回收后: 可用={bullet_pool.available}, 使用中={bullet_pool.in_use}")
    print()


def example_buffer_pool_network():
    """
    BufferPool 网络 I/O 示例
    
    展示如何在网络编程中使用缓冲区池。
    """
    print("=== BufferPool 网络 I/O 示例 ===\n")
    
    # 创建缓冲区池
    buffer_pool = BufferPool(max_buffers_per_tier=16)
    
    print("BufferPool 自动选择合适的缓冲区大小:")
    
    # 模拟接收不同大小的数据
    data_sizes = [50, 200, 800, 3000, 10000, 50000]
    
    buffers = []
    for size in data_sizes:
        buf = buffer_pool.get(size)
        buffers.append(buf)
        print(f"请求 {size} 字节 -> 实际获取 {len(buf)} 字节缓冲区")
    
    print(f"\n统计信息: {buffer_pool.stats}")
    
    # 模拟处理数据后放回
    print("\n放回缓冲区:")
    for buf in buffers:
        buffer_pool.put(buf)
        print(f"  放回 {len(buf)} 字节缓冲区")
    
    print(f"\n总缓冲区数: {buffer_pool.total_buffers}")
    print(f"统计信息: {buffer_pool.stats}")
    print()


def example_arena_allocator_temp_objects():
    """
    ArenaAllocator 临时对象示例
    
    展示如何使用 Arena 分配器管理短生命周期对象。
    """
    print("=== ArenaAllocator 临时对象示例 ===\n")
    
    # 创建 1MB 的 Arena
    arena = ArenaAllocator(1024 * 1024)
    
    print(f"Arena 大小: {arena.arena_size} 字节 ({arena.arena_size / 1024} KB)")
    
    # 分配多个临时缓冲区
    print("\n分配临时对象:")
    
    # 解析 JSON 时需要的临时缓冲区
    json_buf = arena.alloc(500)
    print(f"  JSON 缓冲区: {len(json_buf)} 字节")
    
    # 解析结果存储
    result_buf = arena.alloc(200)
    print(f"  结果缓冲区: {len(result_buf)} 字节")
    
    # 临时字符串处理
    string_buf = arena.alloc(100, align=8)  # 8 字节对齐
    print(f"  字符串缓冲区: {len(string_buf)} 字节 (8字节对齐)")
    
    print(f"\n已用: {arena.used} 字节")
    print(f"可用: {arena.available} 字节")
    print(f"利用率: {arena.utilization:.2%}")
    print(f"分配次数: {arena.allocations}")
    
    # 处理完成后，一次性释放所有
    print("\n批量释放（重置 Arena）:")
    arena.reset()
    print(f"已用: {arena.used} 字节")
    print(f"可用: {arena.available} 字节")
    print()


def example_fixed_size_allocator_database():
    """
    FixedSizeAllocator 数据库缓存示例
    
    展示如何使用固定大小分配器管理数据库缓存页。
    """
    print("=== FixedSizeAllocator 数据库缓存示例 ===\n")
    
    # 创建管理 4KB 页的分配器（数据库常用页大小）
    allocator = FixedSizeAllocator(4096, 100, auto_expand=False)
    
    print(f"页大小: {allocator.block_size} 字节 (4 KB)")
    print(f"总页数: {allocator.total_blocks}")
    print(f"初始可用: {allocator.available}")
    
    # 模拟数据库缓存
    class PageCache:
        def __init__(self, allocator):
            self._allocator = allocator
            self._pages: dict = {}  # page_id -> buffer
        
        def get_page(self, page_id: int) -> bytes:
            """获取页面"""
            if page_id not in self._pages:
                # 从磁盘加载（模拟）
                buf = self._allocator.acquire()
                # 模拟数据
                buf[:100] = f"Page {page_id} data".encode()
                self._pages[page_id] = buf
            return self._pages[page_id]
        
        def release_page(self, page_id: int):
            """释放页面"""
            if page_id in self._pages:
                self._allocator.release(self._pages.pop(page_id))
        
        def stats(self):
            return {
                'cached': len(self._pages),
                'available': self._allocator.available
            }
    
    cache = PageCache(allocator)
    
    print("\n加载页面:")
    for page_id in [1, 2, 3, 5, 10]:
        buf = cache.get_page(page_id)
        data = bytes(buf[:100]).rstrip(b'\x00').decode()
        print(f"  页 {page_id}: {data}")
        print(f"  可用页: {allocator.available}")
    
    print(f"\n缓存统计: {cache.stats()}")
    print(f"利用率: {allocator.utilization:.2%}")
    
    # 释放一些页面
    print("\n释放页面 1 和 2:")
    cache.release_page(1)
    cache.release_page(2)
    print(f"  可用页: {allocator.available}")
    
    print()


def example_string_builder():
    """
    StringBuilder 示例
    
    展示如何使用池化的字符串构建器。
    """
    print("=== StringBuilder 示例 ===\n")
    
    # 创建内存池
    pool = MemoryPool(128, initial_blocks=20)
    
    # 创建字符串构建器
    sb = StringBuilder(pool, chunk_size=128)
    
    print("使用 StringBuilder 构建长字符串:")
    
    # 链式追加
    sb.append("标题: ").append("AllToolkit 使用指南\n")
    sb.append("作者: ").append("OpenClaw Team\n")
    sb.append("日期: ").append("2026-05-11\n")
    sb.append("\n章节列表:\n")
    
    for i in range(1, 6):
        sb.append(f"  {i}. 章节 {i}\n")
    
    # 构建最终字符串
    result = sb.build()
    print(result)
    
    print(f"内存块使用: {pool.in_use}")
    
    # 清空并释放内存
    sb.clear()
    print(f"清空后可用块: {pool.available}")
    print()


def example_pooled_object_context():
    """
    PooledObject 上下文管理器示例
    
    展示如何使用上下文管理器自动管理池化对象。
    """
    print("=== PooledObject 上下文管理器示例 ===\n")
    
    class DatabaseConnection:
        """模拟数据库连接"""
        def __init__(self):
            self.connected = False
            self.query_count = 0
        
        def connect(self):
            self.connected = True
            print("  连接已建立")
        
        def disconnect(self):
            self.connected = False
            print("  连接已关闭")
        
        def execute(self, query: str):
            if self.connected:
                self.query_count += 1
                print(f"  执行查询: {query}")
        
        def reset(self):
            """重置连接状态"""
            self.disconnect()
            self.query_count = 0
    
    # 创建连接池
    conn_pool = ObjectPool(
        factory=DatabaseConnection,
        reset=lambda c: c.reset(),
        initial_size=3
    )
    
    print("使用上下文管理器自动管理连接:")
    
    # 使用 with_pool 函数
    with with_pool(conn_pool) as conn:
        conn.connect()
        conn.execute("SELECT * FROM users")
        conn.execute("SELECT * FROM products")
        print(f"  查询次数: {conn.query_count}")
    
    print(f"\n连接已自动放回池中")
    print(f"可用连接: {conn_pool.available}")
    
    print("\n使用 PooledObject 包装器:")
    
    wrapped = PooledObject(conn_pool, conn_pool.acquire())
    wrapped.obj.connect()
    wrapped.obj.execute("SELECT COUNT(*) FROM orders")
    
    # 手动释放
    wrapped.release()
    print(f"手动释放后可用连接: {conn_pool.available}")
    print()


def example_high_performance_web_server():
    """
    高性能 Web 服务器示例
    
    展示如何在 Web 服务器场景中综合使用各种内存池。
    """
    print("=== 高性能 Web 服务器模拟 ===\n")
    
    # 创建各种池
    request_buffer_pool = BufferPool(max_buffers_per_tier=32)
    response_pool = MemoryPool(4096, initial_blocks=50, max_blocks=200, auto_expand=True)
    
    # 模拟处理请求
    class RequestHandler:
        def __init__(self, buf_pool, resp_pool):
            self._buf_pool = buf_pool
            self._resp_pool = resp_pool
        
        def handle_request(self, request_data: bytes) -> bytes:
            """处理请求"""
            # 获取请求缓冲区
            buf = self._buf_pool.get(len(request_data))
            
            # 获取响应缓冲区
            resp = self._resp_pool.acquire()
            
            # 处理请求（模拟）
            buf[:len(request_data)] = request_data
            response = f"Response: {len(request_data)} bytes processed".encode()
            resp[:len(response)] = response
            
            # 放回请求缓冲区
            self._buf_pool.put(buf)
            
            # 返回响应数据
            result = bytes(resp[:len(response)])
            self._resp_pool.release(resp)
            
            return result
    
    handler = RequestHandler(request_buffer_pool, response_pool)
    
    print("模拟处理 10 个请求:")
    start_time = time.time()
    
    for i in range(10):
        # 模拟不同大小的请求
        request_size = 100 * (i + 1)
        request_data = f"Request {i}".encode() + b'\x00' * (request_size - 10)
        
        response = handler.handle_request(request_data)
        print(f"  请求 {i}: {response.decode()}")
    
    elapsed = time.time() - start_time
    print(f"\n处理时间: {elapsed:.3f} 秒")
    
    print(f"\n缓冲区池统计: {request_buffer_pool.stats}")
    print(f"响应池统计: 可用={response_pool.available}, 使用中={response_pool.in_use}")
    print()


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("Memory Pool Utils 使用示例")
    print("=" * 60)
    print()
    
    example_memory_pool_basic()
    example_object_pool_game()
    example_buffer_pool_network()
    example_arena_allocator_temp_objects()
    example_fixed_size_allocator_database()
    example_string_builder()
    example_pooled_object_context()
    example_high_performance_web_server()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()