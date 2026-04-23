# Base58 编码/解码工具模块

Base58 是一种二进制到文本的编码方式，移除了容易混淆的字符（0、O、I、l），常用于比特币地址、IPFS CID、短链接等场景。

## 功能特性

- **Base58 编码/解码** - 基本的编码和解码功能
- **Base58Check** - 带校验和的编码（比特币地址风格）
- **比特币地址工具** - 生成、解析、验证比特币地址
- **IPFS CID 工具** - CIDv0 和 CIDv1 编码/解码
- **进制转换** - Hex、Base64、整数与 Base58 的互转
- **验证器** - 验证 Base58 字符串有效性

## 快速使用

### 基本编码/解码

```python
from base58_utils import encode, decode

# 编码
encoded = encode(b"Hello World")
print(encoded)  # "2NEpo7TZRRrL"

# 解码
decoded = decode("2NEpo7TZRRrL")
print(decoded)  # b"Hello World"
```

### Base58Check（带校验和）

```python
from base58_utils import encode_check, decode_check

# 编码（自动添加校验和）
encoded = encode_check(b"test data")
print(encoded)

# 解码（自动验证校验和）
decoded = decode_check(encoded)
print(decoded)  # b"test data"
```

### 比特币地址

```python
from base58_utils import BitcoinAddress

btc = BitcoinAddress()

# 生成地址
public_key_hash = bytes.fromhex("010966776008953d5577d...")
address = btc.encode_address(public_key_hash)

# 验证地址
if btc.is_valid_bitcoin_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"):
    print("有效地址")

# 解析地址
version, pk_hash = btc.decode_address(address)
print(f"版本: {version.hex()}, 公钥哈希: {pk_hash.hex()}")
```

### IPFS CID

```python
from base58_utils import IPFSHash

ipfs = IPFSHash()

# 编码 CIDv0
content_hash = bytes.fromhex("a"*64)  # SHA256 哈希
cid_v0 = ipfs.encode_cid(content_hash, version=0)
print(cid_v0)  # 以 "Qm" 开头

# 解码 CID
version, codec, hash = ipfs.decode_cid("Qm...")
print(f"版本: {version}, 编解码器: {codec}")
```

### 进制转换

```python
from base58_utils import Base58Converter

converter = Base58Converter()

# Hex 转 Base58
b58 = converter.from_hex("0x1234abcd")

# Base58 转 Hex
hex_str = converter.to_hex("2NEpo7TZRRrL")

# 整数转 Base58
b58 = converter.from_int(12345)

# Base58 转 Base64
b64 = converter.to_base64(encoded)
```

## API 参考

### 便捷函数

| 函数 | 描述 |
|------|------|
| `encode(data: bytes)` | 编码字节为 Base58 |
| `decode(encoded: str)` | 解码 Base58 为字节 |
| `encode_check(data: bytes)` | 编码为 Base58Check |
| `decode_check(encoded: str)` | 解码 Base58Check |
| `is_valid(encoded: str)` | 验证 Base58 字符串 |

### 类

| 类 | 描述 |
|---|------|
| `Base58Encoder` | Base58 编码器（支持自定义字母表） |
| `Base58Validator` | Base58 验证器 |
| `BitcoinAddress` | 比特币地址工具 |
| `IPFSHash` | IPFS CID 编码工具 |
| `Base58Converter` | 进制转换工具 |

### 预定义字母表

```python
BASE58_ALPHABET   # 比特币风格（默认）
FLICKR_ALPHABET   # Flickr 短 URL 风格
RIPPLE_ALPHABET   # Ripple 风格
```

## 测试

```bash
python Python/base58_utils/base58_utils_test.py
```

测试覆盖：
- 基本编码/解码
- Base58Check 校验和
- 比特币地址生成/验证
- IPFS CID 编码/解码
- 进制转换
- 验证器
- 自定义字母表
- 边界情况（空数据、单字符、极长数据）
- 错误处理

## 相关模块

- `base64_utils` - Base64 编码/解码
- `crypto_utils` - 加密工具
- `hash_utils` - 哈希函数

## License

MIT