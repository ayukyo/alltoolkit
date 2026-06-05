# File Utils - 文件工具

全面的文件处理工具库，支持读写、复制、移动、删除、哈希计算等操作。

## 功能特性

- ✅ 安全的文件读写（编码检测、错误处理）
- ✅ 文件哈希计算（MD5/SHA1/SHA256/SHA512）
- ✅ 文件信息获取（大小、哈希）
- ✅ 目录操作（创建、列表）
- ✅ 文件复制和移动
- ✅ 文件名去重
- ✅ 跨平台支持
- ✅ 零外部依赖

## 安装

无需安装，直接复制 `file_utils.py` 到项目即可使用。

```bash
# Python 3.6+ 内置，无需额外依赖
```

## 快速开始

```python
from file_utils import safe_read_text, safe_write_text, get_file_hash

# 安全读取文件
content = safe_read_text("config.json")
if content is None:
    print("读取失败")

# 安全写入文件
success = safe_write_text("output.txt", "Hello, World!")
if success:
    print("写入成功")

# 计算文件哈希
md5_hash = get_file_hash("document.pdf", algorithm="md5")
sha256_hash = get_file_hash("document.pdf", algorithm="sha256")
```

## API 参考

### 读写函数

#### `safe_read_text(filepath: PathLike, encoding: str = 'utf-8', default: Optional[str] = None) -> Optional[str]`
安全读取文本文件。

```python
# 基本用法
content = safe_read_text("data.txt")

# 指定编码
content = safe_read_text("data.txt", encoding="gbk")

# 自定义失败返回值
content = safe_read_text("nonexistent.txt", default="fallback")

# 使用 Path 对象
from pathlib import Path
content = safe_read_text(Path("data.txt"))
```

#### `safe_write_text(filepath: PathLike, content: str, encoding: str = 'utf-8', append: bool = False) -> bool`
安全写入文本文件。

```python
# 覆写文件
safe_write_text("output.txt", "Hello")

# 追加内容
safe_write_text("log.txt", "new log entry\n", append=True)

# 指定编码
safe_write_text("output.txt", "中文内容", encoding="gbk")
```

### 哈希函数

#### `get_file_hash(filepath: PathLike, algorithm: str = 'md5', chunk_size: int = 8192) -> Optional[str]`
计算文件哈希值。

```python
# MD5（默认）
md5 = get_file_hash("file.txt")

# SHA1
sha1 = get_file_hash("file.txt", algorithm="sha1")

# SHA256
sha256 = get_file_hash("file.txt", algorithm="sha256")

# SHA512
sha512 = get_file_hash("file.txt", algorithm="sha512")

# 自定义块大小（大文件优化）
hash_val = get_file_hash("large_file.bin", chunk_size=65536)
```

### 文件信息函数

#### `get_file_size(filepath: PathLike, human_readable: bool = False, decimal_places: int = 2) -> Union[int, str, None]`
获取文件大小。

```python
# 字节为单位
size = get_file_size("video.mp4")  # 1048576

# 人类可读格式
size_str = get_file_size("video.mp4", human_readable=True)  # "1.00 MB"
size_str = get_file_size("video.mp4", human_readable=True, decimal_places=1)  # "1.0 MB"
```

### 目录函数

#### `ensure_dir(directory: PathLike, mode: int = 0o755) -> bool`
确保目录存在（不存在则创建）。

```python
# 创建单层目录
ensure_dir("./output")

# 创建多层目录
ensure_dir("./output/subdir/nested")

# 自定义权限
ensure_dir("./protected", mode=0o700)
```

#### `list_files(directory: PathLike, pattern: str = '*', recursive: bool = False, sort: bool = True) -> List[str]`
列出目录中的文件。

```python
# 列出当前目录所有文件
files = list_files("./data")

# 列出特定扩展名的文件
py_files = list_files("./src", pattern="*.py")

# 递归列出所有文件
all_files = list_files("./project", recursive=True)

# 排除排序
files = list_files("./data", sort=False)
```

### 复制移动函数

#### `copy_file(src: PathLike, dst: PathLike, overwrite: bool = False) -> bool`
复制文件。

```python
# 基本复制
copy_file("source.txt", "dest.txt")

# 覆盖已存在的文件
copy_file("source.txt", "dest.txt", overwrite=True)
```

#### `move_file(src: PathLike, dst: PathLike, overwrite: bool = False) -> bool`
移动或重命名文件。

```python
# 重命名文件
move_file("old_name.txt", "new_name.txt")

# 移动文件到目录
move_file("file.txt", "./backup/file.txt")

# 覆盖已存在的目标文件
move_file("file.txt", "existing.txt", overwrite=True)
```

### 删除函数

#### `delete_file(filepath: PathLike, missing_ok: bool = True) -> bool`
删除文件。

```python
# 删除文件（文件不存在不报错）
delete_file("temp.txt")

# 文件不存在时报错
delete_file("temp.txt", missing_ok=False)
```

### 工具函数

#### `get_unique_filename(filepath: PathLike, suffix_format: str = '_{}') -> Path`
获取不重复的文件名（避免覆盖）。

```python
# 文件名不冲突，直接返回原路径
unique = get_unique_filename("report.pdf")  # Path("report.pdf")

# 文件名已存在，自动添加后缀
unique = get_unique_filename("report.pdf")  # Path("report_1.pdf")
unique = get_unique_filename("report.pdf")  # Path("report_2.pdf")
unique = get_unique_filename("report.pdf")  # Path("report_3.pdf")

# 自定义后缀格式
unique = get_unique_filename("report.pdf", suffix_format="({})")  # Path("report(1).pdf")
```

## 使用示例

### 场景 1：备份目录中的所有文件
```python
import os
from file_utils import copy_file, list_files, ensure_dir

backup_dir = "./backup"
ensure_dir(backup_dir)

for file in list_files("./data", pattern="*.txt"):
    filename = os.path.basename(file)
    copy_file(file, os.path.join(backup_dir, filename))
```

### 场景 2：计算目录中所有文件的哈希
```python
from file_utils import get_file_hash

for file in list_files("./downloads", pattern="*.iso", recursive=True):
    md5 = get_file_hash(file)
    print(f"{file}: {md5}")
```

### 场景 3：安全的配置文件读写
```python
from file_utils import safe_read_text, safe_write_text
import json

CONFIG_FILE = "config.json"

def load_config():
    content = safe_read_text(CONFIG_FILE)
    if content is None:
        return {}
    return json.loads(content)

def save_config(config):
    safe_write_text(CONFIG_FILE, json.dumps(config, indent=2))
```

## 运行测试

```bash
cd Python
python file_utils_test.py
```

## 注意事项

1. **编码检测**：读取时自动尝试 UTF-8 和 GBK 编码
2. **大文件处理**：哈希计算使用流式读取，内存占用低
3. **路径兼容**：支持字符串和 Path 对象
4. **线程安全**：所有操作都是原子的

## 许可证

MIT License - AllToolkit

## 版本

- Version: 1.0.0
- Author: AllToolkit
- Python: 3.6+