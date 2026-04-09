# Log Utils - Python 日志处理工具模块

AllToolkit 的 Python 日志处理工具模块，提供全面的日志解析、过滤、分析和格式化功能。

## 📦 功能特性

### 日志解析
- `parse_log_level()` - 从日志行提取日志级别
- `parse_timestamp()` - 从日志行提取时间戳
- `parse_apache_log()` - 解析 Apache 日志格式
- `parse_nginx_log()` - 解析 Nginx 日志格式
- `parse_syslog()` - 解析 Syslog 格式
- `parse_json_log()` - 解析 JSON 格式日志
- `parse_log_line()` - 自动检测并解析日志行

### 日志级别
- `LogLevel` 枚举 - 标准日志级别（TRACE/DEBUG/INFO/WARN/ERROR/CRITICAL/FATAL）
- `LogEntry` 类 - 结构化日志条目表示

### 日志过滤
- `filter_by_level()` - 按日志级别过滤
- `filter_by_time_range()` - 按时间范围过滤
- `filter_by_pattern()` - 按正则表达式过滤
- `filter_by_source()` - 按来源/标签过滤

### 日志分析
- `count_by_level()` - 按级别统计
- `count_by_hour()` - 按小时统计
- `get_error_summary()` - 获取最常见错误摘要
- `calculate_error_rate()` - 计算错误率
- `detect_anomalies()` - 检测日志量异常

### 日志格式化
- `format_log_entry()` - 格式化日志条目
- `to_json_lines()` - 转为 JSON Lines 格式
- `to_csv()` - 转为 CSV 格式

### 日志搜索
- `search_logs()` - 搜索日志（支持通配符）
- `extract_field()` - 提取特定字段

### 日志轮转
- `get_log_files()` - 获取目录中的日志文件
- `get_file_size()` - 获取文件大小
- `get_file_age_days()` - 获取文件年龄
- `find_rotation_candidates()` - 查找需要轮转的文件

### 工具函数
- `tail_log()` - 读取日志文件末尾 N 行
- `merge_log_files()` - 合并多个日志文件
- `generate_sample_log()` - 生成示例日志（用于测试）

## 🚀 快速开始

### 安装

无需安装，直接使用：

```python
import sys
sys.path.insert(0, '/path/to/AllToolkit/Python/log_utils')
from mod import *
```

### 基本用法

```python
from mod import *

# 解析日志行
line = "2024-01-15 10:30:45 ERROR Database connection failed"
entry = parse_log_line(line)
print(entry.level)    # LogLevel.ERROR
print(entry.message)  # "Database connection failed"

# 解析 Apache 日志
apache_line = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /path HTTP/1.0" 200 2326'
parsed = parse_apache_log(apache_line)
print(parsed['ip'])     # "127.0.0.1"
print(parsed['status']) # 200

# 过滤日志
logs = [parse_log_line(line) for line in log_lines]
errors_only = filter_by_level(logs, LogLevel.ERROR)

# 按模式过滤
database_logs = filter_by_pattern(logs, r'Database|SQL', case_sensitive=False)

# 按时间范围过滤
from datetime import datetime, timedelta
now = datetime.now()
recent = filter_by_time_range(logs, start_time=now - timedelta(hours=1))

# 日志分析
level_counts = count_by_level(logs)
print(level_counts)  # {'INFO': 50, 'ERROR': 10, 'DEBUG': 40}

error_rate = calculate_error_rate(logs)
print(f"错误率：{error_rate:.2%}")

# 获取最常见错误
top_errors = get_error_summary(logs, top_n=5)
for msg, count in top_errors:
    print(f"{count}x: {msg}")

# 检测异常
anomalies = detect_anomalies(logs, threshold_multiplier=3.0)
for ts in anomalies:
    print(f"异常时间点：{ts}")

# 搜索日志
results = search_logs(logs, 'connection * failed')
for r in results:
    print(r.message)

# 格式化输出
for entry in errors_only:
    print(format_log_entry(entry, '[%(timestamp)s] %(level)s: %(message)s'))

# 转为 JSON Lines
jsonl = to_json_lines(errors_only)

# 转为 CSV
csv_data = to_csv(errors_only, columns=['timestamp', 'level', 'message'])

# 读取日志文件末尾
last_lines = tail_log('/var/log/app.log', lines=100)

# 生成示例日志（用于测试）
sample_logs = generate_sample_log(count=1000)
```

## 📁 文件结构

```
log_utils/
├── mod.py                  # 主模块（所有工具函数）
├── log_utils_test.py       # 测试套件（70+ 测试）
├── README.md               # 本文档
└── examples/
    └── usage_examples.py   # 使用示例
```

## ✅ 测试

运行测试套件：

```bash
cd /path/to/AllToolkit/Python/log_utils
python3 log_utils_test.py
```

预期输出：
```
============================================================
  AllToolkit Log Utils - Test Suite
============================================================
  ✅ [所有测试通过...]
============================================================
  Tests: 70+ | Passed: 70+ | Failed: 0
============================================================
```

## 📖 示例

运行使用示例：

```bash
cd /path/to/AllToolkit/Python/log_utils/examples
python3 usage_examples.py
```

## 💡 实际应用场景

### 1. 日志监控告警

