# Dial Code Utils

国际电话区号工具模块，提供国家代码查询、电话号码格式化和验证功能。

## 功能

- **区号查询**: 根据国家名称或代码查询国际电话区号
- **国家查询**: 根据电话区号查询对应国家信息
- **电话号码格式化**: 支持国际格式、E.164 格式、本地格式
- **号码验证**: 验证电话号码格式是否正确
- **区号提取**: 从完整电话号码中提取区号
- **国家搜索**: 支持模糊搜索国家

## 安装

```bash
# 直接导入
from dial_code_utils.mod import get_dial_code_by_country, format_phone_number

# 或使用工具类
from dial_code_utils.mod import DialCodeUtils
```

## 快速开始

```python
from dial_code_utils.mod import (
    get_country_by_dial_code,
    get_dial_code_by_country,
    format_phone_number,
    validate_phone_number,
    extract_dial_code,
)

# 查询区号对应国家
country = get_country_by_dial_code("86")
print(f"86 区号对应: {country['name']}")  # 中国

# 查询国家对应区号
code = get_dial_code_by_country("中国")
print(f"中国的区号: {code}")  # 86

# 格式化电话号码
formatted = format_phone_number("13800138000", "86", "international")
print(formatted)  # +86 138 0013 8000

# 验证电话号码
valid, result = validate_phone_number("13800138000", "86")
print(f"有效: {valid}")  # True

# 从号码中提取区号
code, local = extract_dial_code("+8613800138000")
print(f"区号: {code}, 本地号码: {local}")  # 86, 13800138000
```

## 支持的国家和地区

本模块包含全球 200+ 国家和地区的电话区号数据，包括：

- **亚洲**: 中国(86)、日本(81)、韩国(82)、印度(91)、泰国(66) 等
- **欧洲**: 英国(44)、法国(33)、德国(49)、俄罗斯(7)、意大利(39) 等
- **非洲**: 南非(27)、尼日利亚(234)、肯尼亚(254) 等
- **北美**: 美国/加拿大(1)、墨西哥(52) 等
- **南美**: 巴西(55)、阿根廷(54)、哥伦比亚(57) 等
- **大洋洲**: 澳大利亚(61)、新西兰(64) 等

## API 参考

### 查询函数

| 函数 | 说明 |
|------|------|
| `get_country_by_dial_code(dial_code)` | 根据区号获取国家信息 |
| `get_dial_code_by_country(country)` | 根据国家名/代码获取区号 |
| `get_all_countries()` | 获取所有国家列表 |
| `get_countries_by_continent(continent)` | 按大洲获取国家列表 |

### 格式化函数

| 函数 | 说明 |
|------|------|
| `format_phone_number(phone, dial_code, format_type)` | 格式化电话号码 |
| `extract_dial_code(phone)` | 从号码中提取区号 |
| `get_country_name(dial_code, lang)` | 获取国家名称 |

### 验证函数

| 函数 | 说明 |
|------|------|
| `validate_phone_number(phone, dial_code)` | 验证电话号码 |
| `is_valid_dial_code(dial_code)` | 检查区号是否有效 |
| `search_countries(query)` | 搜索国家 |
| `compare_dial_codes(code1, code2)` | 比较两个区号 |

### 格式化类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `international` | 国际格式 | `+86 138 0013 8000` |
| `e164` | E.164 格式 | `+8613800138000` |
| `local` | 本地格式 | `138-0013-8000` |
| `readable` | 易读格式 | `+86 138-0013-8000` |

## DialCodeUtils 工具类

```python
from dial_code_utils.mod import DialCodeUtils

# 获取国家信息
country = DialCodeUtils.get_country("86")

# 获取区号
code = DialCodeUtils.get_dial_code("中国")

# 格式化电话
formatted = DialCodeUtils.format_phone("13800138000", "86")

# 验证电话
valid, result = DialCodeUtils.validate("13800138000", "86")

# 搜索国家
results = DialCodeUtils.search("中国")
```

## 数据结构

### 国家信息字典

```python
{
    "name": "中国",           # 国家名称
    "code": "CN",            # ISO alpha-2 代码
    "alpha3": "CHN",         # ISO alpha-3 代码
    "numeric": "156",        # 数字代码
    "continent": "亚洲"      # 所属大洲
}
```

## 运行测试

```bash
python test_dial_code_utils.py -v
```

## License

MIT License