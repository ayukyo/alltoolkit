"""
cache_utils 高级用法示例

演示：
- TimedCache 时间窗口缓存
- MultiLevelCache 多级缓存
- CacheManager 缓存管理器
- 线程安全缓存
"""

import time
import threading
from mod import (
    MemoryCache, TimedCache, MultiLevelCache, 
    CacheManager, create_cache
)


def timed_cache_example():
    """时间窗口缓存示例"""
    print("=== 时间窗口缓存 ===\n")
    
    cache = TimedCache(window_seconds=2)
    fetch_count = 0
    
    def fetch_latest_price():
        nonlocal fetch_count
        fetch_count += 1
        print(f"  [数据源] 获取最新价格 #{fetch_count}")
        return {'price': 100 + fetch_count, 'time': time.time()}
    
    print("第一次获取:")
    data1 = cache.get_or_refresh('btc_price', fetch_latest_price)
    print(f"  价格: {data1['price']}")
    
    print("\n立即再次获取 (窗口内，不刷新):")
    data2 = cache.get_or_refresh('btc_price', fetch_latest_price)
    print(f"  价格: {data2['price']}")
    print(f"  相同数据: {data1 == data2}")
    
    print("\n等待 2.5 秒...")
    time.sleep(2.5)
    
    print("窗口后获取 (刷新数据):")
    data3 = cache.get_or_refresh('btc_price', fetch_latest_price)
    print(f"  价格: {data3['price']}")
    
    print("\n手动失效后获取:")
    cache.invalidate('btc_price')
    data4 = cache.get_or_refresh('btc_price', fetch_latest_price)
    print(f"  价格: {data4['price']}")
    
    print()


def multi_level_cache_example():
    """多级缓存示例"""
    print("=== 多级缓存 (模拟 L1内存 + L2Redis) ===\n")
    
    # 模拟 L2 存储（如 Redis）
    l2_storage = {}
    l2_get_count = 0
    l2_set_count = 0
    
    def l2_get(key):
        nonlocal l2_get_count
        l2_get_count += 1
        print(f"  [L2 Redis] GET {key}")
        return l2_storage.get(key)
    
    def l2_set(key, value, ttl=None):
        nonlocal l2_set_count
        l2_set_count += 1
        print(f"  [L2 Redis] SET {key} (ttl={ttl})")
        l2_storage[key] = value
    
    def l2_delete(key):
        print(f"  [L2 Redis] DEL {key}")
        if key in l2_storage:
            del l2_storage[key]
            return True
        return False
    
    # 创建多级缓存
    cache = MultiLevelCache(l1_size=100, l1_ttl=5)
    cache.set_l2_handlers(l2_get, l2_set, l2_delete)
    
    print("场景1: 直接设置 (写入 L1 和 L2)")
    cache.set('user:1', {'name': 'Alice'})
    print(f"  L1: {cache._l1.get('user:1')}")
    print(f"  L2: {l2_storage.get('user:1')}")
    
    print("\n场景2: 从 L1 获取 (命中)")
    result = cache.get('user:1')
    print(f"  结果: {result}")
    
    print("\n场景3: 清除 L1 后从 L2 获取 (回填)")
    cache._l1.clear()
    print(f"  L1 清除后: {cache._l1.get('user:1')}")
    result = cache.get('user:1')
    print(f"  从缓存获取: {result}")
    print(f"  L1 回填: {cache._l1.get('user:1')}")
    
    print("\n场景4: 删除 (同时删除 L1 和 L2)")
    cache.delete('user:1')
    print(f"  L1: {cache._l1.get('user:1')}")
    print(f"  L2: {l2_storage.get('user:1')}")
    
    print(f"\n统计:")
    print(f"  L2 GET 次数: {l2_get_count}")
    print(f"  L2 SET 次数: {l2_set_count}")
    
    print()


def cache_manager_example():
    """缓存管理器示例"""
    print("=== 缓存管理器 ===\n")
    
    # 获取单例管理器
    manager = CacheManager()
    manager.clear_all()  # 清除之前的缓存
    
    print("创建多个命名缓存:")
    user_cache = manager.get_cache('users', max_size=100, default_ttl=300)
    product_cache = manager.get_cache('products', max_size=500, default_ttl=600)
    session_cache = manager.get_cache('sessions', max_size=1000, default_ttl=1800)
    
    # 使用各个缓存
    user_cache.set('user:1', {'name': 'Alice'})
    user_cache.set('user:2', {'name': 'Bob'})
    user_cache.get('user:1')
    user_cache.get('user:3')  # 未命中
    
    product_cache.set('prod:1', {'name': 'Laptop'})
    product_cache.get('prod:1')
    product_cache.get('prod:1')
    product_cache.get('prod:2')  # 未命中
    
    print("各缓存统计:")
    stats = manager.get_all_stats()
    for name, stat in stats.items():
        print(f"\n  [{name}]")
        print(f"    命中: {stat['hits']}")
        print(f"    未命中: {stat['misses']}")
        print(f"    命中率: {stat['hit_rate']:.2%}")
    
    print("\n清空所有缓存...")
    manager.clear_all()
    
    print(f"user_cache 大小: {user_cache.size()}")
    print(f"product_cache 大小: {product_cache.size()}")
    
    print("\n删除特定缓存...")
    manager.remove_cache('sessions')
    stats = manager.get_all_stats()
    print(f"剩余缓存: {list(stats.keys())}")
    
    print()


