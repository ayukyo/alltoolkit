# compliment_utils - 称赞语生成工具

随机称赞/赞美语生成工具，支持多语言，零外部依赖。

## 功能特性

- **随机称赞生成** - 生成各种类型的称赞语
- **分类称赞** - 工作、外貌、性格、能力等类别
- **多语言支持** - 中文、英文称赞
- **强度分级** - 轻度、中度、强力称赞
- **个性化称赞** - 带名字的定制称赞
- **批量生成** - 一次生成多条称赞

## 主要类

### ComplimentCategory
称赞类别枚举：
- `WORK` - 工作相关
- `APPEARANCE` - 外貌相关
- `PERSONALITY` - 性格相关
- `SKILL` - 能力相关
- `EFFORT` - 努力相关
- `ATTITUDE` - 态度相关
- `ACHIEVEMENT` - 成就相关
- `CREATIVITY` - 创造力相关
- `KINDNESS` - 善良相关
- `INTELLIGENCE` - 智慧相关
- `HUMOR` - 幽默相关
- `FRIENDSHIP` - 友谊相关
- `GENERAL` - 通用称赞

### ComplimentStrength
称赞强度枚举：
- `LIGHT` - 轻度赞美，日常用语
- `MEDIUM` - 标准赞美
- `STRONG` - 强烈赞美，印象深刻

### Language
语言枚举：`CHINESE`, `ENGLISH`

### ComplimentUtils
主要工具类，提供完整的称赞生成功能。

## 主要函数

### get_compliment(category, strength, language)
获取指定类别和强度的称赞。

```python
get_compliment(ComplimentCategory.WORK, ComplimentStrength.MEDIUM, Language.CHINESE)
# "你的工作能力真的很出色"
```

### get_personalized_compliment(name, language)
生成带名字的个性化称赞。

```python
get_personalized_compliment("小明")
# "小明，你的工作能力真的很出色！"
```

### get_daily_compliment(language)
获取每日称赞。

### get_motivational_compliment(language)
获取励志称赞。

### get_batch_compliments(count, language)
批量生成多条称赞。

```python
get_batch_compliments(5)
# ["称赞1", "称赞2", "称赞3", "称赞4", "称赞5"]
```

### random_compliment()
随机生成称赞。

## 使用示例

```python
from compliment_utils import get_compliment, get_personalized_compliment, ComplimentCategory, ComplimentStrength

# 按类别获取称赞
print(get_compliment(ComplimentCategory.WORK, ComplimentStrength.MEDIUM))
# 输出: 你的工作能力真的很出色

# 个性化称赞
print(get_personalized_compliment("小红"))
# 输出: 小红，你的工作能力真的很出色！

# 每日称赞
print(get_daily_compliment())
# 输出: 今天又是美好的一天，继续保持好心情！

# 批量生成
compliments = get_batch_compliments(5)
for c in compliments:
    print(c)
```

## 测试

运行测试：
```bash
python compliment_utils/compliment_utils_test.py
```

测试覆盖率：38 个测试用例，100% 通过。

---

*最后更新: 2026-05-26*