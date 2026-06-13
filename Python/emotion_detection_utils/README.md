# Emotion Detection Utils 💭

基于情感词典的中英文文本情感分析工具模块。

## 功能特性

- **多情感检测** - 快乐、悲伤、愤怒、恐惧、惊讶、厌恶
- **情感极性判断** - 正面、负面、中性
- **中英文支持** - 内置中英文情感词典
- **自动语言检测** - 支持自动检测文本语言
- **否定词处理** - 正确处理"不高兴"等否定表达
- **强度修饰** - 支持"非常"、"very"等程度副词
- **置信度评分** - 提供情感判断的置信度
- **零外部依赖** - 纯 Python 内置实现

## 快速开始

```python
from emotion_detection_utils import (
    EmotionDetector, Emotion, Sentiment, EmotionResult,
    detect_emotion, get_sentiment, is_positive, is_negative
)

# 基础用法
detector = EmotionDetector()
result = detector.detect("今天天气真好，心情特别愉快！")
print(result.dominant_emotion)  # Emotion.JOY
print(result.sentiment)          # Sentiment.POSITIVE

# 便捷函数
sentiment = get_sentiment("这个产品太棒了，我很喜欢")
print(sentiment)  # 'positive'
```

## EmotionDetector 类

### 初始化

```python
from emotion_detection_utils import EmotionDetector

# 自动检测语言（默认）
detector = EmotionDetector()

# 指定中文
detector = EmotionDetector(language="zh")

# 指定英文
detector = EmotionDetector(language="en")
```

### 检测情感

```python
detector = EmotionDetector()

# 检测中文文本
result = detector.detect("这部电影太感人了，我哭了")
print(result.dominant_emotion)  # Emotion.SADNESS
print(result.sentiment)          # Sentiment.NEGATIVE
print(result.confidence)         # 0.75
print(result.emotion_scores)    # {'joy': 0.0, 'sadness': 0.75, ...}
print(result.keywords_found)     # ['哭了', '感人']

# 检测英文文本
result = detector.detect("I'm so happy to see you!")
print(result.dominant_emotion)  # Emotion.JOY
print(result.sentiment)          # Sentiment.POSITIVE
```

### 获取情感分布

```python
detector = EmotionDetector()
result = detector.detect("虽然有点累，但是很开心")

# 获取所有情感分数
scores = result.emotion_scores
for emotion, score in scores.items():
    if score > 0:
        print(f"{emotion.name}: {score:.2f}")
# JOY: 0.65
# SADNESS: 0.35
```

### 判断正负极性

```python
detector = EmotionDetector()

# 判断是否为正面情感
print(detector.is_positive("太棒了！完美！"))     # True
print(detector.is_positive("糟糕，出了问题"))     # False

# 判断是否为负面情感
print(detector.is_negative("好开心啊！"))          # False
print(detector.is_negative("好难过，很伤心"))      # True
```

## 便捷函数

### detect_emotion

```python
from emotion_detection_utils import detect_emotion

result = detect_emotion("这个电影真的很精彩！")
print(result.dominant_emotion)  # Emotion.JOY
```

### get_sentiment

```python
from emotion_detection_utils import get_sentiment

# 返回 'positive', 'negative', 或 'neutral'
print(get_sentiment("太棒了！"))     # 'positive'
print(get_sentiment("好难过"))       # 'negative'
print(get_sentiment("今天周一"))     # 'neutral'
```

### is_positive / is_negative

```python
from emotion_detection_utils import is_positive, is_negative

print(is_positive("完美！"))   # True
print(is_negative("糟透了"))  # True
```

## EmotionResult 对象

```python
result = detector.detect("这部电影太感人了")

# 主导情感
print(result.dominant_emotion)  # Emotion.SADNESS
print(result.dominant_emotion.value)  # 'sadness'

# 情感分数（归一化）
print(result.emotion_scores)
# {
#     Emotion.JOY: 0.0,
#     Emotion.SADNESS: 0.72,
#     Emotion.ANGER: 0.0,
#     Emotion.FEAR: 0.0,
#     Emotion.SURPRISE: 0.0,
#     Emotion.DISGUST: 0.0,
#     Emotion.NEUTRAL: 0.28
# }

# 情感极性
print(result.sentiment)  # Sentiment.NEGATIVE

# 置信度 (0-1)
print(result.confidence)  # 0.72

# 匹配到的情感关键词
print(result.keywords_found)  # ['感人', '太']
```

## 支持的情感类型

| 枚举值 | 中文 | 英文示例 | 极性 |
|--------|------|---------|------|
| `Emotion.JOY` | 快乐 | happy, joy, excited | 正面 |
| `Emotion.SADNESS` | 悲伤 | sad, sorrow, crying | 负面 |
| `Emotion.ANGER` | 愤怒 | angry, furious, hate | 负面 |
| `Emotion.FEAR` | 恐惧 | afraid, scared, worried | 负面 |
| `Emotion.SURPRISE` | 惊讶 | surprised, shocked, wow | 中性 |
| `Emotion.DISGUST` | 厌恶 | disgust, disgusting, gross | 负面 |
| `Emotion.NEUTRAL` | 中性 | - | 中性 |

## 高级用法

### 批量处理

```python
detector = EmotionDetector()

texts = [
    "太开心了！",
    "很难过，想哭",
    "这部电影一般般"
]

for text in texts:
    result = detector.detect(text)
    print(f"'{text}' -> {result.dominant_emotion.name}")
```

### Emoji 情感识别

```python
detector = EmotionDetector()

# Emoji 直接识别
result = detector.detect("今天很开心 😊")
print(result.dominant_emotion)  # Emotion.JOY

result = detector.detect("好难过 😢")
print(result.dominant_emotion)  # Emotion.SADNESS

result = detector.detect("好生气 😡")
print(result.dominant_emotion)  # Emotion.ANGER
```

### 否定词处理

```python
detector = EmotionDetector()

# "不高兴" → 悲伤
result = detector.detect("我不高兴")
print(result.dominant_emotion)  # Emotion.SADNESS

# "不生气" → 中性
result = detector.detect("我不生气")
print(result.dominant_emotion)  # Emotion.NEUTRAL
```

### 强度修饰词

```python
detector = EmotionDetector()

# 无修饰
result = detector.detect("有点开心")
print(result.confidence)  # 较低

# 有修饰词
result = detector.detect("非常开心")
print(result.confidence)  # 较高

result = detector.detect("超级开心")
print(result.confidence)  # 更高
```

## 局限性

- 基于词典的方法，无法理解上下文和讽刺
- 对于网络用语和缩写词支持有限
- 混合语言文本建议设置明确语言

## 测试

```bash
python -m pytest Python/emotion_detection_utils/ -v
```

## 许可证

MIT License