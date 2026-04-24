# AllToolkit - Python Base85 Utils 🔤

**零依赖 Base85 编码解码工具 - 生产就绪**

---

## 📖 概述

`base85_utils` 提供功能完整的 Base85 编码解码解决方案。Base85 是一种比 Base64 更高效的编码方式，将 4 字节编码为 5 个字符（25% 开销），而 Base64 为 33% 开销。

支持多种变体：
- **RFC 1924** - 标准 Base85，用于 IPv6 地址编码
- **Z85** - ZeroMQ 变体，使用可打印字符子集
- **Ascii85** - Adobe/PostScript/PDF 变体，支持零块缩写
- **btoa** - 传统 btoa 编码

---

## ✨ 特性

- **零依赖** - 纯 Python 实现，无需外部库
- **多变体支持** - RFC 1924、Z85、Ascii85、btoa
- **流式编码** - Base85Iterator 支持大数据流式处理
- **IPv6 支持** - RFC 1924 IPv6 地址编码
- **文件操作** - 直接文件编码解码
- **性能对比** - 与 Base64 效率对比
- **完整测试** - 100+ 测试用例

---

## 🚀 快速开始

### 基础编码解码

```python
from mod import encode, decode

# 编码
encoded = encode(b"Hello, World!")
print(encoded)  # 'Xk&0]Cv8Aqt>'

# 解码
decoded = decode(encoded)
print(decoded)  # b'Hello, World!'
```

### 使用不同变体

```python
from mod import encode, decode

# RFC 1924（默认）
rfc1924 = encode(b"Hello", variant="rfc1924")

# Z85（ZeroMQ 变体）
z85 = encode(b"Hello", variant="z85")
decoded = decode(z85, variant="z85")

# Ascii85（Adobe 变体）
ascii85 = encode(b"Hello", variant="ascii85")
decoded = decode(ascii85, variant="ascii85")

# btoa
btoa = encode(b"Hello", variant="btoa")
decoded = decode(btoa, variant="btoa")
```

### Ascii85 特殊功能

```python
from mod import encode_ascii85, decode_ascii85

# 编码（支持帧定界符）
encoded = encode_ascii85(b"Hello", frame=True)
print(encoded)  # '<~87cURDZ~>'

# 解码（自动处理定界符）
decoded = decode_ascii85("<~87cURDZ~>")
print(decoded)  # b'Hello'

# 零块自动缩写（4 个零字节 -> 'z'）
data = b"\x00\x00\x00\x00Hello"
encoded = encode_ascii85(data)  # 'z87cURDZ'
```

### Z85 编码

```python
from mod import encode_z85, decode_z85

# Z85 使用可打印字符，适合 JSON/XML
encoded = encode_z85(b"Hello, World!")
decoded = decode_z85(encoded)

# 非常适合 ZeroMQ CURVE 密钥
key = bytes(range(32))  # 32 字节密钥
encoded = encode_z85(key)  # 40 字符
```

---

## 📚 API 参考

### 编码函数

#### `encode(data, variant="rfc1924")`

将字节或字符串编码为 Base85。

**参数：**
- `data`: bytes 或 str - 要编码的数据
- `variant`: str - 编码变体（"rfc1924"、"z85"、"ascii85"、"btoa"）

**返回：** str - Base85 编码字符串

#### `decode(data, variant="rfc1924")`

将 Base85 字符串解码为字节。

**参数：**
- `data`: str - Base85 编码字符串
- `variant`: str - 编码变体

**返回：** bytes - 解码后的字节

### 便捷函数

```python
# Ascii85 专用
encode_ascii85(data, frame=False)  # frame=True 添加 <~ 和 ~> 定界符
decode_ascii85(data)               # 自动处理定界符

# Z85 专用
encode_z85(data)
decode_z85(data)
```

### 文件操作

