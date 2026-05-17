# semver_utils

语义化版本（SemVer）工具库，完全遵循 [Semantic Versioning 2.0.0](https://semver.org/) 规范。

## ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **完整 SemVer 支持** - 主版本、次版本、修订版本、预发布标识、构建元数据
- **版本比较** - 完整的比较运算符支持
- **版本递增** - major/minor/patch 递增，支持预发布版本
- **版本范围** - 支持 npm 风格的范围语法（^、~、>=、<、x 通配符等）
- **版本排序** - 按语义化版本规范排序
- **版本差异** - 分析两个版本之间的差异

## 🚀 快速开始

### 解析版本

```python
from mod import parse, SemVer

# 解析版本字符串
v = parse("1.2.3")
print(v)  # 1.2.3

# 解析完整版本
v = parse("2.0.0-alpha.1+build.123")
print(v.major)       # 2
print(v.minor)       # 0
print(v.patch)       # 0
print(v.prerelease)  # "alpha.1"
print(v.build)       # "build.123"

# 直接创建
v = SemVer(1, 2, 3, "beta", "exp.sha.123")
```

### 版本比较

```python
from mod import compare, equals, greater_than, less_than, gte, lte

# 比较
compare("1.0.0", "2.0.0")  # -1
compare("2.0.0", "1.0.0")  # 1
compare("1.0.0", "1.0.0")  # 0

# 便捷函数
equals("1.0.0", "1.0.0")       # True
greater_than("2.0.0", "1.0.0") # True
less_than("1.0.0", "2.0.0")    # True
gte("1.0.0", "1.0.0")         # True
lte("1.0.0", "2.0.0")         # True

# 使用运算符
v1 = parse("1.0.0")
v2 = parse("2.0.0")
v1 < v2   # True
v1 == v2  # False
```

### 版本递增

```python
from mod import parse

v = parse("1.2.3")

# 递增版本
v.bump_major()  # 2.0.0
v.bump_minor()  # 1.3.0
v.bump_patch()  # 1.2.4

# 预发布版本
v.bump_prerelease("alpha")  # 1.2.3-alpha.1
v.bump_prerelease("beta")   # 1.2.3-beta.1

# 设置预发布标识和构建元数据
v.with_prerelease("rc.1")  # 1.2.3-rc.1
v.with_build("123")        # 1.2.3+123

# 移除预发布标识（发布正式版本）
v = parse("1.2.3-alpha.1")
v.release()  # 1.2.3
```

### 版本排序

```python
from mod import sort, rsort, min_version, max_version

versions = ["2.0.0", "1.0.0", "1.1.0", "1.0.0-alpha"]

# 升序排序
sorted_v = sort(versions)
# [1.0.0-alpha, 1.0.0, 1.1.0, 2.0.0]

# 降序排序
rsorted_v = rsort(versions)
# [2.0.0, 1.1.0, 1.0.0, 1.0.0-alpha]

# 最小/最大版本
min_version(versions)  # 1.0.0-alpha
max_version(versions)  # 2.0.0
```

### 版本范围匹配

```python
from mod import parse_range, satisfies, filter_versions, find_best_match

# 解析范围
r = parse_range("^1.2.3")
r.contains("1.2.3")  # True
r.contains("1.9.9") # True
r.contains("2.0.0")  # False

# 支持的范围语法
parse_range("*")         # 所有版本
parse_range("1.2.3")     # 精确版本
parse_range(">=1.0.0")    # 大于等于
parse_range(">1.0.0")     # 大于
parse_range("<=2.0.0")    # 小于等于
parse_range("<2.0.0")     # 小于
parse_range(">=1.0.0 <2.0.0")  # 范围
parse_range("^1.2.3")     # 兼容版本 (>=1.2.3 <2.0.0)
parse_range("~1.2.3")     # 补丁范围 (>=1.2.3 <1.3.0)
parse_range("~1.2")       # 次版本范围 (>=1.2.0 <1.3.0)
parse_range("1.2.x")      # 通配符 (>=1.2.0 <1.3.0)

# 检查版本是否满足约束
satisfies("1.2.3", "^1.0.0")  # True
satisfies("2.0.0", "^1.0.0")  # False

# 过滤版本列表
versions = ["1.0.0", "1.1.0", "2.0.0"]
filtered = filter_versions(versions, ">=1.0.0 <2.0.0")
# [1.0.0, 1.1.0]

# 查找最佳匹配（最高版本）
find_best_match(versions, "^1.0.0")  # 1.1.0
```

### 版本差异分析

```python
from mod import diff

d = diff("1.2.3", "2.0.0")
print(d.major_diff)  # 1
print(d.minor_diff)  # -2
print(d.patch_diff)  # -3
print(d.is_upgrade)  # True
print(d.is_major_change)  # True

d = diff("2.0.0", "1.0.0")
print(d.is_downgrade)  # True
```

## 📖 API 参考

### SemVer 类

| 属性/方法 | 说明 |
|-----------|------|
| `major` | 主版本号 |
| `minor` | 次版本号 |
| `patch` | 修订版本号 |
| `prerelease` | 预发布标识 |
| `build` | 构建元数据 |
| `is_prerelease` | 是否为预发布版本 |
| `is_stable` | 是否为稳定版本 |
| `bump_major()` | 递增主版本 |
| `bump_minor()` | 递增次版本 |
| `bump_patch()` | 递增修订版本 |
| `bump_prerelease()` | 递增预发布版本 |
| `with_prerelease()` | 设置预发布标识 |
| `with_build()` | 设置构建元数据 |
| `release()` | 返回正式版本 |

### 解析函数

| 函数 | 说明 |
|------|------|
| `parse(version)` | 解析版本字符串 |
| `try_parse(version)` | 安全解析，失败返回 None |
| `is_valid(version)` | 验证版本字符串 |

### 比较函数

| 函数 | 说明 |
|------|------|
| `compare(v1, v2)` | 比较两个版本 |
| `equals(v1, v2)` | 判断相等 |
| `greater_than(v1, v2)` | 判断 v1 > v2 |
| `less_than(v1, v2)` | 判断 v1 < v2 |
| `gte(v1, v2)` | 判断 v1 >= v2 |
| `lte(v1, v2)` | 判断 v1 <= v2 |

### 排序函数

| 函数 | 说明 |
|------|------|
| `sort(versions)` | 升序排序 |
| `rsort(versions)` | 降序排序 |
| `min_version(versions)` | 最小版本 |
| `max_version(versions)` | 最大版本 |

### 范围函数

| 函数 | 说明 |
|------|------|
| `parse_range(range_str)` | 解析范围字符串 |
| `satisfies(version, range_str)` | 检查是否满足约束 |
| `filter_versions(versions, range_str)` | 过滤版本列表 |
| `find_best_match(versions, range_str)` | 查找最佳匹配 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `diff(v1, v2)` | 计算版本差异 |
| `format(version)` | 格式化版本 |
| `to_tuple(version)` | 转换为元组 |
| `from_tuple(t)` | 从元组创建版本 |
| `unique(versions)` | 去重版本列表 |
| `next_versions(version)` | 可能的下一个版本列表 |

## 📋 范围语法

| 语法 | 含义 | 示例 |
|------|------|------|
| `*` | 所有版本 | `*` |
| `1.2.3` | 精确版本 | `1.2.3` |
| `>=1.0.0` | 大于等于 | `>=1.0.0` |
| `>1.0.0` | 大于 | `>1.0.0` |
| `<=2.0.0` | 小于等于 | `<=2.0.0` |
| `<2.0.0` | 小于 | `<2.0.0` |
| `>=1.0.0 <2.0.0` | 范围 | `>=1.0.0 <2.0.0` |
| `^1.2.3` | 兼容版本 | `>=1.2.3 <2.0.0` |
| `^0.2.3` | 兼容版本(0.x) | `>=0.2.3 <0.3.0` |
| `~1.2.3` | 补丁范围 | `>=1.2.3 <1.3.0` |
| `~1.2` | 次版本范围 | `>=1.2.0 <1.3.0` |
| `1.2.x` | 通配符 | `>=1.2.0 <1.3.0` |

## 🔬 测试

```bash
python Python/semver_utils/semver_utils_test.py
```

测试覆盖：
- 版本解析与验证
- 版本比较（含预发布版本）
- 版本递增
- 版本排序
- 版本范围匹配
- 版本差异分析
- 边界值测试

## 📝 示例

```bash
python Python/semver_utils/examples/usage_examples.py
```

## 📄 许可证

MIT License