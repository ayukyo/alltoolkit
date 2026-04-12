# Process Utils 模块信息

## 模块概述

**语言**: Rust  
**版本**: 1.0.0  
**依赖**: 零依赖（仅使用 Rust 标准库）  
**平台**: Linux/Unix（主要支持），Windows/macOS（部分功能）

## 文件结构

```
process_utils/
├── mod.rs                    # 主模块文件（核心实现）
├── Cargo.toml                # Cargo 配置（可选）
├── README.md                 # 使用文档
├── MODULE_INFO.md            # 本文件
├── process_utils_test.rs     # 独立测试文件
├── examples/
│   ├── basic_usage.rs        # 基础用法示例
│   ├── process_monitor.rs    # 进程监控示例
│   └── batch_processor.rs    # 批处理示例
└── examples/
    ├── basic_usage           # 编译后的可执行文件
    ├── process_monitor
    └── batch_processor
```

## 核心功能

### 1. 进程配置 (ProcessConfig)

```rust
let config = ProcessConfig::new("python3")
    .args(&["script.py", "--verbose"])
    .env("PYTHONPATH", "/path/to/modules")
    .working_dir("/app")
    .timeout_secs(60);
```

### 2. 进程管理器 (ProcessManager)

```rust
let manager = ProcessManager::new();

// 启动进程
let pid = manager.spawn(&config)?;

// 运行并等待
let output = manager.run(&config)?;

// 检查状态
if manager.is_running(pid) {
    manager.kill(pid)?;
}
```

### 3. 便捷函数

```rust
// 简单执行
let result = run_command("ls", &["-la"])?;

// 带超时
let result = run_with_timeout("sleep", &["5"], 10)?;
```

### 4. 进程信息 (Unix)

```rust
// 获取进程信息
let info = get_process_info(pid)?;
println!("内存：{} KB", info.memory_bytes / 1024);

// 获取子进程
let children = get_child_processes(pid)?;

// 获取进程树
let tree = get_process_tree(pid)?;
```

## API 参考

### 类型

| 类型 | 说明 |
|------|------|
| `ProcessConfig` | 进程配置构建器 |
| `ProcessManager` | 进程管理器 |
| `ProcessOutput` | 进程执行结果 |
| `ProcessInfo` | 进程详细信息 |
| `ProcessError` | 错误类型 |
| `ProcessResult<T>` | 结果类型 |

### 函数

| 函数 | 说明 | 平台 |
|------|------|------|
| `run_command(cmd, args)` | 运行命令并捕获输出 | 所有 |
| `run_with_timeout(cmd, args, secs)` | 带超时运行命令 | 所有 |
| `current_pid()` | 获取当前进程 PID | 所有 |
| `process_exists(pid)` | 检查进程是否存在 | 所有 |
| `get_process_info(pid)` | 获取进程详细信息 | Unix |
| `kill_process(pid)` | 终止进程 (SIGTERM) | Unix |
| `force_kill_process(pid)` | 强制终止进程 (SIGKILL) | Unix |
| `get_child_processes(pid)` | 获取子进程列表 | Unix |
| `get_process_tree(pid)` | 获取完整进程树 | Unix |
| `wait_for_process(pid, timeout)` | 等待进程完成 | Unix |

## 测试

### 运行测试

```bash
# 使用 rustc
cd process_utils
rustc --test mod.rs -o process_utils_test
./process_utils_test

# 或使用 Cargo
cargo test
```

### 测试覆盖率

- ✅ 进程配置构建器
- ✅ 进程启动和运行
- ✅ 超时处理
- ✅ 进程终止
- ✅ 输出捕获
- ✅ 进程信息查询
- ✅ 多进程管理
- ✅ 错误处理

## 示例

### 基础示例

```bash
cd examples
rustc basic_usage.rs -o basic_usage
./basic_usage
```

### 进程监控示例

```bash
rustc process_monitor.rs -o process_monitor
./process_monitor
```

### 批处理示例

```bash
rustc batch_processor.rs -o batch_processor
./batch_processor
```

## 使用场景

1. **外部命令执行** - 运行系统命令并捕获输出
2. **长时间任务管理** - 带超时的任务执行
3. **并发进程管理** - 同时管理多个进程
4. **进程监控** - 监控进程状态和资源使用
5. **批处理任务** - 并行执行多个任务
6. **服务管理** - 启动、停止、重启服务

## 注意事项

1. **平台兼容性**: 进程信息和信号功能仅在 Unix/Linux 上完全支持
2. **权限**: 某些操作可能需要 root 权限
3. **资源清理**: 使用 ProcessManager 时记得调用 cleanup()
4. **超时处理**: 超时时进程会被强制终止

## 版本历史

### 1.0.0 (2026-04-11)

- 初始版本
- 核心进程管理功能
- 进程信息查询（Unix）
- 超时控制
- 多进程管理
- 完整测试套件
- 三个示例程序

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 到 AllToolkit 项目。
