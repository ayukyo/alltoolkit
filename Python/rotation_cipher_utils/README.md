# Rotation Cipher Utils


AllToolkit - Rotation Cipher Utilities Module
=============================================
A comprehensive rotation cipher utility module for Python with zero external dependencies.

Features:
    - Caesar cipher (arbitrary shift)
    - ROT13 (rotate by 13)
    - ROT47 (ASCII printable rotation)
    - ROT5 (digits rotation)
    - Custom alphabet rotation
    - File encryption/decryption
    - Brute force attack support
    - Frequency analysis helpers

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **CipherResult**: Container for cipher operation results
- **BruteForceResult**: Container for brute force attack results

### 函数

- **caesar_cipher(text, shift, alphabet**) - Apply Caesar cipher rotation to text.
- **rot13(text**) - Apply ROT13 cipher (rotate by 13 positions).
- **rot5(text**) - Apply ROT5 cipher (rotate digits by 5 positions).
- **rot47(text**) - Apply ROT47 cipher (rotate ASCII printable characters by 47).
- **rot18(text**) - Apply ROT18 cipher (combination of ROT13 + ROT5).
- **vigenere_cipher(text, key, decrypt**) - Apply Vigenere cipher (polyalphabetic substitution).
- **affine_cipher(text, a, b**, ...) - Apply Affine cipher (E(x) = (ax + b) mod 26).
- **atbash_cipher(text**) - Apply Atbash cipher (A↔Z, B↔Y, etc.).
- **brute_force_caesar(ciphertext, language, top_n**) - Brute force attack on Caesar cipher.
- **frequency_analysis(text**) - Perform frequency analysis on text.

... 共 20 个函数

## 使用示例

```python
from mod import caesar_cipher

# 使用 caesar_cipher
result = caesar_cipher()
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
