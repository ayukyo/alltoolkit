"""
Rate Limiter Utils 使用示例

演示各种速率限制算法的实际应用场景。
"""

import time
import threading


def example_token_bucket():
    """令牌桶算法示例 - API 限流"""
    from rate_limiter_utils import TokenBucket

    print("\n=== 令牌桶算法示例 ===")

    # 每秒10个请求，桶容量20（允许突发）
    bucket = TokenBucket(rate=10, capacity=20)

    print(f"初始状态: {bucket}")

    # 模拟突发请求
    print("\n模拟突发请求:")
    for i in range(25):
        success = bucket.consume()
        print(f"请求 {i + 1}: {'✅ 成功' if success else '❌ 拒绝'}")

    print(f"\n消耗后状态: {bucket}")

    # 等待令牌补充
    print("\n等待1秒补充令牌...")
    time.sleep(1)
    print(f"补充后状态: {bucket}")

    # 使用等待模式
    print("\n使用等待模式:")
    wait_time = bucket.consume_or_wait(1, max_wait=5)
    print(f"等待 {wait_time:.3f} 秒后成功获取")


def example_leaky_bucket():
    """漏桶算法示例 - 网络流量整形"""
    from rate_limiter_utils import LeakyBucket

    print("\n=== 漏桶算法示例 ===")

    # 恒定速率处理5个请求/秒，桶容量10
    bucket = LeakyBucket(rate=5, capacity=10)

    print(f"初始状态: {bucket}")

    # 模拟请求进入
    print("\n请求进入:")
    for i in range(15):
        success = bucket.try_add()
        print(f"请求 {i + 1}: {'✅ 进入队列' if success else '❌ 拒绝'}")

    print(f"\n当前水位: {bucket.get_level()}/{bucket.capacity}")

    # 模拟漏水（处理请求）
    print("\n等待1秒，模拟漏水...")
    time.sleep(1)
    print(f"漏水后水位: {bucket.get_level()}/{bucket.capacity}")


def example_sliding_window():
    """滑动窗口算法示例 - 精确限流"""
    from rate_limiter_utils import SlidingWindow

    print("\n=== 滑动窗口算法示例 ===")

    # 每秒最多10个请求
    window = SlidingWindow(limit=10, window_size=1.0)

    print(f"初始状态: {window}")

    # 快速发送请求
    print("\n快速发送10个请求:")
    for i in range(10):
        success = window.try_acquire()
        print(f"请求 {i + 1}: {'✅' if success else '❌'}")

    # 获取时间戳详情
    timestamps = window.get_timestamps()
    print(f"\n窗口内请求时间戳: {len(timestamps)} 个")

    # 查看剩余配额
    print(f"剩余配额: {window.get_remaining()}")

    # 尝试超限请求
    print("\n尝试超限请求:")
    success = window.try_acquire()
    print(f"请求 11: {'✅' if success else '❌ 拒绝'}")

    # 查看等待时间
    wait_time = window.get_wait_time(1)
    print(f"\n需要等待 {wait_time:.3f} 秒")


def example_fixed_window():
    """固定窗口算法示例 - 简单高效的限流"""
    from rate_limiter_utils import FixedWindow

    print("\n=== 固定窗口算法示例 ===")

    # 每分钟最多60个请求
    window = FixedWindow(limit=60, window_size=60)

    print(f"初始状态: {window}")

    # 发送一批请求
    print("\n发送30个请求:")
    for i in range(30):
        window.try_acquire()

    state = window.get_state()
    print(f"当前计数: {state.request_count}")
    print(f"剩余配额: {window.get_remaining()}")
    print(f"窗口结束时间: {state.window_end - state.window_start:.1f} 秒后")


def example_fixed_window_keyed():
    """多键固定窗口示例 - 多用户限流"""
    from rate_limiter_utils.fixed_window import FixedWindowKeyed

    print("\n=== 多键固定窗口示例 ===")

    # 每个用户每分钟最多5个请求
    limiter = FixedWindowKeyed(limit=5, window_size=60)

    print("不同用户独立限流:")

    users = ['user1', 'user2', 'user3']
    for user in users:
        print(f"\n用户 {user}:")
        for i in range(7):
            success = limiter.try_acquire(user)
            if success:
                print(f"  请求 {i + 1}: ✅")
            else:
                print(f"  请求 {i + 1}: ❌ 已达上限")

    # 查看各用户状态
    print("\n各用户状态:")
    for user in users:
        print(f"  {user}: {limiter.get_count(user)}/{limiter.limit}")


