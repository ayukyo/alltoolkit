# Configuration Utilities - AllToolkit Python

**零依赖配置管理工具 - 支持多格式解析、环境变量替换、Schema 验证**

---

## 📖 概述

`config_utils` 是一个功能完整的配置管理模块，提供：

- ✅ **多格式支持**: Key-Value、JSON、INI、.env 文件
- ✅ **环境变量替换**: 支持 `${VAR}`、`$VAR`、`${VAR:-default}` 语法
- ✅ **Schema 验证**: 类型检查、必填字段、范围限制、正则匹配
- ✅ **类型转换**: 自动转换为 int、float、bool、list、dict
- ✅ **嵌套配置**: 支持点号访问 `database.host`
- ✅ **线程安全**: 支持不可变配置
- ✅ **零依赖**: 仅使用 Python 标准库

---

## 🚀 快速开始

### 基本使用

```python
from mod import Config, create_schema, load_config

# 创建配置
config = Config({
    'host': 'localhost',
    'port': 8080,
    'debug': True,
})

# 访问配置
print(config.get('host'))           # 'localhost'
print(config.get_int('port'))       # 8080
print(config.get_bool('debug'))     # True
print(config.get('missing', 'default'))  # 'default'

# 嵌套访问
config = Config({
    'database': {
        'host': 'localhost',
        'port': 5432,
    }
})
print(config.get('database.host'))  # 'localhost'
```

### 从文件加载

```python
from mod import load_config, ConfigFormat

# 自动检测格式（根据文件扩展名）
config = load_config('config.conf')

# 指定格式
config = load_config('settings.json', format=ConfigFormat.JSON)
config = load_config('app.ini', format=ConfigFormat.INI)
config = load_config('.env', format=ConfigFormat.ENV)
```

### 环境变量替换

```python
from mod import Config

# 环境变量：export DB_HOST=localhost
config = Config({
    'host': '${DB_HOST}',           # 替换为 localhost
    'port': '$DB_PORT',             # 另一种语法
    'fallback': '${MISSING:-default}',  # 使用默认值
}, env_substitute=True)
```

---

## 📋 Schema 验证

### 创建 Schema

```python
from mod import create_schema, Config

# 定义配置 Schema
schema = create_schema(
    host=dict(type=str, required=True, description="服务器地址"),
    port=dict(type=int, required=True, min=1, max=65535),
    debug=dict(type=bool, default=False),
    log_level=dict(type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
    email=dict(type=str, pattern=r'^[\w.-]+@[\w.-]+\.\w+$'),
)

# 验证配置
config = Config({
    'host': 'localhost',
    'port': 8080,
}, schema)

# 检查验证结果
is_valid, errors = config.validate()
if not is_valid:
    for error in errors:
        print(f"验证错误：{error}")

# 严格验证（失败时抛出异常）
try:
    config.validate_strict()
except ConfigValidationError as e:
    print(f"验证失败：{e}")
```

### Schema 字段选项

| 选项 | 类型 | 描述 |
|------|------|------|
| `type` | `type` | 字段类型（str, int, float, bool, list, dict） |
| `required` | `bool` | 是否必填 |
| `default` | `Any` | 默认值 |
| `min` | `int/float` | 最小值（数字类型） |
| `max` | `int/float` | 最大值（数字类型） |
| `choices` | `List` | 允许的取值列表 |
| `pattern` | `str` | 正则表达式模式（字符串类型） |
| `description` | `str` | 字段描述 |

### 严格模式

```python
from mod import ConfigSchema, SchemaField

# 严格模式：拒绝未知字段
schema = ConfigSchema(
    fields={'host': SchemaField(type=str)},
    strict=True  # 启用严格模式
)

config = Config({'host': 'localhost', 'unknown': 'value'}, schema)
is_valid, errors = config.validate()
# is_valid = False, errors = ["Unknown configuration key: unknown"]
```

---

## 📁 支持的文件格式

### Key-Value 格式 (.conf, .cfg)

```ini
# 配置文件
host=localhost
port=8080
name="My Application"
debug=true

# 环境变量替换
database_url=postgresql://${DB_HOST}:${DB_PORT}/mydb
```

### JSON 格式 (.json)

```json
{
    "host": "localhost",
    "port": 8080,
    "database": {
        "host": "db.example.com",
        "port": 5432
    },
    "features": ["auth", "logging", "cache"]
}
```

### INI 格式 (.ini)

```ini
[database]
host=localhost
port=5432
name=mydb

[server]
host=0.0.0.0
port=8080
workers=4
```

### ENV 格式 (.env)

```bash
# .env 文件
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DEBUG=true
SECRET_KEY=${SECRET:-fallback}
```

---

## 🔧 API 参考

### Config 类

```python
config = Config(
    data=None,           # 初始配置数据
    schema=None,         # 验证 Schema
    env_substitute=True, # 启用环境变量替换
    env_prefix="",       # 环境变量前缀
    immutable=False      # 是否不可变
)
```

#### 获取值

| 方法 | 描述 | 示例 |
|------|------|------|
| `get(key, default)` | 获取值（支持点号） | `config.get('db.host')` |
| `get_int(key, default)` | 获取整数 | `config.get_int('port', 8080)` |
| `get_float(key, default)` | 获取浮点数 | `config.get_float('ratio', 1.0)` |
| `get_bool(key, default)` | 获取布尔值 | `config.get_bool('debug', False)` |
| `get_list(key, default)` | 获取列表 | `config.get_list('tags', [])` |
| `get_dict(key, default)` | 获取字典 | `config.get_dict('meta', {})` |

