# Spaced Repetition Utils

高效的间隔重复学习工具库，实现 SM-2 算法和 Leitner 系统。零外部依赖。

## 功能特性

- **SM-2 算法**: SuperMemo 2 算法的完整实现，动态计算最优复习间隔
- **Leitner 系统**: 多盒卡片调度系统，固定间隔复习
- **卡片管理**: 创建、更新、调度闪卡，支持序列化
- **学习统计**: 跟踪学习进度、记忆保持率、平均难度系数
- **卡片库管理**: 按主题组织卡片，支持标签分类
- **遗忘曲线**: 预测记忆保持概率，计算最优复习时间
- **辅助函数**: Q&A 卡片、双向卡片、填空卡片、输入型卡片

## 快速开始

### 基础使用

```python
from spaced_repetition_utils.mod import SpacedRepetition, Rating

# 创建 SM-2 系统实例
sr = SpacedRepetition(scheduler="sm2")

# 创建闪卡
card = sr.create_card(
    front="What is the capital of France?",
    back="Paris",
    deck="geography",
    tags=["europe", "capitals"]
)

# 复习卡片
result = sr.review_card(card, Rating.GOOD)

print(f"下次复习: {card.due}")
print(f"间隔: {card.interval} 天")
print(f"难度系数: {card.ease_factor}")
```

### Leitner 系统

```python
from spaced_repetition_utils.mod import SpacedRepetition, Rating

# 创建 Leitner 系统实例
sr = SpacedRepetition(scheduler="leitner")

# 创建卡片
card = sr.create_card("Hello", "你好", deck="vocabulary")

# 复习 - 正确答案会提升到更高盒子
sr.review_card(card, Rating.GOOD)  # Box 1 -> Box 2

# 错误答案会回退到 Box 1
sr.review_card(card, Rating.AGAIN)  # Box 2 -> Box 1
```

### 卡片类型辅助函数

```python
from spaced_repetition_utils.mod import (
    create_question_card,
    create_reversable_card,
    create_cloze_card,
    create_type_in_card,
    check_type_in_answer,
)

# Q&A 卡片
card = create_question_card(
    question="What is the speed of light?",
    answer="299,792,458 m/s",
    deck="physics"
)

# 双向卡片 (词汇学习)
card1, card2 = create_reversable_card(
    front="Cat",
    back="猫",
    deck="vocabulary"
)
# card1: Cat -> 猫
# card2: 猫 -> Cat

# 填空卡片
cards = create_cloze_card(
    text="The Battle of Hastings occurred in 1066.",
    clozes=[(34, 38)],  # "1066"
    deck="history"
)

# 输入型卡片
type_card = create_type_in_card(
    prompt="What is the chemical symbol for water?",
    correct_answers=["H2O", "H₂O"],
    case_sensitive=False
)

# 检查答案
is_correct = check_type_in_answer(type_card, "h2o")  # True
```

## 核心概念

### SM-2 算法参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| min_ease_factor | 1.3 | 最小难度系数 |
| initial_ease_factor | 2.5 | 初始难度系数 |
| easy_bonus | 1.3 | Easy 答案的间隔乘数 |
| interval_modifier | 1.0 | 全局间隔修饰符 |
| graduating_interval | 1.0 | 首次成功后的间隔 |
| easy_interval | 4.0 | 首次 Easy 答案的间隔 |

### Leitner 系统间隔

| 盒子 | 复习间隔 |
|------|----------|
| Box 1 | 当天 |
| Box 2 | 1 天 |
| Box 3 | 3 天 |
| Box 4 | 7 天 |
| Box 5 | 14 天 |
| Box 6 | 30 天 |
| Box 7 | 60 天 |
| Box 8 | 120 天 |

### 评分系统

| 评分 | 值 | 说明 |
|------|----|----|
| AGAIN | 1 | 完全忘记，需要重新学习 |
| HARD | 2 | 错误但有印象 |
| GOOD | 3 | 正确但有些犹豫 |
| EASY | 4 | 立即完美回忆 |

## API 参考

### SpacedRepetition

主类，整合调度器和卡片库管理。

```python
# 创建实例
sr = SpacedRepetition(
    scheduler="sm2",  # 或 "leitner"
    sm2_config={"min_ease_factor": 1.3},
    leitner_config={"intervals": [0, 1, 3, 7, 14]}
)

# 卡片管理
card = sr.create_card(front, back, deck, tags)
sr.create_deck(name)
deck = sr.get_deck(name)

# 复习
result = sr.review_card(card, Rating.GOOD)

# 查询
due_cards = sr.get_due_cards(deck_name, limit=20)
stats = sr.get_statistics(deck_name)

# 导入导出
json_data = sr.export_to_json()
sr.import_from_json(json_data)
```

### Card

闪卡数据结构。

```python
card = Card(
    id="unique-id",
    front="问题",
    back="答案",
    deck="deck-name",
    tags=["tag1", "tag2"]
)

# 属性
card.interval      # 当前间隔（天）
card.repetitions   # 成功复习次数
card.ease_factor   # 难度系数
card.due           # 下次复习日期
card.lapses        # 遗忘次数

# 方法
card.is_due()      # 是否到期
card.to_dict()     # 序列化
Card.from_dict()   # 反序列化
```

### SM2Scheduler

SM-2 算法调度器。

```python
scheduler = SM2Scheduler()

# 计算新间隔
interval, reps, ef = scheduler.calculate_interval(card, Rating.GOOD)

# 复习卡片
result = scheduler.review_card(card, Rating.GOOD)
```

### LeitnerScheduler

Leitner 系统调度器。

```python
scheduler = LeitnerScheduler(
    intervals=[0, 1, 3, 7, 14, 30, 60, 120],
    num_boxes=8
)

# 获取盒子间隔
interval = scheduler.get_interval_for_box(box)

# 计算下次盒子
next_box = scheduler.get_next_box(current_box, correct=True)
```

### 工具函数

```python
# 计算记忆保持率
retention = calculate_retention(reviews, period_days=7)

# 遗忘曲线预测
prob = predict_forgetting_curve(days_since_review, stability)

# 最优复习时间
days = calculate_optimal_review_time(stability, target_retention=0.9)

# 生成复习计划
schedule = generate_review_schedule(cards, max_per_day=20)

# 计算卡片优先级
priority = calculate_card_priority(card)

# 按优先级排序
sorted_cards = sort_cards_by_priority(cards)
```

## 测试

运行测试：

```bash
python Python/spaced_repetition_utils/spaced_repetition_utils_test.py
```

测试覆盖：
- SM-2 算法间隔计算
- Leitner 系统盒子调度
- 卡片创建和序列化
- 卡片库管理
- 复习结果记录
- 遗忘曲线预测
- 边界值处理

## 示例

完整示例见 `examples/usage_examples.py`：

```bash
python Python/spaced_repetition_utils/examples/usage_examples.py
```

## 参考文献

- [SuperMemo 2 Algorithm](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2)
- [Leitner System](https://en.wikipedia.org/wiki/Leitner_system)
- [Anki Manual](https://docs.ankiweb.net/)

## 许可证

MIT License