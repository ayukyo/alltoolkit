# Sentiment Utils - 情感分析工具

零依赖的中英文情感分析工具，基于词典方法实现。

## 功能特性

- ✅ **中英文支持** - 自动检测语言，支持中英文混合
- ✅ **情感极性判断** - 正面/负面/中性三分类
- ✅ **情感得分计算** - -1.0 到 1.0 的连续得分
- ✅ **程度副词处理** - 支持"非常"、"很"、"特别"等程度修饰
- ✅ **否定词处理** - 支持"不"、"没有"等否定修饰
- ✅ **情感词提取** - 提取文本中的情感词汇
- ✅ **自定义词典** - 支持扩展情感词汇库
- ✅ **批量分析** - 高效批量处理文本
- ✅ **零依赖** - 仅使用 Python 标准库

## 安装

无需安装，直接复制 `sentiment_utils.py` 到项目中即可使用。

## 快速开始

```python
from sentiment_utils import SentimentAnalyzer, analyze_sentiment

# 方式1: 使用类
analyzer = SentimentAnalyzer()
result = analyzer.analyze("这个产品非常好用，我很喜欢！")
print(result.polarity)  # SentimentPolarity.POSITIVE
print(result.score)     # 0.8

# 方式2: 使用快捷函数
result = analyze_sentiment("I love this product!")
print(result.score)  # 正值
```

## API 文档

### SentimentAnalyzer 类

主要情感分析器类。

#### 初始化参数

```python
SentimentAnalyzer(
    custom_positive=None,    # 自定义正面词词典 {词: 得分}
    custom_negative=None,    # 自定义负面词词典 {词: 得分}
    custom_intensifiers=None, # 自定义程度副词 {词: 倍数}
    custom_negators=None     # 自定义否定词集合
)
```

#### 主要方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `analyze(text)` | 分析文本情感 | SentimentResult |
| `analyze_batch(texts)` | 批量分析 | List[SentimentResult] |
| `get_sentiment_words(text)` | 提取情感词 | Tuple[List[str], List[str]] |
| `get_score(text)` | 获取情感得分 | float |
| `is_positive(text)` | 判断是否正面 | bool |
| `is_negative(text)` | 判断是否负面 | bool |
| `compare_sentiment(text1, text2)` | 比较两文本情感 | int |

### SentimentResult 数据类

分析结果对象。

| 属性 | 类型 | 说明 |
|------|------|------|
| `polarity` | SentimentPolarity | 极性（POSITIVE/NEGATIVE/NEUTRAL） |
| `score` | float | 综合得分（-1.0 到 1.0） |
| `positive_score` | float | 正面得分 |
| `negative_score` | float | 负面得分 |
| `positive_words` | List[str] | 发现的正面词列表 |
| `negative_words` | List[str] | 发现的负面词列表 |
| `confidence` | float | 置信度（0.0 到 1.0） |

### 便捷函数

```python
from sentiment_utils import (
    analyze_sentiment,    # 分析情感
    get_sentiment_score,  # 获取得分
    is_positive_text,     # 是否正面
    is_negative_text,     # 是否负面
)

result = analyze_sentiment("这个很好")
score = get_sentiment_score("这个很好")
pos = is_positive_text("这个很好")
neg = is_negative_text("这个很差")
```

## 使用示例

### 基本分析

```python
from sentiment_utils import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# 中文
result = analyzer.analyze("这个产品非常好用，我很喜欢！")
print(f"极性: {result.polarity.value}")  # positive
print(f"得分: {result.score}")           # 0.8
print(f"正面词: {result.positive_words}") # ['好', '喜欢']

# 英文
result = analyzer.analyze("This is terrible. I hate it.")
print(f"极性: {result.polarity.value}")  # negative
```

### 否定词处理

```python
analyzer = SentimentAnalyzer()

# 正常正面
r1 = analyzer.analyze("这个很好")
print(r1.score)  # 0.7

# 否定后变负面
r2 = analyzer.analyze("这个不好")
print(r2.score)  # -0.7
```

### 程度副词效果

```python
analyzer = SentimentAnalyzer()

print(analyzer.get_score("这个好"))      # 0.7
print(analyzer.get_score("这个很好"))     # 0.91 (0.7 * 1.3)
print(analyzer.get_score("这个非常好"))   # 1.05 (0.7 * 1.5)
```

### 自定义词典

```python
analyzer = SentimentAnalyzer(
    custom_positive={"牛牛牛": 1.0, "给力": 0.9},
    custom_negative={"坑爹": 0.9, "辣鸡": 0.8}
)

result = analyzer.analyze("这个东西牛牛牛！")
print(result.polarity)  # POSITIVE
```

### 批量分析

```python
analyzer = SentimentAnalyzer()

comments = [
    "质量很好，推荐！",
    "一般般吧。",
    "太差了，退货！",
]

results = analyzer.analyze_batch(comments)

# 统计正面比例
positive = sum(1 for r in results if r.polarity == SentimentPolarity.POSITIVE)
print(f"正面评论: {positive}/{len(comments)}")
```

### 情感比较

```python
analyzer = SentimentAnalyzer()

result = analyzer.compare_sentiment(
    "这个产品很好！",
    "这个产品太差了！"
)
print(result)  # 1 (第一个更正面)
```

## 得分说明

- **得分范围**: -1.0 到 1.0
- **得分 > 0.1**: 正面情感
- **得分 < -0.1**: 负面情感
- **得分在 -0.1 到 0.1 之间**: 中性情感

## 内置词典

工具内置了常用中英文情感词典：

- 中文正面词: 约50个
- 中文负面词: 约50个
- 英文正面词: 约40个
- 英文负面词: 约40个
- 中文程度副词: 约20个
- 英文程度副词: 约20个
- 中文否定词: 约15个
- 英文否定词: 约20个

可通过 `custom_*` 参数扩展。

## 运行测试

```bash
python -m pytest sentiment_utils_test.py -v
```

## 运行示例

```bash
python examples.py
```

## 应用场景

- 商品评论分析
- 社交媒体舆情监控
- 客户反馈分类
- 文本情感过滤
- 推荐系统辅助
- 舆情预警

## 限制说明

- 基于词典方法，无法理解复杂语义和语境
- 讽刺、反语等特殊表达可能识别不准确
- 专业领域词汇需要自定义扩展
- 不支持句子级别的语法分析

对于更复杂的场景，建议结合机器学习模型使用。

## License

MIT License

Author: AllToolkit
Date: 2026-05-01