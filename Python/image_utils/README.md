# Image Utilities - AllToolkit

**功能完整的 Python 图像处理工具 - 支持 Pillow 或优雅降级**

---

## 📦 功能特性

- ✅ **图像格式转换** - PNG, JPEG, GIF, BMP, WebP, TIFF 互相转换
- ✅ **图像缩放/调整大小** - 精确尺寸或按比例缩放，支持多种插值算法
- ✅ **图像裁剪** - 自定义区域裁剪、中心裁剪
- ✅ **图像旋转** - 任意角度旋转，支持画布扩展
- ✅ **图像翻转** - 水平、垂直、180 度翻转
- ✅ **图像压缩** - 质量控制、最大文件大小限制、尺寸限制
- ✅ **缩略图生成** - 保持宽高比，自动居中
- ✅ **图像信息读取** - 尺寸、格式、颜色模式、透明度检测
- ✅ **批量处理** - 批量缩放、批量格式转换
- ✅ **水印添加** - 文字水印、图片水印，支持多位置
- ✅ **图像合并/拼接** - 水平/垂直拼接、网格布局
- ✅ **优雅降级** - 无 Pillow 时使用标准库实现基础功能

---

## 🚀 快速开始

### 安装依赖

```bash
# 推荐：安装 Pillow 获得完整功能
pip install Pillow

# 或仅使用标准库（功能有限）
# 无需安装任何依赖
```

### 基本使用

```python
from mod import (
    get_image_info,
    resize_image,
    convert_format,
    crop_image,
    rotate_image,
    compress_image,
    generate_thumbnail,
    add_watermark,
    merge_images,
)

# 获取图像信息
info = get_image_info('photo.jpg')
print(f"{info.width}x{info.height} {info.format}")

# 调整大小
resize_image('input.jpg', 800, 600, 'output.jpg')

# 格式转换
convert_format('input.png', 'JPEG', 'output.jpg', quality=85)

# 裁剪
crop_image('input.jpg', (0, 0, 100, 100), 'cropped.jpg')

# 旋转
rotate_image('input.jpg', 90, 'rotated.jpg')

# 压缩
compress_image('large.jpg', 'compressed.jpg', quality=75, max_size=100000)

# 生成缩略图
generate_thumbnail('photo.jpg', (200, 200), 'thumb.jpg')

# 添加水印
add_watermark('photo.jpg', '© 2024', 'watermarked.jpg', position='bottom-right')

# 合并图像
merge_images(['a.jpg', 'b.jpg', 'c.jpg'], 'horizontal', 'panorama.jpg')
```

---

## 📖 API 参考

### 图像信息

#### `get_image_info(source)` → `ImageInfo`

获取图像信息（尺寸、格式、颜色模式等）。

```python
from mod import get_image_info

# 从文件路径
info = get_image_info('photo.jpg')
print(f"尺寸：{info.width}x{info.height}")
print(f"格式：{info.format}")
print(f"颜色模式：{info.mode}")
print(f"文件大小：{info.file_size} 字节")
print(f"有透明通道：{info.has_alpha}")

# 从 bytes
with open('photo.jpg', 'rb') as f:
    info = get_image_info(f.read())

# 从文件对象
with open('photo.jpg', 'rb') as f:
    info = get_image_info(f)

# 转换为字典
info_dict = info.to_dict()
```

**ImageInfo 属性：**

| 属性 | 类型 | 说明 |
|------|------|------|
| `width` | int | 宽度（像素） |
| `height` | int | 高度（像素） |
| `format` | str | 格式（PNG, JPEG, GIF, etc.） |
| `mode` | str | 颜色模式（RGB, RGBA, L, etc.） |
| `file_size` | int | 文件大小（字节） |
| `has_alpha` | bool | 是否有透明通道 |
| `bit_depth` | int | 位深度 |

---

### 格式转换

#### `convert_format(source, output_format, output_path, quality)` → `bytes | None`

转换图像格式。

