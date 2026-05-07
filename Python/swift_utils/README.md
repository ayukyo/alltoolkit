# Swift Utils - SWIFT/BIC银行代码验证工具

提供SWIFT/BIC代码的完整验证、解析和生成功能。SWIFT代码（也称BIC代码）是国际银行识别的标准代码，用于国际银行转账、证券交易等金融业务。

## 功能特性

- SWIFT/BIC代码格式验证（8位或11位）
- 详细解析：银行代码、国家代码、地区代码、分行代码
- 国家信息查询（支持249个国家和地区）
- 银行代码生成
- 主要办公机构判断
- SWIFT代码比较
- 包含常见银行示例数据

## SWIFT代码结构

```
位置:  1-4  | 5-6 | 7-8 | 9-11
内容:  BBBB | CC  | LL   | BBB
含义:  银行 | 国家| 地区 | 分行
```

- **银行代码（4位）**: 由SWIFT组织分配给银行
- **国家代码（2位）**: ISO 3166-1 alpha-2国家代码
- **地区代码（2位）**: 表示银行所在地区
- **分行代码（3位，可选）**: 表示特定分行，XXX表示主要办公机构

## 安装

```python
# 直接导入使用，零依赖
from swift_utils.mod import SwiftUtils, BicUtils
```

## 快速开始

### 验证

```python
from swift_utils.mod import SwiftUtils

# 验证SWIFT代码
print(SwiftUtils.validate("BKCHCNBJ"))  # True (中国银行)
print(SwiftUtils.validate("HSBCGB2L"))  # True (汇丰银行)
print(SwiftUtils.validate("DEUTDEFF"))  # True (德意志银行)

# 验证11位代码
print(SwiftUtils.validate("BKCHCNBJXXX"))  # True (主要办公机构)
print(SwiftUtils.validate("BKCHCNBJA01"))  # True (特定分行)

# 严格验证（返回详细错误信息）
valid, errors = SwiftUtils.validate_strict("INVALID")
print(valid)  # False
print(errors)  # ["SWIFT代码长度应为8位或11位..."]
```

### 解析

```python
from swift_utils.mod import SwiftUtils

# 解析SWIFT代码
info = SwiftUtils.parse("BKCHCNBJ")
print(info)
# {
#     'swift_code': 'BKCHCNBJ',
#     'bank_code': 'BKCH',
#     'country_code': 'CN',
#     'location_code': 'BJ',
#     'branch_code': None,
#     'country_name': '中国',
#     'country_name_en': 'China',
#     'country_currency': 'CNY',
#     'bank_name': '中国银行',
#     'bank_name_en': 'Bank of China',
#     'network_status': '活跃',
#     'code_type': '主要办公机构',
#     'length': 8,
#     'is_primary': True
# }

# 解析特定分行
info2 = SwiftUtils.parse("BKCHCNBJA01")
print(info2["branch_code"])  # A01
print(info2["is_primary"])   # False
```

### 提取

```python
from swift_utils.mod import SwiftUtils

swift = "BKCHCNBJXXX"

# 提取各部分代码
print(SwiftUtils.get_bank_code(swift))      # BKCH
print(SwiftUtils.get_country_code(swift))   # CN
print(SwiftUtils.get_location_code(swift))  # BJ
print(SwiftUtils.get_branch_code(swift))    # XXX
```

### 生成

```python
from swift_utils.mod import SwiftUtils

# 生成8位主要办公机构代码
swift1 = SwiftUtils.generate_primary("BKCH", "CN", "BJ")
print(swift1)  # BKCHCNBJ

# 生成11位分行代码
swift2 = SwiftUtils.generate_branch("BKCH", "CN", "BJ", "XXX")
print(swift2)  # BKCHCNBJXXX

swift3 = SwiftUtils.generate_branch("DEUT", "DE", "FF", "500")
print(swift3)  # DEUTDEFF500
```

### 比较

```python
from swift_utils.mod import SwiftUtils

# 比较两个SWIFT代码
result = SwiftUtils.compare("BKCHCNBJ", "BKCHCNBJXXX")
print(result)
# {
#     'same_bank': True,
#     'same_country': True,
#     'same_location': True,
#     'same_bank_system': True,
#     'is_related': True
# }

# 比较不同银行
result2 = SwiftUtils.compare("BKCHCNBJ", "HSBCGB2L")
print(result2["same_bank"])      # False
print(result2["same_country"])   # False
print(result2["is_related"])     # False
```

### 国家信息

```python
from swift_utils.mod import SwiftUtils

# 获取国家信息
info = SwiftUtils.get_country_info("CN")
print(info)
# {'code': 'CN', 'name': '中国', 'name_en': 'China', 'currency': 'CNY'}

info2 = SwiftUtils.get_country_info("US")
print(info2)
# {'code': 'US', 'name': '美国', 'name_en': 'United States', 'currency': 'USD'}

# 获取所有国家列表
countries = SwiftUtils.get_all_countries()
print(f"支持 {len(countries)} 个国家")
# 支持 249 个国家
```

