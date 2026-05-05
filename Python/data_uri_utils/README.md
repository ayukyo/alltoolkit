# Data URI Utilities

一个纯 Python 实现的 Data URI 编解码工具库，零外部依赖。

## 功能特性

- ✅ 将文件编码为 Data URI 格式
- ✅ 从 Data URI 解码提取数据
- ✅ 自动检测 MIME 类型（支持 50+ 常用格式）
- ✅ 支持文本和二进制数据
- ✅ Base64 编码支持
- ✅ Data URI 验证和解析
- ✅ 批量文件编码
- ✅ HTML 嵌入标签生成
- ✅ 大小估算
- ✅ 文件扩展名推断

## 安装

无需安装，直接复制 `data_uri_utils.py` 到项目中即可使用。

```python
from data_uri_utils import encode_file, decode_data_uri
```

## 快速开始

### 基本编码

```python
from data_uri_utils import encode_file, encode_data

# 编码文件
uri = encode_file('image.png')
print(uri)  # data:image/png;base64,iVBORw0KGgo...

# 编码数据
data = b'Hello, World!'
uri = encode_data(data, 'text/plain', use_base64=True)
```

### 快捷函数

```python
from data_uri_utils import (
    text_to_data_uri,
    json_to_data_uri,
    html_to_data_uri,
    svg_to_data_uri,
)

# 文本
uri = text_to_data_uri("Hello, Data URI!")

# JSON
uri = json_to_data_uri('{"name": "test", "value": 123}')

# HTML
uri = html_to_data_uri('<html><body>Hello</body></html>')

# SVG
uri = svg_to_data_uri('<svg><circle cx="50" cy="50" r="40"/></svg>')
```

### 解码 Data URI

```python
from data_uri_utils import decode_data_uri, decode_to_file

# 解析 Data URI
parsed = decode_data_uri(uri)
print(parsed.mime_type)     # 'text/plain'
print(parsed.encoding)      # 'base64'
print(parsed.data)          # b'原始数据'
print(parsed.decode_text()) # '文本内容'（如果是文本类型）

# 解码到文件
output_path = decode_to_file(uri, '/path/to/output.txt')
```

### HTML 嵌入

```python
from data_uri_utils import create_html_embed

# 自动推断标签类型
html = create_html_embed('photo.png', alt_text='My Photo')
# <img src="data:image/png;base64,..." alt="My Photo">

# 音频嵌入
html = create_html_embed('audio.mp3', tag_type='audio')
# <audio controls><source src="data:audio/mpeg;base64,..." type="audio/mpeg"></audio>

# 视频嵌入
html = create_html_embed('video.mp4', tag_type='video')
# <video controls><source src="data:video/mp4;base64,..." type="video/mp4"></video>
```

### 批量编码

```python
from data_uri_utils import batch_encode

files = ['image1.png', 'image2.jpg', 'data.json']
results = batch_encode(files, max_size=100_000)  # 限制 100KB

print(f"成功: {len(results['success'])}")
print(f"失败: {len(results['failed'])}")
print(f"跳过: {len(results['skipped'])}")
```

### 工具函数

```python
from data_uri_utils import is_data_uri, get_info, estimate_size

# 验证 Data URI
is_valid = is_data_uri(uri)  # True/False

# 获取详细信息
info = get_info(uri)
print(info)
# {
#     'mime_type': 'image/png',
#     'encoding': 'base64',
#     'original_size': 12345,
#     'encoded_size': 16460,
#     'overhead_ratio': 1.33,
#     'is_base64': True,
#     'is_text': False,
#     'extension': '.png'
# }

# 估算编码后大小
estimated = estimate_size(1000, 'image/png', use_base64=True)
```

## 支持的 MIME 类型

### 图片
`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.ico`, `.bmp`

### 文档
`.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`

### 音频
`.mp3`, `.wav`, `.ogg`, `.m4a`

### 视频
`.mp4`, `.webm`, `.avi`, `.mov`

### 文本/代码
`.txt`, `.html`, `.css`, `.js`, `.json`, `.xml`, `.csv`, `.md`, `.rtf`

### 字体
`.woff`, `.woff2`, `.ttf`, `.otf`, `.eot`

### 压缩
`.zip`, `.gz`, `.tar`, `.rar`, `.7z`

## API 参考

### 编码函数

| 函数 | 说明 |
|------|------|
| `encode_file(file_path, mime_type=None, use_base64=True)` | 文件编码 |
| `encode_data(data, mime_type, use_base64=True)` | 数据编码 |
| `text_to_data_uri(text, mime_type='text/plain')` | 文本快捷编码 |
| `json_to_data_uri(json_str)` | JSON 快捷编码 |
| `html_to_data_uri(html)` | HTML 快捷编码 |
| `svg_to_data_uri(svg)` | SVG 快捷编码 |

### 解码函数

| 函数 | 说明 |
|------|------|
| `decode_data_uri(data_uri)` | 解析 Data URI |
| `decode_to_file(data_uri, output_path)` | 解码到文件 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `is_data_uri(text)` | 验证 Data URI |
| `get_info(data_uri)` | 获取详细信息 |
| `get_mime_type(file_path)` | 获取 MIME 类型 |
| `get_extension(mime_type)` | 获取扩展名 |
| `estimate_size(data_size, mime_type, use_base64)` | 估算大小 |

### 批量函数

| 函数 | 说明 |
|------|------|
| `batch_encode(file_paths, use_base64=True, max_size=None)` | 批量编码 |
| `create_html_embed(file_path, tag_type='auto', alt_text='', css_class='')` | HTML 嵌入 |

## DataURI 类

```python
@dataclass
class DataURI:
    mime_type: str       # MIME 类型
    encoding: str        # 编码方式 ('base64' 或 None)
    data: bytes          # 解码后的数据
    original_size: int   # 原始大小
    encoded_size: int    # 编码后大小
    
    @property
    def is_base64(self) -> bool
    
    @property
    def is_text(self) -> bool
    
    def decode_text(self, encoding='utf-8') -> str
```

## 使用场景

### 小图片内嵌 CSS

```python
from data_uri_utils import encode_file

icon_uri = encode_file('icon.png')
css = f""".icon {{
    background-image: url({icon_uri});
}}"""
```

### Markdown 图片嵌入

```python
from data_uri_utils import encode_file

img_uri = encode_file('diagram.png')
markdown = f"![架构图]({img_uri})"
```

### 离线 HTML 文档

```python
from data_uri_utils import create_html_embed

# 所有资源内嵌，无需外部依赖
html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        .logo {{ background-image: url({encode_file('logo.png')}); }}
    </style>
</head>
<body>
    {create_html_embed('chart.svg')}
</body>
</html>
"""
```

## 注意事项

- Data URI 有大小限制（浏览器通常支持约 32KB）
- 大文件不适合使用 Data URI
- Base64 编码会增加约 33% 的体积

## 许可证

MIT License