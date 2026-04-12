# Monitoring Utils 📊

**Python 系统监控工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`monitoring_utils` 是一个全面的 Python 系统监控工具模块，提供 CPU、内存、磁盘、网络和进程监控功能。所有实现均使用 Python 标准库，通过读取 Linux `/proc` 文件系统获取系统信息，零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **CPU 监控** - 使用率、负载平均值、核心数
- **内存监控** - RAM、Swap、百分比
- **磁盘监控** - 使用量、I/O 统计
- **网络监控** - 接口统计（RX/TX）
- **进程监控** - 进程列表、详情、Top N
- **系统信息** - 主机名、运行时间、启动时间
- **Linux /proc 文件系统** - 直接读取内核数据
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/monitoring_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

### 基本使用

```python
from mod import (
    get_cpu_stats, get_memory_stats, get_disk_usage,
    get_network_stats, get_process_list, get_system_info
)

# CPU 统计
cpu = get_cpu_stats()
print(f"CPU 使用率：{cpu.usage_percent:.1f}%")
print(f"负载平均：{cpu.load_avg}")

# 内存统计
mem = get_memory_stats()
print(f"总内存：{mem.total_gb:.2f} GB")
print(f"已使用：{mem.used_gb:.2f} GB ({mem.usage_percent:.1f}%)")

# 磁盘使用
disk = get_disk_usage("/")
print(f"磁盘使用：{disk['usage_percent']:.1f}%")
```

### 获取所有统计信息

```python
from mod import get_all_stats

# 一次性获取所有系统统计
stats = get_all_stats()

print(f"主机名：{stats['system']['hostname']}")
print(f"CPU 使用率：{stats['cpu']['usage_percent']:.1f}%")
print(f"内存使用率：{stats['memory']['usage_percent']:.1f}%")
print(f"进程数量：{len(stats['top_cpu_processes'])}")
```

### 监控 CPU 使用率

```python
from mod import get_cpu_stats_percent

# 获取 1 秒间隔的 CPU 使用率
cpu = get_cpu_stats_percent(interval=1.0)
print(f"CPU 使用率：{cpu.usage_percent:.1f}%")
print(f"用户态：{cpu.user:.1f}%")
print(f"内核态：{cpu.system:.1f}%")
```

### 进程监控

```python
from mod import get_top_processes, get_process_info

# 获取 CPU 使用率最高的 5 个进程
top_cpu = get_top_processes(5, by="cpu")
for proc in top_cpu:
    print(f"{proc.name} (PID: {proc.pid}) - CPU: {proc.cpu_percent:.1f}%")

# 获取内存使用率最高的 5 个进程
top_mem = get_top_processes(5, by="memory")
for proc in top_mem:
    print(f"{proc.name} (PID: {proc.pid}) - 内存：{proc.memory_percent:.2f}%")

# 获取特定进程信息
proc = get_process_info(1)  # PID 1
if proc:
    print(f"进程名：{proc.name}")
    print(f"状态：{proc.status}")
    print(f"命令行：{proc.cmdline}")
```

### 网络监控

```python
from mod import get_network_stats

# 获取所有网络接口统计
interfaces = get_network_stats()
for iface in interfaces:
    if iface.name != "lo":  # 跳过回环接口
        print(f"接口：{iface.name}")
        print(f"  接收：{iface.rx_bytes / 1024**2:.2f} MB")
        print(f"  发送：{iface.tx_bytes / 1024**2:.2f} MB")
        print(f"  接收错误：{iface.rx_errors}")
        print(f"  发送错误：{iface.tx_errors}")
```

### 系统信息

```python
from mod import get_system_info, get_uptime, get_hostname

# 获取系统信息
info = get_system_info()
print(f"主机名：{info['hostname']}")
print(f"平台：{info['platform']} {info['release']}")
print(f"CPU 核心数：{info['cpu_count']}")
print(f"Python 版本：{info['python_version']}")

# 获取运行时间
uptime = get_uptime()
hours = int(uptime // 3600)
minutes = int((uptime % 3600) // 60)
print(f"运行时间：{hours}小时 {minutes}分钟")

# 获取主机名
hostname = get_hostname()
print(f"主机名：{hostname}")
```

---

## 📋 API 参考

### 数据类

#### CPUStats
CPU 统计数据。

```python
@dataclass
class CPUStats:
    user: float           # 用户态 CPU 时间
    system: float         # 内核态 CPU 时间
    idle: float           # 空闲时间
    iowait: float         # I/O 等待时间
    irq: float            # 硬中断时间
    softirq: float        # 软中断时间
    steal: float          # 虚拟化窃取时间
    guest: float          # 客户机时间
    usage_percent: float  # CPU 使用率百分比
    cores: int            # CPU 核心数
    load_avg: tuple       # 负载平均 (1min, 5min, 15min)
```

