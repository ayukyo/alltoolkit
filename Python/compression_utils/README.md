# Compression Utils 🗜️

**Python 压缩工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`compression_utils` 是一个全面的 Python 压缩工具模块，提供 ZIP、GZIP、BZ2、LZMA/XZ、TAR 等多种压缩格式的支持。所有实现均使用 Python 标准库，零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库（`zipfile`、`gzip`、`bz2`、`lzma`、`tarfile`）
- **多格式支持** - ZIP、GZIP、BZ2、LZMA/XZ、TAR
- **完整功能** - 压缩、解压、列表、追加、流式处理
- **批量操作** - 文件和目录批量压缩
- **压缩对比** - 自动比较不同压缩方法的效果
- **流式处理** - 支持大文件的流式压缩/解压
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 100+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/compression_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

```python
from mod import create_zip, extract_zip, gzip_compress, create_tar

# 创建 ZIP 压缩包
result = create_zip('archive.zip', ['file1.txt', 'dir1/'])
print(f"压缩了 {result['files']} 个文件，压缩率：{result['ratio']}")

# 解压 ZIP 文件
files = extract_zip('archive.zip', 'output/')
print(f"解压了 {len(files)} 个文件")

# GZIP 压缩
gz_path = gzip_compress('document.txt')
print(f"压缩到：{gz_path}")

# 创建 TAR.GZ 压缩包
result = create_tar('backup.tar.gz', ['data/'], compression='gz')
```

---

## 📚 API 参考

### ZIP 操作

#### `create_zip(output_path, source_paths, compression='deflate', compression_level=6, ...)`

创建 ZIP 压缩包。

```python
# 基本用法
result = create_zip('archive.zip', ['file1.txt', 'file2.txt', 'dir/'])
print(result)
# {'files': 5, 'compressed_size': 1024, 'original_size': 4096, 'ratio': '75.0%'}

# 使用不同压缩方法
result = create_zip('archive.zip', ['data/'], compression='bzip2', compression_level=9)

# 压缩方法：'store'（无压缩）、'deflate'、'bzip2'、'lzma'
```

#### `extract_zip(zip_path, extract_to='.', password=None, members=None)`

解压 ZIP 文件。

```python
# 解压全部
files = extract_zip('archive.zip', 'output/')

# 解压特定文件
files = extract_zip('archive.zip', 'output/', members=['file1.txt', 'dir/file2.txt'])

# 解压加密文件
files = extract_zip('secure.zip', 'output/', password='secret')
```

#### `list_zip_contents(zip_path)`

列出 ZIP 文件内容。

```python
contents = list_zip_contents('archive.zip')
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
# 输出：
# file1.txt: 1024 bytes
# dir/file2.txt: 2048 bytes
```

#### `add_to_zip(zip_path, source_paths, compression='deflate')`

向现有 ZIP 文件添加文件。

```python
added = add_to_zip('archive.zip', ['new_file.txt', 'new_dir/'])
print(f"添加了 {added} 个文件")
```

---

### GZIP 操作

#### `gzip_compress(input_path, output_path=None, compression_level=6, keep_original=True)`

使用 GZIP 压缩文件。

```python
# 基本用法（生成 file.txt.gz）
gz_path = gzip_compress('file.txt')

# 指定输出路径
gz_path = gzip_compress('file.txt', 'compressed.gz')

# 删除原文件
gz_path = gzip_compress('file.txt', keep_original=False)
```

#### `gzip_decompress(input_path, output_path=None, keep_original=True)`

解压 GZIP 文件。

```python
# 解压（自动去掉 .gz 后缀）
path = gzip_decompress('file.txt.gz')

# 指定输出路径
path = gzip_decompress('file.txt.gz', 'output.txt')
```

#### `gzip_compress_bytes(data, compression_level=6)`

压缩字节数据。

```python
compressed = gzip_compress_bytes(b"Hello, World!")
```

#### `gzip_decompress_bytes(data)`

解压 GZIP 字节数据。

```python
original = gzip_decompress_bytes(compressed)
```

---

### BZ2 操作

#### `bz2_compress(input_path, output_path=None, compression_level=6, keep_original=True)`

使用 BZ2 压缩文件。

```python
bz2_path = bz2_compress('file.txt')
```

#### `bz2_decompress(input_path, output_path=None, keep_original=True)`

解压 BZ2 文件。

```python
path = bz2_decompress('file.txt.bz2')
```

#### `bz2_compress_bytes(data)` / `bz2_decompress_bytes(data)`

BZ2 字节数据压缩/解压。

```python
compressed = bz2_compress_bytes(b"data")
original = bz2_decompress_bytes(compressed)
```

---

### LZMA/XZ 操作

#### `lzma_compress(input_path, output_path=None, compression_level=6, keep_original=True)`

使用 LZMA 压缩文件（生成 .xz 文件）。

```python
xz_path = lzma_compress('file.txt')
```

#### `lzma_decompress(input_path, output_path=None, keep_original=True)`

解压 LZMA/XZ 文件。

```python
path = lzma_decompress('file.txt.xz')
```

#### `lzma_compress_bytes(data)` / `lzma_decompress_bytes(data)`

LZMA 字节数据压缩/解压。

```python
compressed = lzma_compress_bytes(b"data")
original = lzma_decompress_bytes(compressed)
```

---

### TAR 操作

