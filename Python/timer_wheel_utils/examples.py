"""
examples.py
时间轮定时器模块使用示例
"""

import time
import threading
from timer_wheel_utils import (
    TimerWheel, TimerTask, TimerState,
    HierarchicalTimerWheel, SimpleTimer,
    CountDownLatch, RateLimiter, Debouncer, Throttler
)


def example_basic_timer():
    """示例1：基本定时器使用"""
    print("\n【示例1】基本定时器使用")
    print("-" * 40)
    
    results = []
    
    def on_timer(task):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        results.append(f"任务{task.id} 在 {current_time} 执行")
        print(f"  执行任务 {task.id}, 标签: {task.tag}")
    
    # 创建时间轮（100ms刻度，60个槽）
    wheel = TimerWheel(tick_ms=100, wheel_size=60)
    
    # 添加一次性任务
    wheel.add_task(on_timer, 200, tag="即时任务")   # 200ms后执行
    wheel.add_task(on_timer, 500, tag="延迟任务")   # 500ms后执行
    wheel.add_task(on_timer, 1000, tag="长时间任务") # 1秒后执行
    
    print("  已添加3个定时任务...")
    
    # 启动时间轮
    wheel.start()
    
    # 等待任务执行
    time.sleep(1.5)
    
    wheel.stop()
    print(f"\n  结果: 共执行 {len(results)} 个任务")


def example_periodic_timer():
    """示例2：周期性任务"""
    print("\n【示例2】周期性任务")
    print("-" * 40)
    
    counter = {'value': 0}
    
    def heartbeat(task):
        counter['value'] += 1
        print(f"  心跳 #{counter['value']} - 任务ID: {task.id}")
    
    wheel = TimerWheel(tick_ms=100, wheel_size=60)
    
    # 每300ms执行一次，最多执行5次
    wheel.add_task(heartbeat, delay_ms=0, period_ms=300, max_executions=5)
    
    print("  启动心跳任务（每300ms，共5次）...")
    wheel.start()
    
    time.sleep(2)
    
    wheel.stop()
    print(f"  心跳任务已完成，共执行 {counter['value']} 次")


def example_task_management():
    """示例3：任务管理"""
    print("\n【示例3】任务管理")
    print("-" * 40)
    
    wheel = TimerWheel(tick_ms=100, wheel_size=60)
    
    def task_a(task):
        print(f"  任务A执行 - 标签: {task.tag}")
    
    def task_b(task):
        print(f"  任务B执行 - 标签: {task.tag}")
    
    # 添加带标签的任务
    id1 = wheel.add_task(task_a, 500, tag="group_alpha")
    id2 = wheel.add_task(task_a, 600, tag="group_alpha")
    id3 = wheel.add_task(task_b, 500, tag="group_beta")
    id4 = wheel.add_task(task_b, 600, tag="group_beta")
    
    print(f"  添加了4个任务，标签分组:")
    print(f"    - group_alpha: {id1}, {id2}")
    print(f"    - group_beta: {id3}, {id4}")
    
    # 查询任务
    task = wheel.get_task(id1)
    print(f"\n  任务{id1}状态: {task.state.value}")
    
    # 按标签查询
    alpha_tasks = wheel.get_tasks_by_tag("group_alpha")
    print(f"  group_alpha 任务数: {len(alpha_tasks)}")
    
    # 取消单个任务
    wheel.cancel_task(id1)
    print(f"\n  已取消任务{id1}")
    
    # 按标签取消
    cancelled = wheel.cancel_tasks_by_tag("group_beta")
    print(f"  取消了 {cancelled} 个 group_beta 任务")
    
    # 查看统计
    stats = wheel.get_stats()
    print(f"\n  统计:")
    print(f"    - 创建: {stats['tasks_created']}")
    print(f"    - 取消: {stats['tasks_cancelled']}")
    
    wheel.clear()
    pending = wheel.get_pending_count()
    print(f"  清除后待执行任务: {pending}")


def example_rate_limiter():
    """示例4：速率限制器"""
    print("\n【示例4】速率限制器")
    print("-" * 40)
    
    # 创建限制器：每秒最多5个请求，桶容量10
    limiter = RateLimiter(rate=5, capacity=10)
    
    print("  速率限制器配置:")
    print("    - 速率: 5 请求/秒")
    print("    - 容量: 10 令牌")
    
    # 模拟突发请求
    print("\n  突发10个请求:")
    successes = 0
    for i in range(10):
        if limiter.acquire():
            successes += 1
            print(f"    请求 {i+1}: 允许 ✓")
        else:
            print(f"    请求 {i+1}: 拒绝 ✗")
    
    print(f"\n  结果: {successes}/10 请求被允许")
    
    # 模拟等待后请求
    print("\n  等待0.4秒后（约恢复2个令牌）:")
    time.sleep(0.4)
    
    for i in range(3):
        if limiter.acquire():
            print(f"    请求 {i+1}: 允许 ✓")
        else:
            print(f"    请求 {i+1}: 拒绝 ✗")


