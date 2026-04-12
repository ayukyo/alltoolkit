# QR Utils - 二维码工具库

纯 Python 实现的二维码生成工具库，零外部依赖。支持多种数据格式编码和灵活的输出方式。

## 功能特性

- ✅ 纯 Python 实现，零外部依赖
- ✅ QR 码矩阵生成（版本 1-10）
- ✅ 多种纠错级别（L/M/Q/H）
- ✅ ASCII 艺术渲染
- ✅ Emoji 艺术渲染
- ✅ PNG 图片生成（纯 Python PNG 编码）
- ✅ Data URL 生成（可直接嵌入 HTML）
- ✅ 多种数据编码（URL/vCard/WiFi/Email/SMS/文本）
- ✅ 批量生成支持
- ✅ 数据验证和统计
- ✅ Python 3.6+ 兼容

## 安装

无需安装，直接复制 `qr_utils.py` 到项目即可使用。

```bash
# 直接复制文件
cp qr_utils.py your_project/
```

## 快速开始

```python
from qr_utils import generate_qr_matrix, render_qr_ascii, save_qr_image

# 生成 QR 码矩阵
matrix = generate_qr_matrix("Hello, World!")

# ASCII 预览
print(render_qr_ascii(matrix))

# 保存为 PNG 图片
save_qr_image(matrix, "qrcode.png")
```

## API 参考

### 核心函数

#### `generate_qr_matrix(data, version=1, error_correction='M')`
生成 QR 码矩阵。

```python
from qr_utils import generate_qr_matrix

# 自动生成版本
matrix = generate_qr_matrix("https://example.com")

# 指定版本和纠错级别
matrix = generate_qr_matrix("data", version=3, error_correction='H')
```

**参数:**
- `data`: 要编码的数据（字符串）
- `version`: QR 码版本 (1-10)，0 表示自动选择
- `error_correction`: 纠错级别 ('L'/'M'/'Q'/'H')

**返回:** 二维布尔矩阵（True=黑色，False=白色）

#### `render_qr_ascii(matrix, dark_char='█', light_char=' ')`
将 QR 码矩阵渲染为 ASCII 艺术。

```python
ascii_art = render_qr_ascii(matrix)
print(ascii_art)
```

#### `render_qr_emoji(matrix)`
将 QR 码矩阵渲染为 Emoji 艺术。

```python
emoji_art = render_qr_emoji(matrix)
print(emoji_art)
# 输出：🟥🟥🟥⬜🟥🟥🟥...
```

#### `save_qr_image(matrix, filepath, **kwargs)`
保存 QR 码为 PNG 图片。

```python
save_qr_image(matrix, "qrcode.png")

# 自定义样式
save_qr_image(matrix, "colorful.png", 
              box_size=15,
              border=4,
              fill_color='#FF0000',
              back_color='#FFFFFF')
```

**参数:**
- `matrix`: QR 码矩阵
- `filepath`: 输出文件路径
- `box_size`: 每个模块的像素大小（默认 10）
- `border`: 边框宽度（默认 4）
- `fill_color`: 填充颜色（支持颜色名和 #RRGGBB）
- `back_color`: 背景颜色

#### `generate_qr_data_url(data, **kwargs)`
生成 QR 码的 Data URL（可直接嵌入 HTML）。

```python
data_url = generate_qr_data_url("https://example.com")
html = f'<img src="{data_url}" alt="QR Code">'
```

### 数据编码函数

#### `encode_url(url)`
编码 URL。

```python
url = encode_url("example.com")  # 自动添加 https://
```

#### `encode_vcard(name, phone, email='', org='', title='')`
编码 vCard 联系人信息。

```python
vcard = encode_vcard(
    name="张三",
    phone="13800138000",
    email="zhangsan@example.com",
    org="测试公司",
    title="工程师"
)
matrix = generate_qr_matrix(vcard)
```

#### `encode_wifi(ssid, password, encryption='WPA', hidden=False)`
编码 WiFi 连接信息（手机扫描即可连接）。

```python
wifi = encode_wifi("MyWiFi", "password123")
matrix = generate_qr_matrix(wifi)
```

#### `encode_email(to, subject='', body='')`
编码邮件信息（扫描后打开邮件客户端）。

```python
mailto = encode_email("user@example.com", "咨询", "您好...")
matrix = generate_qr_matrix(mailto)
```

#### `encode_sms(phone, message='')`
编码短信信息。

```python
sms = encode_sms("13800138000", "Hello!")
matrix = generate_qr_matrix(sms)
```

#### `encode_text(text)`
编码纯文本。

```python
text = encode_text("任意文本内容")
```

### 工具函数

#### `get_qr_info(data)`
获取 QR 码信息（推荐版本、容量等）。

```python
info = get_qr_info("https://example.com")
print(f"推荐版本：{info['recommended_version']}")
print(f"剩余容量：{info['capacity_remaining']} 字节")
```

**返回字段:**
- `data_length`: 数据长度
- `recommended_version`: 推荐版本
- `matrix_size`: 矩阵大小
- `capacity_remaining`: 剩余容量
- `error_correction`: 纠错级别

#### `validate_qr_data(data, data_type='auto')`
验证 QR 码数据格式。

```python
validate_qr_data("https://example.com", "url")  # True
validate_qr_data("not-url", "url")  # False
validate_qr_data(vcard, "vcard")  # True
```

**支持类型:** auto, url, vcard, wifi, email, sms, text

#### `get_matrix_stats(matrix)`
获取 QR 码矩阵统计信息。

```python
stats = get_matrix_stats(matrix)
print(f"深色比例：{stats['dark_ratio']:.2%}")
```

