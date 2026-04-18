# 塔罗牌工具 (Tarot Utils)

完整的塔罗牌工具模块，提供牌组管理、多种牌阵解读、牌面查询等功能。

## 功能特性

- ✨ **完整78张牌组** - 22张大阿卡纳 + 56张小阿卡纳
- 🎴 **多种牌阵** - 单牌、三牌、凯尔特十字、是非牌阵
- 📖 **详细解读** - 每张牌包含正逆位含义、关键词
- 🔮 **神秘学对应** - 元素、星座、行星对应
- 🎲 **可重复结果** - 支持随机种子
- 📦 **零依赖** - 纯Python标准库实现

## 快速开始

```python
from tarot_utils.mod import (
    draw_single_card,
    draw_three_cards,
    draw_celtic_cross,
    ask_yes_no,
    get_card_info
)

# 单牌解读
result = draw_single_card("今天运势如何？")
print(result["interpretation"])

# 三牌牌阵（过去/现在/未来）
result = draw_three_cards("近期感情发展")
for card in result["cards"]:
    print(f"【{card['position']}】{card['card']} ({card['orientation']})")

# 凯尔特十字牌阵（10张牌）
result = draw_celtic_cross("我的事业发展方向？")
print(result["interpretation"])

# 是非问题
result = ask_yes_no("我应该接受这份新工作吗？")
print(f"答案: {result['answer']} (置信度: {result['confidence']})")

# 查询牌信息
info = get_card_info("愚者")
print(f"愚者 - 元素: {info['element']}, 关键词: {info['keywords_upright']}")
```

## 牌阵类型

### 单牌牌阵
快速获得一个指引或建议。

```python
result = draw_single_card("问题")
```

### 三牌牌阵
最常用的牌阵，可自定义位置含义：

```python
# 默认：过去/现在/未来
result = draw_three_cards("问题")

# 自定义位置
result = draw_three_cards(
    "问题",
    positions=("情境", "行动", "结果")
)
```

### 凯尔特十字牌阵
最经典的10张牌大阵，全面分析：

| 位置 | 含义 |
|------|------|
| 1 | 现状 - 你目前的情况 |
| 2 | 挑战 - 面临的障碍 |
| 3 | 根源 - 问题的根源 |
| 4 | 过去 - 已经过去的影响 |
| 5 | 近期未来 - 即将发生的事 |
| 6 | 远期未来 - 最终趋势 |
| 7 | 你的态度 - 心态和立场 |
| 8 | 外部环境 - 他人的影响 |
| 9 | 希望与恐惧 - 期望和担忧 |
| 10 | 最终结果 - 事情的结局 |

```python
result = draw_celtic_cross("问题")
```

### 是非牌阵
针对是非问题的简单解读：

```python
result = ask_yes_no("这是一个好主意吗？")
# 返回: "是的"/"不是"/"不确定" + 置信度
```

## 牌组信息

### 大阿卡纳 (Major Arcana)
22张，代表人生重大主题：

| 编号 | 牌名 | 元素 | 行星/星座 |
|------|------|------|-----------|
| 0 | 愚者 | 风 | 天王星 |
| 1 | 魔术师 | 风 | 水星 |
| 2 | 女祭司 | 水 | 月亮 |
| 3 | 女皇 | 地 | 金星 |
| 4 | 皇帝 | 火 | 白羊座 |
| 5 | 教皇 | 地 | 金牛座 |
| ... | ... | ... | ... |

### 小阿卡纳 (Minor Arcana)
56张，分为四个花色：

| 花色 | 元素 | 主题 |
|------|------|------|
| 权杖 (Wands) | 火 | 行动、激情、创意 |
| 圣杯 (Cups) | 水 | 情感、关系、直觉 |
| 宝剑 (Swords) | 风 | 思维、沟通、冲突 |
| 金币 (Pentacles) | 地 | 物质、财富、实践 |

每个花色14张牌：A-10 + 侍从 + 骑士 + 王后 + 国王

## API 参考

### 核心类

#### TarotDeck
塔罗牌牌组类。

```python
deck = TarotDeck(seed=42)  # 可选随机种子
deck.shuffle()              # 洗牌
card, orientation = deck.draw_card()  # 抽一张牌
cards = deck.draw_cards(5)  # 抽多张牌
```

#### TarotReading
塔罗牌解读类。

```python
reading = TarotReading(deck)
result = reading.single_card_reading("问题")
result = reading.three_card_reading("问题")
result = reading.celtic_cross_reading("问题")
result = reading.yes_no_reading("是非问题")
```

### 便捷函数

| 函数 | 说明 |
|------|------|
| `draw_single_card(question, seed)` | 单牌解读 |
| `draw_three_cards(question, positions, seed)` | 三牌牌阵 |
| `draw_celtic_cross(question, seed)` | 凯尔特十字 |
| `ask_yes_no(question, seed)` | 是非问题 |
| `get_card_info(card_name)` | 获取牌信息 |
| `list_all_cards()` | 列出所有牌 |
| `list_major_arcana()` | 列出大阿卡纳 |
| `list_minor_arcana()` | 列出小阿卡纳 |
| `list_cards_by_suit(suit)` | 按花色列出牌 |

### 数据结构

```python
@dataclass
class TarotCard:
    id: int                    # 牌编号 (0-77)
    name: str                  # 中文名
    english_name: str          # 英文名
    card_type: CardType        # 大/小阿卡纳
    suit: Optional[Suit]       # 花色 (小阿卡纳)
    number: Optional[int]      # 编号 (小阿卡纳 1-14)
    keywords_upright: List[str]    # 正位关键词
    keywords_reversed: List[str]   # 逆位关键词
    meaning_upright: str       # 正位含义
    meaning_reversed: str      # 逆位含义
    element: Optional[str]     # 元素
    zodiac: Optional[str]      # 星座 (大阿卡纳)
    planet: Optional[str]      # 行星 (大阿卡纳)
```

## 示例输出

```
【牌阵解读】

【过去】命运之轮(正位)：命运之轮预示着变化的到来。命运的转折点即将出现，拥抱变化吧。

【现在】星星(正位)：星星带来希望和治愈。风暴过后，平静和光明正在等待着你。

【未来】力量(逆位)：逆位表示你可能正在经历自我怀疑，或者错误地使用了你的力量。

【综合分析】
多张大阿卡纳牌出现，说明这是一个重要的转折点，具有深刻的精神意义。
```

## 运行测试

```bash
python test_tarot.py
```

## 文件结构

```
tarot_utils/
├── mod.py          # 主模块
├── test_tarot.py  # 测试文件
└── README.md      # 说明文档
```

## 许可证

MIT License