def example_debounce_throttle():
    """示例5：防抖和节流"""
    print("\n【示例5】防抖和节流")
    print("-" * 40)
    
    # 防抖示例
    print("  防抖示例（搜索输入）:")
    debounce_results = []
    
    def search(query):
        debounce_results.append(query)
        print(f"    执行搜索: '{query}'")
    
    debouncer = Debouncer(delay=0.2)
    
    # 模拟用户快速输入
    queries = ["a", "ab", "abc", "abcd", "abcde"]
    for q in queries:
        debouncer.call(search, q)
        time.sleep(0.05)
    
    time.sleep(0.3)  # 等待防抖完成
    print(f"    最终只搜索了: {debounce_results}")
    
    # 节流示例
    print("\n  节流示例（滚动事件）:")
    throttle_results = []
    
    def on_scroll(position):
        throttle_results.append(position)
        print(f"    处理滚动: {position}")
    
    throttler = Throttler(interval=0.15)
    
    # 模拟快速滚动
    for i in range(10):
        throttler.call(on_scroll, i * 100)
        time.sleep(0.03)
    
    print(f"    10次滚动事件只处理了 {len(throttle_results)} 次")


def example_countdown_latch():
    """示例6：倒计时门闩"""
    print("\n【示例6】倒计时门闩（多线程同步）")
    print("-" * 40)
    
    latch = CountDownLatch(3)
    results = []
    
    def worker(worker_id):
        print(f"  工作者 {worker_id} 开始工作...")
        time.sleep(0.5 + worker_id * 0.2)
        results.append(f"工作者{worker_id}完成")
        print(f"  工作者 {worker_id} 完成工作")
        latch.count_down()
    
    # 启动3个工作线程
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(i+1,))
        threads.append(t)
        t.start()
    
    print("  主线程等待所有工作者完成...")
    
    # 等待所有工作者完成
    success = latch.await_timeout(timeout=5.0)
    
    if success:
        print("  所有工作者已完成!")
        print(f"  结果: {results}")
    else:
        print("  等待超时!")


def example_simple_timer():
    """示例7：简单定时器"""
    print("\n【示例7】简单定时器")
    print("-" * 40)
    
    timer = SimpleTimer()
    results = []
    
    def delayed_task():
        results.append("延迟任务完成")
        print("  延迟任务已执行")
        return "success"
    
    def repeated_task():
        count = len([r for r in results if r.startswith("重复")])
        results.append(f"重复任务 #{count + 1}")
        print(f"  重复任务执行 #{count + 1}")
    
    # 添加延迟任务
    timer.schedule(delayed_task, 0.3)
    print("  已添加延迟任务（0.3秒后执行）")
    
    # 添加重复任务
    timer.schedule(repeated_task, 0.1, repeat=True)
    print("  已添加重复任务（每0.1秒）")
    
    # 手动更新定时器
    for _ in range(8):
        time.sleep(0.1)
        timer.update()
    
    print(f"\n  执行结果: {results[:5]}...")


def example_task_with_data():
    """示例8：带数据的任务"""
    print("\n【示例8】带数据的任务")
    print("-" * 40)
    
    wheel = TimerWheel(tick_ms=100, wheel_size=60)
    
    def process_order(task):
        order = task.data
        print(f"  处理订单: {order['id']}")
        print(f"    商品: {order['product']}")
        print(f"    数量: {order['quantity']}")
        print(f"    状态: {task.state.value}")
    
    # 添加带数据的任务
    order_data = {
        'id': 'ORD-12345',
        'product': '笔记本电脑',
        'quantity': 2
    }
    
    task_id = wheel.add_task(
        process_order, 
        delay_ms=200,
        tag="order_processing",
        data=order_data
    )
    
    print(f"  已创建订单处理任务 (ID: {task_id})")
    
    # 查看任务数据
    task = wheel.get_task(task_id)
    print(f"  任务数据: {task.data}")
    
    # 执行任务
    wheel.start()
    time.sleep(0.5)
    wheel.stop()


def example_stats():
    """示例9：统计信息"""
    print("\n【示例9】统计信息")
    print("-" * 40)
    
    wheel = TimerWheel(tick_ms=50, wheel_size=100)
    
    def task_callback(task):
        pass
    
    # 添加各种任务
    for i in range(10):
        wheel.add_task(task_callback, (i + 1) * 50, tag=f"batch_{i % 3}")
    
    print("  初始统计:")
    stats = wheel.get_stats()
    print(f"    创建任务数: {stats['tasks_created']}")
    print(f"    待执行任务: {wheel.get_pending_count()}")
    
    # 执行一些任务
    print("\n  推进时间轮...")
    for _ in range(8):
        wheel.tick()
        time.sleep(0.05)
    
    print("\n  执行后统计:")
    stats = wheel.get_stats()
    print(f"    完成任务: {stats['tasks_completed']}")
    print(f"    待执行任务: {wheel.get_pending_count()}")


def run_all_examples():
    """运行所有示例"""
    print("=" * 50)
    print("   timer_wheel_utils 使用示例")
    print("=" * 50)
    
    example_basic_timer()
    example_periodic_timer()
    example_task_management()
    example_rate_limiter()
    example_debounce_throttle()
    example_countdown_latch()
    example_simple_timer()
    example_task_with_data()
    example_stats()
    
    print("\n" + "=" * 50)
    print("   所有示例演示完成")
    print("=" * 50)


if __name__ == "__main__":
    run_all_examples()