# YAML Utilities - AllToolkit

**功能完整的 Python YAML 处理工具 - 支持 PyYAML 或优雅降级**

---

## 📦 功能特性

- ✅ **YAML 读取/写入** - 从文件、字符串、文件对象加载和保存
- ✅ **格式转换** - YAML ↔ JSON 互相转换
- ✅ **验证功能** - 基础语法验证、模式验证
- ✅ **多文档支持** - 加载多文档 YAML 文件
- ✅ **合并功能** - 深度/浅层合并多个 YAML 配置
- ✅ **差分比较** - 比较两个 YAML 文件的差异
- ✅ **便捷操作** - 获取/设置/删除指定路径的值
- ✅ **安全加载** - 防止任意代码执行的不安全标签
- ✅ **优雅降级** - 无 PyYAML 时使用 JSON 作为替代

---

## 🚀 快速开始

### 安装依赖

```bash
# 推荐：安装 PyYAML 获得完整功能
pip install PyYAML

# 或仅使用标准库（功能有限，使用 JSON 降级）
# 无需安装任何依赖
```

### 基本使用

```python
from mod import (
    load_yaml,
    load_yaml_string,
    dump_yaml,
    dump_yaml_file,
    get_yaml_value,
    set_yaml_value,
    validate_yaml,
    yaml_to_json,
    merge_yaml,
    diff_yaml,
)

# 从字符串加载 YAML
data = load_yaml_string("""
name: 配置示例
version: 1.0
database:
  host: localhost
  port: 5432
""")
print(data['name'])  # 输出：配置示例

# 从文件加载
config = load_yaml_file('config.yaml')

# 保存为 YAML 文件
dump_yaml_file(data, 'output.yaml')

# 保存为 YAML 字符串
yaml_str = dump_yaml_string(data)

# 获取嵌套值
host = get_yaml_value('config.yaml', 'database.host')
print(host)  # 输出：localhost

# 设置值
set_yaml_value('config.yaml', 'database.port', 5433)

# 验证 YAML
is_valid, errors = validate_yaml('config.yaml')

# YAML 转 JSON
json_str = yaml_to_json('config.yaml')

# 合并多个配置
merged = merge_yaml(['base.yaml', 'override.yaml'], deep=True)

# 比较差异
diff = diff_yaml('old.yaml', 'new.yaml')
print(f"新增：{diff['added']}")
print(f"移除：{diff['removed']}")
print(f"修改：{diff['modified']}")
```

---

## 📖 API 参考

### 版本信息

#### `get_version()` → `str`

获取模块版本号。

```python
from mod import get_version
print(get_version())  # 输出：1.0.0
```

#### `is_pyyaml_available()` → `bool`

检查 PyYAML 库是否可用。

```python
from mod import is_pyyaml_available
if is_pyyaml_available():
    print("完整功能可用")
else:
    print("使用 JSON 降级模式")
```

---

### 读取功能

#### `load_yaml(source, safe=True)` → `Any`

加载 YAML 数据，支持文件路径、文件对象或字符串。

```python
from mod import load_yaml

# 从文件路径
data = load_yaml('config.yaml')

# 从字符串
data = load_yaml("key: value")

# 不安全模式（不推荐，仅受信任的内容）
data = load_yaml('config.yaml', safe=False)
```

#### `load_yaml_string(yaml_string, safe=True)` → `Any`

从字符串加载 YAML。

```python
from mod import load_yaml_string

yaml_str = """
name: 测试
value: 123
"""
data = load_yaml_string(yaml_str)
```

#### `load_yaml_file(file_path, safe=True)` → `Any`

从文件加载 YAML。

```python
from mod import load_yaml_file

config = load_yaml_file('config.yaml')
```

#### `load_yaml_all(source)` → `List[Any]`

加载多文档 YAML 文件（包含 `---` 分隔符）。

```python
from mod import load_yaml_all

documents = load_yaml_all('multi-doc.yaml')
for doc in documents:
    print(doc)
```

#### `safe_load_yaml(source)` → `Any`

安全加载 YAML（始终使用安全模式）。

```python
from mod import safe_load_yaml

data = safe_load_yaml('config.yaml')
```

---

### 写入功能

