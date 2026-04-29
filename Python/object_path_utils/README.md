# Object Path Utils

通过路径字符串访问和操作嵌套对象的工具库。

## 特性

- 🎯 **简单直观** - 使用路径字符串访问嵌套数据
- 🔧 **功能完整** - 支持 get、set、delete、has、paths 等操作
- 📦 **零依赖** - 仅使用 Python 标准库
- 🛡️ **类型安全** - 完整的类型提示支持
- 🔄 **双向转换** - flatten/unflatten 支持对象扁平化
- 🧩 **类式 API** - ObjectPath 类支持链式调用

## 安装

无需安装，直接复制 `mod.py` 到项目中即可使用。

## 快速开始

```python
from mod import get, set, has, delete

# 嵌套对象
data = {
    "user": {
        "name": "Alice",
        "profile": {
            "age": 30,
            "email": "alice@example.com"
        }
    },
    "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
    ]
}

# 获取值
name = get(data, "user.name")           # "Alice"
age = get(data, "user.profile.age")     # 30
item = get(data, "items[0].name")       # "Item 1"

# 设置值
set(data, "user.profile.phone", "123-456-7890")
set(data, "items[2].name", "Item 3")    # 自动创建中间结构

# 检查存在
has(data, "user.name")                  # True
has(data, "user.address")                # False

# 删除值
delete(data, "user.profile.email")
```

## API 文档

### get(obj, path, default=None)

通过路径获取值。

```python
data = {"user": {"name": "Alice"}}
get(data, "user.name")           # "Alice"
get(data, "user.age", 25)        # 25 (默认值)
```

### set(obj, path, value, create_missing=True)

通过路径设置值。

```python
data = {}
set(data, "user.name", "Alice")  # {"user": {"name": "Alice"}}

# 自动创建中间结构
set(data, "a.b.c.d", 1)          # {"a": {"b": {"c": {"d": 1}}}}
```

### delete(obj, path) -> bool

通过路径删除值。

```python
data = {"user": {"name": "Alice", "age": 30}}
delete(data, "user.age")         # True
# data = {"user": {"name": "Alice"}}
```

### has(obj, path) -> bool

检查路径是否存在。

```python
data = {"user": {"name": "Alice"}}
has(data, "user.name")           # True
has(data, "user.email")          # False
```

### paths(obj, parent="", max_depth=10) -> List[str]

列出对象中的所有路径。

```python
data = {"user": {"name": "Alice", "age": 30}}
paths(data)
# ["user", "user.name", "user.age"]
```

### flatten(obj, separator=".", prefix="") -> Dict[str, Any]

将嵌套对象扁平化为单层字典。

```python
data = {"user": {"name": "Alice", "age": 30}}
flatten(data)
# {"user.name": "Alice", "user.age": 30}
```

### unflatten(obj, separator=".") -> Dict[str, Any]

将扁平化字典还原为嵌套对象。

```python
flat = {"user.name": "Alice", "user.age": 30}
unflatten(flat)
# {"user": {"name": "Alice", "age": 30}}
```

### pick(obj, *paths) -> Dict[str, Any]

从对象中选取指定路径的值。

```python
data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
pick(data, "name", "age")
# {"name": "Alice", "age": 30}
```

### omit(obj, *paths) -> Any

从对象中排除指定路径的值。

```python
data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
omit(data, "email")
# {"name": "Alice", "age": 30}
```

### merge(*objects, deep=True) -> Any

合并多个对象。

```python
merge({"a": 1}, {"b": 2})
# {"a": 1, "b": 2}

merge({"user": {"name": "Alice"}}, {"user": {"age": 30}})
# {"user": {"name": "Alice", "age": 30}}
```

### ObjectPath 类

面向对象的 API，支持链式调用。

```python
from mod import ObjectPath

op = ObjectPath({})
op.set("user.name", "Alice") \
  .set("user.age", 30) \
  .set("user.tags", ["admin"])

op.get("user.name")      # "Alice"
op.has("user.email")     # False
op.paths()               # ["user", "user.name", "user.age", ...]
op.flatten()             # {"user.name": "Alice", ...}
```

## 路径语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `property` | 访问属性 | `"name"` |
| `parent.child` | 嵌套访问 | `"user.name"` |
| `array[index]` | 数组索引 | `"items[0]"` |
| 混合 | 组合使用 | `"users[0].profile.name"` |

## 使用场景

### 1. API 响应处理

```python
response = {
    "code": 200,
    "data": {
        "user": {
            "profile": {"nickname": "Alice"}
        }
    }
}

nickname = get(response, "data.user.profile.nickname", "未知用户")
```

### 2. 配置文件处理

```python
# 从环境变量风格转换
env_config = {
    "APP_NAME": "MyApp",
    "DB_HOST": "localhost",
    "DB_PORT": "5432"
}

normalized = {k.lower().replace("_", "."): v for k, v in env_config.items()}
config = unflatten(normalized)
# {"app": {"name": "MyApp"}, "db": {"host": "localhost", "port": "5432"}}
```

### 3. 表单数据提取

```python
form_data = {
    "user.name": "Alice",
    "user.email": "alice@example.com",
    "preferences.theme": "dark"
}

user_info = pick(form_data, "user.name", "user.email")
# {"user.name": "Alice", "user.email": "alice@example.com"}
```

### 4. 深度合并配置

```python
defaults = {"database": {"host": "localhost", "port": 5432}}
user_config = {"database": {"host": "production-db", "username": "admin"}}

final = merge(defaults, user_config)
# {"database": {"host": "production-db", "port": 5432, "username": "admin"}}
```

## 测试

```bash
python object_path_utils_test.py
```

## 许可证

MIT