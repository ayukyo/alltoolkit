# Throttle Utils


Throttle Utilities - Function throttling with multiple modes.

Throttling limits the rate of function calls, ensuring a function
is not called more than once in a specified time window.

Modes:
- leading: Call immediately on first invocation, then throttle
- trailing: Wait until the throttle period ends before calling
- both: Call immediately AND at the end of the throttle period

This is different from rate limiting (limits call count per window)
and debouncing (waits for a pause before calling).


## 功能

### 类

- **ThrottleMode**: Throttle behavior modes
- **ThrottleState**: Internal state for throttled function
- **ThrottledFunction**: A throttled function wrapper with configurable behavior
  方法: cancel, flush, pending, reset
- **AsyncThrottledFunction**: Async version of ThrottledFunction
  方法: cancel, pending, reset
- **ThrottleQueue**: A queue that throttles the rate at which items are processed
  方法: enqueue, process_next, process_all_available, clear, size ... (6 个方法)
- **SlidingThrottle**: Sliding window throttle - ensures minimum time between each call
  方法: acquire, wait_and_acquire, try_acquire, reset
- **TokenBucketThrottle**: Token bucket throttle for rate limiting
  方法: try_consume, consume, available, reset
- **AdaptiveThrottle**: Adaptive throttle that adjusts interval based on success/failure
  方法: interval, acquire, success, failure, reset

### 函数

- **throttle(interval, mode, leading**, ...) - Decorator to throttle function calls.
- **athrottle(interval, mode, leading**, ...) - Decorator to throttle async function calls.
- **create_throttle(interval, mode**) - Convenience function to create a throttle decorator.
- **cancel(self**) - Cancel any pending trailing call.
- **flush(self**) - Immediately execute any pending trailing call.
- **pending(self**) - Check if there's a pending trailing call.
- **reset(self**) - Reset the throttle state completely.
- **decorator(func**)
- **cancel(self**) - Cancel any pending trailing call.
- **pending(self**) - Check if there's a pending trailing call.

... 共 31 个函数

## 使用示例

```python
from mod import throttle

# 使用 throttle
result = throttle()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
