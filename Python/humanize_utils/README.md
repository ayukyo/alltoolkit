# Humanize Utils


humanize_utils - 人性化格式工具库
将各种数据转换为人类可读的格式

功能：
- 文件大小格式化（1024 → "1.00 KB"）
- 时间间隔格式化（3600 → "1小时"）
- 数字格式化（1000000 → "1M"）
- 相对时间格式化（时间戳 → "3分钟前"）
- 持续时间格式化（秒数 → "01:30:45"）
- 列表格式化（["a", "b", "c"] → "a、b 和 c"）


## 功能

### 函数

- **format_bytes(size, precision, binary**, ...) - 将字节数格式化为人类可读格式
- **parse_size(size_str**) - 解析文件大小字符串为字节数
- **format_number(number, precision, use_chinese**) - 将大数字格式化为缩写形式
- **format_percentage(value, precision, show_sign**) - 格式化百分比
- **format_with_commas(number, decimal_places**) - 用千分位分隔符格式化数字
- **format_duration(seconds, format_type, use_chinese**, ...) - 将秒数格式化为持续时间
- **format_relative_time(timestamp, reference, use_chinese**) - 将时间戳格式化为相对时间（如"3分钟前"）
- **format_time_ago(seconds, use_chinese**) - 将过去的秒数格式化为"多长时间前"
- **format_list(items, use_chinese, limit**, ...) - 将列表格式化为自然语言字符串
- **format_phone(phone, format_type**) - 格式化电话号码

... 共 15 个函数

## 使用示例

```python
from mod import format_bytes

# 使用 format_bytes
result = format_bytes()
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
