# json_flatten_utils - JSON/字典扁平化工具

零依赖的字典扁平化和嵌套操作工具库，用于处理复杂的嵌套数据结构。

## 功能特性

- ✅ **flatten_dict** - 将嵌套字典扁平化为单层字典
- ✅ **unflatten_dict** - 将扁平字典还原为嵌套字典
- ✅ **flatten_list** - 将嵌套列表扁平化为一维列表
- ✅ **deep_merge** - 淰度合并多个字典
- ✅ **get_nested_value** - 安全获取嵌套值
- ✅ **set_nested_value** - 设置嵌套值
- ✅ **delete_nested_value** - 删除嵌套值
- ✅ **has_nested_key** - 检查嵌套键是否存在
- ✅ **diff_dicts** - 比较两个字典的差异
- ✅ **dict_paths** - 获取所有键路径
- ✅ **dict_depth** - 计算嵌套深度
- ✅ **pick_keys** - 选取指定键
- ✅ **omit_keys** - 排除指定键

## 安装

```bash
# 直接使用（零依赖）
python -c "from json_flatten_utils import flatten_dict; print(flatten_dict({'a': {'b': 1}}))"
```

## 快速开始

### 基本用法

```python
from json_flatten_utils import flatten_dict, unflatten_dict

# 扁平化嵌套字典
data = {"user": {"name": "Alice", "age": 30}}
flat = flatten_dict(data)
# {'user.name': 'Alice', 'user.age': 30}

# 反扁平化
nested = unflatten_dict(flat)
# {'user': {'name': 'Alice', 'age': 30}}
```

### 自定义分隔符

```python
# 使用下划线分隔符
flatten_dict({"a": {"b": 1}}, separator="_")
# {'a_b': 1}

# 使用斜杠分隔符（适合URL路径）
flatten_dict({"api": {"v1": {"users": 10}}}, separator="/")
# {'api/v1/users': 10}
```

### 深度限制

```python
# 限制扁平化深度
data = {"a": {"b": {"c": {"d": 1}}}}
flatten_dict(data, max_depth=2)
# {'a.b.c': {'d': 1}}  # 不再继续扁平化
```

### 列表处理

```python
# 扁平化列表中的字典
data = {"items": [{"name": "a"}, {"name": "b"}]}
flatten_dict(data, flatten_lists=True)
# {'items[0].name': 'a', 'items[1].name': 'b'}

# 自定义列表索引格式
flatten_dict(data, flatten_lists=True, list_index_format="_{}")
# {'items_0.name': 'a', 'items_1.name': 'b'}
```

### 列表扁平化

```python
from json_flatten_utils import flatten_list

# 扁平化嵌套列表
flatten_list([1, [2, [3, [4]]]])
# [1, 2, 3, 4]

# 限制深度
flatten_list([1, [2, [3, [4]]]], max_depth=1)
# [1, 2, [3, [4]]]
```

### 深度合并

```python
from json_flatten_utils import deep_merge

# 合并字典
deep_merge({"a": 1}, {"b": 2})
# {'a': 1, 'b': 2}

# 嵌套合并
deep_merge({"user": {"name": "Alice"}}, {"user": {"age": 30}})
# {'user': {'name': 'Alice', 'age': 30}}

# 合并列表
deep_merge({"tags": ["python"]}, {"tags": ["js"]}, merge_lists=True)
# {'tags': ['python', 'js']}
```

### 嵌套值操作

```python
from json_flatten_utils import get_nested_value, set_nested_value

data = {"user": {"name": "Alice", "age": 30}}

# 获取嵌套值
get_nested_value(data, "user.name")
# 'Alice'

# 安全获取（带默认值）
get_nested_value(data, "user.email", default="N/A")
# 'N/A'

# 设置嵌套值
set_nested_value({}, "user.name.first", "Alice")
# {'user': {'name': {'first': 'Alice'}}}

# 检查键是否存在
has_nested_key(data, "user.name")
# True

# 删除嵌套值
delete_nested_value(data, "user.age")
# {'user': {'name': 'Alice'}}
```

### 字典比较

```python
from json_flatten_utils import diff_dicts

dict1 = {"user": {"name": "Alice", "age": 30}}
dict2 = {"user": {"name": "Bob", "age": 30, "email": "bob@example.com"}}

diff = diff_dicts(dict1, dict2)
# {
#   'added': {'user.email': 'bob@example.com'},
#   'removed': {},
#   'changed': {'user.name': {'old': 'Alice', 'new': 'Bob'}},
#   'unchanged': {'user.age': 30}
# }
```

### 工具函数