def example_rate_limiter():
    """统一限流器示例 - 灵活切换算法"""
    from rate_limiter_utils import RateLimiter, Algorithm

    print("\n=== 统一速率限制器示例 ===")

    # 使用不同的算法
    algorithms = [
        ('令牌桶', Algorithm.TOKEN_BUCKET, {'rate': 10, 'capacity': 20}),
        ('漏桶', Algorithm.LEAKY_BUCKET, {'rate': 10, 'capacity': 20}),
        ('滑动窗口', Algorithm.SLIDING_WINDOW, {'limit': 10, 'window_size': 1}),
        ('固定窗口', Algorithm.FIXED_WINDOW, {'limit': 10, 'window_size': 1}),
    ]

    for name, algo, params in algorithms:
        print(f"\n{name}算法:")
        limiter = RateLimiter(algorithm=algo, **params)

        # 发送请求
        for i in range(12):
            success = limiter.try_acquire()
            if not success:
                print(f"  请求 {i + 1}: ❌ 达到限制")
                break

        # 显示状态
        state = limiter.get_state()
        print(f"  状态: {state}")


def example_multi_rate_limiter():
    """多层限流器示例 - 组合多个限制"""
    from rate_limiter_utils import MultiRateLimiter, Algorithm

    print("\n=== 多层速率限制器示例 ===")

    limiter = MultiRateLimiter()

    # 添加多个限制规则
    limiter.add_limit('每秒限制', Algorithm.SLIDING_WINDOW, limit=10, window_size=1)
    limiter.add_limit('每分钟限制', Algorithm.SLIDING_WINDOW, limit=50, window_size=60)
    limiter.add_limit('每小时限制', Algorithm.SLIDING_WINDOW, limit=200, window_size=3600)

    print("限流规则:")
    for rule in limiter.rules:
        print(f"  - {rule}")

    # 模拟请求
    print("\n发送请求:")
    for i in range(12):
        success, failed_rule = limiter.try_acquire()
        if success:
            print(f"  请求 {i + 1}: ✅")
        else:
            print(f"  请求 {i + 1}: ❌ 被规则 '{failed_rule}' 拒绝")


def example_decorators():
    """装饰器示例 - 函数级限流"""
    from rate_limiter_utils import rate_limit, RateLimitExceeded
    from rate_limiter_utils.decorators import (
        rate_limit_per_argument, clear_limiters
    )

    print("\n=== 装饰器示例 ===")

    clear_limiters()  # 清除之前的全局状态

    # 简单限流
    @rate_limit(rate=3, capacity=3)
    def simple_api():
        return "API响应"

    print("简单限流装饰器:")
    for i in range(5):
        try:
            result = simple_api()
            print(f"  调用 {i + 1}: {result}")
        except RateLimitExceeded as e:
            print(f"  调用 {i + 1}: ❌ {e}")

    # 基于参数的限流
    print("\n基于参数的限流:")
    @rate_limit_per_argument(
        key_func=lambda user_id: f"user_{user_id}",
        limit=2,
        window_size=60
    )
    def user_api(user_id):
        return f"用户 {user_id} 的响应"

    for user in [1, 2, 3]:
        print(f"\n用户 {user}:")
        for i in range(3):
            try:
                result = user_api(user)
                print(f"  调用 {i + 1}: {result}")
            except RateLimitExceeded as e:
                print(f"  调用 {i + 1}: ❌ 达到上限")


def example_context_manager():
    """上下文管理器示例"""
    from rate_limiter_utils.decorators import RateLimiterContext, RateLimitExceeded
    from rate_limiter_utils import Algorithm

    print("\n=== 上下文管理器示例 ===")

    # 创建限流器
    limiter = RateLimiterContext(
        algorithm=Algorithm.TOKEN_BUCKET,
        rate=2,
        capacity=2
    )

    print("使用上下文管理器:")

    # 成功获取
    with limiter.acquire_or_raise():
        print("  第1次: ✅ 成功获取许可")

    with limiter.acquire_or_raise():
        print("  第2次: ✅ 成功获取许可")

    # 超限抛异常
    try:
        with limiter.acquire_or_raise():
            print("  第3次: 不应该看到这个")
    except RateLimitExceeded:
        print("  第3次: ❌ 限流，抛出异常")

    # 使用等待模式
    print("\n使用等待模式:")
    limiter2 = RateLimiterContext(
        algorithm=Algorithm.TOKEN_BUCKET,
        rate=10,
        capacity=10
    )

    # 先消耗所有令牌
    for _ in range(10):
        limiter2._limiter.try_acquire()

    # 等待获取
    with limiter2.acquire_or_wait(timeout=1):
        print("  ✅ 等待后成功获取")


