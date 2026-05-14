# Shoe Size Utils (鞋码转换工具)

国际鞋码转换工具，支持各国鞋码系统之间的转换。

## 功能特性

- ✅ 支持 11 种鞋码系统转换
- ✅ 鞋码验证
- ✅ 尺码比较
- ✅ 购鞋建议
- ✅ 零外部依赖

## 支持的鞋码系统

| 系统 | 说明 | 单位 |
|------|------|------|
| EU | 欧洲码 | 巴黎点 |
| US_MEN | 美国男码 | Barleycorn |
| US_WOMEN | 美国女码 | Barleycorn |
| US_CHILD | 美国儿童码 | Barleycorn |
| UK | 英国码 | Barleycorn |
| JP | 日本码 | 厘米 |
| CM | 厘米 | 厘米 |
| CN | 中国码 | 毫米 |
| BR | 巴西码 | 巴黎点 |
| KR | 韩国码 | 毫米 |
| MEX | 墨西哥码 | 巴黎点 |

## 快速开始

```python
from shoe_size_utils import convert_shoe_size, get_all_sizes

# 基本转换
us_size = convert_shoe_size(42, "EU", "US_MEN")  # 8.5
uk_size = convert_shoe_size(42, "EU", "UK")      # 8
cn_size = convert_shoe_size(42, "EU", "CN")      # 265 (毫米)

# 获取所有尺码
all_sizes = get_all_sizes(42, "EU")
print(all_sizes)
# {'cm': 26.5, 'eu': 42, 'us_men': 8.5, 'us_women': 10.0, ...}
```

## 主要 API

### `convert_shoe_size(size, from_system, to_system)`
单一鞋码转换。

```python
convert_shoe_size(42, "EU", "US_MEN")  # → 8.5
convert_shoe_size(8.5, "US_MEN", "EU")  # → 42
```

### `get_all_sizes(size, system)`
获取指定鞋码对应的所有系统尺码。

```python
get_all_sizes(42, "EU")
# {'cm': 26.5, 'jp': 26.5, 'eu': 42, 'us_men': 8.5, 'uk': 8, 'cn': 265, ...}
```

### `recommend_shoe_size(foot_length_cm, shoe_type)`
根据脚长推荐鞋码。

```python
recommend_shoe_size(26.5, "running")
# {'推荐EU码': 42.5, '调整原因': '跑步鞋建议大半码，预留脚趾空间'}
```

### `validate_shoe_size(size, system)`
验证鞋码是否在合理范围内。

```python
validate_shoe_size(42, "EU")   # (True, None)
validate_shoe_size(100, "EU")  # (False, "EU码应在 15-52 范围内")
```

### `compare_sizes(size1, system1, size2, system2)`
比较两个鞋码。

```python
compare_sizes(42, "EU", 8.5, "US_MEN")
# {'equal': True, 'difference_cm': 0, ...}
```

## 文件结构

```
shoe_size_utils/
├── __init__.py      # 包入口
├── mod.py           # 主模块
├── shoe_size_utils_test.py  # 测试文件
├── examples/
│   └── usage_examples.py    # 使用示例
└── README.md        # 说明文档
```

## 测试

```bash
python -m pytest shoe_size_utils/shoe_size_utils_test.py -v
```

## 版本

- v1.0.0 (2026-05-14) - 初始版本