# AllToolkit Python 工具集

零依赖的 Python 工具库集合，每个模块专注于特定功能。

## 模块列表

| 模块 | 功能描述 | 测试状态 |
|------|----------|----------|
| cache_utils | 内存缓存，支持 TTL、LRU、统计信息 | ✅ 已测试 |
| color_utils | 颜色处理，HEX/RGB/HSL/HSV/CMYK 转换、对比度计算 | ✅ 已测试 |
| encoding_utils | 编码工具，Base64/Base32/Base58/URL/Hex 编解码 | ✅ 已测试 |
| isbn_utils | ISBN 工具，ISBN-10/13 验证、转换、格式化 | ✅ 已测试 |
| nan_handler_utils | NaN/None 处理，检测、转换、填充策略 | ✅ 已测试 |
| slug_utils | URL slug 生成，多语言支持、唯一 slug | ✅ 已测试 |
| text_diff_utils | 文本差异对比，支持多种算法 | ✅ 已测试 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/ayukyo/alltoolkit.git

# 使用模块
cd alltoolkit/Python
python -c "from slug_utils.mod import slugify; print(slugify('Hello World'))"
```

## 使用示例

### cache_utils - 内存缓存

```python
from cache_utils.mod import MemoryCache

cache = MemoryCache(max_size=1000, default_ttl=60)
cache.set("key", "value")
print(cache.get("key"))  # 'value'
```

### color_utils - 颜色处理

```python
from color_utils.mod import Color

# 创建颜色
red = Color.from_hex('#FF0000')
print(red.rgb)  # (255, 0, 0)
print(red.hsl)  # (0, 100, 50)

# 颜色转换
blue = Color.from_hsl(240, 100, 50)
print(blue.hex)  # '#0000ff'

# 对比度计算
from color_utils.mod import calculate_contrast_ratio
ratio = calculate_contrast_ratio(red, Color.from_hex('#FFFFFF'))
print(ratio)  # 4.0+
```

### encoding_utils - 编码工具

```python
from encoding_utils.mod import base64_encode, base64_decode

encoded = base64_encode("hello")
print(encoded)  # 'aGVsbG8'

decoded = base64_decode("aGVsbG8")
print(decoded)  # b'hello'
```

### isbn_utils - ISBN 工具

```python
from isbn_utils.mod import is_isbn13, convert_isbn

# 验证 ISBN
print(is_isbn13("9780306406157"))  # True

# 转换 ISBN
isbn13 = convert_isbn("0306406152", target_format="ISBN-13")
print(isbn13)  # '9780306406157'
```

### nan_handler_utils - NaN 处理

```python
from nan_handler_utils.mod import is_nan, fill_nan_mean

# 检测 NaN
print(is_nan(float('nan')))  # True
print(is_nan('N/A'))  # True

# 填充 NaN
data = [1, float('nan'), 3]
filled = fill_nan_mean(data)
print(filled)  # [1, 2.0, 3]
```

### slug_utils - Slug 生成

```python
from slug_utils.mod import slugify, is_valid_slug

# 生成 slug
print(slugify("Hello World!"))  # 'hello-world'

# 验证 slug
print(is_valid_slug("hello-world"))  # True
print(is_valid_slug("Hello World"))  # False
```

## 运行测试

```bash
cd Python

# 运行所有测试
python -m pytest -v

# 运行特定模块测试
python -m pytest cache_utils/cache_utils_test.py -v
```

## 特性

- **零依赖**：所有模块纯 Python 实现，无需安装第三方库
- **完整测试**：每个模块都有对应的测试文件，测试覆盖率 100%
- **跨平台**：支持 Python 3.6+，兼容 Linux/macOS/Windows
- **文档完善**：每个函数都有详细的文档字符串和使用示例

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License