# Archive Utils 📦

**Python 归档压缩工具库**

零依赖、生产就绪的归档和压缩工具，支持 ZIP、TAR、GZIP、BZ2、XZ 等多种格式。

---

## ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **多格式支持** - ZIP, TAR, TAR.GZ, TAR.BZ2, TAR.XZ, GZ, BZ2, XZ
- **完整功能** - 创建、解压、列表、验证、校验和
- **智能检测** - 自动识别归档格式
- **压缩控制** - 支持多级压缩设置
- **流式提取** - 支持单文件提取无需解压全部
- **归档管理** - 支持添加/删除 ZIP 成员

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cd alltoolkit/Python/archive_utils
```

---

## 🚀 快速开始

### 基本使用

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

# 创建 ZIP 归档
result = utils.create_archive("backup.zip", ["file1.txt", "dir/"])
print(result.success)  # True

# 解压归档
result = utils.extract_archive("backup.zip", "output/")
print(result.files_processed)  # 解压的文件数

# 列出内容
members = utils.list_archive("backup.zip")
for m in members:
    print(f"{m.name}: {m.size} bytes")

# 获取归档信息
info = utils.get_archive_info("backup.zip")
print(f"格式：{info.format.value}")
print(f"文件数：{info.file_count}")
print(f"压缩率：{info.compression_ratio:.2%}")
```

### 模块级函数

```python
from archive_utils.mod import (
    create_archive,
    extract_archive,
    list_archive,
    get_archive_info,
    verify_archive,
    calculate_checksum,
)

# 直接使用
result = create_archive("data.zip", ["file1.txt", "file2.txt"])
members = list_archive("data.zip")
info = get_archive_info("data.zip")
valid = verify_archive("data.zip")
checksum = calculate_checksum("data.zip")
```

---

## 📖 API 参考

### ArchiveUtils 类

#### 格式检测

| 方法 | 描述 | 返回 |
|------|------|------|
| `detect_format(path)` | 从文件路径检测归档格式 | `Optional[ArchiveFormat]` |

#### 创建归档

| 方法 | 描述 | 返回 |
|------|------|------|
| `create_archive(output_path, source_paths, format, compression, password, base_dir)` | 创建归档文件 | `ArchiveOperationResult` |

参数说明：
- `output_path`: 输出文件路径
- `source_paths`: 要归档的文件/目录列表
- `format`: 归档格式（可选，默认从扩展名检测）
- `compression`: 压缩级别（可选，默认 DEFAULT）
- `password`: ZIP 密码（可选）
- `base_dir`: 相对路径基准目录（可选）

#### 解压归档

| 方法 | 描述 | 返回 |
|------|------|------|
| `extract_archive(archive_path, output_dir, password, members)` | 解压归档 | `ArchiveOperationResult` |

参数说明：
- `archive_path`: 归档文件路径
- `output_dir`: 输出目录（默认当前目录）
- `password`: 密码（可选）
- `members`: 指定要解压的成员（None=全部）

#### 列表与信息

| 方法 | 描述 | 返回 |
|------|------|------|
| `list_archive(archive_path)` | 列出归档内容 | `List[ArchiveMember]` |
| `get_archive_info(archive_path)` | 获取归档详细信息 | `ArchiveInfo` |

#### 归档管理

| 方法 | 描述 | 返回 |
|------|------|------|
| `add_to_archive(archive_path, source_paths, base_dir)` | 添加文件到归档（仅 ZIP） | `ArchiveOperationResult` |
| `remove_from_archive(archive_path, member_paths)` | 从归档删除文件（仅 ZIP） | `ArchiveOperationResult` |

#### 验证与校验

| 方法 | 描述 | 返回 |
|------|------|------|
| `verify_archive(archive_path)` | 验证归档完整性 | `ArchiveOperationResult` |
| `calculate_checksum(archive_path, algorithm)` | 计算校验和 | `str` |

#### 流式操作

| 方法 | 描述 | 返回 |
|------|------|------|
| `stream_extract(archive_path, member_path, output_path)` | 流式提取单个成员 | `ArchiveOperationResult` |

---

## 📊 数据结构

### ArchiveFormat

