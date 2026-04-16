# 文本差异比较工具集开发报告

## 模块信息

- **模块名称**: text_diff_utils (文本差异比较工具集)
- **位置**: Python/text_diff_utils/
- **开发语言**: Python 3
- **开发日期**: 2026-04-16 21:00

## 核心功能列表

### 1. 差异比较算法 (3 种粒度)

- `diff_lines()` - 按行比较文本，支持忽略空白和大小写
- `diff_words()` - 按单词比较文本
- `diff_chars()` - 按字符比较文本

### 2. 格式化输出 (4 种格式)

- `unified_diff()` - 统一差异格式（git diff 风格）
- `context_diff()` - 上下文差异格式
- `html_diff()` - HTML 并排显示差异（带样式）
- `inline_diff()` - 内联差异格式（自定义前缀）

### 3. 相似度计算 (4 种方法)

- `similarity_ratio()` - 基于 difflib 的相似度（0-1）
- `levenshtein_distance()` - Levenshtein 编辑距离
- `normalized_levenshtein()` - 归一化编辑距离
- `lcs()` / `lcs_length()` - 最长公共子序列

### 4. 补丁功能

- `create_patch()` - 创建统一格式补丁
- `apply_patch()` - 应用补丁到原始文本

### 5. 工具函数

- `find_matching_blocks()` - 查找匹配块
- `get_diff_summary()` - 获取详细统计信息
- `text_diff_summary()` - 人类可读的摘要
- `batch_diff()` - 批量比较文本对
- `find_duplicate_blocks()` - 查找重复块
- `merge_diffs()` - 合并差异结果

### 6. TextDiffer 类

面向对象的差异比较器，支持配置选项（忽略空白、忽略大小写）。

## 测试结果

### 测试执行情况

```
----------------------------------------------------------------------
Ran 59 tests in 0.005s

OK
----------------------------------------------------------------------
```

### 测试覆盖范围

- **TestDiffLines** (7 tests): 行级差异比较
- **TestDiffWords** (4 tests): 单词级差异比较
- **TestDiffChars** (3 tests): 字符级差异比较
- **TestUnifiedDiff** (4 tests): 统一差异格式
- **TestContextDiff** (2 tests): 上下文差异格式
- **TestHtmlDiff** (3 tests): HTML 差异格式
- **TestInlineDiff** (2 tests): 内联差异格式
- **TestSimilarity** (4 tests): 相似度计算
- **TestLevenshtein** (6 tests): Levenshtein 距离
- **TestLCS** (4 tests): 最长公共子序列
- **TestPatch** (2 tests): 补丁功能
- **TestDiffSummary** (3 tests): 差异摘要
- **TestTextDifferClass** (5 tests): TextDiffer 类
- **TestAdvancedFeatures** (3 tests): 高级功能
- **TestEdgeCases** (4 tests): 边缘情况
- **TestDiffOps** (2 tests): 差异操作

### 测试要点

- ✅ 相同文本无差异
- ✅ 添加、删除、替换行正确识别
- ✅ 忽略空白和大小写选项工作正常
- ✅ Unicode 和特殊字符支持
- ✅ 大文本处理（1000 行测试）
- ✅ 空文本和单行文本处理

## 使用示例

### 基础使用

```python
from text_diff_utils.mod import diff_lines, unified_diff

# 比较两个文本
old = "line1\nline2\nline3"
new = "line1\nmodified\nline3"

result = diff_lines(old, new)
print(result.stats)  # {'added': 0, 'deleted': 0, 'replaced': 1, ...}

# 生成统一差异
diff = unified_diff(old, new, "original.txt", "modified.txt")
print(diff)
```

### 相似度计算

```python
from text_diff_utils.mod import similarity_ratio, levenshtein_distance

text1 = "hello world"
text2 = "hello there"

print(f"相似度: {similarity_ratio(text1, text2):.2%}")
print(f"编辑距离: {levenshtein_distance(text1, text2)}")
```

### HTML 差异生成

```python
from text_diff_utils.mod import html_diff

html = html_diff(old_text, new_text, "原文件", "新文件")
with open("diff.html", "w") as f:
    f.write(html)
```

## 文件结构

```
Python/text_diff_utils/
├── mod.py                  # 主模块 (26KB)
├── text_diff_utils_test.py # 测试文件 (18KB)
├── README.md               # 文档 (6KB)
├── REPORT.md               # 开发报告 (3KB)
└── examples/
    └── usage_examples.py   # 使用示例 (8KB)
```

## 特点

- ✅ **零外部依赖** - 纯 Python 标准库实现
- ✅ **多种算法** - 行/单词/字符三种粒度
- ✅ **多种格式** - 统一/上下文/HTML/内联四种输出
- ✅ **完整测试** - 59 个测试用例全部通过
- ✅ **详细文档** - README + 示例代码
- ✅ **Unicode 支持** - 完整支持中文和特殊字符

## 应用场景

1. 版本控制系统 - 比较、合并代码变更
2. 文档对比工具 - 比较文档版本差异
3. 代码审查工具 - 高亮显示代码变更
4. 文本编辑器 - 实现撤销/重做差异
5. 数据同步 - 检测数据变更
6. 抄袭检测 - 计算文本相似度

## 总结

成功开发了全面的文本差异比较工具集，包含差异比较、格式化输出、相似度计算、补丁生成等功能。所有 59 个测试用例通过，代码质量良好，零外部依赖，可广泛应用于各种文本处理场景。