```python
from mod import encode_file, decode_to_file

# 编码文件
encoded = encode_file("/path/to/file")

# 解码到文件
decode_to_file(encoded, "/path/to/output")
```

### 验证函数

```python
from mod import is_valid

# 检查是否为有效 Base85
if is_valid("Xk&0]Cv8Aqt>"):
    print("Valid!")

# 指定变体验证
is_valid("xK0cV", variant="z85")
```

### IPv6 编码（RFC 1924）

```python
from mod import encode_ipv6_to_base85, decode_base85_to_ipv6

# 编码 IPv6 地址
encoded = encode_ipv6_to_base85("2001:db8::1")
print(encoded)  # 20 字符

# 解码回 IPv6
decoded = decode_base85_to_ipv6(encoded)
print(decoded)  # '2001:db8::1'
```

### 流式编码

```python
from mod import Base85Iterator

# 创建流式编码器
iterator = Base85Iterator(variant="rfc1924")

# 处理数据块
result = ""
result += iterator.update(b"Hell")
result += iterator.update(b"o, W")
result += iterator.update(b"orld")
result += iterator.finalize()

# 解码结果
decoded = decode(result)
```

### 工具函数

```python
from mod import (
    get_charset,           # 获取字符集
    estimate_encoded_size, # 估算编码后大小
    estimate_decoded_size, # 估算解码后大小
    compare_with_base64,   # 与 Base64 比较
)

# 获取字符集
charset = get_charset("z85")  # 85 字符字符串

# 估算大小
encoded_size = estimate_encoded_size(100)   # 125 字符
decoded_size = estimate_decoded_size(125)   # 100 字节

# 与 Base64 比较
comparison = compare_with_base64(b"Hello, World!")
# {
#     'original_size': 13,
#     'base85_size': 20,
#     'base64_size': 20,
#     'base85_overhead': 0.538,
#     'base64_overhead': 0.538,
#     'base85_efficiency': 1.0
# }
```

### 编码器类

#### `Base85Encoder`

基础编码器类。

```python
from mod import Base85Encoder, RFC1924_CHARSET

encoder = Base85Encoder(RFC1924_CHARSET, "rfc1924")

encoded = encoder.encode(b"Hello")
decoded = encoder.decode(encoded)

# 带换行的编码
encoded_wrapped = encoder.encode_with_wrap(b"Long data...", wrap=76)
```

#### `Ascii85Encoder`

Ascii85 编码器，支持零块缩写。

```python
from mod import Ascii85Encoder

encoder = Ascii85Encoder()

# 编码（可选帧定界符）
encoded = encoder.encode(b"Hello", frame=True)

# 解码
decoded = encoder.decode(encoded)
```

#### `Z85Encoder`

Z85 编码器。

```python
from mod import Z85Encoder

encoder = Z85Encoder()
encoded = encoder.encode(b"Hello")
decoded = encoder.decode(encoded)
```

---

## 📊 效率对比

| 编码方式 | 4 字节编码为 | 开销 | 适用场景 |
|---------|-------------|------|---------|
| Base64 | 8 字符 | 33% | 通用 |
| Base85 | 5 字符 | 25% | 更高效存储/传输 |
| Hex | 8 字符 | 100% | 可读性 |

### 何时使用 Base85

**推荐使用：**
- 需要更紧凑的编码
- 二进制数据存储
- Git 二进制补丁
- PDF/PostScript 文档
- IPv6 地址编码

**不推荐使用：**
- 需要最大兼容性（Base64 更通用）
- 需要人类可读（Hex 更清晰）
- XML/HTML 嵌入（部分字符需转义）

---

## 🎯 使用场景

### 1. Git 二进制补丁

```python
from mod import encode_ascii85, decode_ascii85

# 读取二进制文件
with open("binary_file", "rb") as f:
    data = f.read()

# 编码为 Git 补丁格式
encoded = encode_ascii85(data, frame=True)
patch = f"literal {len(data)}\n{encoded}\n"
```