```python
from mod import convert_format

# 转换为 JPEG
convert_format('input.png', 'JPEG', 'output.jpg')

# 转换为 WebP（高质量）
convert_format('input.png', 'WebP', 'output.webp', quality=90)

# 返回 bytes（不保存文件）
data = convert_format('input.png', 'JPEG')
```

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `source` | str/bytes | - | 源图像路径或数据 |
| `output_format` | str | - | 目标格式（PNG/JPEG/GIF/BMP/WebP/TIFF） |
| `output_path` | str | None | 输出路径（None 则返回 bytes） |
| `quality` | int | 95 | JPEG/WebP 质量（1-100） |

---

### 缩放/调整大小

#### `resize_image(source, width, height, output_path, method, maintain_aspect)` → `bytes | None`

调整图像尺寸。

```python
from mod import resize_image

# 精确尺寸
resize_image('input.jpg', 800, 600, 'output.jpg')

# 保持宽高比（适应框内）
resize_image('input.jpg', 400, 400, maintain_aspect=True)

# 指定插值算法
resize_image('input.jpg', 800, 600, method='lanczos')
```

**插值算法：**

| 算法 | 说明 | 速度 | 质量 |
|------|------|------|------|
| `nearest` | 最近邻 | 最快 | 最低 |
| `bilinear` | 双线性 | 快 | 中等 |
| `bicubic` | 双三次 | 中等 | 高 |
| `lanczos` | Lanczos | 慢 | 最高（默认） |

#### `scale_image(source, scale_factor, output_path)` → `bytes | None`

按比例缩放。

```python
from mod import scale_image

# 缩小到 50%
scale_image('input.jpg', 0.5, 'half.jpg')

# 放大到 200%
scale_image('input.jpg', 2.0, 'double.jpg')
```

---

### 裁剪

#### `crop_image(source, box, output_path)` → `bytes | None`

自定义区域裁剪。

```python
from mod import crop_image

# 裁剪左上角 100x100 区域
crop_image('input.jpg', (0, 0, 100, 100), 'cropped.jpg')

# box = (left, upper, right, lower)
```

#### `center_crop(source, width, height, output_path)` → `bytes | None`

从中心裁剪。

```python
from mod import center_crop

# 中心裁剪为正方形
center_crop('input.jpg', 400, 400, 'square.jpg')
```

---

### 旋转/翻转

#### `rotate_image(source, angle, output_path, expand, fill_color)` → `bytes | None`

旋转图像。

```python
from mod import rotate_image

# 旋转 90 度
rotate_image('input.jpg', 90, 'rotated.jpg')

# 旋转 45 度并扩展画布
rotate_image('input.jpg', 45, expand=True)

# 旋转并指定填充颜色
rotate_image('input.jpg', 30, fill_color=(255, 255, 255, 0))
```

#### `flip_image(source, direction, output_path)` → `bytes | None`

翻转图像。

```python
from mod import flip_image

# 水平翻转（镜像）
flip_image('input.jpg', 'horizontal', 'mirrored.jpg')

# 垂直翻转
flip_image('input.jpg', 'vertical', 'flipped.jpg')

# 180 度翻转
flip_image('input.jpg', 'both', 'rotated180.jpg')
```

---

### 压缩

#### `compress_image(source, output_path, quality, max_size, max_dimensions)` → `bytes | None`

压缩图像。

```python
from mod import compress_image

# 降低质量
compress_image('input.jpg', 'output.jpg', quality=75)

# 限制最大文件大小（100KB）
compress_image('input.jpg', 'output.jpg', max_size=100000)

# 限制最大尺寸
compress_image('input.jpg', max_dimensions=(1920, 1080))

# 组合使用
compress_image('input.jpg', 'output.jpg', quality=80, max_size=50000)
```

---

### 缩略图

#### `generate_thumbnail(source, size, output_path, maintain_aspect)` → `bytes | None`

生成缩略图。

