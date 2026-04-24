# JSON Utilities (JSON 工具集)

全面的 JSON 处理工具集，提供格式化、验证、路径查询、差异比较、合并、展平等功能。零外部依赖，纯 Python 实现。

## 功能特性

### ✅ 验证

- **validate_json()** - 验证 JSON 字符串是否有效
- **validate_json_schema()** - 简单的 JSON Schema 验证（支持类型、必填、范围、枚举等）
- **is_json_serializable()** - 检查值是否可序列化为 JSON

### 📝 格式化

- **format_json()** - 格式化 JSON 数据（支持美化/压缩/排序）
- **prettify_json()** - 美化 JSON 字符串
- **minify_json()** - 压缩 JSON 字符串
- **dumps()** - 便捷的格式化函数

### 🔍 路径操作

- **get_value()** - 通过路径获取值（支持 `a.b.c`, `items[0].name`）
- **set_value()** - 通过路径设置值（自动创建中间结构）
- **has_path()** - 检查路径是否存在
- **delete_value()** - 删除指定路径的值
- **parse_json_path()** - 解析路径字符串为部分列表

### 🔄 展平和嵌套

- **flatten_json()** - 将嵌套 JSON 展平为单层字典
- **unflatten_json()** - 将展平的字典还原为嵌套 JSON

### 🔎 搜索

- **find_all()** - 查找所有匹配的键或值
- **find_first()** - 查找第一个匹配的键或值
- **grep_json()** - 正则表达式搜索 JSON

### 🧹 过滤和转换

- **filter_json()** - 过滤 JSON 数据
- **map_json()** - 映射转换 JSON 数据中的值

### 📊 差异比较

- **diff_json()** - 比较两个 JSON 的差异
- **diff_summary()** - 生成差异摘要统计

### 🔗 合并

- **merge_json()** - 合并多个 JSON 对象（支持深度合并、数组合并策略）

### 📈 统计

- **json_stats()** - 统计 JSON 数据信息（键数、深度、类型分布、字节大小）

### 🎯 提取和选择

- **select_keys()** - 选择指定的键
- **omit_keys()** - 排除指定的键
- **pick_path()** - 选择多个路径的值

### 🚶 遍历

- **walk_json()** - 遍历 JSON 中所有值
- **get_all_paths()** - 获取所有路径列表
- **get_all_values()** - 获取所有值列表

### 🧬 克隆和比较

- **deep_clone()** - 深度克隆 JSON 数据
- **deep_equals()** - 深度比较两个 JSON 值

### 🛡️ 安全操作

- **safe_get()** - 安全获取嵌套值（避免 KeyError/IndexError）
- **safe_string()** - 安全解析 JSON 字符串
- **loads()** - 安全的 JSON 解析（失败返回默认值）
- **load_file()** / **save_file()** - 文件读写

### 🎯 JsonUtils 类

面向对象的 JSON 工具类，提供链式操作接口。

## 安装

零外部依赖，纯 Python 实现：

```python
from json_utils.mod import *
```

## 快速开始

### 基础格式化

```python
from json_utils.mod import format_json, prettify_json

data = {"name": "张三", "age": 25, "city": "北京"}

# 美化输出
print(format_json(data, indent=2))

# 压缩输出
print(format_json(data, compact=True))

# 从字符串美化
json_str = '{"name":"test","items":[1,2,3]}'
print(prettify_json(json_str))
```

### 验证 JSON

```python
from json_utils.mod import validate_json, validate_json_schema

# 验证 JSON 字符串
result = validate_json('{"name": "test"}')
print(result.valid)  # True

# Schema 验证
data = {"name": "John", "age": 25}
schema = {
    "type": "object",
    "required": ["name", "age"],
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0, "maximum": 150}
    }
}

valid, errors = validate_json_schema(data, schema)
print(f"验证结果: {valid}, 错误: {errors}")
```

### 路径操作

