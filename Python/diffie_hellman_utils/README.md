# Diffie-Hellman 密钥交换工具

## 模块信息

- **模块名称**: `diffie_hellman_utils`
- **语言**: Python 3
- **依赖**: 仅使用 Python 标准库（无外部依赖）

## 功能列表

### 核心功能
- **密钥交换**: 经典 Diffie-Hellman 协议完整实现
- **安全参数**: 预定义 RFC 3526 安全素数（256/1024/2048 位）
- **密钥派生**: HKDF 密钥派生函数支持
- **公钥导出**: 十六进制格式公钥导入导出
- **安全清除**: 敏感数据内存清除

### 便捷功能
- `create_dh_pair()`: 一键创建密钥对
- `perform_key_exchange()`: 执行密钥交换
- `verify_key_exchange()`: 验证交换结果

### 简化 ECDH
- `ECDHKey`: 简化椭圆曲线实现（仅演示用途）

## 使用示例

### 基本密钥交换

```python
from diffie_hellman_utils.mod import DiffieHellman

# Alice 创建密钥对
alice = DiffieHellman(key_bits=2048)
alice_private = alice.generate_private_key()
alice_public = alice.generate_public_key()

# Bob 创建密钥对
bob = DiffieHellman(key_bits=2048)
bob_private = bob.generate_private_key()
bob_public = bob.generate_public_key()

# 交换公钥并计算共享密钥
alice_shared = alice.compute_shared_key(bob_public)
bob_shared = bob.compute_shared_key(alice_public)

# 验证双方共享密钥相同
assert alice_shared == bob_shared
```

### 密钥派生

```python
from diffie_hellman_utils.mod import DiffieHellman

dh = DiffieHellman(key_bits=2048)
dh.generate_private_key()
dh.generate_public_key()

# 计算共享密钥后派生加密密钥
shared_key = dh.compute_shared_key(other_public)
derived_key = dh.derive_key(key_length=32)  # 256-bit AES 密钥

print(f"AES 密钥: {derived_key.hex()}")
```

### 便捷函数

```python
from diffie_hellman_utils.mod import create_dh_pair, perform_key_exchange

# 快速创建密钥对
alice, alice_priv, alice_pub = create_dh_pair(key_bits=2048)
bob, bob_priv, bob_pub = create_dh_pair(key_bits=2048)

# 执行密钥交换
alice_shared, bob_shared = perform_key_exchange(alice, bob)
assert alice_shared == bob_shared
```

### 公钥导入导出

```python
from diffie_hellman_utils.mod import DiffieHellman

dh = DiffieHellman(key_bits=2048)
dh.generate_private_key()
dh.generate_public_key()

# 导出公钥为十六进制字符串
public_hex = dh.export_public_key()
print(f"公钥: {public_hex}")

# 导入公钥
other_dh = DiffieHellman(key_bits=2048)
imported_public = other_dh.import_public_key(public_hex)
```

## API 参考

### DiffieHellman 类

#### 构造函数

```python
DiffieHellman(prime=None, generator=None, key_bits=2048)
```

- `prime`: 自定义素数（可选）
- `generator`: 自定义生成元（可选）
- `key_bits`: 密钥位数，可选 256/1024/2048

#### 方法

| 方法 | 描述 |
|------|------|
| `generate_private_key()` | 生成私钥 |
| `generate_public_key(private_key=None)` | 生成公钥 |
| `compute_shared_key(other_public_key)` | 计算共享密钥 |
| `derive_key(key_length=32, ...)` | 派生加密密钥 |
| `export_public_key()` | 导出公钥为十六进制 |
| `import_public_key(hex_key)` | 导入公钥 |
| `clear_sensitive_data()` | 清除敏感数据 |
| `verify_key_exchange(a, b)` | 验证密钥交换（静态方法） |

### 便捷函数

```python
create_dh_pair(key_bits=2048) -> Tuple[DiffieHellman, int, int]
perform_key_exchange(alice_dh, bob_dh) -> Tuple[int, int]
```

## 安全说明

1. **生产环境**: 建议使用 2048 位参数
2. **256 位参数**: 仅用于演示和测试，不安全！
3. **私钥保护**: 私钥绝不应传输或存储
4. **敏感数据**: 使用后调用 `clear_sensitive_data()` 清除

## 测试

```bash
python test.py
```

## 许可证

MIT License