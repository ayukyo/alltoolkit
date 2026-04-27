# Byte Utils


字节操作工具模块 (Byte Utilities)

提供零外部依赖的字节操作功能，包括：
- 字节序转换（大端/小端）
- 字节数组操作（拼接、切片、填充）
- 位操作（设置、清除、翻转、测试）
- 十六进制转换
- 字节模式匹配
- 字节对齐

适用于底层编程、协议实现、数据处理等场景。


## 功能

### 类

- **ByteUtils**: 字节操作工具类
  方法: to_little_endian, to_big_endian, from_little_endian, from_big_endian, swap_endian ... (41 个方法)

### 函数

- **to_little_endian(value, size**) - 便捷函数：转换为小端字节序
- **to_big_endian(value, size**) - 便捷函数：转换为大端字节序
- **from_little_endian(data**) - 便捷函数：从小端字节序解析
- **from_big_endian(data**) - 便捷函数：从大端字节序解析
- **to_hex(data, uppercase, separator**) - 便捷函数：字节串转十六进制
- **from_hex(hex_str**) - 便捷函数：十六进制转字节串
- **xor_bytes(data, key**) - 便捷函数：字节 XOR
- **to_little_endian(value, size**) - 将整数转换为小端字节序
- **to_big_endian(value, size**) - 将整数转换为大端字节序
- **from_little_endian(data**) - 从小端字节序解析整数

... 共 48 个函数

## 使用示例

```python
from mod import to_little_endian

# 使用 to_little_endian
result = to_little_endian()
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