#### 设置值

```python
config.set('host', 'localhost')
config.set('server.port', 8080)  # 嵌套设置
config.update({'debug': True, 'name': 'App'})

# 链式调用
config.set('a', 1).set('b', 2).update({'c': 3})
```

#### 其他方法

```python
config.has('key')           # 检查是否存在
config.delete('key')        # 删除键
config.keys()               # 获取所有键
config.to_dict()            # 转换为字典
config.make_immutable()     # 设为不可变
config.freeze()             # 同上（别名）
config.validate(schema)     # 验证配置
config.validate_strict()    # 严格验证（抛出异常）
```

#### 便捷访问

```python
config['host']              # 等同于 config.get('host')
config['port'] = 8080       # 等同于 config.set('port', 8080)
'host' in config            # 等同于 config.has('host')
len(config)                 # 获取键数量
```

### ConfigParser 类

```python
parser = ConfigParser(env_prefix="APP_")

# 解析字符串
data = parser.parse(content, ConfigFormat.KEY_VALUE)
data = parser.parse_key_value(content)
data = parser.parse_json(content)
data = parser.parse_ini(content)
data = parser.parse_env(content)

# 解析文件
data = parser.parse_file('config.conf')
data = parser.parse_file('settings.json', ConfigFormat.JSON)

# 环境变量替换
text = parser.substitute_env("Host: ${HOST}, Port: $PORT")
```

### 便捷函数

```python
from mod import (
    load_config,      # 从文件加载配置
    create_config,    # 创建配置对象
    create_schema,    # 创建 Schema
    parse_config,     # 解析配置字符串
)
```

---

## 📦 预定义 Schema

模块提供了一些常用的预定义 Schema：

### DATABASE_SCHEMA

```python
from mod import Config, DATABASE_SCHEMA

config = Config({
    'host': 'localhost',
    'port': 5432,
    'name': 'mydb',
    'user': 'admin',
    'password': 'secret',
    'ssl': False,
}, DATABASE_SCHEMA)
```

### SERVER_SCHEMA

```python
from mod import Config, SERVER_SCHEMA

config = Config({
    'host': '0.0.0.0',
    'port': 8080,
    'debug': False,
    'workers': 4,
}, SERVER_SCHEMA)
```

### LOGGING_SCHEMA

```python
from mod import Config, LOGGING_SCHEMA

config = Config({
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': '/var/log/app.log',
    'max_size': 10485760,
    'backup_count': 5,
}, LOGGING_SCHEMA)
```

---

## 💡 使用示例

### 完整应用配置示例

```python
from mod import Config, create_schema, load_config

# 定义应用 Schema
APP_SCHEMA = create_schema(
    # 服务器配置
    server_host=dict(type=str, default='0.0.0.0'),
    server_port=dict(type=int, required=True, min=1, max=65535),
    
    # 数据库配置
    db_host=dict(type=str, required=True),
    db_port=dict(type=int, default=5432),
    db_name=dict(type=str, required=True),
    db_user=dict(type=str, required=True),
    db_password=dict(type=str, required=True),
    
    # 功能开关
    debug=dict(type=bool, default=False),
    cache_enabled=dict(type=bool, default=True),
    
    # 日志配置
    log_level=dict(type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
)

# 加载配置（支持环境变量替换）
config = load_config('config.conf', schema=APP_SCHEMA, env_substitute=True)

# 使用配置
if config.get_bool('debug'):
    print("调试模式已启用")

# 构建数据库连接字符串
db_url = (
    f"postgresql://{config.get('db_user')}:{config.get('db_password')}@"
    f"{config.get('db_host')}:{config.get_int('db_port')}/{config.get('db_name')}"
)
```

### 配置文件示例 (config.conf)

```ini
# 服务器配置
server_host=0.0.0.0
server_port=${SERVER_PORT:-8080}

# 数据库配置（使用环境变量）
db_host=${DB_HOST}
db_port=${DB_PORT:-5432}
db_name=${DB_NAME}
db_user=${DB_USER}
db_password=${DB_PASSWORD}

# 功能开关
debug=${DEBUG:-false}
cache_enabled=true

# 日志配置
log_level=INFO
```

### 类型转换示例

```python
config = Config({
    'count': '42',              # 字符串
    'ratio': '3.14159',         # 字符串
    'enabled': 'true',          # 字符串
    'tags': 'python,web,api',   # 逗号分隔
    'metadata': '{"version": 1}', # JSON 字符串
})

# 自动类型转换
count = config.get_int('count')      # 42 (int)
ratio = config.get_float('ratio')    # 3.14159 (float)
enabled = config.get_bool('enabled') # True (bool)
tags = config.get_list('tags')       # ['python', 'web', 'api']
metadata = config.get_dict('metadata') # {'version': 1}
```

### 不可变配置示例

```python
# 创建后设为只读
config = Config({'host': 'localhost', 'port': 8080}).freeze()

# 尝试修改会抛出异常
try:
    config.set('port', 9090)
except ConfigError as e:
    print(f"无法修改配置：{e}")
```

---

## 🧪 运行测试

```bash
cd config_utils
python config_utils_test.py
```

---

## ⚠️ 注意事项

1. **敏感信息**: 密码等敏感信息建议使用环境变量，不要硬编码在配置文件中
2. **环境变量优先级**: 环境变量替换优先于配置文件中的值
3. **类型安全**: 使用 `get_int`、`get_bool` 等方法确保类型正确
4. **验证时机**: 建议在应用启动时进行配置验证
5. **文件权限**: 包含敏感信息的配置文件应设置适当的文件权限

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
