"""
AllToolkit - Object Pool Utilities 使用示例

本文件展示 object_pool_utils 模块的各种使用场景。
"""

import sys
import os
import time
import threading
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    ObjectPool, ConnectionPool, PoolManager,
    create_pool, create_connection_pool,
    PooledStringBuilder, PooledList, PooledDict
)


def example_basic_pool():
    """示例 1: 基本对象池"""
    print("=" * 60)
    print("示例 1: 基本对象池")
    print("=" * 60)
    
    # 定义对象工厂
    def create_expensive_object():
        """模拟创建开销较大的对象"""
        time.sleep(0.01)  # 模拟昂贵初始化
        return {
            'id': id(object()),
            'created_at': time.time(),
            'data': []
        }
    
    # 创建对象池
    pool = ObjectPool(
        factory=create_expensive_object,
        max_size=5,
        min_idle=1
    )
    
    print(f"池状态: {pool}")
    
    # 借用对象
    obj1 = pool.borrow()
    print(f"借用对象 1: id={obj1['id']}")
    print(f"池状态: {pool}")
    
    # 再借用一个
    obj2 = pool.borrow()
    print(f"借用对象 2: id={obj2['id']}")
    print(f"池状态: {pool}")
    
    # 归还对象
    pool.return_object(obj1)
    print("归还对象 1")
    print(f"池状态: {pool}")
    
    # 再次借用 - 应该复用对象 1
    obj3 = pool.borrow()
    print(f"借用对象 3: id={obj3['id']}")
    print(f"对象 3 与对象 1 相同: {obj3 is obj1}")
    
    pool.return_object(obj2)
    pool.return_object(obj3)
    pool.close()
    print()


def example_context_manager():
    """示例 2: 使用上下文管理器"""
    print("=" * 60)
    print("示例 2: 使用上下文管理器")
    print("=" * 60)
    
    pool = ObjectPool(
        factory=lambda: {'count': 0},
        max_size=3
    )
    
    # 使用 with 语句自动归还对象
    print("使用 pool.use() 上下文管理器:")
    with pool.use() as obj:
        obj['count'] += 1
        print(f"  对象计数: {obj['count']}")
        print(f"  池状态: {pool}")
    
    print(f"退出上下文后池状态: {pool}")
    
    # 池本身也可以作为上下文管理器
    print("\n池作为上下文管理器:")
    with ObjectPool(factory=lambda: {'value': 42}) as p:
        with p.use() as obj:
            print(f"  对象值: {obj['value']}")
    print("  池已自动关闭")
    print()


def example_validation():
    """示例 3: 对象验证"""
    print("=" * 60)
    print("示例 3: 对象验证")
    print("=" * 60)
    
    def create_connection():
        return {'connected': True, 'queries': 0}
    
    def is_valid(conn):
        """检查连接是否有效"""
        return conn.get('connected', False)
    
    def reset_connection(conn):
        """重置连接状态"""
        conn['queries'] = 0
    
    pool = ObjectPool(
        factory=create_connection,
        validator=is_valid,
        reset=reset_connection,
        max_size=3,
        validation_on_borrow=True,
        reset_on_return=True
    )
    
    # 借用并使用连接
    conn = pool.borrow()
    print(f"借用连接: connected={conn['connected']}")
    
    # 模拟使用
    conn['queries'] += 1
    conn['queries'] += 1
    print(f"执行查询后: queries={conn['queries']}")
    
    # 模拟连接断开
    conn['connected'] = False
    print("模拟连接断开")
    
    # 归还连接
    pool.return_object(conn)
    print("归还连接 (会自动重置)")
    
    # 再次借用 - 会验证并发现连接无效，创建新连接
    conn2 = pool.borrow()
    print(f"借用新连接: connected={conn2['connected']}")
    print(f"查询计数已重置: queries={conn2['queries']}")
    
    pool.return_object(conn2)
    pool.close()
    print()


def example_destructor():
    """示例 4: 对象销毁器"""
    print("=" * 60)
    print("示例 4: 对象销毁器")
    print("=" * 60)
    
    class Resource:
        def __init__(self, name):
            self.name = name
            self.closed = False
            print(f"  创建资源: {name}")
        
        def close(self):
            self.closed = True
            print(f"  关闭资源: {self.name}")
    
    resources = []
    counter = [0]
    
    def factory():
        counter[0] += 1
        r = Resource(f"Resource-{counter[0]}")
        resources.append(r)
        return r
    
    def destructor(r):
        r.close()
    
    pool = ObjectPool(
        factory=factory,
        destructor=destructor,
        max_size=3
    )
    
    r1 = pool.borrow()
    r2 = pool.borrow()
    
    print("\n清理池:")
    pool.clear()  # 清理空闲对象
    print(f"池状态: {pool}")
    
    print("\n关闭池:")
    pool.close()
    print()