```python
from json_utils.mod import get_value, set_value, has_path

data = {
    "name": "项目",
    "user": {
        "id": 1,
        "profile": {"email": "test@example.com"}
    },
    "items": [{"id": 1, "name": "商品A"}, {"id": 2, "name": "商品B"}]
}

# 获取值
print(get_value(data, "name"))                   # "项目"
print(get_value(data, "user.id"))                # 1
print(get_value(data, "user.profile.email"))     # "test@example.com"
print(get_value(data, "items[0].name"))          # "商品A"

# 设置值（自动创建中间结构）
set_value(data, "user.profile.level", "gold")
print(data["user"]["profile"]["level"])          # "gold"

# 检查路径
print(has_path(data, "user.id"))                 # True
print(has_path(data, "user.missing"))            # False
```

### 展平和嵌套

```python
from json_utils.mod import flatten_json, unflatten_json

data = {
    "user": {
        "name": "张三",
        "profile": {"email": "zhang@example.com", "age": 30}
    }
}

# 展平
flat = flatten_json(data)
print(flat)
# {"user.name": "张三", "user.profile.email": "zhang@example.com", "user.profile.age": 30}

# 还原
restored = unflatten_json(flat)
print(restored)
# {"user": {"name": "张三", "profile": {"email": "zhang@example.com", "age": 30}}}
```

### 搜索

```python
from json_utils.mod import find_all, grep_json

data = {
    "name": "主项目",
    "manager": {"name": "李四", "email": "lisi@example.com"},
    "members": [{"name": "张三"}, {"name": "王五"}]
}

# 按键名搜索
results = find_all(data, key="name")
for r in results:
    print(f"{r.path}: {r.value}")

# 正则搜索
results = grep_json(data, r'\w+@example\.com')
for r in results:
    print(f"{r.path}: {r.value}")
```

### 差异比较

```python
from json_utils.mod import diff_json, diff_summary

old = {"name": "项目", "version": "1.0", "config": {"debug": True}}
new = {"name": "项目（新）", "version": "2.0", "config": {"debug": False}}

diffs = diff_json(old, new)
for diff in diffs:
    print(f"[{diff.change_type}] {diff.path}: {diff.old_value} -> {diff.new_value}")

# 摘要
print(diff_summary(diffs))  # {"added": 0, "removed": 0, "changed": 2}
```

### 合并

```python
from json_utils.mod import merge_json

base = {"name": "项目", "config": {"debug": True, "timeout": 30}}
overlay1 = {"version": "2.0", "config": {"timeout": 60}}
overlay2 = {"author": "张三", "config": {"logLevel": "info"}}

# 深度合并
result = merge_json(base, overlay1, overlay2, deep=True)
print(result)
# {"name": "项目", "version": "2.0", "author": "张三", 
#  "config": {"debug": True, "timeout": 60, "logLevel": "info"}}
```

### 使用 JsonUtils 类

```python
from json_utils.mod import JsonUtils

# 从字符串创建
jutil = JsonUtils.from_string('{"name": "test", "items": [1, 2, 3]}')

# 路径操作
print(jutil.get("name"))           # "test"
print(jutil.get("items[0]"))       # 1

jutil.set("items[3]", 4)           # 添加新值
jutil.has("items[3]")              # True

# 查找
results = jutil.find(key="name")

# 统计
stats = jutil.stats()
print(f"最大深度: {stats['max_depth']}")

# 展平
flat = jutil.flatten()

# 差异比较
diffs = jutil.diff({"name": "new"})

# 克隆
cloned = jutil.clone()
```

### 安全操作

```python
from json_utils.mod import safe_get, safe_string, loads

data = {"user": {"profile": {"name": "张三"}}}

# 安全获取（避免 KeyError）
print(safe_get(data, "user", "profile", "name"))           # "张三"
print(safe_get(data, "user", "missing", "field", default="默认"))  # "默认"

# 安全解析
success, result = safe_string('{"valid": true}')
print(f"成功: {success}, 结果: {result}")

# 失败返回默认值
data = loads('{"test": 123}')
data = loads('invalid json', default={})  # 返回 {}
```

