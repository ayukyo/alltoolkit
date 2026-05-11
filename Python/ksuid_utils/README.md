# KSUID Utilities 🆔

KSUID (K-Sortable Unique Identifier) 生成、解析、验证和分析工具。

## 功能

- ✅ **KSUID 生成** - 生成时间排序的唯一标识符
- 🔍 **KSUID 解析** - 解析 KSUID 提取时间戳和随机部分
- 📝 **KSUID 验证** - 验证 KSUID 格式正确性
- ⏱️ **时间戳提取** - 从 KSUID 中提取创建时间
- 📅 **日期时间转换** - KSUID 与 datetime 相互转换
- ⚖️ **KSUID 比较** - 比较两个 KSUID 的创建顺序
- 📊 **排序功能** - 按时间排序 KSUID 列表
- 🔄 **单调生成** - 保证顺序的单调 KSUID 生成
- 📈 **批量处理** - 批量生成和解析 KSUID
- 📋 **格式化输出** - 多种格式展示 KSUID
- 🔎 **完整分析** - KSUID 综合分析报告

## KSUID 特性

- **27 字符长度** - Base62 编码
- **160 位总长度** - 32 位时间戳 + 128 位随机数
- **时间排序** - 自然按创建时间排序
- **自定义 Epoch** - 从 2014-05-13 开始，延长使用寿命
- **约 136 年寿命** - 从 Epoch 起可使用约 136 年

## 快速开始

```python
from mod import generate, parse, validate

# 生成 KSUID
ksuid = generate()  # 'aWgEPTl1tmebfsQzFP4qxw980'

# 解析 KSUID
result = parse(ksuid)
# {'valid': True, 'timestamp': 1640995200, 'datetime': '2022-01-01T00:00:00+00:00'}

# 验证 KSUID
validate(ksuid)  # True
```

## 运行测试

```bash
python Python/ksuid_utils/ksuid_utils_test.py
```

## 许可证

MIT License