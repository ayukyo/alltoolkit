# Date Utils 模块生成报告

## 📦 模块信息

- **名称**: date_utils
- **语言**: Rust
- **版本**: 1.0.0
- **许可证**: MIT
- **依赖**: 零依赖（仅使用 Rust 标准库）

## ✨ 功能特性

### 核心功能

1. **日期创建**
   - `Date::new(year, month, day)` - 带验证的日期创建
   - `Date::today()` - 获取当前日期
   - `Date::from_timestamp(ts)` - 从 Unix 时间戳创建

2. **日期解析**
   - 支持多种格式：ISO (YYYY-MM-DD)、欧洲 (DD/MM/YYYY)、美国 (MM/DD/YYYY)、紧凑 (YYYYMMDD)
   - 智能格式检测

3. **日期格式化**
   - 自定义格式字符串
   - 支持：YYYY, YY, MM, M, MMMM, MMM, DD, D, DDD, EEEE, EEE, W
   - 单引号转义普通文本

4. **日期计算**
   - `add_days()`, `subtract_days()` - 加减天数
   - `add_months()`, `subtract_months()` - 加减月份（自动调整月末）
   - `add_years()`, `subtract_years()` - 加减年份（处理闰年）
   - 运算符重载：`+`, `-`

5. **日期比较**
   - `is_before()`, `is_after()`, `is_equal()` - 比较操作
   - `is_between()` - 范围检查
   - `days_difference()` - 天数差

6. **日期信息**
   - `year()`, `month()`, `day()` - 基本属性
   - `weekday()` - 星期几
   - `day_of_year()` - 一年中的第几天
   - `is_leap_year()` - 闰年检测
   - `days_in_month()` - 月份天数

7. **时间戳转换**
   - `to_timestamp()` - 转为 Unix 时间戳
   - `from_timestamp()` - 从时间戳创建

8. **日期范围**
   - `date_range()` - 生成日期范围
   - `date_range_step()` - 带步长的范围
   - `weekdays_in_range()` - 工作日范围
   - `weekends_in_range()` - 周末范围

9. **边界日期**
   - `first_day_of_month()`, `last_day_of_month()`
   - `first_day_of_year()`, `last_day_of_year()`

## 📁 文件结构

```
date_utils/
├── Cargo.toml              # 项目配置
├── mod.rs                  # 主模块（825+ 行）
├── tests.rs                # 单元测试（660+ 行）
├── README.md               # 使用文档
├── GENERATION_REPORT.md    # 本文件
└── examples/
    ├── basic_usage.rs      # 基本用法示例
    ├── date_arithmetic.rs  # 日期计算示例
    ├── date_range.rs       # 日期范围示例
    └── formatting.rs       # 格式化示例
```

## 🧪 测试覆盖

- **总测试数**: 76 个单元测试 + 1 个文档测试
- **测试类别**:
  - 日期创建测试 (7)
  - 闰年测试 (4)
  - 月份天数测试 (4)
  - 星期测试 (4)
  - 月份测试 (3)
  - 一年中的第几天测试 (3)
  - 时间戳测试 (3)
  - 日期算术测试 (15+)
  - 日期比较测试 (5)
  - 边界日期测试 (4)
  - 日期解析测试 (6)
  - 日期格式化测试 (10+)
  - 日期范围测试 (4)
  - 运算符测试 (3)
  - 显示测试 (3)
  - 边界情况测试 (5)
  - 工具函数测试 (2)

## 📊 代码统计

| 文件 | 行数 | 说明 |
|------|------|------|
| mod.rs | 825+ | 核心实现 |
| tests.rs | 660+ | 完整测试套件 |
| README.md | 230+ | 详细文档 |
| 示例代码 | 4 个文件 | 实用示例 |

## 🎯 设计亮点

1. **零依赖**: 不使用任何外部 crate，编译快速，二进制小
2. **类型安全**: 使用 Rust 类型系统确保正确性
3. **Copy 语义**: `Date` 是 Copy 类型，栈上分配，无堆分配
4. **优雅错误处理**: 使用 `Result` 类型返回错误
5. **完整测试**: 76+ 测试覆盖所有功能
6. **详细文档**: README + 代码注释 + 示例
7. **运算符重载**: 直观的 `+`, `-` 操作
8. **灵活格式化**: 支持多种格式符和转义

## 🚀 使用示例

```rust
use date_utils::{Date, parse_date, format_date};

// 创建和解析
let date = Date::new(2024, 3, 15).unwrap();
let date = parse_date("2024-03-15").unwrap();

// 格式化
format_date(&date, "YYYY-MM-DD");  // "2024-03-15"
format_date(&date, "EEEE, MMMM D, YYYY");  // "Friday, March 15, 2024"

// 计算
date.add_days(30);
date.add_months(1);
date.add_years(1);

// 比较
date1.is_before(&date2);
date1.days_difference(&date2);

// 范围
let range = date_utils::date_range(&start, &end);
let weekdays = date_utils::weekdays_in_range(&start, &end);
```

## 🔧 构建和测试

```bash
cd Rust/date_utils

# 编译
cargo build

# 运行测试
cargo test

# 运行示例
cargo run --example basic_usage
cargo run --example date_arithmetic
cargo run --example date_range
cargo run --example formatting

# 发布构建
cargo build --release
```

## 📝 注意事项

1. 格式化字符串中的普通文本需要用单引号转义：`'Day ' DDD ' of year'`
2. 闰年 2 月 29 日加年时会自动调整为 28 日（非闰年）
3. 月末日期加减月份时会自动调整到目标月份的最后一天
4. 时间戳使用 Unix epoch (1970-01-01) 作为基准

## 📄 许可证

MIT License - 与 AllToolkit 主仓库保持一致。

---

**生成时间**: 2026-04-11
**生成者**: AllToolkit Auto-Generator
