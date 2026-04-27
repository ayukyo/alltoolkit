# Xid Utils


XID Utils - 全局唯一、时间排序的ID生成与解析工具

XID 是一种紧凑的全局唯一标识符：
- 12字节（比UUID的16字节更短）
- 时间排序（可按ID排序）
- URL安全（Base32Hex编码，无填充）
- 分布式友好（包含机器ID和进程ID）

格式（12字节）：
- 4字节：Unix时间戳（秒）
- 3字节：机器ID
- 2字节：进程ID
- 3字节：计数器

零外部依赖，纯Python实现。


## 功能

### 类

- **XIDError**: XID 相关错误
- **XID**: XID 对象 - 表示一个全局唯一、时间排序的标识符

特性：
- 12字节二进制数据
- 20字符Base32Hex字符串表示
- 时间排序
- 包含生成信息（时间、机器、进程、计数器）
  方法: encode, bytes, timestamp, datetime, machine_id ... (7 个方法)
- **XIDGenerator**: XID生成器类 - 支持自定义机器ID和进程ID

适用于需要多租户或手动控制的场景。
  方法: generate

### 函数

- **generate(**) - 生成新的XID
- **from_string(s**) - 从字符串解析XID
- **from_bytes(data**) - 从字节创建XID
- **is_valid(s**) - 验证字符串是否为有效的XID
- **extract_timestamp(xid**) - 从XID提取时间戳
- **extract_datetime(xid**) - 从XID提取datetime对象
- **compare(xid1, xid2**) - 比较两个XID（按时间排序）
- **batch_generate(count**) - 批量生成XID
- **parse_info(xid**) - 解析XID的所有信息
- **min_xid(timestamp**) - 创建指定时间戳的最小XID（计数器=0，机器ID=0，进程ID=0）

... 共 19 个函数

## 使用示例

```python
from mod import generate

# 使用 generate
result = generate()
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
