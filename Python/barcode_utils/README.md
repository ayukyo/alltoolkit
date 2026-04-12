# Barcode Utils 📊

**Python 条形码生成工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`barcode_utils` 是一个全面的 Python 条形码生成工具模块，支持多种主流条形码格式。所有条形码均以 SVG 格式生成，可无限缩放且保持高质量。所有实现均使用 Python 标准库，零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **多种格式** - Code 39、Code 128、EAN-13、EAN-8、UPC-A、ITF、矩阵码
- **SVG 输出** - 可缩放矢量图形，适合打印和屏幕显示
- **可定制** - 完全可配置的颜色、尺寸、边距等参数
- **自动校验** - EAN/UPC 自动计算校验位
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 100+ 测试用例覆盖所有功能

### 📋 支持的格式

| 格式 | 描述 | 字符集 | 典型用途 |
|------|------|--------|----------|
| Code 39 | 字母数字条形码 | 0-9, A-Z, 特殊字符 | 工业、军事、医疗 |
| Code 128 | 高密度条形码 | 全 ASCII | 物流、包装、运输 |
| EAN-13 | 13 位欧洲商品码 | 0-9 | 零售商品（国际） |
| EAN-8 | 8 位紧凑商品码 | 0-9 | 小型商品包装 |
| UPC-A | 12 位通用产品码 | 0-9 | 零售商品（北美） |
| ITF | 交叉 25 码 | 0-9 | 瓦楞纸箱、仓储 |
| Matrix | 矩阵码（类 QR） | 任意 | 演示、简单编码 |

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/barcode_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

```python
from mod import generate_code128, generate_ean13, save_barcode

# 生成 Code 128 条形码
result = generate_code128("Hello World")
print(result.svg)  # SVG 内容

# 保存到文件
save_barcode(result, "barcode.svg")

# 生成 EAN-13 商品码
result = generate_ean13("590123412345")
save_barcode(result, "product_barcode.svg")

# 使用通用生成函数
result = generate_barcode("ABC123", format="code39")
```

---

## 📚 API 参考

### 配置类

#### `BarcodeConfig`

条形码外观配置。

```python
from mod import BarcodeConfig

config = BarcodeConfig(
    width=2,              # 模块宽度（像素）
    height=100,           # 条形码高度（像素）
    margin=10,            # 边距（像素）
    show_text=True,       # 是否显示文本标签
    text_size=14,         # 文本大小
    text_margin=5,        # 文本与条形码间距
    foreground="#000000", # 前景色（条形码颜色）
    background="#FFFFFF", # 背景色
    scale=1.0             # 整体缩放比例
)
```

### 结果类

#### `BarcodeResult`

条形码生成结果。

```python
@dataclass
class BarcodeResult:
    svg: str      # SVG 内容
    width: int    # 总宽度（像素）
    height: int   # 总高度（像素）
    data: str     # 编码的数据
    format: str   # 条形码格式
```

---

### 条形码生成函数

#### `generate_code39(data, config=None)`

生成 Code 39 条形码。

```python
result = generate_code39("ABC123")
# 支持：0-9, A-Z, 空格, -, ., $, /, +, %
# 自动添加起止符 *
```

#### `generate_code128(data, config=None)`

生成 Code 128 条形码（自动选择最佳字符集）。

```python
result = generate_code128("Hello World 123")
# 支持全 ASCII 字符集
# 高密度，适合各种应用
```

#### `generate_ean13(code, config=None)`

生成 EAN-13 条形码。

```python
# 12 位数字（自动计算校验位）
result = generate_ean13("590123412345")

# 或 13 位（忽略最后一位校验位）
result = generate_ean13("5901234123457")
```

#### `generate_ean8(code, config=None)`

生成 EAN-8 条形码（小型商品）。

```python
result = generate_ean8("1234567")  # 7 位数字
```

#### `generate_upca(code, config=None)`

生成 UPC-A 条形码（北美商品）。

```python
result = generate_upca("01234567890")  # 11 位数字
```

#### `generate_itf(data, config=None)`

生成 ITF（交叉 25 码）条形码。

```python
result = generate_itf("12345678")
# 仅支持数字
# 奇数位自动补零
```

#### `generate_matrix(data, size=21, config=None)`

生成矩阵码（类 QR 码，简化版）。

```python
result = generate_matrix("Hello World", size=21)
# 适用于演示和简单编码
# 生产环境建议使用专业 QR 码库
```

---

