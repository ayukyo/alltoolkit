# Semaphore Utils

JavaScript 并发控制信号量工具集。零外部依赖，纯 JavaScript 实现。

## 功能列表

### 🚦 Semaphore（信号量）
- 控制并发访问数量
- 支持 `acquire()`、`release()`、`tryAcquire()`
- 支持超时控制
- 支持 `run()` 方法自动释放

### 🔒 Mutex（互斥锁）
- 二进制信号量，保护临界区
- 确保同一时间只有一个任务访问资源
- 支持 `tryAcquire()` 非阻塞获取

### 📖 ReadWriteLock（读写锁）
- 允许多个读操作同时进行
- 写操作独占访问
- 适合读多写少的场景（如缓存系统）

### 🔢 CountDownLatch（倒数门闩）
- 等待一组事件完成
- 可用于服务启动等待
- 支持超时控制

### 🚧 CyclicBarrier（循环屏障）
- 多个任务在屏障点同步
- 可重复使用
- 支持重置

### 📦 SemaphorePool（信号量池）
- 动态调整容量的信号量
- 支持运行时扩容

## 安装使用

```javascript
const {
  Semaphore,
  Mutex,
  ReadWriteLock,
  CountDownLatch,
  CyclicBarrier,
  SemaphorePool
} = require('./semaphore_utils/mod.js');
```

## 快速示例

### Semaphore - 限制并发数

```javascript
const sem = new Semaphore(3); // 最多3个并发

// 方式1: 手动获取/释放
await sem.acquire();
try {
  // 执行受限操作
} finally {
  sem.release();
}

// 方式2: 自动释放
await sem.run(async () => {
  // 执行受限操作
});
```

### Mutex - 保护共享资源

```javascript
const mutex = new Mutex();

let counter = 0;

const increment = async () => {
  await mutex.run(async () => {
    const temp = counter;
    await someAsyncOperation();
    counter = temp + 1;
  });
};
```

### ReadWriteLock - 缓存系统

```javascript
const rwLock = new ReadWriteLock();
const cache = new Map();

// 读取（多读并发）
const get = async (key) => {
  return rwLock.read(async () => {
    return cache.get(key);
  });
};

// 写入（独占）
const set = async (key, value) => {
  await rwLock.write(async () => {
    cache.set(key, value);
  });
};
```

### CountDownLatch - 等待多个任务

```javascript
const latch = new CountDownLatch(3);

// 在每个任务完成后
task1().then(() => latch.countDown());
task2().then(() => latch.countDown());
task3().then(() => latch.countDown());

// 等待所有完成
await latch.wait();
console.log('所有任务完成！');
```

### CyclicBarrier - 多任务同步

```javascript
const barrier = new CyclicBarrier(3);

const worker = async (id) => {
  // 第一阶段
  await phase1();
  await barrier.await(); // 等待其他 worker
  
  // 第二阶段
  await phase2();
  await barrier.await(); // 等待其他 worker
  
  // 所有阶段完成
};

await Promise.all([worker(1), worker(2), worker(3)]);
```

## API 参考

### Semaphore

| 方法 | 描述 |
|------|------|
| `constructor(permits)` | 创建信号量，指定并发数 |
| `acquire(timeout?)` | 获取许可，可选超时 |
| `release()` | 释放许可 |
| `tryAcquire()` | 非阻塞获取，返回布尔值 |
| `run(fn, timeout?)` | 执行函数并自动释放 |
| `available` | 当前可用许可数 |
| `total` | 总许可数 |
| `waiting` | 等待中的任务数 |

### Mutex

| 方法 | 描述 |
|------|------|
| `constructor()` | 创建互斥锁 |
| `acquire(timeout?)` | 获取锁 |
| `release()` | 释放锁 |
| `tryAcquire()` | 非阻塞获取 |
| `run(fn, timeout?)` | 执行函数并自动释放 |
| `isLocked` | 是否已锁定 |

### ReadWriteLock

| 方法 | 描述 |
|------|------|
| `acquireRead(timeout?)` | 获取读锁 |
| `releaseRead()` | 释放读锁 |
| `acquireWrite(timeout?)` | 获取写锁 |
| `releaseWrite()` | 释放写锁 |
| `read(fn, timeout?)` | 使用读锁执行函数 |
| `write(fn, timeout?)` | 使用写锁执行函数 |
| `getStatus()` | 获取当前状态 |

### CountDownLatch

| 方法 | 描述 |
|------|------|
| `constructor(count)` | 创建门闩，指定等待数 |
| `countDown()` | 计数减一 |
| `wait(timeout?)` | 等待计数归零 |
| `count` | 当前计数 |

### CyclicBarrier

| 方法 | 描述 |
|------|------|
| `constructor(parties)` | 创建屏障，指定参与者数 |
| `await(timeout?)` | 到达屏障并等待 |
| `reset()` | 重置屏障 |
| `parties` | 参与者数量 |
| `waiting` | 当前等待数 |
| `isBroken` | 是否已损坏 |

## 运行测试

```bash
node semaphore_utils_test.js
```

## 运行示例

```bash
node examples/usage_examples.js
```

## 特性

- ✅ 零外部依赖
- ✅ 完整的 API 文档
- ✅ 支持超时控制
- ✅ TypeScript 友好
- ✅ 完整的单元测试
- ✅ 实际应用示例

## 适用场景

- API 请求限流
- 数据库连接池管理
- 共享资源保护
- 批量任务处理
- 服务启动等待
- 多任务分阶段同步

## License

MIT