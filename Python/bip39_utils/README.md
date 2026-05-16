# BIP39 Utils - 助记词工具

BIP39 助记词生成、验证、种子派生工具。完全遵循 [BIP39 规范](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)。

## 功能特性

- **助记词生成**: 支持 12/15/18/21/24 词
- **助记词验证**: 校验和验证、词表检查
- **种子派生**: PBKDF2-HMAC-SHA512，2048 次迭代
- **主密钥派生**: HMAC-SHA512，符合 BIP32 标准
- **熵恢复**: 从助记词恢复原始熵

## 快速开始

```python
from bip39_utils.mod import (
    generate_mnemonic,
    validate_mnemonic,
    mnemonic_to_seed,
    BIP39Mnemonic,
)

# 生成 12 词助记词
mnemonic = generate_mnemonic(12)
print(f"助记词: {mnemonic}")

# 验证助记词
is_valid = validate_mnemonic(mnemonic)
print(f"有效: {is_valid}")

# 生成种子
seed = mnemonic_to_seed(mnemonic, passphrase="")
print(f"种子: {seed.hex()}")
```

## 核心类

### BIP39Mnemonic

```python
from bip39_utils.mod import BIP39Mnemonic, Language

bip = BIP39Mnemonic(language=Language.ENGLISH)

# 生成助记词
result = bip.generate(word_count=24)
print(f"助记词: {result.mnemonic}")
print(f"熵: {result.entropy_hex}")

# 验证助记词
validation = bip.validate(result.mnemonic)
print(f"有效: {validation.is_valid}")
print(f"校验和正确: {validation.checksum_valid}")

# 生成种子
seed_result = bip.to_seed(result.mnemonic, passphrase="my_password")
print(f"种子: {seed_result.seed_hex}")
print(f"主密钥: {seed_result.master_key_hex}")
print(f"链码: {seed_result.chain_code_hex}")

# 恢复熵
entropy = bip.to_entropy(result.mnemonic)
print(f"恢复的熵: {entropy.hex()}")
```

## 助记词长度对照

| 词数 | 熵位数 | 校验和位数 |
|------|--------|------------|
| 12 | 128 | 4 |
| 15 | 160 | 5 |
| 18 | 192 | 6 |
| 21 | 224 | 7 |
| 24 | 256 | 8 |

## 安全注意事项

1. **安全存储**: 助记词是私钥的唯一备份，请安全存储
2. **密码短语**: 添加密码短语可增加安全性
3. **离线生成**: 建议在离线环境生成助记词
4. **校验验证**: 使用前务必验证助记词有效性

## 技术细节

### 种子生成算法

```
seed = PBKDF2-HMAC-SHA512(
    password = mnemonic_normalized (NFKD),
    salt = "mnemonic" + passphrase,
    iterations = 2048,
    dklen = 64
)
```

### 主密钥派生

```
I = HMAC-SHA512(key="Bitcoin seed", data=seed)
master_key = I[0:32]  # 左 32 字节
chain_code = I[32:64] # 右 32 字节
```

## 测试覆盖

- 助记词生成（各长度）
- 校验和验证
- 种子派生
- 熵恢复
- 无效输入处理

## 许可证

MIT License