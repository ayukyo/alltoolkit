# 文本差异比较工具 (text_diff_utils)

一个功能完整的文本差异比较工具模块，支持多种差异检测和展示方式。

## 功能特性

- **行级差异检测** - 精确识别新增、删除、修改的行
- **字符级差异检测** - 细粒度的字符变更追踪
- **统一格式差异** - 生成类似 `git diff` 的标准差异报告
- **并排对比视图** - 直观的双栏对比展示
- **相似度计算** - 量化文本相似程度
- **差异统计** - 详细的变更数据统计
- **公共子串查找** - 发现两段文本的共同部分
- **忽略选项** - 支持忽略大小写、空白字符、空行

## 零外部依赖

仅使用 Python 标准库，无需安装任何第三方包。

## 安装

```bash
# 直接复制 mod.py 到项目中即可使用
cp mod.py your_project/text_diff_utils.py
```

## 快速开始

### 基本文本比较

```python
from mod import compare_texts, format_diff_summary

old_text = """Line 1
Line 2
Line 3"""

new_text = """Line 1
Line 2 modified
Line 3
Line 4"""

result = compare_texts(old_text, new_text)
print(format_diff_summary(result))
```

输出：
```
=== 差异摘要 ===
原文本行数: 3
新文本行数: 4
新增行数: 1
删除行数: 0
修改行数: 1
相似度: 60.00%
```

### 生成统一格式差异

```python
from mod import get_unified_diff

diff = get_unified_diff(old_text, new_text, "old.txt", "new.txt")
print(diff)
```

输出：
```diff
--- old.txt
+++ new.txt
@@ -1,3 +1,4 @@
 Line 1
-Line 2
+Line 2 modified
 Line 3
+Line 4
```

### 并排对比

```python
from mod import TextDiffUtils, format_side_by_side

utils = TextDiffUtils()
pairs = utils.side_by_side(old_text, new_text)
print(format_side_by_side(pairs, "文本对比"))
```

输出：
```
=== 文本对比 ===
原文本                         |  新文本
---------------------------------------  |  ---------------------------------------
Line 1                          |  Line 1                           
Line 2                        ~   Line 2 modified                   
Line 3                          |  Line 3                           
                                +  Line 4                           
```

### 字符级差异

```python
from mod import TextDiffUtils, DiffType

utils = TextDiffUtils()
diffs = utils.char_diff("Hello World", "Hello Python")

for diff_type, text in diffs:
    if diff_type == DiffType.EQUAL:
        print(f"= {text!r}")
    elif diff_type == DiffType.DELETE:
        print(f"- {text!r}")
    else:
        print(f"+ {text!r}")
```

输出：
```
= 'Hello '
- 'World'
+ 'Python'
```

### 相似度计算

```python
from mod import get_similarity

sim = get_similarity("Hello World", "Hello Python")
print(f"相似度: {sim:.2%}")  # 相似度: 46.15%
```

### 差异统计

```python
from mod import TextDiffUtils

utils = TextDiffUtils()
stats = utils.diff_stats(old_text, new_text)

print(f"原文本行数: {stats['old_lines']}")
print(f"新文本行数: {stats['new_lines']}")
print(f"新增行数: {stats['added_lines']}")
print(f"删除行数: {stats['deleted_lines']}")
print(f"修改行数: {stats['changed_lines']}")
print(f"相似度: {stats['similarity']}%")
print(f"是否相同: {stats['is_identical']}")
```

### 忽略选项

```python
from mod import TextDiffUtils

# 忽略大小写
utils = TextDiffUtils(ignore_case=True)
sim = utils.similarity("HELLO", "hello")  # 1.0

# 忽略空白字符
utils = TextDiffUtils(ignore_whitespace=True)
sim = utils.similarity("Hello  World", "Hello World")  # 1.0

# 忽略空行
utils = TextDiffUtils(ignore_blank_lines=True)
result = utils.compare_lines("Line 1\n\nLine 2", "Line 1\nLine 2")

# 组合使用
utils = TextDiffUtils(ignore_case=True, ignore_whitespace=True)
```

### 查找公共子串

```python
from mod import TextDiffUtils

utils = TextDiffUtils()
matches = utils.find_matches(
    "The quick brown fox",
    "The quick brown cat",
    min_length=5
)

for substring, pos_a, pos_b in matches:
    print(f"'{substring}' at A:{pos_a}, B:{pos_b}")
```

## API 参考

### TextDiffUtils 类

主工具类，提供所有差异比较功能。

#### 构造函数

```python
TextDiffUtils(
    ignore_case: bool = False,      # 忽略大小写
    ignore_whitespace: bool = False, # 忽略空白字符
    ignore_blank_lines: bool = False # 忽略空行
)
```

#### 方法

| 方法 | 说明 | 返回类型 |
|------|------|----------|
| `compare_lines(old_text, new_text)` | 比较两段文本的行级差异 | `DiffResult` |
| `unified_diff(old_text, new_text, ...)` | 生成统一格式差异报告 | `str` |
| `side_by_side(old_text, new_text, width)` | 生成并排对比视图 | `List[Tuple[str, str, str]]` |
| `char_diff(old_text, new_text)` | 字符级差异检测 | `List[Tuple[DiffType, str]]` |
| `similarity(old_text, new_text)` | 计算文本相似度 | `float` |
| `diff_stats(old_text, new_text)` | 获取差异统计信息 | `Dict` |
| `find_matches(old_text, new_text, min_length)` | 查找公共子串 | `List[Tuple[str, int, int]]` |

### 便捷函数

```python
compare_texts(old_text, new_text, ignore_case, ignore_whitespace) -> DiffResult
get_unified_diff(old_text, new_text, old_filename, new_filename) -> str
get_similarity(old_text, new_text) -> float
format_diff_summary(result: DiffResult) -> str
format_side_by_side(pairs, title) -> str
```

### 数据类

#### DiffResult

```python
@dataclass
class DiffResult:
    old_lines: int           # 原文本行数
    new_lines: int           # 新文本行数
    added_lines: int         # 新增行数
    deleted_lines: int       # 删除行数
    changed_lines: int       # 修改行数
    similarity: float        # 相似度 (0.0 - 1.0)
    diff_lines: List[DiffLine]  # 差异行列表
```

#### DiffLine

```python
@dataclass
class DiffLine:
    line_number_old: Optional[int]  # 原文件行号
    line_number_new: Optional[int]  # 新文件行号
    content: str                      # 行内容
    diff_type: DiffType               # 差异类型
```

#### DiffType 枚举

```python
class DiffType(Enum):
    EQUAL = "equal"      # 相同
    INSERT = "insert"    # 新增
    DELETE = "delete"    # 删除
    REPLACE = "replace"  # 替换
```

## 使用场景

- **版本控制** - 比较文件版本差异
- **配置管理** - 检测配置文件变更
- **代码审查** - 展示代码修改
- **文档对比** - 比较文档版本
- **数据校验** - 验证数据一致性
- **自动化测试** - 比较期望输出与实际输出

## 运行测试

```bash
python -m pytest test_mod.py -v
```

或直接运行：

```bash
python test_mod.py
```

## 运行示例

```bash
python example.py
```

## 许可证

MIT License