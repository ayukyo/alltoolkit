# Mask Utils - 敏感数据脱敏工具

零依赖的 Python 敏感数据掩码/脱敏工具库，用于日志、调试、数据展示等场景。

## 功能特性

- 🔒 **多种数据类型支持**: 邮箱、手机号、身份证、银行卡、信用卡、姓名、地址、IP、密码、URL
- 🔍 **自动检测**: 自动识别文本中的敏感信息并掩码
- 📦 **批量处理**: 支持批量掩码字典数据
- ⚙️ **高度可定制**: 可配置可见字符数、掩码字符等
- 🚀 **零依赖**: 纯 Python 标准库实现

## 安装

```python
# 直接复制 mask_utils.py 到项目中即可使用
from mask_utils import mask_email, mask_phone
```

## 快速开始

```python
from mask_utils import mask_email, mask_phone, mask_id_card

# 邮箱掩码
print(mask_email("user@example.com"))      # us**@*******.com

# 手机号掩码
print(mask_phone("13812345678"))           # 138****5678

# 身份证掩码
print(mask_id_card("110101199001011234"))   # 11**************34
```

## API 文档

### mask_email(email, visible_prefix=2, visible_domain=1, mask_char="*")

掩码邮箱地址。

```python
mask_email("admin@company.co.uk")
# 输出: ad***@******.co.uk

mask_email("test@demo.cn", visible_prefix=1)
# 输出: t***@****.cn
```

### mask_phone(phone, visible_prefix=3, visible_suffix=4, mask_char="*")

掩码手机号码，支持带国际区号的格式。

```python
mask_phone("13812345678")           # 138****5678
mask_phone("+86 138-1234-5678")     # +86 138****5678
```

### mask_id_card(id_number, visible_prefix=2, visible_suffix=2, mask_char="*")

掩码身份证号码。

```python
mask_id_card("110101199001011234")  # 11**************34
```

### mask_bank_card(card_number, visible_prefix=4, visible_suffix=4, mask_char="*")

掩码银行卡号。

```python
mask_bank_card("6222021234567890123")  # 6222***********0123
```

### mask_credit_card(card_number, show_last4=True, mask_char="*")

掩码信用卡号，格式化为 `****-****-****-xxxx`。

```python
mask_credit_card("4532015112830366")  # ****-****-****-0366
```

### mask_name(name, show_last_char=True, mask_char="*")

掩码姓名，自动识别中文和英文。

```python
mask_name("张三")        # 张*
mask_name("王小明")      # 王**
mask_name("John Smith")  # J*** S****
```

### mask_address(address, show_start=10, show_end=5, mask_char="*")

掩码地址。

```python
mask_address("北京市朝阳区建国路88号SOHO现代城A座1001")
# 输出: 北京市朝阳区建国路******A座1001
```

### mask_ip(ip, mask_octets=2, mask_char="*")

掩码 IP 地址（支持 IPv4 和 IPv6）。

```python
mask_ip("192.168.1.100")  # 192.168.*.*
mask_ip("2001:0db8:85a3:::0370:7334")  # 2001:0db8:*:*:*:*:*:*
```

### mask_password(password, show_length=True, mask_char="*")

掩码密码。

```python
mask_password("MySecret123!")  # ************ (12 chars)
```

### mask_url(url, mask_query=True, mask_path=False, mask_char="***")

掩码 URL 中的敏感查询参数。

```python
mask_url("https://api.example.com/data?token=secret123&name=test")
# 输出: https://api.example.com/data?token=***&name=test
```

敏感参数默认包括: `token`, `key`, `secret`, `password`, `pwd`, `auth`, `api_key`, `apikey`, `access_token`, `refresh_token`, `session`, `session_id`

### mask_custom(text, pattern, mask_char="*")

使用正则表达式自定义掩码模式。

```python
mask_custom("订单号: ABC123456XYZ", r'[A-Z]{3}\d{6}[A-Z]{3}')
# 输出: 订单号: ***********
```

### detect_and_mask(text, mask_char="*")

自动检测文本中的敏感信息并掩码。

```python
text = "用户邮箱: admin@company.com，手机: 13912345678"
result, types = detect_and_mask(text)
print(result)  # 用户邮箱: ad***@******.com，手机: 139****5678
print(types)   # ['email', 'phone']
```

支持自动检测: 邮箱、手机号、身份证号、银行卡号、IPv4 地址

### batch_mask(data, rules, mask_char="*")

根据规则批量掩码字典数据。

```python
data = {
    "email": "user@example.com",
    "phone": "13812345678",
    "name": "张三",
    "address": "北京市朝阳区xxx"
}

rules = {
    "email": "email",
    "phone": "phone",
    "name": "name",
    "address": "address"
}

result = batch_mask(data, rules)
# {'email': 'us**@*****.com', 'phone': '138****5678', 'name': '张*', 'address': '北京市朝阳区**...'}
```

## 使用场景

### 日志脱敏

```python
import logging
from mask_utils import detect_and_mask

class MaskingHandler(logging.Handler):
    def emit(self, record):
        record.msg, _ = detect_and_mask(str(record.msg))
        return super().emit(record)
```

### API 响应过滤

```python
def sanitize_response(user_data):
    rules = {"email": "email", "phone": "phone", "id_card": "id_card"}
    return batch_mask(user_data, rules)
```

### 数据库查询结果脱敏

```python
def get_user_info(user_id):
    user = db.query_user(user_id)
    return batch_mask(user.__dict__, {
        "email": "email",
        "mobile": "phone",
        "real_name": "name"
    })
```

## 测试

```bash
python -m pytest mask_utils_test.py -v
```

或直接运行:

```bash
python mask_utils_test.py
```

## 许可证

MIT License