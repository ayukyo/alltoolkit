# TOML Utils

完整的 TOML 配置文件解析和生成工具，零外部依赖，支持 TOML 1.0.0 规范。

## 功能特性

### 解析 (Parse)
- ✅ 字符串（基础字符串、字面字符串、多行字符串）
- ✅ 整数（十进制、十六进制、八进制、二进制，支持下划线分隔）
- ✅ 浮点数（科学计数法、特殊值 inf/nan）
- ✅ 布尔值（true/false）
- ✅ 日期时间（日期、时间、本地日期时间、带偏移的日期时间）
- ✅ 数组
- ✅ 内联表
- ✅ 表（包括嵌套表、点号键）
- ✅ 表数组 [[...]]

### 生成 (Generate)
- ✅ 自动格式化输出
- ✅ 支持所有 TOML 类型
- ✅ 表数组格式化
- ✅ 键排序输出
- ✅ 特殊字符转义

### 工具函数
- ✅ merge - 合并多个配置
- ✅ get/set_value - 点号路径访问
- ✅ flatten/unflatten - 扁平化与反扁平化
- ✅ diff - 配置差异比较
- ✅ validate - 数据验证
- ✅ read_config/write_config - 带默认值和备份的配置读写

## 使用示例

### 基本解析

```python
from toml_utils import parse, loads

# 解析 TOML 字符串
config = parse('''
[database]
host = "localhost"
port = 5432
credentials = { user = "admin", password = "secret" }

[[servers]]
name = "primary"
ip = "10.0.0.1"

[[servers]]
name = "backup"
ip = "10.0.0.2"
''')

print(config['database']['host'])      # localhost
print(config['servers'][0]['name'])    # primary
```

### 文件读写

```python
from toml_utils import load, dump

# 从文件加载
config = load('config.toml')

# 写入文件
dump(config, 'output.toml')

# 带默认值读取
defaults = {'debug': False, 'port': 8080}
config = read_config('config.toml', defaults)

# 带备份写入
write_config('config.toml', config, backup=True)
```

### 生成 TOML

```python
from toml_utils import dumps
import datetime

config = {
    'project': {
        'name': 'my-app',
        'version': '1.0.0',
        'created': datetime.date(2024, 5, 27)
    },
    'servers': [
        {'host': 'localhost', 'port': 8080},
        {'host': 'production', 'port': 443}
    ]
}

toml_str = dumps(config)
print(toml_str)
```

输出：
```toml
[project]
name = "my-app"
version = "1.0.0"
created = 2024-05-27

[[servers]]
host = "localhost"
port = 8080

[[servers]]
host = "production"
port = 443
```

### 点号路径访问

```python
from toml_utils import get, set_value

config = {'database': {'host': 'localhost', 'port': 5432}}

# 获取值
host = get(config, 'database.host')        # 'localhost'
user = get(config, 'database.user', 'sa')  # 'sa' (默认值)

# 设置值
set_value(config, 'database.credentials.user', 'admin')
# config = {'database': {'host': 'localhost', 'port': 5432, 'credentials': {'user': 'admin'}}}
```

### 配置合并

```python
from toml_utils import merge

base = {
    'server': {'host': 'localhost', 'port': 8080},
    'debug': False
}

override = {
    'server': {'port': 3000},
    'debug': True
}

merged = merge(base, override)
# {'server': {'host': 'localhost', 'port': 3000}, 'debug': True}
```

### 扁平化操作

```python
from toml_utils import flatten, unflatten

config = {
    'database': {
        'primary': {'host': 'db1', 'port': 5432},
        'replica': {'host': 'db2', 'port': 5433}
    }
}

flat = flatten(config)
# {
#     'database.primary.host': 'db1',
#     'database.primary.port': 5432,
#     'database.replica.host': 'db2',
#     'database.replica.port': 5433
# }

original = unflatten(flat)  # 恢复嵌套结构
```

### 配置差异比较

```python
from toml_utils import diff

old_config = {'version': 1, 'features': {'a': True, 'b': False}}
new_config = {'version': 2, 'features': {'a': True, 'c': True}}

result = diff(old_config, new_config)
# {
#     'added': {'features.c': True},
#     'removed': {'features.b': False},
#     'changed': {'version': {'old': 1, 'new': 2}}
# }
```

## 支持的数据类型

| TOML 类型 | Python 类型 |
|-----------|-------------|
| 字符串 | str |
| 整数 | int |
| 浮点数 | float |
| 布尔值 | bool |
| 日期 | datetime.date |
| 时间 | datetime.time |
| 日期时间 | datetime.datetime |
| 数组 | list |
| 表 | dict |

## 错误处理

```python
from toml_utils import parse, TOMLSyntaxError, TOMLValidationError

try:
    config = parse('invalid [toml')
except TOMLSyntaxError as e:
    print(f"语法错误: {e}")

try:
    validate({'set': {1, 2, 3}})  # set 不是有效的 TOML 类型
except TOMLValidationError as e:
    print(f"验证错误: {e}")
```

## 测试

```bash
cd Python/toml_utils
python -m pytest toml_utils_test.py -v
```

## 零依赖

纯 Python 标准库实现，无需安装任何第三方包。

## 许可证

MIT