#### MemoryStats
内存统计数据。

```python
@dataclass
class MemoryStats:
    total: int           # 总内存 (字节)
    available: int       # 可用内存 (字节)
    used: int            # 已用内存 (字节)
    free: int            # 空闲内存 (字节)
    buffers: int         # 缓冲区 (字节)
    cached: int          # 缓存 (字节)
    swap_total: int      # Swap 总量 (字节)
    swap_free: int       # Swap 空闲 (字节)
    swap_used: int       # Swap 已用 (字节)
    usage_percent: float # 内存使用率
    swap_percent: float  # Swap 使用率
    
    # 属性
    total_gb: float      # 总内存 (GB)
    available_gb: float  # 可用内存 (GB)
    used_gb: float       # 已用内存 (GB)
```

#### ProcessStats
进程统计数据。

```python
@dataclass
class ProcessStats:
    pid: int            # 进程 ID
    name: str           # 进程名
    status: str         # 状态 (R, S, D, Z 等)
    ppid: int           # 父进程 ID
    uid: int            # 用户 ID
    cpu_percent: float  # CPU 使用率
    memory_percent: float  # 内存使用率
    memory_rss: int     # 常驻内存 (字节)
    memory_vms: int     # 虚拟内存 (字节)
    num_threads: int    # 线程数
    create_time: float  # 创建时间
    cmdline: str        # 命令行
```

### 主要类

#### SystemMonitor
主系统监控类。

```python
monitor = SystemMonitor()

# 获取 CPU 统计
cpu = monitor.get_cpu_stats()
cpu = monitor.get_cpu_stats_percent(interval=1.0)

# 获取内存统计
mem = monitor.get_memory_stats()

# 获取磁盘使用
disk = monitor.get_disk_usage("/")
disk_io = monitor.get_disk_io_stats("sda")

# 获取网络统计
interfaces = monitor.get_network_stats()

# 获取进程列表
processes = monitor.get_process_list()
proc = monitor.get_process_info(pid)
top = monitor.get_top_processes(10, by="cpu")

# 获取系统信息
info = monitor.get_system_info()
uptime = monitor.get_uptime()
hostname = monitor.get_hostname()

# 获取所有统计
all_stats = monitor.get_all_stats()
```

### 便捷函数

```python
# CPU
get_cpu_stats() -> CPUStats
get_cpu_stats_percent(interval=1.0) -> CPUStats

# 内存
get_memory_stats() -> MemoryStats

# 磁盘
get_disk_usage(path="/") -> dict
get_disk_io_stats(device="sda") -> DiskStats

# 网络
get_network_stats() -> List[NetworkInterfaceStats]

# 进程
get_process_list() -> List[ProcessStats]
get_process_info(pid) -> Optional[ProcessStats]
get_top_processes(n=10, by="cpu") -> List[ProcessStats]

# 系统
get_system_info() -> dict
get_uptime() -> float
get_hostname() -> str
get_all_stats() -> dict
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/monitoring_utils
python monitoring_utils_test.py
```

测试覆盖：
- 数据类功能
- SystemMonitor 类方法
- 便捷函数
- 模块元数据
- 边界情况处理
- 集成测试

---

## 💡 使用示例

### 系统监控仪表板

```python
from mod import SystemMonitor
import time

monitor = SystemMonitor()

print("=" * 60)
print("系统监控仪表板")
print("=" * 60)

while True:
    # 获取统计
    cpu = monitor.get_cpu_stats_percent(interval=0.5)
    mem = monitor.get_memory_stats()
    
    # 清屏并显示
    print("\r" + " " * 60 + "\r", end="")
    print(f"CPU: {cpu.usage_percent:5.1f}% | "
          f"内存：{mem.usage_percent:5.1f}% | "
          f"负载：{cpu.load_avg[0]:.2f}", end="")
    
    time.sleep(1)
```

### 进程监控告警

```python
from mod import get_top_processes

def check_high_cpu_processes(threshold=80.0):
    """检查高 CPU 使用率的进程。"""
    top = get_top_processes(10, by="cpu")
    alerts = []
    
    for proc in top:
        if proc.cpu_percent > threshold:
            alerts.append(f"⚠️ {proc.name} (PID: {proc.pid}) - CPU: {proc.cpu_percent:.1f}%")
    
    return alerts

def check_high_memory_processes(threshold=50.0):
    """检查高内存使用率的进程。"""
    top = get_top_processes(10, by="memory")
    alerts = []
    
    for proc in top:
        if proc.memory_percent > threshold:
            alerts.append(f"⚠️ {proc.name} (PID: {proc.pid}) - 内存：{proc.memory_percent:.2f}%")
    
    return alerts

# 使用示例
cpu_alerts = check_high_cpu_processes()
mem_alerts = check_high_memory_processes()

if cpu_alerts:
    print("高 CPU 使用率告警:")
    for alert in cpu_alerts:
        print(f"  {alert}")

if mem_alerts:
    print("高内存使用率告警:")
    for alert in mem_alerts:
        print(f"  {alert}")
```

