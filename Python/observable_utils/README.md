# Observable Utils


AllToolkit - Python Observable Utilities

A zero-dependency, production-ready observer pattern / event emitter module.
Supports synchronous and async observers, event filtering, one-time subscriptions,
event history, and thread-safe operations.

Author: AllToolkit
License: MIT


## 功能

### 类

- **Priority**: Observer priority levels
- **Subscription**: Represents a subscription to an event
  方法: matches, call_count
- **EventRecord**: Record of a past event emission
- **Observable**: A thread-safe observable that manages event subscriptions and emissions
  方法: name, subscription_count, subscribe, subscribe_once, unsubscribe ... (12 个方法)
- **EventEmitter**: A multi-event observable that supports named events
  方法: on, once, subscribe, emit, unsubscribe ... (8 个方法)
- **PropertyObservable**: An observable property that notifies subscribers when its value changes
  方法: value, value, on_change, set_silent
- **ComputedObservable**: An observable that computes its value from other observables
  方法: value, on_change
- **Subject**: A simple observable value that can be set and observed
  方法: value, next, subscribe, unsubscribe_all
- **BehaviorSubject**: A Subject that remembers the current value and emits it to new subscribers
  方法: value, next, subscribe, unsubscribe_all
- **ReplaySubject**: A Subject that replays a specified number of previous values to new subscribers
  方法: next, subscribe, unsubscribe_all, buffer

### 函数

- **observable(event_name, priority**) - Decorator to create a simple observable function.
- **matches(self, data**) - Check if this subscription matches the given data.
- **call_count(self**) - Number of times this subscription has been called.
- **name(self**) - Get the observable name.
- **subscription_count(self**) - Get total number of active subscriptions.
- **subscribe(self, callback, event_name**, ...) - Subscribe to events.
- **subscribe_once(self, callback, event_name**, ...) - Subscribe to a single event emission.
- **unsubscribe(self, subscription**) - Unsubscribe a subscription.
- **unsubscribe_all(self, event_name**) - Unsubscribe all subscriptions, optionally for a specific event.
- **emit(self, data, event_name**, ...) - Emit an event to all subscribers.

... 共 47 个函数

## 使用示例

```python
from mod import observable

# 使用 observable
result = observable()
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
