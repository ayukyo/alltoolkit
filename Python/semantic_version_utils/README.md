# Semantic Version Utilities - 语义版本控制工具

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

零依赖、生产就绪的语义版本控制工具模块，完整实现 SemVer 2.0.0 规范。

## 功能特性

- **版本解析**：解析语义版本字符串（支持预发布和构建元数据）
- **版本比较**：支持 `<`, `>`, `<=`, `>=`, `==`, `!=` 操作符
- **范围匹配**：支持版本范围表达式（如 `^1.2.3`, `~2.0.0`, `>=1.0.0 <2.0.0`）
- **版本递增**：自动递增 major、minor、patch、prerelease
- **排序**：对版本集合进行排序
- **兼容性检查**：检查版本兼容性

## 安装

```bash
# 直接使用
from semantic_version_utils import SemanticVersion, parse, satisfies

# 或安装为包
pip install alltoolkit-semantic-version-utils
```

## 快速开始

### 版本解析

```python
from semantic_version_utils import parse, SemanticVersion

# 解析版本字符串
v = parse("1.2.3-alpha.1+build.123")
print(v.major)      # 1
print(v.minor)      # 2
print(v.patch)      # 3
print(v.prerelease) # 'alpha.1'
print(v.build)      # 'build.123'

# 直接创建版本对象
v = SemanticVersion(1, 2, 3, prerelease="beta", build="001")
print(v)  # '1.2.3-beta+001'
```

### 版本比较

```python
from semantic_version_utils import parse

v1 = parse("1.2.3")
v2 = parse("1.3.0")
v3 = parse("2.0.0")

# 支持所有比较操作符
print(v1 < v2)   # True
print(v1 <= v2)  # True
print(v2 < v3)   # True
print(v1 == v2)  # False

# 预发布版本比较
v_stable = parse("1.0.0")
v_prerelease = parse("1.0.0-alpha")
print(v_prerelease < v_stable)  # True（预发布版本优先级较低）
```

### 范围匹配

```python
from semantic_version_utils import parse, satisfies

v = parse("1.2.3")

# 基本范围匹配
print(satisfies(v, ">=1.0.0"))        # True
print(satisfies(v, "^1.2.0"))         # True（兼容版本）
print(satisfies(v, "~1.2.0"))         # True（近似版本）
print(satisfies(v, "1.2.3 - 1.3.0"))  # True（范围）
print(satisfies(v, ">=1.0.0 <2.0.0")) # True（复合条件）

# 使用 Range 对象
from semantic_version_utils import VersionRange
r = VersionRange("^1.2.0")
print(v in r)  # True
```

### 版本递增

```python
from semantic_version_utils import parse

v = parse("1.2.3")

# 递增操作
print(v.bump_major())      # 2.0.0
print(v.bump_minor())      # 1.3.0
print(v.bump_patch())      # 1.2.4
print(v.bump_prerelease()) # 1.2.4-0（如果没有预发布标识）
```

### 版本排序

```python
from semantic_version_utils import parse, sort_versions

versions = ["2.0.0", "1.0.0", "1.0.1", "1.0.0-alpha", "1.0.0-beta"]
sorted_versions = sort_versions(versions)
print(sorted_versions)
# ['1.0.0-alpha', '1.0.0-beta', '1.0.0', '1.0.1', '2.0.0']
```

## API 参考

### SemanticVersion

```python
SemanticVersion(
    major: int = 0,
    minor: int = 0, 
    patch: int = 0,
    prerelease: str = None,
    build: str = None
)
```

**属性**:
- `major`, `minor`, `patch`: 版本号
- `prerelease`: 预发布标识（如 `alpha`, `beta.2`）
- `build`: 构建元数据

**方法**:
- `bump_major()` → 返回新的主版本
- `bump_minor()` → 返回新的次版本
- `bump_patch()` → 返回新的补丁版本
- `bump_prerelease()` → 递增预发布版本

### parse(version_string)

解析版本字符串。

```python
>>> parse("1.2.3-alpha.1+build.123")
SemanticVersion(1.2.3-alpha.1+build.123)
```

### satisfies(version, range_string)

检查版本是否满足范围条件。

```python
>>> satisfies(parse("1.2.3"), "^1.0.0")
True
```

### sort_versions(versions)

对版本列表排序。

```python
>>> sort_versions(["2.0.0", "1.0.0", "1.0.1"])
['1.0.0', '1.0.1', '2.0.0']
```

## 范围表达式

| 表达式 | 描述 | 示例 |
|--------|------|------|
| `^1.2.3` | 兼容版本（>=1.2.3 <2.0.0） | `^1.2.3` 匹配 `1.2.3`, `1.3.0`, `1.9.9` |
| `~1.2.3` | 近似版本（>=1.2.3 <1.3.0） | `~1.2.3` 匹配 `1.2.3`, `1.2.9` |
| `>=1.0.0` | 大于等于 | `>=1.0.0` |
| `>1.0.0` | 大于 | `>1.0.0` |
| `<=1.0.0` | 小于等于 | `<=1.0.0` |
| `<1.0.0` | 小于 | `<1.0.0` |
| `1.0.0 - 2.0.0` | 范围（>=1.0.0 <=2.0.0） | `1.0.0 - 2.0.0` |
| `>=1.0.0 <2.0.0` | 复合条件 | 空格分隔多个条件 |

## 使用场景

- **包管理器**：依赖版本解析
- **API 版本控制**：兼容性检查
- **配置管理**：版本约束验证
- **发布流程**：自动化版本号管理

## 测试

```bash
python semantic_version_utils_test.py
```

## 参考

- [Semantic Versioning 2.0.0](https://semver.org/)

## 许可证

MIT License