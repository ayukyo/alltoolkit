# AllToolkit - Python Cron Utils ⏰

**零依赖 Cron 表达式解析器和任务调度工具 - 生产就绪**

---

## 📖 概述

`cron_utils` 提供功能完整的 Cron 表达式解析、验证和任务调度功能。支持标准 Cron 语法、下一个执行时间计算、以及简单的内存任务调度。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **标准 Cron 语法** - 支持 `*`、`,`、`-`、`/` 所有操作符
- **名称别名** - 支持月份 (jan-dec) 和星期 (sun-sat) 名称
- **表达式验证** - 快速验证 Cron 表达式有效性
- **时间匹配** - 检查 datetime 是否匹配表达式
- **下次执行** - 计算下一个/多个执行时间
- **任务调度** - 简单的内存任务调度器
- **线程安全** - 所有操作线程安全
- **零依赖** - 仅使用 Python 标准库
- **表达式缓存** - 自动缓存已解析表达式

---

## 🚀 快速开始

### 基础使用

```python
from mod import parse, validate, next_run, matches
from datetime import datetime

# 验证表达式
print(validate("0 9 * * *"))  # True
print(validate("60 * * * *"))  # False - 分钟超出范围

# 解析表达式
expr = parse("30 14 * * *")
print(f"分钟：{expr.minutes}")  # {30}
print(f"小时：{expr.hours}")    # {14}

# 检查时间匹配
dt = datetime(2024, 6, 15, 14, 30, 0)
print(matches("30 14 * * *", dt))  # True
print(matches("30 15 * * *", dt))  # False

# 计算下次执行时间
now = datetime.now()
next_dt = next_run("0 9 * * *", after=now)
print(f"下次执行：{next_dt}")

# 计算多个执行时间
from mod import next_runs
runs = next_runs("0 * * * *", count=5, after=now)
for run in runs:
    print(run)
```

### 任务调度

```python
from mod import create_scheduler
from datetime import timedelta

# 创建调度器
scheduler = create_scheduler()

# 添加任务
def my_task():
    print("任务执行了！")

scheduler.add_task(
    "my_task",           # 任务 ID
    "我的任务",          # 任务名称
    "*/5 * * * *",       # Cron 表达式（每 5 分钟）
    my_task              # 回调函数
)

# 查看任务
task = scheduler.get_task("my_task")
print(f"下次执行：{task.schedule.next_execution}")

# 手动执行到期任务
scheduler.run_due_tasks()

# 启用/禁用任务
scheduler.disable_task("my_task")
scheduler.enable_task("my_task")

# 删除任务
scheduler.remove_task("my_task")

# 启动后台调度器（可选）
# scheduler.start(check_interval=10.0)
# scheduler.stop()
```

---

## 📚 API 参考

### 便捷函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `parse(expression)` | 解析 Cron 表达式 | `CronExpression` |
| `validate(expression)` | 验证表达式 | `bool` |
| `matches(expression, dt)` | 检查时间匹配 | `bool` |
| `next_run(expression, after)` | 下次执行时间 | `datetime` 或 `None` |
| `next_runs(expression, count, after)` | 多个执行时间 | `List[datetime]` |
| `create_scheduler()` | 创建调度器 | `CronScheduler` |

### CronParser 类

```python
from mod import CronParser

parser = CronParser()

# 解析表达式
expr = parser.parse("0 9 * * *")

# 验证表达式
is_valid = parser.validate("0 9 * * *")

# 清除缓存
parser.clear_cache()
```

### CronMatcher 类

```python
from mod import CronMatcher

matcher = CronMatcher()

# 检查匹配
matches = matcher.matches("0 9 * * *", datetime.now())

# 下次执行
next_dt = matcher.next_run("0 9 * * *")

# 多个执行时间
runs = matcher.next_runs("0 * * * *", count=5)
```

### CronScheduler 类

