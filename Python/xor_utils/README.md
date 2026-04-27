# XOR Utils - XOR（异或）操作工具模块

提供 XOR 加密、解密、校验和位操作功能。零外部依赖，仅使用 Python 标准库。

## 功能概览

| 功能模块 | 描述 |
|---------|------|
| 基础 XOR | 单字节、多字节、滚动密钥、链式 XOR |
| 校验和 | XOR 校验和计算与验证 |
| 密码分析 | 密钥推测、密钥长度猜测、破译 |
| 位操作 | 位翻转、交换、反转、计数、Hamming 距离 |
| 编码解码 | 十六进制、字符串 XOR 编码 |
| 模式检测 | 重复模式检测、碰撞检测 |
| 批量操作 | 批量 XOR、密钥流生成 |
| 加密类 | XORCipher、SingleByteXORCipher |

## 安装使用

```python
from xor_utils import (
    xor_byte, xor_bytes,
    xor_checksum, verify_xor_checksum,
    guess_single_byte_key, break_repeating_key_xor,
    XORCipher, SingleByteXORCipher
)

# 单字节 XOR
encrypted = xor_byte(b'Hello', 0x55)
decrypted = xor_byte(encrypted, 0x55)

# 多字节 XOR
encrypted = xor_bytes(b'Hello World', b'KEY')
decrypted = xor_bytes(encrypted, b'KEY')

# XOR 校验和
checksum = xor_checksum(b'Hello')
```

## 详细功能

### 基础 XOR 操作

#### 单字节 XOR

```python
# 单字节密钥 XOR
encrypted = xor_byte(b'Hello World', 0x55)
decrypted = xor_byte(encrypted, 0x55)  # XOR 是对称的
```

#### 多字节 XOR（重复密钥）

```python
# 多字节密钥，自动重复
encrypted = xor_bytes(b'Hello World', b'KEY')
# 密钥 'KEYKEYKEYKEY' 重复应用到数据
```

#### 滚动密钥 XOR

```python
# 每个字节使用不同的密钥：key[i] = (seed + i) & 0xFF
encrypted = xor_rolling_key(b'Hello', seed=42)
```

#### 链式 XOR

```python
# 多个密钥依次 XOR
result = xor_chain(b'Hello', [0x55, 0xAA, 0xFF])
```

### XOR 校验和

```python
# 计算校验和
checksum = xor_checksum(b'Hello')  # 22

# 分块校验和
checksums = xor_checksum_blocks(b'HelloWorld', 5)  # [22, 87]

# 验证校验和
is_valid = verify_xor_checksum(b'Hello', 22)  # True
```

### 密码分析

#### 单字节密钥推测

```python
# 基于频率分析推测密钥
ciphertext = xor_byte(b'Hello World Hello', 0x55)
guesses = guess_single_byte_key(ciphertext)
# 返回 [(可能的密钥, 置信度), ...]

# 带已知明文的推测
guesses = guess_single_byte_key(ciphertext, known_plaintext=b'Hello')
```

#### 密钥长度推测

```python
# 使用 Hamming 距离方法
ciphertext = xor_bytes(b'Hello World Hello World', b'KEY')
key_lengths = guess_key_length(ciphertext)
# 返回 [(可能的长度, 得分), ...]
```

#### 破译重复密钥 XOR

```python
# 自动破译
key, plaintext = break_repeating_key_xor(ciphertext)
# 或指定密钥长度
key, plaintext = break_repeating_key_xor(ciphertext, key_length=3)
```

### 位操作

```python
# 位翻转
result = flip_bits(b'\x00', [0, 1, 2])  # b'\x07'

# 位交换
result = swap_bits(b'\x01', 0, 7)  # b'\x80'

# 位反转
result = reverse_bits(b'\x01')  # b'\x80'
result = reverse_bits(b'\xF0')  # b'\x0F'

# 位计数
count = count_bits(b'\xFF')  # 8

# Hamming 距离
distance = bit_diff(b'Hello', b'Hallo')  # 2
```