#### `dump_yaml(data, output=None, indent=2, allow_unicode=True, sort_keys=False)` → `Optional[str]`

将数据转储为 YAML 格式。

```python
from mod import dump_yaml

data = {'name': '测试', 'value': 123}

# 返回字符串
yaml_str = dump_yaml(data)

# 保存到文件
dump_yaml(data, output='output.yaml')
```

#### `dump_yaml_file(data, file_path, indent=2, allow_unicode=True)` → `None`

将数据转储为 YAML 文件。

```python
from mod import dump_yaml_file

config = {'app': {'name': 'MyApp', 'version': '1.0'}}
dump_yaml_file(config, 'config.yaml')
```

#### `dump_yaml_string(data, indent=2, allow_unicode=True)` → `str`

将数据转储为 YAML 字符串。

```python
from mod import dump_yaml_string

yaml_str = dump_yaml_string({'key': 'value'})
print(yaml_str)
```

---

### 验证功能

#### `validate_yaml(source, schema=None)` → `Tuple[bool, List[str]]`

验证 YAML 文件，可选模式验证。

```python
from mod import validate_yaml

# 基础验证
is_valid, errors = validate_yaml('config.yaml')

# 带模式验证
schema = {
    'name': str,
    'version': float,
    'port': int,
    'debug': bool,
    'optional': None  # None 表示可选
}
is_valid, errors = validate_yaml('config.yaml', schema)

if not is_valid:
    for error in errors:
        print(f"错误：{error}")
```

#### `is_valid_yaml(source)` → `bool`

检查是否为有效的 YAML。

```python
from mod import is_valid_yaml

if is_valid_yaml('config.yaml'):
    print("YAML 格式有效")
```

---

### 转换功能

#### `yaml_to_json(source, output=None, indent=2)` → `Optional[str]`

将 YAML 转换为 JSON。

```python
from mod import yaml_to_json

# 返回 JSON 字符串
json_str = yaml_to_json('config.yaml')

# 保存到文件
yaml_to_json('config.yaml', 'output.json')
```

#### `json_to_yaml(source, output=None, indent=2)` → `Optional[str]`

将 JSON 转换为 YAML。

```python
from mod import json_to_yaml

# 从文件转换
yaml_str = json_to_yaml('data.json')

# 从字符串转换
yaml_str = json_to_yaml('{"key": "value"}')
```

#### `yaml_to_dict(source)` → `Dict`

将 YAML 转换为字典。

```python
from mod import yaml_to_dict

config = yaml_to_dict('config.yaml')
```

---

### 合并功能

#### `merge_yaml(sources, output=None, deep=True)` → `Optional[Dict]`

合并多个 YAML 文件。

```python
from mod import merge_yaml

# 深度合并（推荐）
merged = merge_yaml(['base.yaml', 'dev.yaml'], deep=True)

# 浅层合并（直接覆盖）
merged = merge_yaml(['base.yaml', 'prod.yaml'], deep=False)

# 保存到文件
merge_yaml(['base.yaml', 'override.yaml'], output='merged.yaml')
```

---

### 差分功能

#### `diff_yaml(source1, source2)` → `Dict[str, Any]`

比较两个 YAML 文件的差异。

```python
from mod import diff_yaml

diff = diff_yaml('old.yaml', 'new.yaml')

# 新增的字段
print(f"新增：{diff['added']}")

# 移除的字段
print(f"移除：{diff['removed']}")

# 修改的字段
for key, change in diff['modified'].items():
    print(f"{key}: {change['old']} → {change['new']}")
```

---

### 便捷功能

#### `get_yaml_value(source, key_path, default=None)` → `Any`

获取 YAML 中指定路径的值（支持点分隔路径）。

```python
from mod import get_yaml_value

# 简单路径
name = get_yaml_value('config.yaml', 'app.name')

# 嵌套路径
host = get_yaml_value('config.yaml', 'database.connection.host')

# 带默认值
timeout = get_yaml_value('config.yaml', 'database.timeout', 30)
```

#### `set_yaml_value(source, key_path, value, output=None)` → `None`

设置 YAML 中指定路径的值。

