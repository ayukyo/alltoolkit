# File Utils 📁

**Lua 文件操作工具函数库**

零依赖、生产就绪的文件路径处理、读写操作、目录管理工具。

---

## ✨ 特性

- **零依赖** - 仅使用 Lua 标准库
- **全面路径处理** - 规范化、拼接、解析、相对路径计算
- **文件读写** - 文本/二进制读写、追加、复制
- **文件信息** - 存在检查、大小获取、MIME 类型识别
- **目录操作** - 创建、列出、递归遍历、删除
- **文件搜索** - 内容搜索、模式匹配查找
- **临时文件** - 安全生成临时文件和目录
- **数据序列化** - Lua 表保存/加载

---

## 📦 安装

无需安装！直接复制 `mod.lua` 到你的项目即可使用。

```bash
# 从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cd alltoolkit/Lua/file_utils

# 或直接复制
cp mod.lua your_project/file_utils.lua
```

---

## 🚀 快速开始

### 基础使用

```lua
local FileUtils = require("file_utils")

-- 路径处理
local path = FileUtils.join("/home", "user", "documents", "file.txt")
-- /home/user/documents/file.txt

local dir = FileUtils.get_directory(path)
-- /home/user/documents

local filename = FileUtils.get_filename(path)
-- file.txt

local ext = FileUtils.get_extension(path)
-- .txt

local basename = FileUtils.get_basename(path)
-- file

-- 规范化路径
local normalized = FileUtils.normalize_path("/a/b/../c/./d")
-- /a/c/d
```

### 文件读写

```lua
-- 读取整个文件
local content, err = FileUtils.read_file("config.txt")
if content then
    print("文件内容：" .. content)
end

-- 读取文件的行
local lines, err = FileUtils.read_lines("data.txt")
for i, line in ipairs(lines) do
    print("第 " .. i .. " 行：" .. line)
end

-- 写入文件（覆盖）
local success, err = FileUtils.write_file("output.txt", "Hello, World!")

-- 追加内容
local success, err = FileUtils.append_file("log.txt", "\n新日志行")

-- 复制文件
local success, err = FileUtils.copy_file("source.txt", "destination.txt")
```

### 文件信息

```lua
-- 检查文件是否存在
if FileUtils.exists("config.txt") then
    print("文件存在")
end

-- 获取文件大小
local size, err = FileUtils.get_file_size("large_file.zip")
print("文件大小：" .. FileUtils.format_file_size(size))
-- 输出：文件大小：1.50 MB

-- 获取 MIME 类型
local mime = FileUtils.get_mime_type("document.pdf")
-- application/pdf
```

### 目录操作

```lua
-- 创建目录（包括父目录）
local success, err = FileUtils.create_directory("/path/to/new/dir")

-- 列出目录内容
local entries, err = FileUtils.list_directory("/home/user")
for i, entry in ipairs(entries) do
    print(entry)
end

-- 递归列出目录
local all_files, err = FileUtils.list_directory_recursive("/project", {
    recursive = true,
    include_files = true,
    include_dirs = false
})

-- 删除空目录
local success, err = FileUtils.remove_directory("/empty/dir")
```

### 文件搜索

```lua
-- 在文件中搜索内容
local matches, err = FileUtils.search_in_file("source.lua", "function")
for _, match in ipairs(matches) do
    print("第 " .. match.line_number .. " 行：" .. match.content)
end

-- 在目录中查找文件
local files, err = FileUtils.find_files("/project", "*.lua", true)
for i, file in ipairs(files) do
    print(file)
end

-- 批量删除文件
local count, err = FileUtils.delete_files_by_pattern("*.tmp", "/tmp")
print("删除了 " .. count .. " 个文件")
```

### 临时文件

```lua
-- 生成临时文件名
local temp_name = FileUtils.temp_name("backup", "txt")
-- backup_1712851200_12345.txt

-- 创建临时文件
local temp_path, err = FileUtils.create_temp_file("cache", "initial content")
print("临时文件：" .. temp_path)

-- 使用后清理
FileUtils.delete_file(temp_path)
```

### 数据序列化

```lua
-- 保存 Lua 表到文件
local data = {
    name = "Project",
    version = "1.0.0",
    dependencies = {"lua", "luv"},
    config = {debug = true, port = 8080}
}

local success, err = FileUtils.save_table("config.lua", data, true)

-- 从文件加载 Lua 表
local loaded_data, err = FileUtils.load_table("config.lua")
print(loaded_data.name)        -- Project
print(loaded_data.version)     -- 1.0.0
print(loaded_data.config.port) -- 8080
```

---

## 📚 API 参考

### 路径处理

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `normalize_path(path)` | 规范化路径（处理 `../` 和 `./`） | `path: string` | `string` |
| `get_directory(path)` | 获取路径的目录部分 | `path: string` | `string` |
| `get_filename(path)` | 获取路径的文件名部分 | `path: string` | `string` |
| `get_extension(path)` | 获取文件扩展名（带点） | `path: string` | `string` |
| `get_basename(path)` | 获取不含扩展名的文件名 | `path: string` | `string` |
| `join(...)` | 拼接多个路径片段 | `...: string` | `string` |
| `is_absolute(path)` | 检查是否为绝对路径 | `path: string` | `boolean` |
| `relative_path(base, target)` | 获取相对路径 | `base: string, target: string` | `string` |

