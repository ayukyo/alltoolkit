# Base32 Utils


Base32 工具模块

提供多种 Base32 编码方案的实现：
- RFC 4648 标准 Base32 (A-Z, 2-7)
- Base32Hex (0-9, A-V)
- Crockford's Base32 (0-9, A-H, J-K, M-N, P-T, V-Z，排除 I, L, O, U)

零外部依赖，纯 Python 实现。


## 功能

### 类

- **Base32Encoder**: 标准 Base32 编码器 (RFC 4648)
  方法: encode, decode
- **Base32HexEncoder**: Base32Hex 编码器 (RFC 4648)
  方法: encode, decode
- **CrockfordBase32Encoder**: Crockford's Base32 编码器

特点：
- 排除易混淆字符 (I, L, O, U)
- 可选校验位
- 大小写不敏感
- 允许可选连字符用于分隔

常用于：URL 友好的 ID、产品序列号等
  方法: encode, decode
- **Base32Utils**: Base32 工具集

提供便捷的静态方法访问各种 Base32 编码方案
  方法: encode, decode, encode_string, decode_string, is_valid_base32 ... (11 个方法)

### 函数

- **encode(data, variant**) - Base32 编码便捷函数
- **decode(encoded, variant**) - Base32 解码便捷函数
- **encode_string(text, encoding, variant**) - 字符串编码便捷函数
- **decode_string(encoded, encoding, variant**) - 字符串解码便捷函数
- **generate_id(length**) - 生成随机 ID 便捷函数
- **encode(self, data**) - 将字节数据编码为 Base32 字符串
- **decode(self, encoded**) - 将 Base32 字符串解码为字节数据
- **encode(self, data**) - 将字节数据编码为 Base32Hex 字符串
- **decode(self, encoded**) - 将 Base32Hex 字符串解码为字节数据
- **encode(self, data, checksum**) - 将字节数据编码为 Crockford's Base32 字符串

... 共 22 个函数

## 使用示例

```python
from mod import encode

# 使用 encode
result = encode()
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