```python
from mod import set_yaml_value

# 覆盖原文件
set_yaml_value('config.yaml', 'app.version', '2.0')

# 输出到新文件
set_yaml_value('config.yaml', 'app.version', '2.0', output='new.yaml')
```

#### `delete_yaml_key(source, key_path, output=None)` → `None`

删除 YAML 中指定路径的键。

```python
from mod import delete_yaml_key

# 删除敏感信息
delete_yaml_key('config.yaml', 'database.password')
```

---

### 安全功能

#### `contains_unsafe_tags(source)` → `bool`

检查 YAML 是否包含不安全标签（如 `!!python`）。

```python
from mod import contains_unsafe_tags

if contains_unsafe_tags('config.yaml'):
    print("警告：包含不安全标签！")
else:
    print("YAML 安全")
```

---

### 工具功能

#### `get_supported_formats()` → `List[str]`

获取支持的格式列表。

```python
from mod import get_supported_formats
print(get_supported_formats())  # ['YAML', 'JSON', 'YAML (full)']
```

#### `get_yaml_info(source)` → `Dict[str, Any]`

获取 YAML 文件信息。

```python
from mod import get_yaml_info

info = get_yaml_info('config.yaml')
print(f"路径：{info['path']}")
print(f"大小：{info['size']} 字节")
print(f"有效：{info['valid']}")
print(f"类型：{info['type']}")
print(f"顶层键：{info['keys']}")
```

---

## 🔒 安全注意事项

### 避免不安全加载

```python
# ❌ 危险：可能执行任意代码
from mod import load_yaml
data = load_yaml('untrusted.yaml', safe=False)

# ✅ 安全：始终使用安全模式
data = load_yaml('untrusted.yaml', safe=True)
# 或
data = safe_load_yaml('untrusted.yaml')
```

### 检测不安全标签

```python
from mod import contains_unsafe_tags

yaml_content = """
!!python/object/apply:os.system
args: ['malicious command']
"""

if contains_unsafe_tags(yaml_content):
    print("拒绝加载：包含不安全标签")
```

---

## 📝 使用场景

### 场景 1: 配置文件管理

```python
from mod import load_yaml_file, get_yaml_value, merge_yaml

# 加载基础配置
base = load_yaml_file('config.base.yaml')

# 加载环境配置
env = load_yaml_file('config.prod.yaml')

# 合并配置
config = merge_yaml([base, env])

# 获取配置值
db_host = get_yaml_value('config.yaml', 'database.host')
```

### 场景 2: 配置迁移

```python
from mod import yaml_to_json, json_to_yaml

# YAML 转 JSON
yaml_to_json('old_config.yaml', 'new_config.json')

# JSON 转 YAML
json_to_yaml('data.json', 'data.yaml')
```

### 场景 3: 配置验证

```python
from mod import validate_yaml

schema = {
    'database': {
        'host': str,
        'port': int,
        'credentials': {
            'username': str,
            'password': str
        }
    },
    'logging': {
        'level': str
    }
}

is_valid, errors = validate_yaml('config.yaml', schema)
if not is_valid:
    for error in errors:
        print(f"配置错误：{error}")
```

### 场景 4: 配置变更审计

```python
from mod import diff_yaml

diff = diff_yaml('config.v1.yaml', 'config.v2.yaml')

print("=== 配置变更报告 ===")
if diff['added']:
    print(f"➕ 新增：{list(diff['added'].keys())}")
if diff['removed']:
    print(f"➖ 移除：{list(diff['removed'].keys())}")
if diff['modified']:
    print(f"🔄 修改：{list(diff['modified'].keys())}")
```

---

## 🧪 运行测试

```bash
cd yaml_utils
python yaml_utils_test.py
```

---

## 📚 示例代码

查看 `examples/basic_usage.py` 获取完整使用示例：

```bash
python examples/basic_usage.py
```

---

## ⚠️ 降级模式说明

当 PyYAML 不可用时，模块会自动降级使用 JSON：

- `load_yaml` → 尝试解析为 JSON
- `dump_yaml` → 输出为 JSON 格式
- 多文档 YAML 不支持
- 部分 YAML 特有功能不可用

建议安装 PyYAML 获得完整功能：

```bash
pip install PyYAML
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