def thread_safe_example():
    """线程安全缓存示例"""
    print("=== 线程安全缓存 ===\n")
    
    cache = MemoryCache(max_size=1000, thread_safe=True)
    errors = []
    
    def writer(thread_id):
        try:
            for i in range(100):
                key = f"thread_{thread_id}_key_{i}"
                cache.set(key, f"value_{i}")
        except Exception as e:
            errors.append((thread_id, str(e)))
    
    def reader(thread_id):
        try:
            for i in range(100):
                key = f"thread_{i % 10}_key_{i % 100}"
                cache.get(key)
        except Exception as e:
            errors.append((thread_id, str(e)))
    
    print("启动 5 个写线程和 5 个读线程...")
    threads = []
    for i in range(5):
        threads.append(threading.Thread(target=writer, args=(i,)))
        threads.append(threading.Thread(target=reader, args=(i,)))
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"并发操作完成")
    print(f"错误数: {len(errors)}")
    print(f"最终缓存大小: {cache.size()}")
    
    stats = cache.get_stats()
    print(f"统计:")
    print(f"  命中: {stats.hits}")
    print(f"  未命中: {stats.misses}")
    print(f"  淘汰: {stats.evictions}")
    
    print()


def rate_limiting_example():
    """限流计数器示例"""
    print("=== API 限流示例 ===\n")
    
    # 使用缓存实现简单的 API 限流
    rate_cache = MemoryCache(max_size=10000)
    
    def check_rate_limit(client_id, limit=100, window=60):
        """
        检查 API 限流
        
        Args:
            client_id: 客户端标识
            limit: 窗口内最大请求数
            window: 时间窗口（秒）
        
        Returns:
            (allowed, remaining, reset_time)
        """
        key = f"rate:{client_id}"
        
        entry = rate_cache._cache.get(key)
        now = time.time()
        
        if entry is None or entry.is_expired() or (now - entry.created_at) > window:
            # 新窗口
            rate_cache.set(key, 1, ttl=window)
            return True, limit - 1, window
        
        # 现有窗口
        count = entry.value
        if count >= limit:
            remaining_time = window - (now - entry.created_at)
            return False, 0, remaining_time
        
        # 增加计数
        rate_cache.set(key, count + 1, ttl=entry.remaining_ttl())
        return True, limit - count - 1, entry.remaining_ttl()
    
    print("模拟客户端请求:")
    client = "client_123"
    
    for i in range(12):
        allowed, remaining, reset = check_rate_limit(client, limit=10, window=5)
        status = "✓ 允许" if allowed else "✗ 拒绝"
        print(f"  请求 {i+1}: {status} (剩余: {remaining}, 重置: {reset:.1f}s)")
    
    print()


def session_cache_example():
    """会话缓存示例"""
    print("=== 会话缓存示例 ===\n")
    
    session_cache = MemoryCache(max_size=1000, default_ttl=1800)  # 30分钟
    
    def create_session(user_id):
        """创建会话"""
        session_id = f"session_{user_id}_{int(time.time())}"
        session_data = {
            'user_id': user_id,
            'created_at': time.time(),
            'data': {}
        }
        session_cache.set(session_id, session_data)
        return session_id
    
    def get_session(session_id):
        """获取会话"""
        return session_cache.get(session_id)
    
    def update_session(session_id, data):
        """更新会话"""
        session = session_cache.get(session_id)
        if session:
            session['data'].update(data)
            session_cache.set(session_id, session)
            return True
        return False
    
    def destroy_session(session_id):
        """销毁会话"""
        return session_cache.delete(session_id)
    
    # 创建会话
    print("创建用户会话...")
    session_id = create_session('user_123')
    print(f"  Session ID: {session_id}")
    
    # 获取会话
    session = get_session(session_id)
    print(f"  会话数据: {session}")
    
    # 更新会话
    print("\n更新会话...")
    update_session(session_id, {'cart': ['item1', 'item2'], 'theme': 'dark'})
    session = get_session(session_id)
    print(f"  更新后: {session}")
    
    # 销毁会话
    print("\n销毁会话...")
    destroy_session(session_id)
    session = get_session(session_id)
    print(f"  销毁后: {session}")
    
    print()


def cleanup_schedule_example():
    """定期清理示例"""
    print("=== 定期清理过期条目 ===\n")
    
    cache = MemoryCache(max_size=100)
    
    # 添加一些短期数据
    for i in range(10):
        cache.set(f"temp_{i}", f"value_{i}", ttl=1 + i * 0.1)
    
    print(f"初始大小: {cache.size()}")
    
    # 模拟定期清理
    print("\n等待 2 秒后清理...")
    time.sleep(2)
    
    cleaned = cache.cleanup_expired()
    print(f"清理了 {cleaned} 个过期条目")
    print(f"剩余大小: {cache.size()}")
    
    stats = cache.get_stats()
    print(f"过期次数: {stats.expirations}")
    
    print()


if __name__ == '__main__':
    timed_cache_example()
    multi_level_cache_example()
    cache_manager_example()
    thread_safe_example()
    rate_limiting_example()
    session_cache_example()
    cleanup_schedule_example()
    
    print("示例完成！")