# Vector Clock Utilities

向量时钟工具模块 - 用于分布式系统中的因果追踪和冲突检测。

## 概述

向量时钟（Vector Clock）是分布式系统中用于捕获事件间因果关系的数据结构。本模块提供了完整的向量时钟实现，支持：

- **事件排序**：确定事件之间的因果关系（发生在...之前、发生在...之后、并发）
- **冲突检测**：识别分布式系统中的并发更新
- **版本追踪**：跟踪数据版本的历史
- **点版本向量**：更细粒度的因果追踪

## 功能特性

- ✅ 完整的 `VectorClock` 类
- ✅ 比较操作符（`<`, `>`, `<=`, `>=`, `==`）
- ✅ 事件关系判断（happens-before, concurrent）
- ✅ 点版本向量（Dotted Version Vector）
- ✅ 冲突检测工具
- ✅ 历史记录追踪
- ✅ JSON 序列化/反序列化
- ✅ 零外部依赖

## 快速开始

### 基本使用

```python
from vector_clock_utils.mod import VectorClock

# 创建向量时钟
vc1 = VectorClock({'A': 1, 'B': 0, 'C': 0})
vc2 = VectorClock({'A': 1, 'B': 2, 'C': 0})

# 检查因果关系
print(vc1.happens_before(vc2))  # True - vc1 发生在 vc2 之前
print(vc2.happens_after(vc1))   # True - vc2 发生在 vc1 之后

# 并发事件
vc3 = VectorClock({'A': 1, 'B': 0, 'C': 1})
vc4 = VectorClock({'A': 0, 'B': 1, 'C': 0})
print(vc3.concurrent_with(vc4))  # True - 并发事件
```

### 本地事件和消息传递

```python
from vector_clock_utils.mod import VectorClock

# 三个节点初始化
node_a = VectorClock({'A': 0, 'B': 0, 'C': 0})
node_b = VectorClock({'A': 0, 'B': 0, 'C': 0})
node_c = VectorClock({'A': 0, 'B': 0, 'C': 0})

# 节点 A 发生本地事件
node_a.increment('A')
print(node_a)  # VC:{A:1, B:0, C:0}

# 节点 A 发送消息给节点 B
node_b.merge(node_a)  # 接收消息
node_b.increment('B')  # 处理消息
print(node_b)  # VC:{A:1, B:1, C:0}

# 检查因果顺序
print(node_a.happens_before(node_b))  # True
```

### 冲突检测

```python
from vector_clock_utils.mod import VectorClock, detect_conflicts

# 两个并发更新
update1 = VectorClock({'A': 1, 'B': 0})
update2 = VectorClock({'A': 0, 'B': 1})

# 检测冲突
conflicts = detect_conflicts([
    ('update_1', update1),
    ('update_2', update2)
])
print(conflicts)  # [('update_1', 'update_2')]
```

### 点版本向量

```python
from vector_clock_utils.mod import DottedVersionVector

# 创建点版本向量
dvv = DottedVersionVector('A')

# 事件
dvv.increment()
print(dvv.dot)  # ('A', 1)

# 另一个节点
dvv2 = DottedVersionVector('B')
dvv2.increment()

# 合并
dvv.merge(dvv2)
print(dvv.vector)  # {'A': 1, 'B': 1}
```

### 历史追踪

```python
from vector_clock_utils.mod import VectorClock, VectorClockHistory

history = VectorClockHistory()

# 记录事件
history.record('event_1', VectorClock({'A': 1}), 'First event')
history.record('event_2', VectorClock({'A': 2}), 'Second event')
history.record('event_3', VectorClock({'A': 3}), 'Third event')

# 获取因果链
chain = history.get_causal_chain('event_3')
for event_id, clock, desc in chain:
    print(f"{event_id}: {clock} - {desc}")
```

## API 参考

### VectorClock 类

| 方法 | 说明 |
|------|------|
| `get(process_id)` | 获取进程计数器值 |
| `set(process_id, value)` | 设置进程计数器值 |
| `increment(process_id)` | 递增进程计数器 |
| `merge(other)` | 合并另一个向量时钟 |
| `happens_before(other)` | 判断是否发生在另一事件之前 |
| `happens_after(other)` | 判断是否发生在另一事件之后 |
| `concurrent_with(other)` | 判断是否与另一事件并发 |
| `copy()` | 创建深拷贝 |
| `to_dict()` / `from_dict()` | 字典转换 |
| `to_json()` / `from_json()` | JSON 序列化 |

### 辅助函数

| 函数 | 说明 |
|------|------|
| `compare_events(vc1, vc2)` | 比较两个事件关系 |
| `find_concurrent_events(clocks)` | 找出所有并发事件对 |
| `sort_by_causality(clocks)` | 按因果顺序排序 |
| `merge_all(clocks)` | 合并多个向量时钟 |
| `detect_conflicts(updates)` | 检测冲突更新 |
| `create_clock(*process_ids)` | 创建初始向量时钟 |

## 应用场景

1. **分布式数据库**：追踪数据版本，检测写入冲突
2. **协作编辑**：实现操作转换（OT）或 CRDT
3. **消息队列**：确保消息因果顺序
4. **分布式文件系统**：文件版本追踪
5. **版本控制系统**：类似 Git 的版本追踪

## 理论背景

向量时钟由 Colin Fidge (1988) 和 Friedemann Mattern (1988) 独立发明。它是 Lamport 时钟的扩展，可以准确检测并发事件。

### 发生在...之前关系

- 如果对于所有进程 i，vc1[i] ≤ vc2[i]，且至少存在一个进程 j 使得 vc1[j] < vc2[j]，则 vc1 发生在 vc2 之前
- 如果 vc1 和 vc2 都不发生在对方之前，则它们是并发的

## 许可证

MIT License

## 作者

AllToolkit Contributors