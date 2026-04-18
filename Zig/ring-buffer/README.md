# Ring Buffer (环形缓冲区)

一个完整的 Zig 环形缓冲区实现，提供固定容量、可扩展和线程安全三种变体。

## 功能特性

### RingBuffer (固定容量)
- 固定容量，O(1) 推入和弹出
- 覆盖模式 (`pushOverwrite`)
- 查看/弹出操作
- 批量操作 (`pushSlice`, `popSlice`)
- 迭代器支持
- 元素查找 (`contains`, `indexOf`)
- 按索引删除 (`removeAt`)
- 零拷贝切片访问 (`asSlices`)

### BoundedRingBuffer (可扩展)
- 自动扩容 (直到最大容量)
- 动态内存管理
- 适合不确定数据规模的场景

### AtomicRingBuffer (线程安全)
- 基于自旋锁的线程安全实现
- 适合多线程生产者-消费者模式

## 安装

将此目录添加到你的 `build.zig.zon`:

```zig
.{
    .dependencies = .{
        .@"ring-buffer" = .{ .path = "path/to/ring-buffer" },
    },
}
```

在 `build.zig` 中:

```zig
const ring_buffer = b.dependency("ring-buffer", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("ring-buffer", ring_buffer.module("ring-buffer"));
```

## 快速开始

```zig
const std = @import("std");
const RingBuffer = @import("ring-buffer").RingBuffer;

pub fn main() !void {
    var buffer = try RingBuffer(i32).init(allocator, 10);
    defer buffer.deinit();

    // 推入元素
    try buffer.push(1);
    try buffer.push(2);
    try buffer.push(3);

    // 查看前端
    std.debug.print("前端: {}\n", .{buffer.peek().?});

    // 弹出元素
    while (buffer.pop()) |item| {
        std.debug.print("弹出: {}\n", .{item});
    }
}
```

## API 参考

### RingBuffer(T)

#### 初始化与清理

```zig
// 创建缓冲区
var buffer = try RingBuffer(i32).init(allocator, capacity);
defer buffer.deinit();

// 清空 (不释放内存)
buffer.clear();
```

#### 推入操作

```zig
// 普通推入 (满时返回错误)
try buffer.push(item);

// 覆盖推入 (满时覆盖最旧)
const was_overwritten = buffer.pushOverwrite(item);

// 批量推入
const pushed_count = buffer.pushSlice(items);
```

#### 弹出操作

```zig
// 弹出前端
const item = buffer.pop(); // ?T

// 批量弹出
var dest: [5]i32 = undefined;
const popped_count = buffer.popSlice(&dest);
```

#### 查看操作

```zig
// 查看前端
const front = buffer.peek(); // ?T

// 查看后端
const back = buffer.peekBack(); // ?T

// 查看指定索引
const item = buffer.peekAt(index); // ?T
```

#### 状态查询

```zig
const len = buffer.length();
const remaining = buffer.remaining();
const is_empty = buffer.isEmpty();
const is_full = buffer.isFull();
```

#### 查找操作

```zig
const found = buffer.contains(item);
const index = buffer.indexOf(item); // ?usize
```

#### 删除操作

```zig
const removed = buffer.removeAt(index); // ?T
```

#### 迭代器

```zig
var iter = buffer.iterator();
while (iter.next()) |item| {
    // 处理 item
}

// 重置迭代器
iter.reset();
```

#### 转换

```zig
// 转换为切片 (需释放内存)
const slice = try buffer.toSlice(allocator);
defer allocator.free(slice);

// 零拷贝切片访问
const slices = buffer.asSlices();
// slices[0] = 第一段连续数据
// slices[1] = 第二段连续数据 (环绕时)
```

### BoundedRingBuffer(T)

```zig
var buffer = try BoundedRingBuffer(i32).init(allocator, initial_capacity, max_capacity);
defer buffer.deinit();

// 自动扩容直到最大容量
try buffer.push(item);

// 其他 API 类似 RingBuffer
```

### AtomicRingBuffer(T)

```zig
var buffer = try AtomicRingBuffer(i32).init(allocator, capacity);
defer buffer.deinit();

// 线程安全操作
try buffer.push(item);
const item = buffer.pop();

// 状态查询
const len = buffer.length();
const is_empty = buffer.isEmpty();
const is_full = buffer.isFull();
```

## 使用场景

1. **日志缓冲区** - 保留最近的 N 条日志
2. **事件队列** - 生产者-消费者模式
3. **滑动窗口** - 计算移动平均值
4. **命令历史** - Shell 命令历史记录
5. **音频/视频缓冲** - 流媒体数据处理
6. **网络包缓冲** - 网络数据包队列

## 构建和测试

```bash
# 构建库
zig build

# 运行测试
zig build test

# 运行基础示例
zig build run-basic

# 运行高级示例
zig build run-advanced
```

## 测试覆盖

- 基本推入/弹出操作
- 覆盖模式
- 查看操作
- 环绕行为
- 批量操作
- 迭代器
- 查找和删除
- 字符串等复杂类型
- 大数据压力测试
- 线程安全测试

## 零依赖

本模块仅使用 Zig 标准库，无需任何外部依赖。

## 许可证

MIT