### 主要办公机构判断

```python
from swift_utils.mod import SwiftUtils

# 判断是否为主要办公机构
print(SwiftUtils.is_primary_office("BKCHCNBJ"))      # True (8位)
print(SwiftUtils.is_primary_office("BKCHCNBJXXX"))   # True (XXX分行)
print(SwiftUtils.is_primary_office("BKCHCNBJA01"))   # False (特定分行)

# 获取主要办公机构代码
primary = SwiftUtils.get_primary_code("BKCHCNBJA01")
print(primary)  # BKCHCNBJ
```

### 格式化

```python
from swift_utils.mod import SwiftUtils

# 格式化SWIFT代码（转大写，去除空格和连字符）
print(SwiftUtils.format("bkchcnbj"))       # BKCHCNBJ
print(SwiftUtils.format("BKCH CNBJ"))      # BKCHCNBJ
print(SwiftUtils.format("BKCH-CNBJ-XXX"))  # BKCHCNBJXXX
```

### BIC别名

```python
from swift_utils.mod import BicUtils

# BIC是SWIFT的别名，提供相同功能
print(BicUtils.validate("BKCHCNBJ"))       # True
print(BicUtils.get_bank_code("BKCHCNBJ"))  # BKCH
print(BicUtils.get_country_code("BKCHCNBJ"))  # CN
```

### 便捷函数

```python
from swift_utils.mod import (
    validate_swift, validate_bic, parse_swift, parse_bic,
    get_swift_bank_code, get_swift_country, is_swift_primary, format_swift
)

# 快速验证
print(validate_swift("BKCHCNBJ"))  # True

# 快速解析
info = parse_swift("BKCHCNBJ")

# 快速提取
print(get_swift_bank_code("BKCHCNBJ"))  # BKCH
print(get_swift_country("BKCHCNBJ"))    # CN

# 快速判断
print(is_swift_primary("BKCHCNBJ"))  # True

# 快速格式化
print(format_swift("bkch cnbj"))  # BKCHCNBJ
```

## API 参考

### SwiftUtils 类

| 方法 | 描述 |
|------|------|
| `validate(swift_code)` | 验证SWIFT代码格式 |
| `validate_strict(swift_code)` | 严格验证，返回错误信息 |
| `parse(swift_code)` | 解析SWIFT代码详细信息 |
| `get_bank_code(swift_code)` | 提取银行代码 |
| `get_country_code(swift_code)` | 提取国家代码 |
| `get_location_code(swift_code)` | 提取地区代码 |
| `get_branch_code(swift_code)` | 提取分行代码 |
| `generate_primary(bank, country, location)` | 生成8位代码 |
| `generate_branch(bank, country, location, branch)` | 生成11位代码 |
| `is_primary_office(swift_code)` | 判断是否主要办公机构 |
| `get_primary_code(swift_code)` | 获取主要办公机构代码 |
| `compare(swift1, swift2)` | 比较两个SWIFT代码 |
| `format(swift_code)` | 格式化SWIFT代码 |
| `get_country_info(country_code)` | 获取国家信息 |
| `get_all_countries()` | 获取所有国家列表 |
| `get_all_bank_examples()` | 获取银行示例数据 |
| `search_by_country(country_code)` | 搜索指定国家的银行 |

### BicUtils 类

BIC (Bank Identifier Code) 是 SWIFT 代码的别名，提供与 SwiftUtils 相同的方法。

### 枚举类

```python
class SwiftCodeType:
    PRIMARY = "主要办公机构"
    BRANCH = "特定分行"
    GENERAL = "通用代码"

class SwiftNetworkStatus:
    ACTIVE = "活跃"
    PASSIVE = "被动"
    TEST = "测试"
    DELETED = "已删除"
```

## 测试

```bash
# 运行测试
python -m pytest swift_utils_test.py -v

# 或直接运行
python swift_utils_test.py
```

## 常见SWIFT代码示例

| SWIFT代码 | 银行 | 国家 |
|-----------|------|------|
| BKCHCNBJ | 中国银行 | 中国 |
| ICBKCNBJ | 中国工商银行 | 中国 |
| HSBCGB2L | 汇丰银行 | 英国 |
| DEUTDEFF | 德意志银行 | 德国 |
| CITIUS33 | 花旗银行 | 美国 |
| BOFAUS3N | 美国银行 | 美国 |
| BNPAFRPP | 法国巴黎银行 | 法国 |
| UBSWCHZH | 瑞银集团 | 瑞士 |

## 依赖

无外部依赖，仅使用 Python 标准库。

## 作者

AllToolkit

## 版本

1.0.0