### 通用生成函数

#### `generate_barcode(data, format='code128', config=None, **kwargs)`

通用条形码生成函数。

```python
# Code 39
result = generate_barcode("ABC123", format="code39")

# EAN-13
result = generate_barcode("590123412345", format="ean13")

# 带自定义配置
config = BarcodeConfig(width=3, height=150)
result = generate_barcode("TEST", format="code128", config=config)
```

---

### 工具函数

#### `get_supported_formats()`

获取支持的条形码格式列表。

```python
formats = get_supported_formats()
# ['code39', 'code128', 'ean13', 'ean8', 'upca', 'itf', 'matrix']
```

#### `save_barcode(result, filepath)`

保存条形码 SVG 到文件。

```python
result = generate_code128("Hello")
save_barcode(result, "hello.svg")

# 验证文件
with open("hello.svg", "r") as f:
    content = f.read()
```

---

## 📝 示例

### 基础示例

```python
from mod import generate_code128, save_barcode

# 最简单的用法
result = generate_code128("PRODUCT-001")
save_barcode(result, "product.svg")
```

### 自定义样式

```python
from mod import generate_code128, BarcodeConfig, save_barcode

# 红色条形码，白色背景
config = BarcodeConfig(
    width=3,
    height=120,
    foreground="#CC0000",
    background="#FFFFFF",
    show_text=True,
    text_size=16
)

result = generate_code128("SPECIAL-ITEM", config)
save_barcode(result, "red_barcode.svg")
```

### 批量生成

```python
from mod import generate_ean13, save_barcode

# 批量生成商品条形码
products = [
    ("590123412345", "product_001.svg"),
    ("590123412346", "product_002.svg"),
    ("590123412347", "product_003.svg"),
]

for code, filename in products:
    result = generate_ean13(code)
    save_barcode(result, filename)
    print(f"Generated: {filename}")
```

### 打印优化

```python
from mod import generate_code128, BarcodeConfig

# 高分辨率打印配置
config = BarcodeConfig(
    width=4,           # 更宽的模块
    height=150,        # 更高的条形码
    margin=20,         # 更大的边距
    scale=2.0,         # 2 倍缩放
    text_size=18       # 更大的文本
)

result = generate_code128("PRINT-READY", config)
save_barcode(result, "print_ready.svg")
```

---

## 🧪 运行测试

```bash
cd barcode_utils
python barcode_utils_test.py
```

测试覆盖：
- 所有条形码格式
- 配置选项
- 边界情况
- 错误处理
- SVG 输出验证
- 校验位计算
- 文件保存

---

## 📊 格式选择指南

### Code 39
- **适用场景**：内部追踪、资产标签、工业应用
- **优点**：简单、广泛支持、可打印字母
- **限制**：密度较低、需要起止符

### Code 128
- **适用场景**：物流、包装、运输标签
- **优点**：高密度、支持全 ASCII、自动校验
- **限制**：比 Code 39 复杂

### EAN-13 / UPC-A
- **适用场景**：零售商品、POS 系统
- **优点**：全球标准、自动校验位
- **限制**：仅数字、固定长度

### EAN-8
- **适用场景**：小型商品包装
- **优点**：紧凑、全球标准
- **限制**：仅 8 位数字

### ITF
- **适用场景**：瓦楞纸箱、仓储管理
- **优点**：适合粗糙表面、仅数字
- **限制**：需要偶数位数字

---

## 🔧 高级用法

### 自定义颜色主题

```python
# 深色主题
config = BarcodeConfig(
    foreground="#00FF00",  # 绿色条形码
    background="#000000",  # 黑色背景
    text_size=14
)

result = generate_code128("DARK-MODE", config)
```

### 无文本模式

```python
config = BarcodeConfig(show_text=False)
result = generate_code128("HIDDEN", config)
# SVG 不包含文本标签
```

### 缩放输出

```python
# 小尺寸（名片）
small = BarcodeConfig(scale=0.5)

# 大尺寸（海报）
large = BarcodeConfig(scale=3.0)
```

---

## ⚠️ 注意事项

1. **打印质量**：确保打印机分辨率足够（至少 203 DPI）
2. **扫描距离**：条形码尺寸应适合预期扫描距离
3. **对比度**：前景/背景色应有足够对比度
4. **静区**：保留足够的空白边距（quiet zone）
5. **QR 码**：本模块的 matrix 格式为简化版，生产环境请使用专业 QR 码库

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
