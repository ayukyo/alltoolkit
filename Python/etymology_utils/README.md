# Etymology Utils - 词源工具库

词源分析和词汇起源追踪工具库，零外部依赖。

## 功能特性

- **词源查询**: 从内置数据库查询单词的起源和历史
- **根词提取**: 从派生词中提取根词
- **词源树构建**: 构建可视化的词源关系树
- **复合词检测**: 检测复合词并提取组成部分
- **词汇比较**: 比较两个词的词源关系
- **词汇家族**: 获取同根词家族
- **同源词查找**: 查找跨语言同源词
- **统计分析**: 获取词源数据库统计数据
- **报告生成**: 生成详细的词源分析报告

## 安装使用

```python
from etymology_utils.mod import (
    get_etymology, analyze_word, build_etymology_tree,
    quick_lookup, is_loanword, generate_word_report
)
```

## API 文档

### 核心查询函数

#### `get_etymology(word: str) -> Optional[EtymologyEntry]`

查询单词的词源信息。

```python
entry = get_etymology("computer")
print(entry.language_origin)  # Latin
print(entry.original_form)    # computare
```

#### `quick_lookup(word: str) -> str`

快速查询，返回简要摘要。

```python
summary = quick_lookup("philosophy")
# "'philosophy' from Greek (φιλοσοφία), Ancient period"
```

### 分析函数

#### `analyze_word(word: str) -> Dict[str, Any]`

全面的词源分析，包含词源、根词、前缀、后缀、同源词等。

```python
analysis = analyze_word("information")
# Returns: {
#   "word": "information",
#   "etymology": {...},
#   "prefix": {"prefix": "in", "meaning": "in/not"},
#   "suffix": {"suffix": "ation", "meaning": "action/process"},
#   "cognates": {"French": "information", ...}
# }
```

#### `build_etymology_tree(word: str) -> EtymologyTree`

构建词源树结构。

```python
tree = build_etymology_tree("telephone")
print(visualize_tree(tree))
# telephone [Greek] (Modern)
# └─ τῆλε + φωνή
```

#### `extract_root(word: str) -> Optional[str]`

从派生词中提取根词。

```python
root = extract_root("action")  # Returns "act"
```

### 搜索函数

#### `search_by_origin(origin: LanguageOrigin) -> List[EtymologyEntry]`

按语言来源搜索词汇。

```python
latin_words = search_by_origin(LanguageOrigin.LATIN)
greek_words = search_by_origin(LanguageOrigin.GREEK)
```

#### `search_by_period(period: HistoricalPeriod) -> List[EtymologyEntry]`

按历史时期搜索词汇。

```python
ancient_words = search_by_period(HistoricalPeriod.ANCIENT)
modern_words = search_by_period(HistoricalPeriod.MODERN)
```

#### `search_words(query: str, fuzzy: bool = False) -> List[str]`

搜索词汇（前缀或模糊匹配）。

```python
results = search_words("com")  # Prefix search
results = search_words("compu", fuzzy=True)  # Fuzzy search
```

### 词汇家族与同源词

#### `get_word_family(root: str) -> Optional[WordFamily]`

获取词汇家族。

```python
family = get_word_family("work")
print(family.members)  # ["worker", "working", "workplace", ...]
```

#### `find_cognates(word: str) -> Dict[str, str]`

查找跨语言同源词。

```python
cognates = find_cognates("computer")
# {"French": "ordinateur", "German": "Computer", "Spanish": "computadora"}
```

### 特殊判断

#### `is_loanword(word: str) -> bool`

判断是否为外来词。

```python
is_loanword("computer")  # True (Latin)
is_loanword("king")      # False (Old English)
```

#### `detect_compound(word: str) -> List[str]`

检测复合词并提取组成部分。

```python
parts = detect_compound("breakfast")  # ["break", "fast"]
parts = detect_compound("airport")    # ["air", "port"]
```

### 比较与报告

#### `compare_words(word1: str, word2: str) -> Dict[str, Any]`

比较两个词的词源关系。

```python
comparison = compare_words("computer", "education")
# {
#   "same_origin": True,  # Both from Latin
#   "same_period": False,
#   "related": True
# }
```

#### `generate_word_report(word: str) -> str`

生成详细的词源报告。

```python
report = generate_word_report("philosophy")
# Full text report with origin, evolution, cognates, etc.
```

### 统计与导出

#### `get_statistics() -> Dict[str, Any]`

获取数据库统计信息。

```python
stats = get_statistics()
# {
#   "total_words": 22,
#   "total_roots": 36,
#   "by_origin": {"Latin": 4, "Greek": 3, ...},
#   "by_period": {"Modern": 5, "Ancient": 3, ...}
# }
```

