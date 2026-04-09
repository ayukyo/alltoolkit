# AllToolkit - TypeScript Event Bus 🚌

**零依赖事件总线 - 生产就绪**

---

## 📖 概述

`event_bus` 提供一个功能完整的事件总线实现，支持同步和异步事件处理、通配符匹配、一次性监听器、优先级执行、事件过滤等功能。完全使用 TypeScript 标准库实现，无需任何外部依赖。

适用于 Deno、Bun、Node.js 等 TypeScript 运行环境。

---

## ✨ 特性

- **零依赖** - 仅使用 TypeScript 标准库
- **通配符支持** - `*` 匹配单层，`**` 匹配多层
- **一次性监听器** - `once()` 方法，自动移除
- **优先级执行** - 高优先级监听器先执行
- **事件过滤** - 基于条件的选择性执行
- **异步支持** - 完美处理 async/await 监听器
- **事件历史** - 可查询历史事件记录
- **暂停/恢复** - 支持事件队列和批量处理
- **类型安全** - 完整的 TypeScript 类型支持
- **统计追踪** - 内置事件和监听器统计

---

## 🚀 快速开始

### 基础使用

```typescript
import { EventBus } from './mod.ts';

const bus = new EventBus();

// 订阅事件
bus.on('user:login', (data) => {
  console.log(`User ${data.username} logged in`);
});

// 发布事件
bus.emit('user:login', { username: 'john', id: 123 });

// 订阅一次性事件
bus.once('user:logout', (data) => {
  console.log('User logged out');
});

// 取消订阅
const unsubscribe = bus.on('event', handler);
unsubscribe(); // 移除该监听器
```

### 通配符订阅

```typescript
// 单层通配符 (*)
bus.on('user:*', (data, eventName) => {
  console.log(`User event: ${eventName}`);
});
// 匹配：user:login, user:logout, user:created
// 不匹配：user:admin:login

// 多层通配符 (**)
bus.on('app:**', (data, eventName) => {
  console.log(`App event: ${eventName}`);
});
// 匹配：app:start, app:user:login, app:user:profile:update
```

### 优先级和过滤

```typescript
// 优先级（数字越大优先级越高）
bus.on('order:created', highPriorityHandler, { priority: 10 });
bus.on('order:created', lowPriorityHandler, { priority: 1 });

// 过滤器（只有满足条件才执行）
bus.on('order:created', handler, {
  filter: (data) => data.amount > 100
});

// 组合使用
bus.on('vip:order', handler, {
  priority: 10,
  filter: (data) => data.amount > 1000,
  once: true  // 一次性监听器
});
```

---

## 📚 API 参考

### 构造函数

```typescript
new EventBus(maxHistorySize?: number)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `maxHistorySize` | `number` | `100` | 最大历史事件数量 |

### 订阅方法

#### `on()` - 订阅事件

```typescript
on<T>(
  eventName: string,
  callback: (data: T, eventName: string) => void | Promise<void>,
  options?: {
    priority?: number;
    filter?: (data: T, eventName: string) => boolean;
    once?: boolean;
  }
): () => void  // 返回取消订阅函数
```

#### `once()` - 订阅一次性事件

```typescript
once<T>(
  eventName: string,
  callback: (data: T, eventName: string) => void | Promise<void>,
  options?: {
    priority?: number;
    filter?: (data: T, eventName: string) => boolean;
  }
): () => void
```

### 取消订阅方法

#### `off()` - 取消订阅

```typescript
// 取消特定监听器
off(eventName: string, callback: Function): number

// 取消事件的所有监听器
off(eventName: string): number

// 取消所有监听器
off(): number
```

返回值为移除的监听器数量。

### 发布方法

#### `emit()` - 发布事件（异步）

```typescript
async emit<T>(
  eventName: string,
  data: T,
  source?: string
): Promise<void>
```

#### `emitSync()` - 发布事件（同步）

```typescript
emitSync<T>(
  eventName: string,
  data: T,
  source?: string
): void
```

⚠️ 不等待异步监听器完成，已废弃，建议使用 `emit()`。

### 历史管理

#### `getHistory()` - 获取历史事件

```typescript
getHistory(limit?: number, eventName?: string): EventData[]
```

#### `clearHistory()` - 清除历史

```typescript
clearHistory(eventName?: string): void
```

### 暂停/恢复

#### `suspend()` - 暂停事件

```typescript
suspend(): void
```

#### `resume()` - 恢复事件

```typescript
async resume(clearPending?: boolean): Promise<void>
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `clearPending` | `boolean` | `false` | 是否清除待处理事件 |

#### `isSuspended()` - 检查暂停状态

```typescript
isSuspended(): boolean
```

#### `getPendingCount()` - 获取待处理事件数

```typescript
getPendingCount(): number
```

### 统计和查询

#### `getStats()` - 获取统计信息

```typescript
getStats(): EventBusStats
```

返回：
```typescript
interface EventBusStats {
  totalEvents: number;           // 总事件数
  totalListeners: number;        // 总监听器数
  eventsByType: Record<string, number>;  // 按类型统计
  activeListeners: Record<string, number>; // 按事件统计监听器
}
```

#### `getListenerCount()` - 获取监听器数量

```typescript
getListenerCount(eventName: string): number
```

#### `getEventNames()` - 获取所有事件名

```typescript
getEventNames(): string[]
```

#### `hasListeners()` - 检查是否有监听器

```typescript
hasListeners(eventName: string): boolean
```

### 清理

#### `destroy()` - 销毁事件总线

```typescript
destroy(): void
```

移除所有监听器，清除历史，重置统计。

---

