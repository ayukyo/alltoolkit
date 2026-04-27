# Classical Cipher Utils


Classical Cipher Utilities - 古典密码工具集

提供多种经典加密算法的实现，包括：
- Caesar Cipher (凯撒密码)
- Vigenère Cipher (维吉尼亚密码)
- Atbash Cipher (埃特巴什密码)
- ROT13 (ROT13加密)
- Affine Cipher (仿射密码)
- Playfair Cipher (普莱费尔密码)
- Rail Fence Cipher (栅栏密码)
- Columnar Transposition Cipher (列置换密码)

所有算法均为零外部依赖的纯 Python 实现。


## 功能

### 类

- **CaesarCipher**: 凯撒密码 - 最简单的替换密码

通过将字母表中的每个字母移动固定位数来实现加密。
  方法: encrypt, decrypt, brute_force
- **ROT13**: ROT13 - 凯撒密码的特例

将字母移动13位，加密和解密使用相同操作。
  方法: transform
- **AtbashCipher**: 埃特巴什密码 - 字母表反转替换

将A替换为Z，B替换为Y，以此类推。
  方法: encrypt
- **VigenereCipher**: 维吉尼亚密码 - 多表替换密码

使用关键词生成不同的位移量进行加密。
  方法: encrypt, decrypt
- **AffineCipher**: 仿射密码 - 数学函数替换密码

使用公式 E(x) = (ax + b) mod 26 进行加密。
a 必须与26互质（即 gcd(a, 26) = 1）。
  方法: encrypt, decrypt
- **PlayfairCipher**: 普莱费尔密码 - 双字母替换密码

使用5x5矩阵进行加密，支持I/J合并或分开处理。
  方法: encrypt, decrypt
- **RailFenceCipher**: 栅栏密码 - 换位密码

将明文按"之"字形排列在多行上，然后逐行读取。
  方法: encrypt, decrypt
- **ColumnarTranspositionCipher**: 列置换密码 - 换位密码

将明文按行写入表格，按密钥顺序读取列。
  方法: encrypt, decrypt
- **SimpleSubstitutionCipher**: 简单替换密码 - 单表替换密码

使用自定义字母映射表进行加密。
  方法: encrypt, decrypt
- **PolybiusSquareCipher**: 波利比乌斯方阵密码

使用5x5方阵将字母转换为坐标对。
  方法: encrypt, decrypt

### 函数

- **caesar_encrypt(text, shift**) - 凯撒加密
- **caesar_decrypt(text, shift**) - 凯撒解密
- **rot13(text**) - ROT13变换
- **atbash(text**) - 埃特巴什密码
- **vigenere_encrypt(text, key**) - 维吉尼亚加密
- **vigenere_decrypt(text, key**) - 维吉尼亚解密
- **affine_encrypt(text, a, b**) - 仿射加密
- **affine_decrypt(text, a, b**) - 仿射解密
- **rail_fence_encrypt(text, rails**) - 栅栏加密
- **rail_fence_decrypt(text, rails**) - 栅栏解密

... 共 32 个函数

## 使用示例

```python
from mod import caesar_encrypt

# 使用 caesar_encrypt
result = caesar_encrypt()
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