### 系统健康检查

```python
from mod import get_all_stats

def system_health_check():
    """执行系统健康检查。"""
    stats = get_all_stats()
    
    issues = []
    
    # 检查 CPU
    cpu_usage = stats['cpu']['usage_percent']
    if cpu_usage > 90:
        issues.append(f"🔴 CPU 使用率过高：{cpu_usage:.1f}%")
    elif cpu_usage > 70:
        issues.append(f"🟡 CPU 使用率偏高：{cpu_usage:.1f}%")
    
    # 检查内存
    mem_usage = stats['memory']['usage_percent']
    if mem_usage > 90:
        issues.append(f"🔴 内存使用率过高：{mem_usage:.1f}%")
    elif mem_usage > 70:
        issues.append(f"🟡 内存使用率偏高：{mem_usage:.1f}%")
    
    # 检查磁盘
    disk_usage = stats['disk']['usage_percent']
    if disk_usage > 90:
        issues.append(f"🔴 磁盘使用率过高：{disk_usage:.1f}%")
    elif disk_usage > 80:
        issues.append(f"🟡 磁盘使用率偏高：{disk_usage:.1f}%")
    
    # 检查负载
    load_1min = stats['cpu']['load_avg'][0]
    cpu_cores = stats['system']['cpu_count']
    if load_1min > cpu_cores * 2:
        issues.append(f"🔴 系统负载过高：{load_1min:.2f} (核心数：{cpu_cores})")
    elif load_1min > cpu_cores:
        issues.append(f"🟡 系统负载偏高：{load_1min:.2f}")
    
    return {
        "healthy": len(issues) == 0,
        "issues": issues,
        "timestamp": stats['timestamp']
    }

# 使用示例
health = system_health_check()
if health["healthy"]:
    print("✅ 系统健康")
else:
    print("⚠️ 系统问题:")
    for issue in health["issues"]:
        print(f"  {issue}")
```

### 网络流量监控

```python
from mod import get_network_stats
import time

def monitor_network_traffic(interval=5):
    """监控网络流量。"""
    prev_stats = {iface.name: iface for iface in get_network_stats()}
    
    while True:
        time.sleep(interval)
        
        curr_stats = {iface.name: iface for iface in get_network_stats()}
        
        print(f"\n网络流量 (过去 {interval} 秒):")
        print("-" * 50)
        
        for name in curr_stats:
            if name == "lo":
                continue
            
            prev = prev_stats.get(name)
            curr = curr_stats[name]
            
            if prev:
                rx_diff = curr.rx_bytes - prev.rx_bytes
                tx_diff = curr.tx_bytes - prev.tx_bytes
                
                rx_rate = rx_diff / interval / 1024  # KB/s
                tx_rate = tx_diff / interval / 1024  # KB/s
                
                print(f"{name}:")
                print(f"  下载：{rx_rate:.2f} KB/s ({rx_diff / 1024:.2f} KB)")
                print(f"  上传：{tx_rate:.2f} KB/s ({tx_diff / 1024:.2f} KB)")
        
        prev_stats = curr_stats

# 使用示例
# monitor_network_traffic()
```

---

## ⚠️ 注意事项

### 平台限制

- **仅支持 Linux** - 本模块通过读取 `/proc` 文件系统工作
- 需要读取 `/proc` 的权限（通常所有用户都有）
- 某些进程信息可能需要 root 权限

### 性能考虑

- `get_cpu_stats_percent()` 会阻塞指定的时间间隔
- `get_process_list()` 会遍历所有进程，在进程数量多时可能较慢
- `get_all_stats()` 会调用多个方法，适合定期采样而非高频调用

### 准确性

- CPU 使用率是基于 `/proc/stat` 的估算值
- 进程 CPU 使用率是累积值，不是实时百分比
- 对于精确的进程 CPU 监控，建议在两个时间点采样差值

---

## 📄 许可证

MIT License - 详见 AllToolkit 主仓库

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📚 相关模块

- `benchmark_utils` - 性能基准测试
- `log_utils` - 日志记录
- `cron_utils` - 定时任务
- `env_utils` - 环境变量
