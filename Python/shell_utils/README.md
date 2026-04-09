# AllToolkit - Shell Utilities 🐚

**零依赖 Python Shell 命令执行与系统操作工具库**

---

## 📖 概述

`shell_utils` 是一个功能强大的 Shell 工具模块，提供命令执行、进程管理、文件操作、系统信息查询等功能。完全使用 Python 标准库实现（subprocess, os, pathlib, shutil, sys, platform），无需任何外部依赖。

### 核心功能

- 🚀 **命令执行**: 支持同步/异步执行、超时控制、stdin 输入
- 🔍 **进程管理**: 查找、终止、监控进程
- 📁 **文件操作**: 创建、复制、移动、删除、权限管理
- 🖥️ **系统信息**: 平台检测、磁盘使用、内存信息
- 🌐 **网络工具**: ping、IP 地址查询
- 🔧 **环境变量**: 读取、设置、批量加载 .env 文件
- ⚡ **快捷命令**: ls, pwd, echo, cat, grep, find 等常用命令封装
- 📦 **批处理**: 顺序/并行执行多个命令、管道操作

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/shell_utils/mod.py your_project/
```

### 基础使用

```python
from mod import *

# 执行命令
result = run_command('ls -la')
print(result.stdout)
print(f"耗时：{result.duration:.2f}s")

# 检查命令是否存在
if command_exists('git'):
    print("Git 已安装")

# 获取系统信息
print(f"操作系统：{get_os_type().value}")
print(f"Python 版本：{get_platform_info()['python_version']}")

# 文件操作
create_directory('/tmp/my_project')
copy_file('source.txt', 'backup.txt')

