# Playing Card Utils - 扑克牌工具模块

提供完整的扑克牌功能，包括牌组创建、洗牌、发牌、手牌评估等。支持德州扑克、21点、战争牌等常见扑克游戏。

## 功能特性

### 核心功能
- **Card**: 扑克牌表示，支持花色、点数、比较大小
- **Deck**: 牌组管理，支持创建、洗牌、发牌、重置
- **HandEvaluator**: 德州扑克手牌评估，支持所有牌型
- **Blackjack**: 21点游戏辅助工具
- **CardGame**: 卡牌游戏通用工具

### 支持的扑克牌型
1. 皇家同花顺 (Royal Flush)
2. 同花顺 (Straight Flush)
3. 四条 (Four of a Kind)
4. 葫芦 (Full House)
5. 同花 (Flush)
6. 顺子 (Straight)
7. 三条 (Three of a Kind)
8. 两对 (Two Pair)
9. 一对 (One Pair)
10. 高牌 (High Card)

## 安装

```python
# 直接导入使用，零依赖
from playing_card_utils.mod import Card, Deck, HandEvaluator
```

## 快速开始

### 创建牌和牌组

```python
from playing_card_utils.mod import Card, Suit, Rank, Deck

# 创建单张牌
card = Card(Suit.SPADES, Rank.ACE)
print(card)  # ♠A
print(card.display)  # 黑桃A

# 从字符串创建牌
card = Card.from_string("♥K")
print(card)  # ♥K

# 创建标准52张牌组
deck = Deck()
print(len(deck))  # 52

# 洗牌
deck.shuffle()

# 发牌
hand = deck.deal(5)  # 发5张牌
print(hand)  # [♠A, ♥K, ♦Q, ...]

# 发多手牌
deck.reset()
hands = deck.deal_hands(4, 5)  # 4个玩家，每人5张
```

### 德州扑克手牌评估

```python
from playing_card_utils.mod import HandEvaluator, Card, Suit, Rank, HandRank

# 创建一手牌（同花顺）
hand = [
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.SPADES, Rank.KING),
    Card(Suit.SPADES, Rank.QUEEN),
    Card(Suit.SPADES, Rank.JACK),
    Card(Suit.SPADES, Rank.TEN),
]

# 评估手牌
result = HandEvaluator.evaluate(hand)
print(result.rank)  # HandRank.ROYAL_FLUSH
print(result.rank.name_zh)  # 皇家同花顺
print(result.score)  # 分数（用于比较）

# 比较两手牌
hand1 = [Card.from_string(c) for c in "♠A ♠K ♠Q ♠J ♠10".split()]
hand2 = [Card.from_string(c) for c in "♥A ♥A ♦A ♣A ♠2".split()]

comparison = HandEvaluator.compare(hand1, hand2)
print(comparison)  # 1 (hand1 赢)

# 从7张牌中找最佳组合（德州扑克：2张手牌 + 5张公共牌）
all_cards = [Card.from_string(c) for c in 
             "♠A ♥K ♠K ♠Q ♠J ♠10 ♦2".split()]
best = HandEvaluator.get_best_hand(all_cards)
print(best.rank)  # HandRank.STRAIGHT_FLUSH (同花顺 K-Q-J-10-9... 实际是 ♠K-Q-J-10-A)
```

### 21点游戏

```python
from playing_card_utils.mod import Blackjack, Card, Suit, Rank

# 创建手牌
hand = [
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.HEARTS, Rank.KING),
]

# 计算点数
value = Blackjack.calculate_hand_value(hand)
print(value)  # 21

# 检查是否是 Blackjack
is_bj = Blackjack.is_blackjack(hand)
print(is_bj)  # True

# 检查是否爆牌
hand2 = [
    Card(Suit.SPADES, Rank.KING),
    Card(Suit.HEARTS, Rank.QUEEN),
    Card(Suit.DIAMONDS, Rank.FIVE),
]
is_bust = Blackjack.is_bust(hand2)
print(is_bust)  # True

# 获取策略建议
player_hand = [Card(Suit.CLUBS, Rank.SIX), Card(Suit.HEARTS, Rank.SIX)]
dealer_card = Card(Suit.DIAMONDS, Rank.SIX)
should_hit = Blackjack.should_hit(player_hand, dealer_card)
print(should_hit)  # False (建议停牌)
```

### 卡牌游戏工具

```python
from playing_card_utils.mod import CardGame, Card, Suit, Rank

# 战争牌比较
card1 = Card(Suit.SPADES, Rank.ACE)
card2 = Card(Suit.HEARTS, Rank.KING)
result = CardGame.war_compare(card1, card2)
print(result)  # 1 (card1 大)

# 从字符串创建手牌
hand = CardGame.create_hand_from_string("♠A ♥K ♦Q ♣J ♠10")
print(len(hand))  # 5

# 手牌转字符串
hand_str = CardGame.cards_to_string(hand)
print(hand_str)  # ♠A ♥K ♦Q ♣J ♠10

# 获取牌的完整中文名称
card = Card(Suit.HEARTS, Rank.QUEEN)
name = CardGame.get_card_name(card)
print(name)  # 红心皇后
```

