# Memory Pool Utils - 内存池工具集 🧠

高效的内存管理和对象复用工具，零外部依赖，线程安全。

## 功能

- **MemoryPool**: 通用内存池，支持块分配和释放
- **ObjectPool**: 对象池，支持对象复用，减少 GC 压力
- **BufferPool**: 缓冲区池，适合网络 I/O 场景
- **ArenaAllocator**: Arena 分配器，批量释放内存
- **FixedSizeAllocator**: 固定大小块分配器，零碎片
- **StringBuilder**: 基于内存池的字符串构建器

## 快速开始

### MemoryPool - 基本内存池

```python
from memory_pool_utils import MemoryPool

# 创建 256 字节大小的内存池
pool = MemoryPool(256, initial_blocks=10)

# 获取内存块
block = pool.acquire()
block[:5] = b"Hello"

# 释放内存块
pool.release(block)

# 查看池状态
print(f"可用: {pool.available}, 使用中: {pool.in_use}")
```

### ObjectPool - 对象池

```python
from memory_pool_utils import ObjectPool

# 定义对象工厂和重置函数
def create_user():
    return {'id': 0, 'name': '', 'active': False}

def reset_user(obj):
    obj['id'] = 0
    obj['name'] = ''
    obj['active'] = False

# 创建对象池
pool = ObjectPool(
    factory=create_user,
    reset=reset_user,
    initial_size=5
)

# 获取对象
user = pool.acquire()
user['id'] = 1
user['name'] = 'Alice'
user['active'] = True

# 释放对象（自动重置）
pool.release(user)
print(user)  # {'id': 0, 'name': '', 'active': False}
```

### BufferPool - 缓冲区池

```python
from memory_pool_utils import BufferPool

# 创建缓冲区池
pool = BufferPool()

# 获取适合大小的缓冲区
buf = pool.get(256)  # 自动选择最接近的大小等级
buf[:10] = b"data..."

# 放回缓冲区
pool.put(buf)

# 查看统计
print(pool.stats)
```

### ArenaAllocator - Arena 分配器

```python
from memory_pool_utils import ArenaAllocator

# 创建 Arena（批量释放）
arena = ArenaAllocator(10240)  # 10KB

# 分配多个缓冲区
buf1 = arena.alloc(100)
buf2 = arena.alloc(200)
buf3 = arena.alloc(150)

print(f"已使用: {arena.used}/{arena.total_size}")

# 一次性释放所有
arena.reset()  # 所有分配瞬间释放
```

### StringBuilder - 字符串构建器

```python
from memory_pool_utils import MemoryPool, StringBuilder

pool = MemoryPool(512)
sb = StringBuilder(pool)

# 高效追加文本
sb.append("Hello").append(", ").append("World!")
result = sb.build()  # "Hello, World!"

# 清空并复用内存
sb.clear()
```

## 使用场景

- 🎮 游戏开发中的对象管理（子弹、敌人、特效）
- 🌐 网络编程中的缓冲区管理（Socket、HTTP）
- 🔄 高频创建销毁对象的场景（减少 GC 压力）
- ⏱️ 实时系统中的内存管理（确定性性能）
- 📊 大数据处理中的临时缓冲区

## 线程安全

所有池实现都支持线程安全操作：

```python
import threading

pool = MemoryPool(256, initial_blocks=100)

def worker():
    for _ in range(50):
        block = pool.acquire()
        # 使用块...
        pool.release(block)

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()

print(pool.available)  # 100 - 所有块都归还了
```

## API 参考

### MemoryPool

| 方法 | 描述 |
|------|------|
| `acquire()` | 获取内存块 |
| `release(block)` | 释放内存块 |
| `clear()` | 清空未使用的块 |
| `available` | 可用块数量 |
| `in_use` | 使用中块数量 |
| `utilization` | 利用率 (0.0-1.0) |

### ObjectPool

| 方法 | 描述 |
|------|------|
| `acquire()` | 获取对象 |
| `release(obj)` | 释放并重置对象 |
| `available` | 可用对象数量 |
| `in_use` | 使用中对象数量 |

### BufferPool

| 方法 | 描述 |
|------|------|
| `get(size)` | 获取指定大小的缓冲区 |
| `put(buf)` | 放回缓冲区 |
| `stats` | 统计信息（gets/puts/misses） |
| `clear()` | 清空所有缓冲区 |

## 测试

```bash
python memory_pool_utils_test.py
```

**测试覆盖**: 41 个测试用例，100% 通过 ✅

---

*最后更新: 2026-05-12*