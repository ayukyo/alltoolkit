"""
timer_wheel_utils.py
零外部依赖的时间轮定时器模块
实现高效的大规模定时任务调度

时间轮（Timing Wheel）是一种高效的定时器数据结构，
适用于需要管理大量定时任务的场景，时间复杂度为O(1)。
"""

import time
import threading
from collections import defaultdict
from typing import Callable, Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class TimerState(Enum):
    """定时器状态枚举"""
    PENDING = "pending"      # 等待执行
    RUNNING = "running"      # 正在执行
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


@dataclass
class TimerTask:
    """定时任务"""
    id: int
    callback: Callable
    delay_ms: int           # 延迟毫秒数
    period_ms: int = 0      # 周期毫秒数（0表示一次性任务）
    state: TimerState = TimerState.PENDING
    created_at: float = field(default_factory=time.time)
    execution_count: int = 0
    max_executions: int = 0  # 最大执行次数（0表示无限制）
    tag: str = ""            # 任务标签，用于分组管理
    data: Any = None         # 附加数据


class TimerWheel:
    """
    时间轮定时器
    
    高效处理大量定时任务的数据结构。
    使用分层时间轮支持广泛的延迟范围。
    """
    
    def __init__(self, tick_ms: int = 100, wheel_size: int = 60):
        """
        初始化时间轮
        
        Args:
            tick_ms: 时间轮刻度（毫秒）
            wheel_size: 时间轮大小（槽数量）
        """
        self.tick_ms = tick_ms
        self.wheel_size = wheel_size
        self.current_tick = 0
        self.wheel: Dict[int, List[TimerTask]] = defaultdict(list)
        self.task_counter = 0
        self.tasks: Dict[int, TimerTask] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._overflow_wheel: Optional['TimerWheel'] = None
        
        # 统计信息
        self.stats = {
            'tasks_created': 0,
            'tasks_completed': 0,
            'tasks_cancelled': 0,
            'total_executions': 0
        }
    
    def add_task(self, callback: Callable, delay_ms: int, 
                 period_ms: int = 0, max_executions: int = 0,
                 tag: str = "", data: Any = None) -> int:
        """
        添加定时任务
        
        Args:
            callback: 回调函数
            delay_ms: 延迟毫秒数
            period_ms: 周期毫秒数（0表示一次性任务）
            max_executions: 最大执行次数（0表示无限制）
            tag: 任务标签
            data: 附加数据
            
        Returns:
            任务ID
        """
        with self._lock:
            self.task_counter += 1
            task = TimerTask(
                id=self.task_counter,
                callback=callback,
                delay_ms=delay_ms,
                period_ms=period_ms,
                max_executions=max_executions,
                tag=tag,
                data=data
            )
            self.tasks[task.id] = task
            self._add_to_wheel(task)
            self.stats['tasks_created'] += 1
            return task.id
    
    def _add_to_wheel(self, task: TimerTask):
        """将任务添加到时间轮"""
        ticks = max(1, task.delay_ms // self.tick_ms)
        
        if ticks >= self.wheel_size:
            # 需要溢出轮处理
            if self._overflow_wheel is None:
                self._overflow_wheel = TimerWheel(
                    self.tick_ms * self.wheel_size,
                    self.wheel_size
                )
            # 递归添加到溢出轮
            self._overflow_wheel._add_to_wheel(task)
        else:
            slot = (self.current_tick + ticks) % self.wheel_size
            self.wheel[slot].append(task)
    
    def cancel_task(self, task_id: int) -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功取消
        """
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.state in (TimerState.PENDING, TimerState.RUNNING):
                    task.state = TimerState.CANCELLED
                    self.stats['tasks_cancelled'] += 1
                    return True
            return False
    
    def get_task(self, task_id: int) -> Optional[TimerTask]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def get_tasks_by_tag(self, tag: str) -> List[TimerTask]:
        """根据标签获取任务列表"""
        return [t for t in self.tasks.values() if t.tag == tag]
    
    def cancel_tasks_by_tag(self, tag: str) -> int:
        """
        取消指定标签的所有任务
        
        Returns:
            取消的任务数量
        """
        count = 0
        with self._lock:
            for task in self.tasks.values():
                if task.tag == tag and task.state in (TimerState.PENDING, TimerState.RUNNING):
                    task.state = TimerState.CANCELLED
                    self.stats['tasks_cancelled'] += 1
                    count += 1
        return count
    
    def start(self):
        """启动时间轮"""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        if self._overflow_wheel:
            self._overflow_wheel.start()
    
    def stop(self):
        """停止时间轮"""
        self._running = False
        if self._overflow_wheel:
            self._overflow_wheel.stop()
        if self._thread:
            self._thread.join(timeout=1)
    
    def _run(self):
        """时间轮主循环"""
        while self._running:
            self._tick()
            time.sleep(self.tick_ms / 1000.0)
    
    def _tick(self):
        """执行一个时间刻度"""
        with self._lock:
            slot = self.current_tick % self.wheel_size
            tasks = self.wheel[slot]
            self.wheel[slot] = []
            self.current_tick += 1
            
            # 处理溢出轮
            if self._overflow_wheel:
                overflow_tasks = self._overflow_wheel._get_current_tasks()
                for task in overflow_tasks:
                    self._add_to_wheel(task)
            
            # 执行任务
            for task in tasks:
                self._execute_task(task)
    
    def _get_current_tasks(self) -> List[TimerTask]:
        """获取当前槽位的任务"""
        slot = self.current_tick % self.wheel_size
        tasks = self.wheel[slot]
        self.wheel[slot] = []
        return tasks
    
    def _execute_task(self, task: TimerTask):
        """执行任务"""
        if task.state == TimerState.CANCELLED:
            return
            
        task.state = TimerState.RUNNING
        try:
            task.callback(task)
            task.execution_count += 1
            self.stats['total_executions'] += 1
            
            # 检查是否需要继续执行
            if task.period_ms > 0:
                if task.max_executions == 0 or task.execution_count < task.max_executions:
                    task.delay_ms = task.period_ms
                    task.state = TimerState.PENDING
                    self._add_to_wheel(task)
                else:
                    task.state = TimerState.COMPLETED
                    self.stats['tasks_completed'] += 1
            else:
                task.state = TimerState.COMPLETED
                self.stats['tasks_completed'] += 1
        except Exception as e:
            task.state = TimerState.COMPLETED
            self.stats['tasks_completed'] += 1
            print(f"Task {task.id} execution error: {e}")
    
    def tick(self):
        """手动推进一个时间刻度（用于测试）"""
        self._tick()
    
    def get_stats(self) -> Dict[str, int]:
        """获取统计信息"""
        return self.stats.copy()
    
    def get_pending_count(self) -> int:
        """获取待执行任务数量"""
        return sum(1 for t in self.tasks.values() if t.state == TimerState.PENDING)
    
    def clear(self):
        """清除所有任务"""
        with self._lock:
            self.wheel.clear()
            self.tasks.clear()
            self.current_tick = 0
            if self._overflow_wheel:
                self._overflow_wheel.clear()


class HierarchicalTimerWheel:
    """
    分层时间轮
    
    多层时间轮设计，支持更大的时间范围和更高的精度
    """
    
    def __init__(self, tick_ms: int = 1, levels: int = 5, wheel_size: int = 60):
        """
        初始化分层时间轮
        
        Args:
            tick_ms: 最底层时间轮的刻度（毫秒）
            levels: 时间轮层数
            wheel_size: 每层时间轮的大小
        """
        self.levels = []
        self.tick_ms = tick_ms
        self.wheel_size = wheel_size
        
        current_tick = tick_ms
        for _ in range(levels):
            wheel = TimerWheel(current_tick, wheel_size)
            self.levels.append(wheel)
            current_tick *= wheel_size
        
        self.task_counter = 0
        self.tasks: Dict[int, TimerTask] = {}
        self._lock = threading.Lock()
        self._running = False
    
    def add_task(self, callback: Callable, delay_ms: int,
                 period_ms: int = 0, tag: str = "", data: Any = None) -> int:
        """添加定时任务"""
        with self._lock:
            self.task_counter += 1
            task = TimerTask(
                id=self.task_counter,
                callback=callback,
                delay_ms=delay_ms,
                period_ms=period_ms,
                tag=tag,
                data=data
            )
            self.tasks[task.id] = task
            self._add_to_level(task)
            return task.id
    
    def _add_to_level(self, task: TimerTask):
        """将任务添加到合适的层级"""
        ticks = task.delay_ms // self.tick_ms
        
        for level, wheel in enumerate(self.levels):
            if ticks < self.wheel_size:
                wheel._add_to_wheel(task)
                return
            ticks //= self.wheel_size
        
        # 如果延迟太大，放到最底层
        self.levels[-1]._add_to_wheel(task)
    
    def start(self):
        """启动所有层级"""
        self._running = True
        for wheel in self.levels:
            wheel.start()
    
    def stop(self):
        """停止所有层级"""
        self._running = False
        for wheel in self.levels:
            wheel.stop()
    
    def cancel_task(self, task_id: int) -> bool:
        """取消任务"""
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.state = TimerState.CANCELLED
                return True
            return False


class SimpleTimer:
    """
    简单定时器
    
    基于时间戳的简单定时器实现
    """
    
    def __init__(self):
        self.tasks: Dict[int, Tuple[float, Callable, bool]] = {}
        self.task_counter = 0
        self._lock = threading.Lock()
    
    def schedule(self, callback: Callable, delay: float, 
                 repeat: bool = False) -> int:
        """
        调度任务
        
        Args:
            callback: 回调函数
            delay: 延迟秒数
            repeat: 是否重复执行
            
        Returns:
            任务ID
        """
        with self._lock:
            self.task_counter += 1
            execute_at = time.time() + delay
            self.tasks[self.task_counter] = (execute_at, callback, repeat)
            return self.task_counter
    
    def cancel(self, task_id: int) -> bool:
        """取消任务"""
        with self._lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                return True
            return False
    
    def update(self) -> List[Any]:
        """
        更新定时器，执行到期任务
        
        Returns:
            执行结果列表
        """
        now = time.time()
        results = []
        
        with self._lock:
            to_execute = []
            to_remove = []
            
            for task_id, (execute_at, callback, repeat) in self.tasks.items():
                if now >= execute_at:
                    to_execute.append((task_id, callback, repeat))
                    if not repeat:
                        to_remove.append(task_id)
            
            for task_id in to_remove:
                del self.tasks[task_id]
            
            for task_id, callback, repeat in to_execute:
                try:
                    result = callback()
                    results.append(result)
                except Exception as e:
                    results.append(e)
        
        return results


class CountDownLatch:
    """
    倒计时门闩
    
    同步工具，允许一个或多个线程等待其他线程完成操作
    """
    
    def __init__(self, count: int):
        """
        初始化
        
        Args:
            count: 计数器初始值
        """
        self.count = count
        self._condition = threading.Condition()
    
    def count_down(self):
        """计数减一"""
        with self._condition:
            self.count -= 1
            if self.count <= 0:
                self._condition.notify_all()
    
    def await_timeout(self, timeout: Optional[float] = None) -> bool:
        """
        等待计数归零
        
        Args:
            timeout: 超时时间（秒），None表示无限等待
            
        Returns:
            是否成功（未超时）
        """
        with self._condition:
            if self.count <= 0:
                return True
            self._condition.wait(timeout)
            return self.count <= 0


class RateLimiter:
    """
    速率限制器
    
    基于令牌桶算法的速率限制
    """
    
    def __init__(self, rate: float, capacity: Optional[int] = None):
        """
        初始化
        
        Args:
            rate: 每秒令牌数
            capacity: 令牌桶容量，默认等于rate
        """
        self.rate = rate
        self.capacity = capacity if capacity else int(rate)
        self.tokens = self.capacity
        self.last_update = time.time()
        self._lock = threading.Lock()
    
    def acquire(self, tokens: int = 1) -> bool:
        """
        尝试获取令牌
        
        Args:
            tokens: 需要的令牌数
            
        Returns:
            是否成功获取
        """
        with self._lock:
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_acquire(self, tokens: int = 1) -> float:
        """
        等待直到可以获取令牌
        
        Args:
            tokens: 需要的令牌数
            
        Returns:
            等待时间（秒）
        """
        while True:
            with self._lock:
                now = time.time()
                elapsed = now - self.last_update
                self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
                self.last_update = now
                
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return 0
                
                needed = tokens - self.tokens
                wait_time = needed / self.rate
            
            time.sleep(wait_time * 0.5)


class Debouncer:
    """
    防抖器
    
    确保函数在指定时间内只执行一次
    """
    
    def __init__(self, delay: float):
        """
        初始化
        
        Args:
            delay: 防抖延迟（秒）
        """
        self.delay = delay
        self._last_call: Optional[float] = None
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()
        self._pending_args: Any = None
        self._pending_func: Optional[Callable] = None
    
    def call(self, func: Callable, *args, **kwargs):
        """
        调用函数（带防抖）
        
        Args:
            func: 要执行的函数
            args, kwargs: 函数参数
        """
        with self._lock:
            self._pending_func = func
            self._pending_args = (args, kwargs)
            
            if self._timer:
                self._timer.cancel()
            
            def execute():
                if self._pending_func:
                    self._pending_func(*self._pending_args[0], **self._pending_args[1])
            
            self._timer = threading.Timer(self.delay, execute)
            self._timer.start()


class Throttler:
    """
    节流器
    
    确保函数在指定时间间隔内最多执行一次
    """
    
    def __init__(self, interval: float):
        """
        初始化
        
        Args:
            interval: 节流间隔（秒）
        """
        self.interval = interval
        self._last_execution: Optional[float] = None
        self._lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        调用函数（带节流）
        
        Args:
            func: 要执行的函数
            args, kwargs: 函数参数
            
        Returns:
            函数执行结果，如果被节流则返回None
        """
        with self._lock:
            now = time.time()
            if self._last_execution is None or now - self._last_execution >= self.interval:
                self._last_execution = now
                return func(*args, **kwargs)
            return None


# 模块信息
__version__ = "1.0.0"
__author__ = "AllToolkit"
__date__ = "2026-05-21"