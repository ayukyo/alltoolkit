# Object Pool Utilities

高效的 Python 对象池实现，用于资源管理和复用。

## 功能特性

- **通用对象池模式** - 复用昂贵创建的对象
- **线程安全操作** - 支持多线程环境
- **对象验证** - 借用/归还时自动验证
- **自动空闲驱逐** - 清理长时间未使用的对象
- **池统计监控** - 详细的性能和使用统计
- **上下文管理器支持** - 自动归还借用对象
- **连接池** - 专为连接类资源设计
- **池管理器** - 管理多个命名池

## 安装使用

```python
from object_pool_utils import ObjectPool, ConnectionPool, PoolManager

# 创建对象池
pool = ObjectPool(
    factory=lambda: expensive_object,
    max_size=10
)

# 借用对象
obj = pool.borrow()

# 使用对象
result = obj.process()

# 归还对象
pool.return_object(obj)

# 或使用上下文管理器
with pool.use() as obj:
    result = obj.process()
```

## 核心类

### ObjectPool

通用对象池，适用于任何需要复用的对象类型。

```python
def create_resource():
    return {'id': id(object()), 'data': []}

pool = ObjectPool(
    factory=create_resource,          # 创建对象的工厂函数
    destructor=lambda r: r.clear(),   # 销毁对象的函数 (可选)
    validator=lambda r: r.get('valid'), # 验证对象的函数 (可选)
    reset=lambda r: r['data'].clear(),  # 重置对象的函数 (可选)
    max_size=10,                      # 最大对象数量
    min_idle=2,                       # 最小空闲对象数量
    max_idle_time=300,                # 空闲对象最大存活时间 (秒)
    borrow_timeout=30,                # 借用超时时间 (秒)
    validation_on_borrow=True,        # 借用时验证对象
    reset_on_return=True              # 归还时重置对象
)
```

### ConnectionPool

专为连接类资源设计的连接池。

```python
import socket

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('example.com', 80))
    return s

def close_socket(s):
    s.close()

def is_socket_alive(s):
    try:
        s.getpeername()
        return True
    except:
        return False

pool = ConnectionPool(
    factory=create_socket,
    destructor=close_socket,
    validator=is_socket_alive,
    max_size=10,
    max_lifetime=3600,    # 连接最大生命周期 (秒)
    max_usage_count=1000  # 最大使用次数
)

# 健康检查
health = pool.health_check()
print(f"健康连接: {health['healthy']}")
```

### PoolManager

管理多个命名池。

```python
manager = PoolManager()

# 创建多个池
manager.create_pool('database', factory=db_factory, max_size=10)
manager.create_pool('cache', factory=cache_factory, max_size=20)
manager.create_pool('http', factory=http_factory, max_size=5)

# 使用命名池
with manager.use('database') as conn:
    conn.execute("SELECT * FROM users")

# 获取所有统计
stats = manager.get_all_stats()
for name, stat in stats.items():
    print(f"{name}: {stat.total_borrowed} borrows")

# 关闭所有池
manager.close_all()
```

## 统计信息

```python
stats = pool.get_stats()

print(f"创建对象数: {stats.total_created}")
print(f"销毁对象数: {stats.total_destroyed}")
print(f"借用次数: {stats.total_borrowed}")
print(f"归还次数: {stats.total_returned}")
print(f"验证失败数: {stats.total_validation_failures}")
print(f"当前空闲: {stats.current_idle}")
print(f"当前活跃: {stats.current_active}")
print(f"最大并发借用: {stats.max_borrowed_at_once}")
print(f"平均等待时间: {stats.avg_wait_time_ms}ms")
print(f"利用率: {stats.utilization_rate:.2%}")
```

## 预定义资源类

```python
from object_pool_utils import PooledStringBuilder, PooledList, PooledDict

# 可池化的字符串构建器
sb = PooledStringBuilder()
sb.append("Hello").append(" ").append("World")
text = sb.build()  # "Hello World"
sb.clear()         # 重置以便复用

# 可池化的列表
pl = PooledList([1, 2, 3])
pl.reset()  # 清空列表

# 可池化的字典
pd = PooledDict({'a': 1})
pd.reset()  # 清空字典
```

## 便捷函数

```python
from object_pool_utils import create_pool, create_connection_pool

# 快速创建对象池
pool = create_pool(factory=my_factory, max_size=10)

# 快速创建连接池
conn_pool = create_connection_pool(
    factory=my_conn_factory,
    destructor=my_destructor,
    validator=my_validator,
    max_size=5
)
```

## 使用场景

1. **数据库连接池** - 复用数据库连接，避免频繁创建
2. **HTTP 连接池** - 复用 HTTP 会话
3. **线程池** - 复用工作线程
4. **缓存对象池** - 复用大型缓存结构
5. **资源池** - 复用任何昂贵的资源

## 设计特点

- **零外部依赖** - 仅使用 Python 标准库
- **线程安全** - 使用 threading.RLock 保护内部状态
- **自动清理** - 支持空闲对象自动驱逐
- **生命周期管理** - 连接池支持最大生命周期和最大使用次数
- **灵活配置** - 支持验证、重置、销毁等回调

## 测试

```bash
python object_pool_utils_test.py
```

## 示例

```bash
python examples/basic_usage.py
```

## 许可证

MIT License