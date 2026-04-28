# Queue Utils 📋

Lua 队列数据结构工具模块 - 零依赖，生产就绪

## 简介

提供全面的队列数据结构实现，包括：
- **Queue**: 标准队列 (FIFO)
- **Deque**: 双端队列
- **Priority Queue**: 优先队列（最小/最大堆）
- **Circular Queue**: 固定容量循环队列
- **Stack**: 栈 (LIFO)

所有实现均使用 Lua 标准库，零外部依赖。

## 安装

```lua
local queue_utils = require("mod")
```

## 快速开始

### 1. 普通队列 (Queue)

```lua
local q = queue_utils.new()
q:push(1):push(2):push(3)

print(q:peek())  -- 1
print(q:pop())   -- 1
print(q:size())  -- 2
print(q:is_empty())  -- false
```

### 2. 双端队列 (Deque)

```lua
local d = queue_utils.new_deque()
d:push_front(0)
d:push_back(1)

print(d:peek_front())  -- 0
print(d:peek_back())   -- 1
print(d:pop_front())   -- 0
print(d:pop_back())    -- 1

-- 支持旋转和反转
d:rotate(2)
d:reverse()
```

### 3. 优先队列 (Priority Queue)

```lua
-- 最小优先队列
local min_q = queue_utils.new_min_queue()
min_q:push(50):push(20):push(80)
print(min_q:pop())  -- 20 (最小值)

-- 最大优先队列
local max_q = queue_utils.new_max_queue()
max_q:push(50):push(20):push(80)
print(max_q:pop())  -- 80 (最大值)

-- 自定义比较函数
local pq = queue_utils.new_priority(function(a, b)
    return a.priority < b.priority
end)
pq:push({name = "task", priority = 1})
```

### 4. 循环队列 (Circular Queue)

```lua
local cq = queue_utils.new_circular(3)  -- 容量为 3

cq:push(1)  -- true
cq:push(2)  -- true
cq:push(3)  -- true
cq:push(4)  -- false (队列已满)

print(cq:pop())  -- 1
print(cq:is_full())  -- false
```

### 5. 栈 (Stack)

```lua
local s = queue_utils.new_stack()
s:push(1):push(2):push(3)

print(s:peek())  -- 3 (栈顶)
print(s:pop())   -- 3
print(s:pop())   -- 2
```

## API 文档

### Queue 方法

| 方法 | 描述 | 返回值 |
|------|------|--------|
| `push(value)` | 向队列尾部添加元素 | 队列自身 |
| `pop()` | 从队列头部移除元素 | 移除的元素或 nil |
| `peek()` | 查看队列头部元素 | 头部元素或 nil |
| `size()` | 获取队列大小 | 元素数量 |
| `is_empty()` | 检查队列是否为空 | boolean |
| `clear()` | 清空队列 | 队列自身 |
| `to_array()` | 将队列转换为数组 | 数组 |
| `iterate()` | 返回迭代器函数 | iterator |

### Deque 方法

| 方法 | 描述 | 返回值 |
|------|------|--------|
| `push_front(value)` | 向头部添加元素 | deque 自身 |
| `push_back(value)` | 向尾部添加元素 | deque 自身 |
| `pop_front()` | 从头部移除元素 | 元素或 nil |
| `pop_back()` | 从尾部移除元素 | 元素或 nil |
| `peek_front()` | 查看头部元素 | 元素或 nil |
| `peek_back()` | 查看尾部元素 | 元素或 nil |
| `rotate(steps)` | 旋转队列 | deque 自身 |
| `reverse()` | 反转队列 | deque 自身 |

### Priority Queue 方法

| 方法 | 描述 | 返回值 |
|------|------|--------|
| `push(value)` | 添加元素 | pq 自身 |
| `pop()` | 移除最高优先级元素 | 元素或 nil |
| `peek()` | 查看最高优先级元素 | 元素或 nil |
| `size()` | 获取大小 | 元素数量 |
| `is_empty()` | 检查是否为空 | boolean |
| `clear()` | 清空队列 | pq 自身 |

### Circular Queue 方法

| 方法 | 描述 | 返回值 |
|------|------|--------|
| `push(value)` | 添加元素 | boolean (成功/失败) |
| `pop()` | 移除元素 | 元素或 nil |
| `peek()` | 查看头部元素 | 元素或 nil |
| `size()` | 当前元素数量 | number |
| `capacity()` | 队列容量 | number |
| `is_empty()` | 检查是否为空 | boolean |
| `is_full()` | 检查是否已满 | boolean |

### Stack 方法

| 方法 | 描述 | 返回值 |
|------|------|--------|
| `push(value)` | 向栈添加元素 | stack 自身 |
| `pop()` | 从栈移除元素 | 元素或 nil |
| `peek()` | 查看栈顶元素 | 元素或 nil |
| `size()` | 获取栈大小 | 元素数量 |
| `is_empty()` | 检查栈是否为空 | boolean |
| `clear()` | 清空栈 | stack 自身 |

### 辅助函数

| 函数 | 描述 | 返回值 |
|------|------|--------|
| `new_min_queue()` | 创建最小优先队列 | 优先队列 |
| `new_max_queue()` | 创建最大优先队列 | 优先队列 |
| `new_weighted_queue()` | 创建带优先级元素的队列 | 优先队列 |
| `from_array(arr)` | 从数组创建队列 | Queue |
| `stack_from_array(arr)` | 从数组创建栈 | Stack |
| `contains(q, value)` | 检查元素是否在队列中 | boolean |
| `index_of(q, value)` | 查找元素索引 | 索引或 nil |

## 特性

✅ **零依赖** - 仅使用 Lua 标准库
✅ **面向对象设计** - 每个数据结构都是一个对象
✅ **链式调用** - 支持 `q:push(1):push(2):push(3)`
✅ **完整测试** - 55 个单元测试全部通过
✅ **内存效率** - 使用索引管理避免内存泄漏

## 测试

```bash
lua queue_utils_test.lua
```

## 示例

```bash
lua examples/basic_usage.lua
```

## 版本

- Version: 1.0.0
- Author: AllToolkit
- License: MIT
- Date: 2026-04-29