| 方法 | 描述 | 返回 |
|------|------|------|
| `add_task(id, name, expr, callback)` | 添加任务 | `ScheduledTask` |
| `remove_task(id)` | 删除任务 | `bool` |
| `get_task(id)` | 获取任务 | `ScheduledTask` 或 `None` |
| `list_tasks()` | 列出所有任务 | `List[ScheduledTask]` |
| `enable_task(id)` | 启用任务 | `bool` |
| `disable_task(id)` | 禁用任务 | `bool` |
| `start(interval)` | 启动后台调度 | `None` |
| `stop()` | 停止调度 | `None` |
| `is_running()` | 检查运行状态 | `bool` |
| `run_due_tasks()` | 手动执行到期任务 | `List[str]` |

### CronExpression 类

| 属性 | 描述 |
|------|------|
| `minutes` | 分钟集合 (0-59) |
| `hours` | 小时集合 (0-23) |
| `days_of_month` | 日期集合 (1-31) |
| `months` | 月份集合 (1-12) |
| `days_of_week` | 星期集合 (0-6, 0=周日) |
| `original` | 原始表达式字符串 |

### ScheduledTask 类

| 属性 | 描述 |
|------|------|
| `id` | 任务唯一标识 |
| `name` | 任务名称 |
| `cron_expr` | Cron 表达式 |
| `callback` | 回调函数 |
| `schedule` | 调度信息 |
| `run_count` | 已执行次数 |
| `last_error` | 最后错误信息 |
| `is_active` | 是否激活 |

---

## 🎯 使用场景

### 1. 每日备份

```python
# 每天凌晨 2 点备份
expr = "0 2 * * *"
next_backup = next_run(expr)
print(f"下次备份时间：{next_backup}")
```

### 2. 工作日提醒

```python
# 工作日早上 9 点提醒
expr = "0 9 * * mon-fri"

scheduler = create_scheduler()
scheduler.add_task(
    "morning_reminder",
    "晨间提醒",
    expr,
    lambda: print("开始工作！")
)
```

### 3. 健康检查

```python
# 每 5 分钟检查一次
expr = "*/5 * * * *"

def check_health():
    # 检查 API、数据库等
    pass

scheduler = create_scheduler()
scheduler.add_task("health_check", "健康检查", expr, check_health)
```

### 4. 定期报告

```python
# 每日报告
scheduler.add_task("daily_report", "日报", "0 7 * * *", generate_daily)

# 每周报告
scheduler.add_task("weekly_report", "周报", "0 9 * * mon", generate_weekly)

# 每月报告
scheduler.add_task("monthly_report", "月报", "0 10 1 * *", generate_monthly)
```

### 5. 维护窗口

```python
# 每周日凌晨 2 点维护
expr = "0 2 * * sun"

def maintenance():
    # 清理临时文件、优化数据库等
    pass

scheduler.add_task("maintenance", "系统维护", expr, maintenance)
```

### 6. 速率限制重置

```python
# 每分钟重置 API 计数
expr = "*/1 * * * *"

# 每天重置配额
daily_expr = "0 0 * * *"

# 每周重置
weekly_expr = "0 0 * * mon"
```

---

## 📋 Cron 语法参考

### 字段位置

```
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日期 (1 - 31)
│ │ │ ┌───────────── 月份 (1 - 12)
│ │ │ │ ┌───────────── 星期 (0 - 6) (周日=0)
│ │ │ │ │
* * * * *
```

### 特殊字符

| 字符 | 描述 | 示例 |
|------|------|------|
| `*` | 任意值 | `*` = 每分钟 |
| `,` | 值列表 | `1,3,5` = 1、3、5 |
| `-` | 范围 | `9-17` = 9 到 17 |
| `/` | 步长 | `*/5` = 每 5 个单位 |

### 常用表达式

| 描述 | 表达式 |
|------|--------|
| 每分钟 | `* * * * *` |
| 每 5 分钟 | `*/5 * * * *` |
| 每小时 | `0 * * * *` |
| 每天午夜 | `0 0 * * *` |
| 每天早上 9 点 | `0 9 * * *` |
| 工作日 9 点 | `0 9 * * mon-fri` |
| 周末 10 点 | `0 10 * * sat,sun` |
| 每月 1 号 | `0 0 1 * *` |
| 每周一 8 点 | `0 8 * * mon` |
| 每季度 | `0 0 1 jan,apr,jul,oct *` |

