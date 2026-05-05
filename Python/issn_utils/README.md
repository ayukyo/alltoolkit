# ISSN Utilities Module

ISSN (International Standard Serial Number) 验证与处理工具库，零外部依赖。

## 功能特性

### 核心验证
- ISSN-8（8位标准格式）验证
- ISSN-13（EAN-13格式）验证
- ISSN-L（链接ISSN）验证
- 支持带分隔符和不带分隔符的格式

### 格式转换
- ISSN-8 ↔ ISSN-13 双向转换
- 多种格式输出（紧凑、带分隔符）
- ISSN-L 格式生成

### 检验位计算
- ISSN-8 模11算法（支持 X 表示10）
- ISSN-13 EAN-13算法（交替权重1和3）
- 检验位有效性分析

### 批量操作
- 多ISSN批量验证
- 文本中提取ISSN
- ISSN对比（判断是否同一出版物）

### 工具功能
- ISSN生成（用于测试）
- ISSN解析与信息提取
- 变体获取（ISSN-8、ISSN-13、ISSN-L）
- 打印版识别（启发式）

## 安装

```python
# 无需安装，直接导入
from issn_utils.mod import *
```

## 快速使用

### 验证

```python
from issn_utils.mod import is_issn8, is_issn13, is_valid_issn, get_issn_type

# ISSN-8 验证
is_issn8("0378-5955")  # True
is_issn8("2434-561X")  # True (X 检验位)

# ISSN-13 验证
is_issn13("9770378595001")  # True

# 通用验证
is_valid_issn("0378-5955")  # True
is_valid_issn("9770378595001")  # True

# 获取类型
get_issn_type("0378-5955")  # "ISSN-8"
get_issn_type("9770378595001")  # "ISSN-13"
```

### 格式化

```python
from issn_utils.mod import format_issn, format_issn_compact

# 添加分隔符
format_issn("03785955")  # "0378-5955"
format_issn("9770378595001")  # "977-0378-5950-01"

# 移除分隔符
format_issn_compact("0378-5955")  # "03785955"
```

### 转换

```python
from issn_utils.mod import issn8_to_issn13, issn13_to_issn8, convert_issn

# ISSN-8 转 ISSN-13
issn8_to_issn13("0378-5955")  # "9770378595001"

# ISSN-13 转 ISSN-8
issn13_to_issn8("9770378595001")  # "03785955"

# 通用转换
convert_issn("0378-5955", "ISSN-13")  # "9770378595001"
convert_issn("9770378595001", "ISSN-8")  # "03785955"
```

### ISSN-L

```python
from issn_utils.mod import is_issn_l, format_issn_l, extract_issn_l

# 验证 ISSN-L 格式
is_issn_l("ISSN-L: 0378-5955")  # True
is_issn_l("0378-5955")  # True

# 格式化为 ISSN-L
format_issn_l("0378-5955")  # "ISSN-L: 0378-5955"

# 提取 ISSN
extract_issn_l("ISSN-L: 0378-5955")  # "03785955"
```

### 检验位

```python
from issn_utils.mod import calculate_issn_check_digit, calculate_issn13_check_digit

# ISSN-8 检验位（模11算法）
calculate_issn_check_digit("0378595")  # "5"
calculate_issn_check_digit("2434561")  # "X" (值为10)

# ISSN-13 检验位（EAN-13算法）
calculate_issn13_check_digit("977037859500")  # "1"
```

### 解析

```python
from issn_utils.mod import parse_issn, get_issn_variants

# 详细解析
info = parse_issn("0378-5955")
# {
#     'valid': True,
#     'type': 'ISSN-8',
#     'clean': '03785955',
#     'formatted': '0378-5955',
#     'check_digit': '5',
#     'issn8': '03785955',
#     'issn13': '9770378595001',
#     'issn_l': 'ISSN-L: 0378-5955'
# }

# 获取所有变体
variants = get_issn_variants("0378-5955")
# {
#     'issn8': '03785955',
#     'issn13': '9770378595001',
#     'formatted8': '0378-5955',
#     'formatted13': '977-0378-5950-01',
#     'issn_l': 'ISSN-L: 0378-5955'
# }
```

### 批量操作

```python
from issn_utils.mod import validate_issns, find_issns_in_text

# 批量验证
results = validate_issns(["0378-5955", "invalid", "9770378595001"])
# {
#     "0378-5955": {'valid': True, 'type': 'ISSN-8', ...},
#     "invalid": {'valid': False, ...},
#     "9770378595001": {'valid': True, 'type': 'ISSN-13', ...}
# }

# 从文本提取
text = "期刊 ISSN 0378-5955 可订阅。另见 2434-561X。"
found = find_issns_in_text(text)  # ['03785955', '2434561X']
```

### 对比

```python
from issn_utils.mod import compare_issns

# 判断两个ISSN是否同一出版物
compare_issns("0378-5955", "9770378595001")  # True
compare_issns("0378-5955", "0378-5956")  # False
```

### 生成（测试用途）

```python
from issn_utils.mod import generate_issn, generate_issn13, generate_issn_l

# 生成 ISSN-8
issn = generate_issn()  # 随机有效 ISSN-8

# 生成 ISSN-13
issn13 = generate_issn13()

# 生成 ISSN-L
issn_l = generate_issn_l()  # "ISSN-L: XXXX-XXXX"

# 带前缀生成
issn = generate_issn("037")  # 以 037 开头的 ISSN-8
```

## 真实ISSN示例

| ISSN | 出版物 |
|------|--------|
| 0028-0836 | Nature |
| 0001-0782 | Communications of the ACM |
| 0036-8075 | Science |
| 0018-9448 | IEEE Transactions on Information Theory |
| 2434-561X | 示例（X检验位） |

## 算法说明

### ISSN-8 检验位
- 权重：8, 7, 6, 5, 4, 3, 2（位置1-7）
- 计算总和，模11，取补数
- 结果为10时用 'X' 表示

### ISSN-13 检验位
- 前缀：977（ISSN专用）
- 权重交替：1, 3, 1, 3, ...
- 模10计算

## 依赖

- Python 3.6+
- 无外部依赖（仅使用标准库）

## 许可证

MIT License