# 进程管理
pids = find_processes_by_name('python')
print(f"找到 {len(pids)} 个 Python 进程")
```

---

## 📚 API 参考

### 系统信息工具

| 函数 | 描述 | 示例 |
|------|------|------|
| `get_os_type()` | 获取操作系统类型 | `get_os_type()` → `OSType.LINUX` |
| `is_windows()` | 检查是否为 Windows | `is_windows()` → `False` |
| `is_unix()` | 检查是否为 Unix-like | `is_unix()` → `True` |
| `get_shell()` | 获取默认 Shell | `get_shell()` → `/bin/bash` |
| `get_platform_info()` | 获取平台详细信息 | `get_platform_info()['os']` |
| `get_hostname()` | 获取主机名 | `get_hostname()` |
| `get_username()` | 获取用户名 | `get_username()` |
| `get_home_directory()` | 获取主目录 | `get_home_directory()` |

### 命令执行

| 函数 | 描述 | 示例 |
|------|------|------|
| `run_command(command, cwd, env, timeout, shell, ...)` | 执行命令 | `run_command('ls -la')` |
| `run_command_checked(command, **kwargs)` | 执行并检查返回码 | `run_command_checked('git status')` |
| `run_command_async(command)` | 异步执行命令 | `proc = run_command_async('sleep 10')` |

### 进程管理

| 函数 | 描述 | 示例 |
|------|------|------|
| `kill_process(pid, signal_num)` | 终止进程 | `kill_process(12345)` |
| `process_exists(pid)` | 检查进程是否存在 | `process_exists(12345)` |
| `get_process_count()` | 获取进程数量 | `get_process_count()` |
| `find_processes_by_name(name)` | 按名称查找进程 | `find_processes_by_name('python')` |

### 文件与路径操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `which(command)` | 查找命令路径 | `which('python')` |
| `command_exists(command)` | 检查命令是否存在 | `command_exists('git')` |
| `get_current_directory()` | 获取当前目录 | `pwd()` |
| `change_directory(path)` | 切换目录 | `change_directory('/tmp')` |
| `create_directory(path, parents, exist_ok)` | 创建目录 | `create_directory('/tmp/a/b', parents=True)` |
| `remove_directory(path, recursive)` | 删除目录 | `remove_directory('/tmp/old')` |
| `file_exists(path)` | 检查文件是否存在 | `file_exists('config.json')` |
| `directory_exists(path)` | 检查目录是否存在 | `directory_exists('/tmp')` |
| `get_file_size(path)` | 获取文件大小 | `get_file_size('file.txt')` |
| `format_file_size(bytes)` | 格式化文件大小 | `format_file_size(1536)` → "1.50 KB" |
| `copy_file(src, dst)` | 复制文件 | `copy_file('a.txt', 'b.txt')` |
| `move_file(src, dst)` | 移动文件 | `move_file('a.txt', '/tmp/a.txt')` |
| `delete_file(path)` | 删除文件 | `delete_file('temp.txt')` |

### 环境变量

| 函数 | 描述 | 示例 |
|------|------|------|
| `get_env_var(name, default)` | 获取环境变量 | `get_env_var('PATH')` |
| `set_env_var(name, value)` | 设置环境变量 | `set_env_var('DEBUG', '1')` |
| `get_all_env_vars()` | 获取所有环境变量 | `get_all_env_vars()` |
| `load_env_file(path)` | 加载 .env 文件 | `load_env_file('.env')` |

### 系统操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `get_temp_directory()` | 获取临时目录 | `get_temp_directory()` |
| `create_temp_file(suffix, prefix, dir)` | 创建临时文件 | `create_temp_file('.txt', 'tmp_')` |
| `create_temp_directory(suffix, prefix, dir)` | 创建临时目录 | `create_temp_directory()` |
| `get_disk_usage(path)` | 获取磁盘使用 | `get_disk_usage('/')` |
| `get_memory_info()` | 获取内存信息 | `get_memory_info()` |

### 网络工具

| 函数 | 描述 | 示例 |
|------|------|------|
| `ping(host, count, timeout)` | Ping 主机 | `ping('8.8.8.8')` |
| `get_local_ip()` | 获取本地 IP | `get_local_ip()` |
| `get_public_ip()` | 获取公网 IP | `get_public_ip()` |

### 快捷命令

| 函数 | 描述 | 示例 |
|------|------|------|
| `ls(path, args)` | 列出目录 | `ls('/tmp', '-la')` |
| `pwd()` | 当前目录 | `pwd()` |
| `echo(text)` | 输出文本 | `echo('hello')` |
| `cat(file_path)` | 读取文件 | `cat('file.txt')` |
| `grep(pattern, file_path, args)` | 搜索内容 | `grep('error', 'log.txt')` |
| `find_files(path, name_pattern, type_filter, max_depth)` | 查找文件 | `find_files('.', '*.py')` |
| `chmod(path, mode)` | 修改权限 | `chmod('script.sh', '755')` |
| `mkdir_p(path)` | 创建目录 | `mkdir_p('/tmp/a/b/c')` |
| `rm_rf(path)` | 递归删除 | `rm_rf('/tmp/old')` |
| `cp(src, dst, recursive)` | 复制 | `cp('a.txt', 'b.txt')` |
| `mv(src, dst)` | 移动 | `mv('old.txt', 'new.txt')` |

### 批处理

| 函数 | 描述 | 示例 |
|------|------|------|
| `run_commands_sequential(commands, stop_on_error)` | 顺序执行 | `run_commands_sequential(['cmd1', 'cmd2'])` |
| `run_commands_parallel(commands, max_workers)` | 并行执行 | `run_commands_parallel(['cmd1', 'cmd2'], 4)` |
| `pipe_commands(commands)` | 管道执行 | `pipe_commands(['ls', 'grep .py', 'wc -l'])` |

### 数据类

| 类 | 描述 | 属性 |
|------|------|------|
| `CommandResult` | 命令执行结果 | `returncode`, `stdout`, `stderr`, `command`, `duration`, `success` |
| `ProcessInfo` | 进程信息 | `pid`, `name`, `status`, `cpu_percent`, `memory_percent`, `username` |
| `OSType` | 操作系统类型枚举 | `LINUX`, `MACOS`, `WINDOWS`, `FREEBSD`, `OTHER` |

---

## 💡 使用示例

### 1. 执行命令并处理输出

```python
from mod import *

# 基本执行
result = run_command('git log --oneline -5')
if result.success:
    print("最近的提交:")
    for line in result.stdout.strip().split('\n'):
        print(f"  {line}")
else:
    print(f"错误：{result.stderr}")
```

### 2. 带超时的命令执行

```python
# 设置 5 秒超时
result = run_command('slow_command', timeout=5)
if not result.success and 'Timeout' in result.stderr:
    print("命令执行超时!")
```

### 3. 批量执行命令

```python
# 顺序执行（出错停止）
commands = [
    'git pull',
    'npm install',
    'npm run build',
    'npm test'
]
results = run_commands_sequential(commands, stop_on_error=True)