#### `create_tar(output_path, source_paths, compression=None, base_path=None)`

创建 TAR 归档文件。

```python
# 无压缩 TAR
result = create_tar('archive.tar', ['dir/'])

# TAR.GZ
result = create_tar('archive.tar.gz', ['dir/'], compression='gz')

# TAR.BZ2
result = create_tar('archive.tar.bz2', ['dir/'], compression='bz2')

# TAR.XZ
result = create_tar('archive.tar.xz', ['dir/'], compression='xz')
```

#### `extract_tar(tar_path, extract_to='.', members=None)`

解压 TAR 归档文件。

```python
# 自动检测压缩格式
files = extract_tar('archive.tar.gz', 'output/')

# 解压特定文件
files = extract_tar('archive.tar', 'output/', members=['file1.txt'])
```

#### `list_tar_contents(tar_path)`

列出 TAR 文件内容。

```python
contents = list_tar_contents('archive.tar.gz')
for item in contents:
    print(f"{item['name']}: {item['size']} bytes, {item['datetime']}")
```

#### `append_to_tar(tar_path, source_paths, compression=None)`

向 TAR 文件追加内容。

```python
added = append_to_tar('archive.tar', ['new_file.txt'])
```

---

### 实用工具函数

#### `get_compression_ratio(original_size, compressed_size)`

计算压缩率。

```python
ratio = get_compression_ratio(1000, 500)
print(ratio)  # "50.0%"
```

#### `format_size(size_bytes)`

格式化字节大小为人类可读格式。

```python
print(format_size(1536))      # "1.50 KB"
print(format_size(1572864))   # "1.50 MB"
print(format_size(500))       # "500.00 B"
```

#### `get_file_info(file_path)`

获取文件详细信息。

```python
info = get_file_info('document.pdf')
print(info)
# {
#     'name': 'document.pdf',
#     'path': '/absolute/path/document.pdf',
#     'size': 1048576,
#     'size_formatted': '1.00 MB',
#     'created': '2024-01-01T00:00:00',
#     'modified': '2024-01-02T00:00:00',
#     'is_file': True,
#     'is_dir': False
# }
```

#### `compare_compression_methods(input_path, methods=['gzip', 'bz2', 'lzma'])`

比较不同压缩方法的效果。

```python
results = compare_compression_methods('large_file.txt')
print(results)
# {
#     'original': {'size': 1000000, 'size_formatted': '976.56 KB'},
#     'gzip': {'compressed_size': 350000, 'ratio': '65.0%', 'size_formatted': '341.80 KB'},
#     'bz2': {'compressed_size': 280000, 'ratio': '72.0%', 'size_formatted': '273.44 KB'},
#     'lzma': {'compressed_size': 220000, 'ratio': '78.0%', 'size_formatted': '214.84 KB'}
# }
```

---

### 流式压缩类

#### `StreamingCompressor`

用于大文件的流式压缩。

```python
compressor = StreamingCompressor('gzip')

# 分块写入
with open('input.bin', 'rb') as f_in, open('output.gz', 'wb') as f_out:
    while chunk := f_in.read(8192):
        compressed = compressor.write(chunk)
        if compressed:
            f_out.write(compressed)
    
    # 刷新缓冲区
    f_out.write(compressor.flush())
```

#### `StreamingDecompressor`

用于大文件的流式解压。

```python
decompressor = StreamingDecompressor('gzip')

with open('input.gz', 'rb') as f_in, open('output.bin', 'wb') as f_out:
    while chunk := f_in.read(8192):
        decompressed = decompressor.write(chunk)
        if decompressed:
            f_out.write(decompressed)
    
    f_out.write(decompressor.flush())
```

---

## 📝 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基本用法示例
- `batch_compress.py` - 批量压缩示例
- `compression_comparison.py` - 压缩方法对比
- `streaming_example.py` - 流式处理示例
- `backup_script.py` - 备份脚本示例

---

## 🧪 运行测试

```bash
cd compression_utils
python compression_utils_test.py
```

测试覆盖：
- ZIP 创建、解压、列表、追加
- GZIP 压缩/解压（文件和字节）
- BZ2 压缩/解压（文件和字节）
- LZMA/XZ 压缩/解压（文件和字节）
- TAR 创建、解压、列表、追加
- 实用工具函数
- 流式压缩类
- 边界情况和错误处理

---

## 📊 压缩方法对比

| 方法 | 压缩率 | 速度 | 适用场景 |
|------|--------|------|----------|
| ZIP (deflate) | 中等 | 快 | 通用文件归档 |
| GZIP | 中等 | 快 | 网络传输、日志压缩 |
| BZ2 | 高 | 中等 | 文本文件、需要高压缩率 |
| LZMA/XZ | 最高 | 慢 | 长期归档、最大压缩率 |
| TAR (无压缩) | 无 | 最快 | 文件打包、保留权限 |
| TAR.GZ | 中等 | 快 | Linux 备份常用 |
| TAR.BZ2 | 高 | 中等 | 源代码分发 |
| TAR.XZ | 最高 | 慢 | 长期归档 |

---

## 🔒 安全注意事项

1. **路径遍历攻击** - 解压时注意检查文件路径，避免解压到预期目录之外
2. **压缩炸弹** - 解压前检查压缩比，避免极端压缩比导致资源耗尽
3. **内存使用** - 大文件建议使用流式处理而非一次性加载

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
