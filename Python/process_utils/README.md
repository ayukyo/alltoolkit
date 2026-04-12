# Process Utils - Python 进程管理工具

**零依赖、生产就绪的进程管理模块**

## 📋 目录

- [简介](#简介)
- [安装](#安装)
- [快速开始](#快速开始)
- [API 参考](#api-参考)
  - [ProcessManager](#processmanager)
  - [ProcessUtils](#processutils)
  - [WorkerPool](#workerpool)
  - [数据类](#数据类)
  - [枚举](#枚举)
  - [便捷函数](#便捷函数)
- [使用示例](#使用示例)
- [测试](#测试)
- [注意事项](#注意事项)

---

## 简介

`process_utils` 是一个功能完整的进程管理模块，提供：

- ✅ **命令执行** - 运行系统命令，支持超时控制
- ✅ **输出流式传输** - 实时捕获 stdout/stderr
- ✅ **进程管理** - 启动、监控、终止进程
- ✅ **环境变量** - 读取、设置、快照
- ✅ **进程池** - 多进程并行执行任务
- ✅ **零依赖** - 仅使用 Python 标准库

---

## 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/process_utils/mod.py ./your_project/
```

或者将整个模块目录复制：

```bash
cp -r AllToolkit/Python/process_utils ./your_project/
```

---

## 快速开始

### 基本用法

```python
from process_utils import run, run_shell

# 运行简单命令
result = run("echo hello")
print(result.stdout)  # "hello\n"

# 运行 shell 命令
result = run_shell("ls -la | head -5")
print(result.stdout)

# 带超时执行
result = run("sleep 5", timeout=2.0)
print(result.state)  # ProcessState.TIMEOUT
```

### 进程管理器

```python
from process_utils import ProcessManager, ProcessConfig

manager = ProcessManager()

# 配置执行参数
config = ProcessConfig(
    timeout=30.0,
    cwd="/tmp",
    env={"MY_VAR": "value"},
)

result = manager.run("python script.py", config)
print(f"Exit code: {result.returncode}")
print(f"Time: {result.execution_time:.2f}s")
```

### 工作进程池

```python
from process_utils import WorkerPool

def square(x):
    return x * x

# 使用上下文管理器
with WorkerPool(num_workers=4) as pool:
    results = pool.map(square, [1, 2, 3, 4, 5])
    print(results)  # [1, 4, 9, 16, 25]
```

---

## API 参考

### ProcessManager

进程管理器，提供完整的进程生命周期管理。

#### 构造函数

```python
manager = ProcessManager(default_config=None)
```

- `default_config`: 默认执行配置（ProcessConfig 对象）

#### 方法

| 方法 | 描述 | 返回值 |
|------|------|--------|
| `run(command, config, callback)` | 执行命令 | `ProcessResult` |
| `run_streaming(command, config, stdout_callback, stderr_callback)` | 流式执行 | `ProcessResult` |
| `kill(pid, signal_num)` | 终止进程 | `bool` |
| `kill_all(signal_num)` | 终止所有进程 | `int` |
| `get_result(pid)` | 获取结果 | `ProcessResult` |
| `get_all_results()` | 获取所有结果 | `Dict[int, ProcessResult]` |
| `is_running(pid)` | 检查是否运行中 | `bool` |
| `get_running_count()` | 获取运行中数量 | `int` |

### ProcessUtils

静态工具类，提供便捷的进程操作函数。

#### 方法

```python
# 执行命令
ProcessUtils.run(command, timeout, shell, cwd, env) -> ProcessResult
ProcessUtils.run_shell(command, **kwargs) -> ProcessResult
ProcessUtils.run_background(command, shell) -> int  # 返回 PID

# 命令检查
ProcessUtils.exists(command) -> bool
ProcessUtils.which(command) -> Optional[str]

# 进程信息
ProcessUtils.get_pid() -> int
ProcessUtils.get_ppid() -> int
ProcessUtils.get_cwd() -> str

# 环境变量
ProcessUtils.get_env(name, default) -> Optional[str]
ProcessUtils.set_env(name, value) -> None
ProcessUtils.unset_env(name) -> None
ProcessUtils.get_env_snapshot() -> Dict[str, str]

# 其他
ProcessUtils.sleep(seconds) -> None
ProcessUtils.exit(code) -> None
ProcessUtils.abort() -> None
```

### WorkerPool

多进程工作池，用于并行执行任务。

#### 构造函数

```python
pool = WorkerPool(num_workers=4)
```

#### 方法

| 方法 | 描述 | 返回值 |
|------|------|--------|
| `start()` | 启动进程池 | `None` |
| `stop(graceful)` | 停止进程池 | `None` |
| `map(func, iterable, chunksize)` | 并行映射 | `List[Any]` |
| `map_async(func, iterable, callback, error_callback)` | 异步映射 | `AsyncResult` |
| `apply(func, args, kwds)` | 应用函数 | `Any` |
| `apply_async(func, args, kwds, callback, error_callback)` | 异步应用 | `AsyncResult` |
| `get_results()` | 获取结果 | `List[Any]` |
| `get_errors()` | 获取错误 | `List[Exception]` |

#### 上下文管理器

```python
with WorkerPool(num_workers=4) as pool:
    results = pool.map(func, data)
# 自动优雅关闭
```

### 数据类

#### ProcessResult

进程执行结果。

```python
@dataclass
class ProcessResult:
    returncode: int          # 返回码
    stdout: str              # 标准输出
    stderr: str              # 标准错误
    execution_time: float    # 执行时间（秒）
    pid: Optional[int]       # 进程 ID
    command: str             # 执行的命令
    state: ProcessState      # 进程状态
    
    def success() -> bool    # 是否成功
    def to_dict() -> Dict    # 转为字典
```

#### ProcessConfig

执行配置。

```python
@dataclass
class ProcessConfig:
    timeout: float = 30.0           # 超时时间
    cwd: Optional[str] = None       # 工作目录
    env: Optional[Dict] = None      # 环境变量
    shell: bool = False             # 是否使用 shell
    capture_output: bool = True     # 捕获输出
    text: bool = True               # 文本模式
    encoding: str = 'utf-8'         # 编码
    priority: ProcessPriority       # 优先级
```

#### ProcessInfo

进程信息（用于扩展）。

```python
@dataclass
class ProcessInfo:
    pid: int
    name: str
    cmdline: List[str]
    status: str
    ppid: int
    username: str
    cpu_percent: float
    memory_percent: float
    num_threads: int
```

### 枚举

#### ProcessState

进程状态。

```python
class ProcessState(Enum):
    RUNNING = "running"      # 运行中
    STOPPED = "stopped"      # 已停止
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败
    TIMEOUT = "timeout"      # 超时
    UNKNOWN = "unknown"      # 未知
```

#### ProcessPriority

进程优先级（Unix nice 值）。

```python
class ProcessPriority(Enum):
    VERY_HIGH = -20    # 最高（需要 root）
    HIGH = -10
    ABOVE_NORMAL = -5
    NORMAL = 0         # 默认
    BELOW_NORMAL = 5
    LOW = 10
    VERY_LOW = 19      # 最低
```

### 便捷函数

模块级别的便捷函数：

```python
from process_utils import (
    run,              # 执行命令
    run_shell,        # 执行 shell 命令
    run_background,   # 后台运行
    exists,           # 检查命令是否存在
    which,            # 查找命令路径
    get_pid,          # 获取当前 PID
    get_env,          # 获取环境变量
    set_env,          # 设置环境变量
)
```

---

## 使用示例

### 1. 基本命令执行

```python
from process_utils import run

# 简单命令
result = run("echo Hello World")
if result.success():
    print(f"Output: {result.stdout.strip()}")
    print(f"Time: {result.execution_time:.3f}s")
```

### 2. 带超时控制

```python
from process_utils import run, ProcessState

result = run("sleep 10", timeout=2.0)
if result.state == ProcessState.TIMEOUT:
    print("Command timed out!")
```

### 3. Shell 命令

```python
from process_utils import run_shell

# 管道命令
result = run_shell("ls -la | grep .py | wc -l")
print(f"Python files: {result.stdout.strip()}")

# 重定向
result = run_shell("echo test > /tmp/test.txt && cat /tmp/test.txt")
```

### 4. 自定义工作目录和环境

```python
from process_utils import ProcessManager, ProcessConfig

manager = ProcessManager()
config = ProcessConfig(
    cwd="/tmp",
    env={"PATH": "/usr/bin:/bin", "MY_VAR": "value"},
    timeout=60.0,
)

result = manager.run("python script.py", config)
```

### 5. 流式输出

```python
from process_utils import ProcessManager, ProcessConfig

def on_stdout(line):
    print(f"OUT: {line}", end="")

def on_stderr(line):
    print(f"ERR: {line}", end="")

manager = ProcessManager()
config = ProcessConfig(timeout=30.0)

result = manager.run_streaming(
    "python -c \"for i in range(10): print(i)\"",
    config,
    stdout_callback=on_stdout,
    stderr_callback=on_stderr,
)
```

### 6. 后台运行

```python
from process_utils import run_background

# 启动后台进程
pid = run_background("python long_running_script.py")
print(f"Started process with PID: {pid}")
```

### 7. 检查命令

```python
from process_utils import exists, which

if exists("git"):
    print(f"Git found at: {which('git')}")
else:
    print("Git not installed")
```

### 8. 环境变量管理

```python
from process_utils import get_env, set_env, unset_env, get_env_snapshot

# 读取
home = get_env("HOME")
path = get_env("PATH", "/default/path")

# 设置
set_env("MY_APP_MODE", "production")

# 快照
snapshot = get_env_snapshot()
print(f"Total env vars: {len(snapshot)}")

# 清理
unset_env("MY_APP_MODE")
```

### 9. 并行处理

```python
from process_utils import WorkerPool
import time

def process_item(item):
    time.sleep(0.1)  # 模拟耗时操作
    return item * 2

# 方法 1: 上下文管理器
with WorkerPool(num_workers=4) as pool:
    results = pool.map(process_item, range(100))
    print(f"Processed {len(results)} items")

# 方法 2: 手动管理
pool = WorkerPool(num_workers=4)
pool.start()

async_result = pool.map_async(process_item, range(100))
results = async_result.get(timeout=30)

pool.stop(graceful=True)
```

### 10. 异步回调

```python
from process_utils import WorkerPool

def square(x):
    return x * x

def on_success(results):
    print(f"Success: {results}")

def on_error(error):
    print(f"Error: {error}")

with WorkerPool(num_workers=2) as pool:
    async_result = pool.map_async(
        square,
        [1, 2, 3, 4, 5],
        callback=on_success,
        error_callback=on_error,
    )
    # 可以做其他事情...
    results = async_result.get()
```

### 11. 进程管理

```python
from process_utils import ProcessManager, ProcessConfig

manager = ProcessManager()

# 启动长时间运行的进程
result = manager.run("sleep 60")
pid = result.pid

# 检查状态
if manager.is_running(pid):
    print("Process still running")

# 获取结果
stored_result = manager.get_result(pid)
print(f"Results so far: {manager.get_all_results()}")

# 终止进程
if manager.kill(pid):
    print("Process terminated")

# 终止所有
count = manager.kill_all()
print(f"Terminated {count} processes")
```

### 12. 错误处理

```python
from process_utils import run, ProcessState

result = run("nonexistent_command")

if result.state == ProcessState.FAILED:
    print(f"Failed to execute: {result.stderr}")
elif result.state == ProcessState.TIMEOUT:
    print("Command timed out")
elif not result.success():
    print(f"Command failed with code {result.returncode}")
else:
    print("Success!")
```

---

## 测试

### 运行测试

```bash
# 进入模块目录
cd AllToolkit/Python/process_utils/

# 运行测试套件
python process_utils_test.py

# 或使用 pytest
python -m pytest process_utils_test.py -v
```

### 测试覆盖

测试套件包含 70+ 个测试用例，覆盖：

- ✅ ProcessResult 创建和属性
- ✅ ProcessConfig 配置
- ✅ ProcessManager 执行和管理
- ✅ ProcessUtils 静态方法
- ✅ WorkerPool 并行处理
- ✅ 便捷函数
- ✅ 边界情况和错误处理
- ✅ Unicode 和多行输出
- ✅ 并发执行

---

## 注意事项

### 安全性

1. **命令注入** - 避免直接拼接用户输入到命令中
   ```python
   # ❌ 危险
   run(f"echo {user_input}")
   
   # ✅ 安全
   run(["echo", user_input])
   ```

2. **Shell 模式** - 仅在需要时使用 `shell=True`
   ```python
   # 需要 shell 特性（管道、重定向等）
   run_shell("ls | grep .py")
   
   # 简单命令不需要 shell
   run(["ls", "-la"])
   ```

### 性能

1. **进程池大小** - 根据 CPU 核心数设置
   ```python
   import multiprocessing
   num_workers = multiprocessing.cpu_count()
   pool = WorkerPool(num_workers=num_workers)
   ```

2. **超时设置** - 始终设置合理的超时
   ```python
   result = run("command", timeout=30.0)  # 避免无限等待
   ```

### 平台差异

- Unix/Linux: 支持所有功能
- Windows: 部分功能受限（如信号处理、优先级）
- macOS: 完全支持

### 资源清理

使用上下文管理器确保资源正确释放：

```python
with WorkerPool(num_workers=4) as pool:
    # 自动清理
    results = pool.map(func, data)
```

---

## 版本信息

- **版本**: 1.0.0
- **Python**: 3.7+
- **依赖**: 无（标准库）
- **许可证**: MIT

---

## 贡献

欢迎提交问题和 Pull Request！

1. Fork 项目
2. 创建特性分支
3. 添加测试
4. 提交更改
5. 推送到分支
6. 开启 Pull Request

---

## 相关链接

- [AllToolkit 主项目](https://github.com/ayukyo/alltoolkit)
- [Python subprocess 文档](https://docs.python.org/3/library/subprocess.html)
- [Python multiprocessing 文档](https://docs.python.org/3/library/multiprocessing.html)
