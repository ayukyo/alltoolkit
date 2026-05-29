# batch_rename_utils - 批量文件重命名工具模块

提供多种批量重命名策略，包括序号命名、前缀后缀、正则替换、大小写转换等。
零外部依赖，纯 Python 标准库实现。

## 功能列表

| 功能 | 说明 |
|------|------|
| `add_prefix()` | 为文件名添加前缀 |
| `add_suffix()` | 为文件名添加后缀（支持扩展名前/后） |
| `remove_prefix()` | 移除文件名前缀 |
| `remove_suffix()` | 移除文件名后缀 |
| `replace_text()` | 替换文件名中的文本 |
| `regex_replace()` | 使用正则表达式替换文件名 |
| `change_case()` | 更改文件名大小写（lower/upper/title/capitalize/swap） |
| `sequential_rename()` | 序号重命名（如 photo_001.jpg, photo_002.jpg） |
| `datetime_rename()` | 使用日期时间重命名 |
| `change_extension()` | 更改文件扩展名 |
| `custom_rename()` | 自定义重命名函数 |
| `batch_rename()` | 批量执行多个重命名操作 |
| `undo_rename()` | 撤销重命名操作 |
| `get_files_by_pattern()` | 按模式获取文件列表 |

## 快速开始

### 添加前缀/后缀

```python
from batch_rename_utils import add_prefix, add_suffix, remove_prefix

# 预览（不执行）
previews = add_prefix(['a.txt', 'b.txt'], 'new_', preview=True)
for p in previews:
    print(p)  # 'a.txt' -> 'new_a.txt'

# 执行重命名
results = add_prefix(['photo.jpg'], 'IMG_')
print(results[0].success)  # True

# 添加后缀
previews = add_suffix(['data.txt'], '_backup', preview=True)
# data.txt -> data_backup.txt

# 在扩展名后添加
previews = add_suffix(['data.txt'], '.bak', before_ext=False, preview=True)
# data.txt -> data.txt.bak

# 移除前缀
results = remove_prefix(['prefix_file.txt'], 'prefix_')
# prefix_file.txt -> file.txt
```

### 文本替换

```python
from batch_rename_utils import replace_text, regex_replace

# 简单文本替换
previews = replace_text(['old_file.txt'], 'old', 'new', preview=True)
# old_file.txt -> new_file.txt

# 正则表达式替换
previews = regex_replace(['IMG_1234.jpg'], r'IMG_(\d+)', r'Photo_\1', preview=True)
# IMG_1234.jpg -> Photo_1234.jpg

# 大小写不敏感
import re
previews = regex_replace(['TEST_FILE.txt'], r'test', 'demo', 
                         flags=re.IGNORECASE, preview=True)
# TEST_FILE.txt -> demo_FILE.txt
```

### 大小写转换

```python
from batch_rename_utils import change_case

# 转小写
previews = change_case(['HELLO.txt'], 'lower', preview=True)
# HELLO.txt -> hello.txt

# 转大写
previews = change_case(['hello.txt'], 'upper', preview=True)
# hello.txt -> HELLO.TXT

# 标题化
previews = change_case(['hello world.txt'], 'title', preview=True)
# hello world.txt -> Hello World.Txt

# 大小写互换
previews = change_case(['HeLLo.txt'], 'swap', preview=True)
# HeLLo.txt -> hEllO.TXT
```

### 序号重命名

```python
from batch_rename_utils import sequential_rename

files = ['a.jpg', 'b.jpg', 'c.jpg']

# 默认序号（3位数）
previews = sequential_rename(files, 'photo', preview=True)
# photo_001.jpg, photo_002.jpg, photo_003.jpg

# 自定义参数
previews = sequential_rename(
    files, 
    base_name='IMG',
    start=10,          # 起始序号
    digits=4,          # 位数
    separator='-',     # 分隔符
    preview=True
)
# IMG-0010.jpg, IMG-0011.jpg, IMG-0012.jpg

# 不保留扩展名
previews = sequential_rename(files, 'data', keep_ext=False, preview=True)
# data_001, data_002, data_003
```

### 日期时间重命名

```python
from batch_rename_utils import datetime_rename

# 默认格式
previews = datetime_rename(['photo.jpg'], preview=True)
# 20260529_170000.jpg

# 自定义格式
previews = datetime_rename(
    ['photo.jpg'],
    format_str='%Y-%m-%d',
    prefix='IMG_',
    preview=True
)
# IMG_2026-05-29.jpg

# 带后缀
previews = datetime_rename(
    ['photo.jpg'],
    format_str='%Y%m%d',
    suffix='_backup',
    preview=True
)
# 20260529_backup.jpg
```