#### `export_to_json(entries: Optional[List[EtymologyEntry]] = None) -> str`

导出词源数据为JSON。

```python
json_data = export_to_json()
# Full database export with statistics
```

## 数据类

### EtymologyEntry

词源条目数据结构。

```python
entry = EtymologyEntry(
    word="computer",
    language_origin=LanguageOrigin.LATIN,
    historical_period=HistoricalPeriod.MODERN,
    original_form="computare",
    intermediate_forms=["compute", "computer"],
    meaning_evolution=["calculate", "machine"],
    related_words=["computing"],
    cognates={"French": "ordinateur"},
    confidence=0.95
)
```

### EtymologyTree

词源树结构。

```python
tree = EtymologyTree(
    word="root",
    origin=LanguageOrigin.LATIN,
    period=HistoricalPeriod.MODERN
)
tree.add_child(EtymologyTree(word="child"))
```

### WordFamily

词汇家族结构。

```python
family = WordFamily(root="work")
family.add_member("worker")
family.add_member("working", "work + -er")
```

## 语言来源枚举

支持的语言来源：

- `LATIN` - 拉丁语
- `GREEK` - 希腊语
- `GERMANIC` - 日耳曼语
- `OLD_ENGLISH` - 古英语
- `FRENCH` - 法语
- `NORMAN` - 诺曼语
- `CELTIC` - 凯尔特语
- `ARABIC` - 阿拉伯语
- `HEBREW` - 希伯来语
- `PERSIAN` - 波斯语
- `CHINESE` - 中文
- `JAPANESE` - 日语
- `SPANISH` - 西班牙语
- `ITALIAN` - 意大利语
- `DUTCH` - 荷兰语
- `NORSE` - 北欧语
- `SLAVIC` - 斯拉夫语
- `HINDI` - 印地语
- `UNKNOWN` - 未知

## 历史时期枚举

- `ANCIENT` - 古代 (公元500年以前)
- `MEDIEVAL` - 中世纪 (500-1500年)
- `EARLY_MODERN` - 近代早期 (1500-1800年)
- `MODERN` - 现代 (1800年至今)
- `CONTEMPORARY` - 当代 (20-21世纪)

## 使用示例

### 基本查询

```python
# 查询词源
entry = get_etymology("philosophy")
print(f"Origin: {entry.language_origin.value}")
print(f"Original: {entry.original_form}")
print(f"Cognates: {entry.cognates}")

# 快速查询
print(quick_lookup("telephone"))
```

### 分析词汇

```python
# 全面分析
analysis = analyze_word("education")
print(f"Is compound: {analysis['is_compound']}")
print(f"Prefix: {analysis['prefix']}")
print(f"Suffix: {analysis['suffix']}")
print(f"Cognates: {analysis['cognates']}")
```

### 词源树可视化

```python
# 构建并可视化词源树
tree = build_etymology_tree("computer")
print(visualize_tree(tree))
# computer [Latin] (Modern)
# └─ computare [Latin] (Ancient)
# └─ compute
# └─ computational
```

### 查找同根词

```python
# 获取词汇家族
family = get_word_family("work")
print(family.members)
# ['worker', 'working', 'workplace', 'network', ...]

# 查找同源词
cognates = find_cognates("mathematics")
# {'French': 'mathématiques', 'German': 'Mathematik', ...}
```

### 搜索与统计

```python
# 按来源搜索
latin_words = search_by_origin(LanguageOrigin.LATIN)
print(f"Latin origin words: {len(latin_words)}")

# 获取统计数据
stats = get_statistics()
print(f"Total words: {stats['total_words']}")
print(f"By origin: {stats['by_origin']}")
```

### 报告生成

```python
# 生成详细报告
report = generate_word_report("king")
print(report)
# ================================================
# ETYMOLOGY REPORT: KING
# ================================================
# 
# Origin: Old English
# Period: Ancient
# Original Form: cyning
# ...
```

## 内置数据库

模块包含丰富的词源数据：

- **22+ 词源条目**: 涵盖拉丁语、希腊语、古英语、法语、阿拉伯语等来源
- **36+ 根词家族**: work, act, form, play, read, write 等
- **30+ 前缀**: a-, anti-, auto-, bi-, co-, de-, pre-, re-, 等
- **28+ 后缀**: -able, -ful, -ing, -tion, -ment, -ness, 等

## 测试

运行测试：

```bash
python Python/etymology_utils/etymology_utils_test.py
```

测试覆盖：
- 60+ 测试用例
- 100% 覆盖核心功能
- 边界值测试（空字符串、Unicode、特殊字符）

## 许可证

MIT License