```python
from mod import generate_thumbnail

# 生成 200x200 缩略图
generate_thumbnail('photo.jpg', (200, 200), 'thumb.jpg')

# 保持宽高比（可能小于指定尺寸）
generate_thumbnail('photo.jpg', (200, 200), maintain_aspect=True)
```

---

### 水印

#### `add_watermark(source, text, output_path, position, font_size, color, margin)` → `bytes | None`

添加文字水印。

```python
from mod import add_watermark

# 右下角水印
add_watermark('photo.jpg', '© 2024', 'watermarked.jpg')

# 中心大水印
add_watermark('photo.jpg', 'CONFIDENTIAL', position='center',
              font_size=48, color=(255, 0, 0, 100))

# 左上角小水印
add_watermark('photo.jpg', 'Logo', position='top-left',
              font_size=16, color=(255, 255, 255, 200))
```

**位置选项：** `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center`

**颜色格式：** `(R, G, B, A)` - RGBA 值（0-255）

#### `add_image_watermark(source, watermark_path, output_path, position, opacity, scale, margin)` → `bytes | None`

添加图片水印。

```python
from mod import add_image_watermark

# 添加 logo 水印
add_image_watermark('photo.jpg', 'logo.png', 'watermarked.jpg')

# 半透明小水印
add_image_watermark('photo.jpg', 'logo.png', opacity=0.5, scale=0.1)
```

---

### 合并/拼接

#### `merge_images(images, direction, output_path, gap, background_color)` → `bytes | None`

拼接多张图像。

```python
from mod import merge_images

# 水平拼接（全景图）
merge_images(['left.jpg', 'center.jpg', 'right.jpg'],
             'horizontal', 'panorama.jpg')

# 垂直拼接
merge_images(['top.png', 'bottom.png'], 'vertical', 'combined.png')

# 带间距拼接
merge_images(['a.jpg', 'b.jpg'], 'horizontal', gap=10)
```

#### `create_grid(images, cols, output_path, cell_size, gap, background_color)` → `bytes | None`

创建图像网格。

```python
from mod import create_grid

# 2x2 网格
create_grid(['1.jpg', '2.jpg', '3.jpg', '4.jpg'],
            cols=2, output_path='grid.png')

# 3 列网格，带间距
create_grid(images, cols=3, gap=5, background_color=(255, 255, 255, 255))
```

---

### 批量处理

#### `batch_resize(input_dir, output_dir, width, height, pattern, maintain_aspect)` → `Dict`

批量调整大小。

```python
from mod import batch_resize

# 批量缩放到 800x600
result = batch_resize('photos/', 'thumbnails/', 800, 600)

# 保持宽高比
result = batch_resize('photos/', 'thumbnails/', 400, 400, maintain_aspect=True)

# 仅处理 JPG 文件
result = batch_resize('photos/', 'output/', 800, 600, pattern='*.jpg')

print(f"处理：{result['processed']} 成功，{result['failed']} 失败")
```

#### `batch_convert(input_dir, output_dir, target_format, pattern, quality)` → `Dict`

批量格式转换。

```python
from mod import batch_convert

# 批量转换为 WebP
result = batch_convert('photos/', 'webp/', 'webp')

# 批量转换为 JPEG（高质量）
result = batch_convert('photos/', 'jpg/', 'jpg', quality=95)

print(f"转换：{result['processed']} 成功，{result['failed']} 失败")
```

---

### 模块信息

```python
from mod import get_version, is_pillow_available, get_supported_formats

# 获取版本
version = get_version()  # "1.0.0"

# 检查 Pillow
has_pillow = is_pillow_available()  # True/False

# 获取支持的格式
formats = get_supported_formats()  # ['BMP', 'GIF', 'JPEG', 'PNG', 'WebP', ...]
```

---

## 💡 使用场景

### 1. 网站图片优化

