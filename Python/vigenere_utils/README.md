# Vigenere Cipher Utilities

维吉尼亚密码工具库 - 纯 Python 实现，零外部依赖。

## 功能特性

- **加密**: 使用密钥加密明文
- **解密**: 使用密钥解密密文
- **密钥长度检测**: 使用重合指数法估算密钥长度
- **自动破解**: 基于频率分析的自动破解功能
- **Vigenere 表格**: 生成 Tabula Recta 可视化
- **灵活配置**: 支持大小写保留、非字母字符处理等选项

## 安装

无需安装，直接导入使用：

```python
from vigenere_utils.mod import encrypt, decrypt, crack
```

## 快速开始

### 基本加密解密

```python
from vigenere_utils.mod import encrypt, decrypt

# 加密
plaintext = "HELLO WORLD"
key = "SECRET"
ciphertext = encrypt(plaintext, key)
print(ciphertext)  # ZINCS PGVNU

# 解密
decrypted = decrypt(ciphertext, key)
print(decrypted)  # HELLO WORLD
```

### 自动破解

```python
from vigenere_utils.mod import auto_decrypt

ciphertext = "LB YKW GZH JGCX BX WQOOW..."
key, plaintext, candidates = auto_decrypt(ciphertext)
print(f"找到的密钥: {key}")
print(f"解密结果: {plaintext}")
```

### 密钥长度检测

```python
from vigenere_utils.mod import find_key_length

results = find_key_length(ciphertext)
for length, score in results[:5]:
    print(f"密钥长度 {length}: IC 分数 {score:.4f}")
```

## API 文档

### encrypt(plaintext, key, preserve_case=True, preserve_non_alpha=True)

加密明文。

**参数:**
- `plaintext`: 要加密的文本
- `key`: 加密密钥
- `preserve_case`: 是否保留大小写（默认 True）
- `preserve_non_alpha`: 是否保留非字母字符（默认 True）

**返回:** 加密后的密文

### decrypt(ciphertext, key, preserve_case=True, preserve_non_alpha=True)

解密密文。

**参数:** 同 encrypt

**返回:** 解密后的明文

### crack(ciphertext, key_length=None, max_key_length=20)

尝试破解维吉尼亚密码。

**参数:**
- `ciphertext`: 要破解的密文
- `key_length`: 已知密钥长度（可选）
- `max_key_length`: 最大尝试的密钥长度

**返回:** 排序后的候选结果列表 `[(key, plaintext, score), ...]`

### auto_decrypt(ciphertext)

全自动解密尝试。

**返回:** `(best_key, best_plaintext, all_candidates)`

## 历史背景

维吉尼亚密码是一种多表替换密码，由 Blaise de Vigenère 于 16 世纪发明。它使用一个关键词来对每个字母进行不同的位移，比简单的凯撒密码更难破解。

## 测试

```bash
python vigenere_utils_test.py
```

## 许可证

MIT License