### 编码/解码

```python
# 十六进制编码
hex_str = xor_encode_hex(b'Hello', b'K')  # '1d34393936'
data = xor_decode_hex('1d34393936', b'K')  # b'Hello'

# 字符串编码
hex_str = xor_encode_string('Hello', 'KEY')
text = xor_decode_string('0b051e4b05', 'KEY')  # 'Hello'
```

### 模式检测

```python
# 检测重复模式
patterns = detect_xor_pattern(ciphertext, min_pattern_len=3)

# 找出碰撞位置
collisions = find_xor_collisions(b'Hello', b'Hallo')  # [0]
```

### 批量操作

```python
# 批量 XOR
datas = [b'Hello', b'World']
results = xor_all_with_key(datas, b'K')

# 配对 XOR
results = xor_pairs([b'Hello', b'Test'], [b'KEYKE', b'ABC'])

# 密钥流生成
key_stream = generate_xor_key_stream(seed=0x55, length=32)
```

### 文件加密

```python
# 加密文件内容（带校验和）
encrypted = xor_encrypt_file_content(b'Hello World', b'KEY', add_checksum=True)

# 解密并验证
content, is_valid = xor_decrypt_file_content(encrypted, b'KEY', verify_checksum=True)
```

### 加密类

#### XORCipher

```python
cipher = XORCipher(b'KEY')

# 加密解密
encrypted = cipher.encrypt(b'Hello World')
decrypted = cipher.decrypt(encrypted)

# 流式加密
def data_stream():
    yield b'Hello'
    yield b'World'

for chunk in cipher.encrypt_stream(data_stream()):
    print(chunk)
```

#### SingleByteXORCipher

```python
cipher = SingleByteXORCipher(0x55)

# 加密解密
encrypted = cipher.encrypt(b'Hello')
decrypted = cipher.decrypt(encrypted)

# 暴力破解
ciphertext = xor_byte(b'Hello World Hello', 0x55)
results = cipher.brute_force_decrypt(ciphertext, top_n=10)
# 返回 [(密钥, 解密结果, 置信度), ...]
```

## 数据类

### XORResult

```python
result = create_xor_result(b'Hello', b'K')

# 属性
result.data      # XOR 后的数据
result.key       # 密钥
result.checksum  # 校验和

# 方法
result.to_hex()          # 十六进制字符串
result.to_base64()       # Base64 字符串
result.to_string()       # UTF-8 字符串（失败时返回十六进制）
```

## 测试

```bash
python test_mod.py
```

测试覆盖:
- 基础 XOR 操作（单字节、多字节、滚动、链式）
- XOR 校验和
- 密码分析（密钥推测、密钥长度猜测、破译）
- 位操作
- 编码/解码
- 模式检测
- 批量操作
- 文件加密
- 加密类
- 边界值处理

## 应用场景

- 简单数据加密
- 数据校验和验证
- 密码学教学
- CTF 密码分析挑战
- 数据混淆
- 嵌入式系统通信
- 文件完整性验证

## 算法说明

### XOR 加密原理

XOR 加密是一种对称加密方式：
- 加密：plaintext XOR key = ciphertext
- 解密：ciphertext XOR key = plaintext

特点：
- 对称性：同一密钥加密和解密
- 简单高效：位操作，计算快速
- 易于破解：不适合强加密需求

### 密码分析方法

#### 单字节密钥破解

使用频率分析：
- 分析密文字节频率
- 对照英文字符频率（e、t、a、o 等）
- 计算每个密钥的得分
- 高得分密钥为候选

#### 重复密钥破解

使用 Hamming 距离法：
- 计算不同密钥长度下的平均 Hamming 距离
- 距离最小表示密钥长度正确
- 对每列进行单字节破解

## 许可证

MIT License - 详见项目 LICENSE 文件

---

**作者**: AllToolkit  
**日期**: 2026-04-27