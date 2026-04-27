# Natural Time Parser Utils


Natural Time Parser Utilities - 自然语言时间解析工具模块

解析人类友好的时间表达式，支持中英文混合输入。
零依赖，仅使用 Python 标准库。

支持的格式：
- 相对时间：in 5 minutes, 2小时后, 3天后的下午
- 绝对时间：tomorrow, next monday, 下周三
- 时间点：at 3pm, 早上8点, 下午3点半
- 组合表达式：tomorrow at 3pm, 下周一早上9点

Author: AllToolkit
Version: 1.0.0


## 功能

### 类

- **ParseError**: 解析错误异常
- **NaturalTimeParser**: 自然语言时间解析器
  方法: parse
- **DurationParser**: 时长解析器
  方法: parse, format_duration
- **TimeExpressionExtractor**: 时间表达式提取器
  方法: extract
- **RelativeTimeFormatter**: 相对时间格式化器
  方法: format

### 函数

- **parse_time(text, reference**) - 解析自然语言时间表达式
- **parse_duration(text**) - 解析时长表达式
- **format_duration(duration, language**) - 格式化时长
- **extract_times(text**) - 从文本中提取时间表达式
- **relative_time(dt, reference, language**) - 格式化相对时间
- **when(text, reference**) - when() 函数别名，用于解析自然语言时间
- **how_long(text**) - how_long() 函数别名，用于解析时长表达式
- **parse(self, text**) - 解析自然语言时间表达式
- **parse(cls, text**) - 解析时长表达式
- **format_duration(cls, duration, language**) - 格式化时长

... 共 12 个函数

## 使用示例

```python
from mod import parse_time

# 使用 parse_time
result = parse_time()
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