## 📋 数据类型

### EventData

```typescript
interface EventData<T = any> {
  name: string;        // 事件名称
  data: T;            // 事件数据
  timestamp: number;  // 时间戳
  source?: string;    // 事件来源（可选）
}
```

### ListenerConfig

```typescript
interface ListenerConfig {
  callback: EventCallback;  // 回调函数
  filter?: EventFilter;     // 过滤器（可选）
  once: boolean;           // 是否一次性
  priority: number;        // 优先级
}
```

---

## 💡 使用场景

### 1. 组件间通信

```typescript
// 事件总线作为全局通信中心
const eventBus = new EventBus();

// 组件 A 发布事件
eventBus.emit('cart:updated', { itemId: 123, quantity: 2 });

// 组件 B 订阅事件
eventBus.on('cart:updated', (data) => {
  updateCartDisplay(data);
});

// 组件 C 也订阅同一事件
eventBus.on('cart:updated', (data) => {
  recalculateTotal(data);
});
```

### 2. 日志系统

```typescript
// 日志事件总线
const logger = new EventBus();

// 订阅所有日志事件
logger.on('log:**', (data, eventName) => {
  console.log(`[${eventName}] ${data.message}`);
});

// 发布日志
logger.emit('log:error', { message: 'Something went wrong' });
logger.emit('log:warn', { message: 'Low disk space' });
logger.emit('log:info', { message: 'Server started' });
```

### 3. 状态管理

```typescript
class Store {
  private state: Record<string, any> = {};
  private bus = new EventBus();

  setState(key: string, value: any) {
    this.state[key] = value;
    this.bus.emit(`state:${key}`, value);
  }

  subscribe(key: string, callback: (value: any) => void) {
    return this.bus.on(`state:${key}`, callback);
  }

  getState(key: string) {
    return this.state[key];
  }
}

// 使用
const store = new Store();
store.subscribe('user', (user) => {
  console.log('User updated:', user);
});
store.setState('user', { name: 'John' });
```

### 4. 插件系统

```typescript
class PluginSystem {
  private bus = new EventBus();

  registerPlugin(name: string, plugin: any) {
    this.bus.emit('plugin:registered', { name, plugin });
  }

  onPlugin(event: string, callback: Function) {
    return this.bus.on(`plugin:${event}`, callback);
  }

  async initialize() {
    // 等待所有插件注册完成
    await this.bus.emit('system:init', {});
  }
}
```

### 5. 批量处理

```typescript
const bus = new EventBus();

// 暂停事件处理
bus.suspend();

// 批量发布事件（不会立即触发监听器）
for (const item of items) {
  bus.emit('item:processed', item);
}

console.log(`Pending events: ${bus.getPendingCount()}`);

// 恢复处理（一次性触发所有待处理事件）
await bus.resume();
```

### 6. 事件溯源

```typescript
const bus = new EventBus(1000); // 保留 1000 个历史事件

// 记录所有事件
bus.on('**', (data, eventName) => {
  saveToDatabase({ event: eventName, data, time: Date.now() });
});

// 回放历史事件
const history = bus.getHistory();
for (const event of history) {
  replay(event);
}
```

### 7. 类型安全事件

```typescript
// 定义事件类型映射
interface AppEvents {
  'user:login': { username: string; id: number };
  'user:logout': { id: number };
  'order:created': { orderId: string; amount: number };
  'order:shipped': { orderId: string; trackingId: string };
}

// 创建类型化事件总线
const bus = createTypedEventBus<AppEvents>();

// TypeScript 会检查事件数据类型
bus.on('user:login', (data) => {
  console.log(data.username); // ✅ 类型安全
  // console.log(data.invalid); // ❌ 编译错误
});

bus.emit('user:login', { username: 'john', id: 123 }); // ✅
bus.emit('user:login', { invalid: 'data' }); // ❌ 编译错误
```

---

## 🧪 运行测试

### Deno

```bash
cd event_bus
deno run --allow-read event_bus_test.ts
```

### Bun

```bash
bun run event_bus_test.ts
```

### Node.js

```bash
# 编译 TypeScript
npx tsc event_bus_test.ts --target ES2020 --module commonjs

# 运行测试
node event_bus_test.js
```

### 测试覆盖

- ✅ 基础订阅和发布
- ✅ 多监听器支持
- ✅ 一次性监听器
- ✅ 取消订阅
- ✅ 通配符匹配（* 和 **）
- ✅ 优先级执行
- ✅ 事件过滤
- ✅ 事件历史
- ✅ 暂停/恢复
- ✅ 统计信息
- ✅ 异步监听器
- ✅ 错误处理
- ✅ 边界情况
- ✅ 类型化事件总线

---

## ⚠️ 注意事项

1. **内存管理**: 不再需要的事件总线请调用 `destroy()` 清理
2. **错误处理**: 监听器中的错误不会影响其他监听器，但会被记录到控制台
3. **异步执行**: 使用 `emit()` 而非 `emitSync()` 以确保异步监听器完成
4. **通配符性能**: 大量通配符监听器可能影响性能
5. **历史大小**: 根据内存限制合理设置 `maxHistorySize`

---

## 📁 文件结构

```
event_bus/
├── mod.ts                      # 主要实现
├── event_bus_test.ts           # 测试套件 (35+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.ts          # 基础使用示例
    └── advanced_example.ts     # 高级使用示例
```

---

## 🔗 相关链接

- [TypeScript 文档](https://www.typescriptlang.org/docs/)
- [Deno 文档](https://deno.land/manual)
- [Bun 文档](https://bun.sh/docs)
- [事件总线模式](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
