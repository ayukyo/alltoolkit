# Pub/Sub Utilities

零依赖的发布-订阅模式实现，支持多种匹配模式、消息过滤、优先级排序和异步处理。

## 特性

- **多种匹配模式**: 精确匹配、前缀匹配、通配符匹配、正则表达式匹配
- **消息过滤**: 可选的过滤函数进一步筛选消息
- **优先级排序**: 高优先级的订阅者优先处理
- **异步处理**: 支持同步、异步和发后即忘三种交付模式
- **统计追踪**: 完整的消息统计和订阅统计
- **线程安全**: 所有操作都支持多线程并发
- **EventEmitter**: 简化的事件发射器模式

## 快速开始

### 基本使用

```python
from pub_sub_utils import PubSub

broker = PubSub()

# 订阅
broker.subscribe('user.created', lambda msg: print(f"User: {msg}"))

# 发布
broker.publish('user.created', {'id': 1, 'name': 'Alice'})
```

### 通配符订阅

```python
# 单级通配符 (*)
broker.subscribe('user.*', handler, match_mode=MatchMode.WILDCARD)

# 多级通配符 (>)
broker.subscribe('order.>', handler, match_mode=MatchMode.WILDCARD)
```

### 装饰器语法

```python
@subscribe('app.event')
def handle_app_event(payload):
    print(f"Event: {payload}")
```

### EventEmitter 模式

```python
from pub_sub_utils import EventEmitter

emitter = EventEmitter()

@emitter.on('data')
def handler(data):
    print(f"Data: {data}")

emitter.emit('data', {'value': 42})
```

## API 参考

### PubSub 类

| 方法 | 说明 |
|------|------|
| `subscribe(topic, handler, ...)` | 订阅主题，返回订阅ID |
| `unsubscribe(subscriber_id)` | 取消订阅 |
| `publish(topic, payload, ...)` | 发布消息 |
| `pause_subscription(id)` | 暂停订阅 |
| `resume_subscription(id)` | 恢复订阅 |
| `get_stats()` | 获取统计信息 |

### MatchMode 匹配模式

- `EXACT`: 精确匹配
- `PREFIX`: 前缀匹配
- `WILDCARD`: 通配符匹配 (`*` 单级, `>` 多级)
- `REGEX`: 正则表达式匹配

### DeliveryMode 交付模式

- `SYNC`: 同步处理
- `ASYNC`: 异步线程池处理
- `FIRE_FORGET`: 发后即忘

## 测试

```bash
python pub_sub_utils_test.py
```

## 示例

```bash
python examples/usage_examples.py
```

## 许可证

MIT License