# Datetime Utils


DateTime Utilities - 时间日期工具模块

提供全面的时间日期处理功能，包括格式化、解析、计算、时区转换等。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0


## 功能

### 类

- **DateTimeUtils**: 时间日期工具类
  方法: now, now_utc, today, timestamp, timestamp_ms ... (49 个方法)

### 函数

- **now(**) - 获取当前日期时间
- **format_datetime(dt, fmt**) - 格式化日期时间
- **parse_datetime(date_string, fmt**) - 解析日期时间字符串
- **days_between(start, end**) - 计算两个日期之间的天数差
- **is_leap_year(year**) - 判断是否为闰年
- **get_age(birth_date**) - 计算年龄
- **relative_time(dt**) - 获取相对时间描述
- **now(**) - 获取当前日期时间
- **now_utc(**) - 获取当前 UTC 日期时间
- **today(**) - 获取今天日期（时间为 00:00:00）

... 共 56 个函数

## 使用示例

```python
from mod import now

# 使用 now
result = now()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
