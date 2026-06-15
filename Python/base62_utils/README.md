# Base62 Utils �缩短

Base62 编码工具，用于生成 URL 安全的短 ID。

## 特性

- ✅ **Base62 编解码** - 数字/字符串转换
- ✅ **UUID → Base62** - UUID 转短字符串
- ✅ **雪花 ID** - Twitter Snowflake 兼容
- ✅ **自定义字符集** - 可选字符集
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from base62_utils import encode, decode, encode_bytes

# 数字编码
encoded = encode(12345)
print(encoded)  # '3V'

# 解码
decoded = decode('3V')
print(decoded)  # 12345

# UUID 编码
import uuid
uid = uuid.uuid4()
short = encode(uid.int)
print(short)  # 随机短字符串
```

## API 参考

| 函数 | 说明 |
|------|------|
| `encode(num)` | 数字转 Base62 |
| `decode(s)` | Base62 转数字 |
| `encode_bytes(data)` | 字节转 Base62 |
| `uuid_to_base62(uuid)` | UUID 编码 |
| `snowflake_to_base62(snowflake_id)` | 雪花 ID 编码 |
