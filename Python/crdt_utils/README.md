# CRDT Utils 🔄

无冲突复制数据类型（CRDT）工具模块，用于分布式系统中的最终一致性数据处理。

## 功能特性

- **VectorClock** - 向量时钟，用于分布式因果排序
- **GCounter** - 只增计数器（G-Counter）
- **PNCounter** - 增减计数器（PN-Counter）
- **GSet** - 只增集合（G-Set）
- **TwoPSet** - 两阶段集合（Two-Phase Set）
- **LWWRegister** - Last-Write-Wins 寄存器
- **ORSet** - 可观察可删除集合（Observed-Remove Set）
- **LWWElementSet** - LWW 元素集合
- **CRDTMap** - CRDT 映射容器
- **JSONCRDT** - JSON 格式的 CRDT
- **零外部依赖** - 纯 Python 实现

## 概念

CRDT（Conflict-free Replicated Data Types）是一种特殊的数据结构，设计用于在分布式系统中实现最终一致性，无需协调即可合并多个副本的更新。

## 快速开始

```python
from crdt_utils import (
    GCounter, PNCounter, GSet, TwoPSet,
    LWWRegister, ORSet, VectorClock
)

# 创建节点 ID
from crdt_utils import generate_node_id
node_a = generate_node_id()
node_b = generate_node_id()

# G-Counter：只增计数器
counter = GCounter(node_a)
counter.increment(node_a)
counter.increment(node_a)
print(counter.value)  # 2

# 合并两个 counter
counter2 = GCounter(node_b)
counter2.increment(node_b)
counter.merge(counter2)
print(counter.value)  # 3
```

## VectorClock（向量时钟）

```python
from crdt_utils import VectorClock, generate_node_id

node_a = generate_node_id()
node_b = generate_node_id()

# 创建向量时钟
clock = VectorClock()
clock.increment(node_a)
clock.increment(node_b)
print(clock.get(node_a))  # 1
print(clock.get(node_b))  # 1

# 比较因果关系
clock2 = VectorClock()
clock2.increment(node_a)
print(clock.happened_before(clock2))  # False 或 True 取决于具体实现

# 合并
clock.merge(clock2)
```

## GCounter（只增计数器）

```python
from crdt_utils import GCounter, generate_node_id

node_a = generate_node_id()
node_b = generate_node_id()

# 创建计数器
counter = GCounter(node_a)

# 递增
counter.increment(node_a)
counter.increment(node_a)
counter.increment(node_b)  # 从不同节点

print(counter.value)  # 3

# 合并
other = GCounter(node_b)
other.increment(node_b)
counter.merge(other)
print(counter.value)  # 4
```

## PNCounter（增减计数器）

```python
from crdt_utils import PNCounter, generate_node_id

node_a = generate_node_id()
node_b = generate_node_id()

counter = PNCounter(node_a)
counter.increment(node_a)  # +1
counter.decrement(node_a)  # -1
counter.increment(node_b)

print(counter.value)  # 1

# 合并
other = PNCounter(node_b)
other.decrement(node_b)
counter.merge(other)
print(counter.value)  # 0
```

## GSet（只增集合）

```python
from crdt_utils import GSet

# 创建集合
s = GSet()
s.add("apple")
s.add("banana")
s.add("apple")  # 重复添加被忽略

print(s.value)  # {'apple', 'banana'}
print("apple" in s.value)  # True
print("orange" in s.value)  # False

# 合并
other = GSet()
other.add("orange")
other.add("banana")  # banana 已存在
s.merge(other)
print(s.value)  # {'apple', 'banana', 'orange'}
```

## TwoPSet（两阶段集合）

```python
from crdt_utils import TwoPSet

# 创建集合
s = TwoPSet()
s.add("apple")
s.add("banana")
s.add("cherry")

# 删除（删除后不能再添加回来）
s.remove("banana")

print(s.value)  # {'apple', 'cherry'}

# 合并
other = TwoPSet()
other.add("banana")  # 被删除的不能再添加
other.add("date")
s.merge(other)
print(s.value)  # {'apple', 'cherry', 'date'}
```