### 便捷函数

```python
from playing_card_utils.mod import (
    create_deck, shuffle_deck, deal_hand,
    evaluate_poker_hand, compare_hands, get_best_poker_hand
)

# 创建牌组
deck = create_deck()

# 创建并洗好的牌组
deck = shuffle_deck(seed=42)  # 可选种子保证可重复

# 快速发一手牌
hand = deal_hand(5)

# 快速评估手牌
result = evaluate_poker_hand(hand)

# 快速比较手牌
result = compare_hands(hand1, hand2)

# 从7张牌中找最佳组合
best = get_best_poker_hand(all_cards)
```

## API 参考

### Card 类

| 方法/属性 | 描述 |
|----------|------|
| `Card(suit, rank)` | 创建扑克牌 |
| `Card.from_string(str)` | 从字符串创建牌 |
| `suit` | 花色 |
| `rank` | 点数 |
| `display` | 完整显示名称（如"黑桃A"） |
| `is_face_card` | 是否是人头牌（J/Q/K） |
| `is_ace` | 是否是A |
| `<`, `>`, `<=`, `>=` | 支持比较运算 |

### Deck 类

| 方法 | 描述 |
|------|------|
| `Deck(include_jokers)` | 创建牌组 |
| `shuffle(seed)` | 洗牌 |
| `deal(n)` | 发n张牌 |
| `deal_hands(num, cards)` | 发多手牌 |
| `draw()` | 抽一张牌 |
| `peek(index)` | 查看牌（不移除） |
| `reset()` | 重置牌组 |
| `add_card(card)` | 添加牌 |
| `remove_card(card)` | 移除牌 |

### HandEvaluator 类

| 方法 | 描述 |
|------|------|
| `evaluate(cards)` | 评估5张牌的手牌 |
| `compare(hand1, hand2)` | 比较两手牌 |
| `get_best_hand(cards)` | 从7张牌中找最佳组合 |

### Blackjack 类

| 方法 | 描述 |
|------|------|
| `calculate_hand_value(cards)` | 计算点数 |
| `is_blackjack(cards)` | 是否是Blackjack |
| `is_bust(cards)` | 是否爆牌 |
| `should_hit(player, dealer)` | 策略建议 |

### 枚举类

```python
class Suit(Enum):
    SPADES = "♠"      # 黑桃
    HEARTS = "♥"      # 红心
    DIAMONDS = "♦"    # 方块
    CLUBS = "♣"       # 梅花

class Rank(Enum):
    TWO = (2, "2")
    THREE = (3, "3")
    # ...
    ACE = (14, "A")

class HandRank(Enum):
    HIGH_CARD = (1, "高牌")
    ONE_PAIR = (2, "一对")
    # ...
    ROYAL_FLUSH = (10, "皇家同花顺")
```

## 示例游戏

### 简单战争牌游戏

```python
from playing_card_utils.mod import Deck, CardGame

# 创建并洗牌
deck = Deck()
deck.shuffle()

# 发牌给两个玩家
player1 = deck.deal(26)
player2 = deck.deal(26)

# 每回合比较
while player1 and player2:
    card1 = player1.pop(0)
    card2 = player2.pop(0)
    
    result = CardGame.war_compare(card1, card2)
    
    if result > 0:
        player1.extend([card1, card2])
        print(f"玩家1赢: {card1} > {card2}")
    elif result < 0:
        player2.extend([card1, card2])
        print(f"玩家2赢: {card2} > {card1}")
    else:
        print(f"平局: {card1} = {card2}")
```

### 德州扑克模拟

```python
from playing_card_utils.mod import Deck, HandEvaluator, get_best_poker_hand

# 创建牌组
deck = Deck()
deck.shuffle()

# 发牌给4个玩家
hands = deck.deal_hands(4, 2)

# 发公共牌
community = deck.deal(5)

# 评估每个玩家的最佳手牌
results = []
for i, hand in enumerate(hands):
    all_cards = hand + community
    best = get_best_poker_hand(all_cards)
    results.append((i + 1, best))

# 排序找出赢家
results.sort(key=lambda x: x[1].score, reverse=True)
winner = results[0]
print(f"赢家: 玩家{winner[0]}, 牌型: {winner[1].rank.name_zh}")
```

## 测试

```bash
# 运行测试
python -m pytest playing_card_utils_test.py -v

# 或直接运行
python playing_card_utils_test.py
```

## 依赖

无外部依赖，仅使用 Python 标准库。

## 作者

AllToolkit

## 版本

1.0.0