for i, result in enumerate(results):
    print(f"命令 {i+1}: {'✓' if result.success else '✗'}")
```

### 4. 查找并终止进程

```python
# 查找所有 Python 进程
pids = find_processes_by_name('python')
print(f"找到 {len(pids)} 个 Python 进程")

# 终止特定进程
for pid in pids:
    if process_exists(pid):
        print(f"终止进程 {pid}")
        kill_process(pid)
```

### 5. 系统监控

```python
# 获取系统信息
info = get_platform_info()
print(f"系统：{info['os']}")
print(f"Python: {info['python_version']}")

# 磁盘使用
disk = get_disk_usage('/')
print(f"磁盘使用：{disk['percent']}%")
print(f"  总计：{format_file_size(disk['total'])}")
print(f"  已用：{format_file_size(disk['used'])}")
print(f"  剩余：{format_file_size(disk['free'])}")

# 内存使用
mem = get_memory_info()
print(f"内存使用：{mem['percent']}%")
```

### 6. 环境变量管理

```python
# 加载 .env 文件
env_vars = load_env_file('.env')
for key, value in env_vars.items():
    set_env_var(key, value)
    print(f"设置 {key}={value}")

# 获取数据库配置
db_host = get_env_var('DB_HOST', 'localhost')
db_port = get_env_var('DB_PORT', '5432')
```

### 7. 临时文件处理

```python
# 创建临时文件
temp_file, fd = create_temp_file(prefix='data_', suffix='.json')
print(f"临时文件：{temp_file}")

# 写入数据
with os.fdopen(fd, 'w') as f:
    f.write('{"key": "value"}')

# 使用完毕后删除
delete_file(temp_file)
```

### 8. 网络诊断

```python
# 检查网络连通性
result = ping('8.8.8.8', count=4)
if result['success']:
    print("网络正常")
else:
    print("网络异常!")

# 获取 IP 地址
print(f"本地 IP: {get_local_ip()}")
print(f"公网 IP: {get_public_ip()}")
```

### 9. 文件搜索

```python
# 查找所有 Python 文件
py_files = find_files('/home/project', '*.py', type_filter='f', max_depth=5)
print(f"找到 {len(py_files)} 个 Python 文件")

# 查找配置文件
config_files = find_files('.', '*.{json,yaml,yml}', max_depth=3)
```

### 10. 管道命令

```python
# 等效于：ls -la | grep .py | wc -l
result = pipe_commands(['ls -la', 'grep .py', 'wc -l'])
print(f"Python 文件数量：{result.stdout.strip()}")
```

---

## 🔒 安全注意事项

### 命令注入防护

```python
# ❌ 危险：直接拼接用户输入
user_input = "file.txt; rm -rf /"
run_command(f'cat {user_input}')  # 危险!

# ✅ 安全：使用列表形式
run_command(['cat', user_input])  # 安全

# ✅ 安全：验证输入
if not user_input.replace('/', '').replace('.', '').isalnum():
    raise ValueError("非法文件名")
run_command(f'cat {user_input}')
```

### 权限检查

```python
# 检查是否有足够权限
if is_unix() and get_username() != 'root':
    print("警告：非 root 用户，某些操作可能失败")
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/shell_utils
python shell_utils_test.py
```

测试覆盖：
- ✓ 系统信息工具
- ✓ 命令执行
- ✓ 快捷命令
- ✓ 文件操作
- ✓ 环境变量
- ✓ 临时文件
- ✓ 磁盘和内存信息
- ✓ 网络工具
- ✓ 文件查找
- ✓ 顺序执行命令
- ✓ 进程管理
- ✓ 异步执行
- ✓ 操作系统特定功能
- ✓ 边界情况处理

---

## 📝 常量

| 常量 | 值 | 描述 |
|------|-----|------|
| `DEFAULT_ENCODING` | `'utf-8'` | 默认编码 |
| `DEFAULT_TIMEOUT` | `30` | 默认超时时间（秒） |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 📦 零依赖优势

- ✅ 无需 pip 安装
- ✅ 适用于受限环境
- ✅ 无版本冲突问题
- ✅ 启动速度快
- ✅ 易于审计和安全检查

---

**AllToolkit - 让系统操作更简单! 🐚**