### 更改扩展名

```python
from batch_rename_utils import change_extension

previews = change_extension(['data.txt'], '.md', preview=True)
# data.txt -> data.md

# 不带点也可以
previews = change_extension(['data.txt'], 'json', preview=True)
# data.txt -> data.json
```

### 自定义重命名

```python
from batch_rename_utils import custom_rename

def my_rename(path):
    # 大写文件名 + MD5 后缀
    import hashlib
    h = hashlib.md5(path.stem.encode()).hexdigest()[:8]
    return f"{path.stem.upper()}_{h}{path.suffix}"

previews = custom_rename(['test.txt'], my_rename, preview=True)
# test.txt -> TEST_098f6bcd.txt
```

### 批量操作

```python
from batch_rename_utils import batch_rename

# 一次执行多个操作
operations = [
    {'type': 'prefix', 'value': 'IMG_'},
    {'type': 'case', 'mode': 'lower'},
    {'type': 'suffix', 'value': '_backup'}
]

previews = batch_rename(['TEST.txt'], operations, preview=True)
# TEST.txt -> img_test_backup.txt
```

### 撤销操作

```python
from batch_rename_utils import add_prefix, undo_rename

# 执行重命名
results = add_prefix(['file.txt'], 'new_')

# 撤销
undo_results = undo_rename(results)
# new_file.txt -> file.txt
```

### 获取文件列表

```python
from batch_rename_utils import get_files_by_pattern

# 获取当前目录所有 txt 文件
files = get_files_by_pattern('.', '*.txt')

# 递归获取
files = get_files_by_pattern('./photos', 'IMG_*.jpg', recursive=True)
```

## 预览模式

所有重命名函数都支持 `preview=True` 参数，只返回预览结果而不实际执行：

```python
# 预览
previews = add_prefix(['a.txt'], 'new_', preview=True)
for p in previews:
    print(f"{p.old_name} -> {p.new_name}")

# 执行
results = add_prefix(['a.txt'], 'new_')
for r in results:
    if r.success:
        print(f"成功: {r.old_path.name} -> {r.new_path.name}")
    else:
        print(f"失败: {r.error}")
```

## 冲突处理

当重命名目标已存在时，模块会自动处理冲突：

```python
# 如果 new_file.txt 已存在，会自动重命名为 new_file_1.txt
results = add_prefix(['file.txt'], 'new_')
```

## 测试覆盖

- **52 个单元测试，100% 通过率**
- 测试内容：
  - 所有重命名操作的预览和执行
  - 边界情况（空列表、Unicode 文件名、特殊字符）
  - 冲突处理
  - 撤销操作
  - 批量操作
  - 错误处理

## API 参考

### `add_prefix(paths, prefix, preview=False)`

为文件名添加前缀。

**参数：**
- `paths`: 文件路径列表
- `prefix`: 要添加的前缀
- `preview`: 是否只预览不执行

**返回：**
- 预览模式：`List[RenamePreview]`
- 执行模式：`List[RenameResult]`

### `sequential_rename(paths, base_name, start=1, digits=3, separator='_', keep_ext=True, preview=False)`

序号重命名文件。

**参数：**
- `paths`: 文件路径列表
- `base_name`: 基础文件名
- `start`: 起始序号，默认 1
- `digits`: 序号位数，默认 3
- `separator`: 分隔符，默认 '_'
- `keep_ext`: 是否保留原扩展名，默认 True
- `preview`: 是否只预览不执行

### `batch_rename(paths, operations, preview=False)`

批量执行多个重命名操作。

**支持的操作类型：**
- `{'type': 'prefix', 'value': 'xxx'}` - 添加前缀
- `{'type': 'suffix', 'value': 'xxx', 'before_ext': True}` - 添加后缀
- `{'type': 'replace', 'old': 'xxx', 'new': 'yyy'}` - 文本替换
- `{'type': 'regex', 'pattern': r'xxx', 'replacement': 'yyy'}` - 正则替换
- `{'type': 'case', 'mode': 'lower'}` - 大小写转换
- `{'type': 'extension', 'value': '.md'}` - 更改扩展名

## 许可证

MIT License