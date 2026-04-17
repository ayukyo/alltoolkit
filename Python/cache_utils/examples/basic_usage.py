"""
cache_utils 基本用法示例

演示：
- 基本的缓存读写操作
- TTL 过期机制
- LRU 淘汰策略
- 缓存统计
"""

import time
from mod import MemoryCache, create_cache


def basic_operations():
    """基本操作示例"""
    print("=== 基本操作 ===\n")
    
    cache = MemoryCache()
    
    # 设置值
    cache.set('name', 'Alice')
    cache.set('age', 30)
    cache.set('active', True)
    
    # 获取值
    print(f"name: {cache.get('name')}")
    print(f"age: {cache.get('age')}")
    print(f"active: {cache.get('active')}")
    
    # 不存在的键
    print(f"missing: {cache.get('missing', '默认值')}")
    
    # 删除
    cache.delete('active')
    print(f"删除后 active: {cache.get('active')}")
    
    # 字典接口
    cache['city'] = 'Beijing'
    print(f"city: {cache['city']}")
    print(f"是否包含 name: {'name' in cache}")
    
    print()


def ttl_example():
    """TTL 过期示例"""
    print("=== TTL 过期示例 ===\n")
    
    cache = MemoryCache(default_ttl=2)  # 默认2秒过期
    
    cache.set('temp', '临时数据')
    cache.set('permanent', '永久数据', ttl=None)
    cache.set('short', '短数据', ttl=1)
    
    print("初始状态:")
    print(f"  temp: {cache.get('temp')}")
    print(f"  permanent: {cache.get('permanent')}")
    print(f"  short: {cache.get('short')}")
    
    print("\n等待 1.5 秒...")
    time.sleep(1.5)
    
    print("1.5秒后:")
    print(f"  temp: {cache.get('temp')}")
    print(f"  permanent: {cache.get('permanent')}")
    print(f"  short: {cache.get('short')}")  # 已过期
    
    print("\n等待 1 秒...")
    time.sleep(1)
    
    print("2.5秒后:")
    print(f"  temp: {cache.get('temp')}")  # 已过期
    print(f"  permanent: {cache.get('permanent')}")
    
    print()


def lru_example():
    """LRU 淘汰示例"""
    print("=== LRU 淘汰示例 ===\n")
    
    cache = MemoryCache(max_size=3)
    
    print("添加 a, b, c:")
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 3)
    print(f"  缓存: {cache.get_all_keys()}")
    
    print("\n访问 'a' 使其成为最近使用:")
    cache.get('a')
    print(f"  缓存: {cache.get_all_keys()}")
    
    print("\n添加 'd'，应淘汰最久未使用的 'b':")
    cache.set('d', 4)
    print(f"  缓存: {cache.get_all_keys()}")
    print(f"  'a' 存在: {cache.exists('a')}")
    print(f"  'b' 存在: {cache.exists('b')}")
    
    stats = cache.get_stats()
    print(f"\n淘汰次数: {stats.evictions}")
    
    print()


def stats_example():
    """统计信息示例"""
    print("=== 统计信息示例 ===\n")
    
    cache = create_cache(max_size=10, ttl=60)
    
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    
    # 命中
    cache.get('key1')
    cache.get('key1')
    cache.get('key2')
    
    # 未命中
    cache.get('missing1')
    cache.get('missing2')
    
    stats = cache.get_stats()
    print(f"命中次数: {stats.hits}")
    print(f"未命中次数: {stats.misses}")
    print(f"总请求: {stats.total_requests}")
    print(f"命中率: {stats.hit_rate:.2%}")
    print(f"\n完整统计: {stats.to_dict()}")
    
    # 重置
    stats.reset()
    print(f"\n重置后命中次数: {stats.hits}")
    
    print()


def get_or_set_example():
    """get_or_set 示例"""
    print("=== get_or_set 示例 ===\n")
    
    cache = MemoryCache(ttl=30)
    call_count = 0
    
    def fetch_data(key):
        nonlocal call_count
        call_count += 1
        print(f"  [模拟数据库查询] key={key}, 调用次数={call_count}")
        return f"data_for_{key}"
    
    print("第一次获取 'user:1':")
    result1 = cache.get_or_set('user:1', lambda: fetch_data('user:1'))
    print(f"  结果: {result1}")
    
    print("\n第二次获取 'user:1' (应该命中缓存):")
    result2 = cache.get_or_set('user:1', lambda: fetch_data('user:1'))
    print(f"  结果: {result2}")
    print(f"  总查询次数: {call_count}")
    
    print()


def entries_info_example():
    """条目详情示例"""
    print("=== 条目详情示例 ===\n")
    
    cache = MemoryCache(ttl=60)
    
    cache.set('user:1', {'name': 'Alice'})
    cache.set('user:2', {'name': 'Bob'})
    
    # 访问一次
    cache.get('user:1')
    
    info = cache.get_entries_info()
    for entry in info:
        print(f"键: {entry['key']}")
        print(f"  创建时间: {entry['created_at']:.2f}")
        print(f"  最后访问: {entry['last_access']:.2f}")
        print(f"  访问次数: {entry['access_count']}")
        print(f"  剩余TTL: {entry['remaining_ttl']:.2f}s")
        print()
    
    print()


if __name__ == '__main__':
    basic_operations()
    ttl_example()
    lru_example()
    stats_example()
    get_or_set_example()
    entries_info_example()
    
    print("示例完成！")