# Process Utils 🔄

**零依赖、生产就绪的 Rust 进程管理工具库**

支持进程启动、监控、资源跟踪和进程树操作等功能。

---

## ✨ 特性

- **进程管理** - 启动、停止、监控进程
- **超时控制** - 支持带超时的进程执行
- **输出捕获** - 捕获 stdout/stderr
- **进程信息** - 获取进程详细信息（PID、PPID、内存等）
- **进程树** - 获取子进程和进程树
- **信号支持** - 优雅关闭和强制终止
- **线程安全** - 所有操作支持多线程并发
- **跨平台** - 支持 Linux/Unix 系统

---

## 📦 安装

无需 Cargo 依赖，直接复制 `mod.rs` 到你的项目即可使用。

```bash
# 从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cp AllToolkit/Rust/process_utils/mod.rs your_project/
```

在你的 `main.rs` 或模块中使用：

```rust
mod process_utils;
use process_utils::*;
```

---

## 🚀 快速开始

### 基础用法

```rust
use process_utils::{ProcessManager, ProcessConfig};

// 创建进程管理器
let manager = ProcessManager::new();

// 配置进程
let config = ProcessConfig::new("echo")
    .args(&["Hello, World!"])
    .timeout_secs(30);

// 运行并等待完成
let result = manager.run(&config);

match result {
    Ok(output) => {
        if output.success() {
            println!("输出：{}", output.stdout);
        } else {
            println!("错误：{}", output.stderr);
        }
    }
    Err(e) => println!("执行失败：{}", e),
}
```

### 便捷函数

```rust
use process_utils::{run_command, run_with_timeout};

// 简单执行
let result = run_command("ls", &["-la"]);
println!("{}", result.unwrap().stdout);

// 带超时执行
let result = run_with_timeout("sleep", &["5"], 10);
```

---

## 📖 API 文档

### 核心类型

#### `ProcessConfig`

进程配置构建器。

```rust
let config = ProcessConfig::new("python3")
    .args(&["script.py", "--verbose"])
    .env("PYTHONPATH", "/path/to/modules")
    .working_dir("/app")
    .timeout_secs(60)
    .capture_stdout(true)
    .capture_stderr(true);
```

**方法：**

| 方法 | 说明 |
|------|------|
| `new(command)` | 创建新配置 |
| `args(&[&str])` | 设置参数 |
| `env(key, value)` | 设置环境变量 |
| `working_dir(path)` | 设置工作目录 |
| `timeout_secs(secs)` | 设置超时时间 |

#### `ProcessManager`

进程管理器，支持多进程管理。

```rust
let manager = ProcessManager::new();

// 启动进程
let pid = manager.spawn(&config)?;

// 运行并等待
let output = manager.run(&config)?;

// 检查是否运行中
if manager.is_running(pid) {
    // 终止进程
    manager.kill(pid)?;
}

// 获取输出
if let Some(output) = manager.get_output(pid) {
    println!("{}", output.stdout);
}
```

**方法：**

| 方法 | 说明 |
|------|------|
| `spawn(&config)` | 启动进程，返回 PID |
| `run(&config)` | 运行并等待完成 |
| `kill(pid)` | 终止进程 |
| `is_running(pid)` | 检查进程是否运行 |
| `get_output(pid)` | 获取进程输出 |
| `list_pids()` | 获取所有管理的 PID |
| `cleanup()` | 清理已完成的进程 |

#### `ProcessOutput`

进程执行结果。

```rust
pub struct ProcessOutput {
    pub pid: u32,
    pub exit_code: Option<i32>,
    pub stdout: String,
    pub stderr: String,
    pub duration_ms: u64,
    pub timed_out: bool,
}
```

**方法：**

| 方法 | 说明 |
|------|------|
| `success()` | 检查是否成功（退出码 0 且未超时） |

#### `ProcessInfo`

进程信息（仅 Unix/Linux）。

```rust
pub struct ProcessInfo {
    pub pid: u32,
    pub ppid: u32,
    pub name: String,
    pub command: String,
    pub status: String,
    pub cpu_percent: f32,
    pub memory_bytes: u64,
    pub start_time: u64,
    pub user: String,
    pub threads: u32,
}
```

---

### 独立函数

```rust
use process_utils::*;

// 获取当前 PID
let pid = current_pid();

// 检查进程是否存在
if process_exists(1234) {
    println!("进程存在");
}

// 获取进程信息
let info = get_process_info(1234)?;
println!("进程名：{}, 内存：{} KB", info.name, info.memory_bytes / 1024);

// 终止进程
kill_process(1234)?;           // 发送 SIGTERM
force_kill_process(1234)?;     // 发送 SIGKILL

// 获取子进程
let children = get_child_processes(1234)?;

// 获取完整进程树
let tree = get_process_tree(1234)?;

// 等待进程完成（带超时）
let exit_code = wait_for_process(1234, Duration::from_secs(30))?;
```

