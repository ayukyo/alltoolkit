# Changelog Utils

变更日志解析、生成和管理工具模块。

## 功能

- **解析 CHANGELOG.md** - 支持 Keep a Changelog 格式
- **生成标准化变更日志** - 自动格式化输出
- **版本信息提取** - 解析语义化版本
- **版本比较** - 比较版本差异和变更
- **格式转换** - Markdown、JSON、纯文本
- **版本排序和验证** - 自动排序和验证
- **发布说明生成** - 自动生成发布说明

## 安装

```python
from changelog_utils.mod import ChangelogParser, ChangelogGenerator, Version
```

## 快速开始

### 解析变更日志

```python
from changelog_utils.mod import ChangelogParser

# 从文件解析
parser = ChangelogParser()
changelog = parser.parse_file('CHANGELOG.md')

# 从字符串解析
changelog = parser.parse("""
## [1.0.0] - 2024-01-01
### Added
- Initial release
""")

# 获取所有版本
versions = changelog.get_versions()
print(versions)  # [Version(1, 0, 0)]

# 获取特定版本的变更
changes = changelog.get_changes(versions[0])
```

### 生成变更日志

```python
from changelog_utils.mod import ChangelogGenerator, ChangeType

generator = ChangelogGenerator()

# 添加版本
generator.add_version('1.0.0', date='2024-01-01')
generator.add_change('1.0.0', ChangeType.ADDED, 'Initial release')
generator.add_change('1.0.0', ChangeType.FIXED, 'Bug fix')

# 生成 Markdown
markdown = generator.to_markdown()
print(markdown)
```

### 版本操作

```python
from changelog_utils.mod import Version

# 创建版本
v1 = Version(1, 0, 0)
v2 = Version(1, 1, 0)

# 版本比较
print(v1 < v2)  # True
print(v1 == Version(1, 0, 0))  # True

# 版本字符串
print(str(v1))  # "1.0.0"

# 预发布版本
v_pre = Version(1, 0, 0, prerelease='alpha.1')
print(str(v_pre))  # "1.0.0-alpha.1"
```

### 变更类型

支持 Keep a Changelog 标准变更类型：

- `ADDED` - 新功能
- `CHANGED` - 功能变更
- `DEPRECATED` - 废弃功能
- `REMOVED` - 移除功能
- `FIXED` - Bug 修复
- `SECURITY` - 安全修复

### 格式转换

```python
from changelog_utils.mod import ChangelogParser

parser = ChangelogParser()
changelog = parser.parse_file('CHANGELOG.md')

# 转换为 JSON
json_data = changelog.to_json()

# 转换为纯文本
text = changelog.to_text()
```

## API 参考

### ChangelogParser

| 方法 | 说明 |
|------|------|
| `parse_file(path)` | 从文件解析变更日志 |
| `parse(text)` | 从字符串解析变更日志 |

### ChangelogGenerator

| 方法 | 说明 |
|------|------|
| `add_version(version, date)` | 添加版本 |
| `add_change(version, change_type, description)` | 添加变更 |
| `to_markdown()` | 生成 Markdown 格式 |
| `to_json()` | 生成 JSON 格式 |

### Version

| 方法/属性 | 说明 |
|-----------|------|
| `major`, `minor`, `patch` | 版本号组成部分 |
| `prerelease` | 预发布标识 |
| `build` | 构建元数据 |
| `__str__()` | 字符串表示 |
| `__eq__`, `__lt__`, ... | 版本比较 |

## 测试

```bash
cd Python/changelog_utils
python changelog_utils_test.py
```

测试覆盖率：57 个测试用例，100% 通过 ✅

## 许可证

MIT License