### 2. ZeroMQ CURVE 密钥

```python
from mod import encode_z85, decode_z85

# 生成 CURVE 密钥对
public_key = os.urandom(32)
secret_key = os.urandom(32)

# 编码为 Z85（用于配置文件）
public_z85 = encode_z85(public_key)
secret_z85 = encode_z85(secret_key)

print(f"PUBLIC_KEY={public_z85}")
print(f"SECRET_KEY={secret_z85}")
```

### 3. IPv6 紧凑表示

```python
from mod import encode_ipv6_to_base85, decode_base85_to_ipv6

# RFC 1924 IPv6 编码
ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
encoded = encode_ipv6_to_base85(ipv6)
print(f"编码后: {encoded}")  # 20 字符

decoded = decode_base85_to_ipv6(encoded)
print(f"解码后: {decoded}")
```

### 4. 大文件流式编码

```python
from mod import Base85Iterator

def encode_large_file(input_path, output_path):
    iterator = Base85Iterator()
    
    with open(input_path, "rb") as fin, open(output_path, "w") as fout:
        while True:
            chunk = fin.read(4096)  # 4KB 块
            if not chunk:
                break
            encoded = iterator.update(chunk)
            fout.write(encoded)
        
        # 处理剩余数据
        final = iterator.finalize()
        fout.write(final)
```

### 5. 配置文件嵌入

```python
from mod import encode_z85, decode_z85
import json

# 将二进制数据嵌入 JSON 配置
config = {
    "name": "MyApp",
    "api_key": encode_z85(os.urandom(32)),
    "certificate": encode_z85(certificate_bytes)
}

# 保存配置
with open("config.json", "w") as f:
    json.dump(config, f)

# 读取配置
with open("config.json") as f:
    config = json.load(f)
    api_key = decode_z85(config["api_key"])
```

---

## 🔧 高级用法

### 自定义字符集

```python
from mod import Base85Encoder

# 自定义 85 字符字符集
custom_charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"

encoder = Base85Encoder(custom_charset, "custom")
encoded = encoder.encode(b"Hello")
```

### 性能监控

```python
from mod import encode, decode, compare_with_base64
import time

data = bytes(range(256)) * 1000  # 256KB

# 测量编码时间
start = time.time()
for _ in range(100):
    encode(data)
encode_time = time.time() - start

# 测量解码时间
encoded = encode(data)
start = time.time()
for _ in range(100):
    decode(encoded)
decode_time = time.time() - start

print(f"编码时间: {encode_time:.3f}s")
print(f"解码时间: {decode_time:.3f}s")

# 与 Base64 比较
comparison = compare_with_base64(data)
print(f"Base85 效率: {comparison['base85_efficiency']:.2f}x")
```

### 批量处理

```python
from mod import encode, decode

def batch_encode(items: list[bytes]) -> list[str]:
    """批量编码"""
    return [encode(item) for item in items]

def batch_decode(items: list[str]) -> list[bytes]:
    """批量解码"""
    return [decode(item) for item in items]

# 使用
data_list = [b"item1", b"item2", b"item3"]
encoded_list = batch_encode(data_list)
decoded_list = batch_decode(encoded_list)
```

---

## 🧪 运行测试

```bash
cd /path/to/base85_utils
python base85_utils_test.py
```

测试覆盖：
- ✅ Base85Encoder 类
- ✅ Ascii85Encoder 类（含零块缩写）
- ✅ Z85Encoder 类
- ✅ 便捷函数
- ✅ 文件操作
- ✅ IPv6 编码
- ✅ 流式编码
- ✅ 边界情况
- ✅ 性能测试

---

## 📝 示例代码

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基础使用示例
- `variants.py` - 不同变体示例
- `streaming.py` - 流式编码示例
- `ipv6.py` - IPv6 编码示例
- `performance.py` - 性能测试示例

---

## ⚖️ 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit