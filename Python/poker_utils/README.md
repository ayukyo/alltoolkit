# Poker Utils


扑克牌工具集 (Poker Utils)
==========================

零外部依赖的扑克牌处理工具，支持：
- 创建牌组、洗牌、发牌
- 牌型判断（高牌到皇家同花顺）
- 手牌比较和胜负判定
- 概率计算

作者: AllToolkit 自动生成
日期: 2026-04-24


## 功能

### 类

- **Suit**: 花色枚举
- **Rank**: 牌面大小枚举
- **HandRank**: 牌型等级
- **Card**: 扑克牌类
  方法: to_dict, from_string
- **Deck**: 牌组类
  方法: shuffle, draw, draw_one, add_card, add_cards ... (10 个方法)
- **Hand**: 手牌类
  方法: evaluate, get_rank_name, compare, to_dict
- **PokerGame**: 扑克游戏辅助类
  方法: new_round, deal_to_players, deal_community, flop, turn ... (8 个方法)

### 函数

- **create_deck(**) - 创建新的牌组
- **shuffle_deck(deck**) - 洗牌
- **deal_hands(deck, num_players, cards_per_hand**) - 发牌给多个玩家
- **evaluate_hand(cards**) - 评估手牌牌型
- **compare_hands(hand1, hand2**) - 比较两手牌
- **best_hand(seven_cards**) - 从7张牌中选出最佳的5张牌组合（德州扑克场景）
- **hand_probability(hand_rank**) - 获取牌型概率（在5张随机牌中出现的概率）
- **hand_combinations_count(hand_rank**) - 获取牌型的组合数
- **cards_to_string(cards, chinese**) - 将牌列表转换为字符串
- **string_to_cards(s**) - 从字符串解析多张牌

... 共 37 个函数

## 使用示例

```python
from mod import create_deck

# 使用 create_deck
result = create_deck()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
