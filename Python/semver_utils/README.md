# semver_utils - 语义版本工具

语义版本号解析、比较、验证工具。遵循 [Semantic Versioning 2.0.0](https://semver.org/) 规范。

## 功能

### 版本解析
- 解析语义版本字符串，提取 major、minor、patch、prerelease、build_metadata
- 支持预发布标识符和构建元数据
- 自动识别数值和字符串预发布标识符

### 版本比较
- 支持 `>`, `<`, `>=`, `<=`, `==`, `!=` 比较操作
- 正确处理预发布版本比较规则
- 正式版本 > 预发布版本
- 数字标识符 < 字符串标识符

### 版本验证
- 验证字符串是否符合 SemVer 2.0.0 规范
- 详细错误信息返回

### 版本递增
- `increment_major`: 递增主版本号
- `increment_minor`: 递增次版本号
- `increment_patch`: 递增修订版本号
- `increment_prerelease`: 递增预发布版本

### 版本范围匹配
- 插入号范围 `^1.2.3`: 主版本兼容
- 波浪号范围 `~1.2.3`: 次版本兼容
- 比较运算符 `>=`, `<`, 等
- 通配符 `1.x`, `1.2.*`
- 范围 `1.0.0 - 2.0.0`

### 其他功能
- 版本排序
- 版本差异检测
- 版本变更类型判断
- 版本强制转换（从不规范字符串）
- 最佳版本选择

## 快速开始

```python
from mod import parse, compare, satisfies, increment_major

# 解析版本
v = parse("1.2.3-alpha.1+build.123")
print(v.major)      # 1
print(v.minor)      # 2
print(v.patch)      # 3
print(v.prerelease) # ['alpha', 1]
print(v.build_metadata)  # 'build.123'

# 比较版本
compare("1.0.0", "2.0.0")  # -1 (小于)
compare("2.0.0", "1.0.0")  # 1 (大于)
compare("1.0.0", "1.0.0")  # 0 (相等)

# 版本范围匹配
satisfies("1.2.3", "^1.0.0")  # True
satisfies("2.0.0", "^1.0.0")  # False

# 版本递增
increment_major("1.2.3")  # "2.0.0"
increment_minor("1.2.3")  # "1.3.0"
increment_patch("1.2.3")  # "1.2.4"
```

## API 文档

### 解析函数

#### `parse(version_string: str) -> SemanticVersion`
解析语义版本字符串，返回 SemanticVersion 对象。

```python
v = parse("1.2.3-alpha.1+build.123")
```

#### `is_valid(version_string: str) -> bool`
验证字符串是否为有效的语义版本。

#### `validate(version_string: str) -> Tuple[bool, Optional[str]]`
详细验证，返回 (是否有效, 错误信息)。

#### `coerce(version_string: str) -> Optional[SemanticVersion]`
尝试将不规范字符串强制转换为版本对象。

```python
coerce("v1.2.3")  # SemanticVersion(1.2.3)
coerce("1.2")     # SemanticVersion(1.2.0)
```

### 比较函数

#### `compare(v1: str, v2: str) -> int`
比较两个版本，返回 -1/0/1。

#### `gt(v1: str, v2: str) -> bool`
大于比较。

#### `gte(v1: str, v2: str) -> bool`
大于等于比较。

#### `lt(v1: str, v2: str) -> bool`
小于比较。

#### `lte(v1: str, v2: str) -> bool`
小于等于比较。

#### `eq(v1: str, v2: str) -> bool`
相等比较（忽略构建元数据）。

#### `neq(v1: str, v2: str) -> bool`
不等比较。

### 递增函数

#### `increment_major(version: str) -> str`
递增主版本号，重置 minor/patch 为 0。

#### `increment_minor(version: str) -> str`
递增次版本号，重置 patch 为 0。

#### `increment_patch(version: str) -> str`
递增修订版本号。

#### `increment_prerelease(version: str, identifier: str = "rc") -> str`
递增预发布版本。

#### `next_version(version: str, release_type: str) -> str`
获取下一个版本，release_type 为 "major"/"minor"/"patch"/"prerelease"。

### 范围匹配函数

#### `satisfies(version: str, range_str: str) -> bool`
检查版本是否满足版本范围约束。

支持的格式：
- 精确匹配：`"1.2.3"`
- 比较运算符：`">1.0.0"`, `">=1.0.0"`, `"<2.0.0"`, `"<=2.0.0"`
- 插入号范围：`"^1.2.3"` (主版本兼容)
- 波浪号范围：`"~1.2.3"` (次版本兼容)
- 通配符：`"1.x"`, `"1.2.*"`
- 范围：`"1.0.0 - 2.0.0"`
- 复合条件：`">=1.0.0 <2.0.0"`

#### `max_satisfying(versions: List[str], range_str: str) -> Optional[str]`
在版本列表中找到满足范围的最大版本。

#### `min_satisfying(versions: List[str], range_str: str) -> Optional[str]`
在版本列表中找到满足范围的最小版本。

### 工具函数

#### `major(version: str) -> int`
获取主版本号。

#### `minor(version: str) -> int`
获取次版本号。

#### `patch(version: str) -> int`
获取修订版本号。

#### `prerelease(version: str) -> Optional[List[Union[str, int]]]`
获取预发布标识符。

#### `build_metadata(version: str) -> Optional[str]`
获取构建元数据。

#### `diff(v1: str, v2: str) -> Optional[str]`
获取版本差异类型：`"major"`, `"minor"`, `"patch"`, `"prerelease"`, `None`。

#### `get_change_type(from_version: str, to_version: str) -> str`
获取版本变更类型：`"major"`, `"minor"`, `"patch"`, `"prerelease"`, `"none"`, `"downgrade"`。

#### `sort_versions(versions: List[str], reverse: bool = False) -> List[str]`
对版本列表排序。

#### `create(major, minor, patch, prerelease=None, build_metadata=None) -> SemanticVersion`
创建 SemanticVersion 对象。

### SemanticVersion 类

```python
class SemanticVersion:
    major: int
    minor: int
    patch: int
    prerelease: Optional[List[Union[str, int]]]
    build_metadata: Optional[str]
    
    def __str__(self) -> str          # 转换为字符串
    def __eq__(self, other) -> bool   # 相等比较
    def __lt__(self, other) -> bool   # 小于比较
    def __le__(self, other) -> bool   # 小于等于比较
    def __gt__(self, other) -> bool   # 大于比较
    def __ge__(self, other) -> bool   # 大于等于比较
    def __hash__(self) -> int         # 哈希值（可用于 set/dict）
    
    def to_tuple(self) -> Tuple[int, int, int]  # 转换为元组
    def is_prerelease(self) -> bool             # 是否为预发布版本
    def is_stable(self) -> bool                 # 是否为稳定版本
```

## 版本范围规则

### 插入号范围 (^)
- `^1.2.3` := `>=1.2.3 <2.0.0` (主版本不变)
- `^0.2.3` := `>=0.2.3 <0.3.0` (次版本不变，因为 major=0)
- `^0.0.3` := `>=0.0.3 <0.0.4` (patch 不变，因为 major=minor=0)

### 波浪号范围 (~)
- `~1.2.3` := `>=1.2.3 <1.3.0` (次版本不变)

### 预发布版本比较规则
1. 正式版本 > 预发布版本
2. 预发布标识符从左到右逐个比较
3. 数字标识符 < 字符串标识符
4. 短列表 < 长列表（相同前缀时）

示例：
- `1.0.0` > `1.0.0-alpha`
- `1.0.0-alpha` < `1.0.0-beta`
- `1.0.0-alpha` < `1.0.0-alpha.1`
- `1.0.0-1` < `1.0.0-alpha`

## 测试

```bash
python semver_utils_test.py
```

测试覆盖：
- 版本解析（20+ 测试）
- 版本比较（15+ 测试）
- 版本递增（10+ 测试）
- 版本范围匹配（20+ 测试）
- 边界值测试
- Unicode 和特殊字符测试

## 示例

```bash
python examples/usage_examples.py
```

## 零依赖

仅使用 Python 标准库：
- `re` (正则表达式)
- `dataclasses` (数据类)
- `typing` (类型注解)

## SemVer 2.0.0 规范参考

完整规范请参考：https://semver.org/

核心规则：
- 版本格式：`MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`
- 各部分只能是非负整数，不允许前导零
- 预发布标识符由字母数字和连字符组成，用点分隔
- 构建元数据不影响版本比较

## 许可证

MIT License