---

## 💡 使用示例

### 示例 1：运行外部命令

```rust
use process_utils::{ProcessManager, ProcessConfig};

fn main() {
    let manager = ProcessManager::new();
    
    // 运行 git status
    let config = ProcessConfig::new("git")
        .args(&["status", "--short"])
        .working_dir("/path/to/repo");
    
    match manager.run(&config) {
        Ok(output) if output.success() => {
            println!("Git 状态:\n{}", output.stdout);
        }
        Ok(output) => {
            eprintln!("Git 错误：{}", output.stderr);
        }
        Err(e) => {
            eprintln!("执行失败：{}", e);
        }
    }
}
```

### 示例 2：带超时的长时间任务

```rust
use process_utils::{run_with_timeout, ProcessError};

fn main() {
    // 运行可能超时的任务
    match run_with_timeout("python3", &["long_script.py"], 30) {
        Ok(output) if output.timed_out => {
            println!("任务超时！");
        }
        Ok(output) => {
            println!("任务完成，耗时：{}ms", output.duration_ms);
        }
        Err(ProcessError::Timeout) => {
            println!("执行超时");
        }
        Err(e) => {
            eprintln!("错误：{}", e);
        }
    }
}
```

### 示例 3：管理多个进程

```rust
use process_utils::{ProcessManager, ProcessConfig};
use std::thread;
use std::time::Duration;

fn main() {
    let manager = ProcessManager::new();
    
    // 启动多个后台任务
    let config1 = ProcessConfig::new("sleep").args(&["5"]);
    let config2 = ProcessConfig::new("sleep").args(&["3"]);
    let config3 = ProcessConfig::new("sleep").args(&["7"]);
    
    let pid1 = manager.spawn(&config1).unwrap();
    let pid2 = manager.spawn(&config2).unwrap();
    let pid3 = manager.spawn(&config3).unwrap();
    
    println!("启动了进程：{}, {}, {}", pid1, pid2, pid3);
    
    // 等待一段时间后检查
    thread::sleep(Duration::from_secs(4));
    
    println!("进程 {} 运行中：{}", pid1, manager.is_running(pid1));
    println!("进程 {} 运行中：{}", pid2, manager.is_running(pid2));
    println!("进程 {} 运行中：{}", pid3, manager.is_running(pid3));
    
    // 清理已完成的进程
    let finished = manager.cleanup();
    println!("已完成的进程：{:?}", finished);
}
```

### 示例 4：进程监控

```rust
use process_utils::{get_process_info, current_pid, get_child_processes};

fn main() {
    let pid = current_pid();
    
    // 获取当前进程信息
    if let Ok(info) = get_process_info(pid) {
        println!("进程信息:");
        println!("  PID: {}", info.pid);
        println!("  名称：{}", info.name);
        println!("  状态：{}", info.status);
        println!("  内存：{} KB", info.memory_bytes / 1024);
        println!("  线程数：{}", info.threads);
    }
    
    // 获取子进程
    if let Ok(children) = get_child_processes(pid) {
        println!("\n子进程：{:?}", children);
    }
}
```

### 示例 5：环境变量和工作目录

```rust
use process_utils::{ProcessManager, ProcessConfig};

fn main() {
    let manager = ProcessManager::new();
    
    let config = ProcessConfig::new("env")
        .env("APP_ENV", "production")
        .env("LOG_LEVEL", "debug")
        .env("DATABASE_URL", "postgres://localhost/mydb")
        .working_dir("/app");
    
    let output = manager.run(&config).unwrap();
    println!("{}", output.stdout);
}
```

---

## ⚠️ 注意事项

1. **平台支持** - 进程信息和信号功能仅在 Unix/Linux 系统上完全支持
2. **权限** - 某些操作可能需要 root 权限（如获取其他用户进程信息）
3. **资源清理** - 使用 `ProcessManager` 时，记得调用 `cleanup()` 清理已完成的进程
4. **超时处理** - 超时时进程会被强制终止，可能不会执行清理逻辑

---

## 🧪 测试

运行测试：

```bash
cd AllToolkit/Rust/process_utils
rustc --test mod.rs -o process_utils_test
./process_utils_test
```

或者使用 cargo（如果有 Cargo.toml）：

```bash
cargo test
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**AllToolkit** - 多语言工具集合，让开发更简单