def example_real_world_api():
    """真实场景示例 - API 服务器限流"""
    from rate_limiter_utils import MultiRateLimiter, Algorithm

    print("\n=== 真实场景：API 服务器限流 ===")

    # 创建多层限流器
    global_limiter = MultiRateLimiter()
    global_limiter.add_limit('全局QPS', Algorithm.SLIDING_WINDOW, limit=1000, window_size=1)
    global_limiter.add_limit('全局QPM', Algorithm.SLIDING_WINDOW, limit=5000, window_size=60)

    # 用户级别限流器
    from rate_limiter_utils.fixed_window import FixedWindowKeyed
    user_limiter = FixedWindowKeyed(limit=10, window_size=60, max_keys=1000)

    def handle_api_request(user_id: str):
        """模拟API请求处理"""
        # 先检查全局限制
        global_success, global_rule = global_limiter.try_acquire()
        if not global_success:
            return {
                'status': 429,
                'error': f'服务器繁忙，被规则 {global_rule} 限制'
            }

        # 再检查用户限制
        user_success = user_limiter.try_acquire(user_id)
        if not user_success:
            return {
                'status': 429,
                'error': f'用户 {user_id} 请求过快'
            }

        return {
            'status': 200,
            'data': f'用户 {user_id} 的数据'
        }

    print("模拟API请求:")
    users = ['alice', 'bob', 'charlie']

    for user in users:
        print(f"\n用户 {user}:")
        for i in range(12):
            result = handle_api_request(user)
            if result['status'] == 200:
                print(f"  请求 {i + 1}: ✅ {result['data']}")
            else:
                print(f"  请求 {i + 1}: ❌ {result['error']}")
                break


def example_web_crawler():
    """真实场景示例 - 爬虫限流"""
    from rate_limiter_utils import RateLimiter, Algorithm
    from rate_limiter_utils.fixed_window import FixedWindowKeyed

    print("\n=== 真实场景：Web爬虫限流 ===")

    # 每个域名独立限流
    domain_limiter = FixedWindowKeyed(limit=20, window_size=60, max_keys=100)

    # 全局请求限制
    request_limiter = RateLimiter(
        algorithm=Algorithm.TOKEN_BUCKET,
        rate=5,  # 每秒5个请求
        capacity=10  # 允许突发10个
    )

    domains = ['example.com', 'api.service.com', 'data.site.com']

    print("爬虫请求模拟:")
    for domain in domains:
        print(f"\n爬取 {domain}:")
        for i in range(25):
            # 检查域名限制
            if not domain_limiter.try_acquire(domain):
                print(f"  请求 {i + 1}: ❌ 域名 {domain} 达到限制")
                break

            # 检查全局限制
            if not request_limiter.try_acquire():
                print(f"  请求 {i + 1}: ❌ 全局请求限制")
                break

            print(f"  请求 {i + 1}: ✅ 成功爬取")


def example_game_server():
    """真实场景示例 - 游戏服务器限流"""
    from rate_limiter_utils import MultiRateLimiter, Algorithm
    from rate_limiter_utils.fixed_window import FixedWindowKeyed

    print("\n=== 真实场景：游戏服务器限流 ===")

    # 动作限流（防止作弊）
    action_limiter = FixedWindowKeyed(limit=30, window_size=1, max_keys=10000)

    # 聊天限流
    chat_limiter = FixedWindowKeyed(limit=5, window_size=1, max_keys=10000)

    # 全局带宽限制
    bandwidth_limiter = MultiRateLimiter()
    bandwidth_limiter.add_limit('带宽', Algorithm.TOKEN_BUCKET, rate=1000, capacity=2000)

    def player_action(player_id: str, action: str):
        """模拟玩家动作"""
        # 检查动作限制
        if not action_limiter.try_acquire(player_id):
            return {
                'success': False,
                'message': f'玩家 {player_id} 动作过快'
            }

        # 检查带宽限制
        success, _ = bandwidth_limiter.try_acquire()
        if not success:
            return {
                'success': False,
                'message': '服务器带宽限制'
            }

        return {
            'success': True,
            'message': f'玩家 {player_id} 执行 {action}'
        }

    def player_chat(player_id: str, message: str):
        """模拟玩家聊天"""
        if not chat_limiter.try_acquire(player_id):
            return {
                'success': False,
                'message': f'玩家 {player_id} 发言过快'
            }

        return {
            'success': True,
            'message': f'玩家 {player_id}: {message}'
        }

    print("模拟玩家活动:")
    player = 'hero123'

    print(f"\n玩家 {player} 动作:")
    for action in ['移动', '攻击', '跳跃', '技能', '拾取']:
        result = player_action(player, action)
        print(f"  {action}: {'✅' if result['success'] else '❌'} {result['message']}")

    # 快速发送多个动作（模拟作弊）
    print("\n快速动作测试（模拟作弊）:")
    for i in range(35):
        result = player_action(player, '快速攻击')
        if not result['success']:
            print(f"  第 {i + 1} 次攻击: ❌ {result['message']}")
            break

    print(f"\n玩家 {player} 聊天:")
    messages = ['大家好', '游戏不错', '新手求教', '组队吗', '晚上在线']
    for msg in messages:
        result = player_chat(player, msg)
        print(f"  {msg}: {'✅' if result['success'] else '❌'} {result['message']}")


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("Rate Limiter Utils 使用示例")
    print("=" * 60)

    example_token_bucket()
    example_leaky_bucket()
    example_sliding_window()
    example_fixed_window()
    example_fixed_window_keyed()
    example_rate_limiter()
    example_multi_rate_limiter()
    example_decorators()
    example_context_manager()
    example_real_world_api()
    example_web_crawler()
    example_game_server()

    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()