# VCard Utilities - 电子名片工具模块

功能完整的 VCard (电子名片) 处理工具模块，支持 VCard 文件的创建、解析、验证、转换等功能。

## 功能特性

- ✅ **零外部依赖** - 仅使用 Python 标准库
- ✅ **支持多种版本** - VCard 2.1, 3.0, 4.0
- ✅ **完整属性支持** - 姓名、电话、邮箱、地址、组织、照片等
- ✅ **创建与解析** - 双向转换，完整循环测试
- ✅ **验证功能** - 自动验证 VCard 格式和属性
- ✅ **批量处理** - 支持多 VCard 文件的读写
- ✅ **快速创建** - 商务名片和个人名片快捷方式

## 支持的 VCard 属性

| 属性 | 说明 | 示例 |
|------|------|------|
| FN | 全名（必需） | 张三 |
| N | 结构化姓名 | 姓;名;中间名;前缀;后缀 |
| TEL | 电话号码 | 13800138000 |
| EMAIL | 电子邮箱 | test@example.com |
| ADR | 地址 | 街道;扩展;城市;省;邮编;国家 |
| ORG | 组织信息 | 公司名称;部门 |
| TITLE | 职位 | 软件工程师 |
| URL | 网址 | https://example.com |
| BDAY | 生日 | 1990-05-20 |
| NOTE | 备注 | 备注信息 |
| PHOTO | 照片 | BASE64 编码 |
| UID | 唯一标识 | UUID |
| REV | 修订时间 | 时间戳 |

## 快速开始

### 安装

```python
from vcard_utils.mod import create_vcard, save_vcard, parse_vcard
```

### 创建 VCard

```python
# 基本创建
card = create_vcard("张三")

# 详细创建
card = create_vcard(
    full_name="张三",
    organization="科技公司",
    title="软件工程师",
    phones=[
        {"number": "13800138000", "type": "cell"},
        {"number": "010-12345678", "type": "work"}
    ],
    emails=[{"address": "zhangsan@example.com", "type": "work"}],
    birthday="1990-05-20",
    note="重要客户"
)

# 快速商务名片
card = quick_business_card(
    name="李四",
    company="大公司",
    title="经理",
    phone="13900139000",
    email="lisi@bigcorp.com"
)

# 快速个人名片
card = quick_personal_card(
    name="小明",
    phone="13800138000",
    email="xiaoming@example.com",
    birthday="1995-03-15"
)
```

### 保存 VCard

```python
# 保存单个
save_vcard(card, "contact.vcf")

# 保存多个
cards = [create_vcard("张三"), create_vcard("李四")]
save_vcards(cards, "contacts.vcf")

# 转换为字符串
vcard_str = vcard_to_string(card)
print(vcard_str)
```

### 解析 VCard

```python
# 从文件解析
card = parse_vcard("contact.vcf")

# 从字符串解析
vcard_str = """BEGIN:VCARD
VERSION:3.0
FN:张三
TEL:13800138000
END:VCARD"""
card = parse_vcard(vcard_str)

# 解析多个
cards = parse_vcards("contacts.vcf")

# 获取信息
print(card.full_name)
print(card.phones[0].number)
```

### 验证 VCard

```python
# 验证对象
valid, errors = validate_vcard(card)
if not valid:
    print("错误:", errors)

# 验证文件
valid, errors = validate_vcard_file("contact.vcf")
```

### 转换格式

```python
# VCard → 字典
data = vcard_to_dict(card)
print(data['full_name'])

# 字典 → VCard
card = dict_to_vcard({
    'full_name': '张三',
    'phones': [{'number': '13800138000'}]
})

# 获取摘要
summary = get_contact_summary(card)
print(summary)
```

## API 参考

### 创建函数

| 函数 | 说明 |
|------|------|
| `create_vcard()` | 创建完整 VCard |
| `quick_business_card()` | 快速商务名片 |
| `quick_personal_card()` | 快速个人名片 |

### 解析函数

| 函数 | 说明 |
|------|------|
| `parse_vcard(source)` | 解析单个 VCard |
| `parse_vcards(source)` | 解析多个 VCard |

### 保存函数

| 函数 | 说明 |
|------|------|
| `save_vcard(vcard, path)` | 保存单个 VCard |
| `save_vcards(vcards, path)` | 保存多个 VCard |
| `vcard_to_string(vcard)` | 转换为字符串 |

### 验证函数

| 函数 | 说明 |
|------|------|
| `validate_vcard(vcard)` | 验证 VCard 对象 |
| `validate_vcard_file(path)` | 验证 VCard 文件 |

### 转换函数

| 函数 | 说明 |
|------|------|
| `vcard_to_dict(vcard)` | VCard → 字典 |
| `dict_to_vcard(data)` | 字典 → VCard |

### 工具函数

| 函数 | 说明 |
|------|------|
| `get_contact_summary(vcard)` | 获取联系人摘要 |
| `get_supported_versions()` | 支持的版本列表 |
| `get_supported_properties()` | 支持的属性列表 |
| `get_module_info()` | 模块信息 |

## 数据类

### VCard
完整联系人对象，包含所有属性。

### VCardName
结构化姓名：
- `family_name` - 姓
- `given_name` - 名
- `additional_names` - 中间名列表
- `honorific_prefixes` - 前缀列表
- `honorific_suffixes` - 后缀列表

### VCardAddress
地址信息：
- `street` - 街道
- `city` - 城市
- `region` - 省/州
- `postal_code` - 邮政编码
- `country` - 国家

### VCardPhone
电话号码：
- `number` - 号码
- `type` - 类型（cell, work, home, fax）
- `pref` - 偏好级别

### VCardEmail
电子邮箱：
- `address` - 雨箱地址
- `type` - 类型（work, home, internet）

### VCardOrganization
组织信息：
- `name` - 公司名称
- `unit` - 部门
- `title` - 职位
- `role` - 角色

## VCard 格式示例

```
BEGIN:VCARD
VERSION:3.0
FN:张三
N:张;三;;;;
ORG:科技公司;
TITLE:软件工程师
TEL;TYPE=cell:13800138000
TEL;TYPE=work:010-12345678
EMAIL;TYPE=work:zhangsan@example.com
ADR;TYPE=work:;;科技路1号;北京;北京;100000;中国
URL:https://example.com
BDAY:1990-05-20
NOTE:重要客户
UID:550e8400-e29b-41d4-a716-446655440000
REV:2026-05-26T10:00:00Z
END:VCARD
```

## 异常类

| 异常 | 说明 |
|------|------|
| `VCardUtilsError` | 基础异常 |
| `VCardFileNotFoundError` | 文件不存在 |
| `VCardValidationError` | 验证失败 |
| `VCardFormatError` | 格式错误 |

## 测试

```bash
python vcard_utils_test.py
```

## 版本信息

- 版本: 1.0.0
- 作者: AllToolkit
- 许可证: MIT
- 支持版本: VCard 2.1, 3.0, 4.0

## 兼容性

- Python 3.6+
- 无外部依赖
- 跨平台支持