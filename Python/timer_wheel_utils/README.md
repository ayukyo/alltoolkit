# Timer Wheel Utils

时间轮定时器工具模块，零外部依赖，高效处理大规模定时任务。

## 功能特性

### TimerWheel - 时间轮定时器
- O(1)时间复杂度的任务添加和执行
- 支持一次性任务和周期性任务
- 任务标签分组管理
- 任务取消（单个或按标签）
- 执行统计功能

### HierarchicalTimerWheel - 分层时间轮
- 多层级设计，支持更广泛的延迟范围
- 自动将任务分配到合适的层级

### SimpleTimer - 简单定时器
- 基于时间戳的轻量级实现
- 支持重复任务

### RateLimiter - 速率限制器
- 令牌桶算法实现
- 支持突发流量控制

### Debouncer - 防抖器
- 确保函数在指定时间内只执行一次
- 适用于搜索输入、按钮点击等场景

### Throttler - 节流器
- 确保函数在指定间隔内最多执行一次
- 适用于滚动事件、resize事件等场景

### CountDownLatch - 倒计时门闩
- 多线程同步工具
- 支持超时等待

## 使用示例

```python
from timer_wheel_utils import TimerWheel

# 创建时间轮
wheel = TimerWheel(tick_ms=100, wheel_size=60)

# 添加任务
def callback(task):
    print(f"任务 {task.id} 执行")

wheel.add_task(callback, delay_ms=500, tag="my_task")

# 启动
wheel.start()
```

## 文件结构

- `timer_wheel_utils.py` - 主模块
- `test_timer_wheel_utils.py` - 测试文件
- `examples.py` - 使用示例
- `README.md` - 说明文档

## 测试结果

所有13项测试全部通过。