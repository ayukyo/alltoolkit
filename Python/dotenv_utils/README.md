# dotenv Utils 📄

`.env` 文件解析和序列化工具模块，支持环境变量配置文件的读写。

## 功能特性

- **解析 .env 文件** - 将 .env 格式字符串解析为字典
- **序列化** - 将字典转换为 .env 格式字符串
- **变量插值** - 支持 `${VAR}` 和 `$VAR` 格式的变量引用
- **多行值** - 支持反斜杠换行延续
- **注释支持** - 支持行注释和行内注释
- **引号处理** - 支持单引号和双引号
- **export 前缀** - 自动处理 export 关键字
- **零外部依赖** - 纯 Python 实现

## 快速开始

```python
from dotenv_utils import parse, serialize, load

# 解析 .env 字符串
content = '''
# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME="mydb"

# API 密钥（带引号）
API_KEY='secret-key-123'
'''
env = parse(content)
print(env)
# {'DB_HOST': 'localhost', 'DB_PORT': '5432', 'DB_NAME': 'mydb', 'API_KEY': 'secret-key-123'}

# 序列化字典为 .env 格式
env = {'DEBUG': 'true', 'PORT': '8080'}
output = serialize(env)
print(output)
# DEBUG=true
# PORT=8080
```

## parse 函数

### 基本解析

```python
from dotenv_utils import parse

# 键值对
env = parse("FOO=bar")
print(env)  # {'FOO': 'bar'}

# 带空格的值的引号
env = parse('MESSAGE="hello world"')
print(env)  # {'MESSAGE': 'hello world'}

# 单引号保留内容
env = parse("PATH='/usr/local/bin'")
print(env)  # {'PATH': '/usr/local/bin'}
```

### 注释处理

```python
from dotenv_utils import parse

content = '''
# 这是注释
FOO=bar    # 行内注释
BAZ=qux
'''
env = parse(content)
# {'FOO': 'bar', 'BAZ': 'qux'}
```

### 多行值

```python
from dotenv_utils import parse

content = '''
MULTILINE="第一行\
第二行\
第三行"
'''
env = parse(content)
# {'MULTILINE': '第一行第二行第三行'}
```

### 变量插值

```python
from dotenv_utils import parse

content = '''
BASE_DIR=/app
DATA_DIR=$BASE_DIR/data
CONFIG_PATH=${BASE_DIR}/config.json
'''
env = parse(content)
# {'BASE_DIR': '/app', 'DATA_DIR': '/app/data', 'CONFIG_PATH': '/app/config.json'}
```

### export 前缀

```python
from dotenv_utils import parse

content = '''
export API_KEY=secret
export DB_HOST=localhost
'''
env = parse(content)
# {'API_KEY': 'secret', 'DB_HOST': 'localhost'}
```

## serialize 函数

### 基本序列化

```python
from dotenv_utils import serialize

env = {
    'DEBUG': 'true',
    'PORT': '8080',
    'HOST': 'localhost'
}
output = serialize(env)
print(output)
# DEBUG=true
# HOST=localhost
# PORT=8080
```

### 带空格的值的引号处理

```python
from dotenv_utils import serialize

env = {
    'MESSAGE': 'hello world',    # 带空格，需要引号
    'SIMPLE': 'value',            # 无空格，无引号
    'WITH_QUOTE': 'say "hi"',     # 包含引号
}
output = serialize(env)
```

### 特殊字符处理

```python
from dotenv_utils import serialize

env = {
    'NEWLINE': 'line1\nline2',
    'TAB': 'col1\tcol2',
    'BACKSLASH': 'path\\to\\file'
}
output = serialize(env)
# 自动转义特殊字符
```

## load 函数

```python
from dotenv_utils import load
import os

# 加载 .env 文件到环境变量
load('.env')

# 或者手动设置
os.environ['FOO'] = 'bar'
```

## 完整示例

```python
from dotenv_utils import parse, serialize

# 模拟 .env 文件内容
env_content = '''
# Database Configuration
DB_ENGINE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=admin
DB_PASSWORD='p@ssw0rd!'

# Redis Configuration
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# Application Settings
DEBUG=true
SECRET_KEY="a1b2c3d4e5f6"
ALLOWED_HOSTS=localhost,127.0.0.1
'''

# 解析
config = parse(env_content)
print(config['DB_NAME'])  # myapp
print(config['DEBUG'])     # true

# 修改配置
config['DEBUG'] = 'false'

# 序列化回 .env 格式
output = serialize(config)
print(output)
```

## 主要函数

| 函数 | 说明 |
|------|------|
| `parse(content)` | 解析 .env 格式字符串为字典 |
| `serialize(env)` | 将字典序列化为 .env 格式字符串 |
| `load(path)` | 加载 .env 文件并设置到环境变量 |

## 测试

```bash
python -m pytest Python/dotenv_utils/ -v
```

## 许可证

MIT License