```python
from json_flatten_utils import dict_paths, dict_depth, pick_keys, omit_keys

data = {"user": {"name": "Alice", "age": 30}, "status": "active"}

# 获取所有键路径
dict_paths(data)
# ['user.name', 'user.age', 'status']

# 计算嵌套深度
dict_depth({"a": {"b": {"c": 1}}})
# 3

# 选取指定键
pick_keys(data, ["user.name"])
# {'user': {'name': 'Alice'}}

# 排除指定键
omit_keys(data, ["user.age"])
# {'user': {'name': 'Alice'}, 'status': 'active'}
```

## API文档

### `flatten_dict(data, ...)`

将嵌套字典扁平化。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data` | `dict` | - | 要扁平化的字典 |
| `separator` | `str` | `'.'` | 键分隔符 |
| `max_depth` | `int` | `None` | 最大深度限制 |
| `flatten_lists` | `bool` | `False` | 是否扁平化列表中的字典 |
| `list_index_format` | `str` | `'[{}}'` | 列表索引格式 |

### `unflatten_dict(data, ...)`

将扁平字典还原为嵌套字典。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data` | `dict` | - | 扁平字典 |
| `separator` | `str` | `'.'` | 键分隔符 |

### `flatten_list(data, ...)`

将嵌套列表扁平化。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data` | `list` | - | 要扁平化的列表 |
| `max_depth` | `int` | `None` | 最大深度限制 |
| `preserve_types` | `bool` | `False` | 保留元组/集合类型 |

### `deep_merge(*dicts, ...)`

深度合并多个字典。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `*dicts` | `dict` | - | 要合并的字典 |
| `overwrite` | `bool` | `True` | 是否覆盖已存在的键 |
| `merge_lists` | `bool` | `False` | 是否合并列表 |
| `unique_lists` | `bool` | `True` | 合并列表时是否去重 |

### `get_nested_value(data, key_path, ...)`

安全获取嵌套值。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data` | `dict` | - | 字典数据 |
| `key_path` | `str/list` | - | 键路径 |
| `separator` | `str` | `'.'` | 分隔符 |
| `default` | `any` | `None` | 默认值 |
| `raise_error` | `bool` | `False` | 是否抛出错误 |

### `set_nested_value(data, key_path, value, ...)`

设置嵌套值。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data` | `dict` | - | 字典数据 |
| `key_path` | `str/list` | - | 键路径 |
| `value` | `any` | - | 要设置的值 |
| `create_parents` | `bool` | `True` | 是否创建父级 |

### `diff_dicts(dict1, dict2, ...)`

比较两个字典的差异。

返回包含 `added`, `removed`, `changed`, `unchanged` 的字典。

## 真实场景示例

### 配置文件合并

```python
# 合并多层配置
default_config = {"server": {"port": 8080, "host": "localhost"}}
user_config = {"server": {"port": 3000}, "debug": True}

final_config = deep_merge(default_config, user_config)
# {'server': {'port': 3000, 'host': 'localhost'}, 'debug': True}
```

### API响应扁平化

```python
# 处理复杂API响应
response = {
    "data": {
        "users": [
            {"id": 1, "profile": {"name": "Alice"}},
            {"id": 2, "profile": {"name": "Bob"}}
        ]
    }
}

flat = flatten_dict(response, flatten_lists=True)
# {'data.users[0].id': 1, 'data.users[0].profile.name': 'Alice', ...}

# 获取特定值
get_nested_value(flat, "data.users[0].profile.name")
# 'Alice'
```

### 数据差异检测

```python
# 检测前后变化
before = {"user": {"name": "Alice", "settings": {"theme": "dark"}}}
after = {"user": {"name": "Alice", "settings": {"theme": "light", "lang": "en"}}}

diff = diff_dicts(before, after)
# 新增: user.settings.lang
# 变化: user.settings.theme (dark -> light)
```

### CSV导出准备

```python
# 将嵌套数据转为扁平格式以便导出
records = [
    {"name": "Alice", "address": {"city": "Beijing", "zip": "100000"}},
    {"name": "Bob", "address": {"city": "Shanghai", "zip": "200000"}}
]

flat_records = [flatten_dict(r) for r in records]
# [{'name': 'Alice', 'address.city': 'Beijing', 'address.zip': '100000'}, ...]
```

## 测试

```bash
# 运行测试
python Python/json_flatten_utils/json_flatten_utils_test.py

# 运行示例
python Python/json_flatten_utils/examples/usage_examples.py
```

## 测试覆盖

- 17个测试函数
- 50+ 测试用例
- 覆盖正常场景、边界值、异常情况
- 100% 通过率 ✅

## 版本

- **版本**: 1.0.0
- **作者**: AllToolkit
- **日期**: 2026-05-03
- **语言**: Python 3.x
- **依赖**: 无（仅使用标准库）

## 许可证

MIT License