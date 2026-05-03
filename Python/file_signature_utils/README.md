# file_signature_utils

文件签名/魔数检测工具 - 通过文件头部魔数检测文件真实类型。

## 功能特性

- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **支持 100+ 文件格式** - 图片、视频、音频、文档、压缩包等
- ✅ **真实类型检测** - 即使扩展名被更改也能正确识别
- ✅ **多种输入方式** - 支持文件路径、字节流、文件对象
- ✅ **扩展名验证** - 检查文件扩展名与实际类型是否匹配
- ✅ **MIME 类型检测** - 自动获取文件的 MIME 类型
- ✅ **批量处理** - 支持批量检测多个文件
- ✅ **安全检查** - 适用于上传文件安全验证

## 支持的文件格式

### 图片格式
- JPEG, PNG, GIF, BMP, TIFF, WebP
- ICO, PSD, PBM, PGM, PPM, PAM, HEIC

### 视频格式
- MP4, MKV, AVI, MOV, WMV, FLV, WebM
- MPEG, 3GP

### 音频格式
- MP3, FLAC, WAV, OGG, M4A, M4B
- WMA, AIFF, APE, MIDI

### 文档格式
- PDF, XML, HTML, JSON
- Office OLE (DOC, XLS, PPT)
- Office OpenXML (DOCX, XLSX, PPTX)

### 压缩格式
- ZIP, RAR, GZIP, BZIP2, XZ
- 7-Zip, LZ4, Zstandard, ARJ

### 可执行文件
- Windows EXE/DLL
- Linux ELF
- macOS Mach-O
- Java Class
- Android DEX/APK

### 数据库
- SQLite
- HDF5
- NumPy (.npy)
- MATLAB (.mat)

### 字体格式
- TrueType (TTF)
- OpenType (OTF)
- WOFF, WOFF2

### 证书格式
- PEM
- DER
- SSH Keys
- PGP Keys

### 磁盘镜像
- ISO
- DMG
- VMDK, VHD, VHDX

## 快速开始

### 基本检测

```python
from file_signature_utils.mod import detect_file_type

# 从字节流检测
jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF'
ft = detect_file_type(jpeg_data)
print(ft.extension)   # 'jpg'
print(ft.mime_type)   # 'image/jpeg'
print(ft.description) # 'JPEG Image'

# 从文件路径检测
ft = detect_file_type('/path/to/file.pdf')
print(ft.extension)   # 'pdf'

# 从文件对象检测
with open('/path/to/file.png', 'rb') as f:
    ft = detect_file_type(f)
    print(ft.extension)  # 'png'
```

### 只获取扩展名

```python
from file_signature_utils.mod import detect_extension

ext = detect_extension(b'\x89PNG\r\n\x1a\n')
print(ext)  # 'png'
```

### 只获取 MIME 类型

```python
from file_signature_utils.mod import detect_mime_type

mime = detect_mime_type('/path/to/audio.mp3')
print(mime)  # 'audio/mpeg'
```

### 验证扩展名

```python
from file_signature_utils.mod import verify_extension

match, declared, actual = verify_extension('/path/to/fake.txt')
# 如果文件实际是 PNG 但扩展名是 txt:
# match = False, declared = 'txt', actual = 'png'
```

### 类型检查

```python
from file_signature_utils.mod import is_image, is_video, is_audio

# 检查是否为图片
if is_image('/path/to/file.jpg'):
    print("这是一个图片文件")

# 检查是否为视频
if is_video(b'\x00\x00\x00\x20ftypisom'):
    print("这是 MP4 视频")

# 检查是否为压缩包
if is_archive('/path/to/file.rar'):
    print("这是一个压缩文件")
```

### 批量检测

```python
from file_signature_utils.mod import batch_detect

files = ['/path/to/file1', '/path/to/file2', '/path/to/file3']
results = batch_detect(files)

for file_path, file_type in results.items():
    print(f"{file_path}: {file_type.extension}")
```

### 全面分析

```python
from file_signature_utils.mod import analyze_file

result = analyze_file('/path/to/file.png')
print(result['file_type'])      # FileType 对象
print(result['extension_match']) # True/False
print(result['is_image'])       # True
print(result['size'])           # 文件大小
```

## 安全检查场景

```python
from file_signature_utils.mod import verify_extension, is_executable

# 检查上传的文件是否伪装
match, declared, actual = verify_extension(uploaded_file)

if not match:
    print(f"警告: 文件声称是 {declared}，实际是 {actual}")

# 检查是否伪装成图片的可执行文件
if declared == 'jpg' and is_executable(uploaded_file):
    print("警告: 可能是恶意软件！")
```

## API 参考

### FileType 类

文件类型信息对象。

```python
FileType(
    extension: str,      # 文件扩展名
    mime_type: str,      # MIME 类型
    description: str,    # 类型描述
    confidence: float    # 置信度 (0-1)
)
```

### 主要函数

| 函数 | 说明 |
|------|------|
| `detect_file_type(source)` | 检测文件类型 |
| `detect_extension(source)` | 检测文件扩展名 |
| `detect_mime_type(source)` | 检测 MIME 类型 |
| `verify_extension(file_path)` | 验证扩展名是否匹配 |
| `batch_detect(file_paths)` | 批量检测多个文件 |
| `analyze_file(file_path)` | 全面分析文件 |

### 类型检查函数

| 函数 | 说明 |
|------|------|
| `is_type(source, extension)` | 检查是否为指定类型 |
| `is_image(source)` | 检查是否为图片 |
| `is_video(source)` | 检查是否为视频 |
| `is_audio(source)` | 检查是否为音频 |
| `is_document(source)` | 检查是否为文档 |
| `is_archive(source)` | 检查是否为压缩包 |
| `is_executable(source)` | 检查是否为可执行文件 |

### 辅助函数

| 函数 | 说明 |
|------|------|
| `get_supported_types()` | 获取支持的文件类型列表 |
| `get_extension_mime_map()` | 获取扩展名到 MIME 映射 |

## 运行测试

```bash
python Python/file_signature_utils/file_signature_utils_test.py
```

## 运行示例

```bash
python Python/file_signature_utils/examples/usage_examples.py
```

## 测试覆盖

- 60+ 测试用例
- 覆盖所有主要文件格式
- 边界值测试（空数据、短数据、未知格式）
- 文件对象输入测试
- Unicode 文件名测试
- 安全检查场景测试

## 许可证

MIT License