```python
def check_log_health(log_file_path):
    """检查日志健康状态"""
    with open(log_file_path, 'r') as f:
        logs = [parse_log_line(line) for line in f.readlines()]
    
    error_rate = calculate_error_rate(logs)
    
    if error_rate > 0.1:  # 错误率超过 10%
        return {'status': 'CRITICAL', 'error_rate': error_rate}
    elif error_rate > 0.05:  # 错误率超过 5%
        return {'status': 'WARNING', 'error_rate': error_rate}
    else:
        return {'status': 'HEALTHY', 'error_rate': error_rate}
```

### 2. 日志聚合分析

```python
def analyze_service_logs(log_files):
    """分析多个服务日志文件"""
    all_logs = []
    for log_file in log_files:
        with open(log_file, 'r') as f:
            for line in f:
                entry = parse_log_line(line)
                if entry:
                    all_logs.append(entry)
    
    # 按小时统计
    hourly_dist = count_by_hour(all_logs)
    
    # 错误摘要
    top_errors = get_error_summary(all_logs, top_n=10)
    
    # 检测异常
    anomalies = detect_anomalies(all_logs)
    
    return {
        'total_logs': len(all_logs),
        'level_distribution': count_by_level(all_logs),
        'hourly_distribution': hourly_dist,
        'top_errors': top_errors,
        'anomalies': anomalies,
    }
```

### 3. 实时日志过滤

```python
def tail_and_filter(log_file, level_filter='WARNING', pattern=None):
    """实时监控日志并过滤"""
    import time
    
    with open(log_file, 'r') as f:
        # 移动到文件末尾
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            entry = parse_log_line(line)
            if entry:
                # 按级别过滤
                if entry.level.value >= LogLevel.from_string(level_filter).value:
                    # 按模式过滤
                    if pattern is None or re.search(pattern, entry.message, re.I):
                        print(f"[{entry.timestamp}] {entry.level.name}: {entry.message}")
```

### 4. 日志轮转检查

```python
def check_rotation_needed(log_dir, max_size_mb=100, max_age_days=30):
    """检查哪些日志需要轮转"""
    candidates = find_rotation_candidates(
        log_dir,
        max_size_mb=max_size_mb,
        max_age_days=max_age_days
    )
    
    for candidate in candidates:
        reasons = ', '.join(candidate['reason'])
        print(f"{candidate['path']}: {candidate['size_mb']:.1f}MB, "
              f"{candidate['age_days']:.1f}天 - 需要轮转 ({reasons})")
    
    return candidates
```

### 5. Apache/Nginx 访问日志分析

```python
def analyze_access_log(log_file):
    """分析 Web 服务器访问日志"""
    with open(log_file, 'r') as f:
        requests = [parse_apache_log(line) for line in f if parse_apache_log(line)]
    
    # 状态码统计
    status_counts = Counter(r['status'] for r in requests if r.get('status'))
    
    # 404 错误
    not_found = [r for r in requests if r.get('status') == 404]
    
    # 最频繁访问的路径
    path_counts = Counter(r['path'] for r in requests if r.get('path'))
    
    # 最频繁的 IP
    ip_counts = Counter(r['ip'] for r in requests if r.get('ip'))
    
    return {
        'total_requests': len(requests),
        'status_codes': dict(status_counts),
        '404_count': len(not_found),
        'top_paths': path_counts.most_common(10),
        'top_ips': ip_counts.most_common(10),
    }
```

### 6. Syslog 分析

```python
def analyze_syslog(log_file):
    """分析系统日志"""
    with open(log_file, 'r') as f:
        entries = [parse_syslog(line) for line in f if parse_syslog(line)]
    
    # 按服务统计
    service_counts = Counter(e['tag'] for e in entries if e.get('tag'))
    
    # 严重错误
    critical = [e for e in entries if e.get('severity', 7) <= 3]
    
    return {
        'total_entries': len(entries),
        'services': dict(service_counts),
        'critical_count': len(critical),
    }
```

## 🔒 安全特性

- **输入验证** - 所有函数处理 None 安全
- **错误处理** - 解析失败返回 None 而非抛出异常
- **编码处理** - 文件读取使用 UTF-8 并忽略错误字符

## 📊 性能特点

- **零依赖** - 仅使用 Python 标准库
- **高效实现** - 使用正则表达式和内置函数
- **流式处理** - tail_log 支持大文件高效读取
- **内存友好** - 分析函数可处理大型日志文件

## 📝 支持的日志格式

| 格式 | 示例 | 解析函数 |
|------|------|----------|
| 通用日志 | `2024-01-15 10:30:45 ERROR msg` | `parse_log_line()` |
| Apache | `127.0.0.1 - - [10/Oct/2000:13:55:36] "GET / HTTP/1.0" 200 1234` | `parse_apache_log()` |
| Nginx | 同 Apache 格式 | `parse_nginx_log()` |
| Syslog | `<13>Jan 15 10:30:45 host app[1234]: msg` | `parse_syslog()` |
| JSON | `{"timestamp": "...", "level": "INFO", "message": "..."}` | `parse_json_log()` |

## 📖 日志级别

| 级别 | 值 | 说明 |
|------|-----|------|
| TRACE | 0 | 最详细的调试信息 |
| DEBUG | 10 | 调试信息 |
| INFO | 20 | 一般信息 |
| WARN | 30 | 警告信息 |
| ERROR | 40 | 错误信息 |
| CRITICAL | 50 | 严重错误 |
| FATAL | 60 | 致命错误 |

## 📝 许可证

MIT License - 详见 AllToolkit 主项目 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请在 AllToolkit 仓库提交 Issue。
