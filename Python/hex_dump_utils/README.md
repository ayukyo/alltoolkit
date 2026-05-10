# hex_dump_utils -十六进制转储工具模块

二进制数据可视化工具，支持多种十六进制转储格式。零外部依赖，纯 Python 实现。

## 功能列表

| 功能 | 说明 |
|------|------|
| 经典 hexdump 格式 | Unix hexdump 风格 |
| xxd 兼容输出 | Vim xxd 风格 |
| 规范 hex+ASCII 显示 |十六进制 + ASCII 对照 |
| 彩色输出支持 | ANSI 颜色高亮 |
| 二进制补丁生成 | 修改建议生成 |
| 偏移量标注 | 自定义偏移显示 |
| 可定制分组格式 | 自定义字节分组 |

## 快速使用

```python
from hex_dump_utils.mod import (
    hex_dump,
    xxd_dump,
    hex_dump_to_file,
    parse_hex_dump,
    compare_hex_dumps,
    binary_patch
)

# 基本 hex dump
data = b'Hello, World!\x00\xff\xfe'
output = hex_dump(data)
print(output)
# 00000000  48 65 6c 6c 6f 2c 20 57  6f 72 6c 64 21 00 ff fe  |Hello, World!...|

# xxd 风格
output = xxd_dump(data)

# 彩色输出
output = hex_dump(data, colorize=True)

# 自定义格式
output = hex_dump(
    data,
    width=8,           # 每行8字节
    group_size=4,      # 4字节一组
    show_ascii=True,   # 显示ASCII
    uppercase=True     # 大写十六进制
)

# 解析 hex dump
parsed = parse_hex_dump(output)
# 返回原始字节

# 比较两个 dump
diff = compare_hex_dumps(data1, data2)
```

## 输出格式说明

### 经典 Hexdump

```
00000000  48 65 6c 6c 6f 2c 20 57  6f 72 6c 64 21 00 ff fe  |Hello, World!...|
00000010  ab cd ef...
```

- 偏移量（8位十六进制）
-十六进制字节（分组显示）
- ASCII 对照（可打印字符显示，不可打印用`.`）

### xxd 风格

```
00000000: 4865 6c6c 6f2c 2057 6f72 6c64 2100 fffe  Hello, World!...
```

- 偏移量带冒号
- 2字节分组
- 空格分隔

## 详细示例

### 彩色输出

```python
from hex_dump_utils.mod import hex_dump

data = b'\x00\x01Hello\xFF\xFE'
output = hex_dump(data, colorize=True)
# 空字节: 灰色
# 可打印字符: 绿色
# 不可打印字节: 红色
```

### 自定义宽度

```python
#窄格式（8字节/行）
output = hex_dump(data, width=8)

#宽格式（32字节/行）
output = hex_dump(data, width=32)
```

### 二进制补丁

```python
from hex_dump_utils.mod import binary_patch

# 生成补丁
original = b'Hello, World!'
modified = b'Hello, Python!'
patch = binary_patch(original, modified)

# 应用补丁
result = apply_patch(original, patch)
```

### 文件转储

```python
from hex_dump_utils.mod import hex_dump_file

# 直接转储文件
output = hex_dump_file('binary.dat', max_bytes=1024)
```

## API 参考

### hex_dump

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `data` | bytes | 必需 | 二进制数据 |
| `offset` | int | 0 | 起始偏移 |
| `length` | int | None | 最大字节数 |
| `width` | int | 16 | 每行字节数 |
| `group_size` | int | 2 | 字节分组大小 |
| `show_ascii` | bool | True | 显示ASCII |
| `show_offset` | bool | True | 显示偏移 |
| `offset_base` | int | 16 | 偏移进制 |
| `uppercase` | bool | False | 大写十六进制 |
| `colorize` | bool | False | 彩色输出 |

### 其他函数

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `xxd_dump(data)` | bytes | str | xxd风格输出 |
| `parse_hex_dump(text)` | str | bytes | 解析hex dump |
| `compare_hex_dumps(d1, d2)` | bytes, bytes | Dict | 比较差异 |
| `binary_patch(orig, mod)` | bytes, bytes | Dict | 生成补丁 |
| `hex_dump_file(path)` | str | str | 文件转储 |

## 测试

运行测试：

```bash
python hex_dump_utils/hex_dump_utils_test.py
```

---

**最后更新**: 2026-05-11