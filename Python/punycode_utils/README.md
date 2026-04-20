# Punycode Utilities

零依赖的 Punycode 和国际化域名（IDN）工具库，用于 Unicode 域名与 ASCII 兼容编码（ACE）之间的转换。

## 功能特性

- ✅ 域名编码/解码（Unicode ↔ Punycode）
- ✅ 邮箱地址编码/解码
- ✅ 域名验证
- ✅ IDN 检测
- ✅ 批量操作
- ✅ 域名信息分析
- ✅ 零外部依赖（仅使用 Python 标准库）

## 安装

无需安装外部依赖，直接导入使用：

```python
from punycode_utils.mod import encode_domain, decode_domain
```

## 快速开始

### 域名编码

```python
from punycode_utils.mod import encode_domain

# 中文域名
result = encode_domain("中国.cn")
print(result.encoded)  # xn--fiqs8s.cn

# 日文域名
result = encode_domain("日本.jp")
print(result.encoded)  # xn--wgv71a.jp

# 德文域名
result = encode_domain("münchen.de")
print(result.encoded)  # xn--mnchen-3ya.de

# ASCII 域名（保持不变）
result = encode_domain("example.com")
print(result.encoded)  # example.com
```

### 域名解码

```python
from punycode_utils.mod import decode_domain

result = decode_domain("xn--fiqs8s.cn")
print(result.encoded)  # 中国.cn

result = decode_domain("xn--wgv71a.jp")
print(result.encoded)  # 日本.jp
```

### 邮箱地址处理

```python
from punycode_utils.mod import encode_email, decode_email

# 编码邮箱域名
email = encode_email("用户@中国.cn")
print(email)  # 用户@xn--fiqs8s.cn

# 解码邮箱域名
email = decode_email("user@xn--fiqs8s.cn")
print(email)  # user@中国.cn
```

### 域名验证

```python
from punycode_utils.mod import validate_domain, is_idn, is_punycode

# 验证域名
is_valid, error = validate_domain("中国.cn")
print(is_valid)  # True

is_valid, error = validate_domain("-invalid.com")
print(is_valid)  # False

# 检测 IDN
print(is_idn("中国.cn"))      # True
print(is_idn("example.com"))  # False

# 检测 Punycode
print(is_punycode("xn--fiqs8s.cn"))  # True
print(is_punycode("example.com"))    # False
```

### 批量操作

```python
from punycode_utils.mod import batch_encode, batch_decode

# 批量编码
domains = ["中国.cn", "日本.jp", "example.com"]
encoded = batch_encode(domains)
print(encoded)
# {'中国.cn': 'xn--fiqs8s.cn', '日本.jp': 'xn--wgv71a.jp', 'example.com': 'example.com'}

# 批量解码
punycode_domains = ["xn--fiqs8s.cn", "xn--wgv71a.jp"]
decoded = batch_decode(punycode_domains)
print(decoded)
# {'xn--fiqs8s.cn': '中国.cn', 'xn--wgv71a.jp': '日本.jp'}
```

### 域名信息

```python
from punycode_utils.mod import domain_info

info = domain_info("中国.cn")
print(info['unicode'])      # 中国.cn
print(info['ascii'])        # xn--fiqs8s.cn
print(info['is_idn'])       # True
print(info['is_punycode'])  # True
print(info['tld'])          # cn
print(info['is_valid'])     # True
```

## API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `encode_domain(domain)` | 将 Unicode 域名编码为 Punycode |
| `decode_domain(domain)` | 将 Punycode 域名解码为 Unicode |
| `encode_email(email)` | 编码邮箱地址的域名部分 |
| `decode_email(email)` | 解码邮箱地址的域名部分 |

### 验证函数

| 函数 | 说明 |
|------|------|
| `is_idn(domain)` | 检测域名是否包含 Unicode 字符 |
| `is_punycode(domain)` | 检测域名是否为 Punycode 编码 |
| `validate_domain(domain)` | 验证域名格式，返回 (is_valid, error) |

### 工具函数

| 函数 | 说明 |
|------|------|
| `get_tld(domain)` | 获取顶级域名 |
| `normalize_domain(domain, to_ascii)` | 规范化域名 |
| `batch_encode(domains)` | 批量编码域名 |
| `batch_decode(domains)` | 批量解码域名 |
| `domain_info(domain)` | 获取域名详细信息 |

### 数据类

#### IDNResult

```python
@dataclass
class IDNResult:
    original: str           # 原始输入
    encoded: str            # 编码/解码结果
    is_ascii: bool          # 原始是否为纯 ASCII
    labels: List[Tuple[str, str]]  # 标签对列表
    success: bool           # 操作是否成功
    error: Optional[str]    # 错误信息
```

### 常量

| 常量 | 值 | 说明 |
|------|-----|------|
| `ACE_PREFIX` | `"xn--"` | Punycode 前缀 |
| `MAX_LABEL_LENGTH` | `63` | DNS 标签最大长度 |
| `MAX_DOMAIN_LENGTH` | `253` | 域名最大长度 |

## 运行测试

```bash
python punycode_utils_test.py -v
```

## 示例

参见 `examples/` 目录获取更多使用示例。

## 许可证

MIT License