### 文件操作

```python
from json_utils.mod import load_file, save_file

# 从文件加载
data = load_file("config.json")

# 保存到文件
save_file(data, "output.json", indent=2)

# 使用 JsonUtils
jutil = JsonUtils.from_file("config.json")
jutil.to_file("output.json")
```

## 运行测试

```bash
cd Python/json_utils
python json_utils_test.py
```

## 运行示例

```bash
cd Python/json_utils/examples
python usage_examples.py
```

## 应用场景

1. **配置文件处理** - 读取、验证、合并配置
2. **API 响应解析** - 安全解析、路径提取、数据转换
3. **数据迁移** - 差异比较、合并、转换
4. **日志分析** - JSON 日志搜索、过滤、统计
5. **数据校验** - Schema 验证、类型检查
6. **动态配置** - 深度合并、路径操作
7. **数据对比** - 版本差异、配置变更检测
8. **数据转换** - 展平嵌套数据、键值提取

## 特点

- ✅ 零外部依赖
- ✅ 纯 Python 实现
- ✅ 完整的测试覆盖
- ✅ 支持中文（ensure_ascii=False）
- ✅ 丰富的路径操作（支持数组索引、嵌套）
- ✅ 安全的错误处理
- ✅ 面向对象和函数式双接口

## API 参考

### 格式化

```python
format_json(data, indent=2, ensure_ascii=False, sort_keys=False, compact=False) -> str
prettify_json(json_string, indent=2) -> str
minify_json(json_string) -> str
dumps(data, indent=2, ensure_ascii=False) -> str
```

### 验证

```python
validate_json(json_string) -> ValidationResult
validate_json_schema(data, schema) -> Tuple[bool, List[str]]
is_json_serializable(value) -> bool
```

### 路径

```python
get_value(data, path, default=None) -> Any
set_value(data, path, value) -> data
has_path(data, path) -> bool
delete_value(data, path) -> bool
parse_json_path(path) -> List[str]
```

### 展平/嵌套

```python
flatten_json(data, separator='.', preserve_arrays=False) -> Dict[str, Any]
unflatten_json(data, separator='.') -> Dict[str, Any]
```

### 搜索

```python
find_all(data, key=None, value=None) -> List[JsonPath]
find_first(data, key=None, value=None) -> Optional[JsonPath]
grep_json(data, pattern, ignore_case=False) -> List[JsonPath]
```

### 过滤/映射

```python
filter_json(data, predicate) -> Any
map_json(data, mapper) -> Any
```

### 差异

```python
diff_json(old_data, new_data) -> List[JsonDiff]
diff_summary(diffs) -> Dict[str, int]
```

### 合并

```python
merge_json(base, *overlays, deep=True, arrays='replace') -> Dict[str, Any]
```

### 统计

```python
json_stats(data) -> Dict[str, Any]
```

### 选择/排除

```python
select_keys(data, keys) -> Dict[str, Any]
omit_keys(data, keys) -> Dict[str, Any]
pick_path(data, paths) -> Dict[str, Any]
```

### 遍历

```python
walk_json(data) -> Iterator[Tuple[str, Any]]
get_all_paths(data) -> List[str]
get_all_values(data) -> List[Any]
```

### 克隆/比较

```python
deep_clone(data) -> Any
deep_equals(a, b) -> bool
```

### 安全操作

```python
safe_get(data, *keys, default=None) -> Any
safe_string(json_string) -> Tuple[bool, Any]
loads(json_string, default=None) -> Any
load_file(filepath, encoding='utf-8', default=None) -> Any
save_file(data, filepath, indent=2, encoding='utf-8') -> bool
```

## 作者

AllToolkit 自动化开发

## 版本

1.0.0 (2026-04-25)