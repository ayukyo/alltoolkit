"""
test_timer_wheel_utils.py
时间轮定时器模块测试
"""

import time
import threading
from timer_wheel_utils import (
    TimerWheel, TimerTask, TimerState,
    HierarchicalTimerWheel, SimpleTimer,
    CountDownLatch, RateLimiter, Debouncer, Throttler
)


def test_timer_task():
    """测试TimerTask数据类"""
    print("--- TimerTask 测试 ---")
    
    task = TimerTask(
        id=1,
        callback=lambda t: None,
        delay_ms=100,
        period_ms=50,
        tag="test"
    )
    
    assert task.id == 1
    assert task.delay_ms == 100
    assert task.period_ms == 50
    assert task.state == TimerState.PENDING
    assert task.tag == "test"
    print("✓ TimerTask 创建成功")


def test_timer_wheel_basic():
    """测试TimerWheel基本功能"""
    print("\n--- TimerWheel 基本功能测试 ---")
    
    results = []
    
    def callback(task):
        results.append(task.id)
    
    wheel = TimerWheel(tick_ms=10, wheel_size=10)
    
    # 添加任务
    task_id1 = wheel.add_task(callback, 50, tag="task1")
    task_id2 = wheel.add_task(callback, 100, tag="task2")
    
    assert task_id1 == 1
    assert task_id2 == 2
    print(f"✓ 添加任务: {task_id1}, {task_id2}")
    
    # 获取任务
    task = wheel.get_task(task_id1)
    assert task is not None
    assert task.tag == "task1"
    print("✓ 获取任务成功")
    
    # 按标签获取任务
    tasks = wheel.get_tasks_by_tag("task1")
    assert len(tasks) == 1
    print("✓ 按标签获取任务成功")


def test_timer_wheel_execution():
    """测试TimerWheel任务执行"""
    print("\n--- TimerWheel 任务执行测试 ---")
    
    results = []
    lock = threading.Lock()
    
    def callback(task):
        with lock:
            results.append((task.id, time.time()))
    
    wheel = TimerWheel(tick_ms=10, wheel_size=100)
    
    # 添加延迟任务
    start_time = time.time()
    wheel.add_task(callback, 50)   # 50ms
    wheel.add_task(callback, 100)  # 100ms
    wheel.add_task(callback, 150)  # 150ms
    
    # 手动推进时间轮
    for _ in range(20):
        wheel.tick()
        time.sleep(0.01)  # 10ms
    
    assert len(results) == 3
    print(f"✓ 执行了 {len(results)} 个任务")
    
    # 验证执行顺序
    for i in range(len(results) - 1):
        assert results[i][0] < results[i + 1][0]
    print("✓ 任务按顺序执行")


def test_timer_wheel_periodic():
    """测试TimerWheel周期任务"""
    print("\n--- TimerWheel 周期任务测试 ---")
    
    execution_times = []
    lock = threading.Lock()
    
    def callback(task):
        with lock:
            execution_times.append(time.time())
    
    wheel = TimerWheel(tick_ms=10, wheel_size=100)
    wheel.add_task(callback, delay_ms=50, period_ms=30, max_executions=3)
    
    # 推进时间轮
    for _ in range(15):
        wheel.tick()
        time.sleep(0.01)
    
    assert len(execution_times) == 3
    print(f"✓ 周期任务执行了 {len(execution_times)} 次")


def test_timer_wheel_cancel():
    """测试TimerWheel任务取消"""
    print("\n--- TimerWheel 任务取消测试 ---")
    
    results = []
    
    def callback(task):
        results.append(task.id)
    
    wheel = TimerWheel(tick_ms=10, wheel_size=100)
    
    task_id = wheel.add_task(callback, 50)
    wheel.cancel_task(task_id)
    
    task = wheel.get_task(task_id)
    assert task.state == TimerState.CANCELLED
    print("✓ 任务已取消")
    
    # 推进时间轮
    for _ in range(10):
        wheel.tick()
        time.sleep(0.01)
    
    assert len(results) == 0
    print("✓ 取消的任务未执行")


def test_timer_wheel_cancel_by_tag():
    """测试按标签取消任务"""
    print("\n--- TimerWheel 按标签取消测试 ---")
    
    wheel = TimerWheel(tick_ms=10, wheel_size=100)
    
    def callback(task):
        pass
    
    wheel.add_task(callback, 100, tag="group1")
    wheel.add_task(callback, 100, tag="group1")
    wheel.add_task(callback, 100, tag="group2")
    
    count = wheel.cancel_tasks_by_tag("group1")
    assert count == 2
    print(f"✓ 取消了 {count} 个标签为 'group1' 的任务")
    
    # 验证
    tasks = wheel.get_tasks_by_tag("group2")
    assert len(tasks) == 1
    assert tasks[0].state == TimerState.PENDING
    print("✓ 标签为 'group2' 的任务未被取消")


