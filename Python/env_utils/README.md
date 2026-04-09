# AllToolkit - Environment Utilities 🔧

**零依赖环境变量与配置管理工具库**

完全使用 Python 标准库实现，无需任何外部依赖。

## 功能特性

- ✅ **环境变量读写** - 获取、设置、删除环境变量
- ✅ **类型转换** - 自动转换字符串为 int/float/bool/list/json
- ✅ **.env 文件支持** - 解析、加载、保存、合并 .env 文件
- ✅ **变量验证** - 支持 required、pattern、range、choices 等验证规则
- ✅ **快照功能** - 捕获、保存、恢复、比较环境变量快照
- ✅ **敏感信息脱敏** - 自动识别并脱敏密码、密钥等敏感变量
- ✅ **环境变量展开** - 支持 `$VAR` 和 `${VAR}` 语法
- ✅ **配置插值** - 递归处理配置对象中的环境变量
- ✅ **跨平台支持** - Linux、macOS、Windows 完全兼容

## 快速开始

### 安装

无需安装！只需将 `mod.py` 复制到你的项目中即可使用。

```bash
# 方式 1: 直接复制
cp AllToolkit/Python/env_utils/mod.py your_project/

# 方式 2: 导入使用
from env_utils.mod import *
```

### 基本使用

```python
from mod import *

# 获取环境变量
home = get_env('HOME')
port = get_env('PORT', default='3000')

# 设置环境变量
set_env('MY_VAR', 'hello')

# 检查是否存在
if has_env('DATABASE_URL'):
    print("数据库已配置")

# 获取并转换类型
port = get_env_as('PORT', VarType.INTEGER, default=8080)
debug = get_env_as('DEBUG', VarType.BOOLEAN)
config = get_env_as('CONFIG', VarType.JSON)
```

### .env 文件操作

```python
# 加载 .env 文件
load_env_file('.env')

# 解析 .env 文件
env_vars = parse_env_file('.env.production')

# 保存环境变量
save_env_file('.env.backup', {'KEY': 'value'})

# 合并多个 .env 文件
merged = merge_env_files(['.env.base', '.env.local'])
```

### 变量验证

```python
# 单个变量验证
result = validate_env('PORT', [
    {'rule': 'required'},
    {'rule': 'min_value', 'value': 1024},
    {'rule': 'max_value', 'value': 65535}
])

if not result.valid:
    print(f"验证失败：{result.errors}")

# Schema 验证
schema = {
    'DATABASE_URL': {'rules': [{'rule': 'required'}]},
    'PORT': {'rules': [
        {'rule': 'required'},
        {'rule': 'min_value', 'value': 1024}
    ]},
    'ENV': {'rules': [
        {'rule': 'choices', 'value': ['development', 'production']}
    ]}
}

result = validate_env_schema(schema)
```

### 快照功能

```python
# 捕获快照
snapshot = capture_snapshot('部署前快照')

# 保存快照
save_snapshot(snapshot, 'snapshot_before_deploy.json')

# 加载快照
snapshot = load_snapshot('snapshot_before_deploy.json')

# 比较差异
before = load_snapshot('before.json')
after = load_snapshot('after.json')
diff = diff_snapshots(before, after)

print(f"新增：{diff['added']}")
print(f"删除：{diff['removed']}")
print(f"修改：{diff['changed']}")

# 恢复快照
restore_snapshot(snapshot)
```

### 敏感信息处理

```python
# 脱敏变量
vars = {
    'DATABASE_PASSWORD': 'secret123',
    'API_KEY': 'key-abc-123',
    'APP_NAME': 'MyApp'
}

masked = mask_sensitive_vars(vars)
# 输出:
# {
#   'DATABASE_PASSWORD': 'se******23',
#   'API_KEY': 'ke*********23',
#   'APP_NAME': 'MyApp'
# }

# 安全转储（用于日志）
safe_dump = get_safe_env_dump()
print(safe_dump)  # 敏感信息已脱敏
```

### 环境变量展开

```python
# 展开文本中的变量
os.environ['HOME'] = '/home/user'
text = expand_env_vars('Path: $HOME/documents')
# 结果：'Path: /home/user/documents'

text = expand_env_vars('Value: ${NONEXISTENT:-default}')
# 结果：'Value: default'

# 递归插值配置
config = {
    'database': {
        'host': '${DB_HOST}',
        'port': '${DB_PORT}'
    }
}
result = interpolate_env_vars(config)
```

## API 参考

### 环境变量读写

| 函数 | 描述 |
|------|------|
| `get_env(name, default, required)` | 获取环境变量 |
| `set_env(name, value)` | 设置环境变量 |
| `delete_env(name)` | 删除环境变量 |
| `has_env(name)` | 检查变量是否存在 |
| `get_all_env()` | 获取所有环境变量 |
| `clear_env(names)` | 清除环境变量 |

### 类型转换

| 函数 | 描述 |
|------|------|
| `convert_value(value, var_type)` | 转换字符串为指定类型 |
| `get_env_as(name, var_type, default)` | 获取并转换类型 |

支持类型：`VarType.STRING`, `VarType.INTEGER`, `VarType.FLOAT`, `VarType.BOOLEAN`, `VarType.LIST`, `VarType.JSON`

### .env 文件操作

| 函数 | 描述 |
|------|------|
| `parse_env_file(filepath)` | 解析 .env 文件 |
| `load_env_file(filepath, override)` | 加载 .env 到环境变量 |
| `save_env_file(filepath, variables)` | 保存环境变量到文件 |
| `merge_env_files(filepaths, output)` | 合并多个 .env 文件 |

### 验证

| 函数 | 描述 |
|------|------|
| `validate_env(name, rules)` | 验证单个变量 |
| `validate_env_schema(schema)` | 根据 schema 验证多个变量 |

验证规则：`required`, `not_empty`, `min_length`, `max_length`, `pattern`, `choices`, `min_value`, `max_value`

### 快照

| 函数 | 描述 |
|------|------|
| `capture_snapshot(description)` | 捕获当前快照 |
| `save_snapshot(snapshot, filepath)` | 保存快照到文件 |
| `load_snapshot(filepath)` | 从文件加载快照 |
| `restore_snapshot(snapshot, clear_first)` | 恢复快照 |
| `diff_snapshots(before, after)` | 比较两个快照 |

### 敏感信息

| 函数 | 描述 |
|------|------|
| `mask_sensitive_vars(variables, patterns)` | 脱敏敏感变量 |
| `get_safe_env_dump(patterns)` | 获取安全转储 |

### 工具函数

| 函数 | 描述 |
|------|------|
| `expand_env_vars(text, default)` | 展开文本中的变量 |
| `interpolate_env_vars(config)` | 递归插值配置 |
| `get_env_tree(prefix)` | 获取树状结构 |
| `is_production()` | 检查是否生产环境 |
| `is_development()` | 检查是否开发环境 |
| `is_testing()` | 检查是否测试环境 |
| `get_app_info()` | 获取应用信息 |
| `require_envs(*names)` | 要求多个变量存在 |

## 命令行使用

```bash
# 获取环境变量
python mod.py get HOME

# 设置环境变量
python mod.py set MY_VAR hello

# 列出环境变量
python mod.py list [PATTERN]

# 加载 .env 文件
python mod.py load .env

# 保存环境变量
python mod.py save .env.backup

# 脱敏输出
python mod.py mask

# 捕获快照
python mod.py snapshot
```

## 示例

查看 `examples/` 目录中的完整示例代码。

## 测试

运行测试套件：

```bash
cd AllToolkit/Python/env_utils
python env_utils_test.py
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