支持的归档格式：

```python
class ArchiveFormat(Enum):
    ZIP = "zip"
    TAR = "tar"
    TAR_GZ = "tar.gz"
    TAR_BZ2 = "tar.bz2"
    TAR_XZ = "tar.xz"
    GZ = "gz"
    BZ2 = "bz2"
    XZ = "xz"
```

### CompressionLevel

压缩级别：

```python
class CompressionLevel(Enum):
    FASTEST = 1   # 最快，压缩率最低
    FAST = 3      # 快速
    DEFAULT = 6   # 默认平衡
    BEST = 9      # 最佳压缩率
```

### ArchiveInfo

归档详细信息：

```python
@dataclass
class ArchiveInfo:
    path: str                    # 文件路径
    format: ArchiveFormat        # 格式
    size: int                    # 文件大小（字节）
    file_count: int              # 文件数量
    files: List[str]             # 文件列表
    created: Optional[datetime]  # 创建时间
    modified: Optional[datetime] # 修改时间
    compressed_size: int         # 压缩后大小
    uncompressed_size: int       # 原始大小
    compression_ratio: float     # 压缩率
```

### ArchiveMember

归档成员信息：

```python
@dataclass
class ArchiveMember:
    name: str              # 文件名
    size: int              # 原始大小
    compressed_size: int   # 压缩后大小
    is_dir: bool           # 是否为目录
    modified: datetime     # 修改时间
    crc32: Optional[int]   # CRC32 校验值
    permissions: Optional[int]  # 权限
```

### ArchiveOperationResult

操作结果：

```python
@dataclass
class ArchiveOperationResult:
    success: bool          # 是否成功
    message: str           # 消息
    files_processed: int   # 处理文件数
    bytes_processed: int   # 处理字节数
    errors: List[str]      # 错误列表
```

---

## 💡 使用示例

### 1. 创建备份归档

```python
from archive_utils.mod import ArchiveUtils, CompressionLevel

utils = ArchiveUtils()

# 创建高压缩率备份
result = utils.create_archive(
    "backup.zip",
    ["documents/", "photos/", "config.json"],
    compression=CompressionLevel.BEST
)

if result.success:
    print(f"备份完成：{result.files_processed} 个文件")
else:
    print(f"备份失败：{result.errors}")
```

### 2. 解压特定文件

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

# 只解压配置文件
result = utils.extract_archive(
    "backup.zip",
    "restored/",
    members=["config.json", "settings.ini"]
)

print(f"解压了 {result.files_processed} 个文件")
```

### 3. 归档分析与报告

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

archives = ["backup1.zip", "backup2.tar.gz", "data.tar.bz2"]

for archive in archives:
    info = utils.get_archive_info(archive)
    print(f"\n{archive}:")
    print(f"  格式：{info.format.value}")
    print(f"  文件数：{info.file_count}")
    print(f"  原始大小：{info.uncompressed_size / 1024:.1f} KB")
    print(f"  压缩大小：{info.compressed_size / 1024:.1f} KB")
    print(f"  压缩率：{info.compression_ratio:.1%}")
```

### 4. 验证与校验

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

archive = "important_data.zip"

# 验证完整性
verify_result = utils.verify_archive(archive)
if verify_result.success:
    print("✓ 归档完整性验证通过")
else:
    print(f"✗ 验证失败：{verify_result.errors}")

# 计算多种校验和
algorithms = ['md5', 'sha1', 'sha256']
for algo in algorithms:
    checksum = utils.calculate_checksum(archive, algo)
    print(f"{algo.upper()}: {checksum}")
```

### 5. 流式提取大文件

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

# 从大型归档中提取单个文件，无需解压全部
result = utils.stream_extract(
    "large_archive.zip",
    "path/to/specific/file.txt",
    "output/file.txt"
)

if result.success:
    print(f"提取完成：{result.bytes_processed} 字节")
```

### 6. 增量备份（添加文件）

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

# 向现有 ZIP 添加新文件
result = utils.add_to_archive(
    "backup.zip",
    ["new_file.txt", "updated_config.json"]
)

