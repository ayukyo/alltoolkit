# Crypto Utils


AllToolkit - Python Crypto Utilities
加密工具模块 - 提供哈希、编码、加密等常用功能

@module: crypto_utils
@author: AllToolkit Contributors
@license: MIT
@version: 1.0.0

功能列表:
- 哈希算法: MD5, SHA1, SHA256, SHA512, SHA3_256, SHA3_512, BLAKE2b
- HMAC: HMAC-SHA256, HMAC-SHA512
- 编码: Base64, Base32, Base16, URL-safe Base64
- 加密: XOR 对称加密
- 随机数: 安全随机字符串、密码、UUID
- 验证: 哈希格式验证、Base64验证

使用示例:
    from crypto_utils.mod import CryptoUtils
    
    # 计算哈希
    hash_value = CryptoUtils.sha256_hash("hello world")
    
    # Base64 编解码
    encoded = CryptoUtils.base64_encode("你好世界")
    decoded = CryptoUtils.base64_decode(encoded)
    
    # 生成随机密码
    password = CryptoUtils.random_password(16)


## 功能

### 类

- **CryptoUtils**: 加密工具类 - 提供静态方法进行哈希、编码和加密操作
  方法: md5_hash, sha1_hash, sha256_hash, sha512_hash, sha3_256_hash ... (35 个方法)

### 函数

- **md5_hash(data**) - 计算 MD5 哈希值
- **sha256_hash(data**) - 计算 SHA256 哈希值
- **sha512_hash(data**) - 计算 SHA512 哈希值
- **base64_encode(data**) - Base64 编码
- **base64_decode(data**) - Base64 解码
- **random_string(length, chars**) - 生成安全随机字符串
- **random_password(length**) - 生成安全随机密码
- **uuid_v4(**) - 生成 UUID v4
- **md5_hash(data**) - 计算 MD5 哈希值
- **sha1_hash(data**) - 计算 SHA1 哈希值

... 共 43 个函数

## 使用示例

```python
from mod import md5_hash

# 使用 md5_hash
result = md5_hash()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