def example_connection_pool():
    """示例 5: 连接池"""
    print("=" * 60)
    print("示例 5: 连接池")
    print("=" * 60)
    
    class MockConnection:
        def __init__(self, conn_id):
            self.id = conn_id
            self.alive = True
            self.query_count = 0
            print(f"  创建连接 {conn_id}")
        
        def execute(self, query):
            if not self.alive:
                raise Exception("Connection is dead")
            self.query_count += 1
            return f"Result of: {query}"
        
        def close(self):
            self.alive = False
            print(f"  关闭连接 {self.id}")
    
    counter = [0]
    
    def create_connection():
        counter[0] += 1
        return MockConnection(counter[0])
    
    def validate_connection(conn):
        return conn.alive
    
    pool = ConnectionPool(
        factory=create_connection,
        destructor=lambda c: c.close(),
        validator=validate_connection,
        max_size=5,
        min_idle=1,
        max_lifetime=3600,  # 1小时最大生命周期
        max_usage_count=1000  # 最多使用1000次
    )
    
    print("执行查询:")
    with pool.use() as conn:
        result = conn.execute("SELECT * FROM users")
        print(f"  结果: {result}")
        print(f"  连接 ID: {conn.id}")
    
    print(f"\n池状态: {pool}")
    
    # 健康检查
    print("\n健康检查:")
    health = pool.health_check()
    print(f"  健康: {health['healthy']}")
    print(f"  不健康: {health['unhealthy']}")
    
    pool.close()
    print()


def example_pool_manager():
    """示例 6: 池管理器"""
    print("=" * 60)
    print("示例 6: 池管理器")
    print("=" * 60)
    
    manager = PoolManager()
    
    # 创建不同类型的池
    manager.create_pool(
        'database',
        factory=lambda: {'type': 'db', 'connected': True},
        max_size=10
    )
    
    manager.create_pool(
        'cache',
        factory=lambda: {'type': 'cache', 'hits': 0},
        max_size=20
    )
    
    manager.create_pool(
        'http',
        factory=lambda: {'type': 'http', 'requests': 0},
        max_size=5
    )
    
    print("创建的池:")
    for name in ['database', 'cache', 'http']:
        pool = manager.get_pool(name)
        print(f"  {name}: {pool}")
    
    # 使用不同池
    print("\n使用池:")
    with manager.use('database') as db:
        print(f"  数据库连接: {db['type']}")
    
    with manager.use('cache') as cache:
        cache['hits'] += 1
        print(f"  缓存连接: {cache['type']}, hits={cache['hits']}")
    
    # 获取所有统计
    print("\n所有池统计:")
    all_stats = manager.get_all_stats()
    for name, stats in all_stats.items():
        print(f"  {name}: created={stats.total_created}, borrowed={stats.total_borrowed}")
    
    manager.close_all()
    print()


def example_thread_safety():
    """示例 7: 线程安全"""
    print("=" * 60)
    print("示例 7: 线程安全")
    print("=" * 60)
    
    pool = ObjectPool(
        factory=lambda: {'value': 0, 'operations': 0},
        max_size=5
    )
    
    results = []
    lock = threading.Lock()
    
    def worker(worker_id, iterations):
        for i in range(iterations):
            with pool.use() as obj:
                obj['value'] += 1
                obj['operations'] += 1
                time.sleep(0.0001)  # 模拟工作
            with lock:
                results.append((worker_id, i))
    
    threads = []
    num_threads = 5
    iterations = 20
    
    print(f"启动 {num_threads} 个线程, 每个执行 {iterations} 次操作...")
    
    start = time.time()
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i, iterations))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    
    print(f"完成 {len(results)} 次操作")
    print(f"耗时: {elapsed*1000:.2f}ms")
    
    stats = pool.get_stats()
    print(f"池统计:")
    print(f"  总借用次数: {stats.total_borrowed}")
    print(f"  总归还次数: {stats.total_returned}")
    print(f"  最大并发借用: {stats.max_borrowed_at_once}")
    
    pool.close()
    print()


def example_statistics():
    """示例 8: 统计信息"""
    print("=" * 60)
    print("示例 8: 统计信息")
    print("=" * 60)
    
    pool = ObjectPool(
        factory=lambda: {'id': id(object())},
        max_size=5,
        min_idle=2
    )
    
    # 执行一些操作
    obj1 = pool.borrow()
    obj2 = pool.borrow()
    obj3 = pool.borrow()
    
    pool.return_object(obj1)
    pool.return_object(obj2)
    
    stats = pool.get_stats()
    print("池统计:")
    print(f"  创建对象数: {stats.total_created}")
    print(f"  借用次数: {stats.total_borrowed}")
    print(f"  归还次数: {stats.total_returned}")
    print(f"  当前空闲: {stats.current_idle}")
    print(f"  当前活跃: {stats.current_active}")
    print(f"  最大并发借用: {stats.max_borrowed_at_once}")
    print(f"  利用率: {stats.utilization_rate:.2%}")
    print(f"  平均等待时间: {stats.avg_wait_time_ms:.4f}ms")
    
    print(f"\n统计字典:")
    for key, value in stats.to_dict().items():
        print(f"  {key}: {value}")
    
    pool.return_object(obj3)
    pool.close()
    print()


def example_idle_eviction():
    """示例 9: 空闲对象驱逐"""
    print("=" * 60)
    print("示例 9: 空闲对象驱逐")
    print("=" * 60)
    
    def factory():
        print("  创建新对象...")
        return {'id': id(object())}
    
    def destructor(obj):
        print(f"  销毁对象 {obj['id']}")
    
    pool = ObjectPool(
        factory=factory,
        destructor=destructor,
        max_size=5,
        max_idle_time=0.2,  # 200ms
        min_idle=0
    )
    
    print("借用并归还对象:")
    obj = pool.borrow()
    pool.return_object(obj)
    print(f"池状态: {pool}")
    
    print("\n等待空闲对象过期...")
    time.sleep(0.3)
    
    print("手动触发驱逐:")
    evicted = pool.evict_idle_objects()
    print(f"驱逐了 {evicted} 个对象")
    print(f"池状态: {pool}")
    
    pool.close()
    print()


def example_pooled_resources():
    """示例 10: 预定义的可池化资源"""
    print("=" * 60)
    print("示例 10: 预定义的可池化资源")
    print("=" * 60)
    
    # 使用 PooledStringBuilder
    print("PooledStringBuilder:")
    sb = PooledStringBuilder()
    for word in ["Hello", " ", "World", "!"]:
        sb.append(word)
    print(f"  结果: {sb.build()}")
    sb.clear()
    print(f"  清空后: '{sb.build()}'")
    
    # 使用池化的 StringBuilder
    print("\n池化 StringBuilder:")
    pool = ObjectPool(
        factory=lambda: PooledStringBuilder(256),
        reset=lambda sb: sb.clear(),
        max_size=3
    )
    
    with pool.use() as sb:
        sb.append("使用池化的 StringBuilder")
        sb.append(" 更高效!")
        print(f"  结果: {sb.build()}")
    
    print(f"池状态: {pool}")
    
    # 再次使用 - 已清空
    with pool.use() as sb:
        sb.append("新消息")
        print(f"  结果: {sb.build()}")
    
    # PooledList
    print("\nPooledList:")
    pl = PooledList()
    pl.extend([1, 2, 3, 4, 5])
    print(f"  内容: {list(pl)}")
    pl.reset()
    print(f"  重置后: {list(pl)}")
    
    # PooledDict
    print("\nPooledDict:")
    pd = PooledDict()
    pd.update({'a': 1, 'b': 2, 'c': 3})
    print(f"  内容: {dict(pd)}")
    pd.reset()
    print(f"  重置后: {dict(pd)}")
    
    pool.close()
    print()


def example_convenience_functions():
    """示例 11: 便捷函数"""
    print("=" * 60)
    print("示例 11: 便捷函数")
    print("=" * 60)
    
    # create_pool
    pool = create_pool(
        factory=lambda: {'id': id(object())},
        max_size=5
    )
    print(f"create_pool 创建的池: {pool}")
    pool.close()
    
    # create_connection_pool
    conn_pool = create_connection_pool(
        factory=lambda: {'connected': True, 'id': id(object())},
        validator=lambda c: c.get('connected', False),
        max_size=3
    )
    print(f"create_connection_pool 创建的连接池: {conn_pool}")
    conn_pool.close()
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Object Pool Utilities - 使用示例")
    print("=" * 60 + "\n")
    
    example_basic_pool()
    example_context_manager()
    example_validation()
    example_destructor()
    example_connection_pool()
    example_pool_manager()
    example_thread_safety()
    example_statistics()
    example_idle_eviction()
    example_pooled_resources()
    example_convenience_functions()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()