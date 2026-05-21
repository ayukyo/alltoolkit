# Blackjack Utils

21 点（Blackjack）游戏完整工具集，零依赖。

## 功能特性

- **牌组管理**: 创建、洗牌、发牌
- **手牌评估**: 计算得分、识别手牌类型
- **基础策略表**: 标准 21 点策略建议
- **牌数计算**: Hi-Lo、KO、Hi-Opt 系统
- **概率计算**: 获胜概率、最优行动概率
- **下注策略**: 马丁格尔、凯利准则
- **游戏模拟**: 快速模拟验证策略

## 快速开始

```python
from blackjack_utils.mod import Deck, Hand, calculate_hand_value

# 创建牌组并洗牌
deck = Deck()
deck.shuffle()

# 发牌
hand = Hand()
hand.add_card(deck.draw())
hand.add_card(deck.draw())

# 计算手牌值
value = hand.value  # 或 calculate_hand_value(hand.cards)
print(f"手牌值: {value}")
```

## 使用示例

### 牌和牌组

```python
from blackjack_utils.mod import Card, Deck, Suit, Rank

# 创建单张牌
card = Card(Suit.HEARTS, Rank.ACE)
print(card)  # A♥

# 创建牌组（1-8 副）
deck = Deck(num_decks=6)
deck.shuffle()

# 发牌
card = deck.draw()
cards = deck.draw_multiple(2)

# 剩余牌数
remaining = deck.remaining_cards()

# 重置牌组
deck.reset()
```

### 手牌评估

```python
from blackjack_utils.mod import Hand, HandType

hand = Hand()
hand.add_card(Card(Suit.HEARTS, Rank.ACE))
hand.add_card(Card(Suit.SPADES, Rank.KING))

# 手牌值
value = hand.value  # 21

# 手牌类型
hand_type = hand.type  # HandType.BLACKJACK

# 是否是软牌（Ace 可计为 11）
is_soft = hand.is_soft  # True

# 是否爆牌
is_bust = hand.is_bust  # False
```

### 基础策略

```python
from blackjack_utils.mod import BasicStrategy, Action

strategy = BasicStrategy()

# 获取建议行动
player_hand = Hand([Card(Suit.HEARTS, Rank.TEN), Card(Suit.CLUBS, Rank.SIX)])
dealer_upcard = Card(Suit.SPADES, Rank.TEN)

action = strategy.get_action(player_hand, dealer_upcard)
print(action)  # Action.HIT 或 Action.STAND 等
```

### 牌数计算

```python
from blackjack_utils.mod import CardCounter, CountSystem

# Hi-Lo 系统计数器
counter = CardCounter(CountSystem.HI_LO)

# 观察牌
counter.observe(Card(Suit.HEARTS, Rank.TWO))   # +1
counter.observe(Card(Suit.SPADES, Rank.TEN))   # -1
counter.observe(Card(Suit.CLUBS, Rank.ACE))    # -1

# 当前计数
running_count = counter.running_count

# 真实计数（调整剩余牌数）
true_count = counter.true_count(deck.remaining_cards(), deck.num_decks)

# 下注建议
bet_size = counter.suggest_bet(base_bet=10, true_count=true_count)
```

### 概率计算

```python
from blackjack_utils.mod import ProbabilityCalculator

calc = ProbabilityCalculator()

# 计算获胜概率
player_value = 18
dealer_upcard_value = 10
win_prob = calc.win_probability(player_value, dealer_upcard_value)

# 计算爆牌概率
bust_prob = calc.bust_probability(player_value)

# 计算最优行动期望值
expected_values = calc.action_expected_values(hand, dealer_upcard, deck)
```

### 游戏模拟

```python
from blackjack_utils.mod import GameSimulator

sim = GameSimulator(num_decks=6, num_players=1)

# 模拟单局
result = sim.play_round()
print(f"玩家得分: {result.player_final}")
print(f"庄家得分: {result.dealer_final}")
print(f"结果: {result.outcome}")

# 模拟多局
stats = sim.simulate(num_rounds=10000)
print(f"胜率: {stats.win_rate}")
print(f"平均收益: {stats.average_profit}")
```

### 下注策略

```python
from blackjack_utils.mod import BettingStrategy, KellyCriterion

# 凯利准则下注
kelly = KellyCriterion(bankroll=1000, win_prob=0.49, odds=1.0)
bet = kelly.calculate_bet()

# 丁格尔策略
martingale = BettingStrategy("martingale")
next_bet = martingale.next_bet(last_result="loss", base_bet=10)
```

## API 参考

### Card / Deck

| 类/方法 | 说明 |
|---------|------|
| `Card(suit, rank)` | 单张牌 |
| `Deck(num_decks=1)` | 牌组 |
| `shuffle()` | 洗牌 |
| `draw()` | 发一张牌 |
| `draw_multiple(n)` | 发多张牌 |
| `remaining_cards()` | 剩余牌数 |

### Hand

| 属性/方法 | 说明 |
|-----------|------|
| `cards` | 手牌列表 |
| `value` | 手牌值 |
| `type` | HandType (HARD/SOFT/BLACKJACK/BUST) |
| `is_soft` | 是否软牌 |
| `is_bust` | 是否爆牌 |
| `add_card(card)` | 添加牌 |
| `can_split()` | 是否可分牌 |

### BasicStrategy

| 方法 | 说明 |
|------|------|
| `get_action(hand, dealer_upcard)` | 获取策略建议 |
| `get_action_with_surrender(hand, dealer)` | 带投降选项 |

### CardCounter

| 方法 | 说明 |
|------|------|
| `observe(card)` | 观察牌并更新计数 |
| `running_count` | 运行计数 |
| `true_count(remaining, decks)` | 真实计数 |
| `suggest_bet(base_bet, true_count)` | 下注建议 |

### ProbabilityCalculator

| 方法 | 说明 |
|------|------|
| `win_probability(player_value, dealer_upcard)` | 获胜概率 |
| `bust_probability(value)` | 爆牌概率 |
| `action_expected_values(hand, dealer, deck)` | 行动期望值 |

## 牌数系统

| 系统 | 2-6 | 7-9 | 10-A |
|------|-----|-----|------|
| Hi-Lo | +1 | 0 | -1 |
| KO | +1 | 0 | -1（无真实计数） |
| Hi-Opt I | +1 | 0 | -1（Ace=0） |
| Hi-Opt II | +1/+2 | +1 | -2 |

## 基础策略要点

- **硬牌 12-16**: 对庄家 2-6 站住，对 7-A 拿牌
- **软牌 17-18**: 对庄家 2-8 翻倍，对 9-A 拿牌
- **11**: 翻倍（除非庄家 A）
- **10**: 翻倍（除非庄家 10 或 A）
- **分牌**: A-A、8-8 必分；10-10 不分

---

**测试覆盖**: 完整测试套件，覆盖牌组、手牌、策略、计数、概率等