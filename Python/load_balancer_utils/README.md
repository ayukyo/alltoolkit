# Load Balancer Utilities

多样化的负载均衡算法实现，零外部依赖，仅使用 Python 标准库。

## 功能特性

- **轮询 (Round Robin)**: 简单轮询，依次分配
- **加权轮询 (Weighted Round Robin)**: 按权重比例分配
- **最少连接 (Least Connections)**: 分配给连接数最少的服务器
- **随机 (Random)**: 随机选择服务器
- **加权随机 (Weighted Random)**: 按权重随机选择
- **IP 哈希 (IP Hash)**: 基于 key 的一致性哈希路由

### 额外特性

- 线程安全操作
- 连接追踪
- 健康检查集成
- 服务器统计监控
- 后台健康检查线程
- 连接上下文管理器
- 零外部依赖

## 快速开始

```python
from load_balancer_utils.mod import LoadBalancer, LoadBalancerStrategy

# 创建负载均衡器
lb = LoadBalancer(strategy=LoadBalancerStrategy.WEIGHTED_ROUND_ROBIN)

# 添加服务器
lb.add_server("server1", "192.168.1.1:8080", weight=3)
lb.add_server("server2", "192.168.1.2:8080", weight=2)
lb.add_server("server3", "192.168.1.3:8080", weight=1)

# 选择服务器
server = lb.select()
print(f"Selected: {server.id} -> {server.target}")

# 使用连接追踪
with lb.connection(server):
    # 在这里使用 server.target 进行请求
    # 连接计数会自动管理
    response = make_request(server.target)
    lb.record_success(server, response_time_ms=50.0)
```

## 使用示例

### 轮询策略

```python
lb = LoadBalancer(strategy=LoadBalancerStrategy.ROUND_ROBIN)
lb.add_server("s1", "server1.example.com")
lb.add_server("s2", "server2.example.com")

# 依次轮询
lb.select().id  # "s1"
lb.select().id  # "s2"
lb.select().id  # "s1"
```

### 加权轮询

```python
lb = LoadBalancer(strategy=LoadBalancerStrategy.WEIGHTED_ROUND_ROBIN)
lb.add_server("high", "high.example.com", weight=5)
lb.add_server("low", "low.example.com", weight=1)

# high 服务器被选中概率约为 low 的 5 倍
```

### 最少连接

```python
lb = LoadBalancer(strategy=LoadBalancerStrategy.LEAST_CONNECTIONS)
lb.add_server("s1", "server1.example.com")
lb.add_server("s2", "server2.example.com")

# 模拟连接
server = lb.select()
with lb.connection(server):
    # 此连接期间 s1 的 active_connections 为 1
    # 下次 select 会选择 s2（连接数更少）
    pass
```

### IP 哈希 (一致性路由)

```python
lb = LoadBalancer(strategy=LoadBalancerStrategy.IP_HASH)
lb.add_server("s1", "server1.example.com")
lb.add_server("s2", "server2.example.com")
lb.add_server("s3", "server3.example.com")

# 相同的客户端 IP 总是路由到同一服务器
lb.select(key="192.168.1.100")  # 始终选择同一服务器
lb.select(key="192.168.1.100")  # 结果相同
```

### 健康检查

```python
from load_balancer_utils.mod import LoadBalancer, HealthChecker, Server

class MyHealthChecker(HealthChecker):
    def check(self, server: Server) -> bool:
        # 自定义健康检查逻辑
        try:
            # 例如：TCP 连接测试
            return ping_server(server.target)
        except:
            return False

lb = LoadBalancer(health_checker=MyHealthChecker())
lb.add_server("s1", "server1.example.com")

# 手动执行健康检查
results = lb.run_health_checks()

# 启动后台健康检查
lb.start_health_checks()

# 停止健康检查
lb.stop_health_checks()
```

### 服务器管理

```python
# 标记服务器为不健康
lb.mark_server_unhealthy("s1")

# 标记服务器为健康
lb.mark_server_healthy("s1")

# 排空服务器（不接受新连接）
lb.drain_server("s1")

# 修改权重
lb.set_server_weight("s1", 5)

# 移除服务器
lb.remove_server("s1")
```

### 统计信息

```python
# 获取统计信息
stats = lb.get_stats()
print(f"总请求数: {stats['total_requests']}")
print(f"成功率: {stats['success_rate']:.2f}%")
print(f"健康服务器: {stats['healthy_servers']}/{stats['total_servers']}")

# 各服务器详细统计
for server_id, server_stats in stats['servers'].items():
    print(f"{server_id}: {server_stats['success_rate']:.2f}% 成功率")

# 重置统计
lb.reset_stats()
```

### 便捷函数

```python
from load_balancer_utils.mod import (
    create_round_robin_balancer,
    create_weighted_balancer,
    create_least_connections_balancer
)

# 快速创建负载均衡器
lb = create_round_robin_balancer([
    ("s1", "server1.example.com", 1),
    ("s2", "server2.example.com", 2),
    ("s3", "server3.example.com", 1),
])
```

## API 参考

### LoadBalancer

```python
class LoadBalancer(Generic[T]):
    def __init__(
        self,
        strategy: LoadBalancerStrategy = LoadBalancerStrategy.ROUND_ROBIN,
        health_checker: Optional[HealthChecker] = None,
        health_check_interval: float = 30.0,
        enable_stats: bool = True
    ): ...
    
    def add_server(
        self,
        server_id: str,
        target: T,
        weight: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Server[T]: ...
    
    def remove_server(self, server_id: str) -> bool: ...
    def select(self, key: Optional[str] = None) -> Server[T]: ...
    def connection(self, server: Server[T]) -> ConnectionContext[T]: ...
    def record_success(self, server: Server[T], response_time_ms: Optional[float] = None) -> None: ...
    def record_failure(self, server: Server[T]) -> None: ...
    def get_stats(self) -> Dict[str, Any]: ...
```

### Server

```python
@dataclass
class Server(Generic[T]):
    id: str
    target: T
    weight: int = 1
    state: ServerState = ServerState.HEALTHY
    stats: ServerStats = field(default_factory=ServerStats)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### LoadBalancerStrategy

```python
class LoadBalancerStrategy(Enum):
    ROUND_ROBIN = auto()
    WEIGHTED_ROUND_ROBIN = auto()
    LEAST_CONNECTIONS = auto()
    RANDOM = auto()
    WEIGHTED_RANDOM = auto()
    IP_HASH = auto()
```

### ServerState

```python
class ServerState(Enum):
    HEALTHY = auto()      # 正常服务
    UNHEALTHY = auto()    # 不健康，不参与负载
    DRAINING = auto()     # 排水中，不接受新连接
```

## 线程安全

所有操作都是线程安全的，可以在多线程环境中使用：

```python
import threading

lb = LoadBalancer()
lb.add_server("s1", "server1.example.com")
lb.add_server("s2", "server2.example.com")

def worker():
    for _ in range(100):
        server = lb.select()
        with lb.connection(server):
            # 处理请求
            pass

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## 许可证

MIT License