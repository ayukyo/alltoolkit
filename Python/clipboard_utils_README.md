# Clipboard Utils - 剪贴板工具

跨平台剪贴板操作工具库，支持文本和文件路径的复制粘贴。

## 功能特性

- ✅ 跨平台支持（Windows/macOS/Linux）
- ✅ 文本复制粘贴
- ✅ 文件路径复制
- ✅ 多文件路径列表复制
- ✅ 剪贴板清空
- ✅ 剪贴板可用性检测
- ✅ Python 3.6+ 兼容
- ✅ 零外部依赖

## 安装

无需安装，直接复制 `clipboard_utils.py` 到项目即可使用。

```bash
# 可选：Linux 系统安装剪贴板工具
sudo apt install xclip    # 或
sudo apt install xsel     # 或
sudo apt install wl-clipboard
```

## 快速开始

```python
from clipboard_utils import copy_text, paste_text

# 复制文本
copy_text("Hello, World!")

# 粘贴文本
content = paste_text()
print(content)  # 输出：Hello, World!
```

## API 参考

### 核心函数

#### `copy_text(text: str) -> bool`
复制文本到剪贴板。

```python
success = copy_text("要复制的内容")
```

#### `paste_text() -> Optional[str]`
从剪贴板粘贴文本。

```python
content = paste_text()
if content:
    print("剪贴板内容:", content)
```

#### `clear_clipboard() -> bool`
清空剪贴板。

```python
clear_clipboard()
```

### 文件路径函数

#### `copy_file_path(filepath: str) -> bool`
复制文件的绝对路径到剪贴板。

```python
copy_file_path("document.pdf")
copy_file_path("/home/user/data/config.json")
```

#### `copy_files_list(filepaths: List[str], separator: str = '\n') -> bool`
复制多个文件路径到剪贴板。

```python
files = ["file1.txt", "file2.txt", "file3.txt"]
copy_files_list(files)  # 换行分隔
copy_files_list(files, separator=', ')  # 逗号分隔
```

### 工具函数

#### `is_clipboard_available() -> bool`
检测剪贴板是否可用。

```python
if is_clipboard_available():
    copy_text("Hello")
else:
    print("剪贴板不可用")
```

#### `get_platform_info() -> dict`
获取平台信息。

```python
info = get_platform_info()
print("平台:", info['platform'])
print("工具:", info['tools'])
print("可用:", info['available'])
```

#### `get_clipboard_history(max_items: int = 10) -> List[str]`
获取剪贴板历史（如果系统支持）。

```python
history = get_clipboard_history()
for item in history:
    print(item)
```

## 跨平台说明

### Windows
- 使用 `clip.exe` 和 PowerShell
- 默认可用，无需额外安装

### macOS
- 使用 `pbcopy` 和 `pbpaste`
- 默认可用，无需额外安装

### Linux
- 支持 `xclip`、`xsel`、`wl-clipboard`
- 需要安装至少一个工具：
  ```bash
  sudo apt install xclip
  # 或
  sudo apt install xsel
  # 或（Wayland）
  sudo apt install wl-clipboard
  ```

## 使用示例

### 场景 1：快速复制代码
```python
code = """
def hello():
    print("Hello, World!")
"""
copy_text(code)
```

### 场景 2：分享文件列表
```python
project_files = [
    "src/main.py",
    "tests/test_main.py",
    "README.md"
]
copy_files_list(project_files)
```

### 场景 3：安全复制（先检查可用性）
```python
if is_clipboard_available():
    copy_text("敏感信息")
else:
    print("剪贴板不可用，请手动复制")
```

## 运行测试

```bash
cd Python
python clipboard_utils_test.py
```

## 运行示例

```bash
cd Python
python examples/clipboard_utils_example.py
```

## 注意事项

1. **无头环境**：在无图形界面的服务器或 Docker 容器中，剪贴板可能不可用
2. **Wayland**：在 Wayland 显示服务器上，需要使用 `wl-clipboard`
3. **超时处理**：所有操作都有 5 秒超时保护
4. **Unicode 支持**：完全支持 Unicode 和 Emoji 字符

## 许可证

MIT License - AllToolkit

## 版本

- Version: 1.0.0
- Author: AllToolkit
- Python: 3.6+