### 文件读取

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `read_file(path)` | 读取整个文件内容 | `path: string` | `string?, error?` |
| `read_lines(path)` | 读取文件的行 | `path: string` | `table, error?` |
| `read_binary(path)` | 读取二进制内容 | `path: string` | `string?, error?` |

### 文件写入

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `write_file(path, content)` | 写入文件（覆盖） | `path: string, content: string` | `boolean, error?` |
| `append_file(path, content)` | 追加内容到文件 | `path: string, content: string` | `boolean, error?` |
| `write_binary(path, content)` | 写入二进制内容 | `path: string, content: string` | `boolean, error?` |
| `copy_file(src, dst)` | 复制文件 | `src: string, dst: string` | `boolean, error?` |

### 文件信息

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `exists(path)` | 检查文件是否存在 | `path: string` | `boolean` |
| `is_directory(path)` | 检查是否为目录 | `path: string` | `boolean` |
| `get_file_size(path)` | 获取文件大小（字节） | `path: string` | `number?, error?` |
| `format_file_size(size)` | 格式化文件大小 | `size: number` | `string` |
| `get_mime_type(path)` | 获取 MIME 类型 | `path: string` | `string` |
| `is_readable(path)` | 检查文件是否可读 | `path: string` | `boolean` |
| `is_writable(path)` | 检查文件是否可写 | `path: string` | `boolean` |
| `get_file_hash(path, algo)` | 获取文件哈希值 | `path: string, algo: string` | `string?, error?` |

### 目录操作

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `create_directory(path)` | 创建目录（包括父目录） | `path: string` | `boolean, error?` |
| `list_directory(path)` | 列出目录内容 | `path: string` | `table, error?` |
| `list_directory_recursive(path, opts)` | 递归列出目录 | `path: string, opts: table` | `table, error?` |
| `remove_directory(path)` | 删除空目录 | `path: string` | `boolean, error?` |

### 文件操作

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `delete_file(path)` | 删除文件 | `path: string` | `boolean, error?` |
| `rename_file(old, new)` | 重命名/移动文件 | `old: string, new: string` | `boolean, error?` |
| `delete_files_by_pattern(pattern, dir)` | 批量删除匹配的文件 | `pattern: string, dir: string` | `number, error?` |

### 临时文件

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `temp_name(prefix, ext)` | 生成临时文件名 | `prefix: string, ext: string` | `string` |
| `create_temp_file(prefix, content)` | 创建临时文件 | `prefix: string, content: string` | `string?, error?` |

### 文件搜索

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `search_in_file(path, pattern)` | 在文件中搜索内容 | `path: string, pattern: string` | `table, error?` |
| `find_files(dir, pattern, recursive)` | 在目录中查找文件 | `dir: string, pattern: string, recursive: boolean` | `table, error?` |

### 工具函数

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `load_table(path)` | 加载 Lua 表文件 | `path: string` | `table?, error?` |
| `save_table(path, data, pretty)` | 保存 Lua 表到文件 | `path: string, data: table, pretty: boolean` | `boolean, error?` |
| `serialize_table(data, pretty, indent)` | 序列化 Lua 表为字符串 | `data: table, pretty: boolean, indent: number` | `string` |
| `get_current_directory()` | 获取当前工作目录 | - | `string` |

---

## 🧪 测试

运行完整的测试套件：

```bash
cd Lua/file_utils
lua file_utils_test.lua
```

### 测试覆盖

- ✅ 路径处理（规范化、拼接、解析、相对路径）
- ✅ 文件读取（文本、二进制、行）
- ✅ 文件写入（覆盖、追加、复制）
- ✅ 文件信息（存在、大小、MIME 类型）
- ✅ 目录操作（创建、列出、递归、删除）
- ✅ 文件操作（删除、重命名、批量删除）
- ✅ 临时文件（生成、创建）
- ✅ 文件搜索（内容搜索、模式查找）
- ✅ 工具函数（序列化、哈希、权限检查）
- ✅ 边界条件（nil 处理、空字符串、特殊路径）

---

## 📝 示例

更多示例请查看 `examples/` 目录：

```bash
lua examples/file_utils_examples.lua
```

---

## ⚠️ 注意事项

1. **跨平台兼容性**：部分函数（如 `create_directory`、`delete_file`）使用系统命令，在 Windows 上可能需要调整
2. **权限问题**：文件操作需要适当的文件系统权限
3. **路径分隔符**：自动处理 `/` 和 `\`，统一使用 `/` 作为内部表示
4. **安全性**：`load_table` 使用 `load` 函数，确保只加载可信的 Lua 表文件

---

## 📄 许可证

MIT License - 详见 AllToolkit 主项目 LICENSE

---

## 🔗 相关模块

- **string_utils** - 字符串处理工具
- **table_utils** - 表操作工具
- **math_utils** - 数学计算工具

---

**最后更新**: 2026-04-11
**版本**: 1.0.0