**返回字段:**
- `size`: 矩阵尺寸
- `total_modules`: 总模块数
- `dark_modules`: 深色模块数
- `light_modules`: 浅色模块数
- `dark_ratio`: 深色比例

#### `generate_qr_batch(data_list, output_dir, prefix='qr', **kwargs)`
批量生成 QR 码图片。

```python
urls = [
    "https://site1.com",
    "https://site2.com",
    "https://site3.com",
]
files = generate_qr_batch(urls, "./qrcodes", prefix="site")
# 生成：site_0000.png, site_0001.png, site_0002.png
```

### 模块信息

#### `get_version()`
获取模块版本。

```python
version = get_version()  # "1.0.0"
```

#### `get_capabilities()`
获取功能列表。

```python
caps = get_capabilities()
for cap in caps:
    print(f"  - {cap}")
```

## 使用示例

### 场景 1：生成网站 QR 码

```python
from qr_utils import generate_qr_matrix, save_qr_image

matrix = generate_qr_matrix("https://example.com")
save_qr_image(matrix, "website_qr.png", box_size=15)
```

### 场景 2：创建 WiFi 连接码

```python
from qr_utils import encode_wifi, generate_qr_matrix, save_qr_image

wifi = encode_wifi("Office-WiFi", "SecurePass123", encryption="WPA2")
matrix = generate_qr_matrix(wifi)
save_qr_image(matrix, "wifi_qr.png")
```

### 场景 3：生成电子名片

```python
from qr_utils import encode_vcard, generate_qr_matrix, save_qr_image

vcard = encode_vcard(
    name="李明",
    phone="13800138000",
    email="liming@company.com",
    org="某某科技",
    title="技术总监"
)
matrix = generate_qr_matrix(vcard)
save_qr_image(matrix, "business_card.png")
```

### 场景 4：终端快速预览

```python
from qr_utils import generate_qr_matrix, render_qr_ascii

matrix = generate_qr_matrix("Hello!")
print(render_qr_ascii(matrix))
```

输出：
```
███████  ████  ███████
█     █  █  █  █     █
███████  ████  ███████
...
```

### 场景 5：社交媒体分享（Emoji）

```python
from qr_utils import generate_qr_matrix, render_qr_emoji

matrix = generate_qr_matrix("https://example.com")
emoji_qr = render_qr_emoji(matrix)
print(emoji_qr)  # 可直接复制到微信/微博
```

### 场景 6：HTML 嵌入

```python
from qr_utils import generate_qr_data_url

data_url = generate_qr_data_url("https://example.com", box_size=8)
html = f'''
<html>
<body>
  <h1>扫描二维码访问</h1>
  <img src="{data_url}" alt="QR Code" width="200">
</body>
</html>
'''
```

### 场景 7：批量生成产品码

```python
from qr_utils import generate_qr_batch

products = [
    "https://shop.com/product/001",
    "https://shop.com/product/002",
    "https://shop.com/product/003",
    # ... 更多产品
]

files = generate_qr_batch(
    products, 
    "./product_qrcodes",
    prefix="product",
    box_size=12
)
```

## 技术规格

### QR 码版本

| 版本 | 矩阵大小 | 容量 (M 级) |
|------|----------|-------------|
| 1 | 21x21 | 47 字节 |
| 2 | 25x25 | 77 字节 |
| 3 | 29x29 | 127 字节 |
| 4 | 33x33 | 187 字节 |
| 5 | 37x37 | 255 字节 |
| 6 | 41x41 | 322 字节 |
| 7 | 45x45 | 370 字节 |
| 8 | 49x49 | 461 字节 |
| 9 | 53x53 | 552 字节 |
| 10 | 57x57 | 652 字节 |

### 纠错级别

| 级别 | 恢复能力 | 适用场景 |
|------|----------|----------|
| L | 7% | 数据量小，环境良好 |
| M | 15% | 标准使用（默认） |
| Q | 25% | 可能部分污损 |
| H | 30% | 高可靠性需求 |

### 颜色支持

支持以下颜色格式：
- 颜色名：`black`, `white`, `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`, `gray`
- Hex 代码：`#RRGGBB`（如 `#FF0000`）

## 注意事项

1. **版本限制**: 当前实现支持版本 1-10，适合中小型数据。如需更大数据容量，建议安装 `qrcode` 库。

2. **无头环境**: 可在服务器、Docker 等无图形界面环境中使用。

3. **Unicode 支持**: 完全支持中文、Emoji 等 Unicode 字符。

4. **性能**: 纯 Python 实现适合中小批量生成。大批量场景建议：
   - 使用 `generate_qr_batch` 批量处理
   - 或安装 `qrcode` + `Pillow` 获得更好性能

5. **PNG 压缩**: 使用 zlib 最大压缩级别，文件较小但生成稍慢。

## 与 qrcode 库对比

| 特性 | qr_utils | qrcode + Pillow |
|------|----------|-----------------|
| 外部依赖 | 无 | 需要安装 |
| 安装复杂度 | 复制即用 | pip install |
| 版本支持 | 1-10 | 1-40 |
| PNG 生成 | 纯 Python | Pillow |
| 自定义渲染 | ASCII/Emoji | 需自行实现 |
| 适用场景 | 轻量/嵌入式 | 专业应用 |

## 运行测试

```bash
cd Python
python qr_utils_test.py
```

## 许可证

MIT License - AllToolkit

## 版本

- Version: 1.0.0
- Author: AllToolkit
- Python: 3.6+
- Dependencies: None (pure Python stdlib)

## 更新日志

### v1.0.0 (2026-04-12)
- 初始版本
- 纯 Python QR 码矩阵生成
- ASCII/Emoji 渲染
- PNG 图片生成
- 多种数据编码格式
- 批量处理支持
- 完整测试套件