## LWWRegister（最后写入胜出寄存器）

```python
from crdt_utils import LWWRegister, generate_node_id
import time

node_a = generate_node_id()

# 创建寄存器
reg = LWWRegister(node_a)
reg.set("initial")

# 更新
reg.set("updated")

print(reg.value)  # 'updated'

# 时间戳更新
reg.set("newer", timestamp=time.time() + 10)

# 合并（时间戳更大的获胜）
other = LWWRegister(generate_node_id())
other.set("conflicting", timestamp=time.time() + 5)
reg.merge(other)
print(reg.value)  # 'newer' (时间戳更大)
```

## ORSet（可观察可删除集合）

```python
from crdt_utils import ORSet

# 创建集合
s = ORSet()
s.add("apple")
s.add("banana")
tag = s.add("cherry")  # 返回 tag

print(s.value)  # {'apple', 'banana', 'cherry'}

# 删除（使用 tag）
s.remove("cherry", tag=tag)
print(s.value)  # {'apple', 'banana'}

# 合并
other = ORSet()
other.add("cherry")  # 新增 cherry
s.merge(other)
print(s.value)  # {'apple', 'banana', 'cherry'}
```

## LWWElementSet（LWW 元素集合）

```python
from crdt_utils import LWWElementSet
import time

s = LWWElementSet()
s.add("apple")
s.add("banana")
s.remove("banana")  # 基于 LWW 删除

print(s.value)  # {'apple'}

# 合并（带时间戳）
other = LWWElementSet()
other.add("cherry")
s.merge(other)
print(s.value)  # {'apple', 'cherry'}
```

## CRDTMap

```python
from crdt_utils import CRDTMap, GSet, LWWRegister

# 创建 CRDT 映射
m = CRDTMap()

# 设置值
m["counter"] = GSet()
m["name"] = LWWRegister()

# 添加到 GSet
m["counter"].add("item1")
m["counter"].add("item2")

# 设置寄存器
m["name"].set("Alice")

# 合并
other = CRDTMap()
other["counter"] = GSet()
other["counter"].add("item3")
m.merge(other)
```

## JSONCRDT

```python
from crdt_utils import JSONCRDT

# 创建 JSON CRDT
j = JSONCRDT()
j.set("name", "Alice")
j.set("age", 30)
j.set("tags", ["developer", "python"])

print(j.to_json())
# {'name': {'value': 'Alice', 'timestamp': ...}, 'age': {...}, 'tags': [...]}

# 合并
other = JSONCRDT()
other.set("name", "Bob")  # 不同的值
other.set("city", "NYC")
j.merge(other)
```

## 工具函数

```python
from crdt_utils import generate_node_id, crdt_hash, merge_all

# 生成唯一节点 ID
node_id = generate_node_id()

# 计算 CRDT 哈希
counter = GCounter(node_id)
counter.increment(node_id)
h = crdt_hash(counter)

# 合并多个 CRDT
all_merged = merge_all([counter1, counter2, counter3])
```

## 主要类

| 类 | 说明 | 特性 |
|---|------|------|
| `VectorClock` | 向量时钟 | 因果排序 |
| `GCounter` | G-计数器 | 只增 |
| `PNCounter` | PN-计数器 | 增减 |
| `GSet` | G-集合 | 只增 |
| `TwoPSet` | 2P-集合 | 添加+删除 |
| `LWWRegister` | LWW-寄存器 | 最后写入胜出 |
| `ORSet` | OR-集合 | 可观察删除 |
| `LWWElementSet` | LWW-元素集合 | LWW 删除 |
| `CRDTMap` | CRDT-映射 | 容器 |
| `JSONCRDT` | JSON-CRDT | JSON 序列化 |

## 测试

```bash
python -m pytest Python/crdt_utils/ -v
```

## 许可证

MIT License