### 月份和星期别名

**月份：** jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec

**星期：** sun, mon, tue, wed, thu, fri, sat

```python
# 使用别名
parse("0 9 * * mon-fri")  # 工作日 9 点
parse("0 0 1 jan * *")    # 1 月 1 日午夜
```

---

## 🧪 运行测试

```bash
cd cron_utils
python cron_utils_test.py -v
```

### 测试覆盖

- ✅ CronParser 解析功能
- ✅ 所有字段类型（分钟、小时、日期、月份、星期）
- ✅ 特殊字符（`*`、`,`、`-`、`/`）
- ✅ 月份和星期别名
- ✅ 表达式验证
- ✅ 错误处理
- ✅ 表达式缓存
- ✅ CronMatcher 时间匹配
- ✅ 下次执行时间计算
- ✅ 多个执行时间计算
- ✅ CronScheduler 任务管理
- ✅ 任务启用/禁用
- ✅ 任务执行和错误处理
- ✅ 边界情况
- ✅ 集成测试

---

## ⚠️ 注意事项

1. **内存调度器**: 内置调度器是内存级别的，进程重启后任务会丢失。生产环境建议使用持久化方案。

2. **星期匹配**: Cron 中 0=周日，Python 中 0=周一，已自动转换。

3. **时区**: 使用系统本地时区，如需 UTC 请自行转换。

4. **并发执行**: 调度器使用守护线程，任务执行阻塞会影响其他任务。

5. **错误处理**: 任务异常会被捕获并记录在 `last_error`，但不会中断调度器。

6. **检查间隔**: 默认 10 秒检查一次，可根据需求调整。

---

## 🔧 配置选项

```python
# 自定义调度器
scheduler = CronScheduler()

# 启动时配置检查间隔
scheduler.start(check_interval=5.0)  # 每 5 秒检查一次

# 自定义解析器
parser = CronParser()
matcher = CronMatcher(parser)
```

---

## 📁 文件结构

```
cron_utils/
├── mod.py                      # 主要实现
├── cron_utils_test.py          # 测试套件 (100+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.py          # 基础使用示例
    └── advanced_example.py     # 高级使用示例
```

---

## 💡 最佳实践

### 1. 验证表达式

```python
# 总是先验证
if validate(expr):
    scheduler.add_task(...)
else:
    print(f"无效的 Cron 表达式：{expr}")
```

### 2. 任务命名

```python
# 使用有意义的 ID 和名称
scheduler.add_task(
    "daily_backup_prod",  # 唯一 ID
    "生产环境每日备份",    # 可读名称
    "0 2 * * *",
    backup_task
)
```

### 3. 错误处理

```python
def safe_task():
    try:
        # 任务逻辑
        pass
    except Exception as e:
        # 记录错误、发送通知等
        print(f"任务失败：{e}")
        raise  # 重新抛出以便调度器记录

scheduler.add_task("my_task", "我的任务", "0 * * * *", safe_task)
```

### 4. 任务监控

```python
# 定期检查任务状态
for task in scheduler.list_tasks():
    print(f"{task.name}:")
    print(f"  执行次数：{task.run_count}")
    print(f"  下次执行：{task.schedule.next_execution}")
    if task.last_error:
        print(f"  最后错误：{task.last_error}")
```

### 5. 优雅关闭

```python
import atexit

scheduler = create_scheduler()

@atexit.register
def cleanup():
    scheduler.stop()
    print("调度器已停止")
```

---

## 📊 性能考虑

- **表达式缓存**: 相同表达式只解析一次
- **时间复杂度**: next_run 为 O(n)，n 为搜索的分钟数
- **内存占用**: 每个任务约 1KB，适合数百个任务
- **线程安全**: 使用 RLock 保护共享状态

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit

---

## 📄 许可证

MIT License
