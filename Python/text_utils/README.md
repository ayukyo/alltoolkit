# Text Utils 📝

**Python 文本处理工具库**

零依赖、生产就绪的文本格式化、分析、转换、清理和统计工具。

---

## ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **全面格式化** - 支持 9 种文本大小写风格
- **深度分析** - 词频、n-gram、关键词密度、可读性评分
- **智能清理** - HTML 标签、URL、邮箱、Unicode 标准化
- **文本转换** - 截断、反转、旋转、交替大小写
- **搜索替换** - 多模式替换、高亮、位置查找
- **文本比较** - 相似度计算、Levenshtein 距离
- **哈希编码** - MD5、SHA1、SHA256、SHA512、Base64

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cd alltoolkit/Python/text_utils
```

---

## 🚀 快速开始

### 基本使用

```python
from text_utils.mod import TextUtils

utils = TextUtils()

# 文本清理
text = "  Hello   World!  <br>Visit https://example.com  "
clean = utils.clean(text, remove_extra_spaces=True, remove_html=True)
print(clean)  # "Hello World! Visit"

# 大小写转换
utils.to_case("hello world", TextCase.SNAKE)    # "hello_world"
utils.to_case("hello world", TextCase.CAMEL)    # "helloWorld"
utils.to_case("hello world", TextCase.PASCAL)   # "HelloWorld"
utils.to_case("hello world", TextCase.KEBAB)    # "hello-world"

# 文本统计
stats = utils.get_stats("Hello world. This is a test.")
print(stats.word_count)        # 6
print(stats.sentence_count)    # 2
print(stats.avg_word_length)   # 3.83
```

### 模块级函数

```python
from text_utils.mod import (
    clean,
    get_stats,
    analyze,
    remove_html,
    truncate,
    similarity,
)

# 直接使用
text = "Great product! Highly recommended."
stats = get_stats(text)
clean_text = clean(text, remove_punctuation=True)
```

---

## 📖 API 参考

### TextUtils 类

#### 格式化方法

| 方法 | 描述 | 返回 |
|------|------|------|
| `to_case(text, case, separator)` | 转换大小写风格 | `str` |
| `to_sentence_case(text)` | 转换为句首大写 | `str` |
| `split_into_words(text)` | 分割为单词列表 | `List[str]` |
| `pad(text, width, side, char)` | 填充文本 | `str` |
| `wrap(text, width)` | 文本换行 | `List[str]` |

#### 清理方法

| 方法 | 描述 | 返回 |
|------|------|------|
| `clean(text, **options)` | 综合清理 | `str` |
| `remove_html(text)` | 移除 HTML 标签 | `str` |
| `remove_urls(text, replace_with)` | 移除 URL | `str` |
| `remove_emails(text, replace_with)` | 移除邮箱 | `str` |
| `normalize_whitespace(text)` | 标准化空白 | `str` |
| `normalize_line_endings(text, style)` | 标准化换行符 | `str` |

#### 分析方法

| 方法 | 描述 | 返回 |
|------|------|------|
| `analyze(text, top_n, ngram_range)` | 全面文本分析 | `TextAnalysis` |
| `get_stats(text)` | 获取统计信息 | `TextStats` |
| `extract_words(text, min_length)` | 提取单词 | `List[str]` |
| `split_sentences(text)` | 分割句子 | `List[str]` |
| `get_ngrams(words, n)` | 生成 n-gram | `List[Tuple]` |
| `keyword_density(text)` | 关键词密度 | `List[Tuple]` |

#### 转换方法

| 方法 | 描述 | 返回 |
|------|------|------|
| `reverse(text, preserve_words)` | 反转文本 | `str` |
| `rotate(text, shift)` | 旋转字符 | `str` |
| `alternate_case(text)` | 交替大小写 | `str` |
| `mirror(text)` | 镜像文本 | `str` |
| `truncate(text, max_length, suffix)` | 截断文本 | `str` |
| `abbreviate(text, max_words)` | 创建缩写 | `str` |

#### 搜索与比较

| 方法 | 描述 | 返回 |
|------|------|------|
| `find_all(text, pattern)` | 查找所有匹配位置 | `List[int]` |
| `replace_all(text, replacements)` | 多模式替换 | `str` |
| `highlight(text, terms, marker)` | 高亮关键词 | `str` |
| `similarity(text1, text2)` | 文本相似度 | `float` |
| `contains_all(text, terms)` | 检查是否包含所有 | `bool` |
| `contains_any(text, terms)` | 检查是否包含任一 | `bool` |
| `levenshtein_distance(s1, s2)` | 编辑距离 | `int` |

#### 哈希与编码

| 方法 | 描述 | 返回 |
|------|------|------|
| `hash_text(text, algorithm)` | 哈希文本 | `str` |
| `to_base64(text)` | Base64 编码 | `str` |
| `from_base64(text)` | Base64 解码 | `str` |

---

## 📊 TextStats 数据结构

```python
@dataclass
class TextStats:
    char_count: int           # 字符总数
    char_count_no_spaces: int # 不含空格字符数
    word_count: int           # 单词数
    sentence_count: int       # 句子数
    paragraph_count: int      # 段落数
    line_count: int           # 行数
    avg_word_length: float    # 平均单词长度
    avg_sentence_length: float # 平均句子长度
    unique_words: int         # 唯一单词数
    readability_score: float  # 可读性评分 (0-100)
