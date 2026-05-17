# Cron Expression Utilities (Rust)

一个完整的 cron 表达式解析、验证和计算工具库。支持标准 5 字段和 6 字段（含秒）格式。

## 功能特性

- **解析 cron 表达式**：将表达式解析为结构化格式
- **验证 cron 表达式**：检查表达式是否有效
- **计算下次执行时间**：计算下一个或多个执行时间点
- **支持特殊字符**：`*`（任意值）、`,`（列表分隔）、`-`（范围）、`/`（步长）
- **支持名称缩写**：月名（jan-dec）、星期名（sun-sat）
- **零外部依赖**：纯 Rust 标准库实现

## 表达式格式

### 5 字段格式
```
┌───────────── 分钟 (0-59)
│ ┌───────────── 小时 (0-23)
│ │ ┌───────────── 月内日 (1-31)
│ │ │ ┌───────────── 月 (1-12)
│ │ │ │ ┌───────────── 周内日 (0-6, 0=周日)
│ │ │ │ │
* * * * *
```

### 6 字段格式（含秒）
```
┌───────────── 秒 (0-59)
│ ┌───────────── 分钟 (0-59)
│ │ ┌───────────── 小时 (0-23)
│ │ │ ┌───────────── 月内日 (1-31)
│ │ │ │ ┌───────────── 月 (1-12)
│ │ │ │ │ ┌───────────── 周内日 (0-6, 0=周日)
│ │ │ │ │ │
* * * * * *
```

## 使用示例

### 基本解析

```rust
use cron_expression_utils::CronExpression;

// 解析 5 字段表达式
let cron = CronExpression::parse("* * * * *").unwrap();
assert!(!cron.has_seconds);

// 解析 6 字段表达式（含秒）
let cron = CronExpression::parse("0 0 0 * * *").unwrap();
assert!(cron.has_seconds);
```

### 获取字段值

```rust
let cron = CronExpression::parse("*/15 9-17 * * mon-fri").unwrap();

// 获取解析后的值
println!("分钟: {:?}", cron.minute_values());  // [0, 15, 30, 45]
println!("小时: {:?}", cron.hour_values());    // [9, 10, 11, 12, 13, 14, 15, 16, 17]
println!("星期: {:?}", cron.day_of_week_values()); // [1, 2, 3, 4, 5]
```

### 人类可读描述

```rust
let cron = CronExpression::parse("*/15 9-17 * * mon-fri").unwrap();
println!("{}", cron.to_human_readable());
// 输出: "at minutes 0, 15, 30, 45 of hours 9, 10, 11, 12, 13, 14, 15, 16, 17 
//        on Monday, Tuesday, Wednesday, Thursday, Friday"
```

### 计算下次执行时间

```rust
let cron = CronExpression::parse("0 12 * * *").unwrap();

// 计算下次执行时间（从指定时间戳）
let timestamp = 1700000000u64; // 2023-11-14 22:13:20 UTC
let next = cron.next_run(timestamp).unwrap();
println!("下次执行: {}", next);

// 计算接下来 5 次执行时间
let runs = cron.next_runs(timestamp, 5).unwrap();
for (i, run) in runs.iter().enumerate() {
    println!("执行 {}: {}", i + 1, run);
}
```

### 便捷函数

```rust
use cron_expression_utils::{validate, next_run, next_runs};

// 验证表达式
if validate("*/5 * * * *").is_ok() {
    println!("表达式有效");
}

// 直接获取下次执行时间
let next = next_run("0 12 * * *", 0).unwrap();  // 0 表示当前时间
let runs = next_runs("0 12 * * *", 0, 5).unwrap();
```

### 预设表达式

```rust
use cron_expression_utils::{get_preset, list_presets};

// 获取预设表达式
let expr = get_preset("every_hour");  // "0 * * * *"
let expr = get_preset("every_weekday"); // "0 0 * * 1-5"

// 列出所有预设
let presets = list_presets();
for (name, expr) in presets {
    println!("{}: {}", name, expr);
}
```

### 可用预设

| 名称 | 表达式 | 说明 |
|------|--------|------|
| every_minute | `* * * * *` | 每分钟 |
| every_hour | `0 * * * *` | 每小时 |
| every_day | `0 0 * * *` | 每天 |
| every_week | `0 0 * * 0` | 每周（周日） |
| every_month | `0 0 1 * *` | 每月（1号） |
| every_year | `0 0 1 1 *` | 每年（1月1日） |
| every_5_minutes | `*/5 * * * *` | 每5分钟 |
| every_15_minutes | `*/15 * * * *` | 每15分钟 |
| every_30_minutes | `*/30 * * * *` | 每30分钟 |
| every_6_hours | `0 */6 * * *` | 每6小时 |
| every_12_hours | `0 */12 * * *` | 每12小时 |
| every_weekday | `0 0 * * 1-5` | 每个工作日 |
| every_weekend | `0 0 * * 0,6` | 每个周末 |

### 时间匹配检查

```rust
let cron = CronExpression::parse("30 14 * * *").unwrap();

// 检查特定时间是否匹配
// 参数: 秒, 分, 时, 日, 月, 星期
assert!(cron.matches(0, 30, 14, 15, 5, 3));  // 14:30 匹配
assert!(!cron.matches(0, 31, 14, 15, 5, 3)); // 14:31 不匹配
assert!(!cron.matches(0, 30, 15, 15, 5, 3)); // 15:30 不匹配
```

## 特殊字符说明

| 字符 | 说明 | 示例 |
|------|------|------|
| `*` | 任意值 | `* * * * *` (每分钟) |
| `,` | 列表分隔 | `0,15,30,45 * * * *` (每15分钟) |
| `-` | 范围 | `0 9-17 * * *` (工作时间) |
| `/` | 步长 | `*/10 * * * *` (每10分钟) |

## 组合使用示例

```rust
// 工作时间（9am-5pm）内每10分钟
let cron = CronExpression::parse("*/10 9-17 * * mon-fri").unwrap();

// 每月1号和15号中午
let cron = CronExpression::parse("0 12 1,15 * *").unwrap();

// 工作日早9点
let cron = CronExpression::parse("0 9 * * mon-fri").unwrap();

// 一月和七月每天
let cron = CronExpression::parse("0 0 * jan,jul *").unwrap();
```

## 错误处理

```rust
use cron_expression_utils::{CronExpression, CronError};

let result = CronExpression::parse("invalid");
match result {
    Err(CronError::InvalidFieldCount { expected, got }) => {
        println!("字段数错误: 期望 {}, 实际 {}", expected, got);
    }
    Err(CronError::InvalidValue { field, value, reason }) => {
        println!("值错误: 字段 {}, 值 {}, 原因: {}", field, value, reason);
    }
    Err(CronError::InvalidRange { field, range }) => {
        println!("范围错误: 字段 {}, 范围 {}", field, range);
    }
    Err(CronError::InvalidStep { field, step }) => {
        println!("步长错误: 字段 {}, 步长 {}", field, step);
    }
    Err(CronError::NoNextRunTime) => {
        println!("无法找到下次执行时间");
    }
    Ok(_) => {}
}
```

## 测试覆盖

- 37 个单元测试全部通过
- 测试覆盖所有核心功能：
  - 基本解析
  - 6 字段格式
  - 范围、列表、步长
  - 月名、星期名
  - 时间匹配
  - 下次执行时间计算
  - 人类可读描述
  - 预设表达式
  - 错误处理

## 应用场景

- 任务调度系统
- 定时任务管理
- 日历提醒
- 数据同步
- 日志轮转
- 报表生成
- 自动化运维

## 许可证

MIT License