# 自然语言日期解析工具库 (natural_date_utils)

解析中文自然语言日期表达式，转换为精确的 datetime 对象。

## 功能特点

- **零外部依赖**：仅使用 Python 标准库
- **丰富的表达式支持**：相对日期、星期日期、月度日期、年度日期、节日等
- **时间组合解析**：支持日期与时间组合表达式
- **中文数字支持**：自动转换中文数字（三天后、十五天后等）
- **时间段解析**：凌晨、早上、上午、下午、晚上等
- **批量处理**：支持批量解析和文本日期提取

## 支持的表达式类型

### 相对日期
- `今天`、`明天`、`后天`、`昨天`、`前天`、`大后天`、`大前天`
- `今天下午3点`、`明天早上8点`、`昨天晚上9点`

### 星期日期
- `周一`、`周三`、`周五`、`周日`
- `下周二`、`上周五`、`这周四`
- `下周三下午3点`

### 月度日期
- `下个月`、`上个月`
- `下个月15号`、`月底`、`月末`

### 年度日期
- `明年`、`今年`、`去年`
- `明年5月`、`去年国庆节`

### 节日日期
- `元旦`、`情人节`、`劳动节`、`儿童节`、`国庆节`、`圣诞节` 等16个节日

### 绝对日期
- `2024年5月20日`
- `5月20日`
- `2024年6月1日下午3点`

### 数字天数
- `3天后`、`7天前`
- `2周后`、`1个月后`、`1年后`

### 时间段
- `凌晨` (0-6点)、`早上` (6-9点)、`上午` (9-12点)
- `中午` (11-14点)、`下午` (14-18点)、`傍晚` (17-19点)
- `晚上` (18-22点)、`深夜` (22-24点)

### 日期范围
- `这周`、`下周`、`这个月`、`下个月`

## 快速使用

```python
from datetime import datetime
from natural_date_utils import parse, parse_with_info, NaturalDateParser

# 快速解析
dt = parse("明天下午3点")
print(dt)  # 2024-01-16 15:00:00

# 获取详细信息
result = parse_with_info("下周三")
print(result.date_type)  # 'weekday'
print(result.has_time)   # False

# 使用解析器
parser = NaturalDateParser(now=datetime(2024, 1, 15, 10, 30))
result = parser.parse("国庆节")
print(result.datetime_obj)  # 2024-10-01 00:00:00
```

## API

### 便捷函数

| 函数 | 说明 |
|------|------|
| `parse(text, now)` | 快速解析，返回 datetime 或 None |
| `parse_with_info(text, now)` | 解析，返回 ParseResult 详细信息 |
| `is_valid(text, now)` | 检查是否能解析为有效日期 |
| `get_date_type(text, now)` | 获取日期表达式类型 |
| `parse_range(text, now)` | 解析日期范围，返回 (start, end) |
| `parse_batch(texts, now)` | 批量解析多个表达式 |
| `extract_dates(text, now)` | 从文本中提取所有日期 |

### NaturalDateParser 类

```python
parser = NaturalDateParser(now=None, strict=False)
result = parser.parse(text)
```

### ParseResult 数据类

| 属性 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 是否成功解析 |
| `datetime_obj` | datetime | 解析结果 |
| `original_text` | str | 原始文本 |
| `normalized_text` | str | 标准化文本 |
| `date_type` | DateType | 日期类型 |
| `confidence` | float | 解析置信度 (0.0-1.0) |
| `has_time` | bool | 是否包含时间 |
| `error_message` | str | 错误信息（失败时） |

### DateType 枚举

| 值 | 说明 |
|----|------|
| `ABSOLUTE` | 绝对日期 (2024年1月1日) |
| `RELATIVE` | 相对日期 (今天、明天、昨天) |
| `WEEKDAY` | 星期日期 (周一、下周三) |
| `MONTHLY` | 月度日期 (每月15号) |
| `YEARLY` | 年度日期 (明年、今年) |
| `RANGE` | 日期范围 (这周、下个月) |
| `UNKNOWN` | 未知/无法解析 |

## 应用场景

- 日程安排系统
- 提醒/定时任务系统
- 客服对话理解
- 聊天机器人日期理解
- 自然语言查询接口

## 测试

```bash
python -m pytest natural_date_utils_test.py -v
```

测试覆盖：65+ 测试用例，涵盖所有解析类型和边界场景。