```

---

## 📊 TextAnalysis 数据结构

```python
@dataclass
class TextAnalysis:
    stats: TextStats                    # 统计信息
    word_frequencies: Dict[str, int]    # 词频
    char_frequencies: Dict[str, int]    # 字符频率
    ngrams: Dict[int, List[Tuple]]      # n-gram
    keywords: List[str]                 # 关键词
    sentences: List[str]                # 句子列表
    words: List[str]                    # 单词列表
```

---

## 🎯 TextCase 枚举

```python
class TextCase(Enum):
    LOWER = "lower"       # hello world
    UPPER = "upper"       # HELLO WORLD
    TITLE = "title"       # Hello World
    SENTENCE = "sentence" # Hello world
    CAMEL = "camel"       # helloWorld
    PASCAL = "pascal"     # HelloWorld
    SNAKE = "snake"       # hello_world
    KEBAB = "kebab"       # hello-world
    CONSTANT = "constant" # HELLO_WORLD
```

---

## 💡 实用示例

### 1. 文本预处理管道

```python
def preprocess_text(text: str) -> str:
    utils = TextUtils()
    
    # 清理流程
    text = utils.remove_html(text)
    text = utils.remove_urls(text)
    text = utils.remove_emails(text)
    text = utils.clean(text, 
                       remove_extra_spaces=True,
                       normalize_unicode=True)
    return text
```

### 2. 关键词提取

```python
def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    utils = TextUtils()
    analysis = utils.analyze(text, top_n=top_n)
    return analysis.keywords
```

### 3. 文本相似度检测

```python
def check_plagiarism(text1: str, text2: str, threshold: float = 0.7) -> bool:
    utils = TextUtils()
    similarity = utils.similarity(text1, text2)
    return similarity >= threshold
```

### 4. 可读性分析

```python
def analyze_readability(text: str) -> Dict[str, Any]:
    utils = TextUtils()
    stats = utils.get_stats(text)
    
    if stats.readability_score >= 90:
        level = "Very Easy"
    elif stats.readability_score >= 80:
        level = "Easy"
    elif stats.readability_score >= 70:
        level = "Fairly Easy"
    elif stats.readability_score >= 60:
        level = "Standard"
    elif stats.readability_score >= 50:
        level = "Fairly Difficult"
    else:
        level = "Difficult"
    
    return {
        'score': stats.readability_score,
        'level': level,
        'avg_sentence_length': stats.avg_sentence_length,
        'avg_word_length': stats.avg_word_length,
    }
```

### 5. 智能截断

```python
def smart_truncate(text: str, max_length: int = 100) -> str:
    utils = TextUtils()
    # 在单词边界截断
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    if last_space > max_length * 0.8:
        truncated = truncated[:last_space]
    
    return utils.truncate(truncated, max_length, suffix='...')
```

---

## 🖥️ 命令行使用

```bash
# 获取统计信息
python mod.py stats "Hello world. This is a test."

# 清理文本
python mod.py clean "  Hello   World!  "

# 转换大小写
python mod.py case "hello_world" snake
python mod.py case "helloWorld" camel

# 完整分析
python mod.py analyze "Great product! Highly recommended."

# 哈希文本
python mod.py hash "secret_password"

# 比较相似度
python mod.py similarity "hello world" "world hello"
```

---

## 🧪 运行测试

```bash
cd text_utils
python text_utils_test.py
```

---

## 📁 目录结构

```
text_utils/
├── mod.py              # 主模块
├── README.md           # 文档
├── text_utils_test.py  # 测试文件
└── examples/           # 示例代码
    ├── basic_usage.py
    ├── text_analysis.py
    └── preprocessing.py
```

---

## ⚡ 性能特点

- **零依赖** - 无需 pip 安装，开箱即用
- **纯 Python** - 兼容 Python 3.7+
- **内存高效** - 使用生成器和迭代器
- **类型安全** - 完整的类型注解

---

## 📝 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
