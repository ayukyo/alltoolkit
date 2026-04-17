"""
cache_utils 装饰器用法示例

演示：
- @cached 装饰器基本用法
- TTL 过期
- 自定义缓存键
- 缓存统计
"""

import time
from mod import cached, MemoryCache


def basic_decorator():
    """基本装饰器用法"""
    print("=== 基本装饰器用法 ===\n")
    
    @cached(ttl=60)
    def compute_fibonacci(n):
        """计算斐波那契数列（演示缓存效果）"""
        print(f"  计算中: fib({n})")
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    print("第一次调用 fib(10):")
    result1 = compute_fibonacci(10)
    print(f"  结果: {result1}")
    
    print("\n第二次调用 fib(10) (缓存命中):")
    result2 = compute_fibonacci(10)
    print(f"  结果: {result2}")
    
    print("\n调用不同参数 fib(20):")
    result3 = compute_fibonacci(20)
    print(f"  结果: {result3}")
    
    # 查看缓存统计
    stats = compute_fibonacci.cache_stats()
    print(f"\n缓存统计:")
    print(f"  命中: {stats.hits}")
    print(f"  未命中: {stats.misses}")
    print(f"  命中率: {stats.hit_rate:.2%}")
    
    print()


def ttl_decorator():
    """带 TTL 的装饰器"""
    print("=== TTL 过期示例 ===\n")
    
    @cached(ttl=2)
    def get_current_time():
        """获取当前时间（2秒缓存）"""
        return time.strftime("%H:%M:%S")
    
    print("第一次调用:")
    t1 = get_current_time()
    print(f"  时间: {t1}")
    
    print("\n立即再次调用 (缓存命中):")
    t2 = get_current_time()
    print(f"  时间: {t2}")
    print(f"  相同? {t1 == t2}")
    
    print("\n等待 2.5 秒...")
    time.sleep(2.5)
    
    print("过期后再次调用:")
    t3 = get_current_time()
    print(f"  时间: {t3}")
    print(f"  与第一次相同? {t1 == t3}")
    
    print()


def custom_key_decorator():
    """自定义缓存键"""
    print("=== 自定义缓存键 ===\n")
    
    # 使用前缀
    @cached(ttl=60, key_prefix='user_')
    def get_user(user_id):
        print(f"  查询用户: {user_id}")
        return {'id': user_id, 'name': f'User{user_id}'}
    
    print("调用 get_user(1):")
    user1 = get_user(1)
    print(f"  结果: {user1}")
    
    print("\n再次调用 get_user(1) (缓存命中):")
    user1_cached = get_user(1)
    print(f"  结果: {user1_cached}")
    
    print()
    
    # 完全自定义键构建
    def build_cache_key(*args, **kwargs):
        """根据参数构建缓存键"""
        user_id = args[0] if args else kwargs.get('user_id')
        include_details = kwargs.get('include_details', False)
        return f"custom:user:{user_id}:details:{include_details}"
    
    @cached(ttl=60, key_builder=build_cache_key)
    def fetch_user_data(user_id, include_details=False):
        print(f"  获取用户数据: id={user_id}, details={include_details}")
        data = {'id': user_id}
        if include_details:
            data['details'] = '详细信息'
        return data
    
    print("调用 fetch_user_data(1, include_details=False):")
    data1 = fetch_user_data(1, include_details=False)
    print(f"  结果: {data1}")
    
    print("\n调用 fetch_user_data(1, include_details=True) (不同键):")
    data2 = fetch_user_data(1, include_details=True)
    print(f"  结果: {data2}")
    
    print()


def cache_control():
    """缓存控制"""
    print("=== 缓存控制 ===\n")
    
    @cached(ttl=60, max_size=100)
    def expensive_operation(n):
        print(f"  执行耗时操作: {n}")
        return n ** 2
    
    print("执行操作...")
    expensive_operation(1)
    expensive_operation(2)
    expensive_operation(3)
    
    stats = expensive_operation.cache_stats()
    print(f"\n缓存大小: {expensive_operation.cache.size()}")
    print(f"命中: {stats.hits}, 未命中: {stats.misses}")
    
    print("\n清除缓存...")
    expensive_operation.cache_clear()
    print(f"清除后大小: {expensive_operation.cache.size()}")
    
    print("\n再次执行 (缓存已清除):")
    expensive_operation(1)
    stats = expensive_operation.cache_stats()
    print(f"未命中次数: {stats.misses}")
    
    print()


def max_size_decorator():
    """最大容量限制"""
    print("=== 最大容量限制 ===\n")
    
    @cached(ttl=60, max_size=5)
    def process(n):
        print(f"  处理: {n}")
        return n * 2
    
    print("添加 1-5:")
    for i in range(1, 6):
        process(i)
    
    print(f"缓存大小: {process.cache.size()}")
    
    print("\n添加 6 (应淘汰最久未使用的):")
    process(6)
    print(f"缓存大小: {process.cache.size()}")
    
    stats = process.cache_stats()
    print(f"淘汰次数: {stats.evictions}")
    
    print()


def method_caching():
    """方法缓存示例"""
    print("=== 方法缓存示例 ===\n")
    
    class DataService:
        def __init__(self):
            self.query_count = 0
        
        @cached(ttl=30)
        def get_data(self, key):
            """实例方法缓存（注意：装饰器不感知 self）"""
            self.query_count += 1
            print(f"  查询数据: {key}")
            return f"data_for_{key}"
    
    service = DataService()
    
    print("第一次查询 'item1':")
    result1 = service.get_data('item1')
    print(f"  结果: {result1}")
    
    print("\n第二次查询 'item1' (缓存命中):")
    result2 = service.get_data('item1')
    print(f"  结果: {result2}")
    
    print(f"\n实际查询次数: {service.query_count}")
    
    print()


def real_world_example():
    """实际应用示例"""
    print("=== 实际应用示例: 模拟 API 缓存 ===\n")
    
    @cached(ttl=60, max_size=100)
    def fetch_api_data(endpoint, params=None):
        """模拟 API 调用缓存"""
        print(f"  [API调用] endpoint={endpoint}, params={params}")
        # 模拟返回数据
        return {
            'endpoint': endpoint,
            'params': params or {},
            'data': f"response_for_{endpoint}",
            'timestamp': time.time()
        }
    
    print("请求 /users:")
    result1 = fetch_api_data('/users')
    print(f"  返回: {result1['data']}")
    
    print("\n请求 /users (相同参数，缓存命中):")
    result2 = fetch_api_data('/users')
    print(f"  返回: {result2['data']}")
    
    print("\n请求 /users?page=2 (不同参数):")
    result3 = fetch_api_data('/users', {'page': 2})
    print(f"  返回: {result3['data']}")
    
    stats = fetch_api_data.cache_stats()
    print(f"\nAPI调用统计:")
    print(f"  总请求: {stats.total_requests}")
    print(f"  缓存命中: {stats.hits}")
    print(f"  实际API调用: {stats.misses}")
    print(f"  节省请求: {stats.hits} 次")
    
    print()


if __name__ == '__main__':
    basic_decorator()
    ttl_decorator()
    custom_key_decorator()
    cache_control()
    max_size_decorator()
    method_caching()
    real_world_example()
    
    print("示例完成！")