def test_timer_wheel_stats():
    """测试TimerWheel统计功能"""
    print("\n--- TimerWheel 统计功能测试 ---")
    
    wheel = TimerWheel(tick_ms=10, wheel_size=100)
    
    def callback(task):
        pass
    
    # 添加多个任务
    for _ in range(5):
        wheel.add_task(callback, 50)
    
    stats = wheel.get_stats()
    assert stats['tasks_created'] == 5
    print(f"✓ 创建了 {stats['tasks_created']} 个任务")
    
    # 执行任务
    for _ in range(10):
        wheel.tick()
        time.sleep(0.01)
    
    stats = wheel.get_stats()
    assert stats['tasks_completed'] == 5
    print(f"✓ 完成了 {stats['tasks_completed']} 个任务")


def test_simple_timer():
    """测试SimpleTimer"""
    print("\n--- SimpleTimer 测试 ---")
    
    results = []
    timer = SimpleTimer()
    
    def callback():
        results.append(time.time())
        return "done"
    
    timer.schedule(callback, 0.1)
    time.sleep(0.15)
    
    executed = timer.update()
    assert len(executed) == 1
    assert executed[0] == "done"
    print("✓ SimpleTimer 任务执行成功")


def test_simple_timer_repeat():
    """测试SimpleTimer重复任务"""
    print("\n--- SimpleTimer 重复任务测试 ---")
    
    results = []
    timer = SimpleTimer()
    
    def callback():
        results.append(time.time())
        return len(results)
    
    timer.schedule(callback, 0.05, repeat=True)
    
    for _ in range(5):
        time.sleep(0.05)
        timer.update()
    
    assert len(results) >= 3
    print(f"✓ 重复任务执行了 {len(results)} 次")


def test_count_down_latch():
    """测试CountDownLatch"""
    print("\n--- CountDownLatch 测试 ---")
    
    latch = CountDownLatch(3)
    results = []
    
    def worker():
        time.sleep(0.1)
        results.append(threading.current_thread().name)
        latch.count_down()
    
    threads = [
        threading.Thread(target=worker, name=f"worker-{i}")
        for i in range(3)
    ]
    
    for t in threads:
        t.start()
    
    success = latch.await_timeout(1.0)
    assert success
    assert len(results) == 3
    print(f"✓ CountDownLatch 成功等待 {len(results)} 个线程完成")


def test_rate_limiter():
    """测试RateLimiter"""
    print("\n--- RateLimiter 测试 ---")
    
    # 每秒5个令牌
    limiter = RateLimiter(rate=5, capacity=10)
    
    # 快速获取
    successes = 0
    for _ in range(10):
        if limiter.acquire():
            successes += 1
    
    assert successes == 10  # 容量允许
    print(f"✓ 成功获取 {successes} 个令牌（容量）")
    
    # 容量耗尽后
    assert not limiter.acquire()
    print("✓ 容量耗尽后无法获取")
    
    # 等待恢复
    time.sleep(0.4)  # 恢复约2个令牌
    assert limiter.acquire()
    print("✓ 等待后可获取令牌")


def test_debouncer():
    """测试Debouncer"""
    print("\n--- Debouncer 测试 ---")
    
    results = []
    debouncer = Debouncer(delay=0.1)
    
    def callback(value):
        results.append(value)
    
    # 快速调用多次
    for i in range(5):
        debouncer.call(callback, i)
        time.sleep(0.02)
    
    time.sleep(0.2)  # 等待防抖完成
    
    assert len(results) == 1
    assert results[0] == 4  # 最后一次调用的值
    print(f"✓ Debouncer 执行了 {len(results)} 次，值为 {results[0]}")


def test_throttler():
    """测试Throttler"""
    print("\n--- Throttler 测试 ---")
    
    results = []
    throttler = Throttler(interval=0.1)
    
    def callback(value):
        results.append(value)
        return value
    
    # 快速调用多次
    for i in range(5):
        result = throttler.call(callback, i)
        time.sleep(0.03)
    
    # 应该只执行了部分
    assert len(results) >= 1
    assert len(results) <= 3
    print(f"✓ Throttler 执行了 {len(results)} 次（5次调用中）")


def test_hierarchical_timer_wheel():
    """测试HierarchicalTimerWheel"""
    print("\n--- HierarchicalTimerWheel 测试 ---")
    
    results = []
    
    def callback(task):
        results.append(task.id)
    
    wheel = HierarchicalTimerWheel(tick_ms=10, levels=3, wheel_size=60)
    
    # 添加不同延迟的任务
    wheel.add_task(callback, 50)    # 短延迟
    wheel.add_task(callback, 1000)  # 中等延迟
    wheel.add_task(callback, 5000)  # 长延迟
    
    assert len(wheel.tasks) == 3
    print("✓ 分层时间轮添加任务成功")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("   timer_wheel_utils 测试套件")
    print("=" * 50)
    
    test_timer_task()
    test_timer_wheel_basic()
    test_timer_wheel_execution()
    test_timer_wheel_periodic()
    test_timer_wheel_cancel()
    test_timer_wheel_cancel_by_tag()
    test_timer_wheel_stats()
    test_simple_timer()
    test_simple_timer_repeat()
    test_count_down_latch()
    test_rate_limiter()
    test_debouncer()
    test_throttler()
    test_hierarchical_timer_wheel()
    
    print("\n" + "=" * 50)
    print("   所有测试通过！ ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()