```python
from mod import compress_image, generate_thumbnail, convert_format

# 上传处理
def process_upload(input_path, output_dir):
    # 转换为 WebP
    convert_format(input_path, 'WebP', f'{output_dir}/image.webp', quality=85)
    
    # 生成缩略图
    generate_thumbnail(input_path, (200, 200), f'{output_dir}/thumb.jpg')
    
    # 生成中等尺寸
    resize_image(input_path, 800, 800, f'{output_dir}/medium.jpg', maintain_aspect=True)
```

### 2. 批量水印

```python
from mod import add_watermark
import glob

for img_path in glob.glob('photos/*.jpg'):
    add_watermark(img_path, '© MyCompany', 
                  output_path=img_path.replace('.jpg', '_wm.jpg'),
                  position='bottom-right',
                  font_size=24,
                  color=(255, 255, 255, 180))
```

### 3. 制作拼图

```python
from mod import create_grid

# 制作 9 宫格
images = [f'photo{i}.jpg' for i in range(1, 10)]
create_grid(images, cols=3, output_path='collage.png', gap=5)
```

### 4. 图像预处理（机器学习）

```python
from mod import resize_image, compress_image

# 预处理训练数据
for img in glob.glob('dataset/*.jpg'):
    # 调整到统一尺寸
    resize_image(img, 224, 224, img.replace('.jpg', '_processed.jpg'))
    
    # 压缩以节省空间
    compress_image(img, img.replace('.jpg', '_compressed.jpg'),
                   max_size=50000, max_dimensions=(512, 512))
```

### 5. 社交媒体图片适配

```python
from mod import center_crop, resize_image

# Instagram 正方形
center_crop('photo.jpg', 1080, 1080, 'instagram_square.jpg')

# Instagram 故事
resize_image('photo.jpg', 1080, 1920, 'instagram_story.jpg', maintain_aspect=True)

# Twitter 封面
center_crop('photo.jpg', 1500, 500, 'twitter_header.jpg')
```

---

## 🧪 运行测试

```bash
cd image_utils
python image_utils_test.py
```

测试覆盖：

- ✅ ImageInfo 类功能
- ✅ 图像信息读取（PNG/JPEG/GIF/BMP/WebP）
- ✅ 格式转换
- ✅ 缩放/比例缩放
- ✅ 裁剪（自定义/中心）
- ✅ 旋转/翻转
- ✅ 压缩（质量/大小限制）
- ✅ 缩略图生成
- ✅ 水印添加（文字/图片）
- ✅ 图像合并/网格
- ✅ 批量处理
- ✅ 边界情况（极小/大图像、RGBA）

---

## 📊 性能提示

1. **使用 Pillow**：完整功能需要 Pillow，标准库实现仅支持信息读取
2. **Lanczos 质量最高**：缩放时使用 `method='lanczos'` 获得最佳质量
3. **WebP 更优压缩**：相同质量下 WebP 比 JPEG 小 25-35%
4. **批量处理**：使用 `batch_*` 函数比循环调用更高效
5. **缩略图缓存**：生成后保存，避免重复生成

---

## 🔧 无 Pillow 降级

当 Pillow 不可用时：

| 功能 | 状态 |
|------|------|
| 图像信息读取 | ✅ 支持（PNG/JPEG/GIF/BMP/WebP） |
| 格式转换 | ❌ 需要 Pillow |
| 缩放/裁剪 | ❌ 需要 Pillow |
| 旋转/翻转 | ❌ 需要 Pillow |
| 压缩 | ❌ 需要 Pillow |
| 缩略图 | ❌ 需要 Pillow |
| 水印 | ❌ 需要 Pillow |
| 合并 | ❌ 需要 Pillow |

**安装 Pillow：**

```bash
pip install Pillow
# 或
pip3 install Pillow
```

---

## 🔒 注意事项

1. **透明度处理**：JPEG 不支持透明，转换时会自动添加白色背景
2. **EXIF 数据**：转换/处理时可能丢失 EXIF 元数据
3. **动画 GIF**：当前实现仅处理第一帧
4. **大文件**：处理大图像时注意内存使用
5. **字体**：水印功能需要系统字体，会自动查找 DejaVu 字体

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
