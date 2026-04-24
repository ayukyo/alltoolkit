# IMEI Utilities

IMEI (International Mobile Equipment Identity) 验证、解析和生成工具。

## 功能

- ✅ **验证** - 使用 Luhn 算法验证 IMEI 号码
- 📋 **解析** - 提取 TAC、SNR 和校验位
- 🎨 **格式化** - 支持多种输出格式
- 🎲 **生成** - 生成随机有效的 IMEI（测试用）
- 🔍 **提取** - 从文本中提取 IMEI 号码
- ⚖️ **比较** - 比较两个 IMEI 的差异
- 🏷️ **TAC 信息** - 查询 TAC 基本信息o

## IMEI 结构

IMEI 是 15 位数字：
```
AA-BBBBBB-CCCCCC-D
│  │       │      └─ 校验位 (1位)
│  │       └──────── SNR 序列号 (6位)
│  └──────────────── TAC 类型分配码 (6位)
└─────────────────── 报告机构标识 (2位)
```

## 安装

```python
from imei_utils.mod import validate, parse, generate_random
```

## 快速开始

### 验证 IMEI

```python
from imei_utils.mod import validate

# 验证 IMEI (verified correct)
validate("490154203237518")  # True
validate("49-015420-323751-8")  # True (支持分隔符)
validate("490154203237519")  # False (错误的校验位)
```

### 解析 IMEI

```python
from imei_utils.mod import parse

result = parse("490154203237518")
# {
#     'tac': '49015420',
#     'snr': '323751',
#     'cd': '8',
#     'valid': True
# }
```

### 格式化 IMEI

```python
from imei_utils.mod import format_imei

imei = "490154203237518"

format_imei(imei, "standard")  # "49-015420-323751-8"
format_imei(imei, "compact")   # "490154203237518"
format_imei(imei, "spaced")    # "49 015420 323751 8"
```

### 生成测试 IMEI

```python
from imei_utils.mod import generate_random, generate_batch

# 生成随机 IMEI
imei = generate_random()  # 返回有效的 15 位 IMEI

# 指定 TAC 生成
imei = generate_random("35209900")  # 以指定 TAC 开头

# 批量生成
imeis = generate_batch(10)  # 生成 10 个不同的 IMEI
```

### 校验位计算

```python
from imei_utils.mod import calculate_check_digit

cd = calculate_check_digit("35209900176148")
# 返回 8
```

### 从文本提取

```python
from imei_utils.mod import extract_digits

text = "设备 IMEI: 352099001761488"
imeis = extract_digits(text)
# ['352099001761488']
```

### 类式验证器

```python
from imei_utils.mod import IMEIValidator

validator = IMEIValidator("352099001761488")

validator.is_valid     # True
validator.tac          # "35209900"
validator.snr          # "176148"
validator.check_digit  # "8"
validator.format("standard")  # "35-209900-176148-8"
```

## API 参考

### 函数

| 函数 | 说明 |
|------|------|
| `validate(imei)` | 验证 IMEI 有效性 |
| `parse(imei)` | 解析 IMEI 结构 |
| `format_imei(imei, style)` | 格式化 IMEI |
| `generate_random(tac?)` | 生成随机 IMEI |
| `generate_batch(count, tac?)` | 批量生成 IMEI |
| `calculate_check_digit(imei14)` | 计算校验位 |
| `get_tac_info(tac)` | 获取 TAC 信息 |
| `compare_imei(imei1, imei2)` | 比较两个 IMEI |
| `extract_digits(text)` | 从文本提取 IMEI |

### 类

```python
class IMEIValidator:
    def __init__(self, imei: str)
    @property is_valid -> bool
    @property tac -> str | None
    @property snr -> str | None
    @property check_digit -> str | None
    def format(style) -> str
```

## 测试

```bash
cd Python/imei_utils
python imei_utils_test.py
```

## 依赖

零外部依赖，仅使用 Python 标准库。

## 许可证

MIT