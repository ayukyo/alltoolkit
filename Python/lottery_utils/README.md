# lottery_utils - 中国彩票工具模块

零外部依赖的中国彩票工具库，支持双色球、大乐透、排列三/五、七星彩。

## 功能特性

- 🎲 **号码生成** - 支持多种彩票类型的随机号码生成
- 🏆 **中奖判断** - 自动计算奖项等级和奖金
- 📊 **概率计算** - 各奖项的中奖概率
- 📈 **数据分析** - 历史数据频率分析、热号冷号、奇偶比等
- 🎰 **购票模拟** - 模拟购票计算收益

## 支持的彩票类型

| 类型 | 规则 |
|------|------|
| 双色球 (SSQ) | 6红球(1-33) + 1蓝球(1-16) |
| 大乐透 (DLT) | 5前区(1-35) + 2后区(1-12) |
| 排列三 (P3) | 3位数字(0-9) |
| 排列五 (P5) | 5位数字(0-9) |
| 七星彩 (QXC) | 7位数字(0-9) |

## 安装

无需安装，直接复制 `lottery_utils.py` 到项目中即可使用。

## 快速开始

### 双色球

```python
from lottery_utils import SSQUtils, LotteryType

# 生成号码
result = SSQUtils.generate()
print(result)  # 双色球: 1 5 12 18 25 30 + 8

# 批量生成
results = SSQUtils.generate_multiple(5)
for r in results:
    print(r)

# 检查中奖
my_numbers = SSQUtils.generate(seed=42)
winning_numbers = SSQUtils.generate(seed=100)
prize = SSQUtils.check_prize(my_numbers, winning_numbers)
if prize:
    print(f"恭喜获得 {prize.prize_name}！奖金: {prize.prize_amount/100}元")

# 计算概率
prob = SSQUtils.calculate_probability(1)  # 一等奖概率
print(f"一等奖概率: 1/{1/prob:.0f}")
```

### 大乐透

```python
from lottery_utils import DLTUtils

# 生成号码
result = DLTUtils.generate()
print(result)  # 大乐透: 3 8 15 22 30 + 4 9

# 检查中奖
prize = DLTUtils.check_prize(my_numbers, winning_numbers)
```

### 排列三/五

```python
from lottery_utils import P3P5Utils

# 排列三
result = P3P5Utils.generate_p3()
print(result)

# 排列五
result = P3P5Utils.generate_p5()
print(result)

# 检查中奖（支持直选、组选三、组选六）
prize = P3P5Utils.check_prize_p3(my_numbers, winning_numbers)
```

### 七星彩

```python
from lottery_utils import QXCUtils

result = QXCUtils.generate()
print(result)

prize = QXCUtils.check_prize(my_numbers, winning_numbers)
```

### 统一接口

```python
from lottery_utils import quick_pick, LotteryType, generate_lucky_numbers

# 快速选号
results = quick_pick("双色球", 5)  # 生成5注

# 使用枚举类型
result = generate_lucky_numbers(LotteryType.SSQ)
```

### 数据分析

```python
from lottery_utils import LotteryAnalyzer

# 分析历史数据频率
history = [...]  # LotteryResult 列表
freq = LotteryAnalyzer.analyze_frequency(history, LotteryType.SSQ)
print(freq["main"])  # 主号频率
print(freq["special"])  # 特别号频率

# 找热号冷号
hot_cold = LotteryAnalyzer.find_hot_cold_numbers(history, LotteryType.SSQ)
print(f"热号: {hot_cold['hot']}")
print(f"冷号: {hot_cold['cold']}")

# 计算奇偶比
result = SSQUtils.generate()
ratio = LotteryAnalyzer.calculate_odd_even_ratio(result)
print(f"奇偶比: {ratio['odd']}:{ratio['even']}")

# 计算和值
total = LotteryAnalyzer.calculate_sum(result)

# 计算跨度
span = LotteryAnalyzer.calculate_span(result)

# 找连号
consecutive = LotteryAnalyzer.find_consecutive(result)
```

### 购票模拟

```python
from lottery_utils import LotterySimulator

# 模拟购买100注双色球
result = LotterySimulator.simulate_ssq(100)
print(f"开奖号码: {result['winning_numbers']}")
print(f"花费: {result['cost']/100}元")
print(f"中奖情况: {result['prize_breakdown']}")
print(f"收益: {result['profit']/100}元")
print(f"投资回报率: {result['roi']*100:.2f}%")
```

## 奖项说明

### 双色球奖项

| 奖项 | 条件 | 默认奖金 |
|------|------|----------|
| 一等奖 | 6红+1蓝 | 500万 |
| 二等奖 | 6红+0蓝 | 100万 |
| 三等奖 | 5红+1蓝 | 3000元 |
| 四等奖 | 5红+0蓝 / 4红+1蓝 | 200元 |
| 五等奖 | 4红+0蓝 / 3红+1蓝 | 10元 |
| 六等奖 | 2红+1蓝 / 1红+1蓝 / 0红+1蓝 | 5元 |

### 排列三奖项

| 奖项 | 条件 | 奖金 |
|------|------|------|
| 直选 | 完全匹配（位置+数字） | 1040元 |
| 组选三 | 三个数字有两个相同，匹配不分顺序 | 346元 |
| 组选六 | 三个数字各不相同，匹配不分顺序 | 173元 |

## 运行测试

```bash
python lottery_utils_test.py
```

## 注意事项

1. 本模块仅供学习和娱乐使用
2. 彩票中奖概率极低，请理性购彩
3. 实际奖金以官方公告为准

## License

MIT