print(f"添加了 {result.files_processed} 个文件")
```

### 7. 清理归档（删除文件）

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

# 从 ZIP 中删除临时文件
result = utils.remove_from_archive(
    "backup.zip",
    ["temp/cache.dat", "logs/old.log"]
)

print(f"删除了 {result.files_processed} 个文件")
```

### 8. 多格式转换

```python
from archive_utils.mod import ArchiveUtils, ArchiveFormat

utils = ArchiveUtils()
import tempfile
import os

# ZIP → TAR.GZ 转换
with tempfile.TemporaryDirectory() as tmpdir:
    # 先解压
    utils.extract_archive("source.zip", tmpdir)
    
    # 再打包为 TAR.GZ
    utils.create_archive(
        "output.tar.gz",
        [os.path.join(tmpdir, f) for f in os.listdir(tmpdir)]
    )

print("格式转换完成！")
```

---

## 🧪 测试

运行测试套件：

```bash
cd /path/to/AllToolkit/Python/archive_utils
python archive_utils_test.py
```

测试覆盖：

- ✅ 格式检测（所有支持格式）
- ✅ ZIP 创建与解压
- ✅ TAR/TAR.GZ/TAR.BZ2/TAR.XZ 操作
- ✅ GZ/BZ2/XZ 单文件压缩
- ✅ 归档列表与信息
- ✅ 完整性验证
- ✅ 校验和计算
- ✅ 错误处理
- ✅ 模块级函数
- ✅ 压缩级别测试

---

## 📁 文件结构

```
archive_utils/
├── mod.py                      # 主模块
├── archive_utils_test.py       # 测试套件
├── README.md                   # 本文档
└── examples/
    └── usage_examples.py       # 使用示例
```

---

## 🔧 高级用法

### 自定义压缩级别

```python
from archive_utils.mod import ArchiveUtils, CompressionLevel

utils = ArchiveUtils()

# 最快压缩（适合临时文件）
utils.create_archive("temp.zip", ["data/"], compression=CompressionLevel.FASTEST)

# 最佳压缩（适合长期存储）
utils.create_archive("archive.zip", ["data/"], compression=CompressionLevel.BEST)
```

### 批量处理多个归档

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

archives = ["backup1.zip", "backup2.zip", "backup3.zip"]
results = []

for archive in archives:
    info = utils.get_archive_info(archive)
    results.append({
        'name': archive,
        'files': info.file_count,
        'ratio': info.compression_ratio
    })

# 生成报告
for r in results:
    print(f"{r['name']}: {r['files']} files, {r['ratio']:.1%} compression")
```

### 安全验证

```python
from archive_utils.mod import ArchiveUtils

utils = ArchiveUtils()

def safe_extract(archive_path, output_dir, expected_checksum=None):
    """安全解压：先验证再解压"""
    # 验证完整性
    verify_result = utils.verify_archive(archive_path)
    if not verify_result.success:
        return False, f"验证失败：{verify_result.errors}"
    
    # 验证校验和
    if expected_checksum:
        actual = utils.calculate_checksum(archive_path)
        if actual != expected_checksum:
            return False, "校验和不匹配"
    
    # 执行解压
    result = utils.extract_archive(archive_path, output_dir)
    return result.success, result.message

# 使用
success, msg = safe_extract("downloaded.zip", "output/", 
                           "abc123...")
```

---

## 📝 注意事项

1. **ZIP 密码**: Python 标准库对加密 ZIP 支持有限，建议使用其他工具进行加密
2. **符号链接**: TAR 格式保留符号链接，ZIP 会存储为普通文件
3. **大文件**: 对于超大归档，建议使用 `stream_extract` 避免内存问题
4. **权限**: TAR 保留文件权限，ZIP 权限信息可能丢失
5. **兼容性**: Python 3.8+（使用 walrus operator）

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 报告 Bug
- 请求新功能
- 改进文档
- 添加测试用例

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🔗 相关链接

- [AllToolkit 主项目](../../README.md)
- [Python 工具列表](../README.md)
- [Python zipfile 文档](https://docs.python.org/3/library/zipfile.html)
- [Python tarfile 文档](https://docs.python.org/3/library/tarfile.html)

---

**最后更新**: 2026-04-11
