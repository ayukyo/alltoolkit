# Fuzzy Clock Utils

模糊时钟工具模块，将精确时间转换为人类可读的模糊时间表达。

## 功能

- **模糊时间转换**: 将时间转换为"三点过一刻"、"快四点了"等表达
- **口语化时间**: 生成"早上八点半"、"晚上七点"等自然表达
- **时间段查询**: 获取"上午"、"下午"、"傍晚"等时间范围描述
- **近似时间**: "三点左右"、"快四点了"等近似表达
- **相对时间**: "十分钟后"、"三天前"等相对时间描述
- **多语言支持**: 支持中文(zh)和英文(en)

## 安装

```bash
# 直接导入
from fuzzy_clock_utils.mod import fuzzy_time, colloquial_time

# 或使用工具类
from fuzzy_clock_utils.mod import FuzzyClock
```

## 快速开始

```python
from fuzzy_clock_utils.mod import (
    fuzzy_time,
    colloquial_time,
    time_range,
    approximate_time,
    relative_time,
    FuzzyClock,
)

# 模糊时间
result = fuzzy_time(hour=14, minute=30, language="zh")
print(result)  # 两点半 或 三点半 (取决于精度设置)

# 口语化时间
result = colloquial_time(hour=8, minute=30, language="zh")
print(result)  # 早上八点半

# 时间段
result = time_range(hour=15, minute=0, language="zh")
print(result)  # 下午

# 近似时间
result = approximate_time(hour=10, minute=55, language="zh")
print(result)  # 快十一点了

# 相对时间
from datetime import datetime, timedelta
future = datetime.now() + timedelta(hours=2)
result = relative_time(dt=future, language="zh")
print(result)  # 两小时后
```

## 精度级别

| 精度 | 说明 | 示例 |
|------|------|------|
| `exact` | 精确到5分钟 | 三点过五分、差十分四点 |
| `fuzzy` | 使用一刻/半小时 | 三点一刻、差一刻四点 |
| `approximate` | 非常模糊 | 三点左右、快四点了 |

## API 参考

### 主要函数

| 函数 | 说明 |
|------|------|
| `fuzzy_time(dt, hour, minute, language, precision)` | 转换为模糊时间 |
| `colloquial_time(dt, hour, minute, language)` | 转换为口语化时间 |
| `time_range(dt, hour, minute, language)` | 获取时间范围描述 |
| `approximate_time(dt, hour, minute, language)` | 转换为近似时间 |
| `relative_time(dt, language)` | 转换为相对时间 |

### FuzzyClock 类

```python
from fuzzy_clock_utils.mod import FuzzyClock

# 创建实例
clock = FuzzyClock(language="zh", precision="fuzzy")

# 获取模糊时间
result = clock.fuzzy_time(hour=14, minute=30)

# 获取口语化时间
result = clock.to_colloquial(hour=14, minute=30)

# 获取时间范围
result = clock.time_range(hour=14, minute=30)

# 获取近似时间
result = clock.to_approximate_time(hour=14, minute=30)
```

## 时间段映射 (中文)

| 小时范围 | 时间段 |
|----------|--------|
| 0-4 | 深夜 |
| 5-7 | 清晨 |
| 8-10 | 上午 |
| 11-12 | 中午 |
| 13 | 午后 |
| 14-16 | 下午 |
| 17-18 | 傍晚 |
| 19-21 | 晚上 |
| 22-23 | 深夜 |

## 时间段映射 (英文)

| 小时范围 | 时间段 |
|----------|--------|
| 0-4 | late night |
| 5-7 | early morning |
| 8-11 | morning |
| 12-13 | noon |
| 14-16 | afternoon |
| 17-18 | evening |
| 19-21 | night |
| 22-23 | late night |

## 运行测试

```bash
python test_fuzzy_clock_utils.py -v
```

## License

MIT License