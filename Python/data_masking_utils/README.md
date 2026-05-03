# Data Masking Utils - 敏感数据脱敏工具

一个纯Python实现的敏感数据脱敏工具库，零外部依赖，支持多种常见敏感数据的自动识别和脱敏处理。

## 功能特性

- ✅ **手机号脱敏** - 支持中国大陆11位手机号，自动处理分隔符
- ✅ **身份证号脱敏** - 支持15位和18位身份证号
- ✅ **银行卡号脱敏** - 支持16-19位银行卡号，自动格式化
- ✅ **邮箱脱敏** - 保留首字符和域名
- ✅ **姓名脱敏** - 支持中文姓名和英文姓名
- ✅ **地址脱敏** - 智能识别省市区
- ✅ **IP地址脱敏** - 支持IPv4和IPv6
- ✅ **自定义规则** - 支持正则表达式自定义脱敏规则
- ✅ **批量处理** - 支持字典和列表的批量脱敏

## 安装

```python
# 直接复制 data_masking_utils 目录到项目中使用
# 无需安装任何依赖
```

## 快速开始

### 基础使用

```python
from data_masking_utils import (
    mask_phone,
    mask_id_card,
    mask_bank_card,
    mask_email,
    mask_name,
    mask_address,
    mask_ip,
)

# 手机号脱敏
print(mask_phone("13812345678"))  # 输出: 138****5678

# 身份证号脱敏
print(mask_id_card("110101199001011234"))  # 输出: 110101********1234

# 银行卡号脱敏
print(mask_bank_card("6222021234567890"))  # 输出: 6222 **** **** 7890

# 邮箱脱敏
print(mask_email("example@domain.com"))  # 输出: e******@domain.com

# 姓名脱敏
print(mask_name("张三"))  # 输出: 张*
print(mask_name("John Smith"))  # 输出: J*** S****

# 地址脱敏
print(mask_address("北京市朝阳区建国路88号"))  # 输出: 北京市朝阳区***

# IP地址脱敏
print(mask_ip("192.168.1.100"))  # 输出: 192.168.*.*
```

### 使用 DataMasker 类

```python
from data_masking_utils import DataMasker

masker = DataMasker()

# 自动识别并脱敏文本中的敏感信息
text = """
用户信息：
手机：13812345678
身份证：110101199001011234
邮箱：test@example.com
银行卡：6222021234567890
"""

masked_text = masker.mask(text)
print(masked_text)
```

### 字典数据脱敏

```python
user_data = {
    "name": "张三",
    "phone": "13812345678",
    "email": "test@example.com",
    "id_card": "110101199001011234",
    "address": "北京市朝阳区建国路88号"
}

masked_data = masker.mask_dict(user_data)
print(masked_data)
# 输出:
# {
#     "name": "张*",
#     "phone": "138****5678",
#     "email": "t***@example.com",
#     "id_card": "110101********1234",
#     "address": "北京市朝阳区***"
# }
```

### 添加自定义规则

```python
masker = DataMasker()

# 添加工号脱敏规则
masker.add_rule(
    pattern=r"工号：(\d+)",
    keep_start=2,
    keep_end=2,
    name="employee_id"
)

text = "工号：123456"
print(masker.mask(text))  # 输出: 工号：12**56

# 移除规则
masker.remove_rule("employee_id")
```

### 自定义脱敏字符

```python
# 使用 # 作为脱敏字符
print(mask_phone("13812345678", "#"))  # 输出: 138####5678
print(mask_id_card("110101199001011234", "#"))  # 输出: 110101########1234
```

## API 文档

### 函数列表

| 函数 | 说明 |
|------|------|
| `mask_phone(phone, mask_char="*")` | 手机号脱敏 |
| `mask_id_card(id_card, mask_char="*")` | 身份证号脱敏 |
| `mask_bank_card(card, mask_char="*")` | 银行卡号脱敏 |
| `mask_email(email, mask_char="*")` | 邮箱脱敏 |
| `mask_name(name, mask_char="*")` | 姓名脱敏 |
| `mask_address(address, mask_char="*")` | 地址脱敏 |
| `mask_ip(ip, mask_char="*")` | IP地址脱敏 |
| `mask_custom(text, pattern, keep_start, keep_end, mask_char="*")` | 自定义正则脱敏 |
| `mask_string(text, keep_start, keep_end, mask_char="*")` | 通用字符串脱敏 |

### DataMasker 类

```python
class DataMasker:
    def __init__(self, default_mask_char="*"):
        """初始化脱敏器"""
    
    def mask(self, text: str) -> str:
        """对文本进行脱敏"""
    
    def mask_dict(self, data: dict, fields: list = None) -> dict:
        """对字典数据进行脱敏"""
    
    def mask_list(self, data: list) -> list:
        """对列表数据进行脱敏"""
    
    def add_rule(self, pattern, keep_start=0, keep_end=0, 
                 mask_char=None, name=None, handler=None):
        """添加自定义规则"""
    
    def remove_rule(self, name: str):
        """移除规则"""
```

### MaskRule 类

```python
class MaskRule:
    def __init__(self, pattern, mask_char="*", keep_start=0, 
                 keep_end=0, mode=MaskMode.KEEP_BOTH, min_mask_length=1):
        """初始化脱敏规则"""

class MaskMode(Enum):
    KEEP_START = "keep_start"  # 保留开头
    KEEP_END = "keep_end"      # 保留结尾
    KEEP_BOTH = "keep_both"    # 保留两端
    FULL = "full"              # 完全脱敏
    MIDDLE = "middle"          # 保留中间
```

## 使用场景

- 日志脱敏
- 数据导出脱敏
- API响应脱敏
- 数据库查询结果脱敏
- 测试数据生成
- 合规审计数据准备

## 许可证

MIT License