# dice_utils - 骰子工具模块 🎲

完整的骰子游戏和概率计算工具库，零外部依赖，纯 Go 标准库实现。

## 功能概览

### 🎯 基础掷骰
- **单骰掷骰**: `Die.Roll()` - 掷一个骰子
- **多骰掷骰**: `RollDice(numDice, sides)` - 掷多个骰子
- **带修饰符**: `RollWithModifier(numDice, sides, modifier)` - 加/减修饰符
- **骰子表达式**: `RollNotation("2d6+5")` - 解析如 "2d6+5"、"1d20-2" 等表达式
- **快速函数**: `RollD4()`, `RollD6()`, `RollD8()`, `RollD10()`, `RollD12()`, `RollD20()`, `RollD100()`

### 📊 概率计算
- **精确概率**: `Probability(numDice, sides, target)` - 计算精确概率
- **概率范围**: `ProbabilityRange(numDice, sides, target)` - 精确/至少/至多概率
- **组合计数**: `CountWays(numDice, sides, target)` - 计算达成目标的方式数
- **全概率分布**: `AllProbabilities(numDice, sides)` - 所有可能值的概率
- **蒙特卡洛模拟**: `MonteCarloProbability(numDice, sides, target, simulations)` - 模拟估算概率
- **概率表**: `ProbabilityTable(numDice, sides)` - 格式化概率表字符串

### 📈 统计分析
- **期望值**: `ExpectedValue(numDice, sides)` - 计算期望值
- **方差**: `Variance(numDice, sides)` - 计算方差
- **标准差**: `StandardDeviation(numDice, sides)` - 计算标准差
- **最可能结果**: `MostProbableResult(numDice, sides)` - 返回最可能的值
- **频率分布**: `Histogram(numRolls, numDice, sides)` - 多次掷骰的频率分布

### 🎮 游戏模式 (Yahtzee/D&D)
- **Yahtzee检测**: `IsYahtzee(dice)` - 五同检查
- **Full House**: `IsFullHouse(dice)` - 三同+两同检查
- **小顺子**: `IsSmallStraight(dice)` - 4连序列检查
- **大顺子**: `IsLargeStraight(dice)` - 5连序列检查
- **同值计数**: `CountOfKind(dice)` - 返回最多同值的数量和值
- **暴击检测**: `CriticalHit(roll)`, `CriticalMiss(roll)` - D&D 20/1 检测
- **优势/劣势**: `Advantage(sides)`, `Disadvantage(sides)` - 掷两次取高/低

### ⚡ 特殊掷骰
- **爆炸骰**: `ExplodingDie(sides, maxExplodes)` - 最大值时继续掷骰
- **保留最高**: `KeepHighest(numDice, sides, keep)` - 掷骰后保留最高 N 个
- **保留最低**: `KeepLowest(numDice, sides, keep)` - 掷骰后保留最低 N 个
- **选择重掷**: `RerollSelective(dice, sides, indices)` - 重掷指定位置的骰子
- **FUDGE骰**: `FudgeRoll(numDice)` - -1/0/+1 骰子 (用于 FUDGE 系统)

### 🪙 其他工具
- **硬币翻转**: `CoinFlip()`, `CoinFlipN(n)` - 模拟硬币翻转
- **百分骰**: `PercentileRoll()` - 掷 d100
- **骰子求和**: `SumDice(dice)`, `SumOfValue(dice, value)` - 骰子值求和
- **种子设置**: `SetSeed(seed)` - 设置随机种子以复现结果

## 使用示例

### 基础掷骰
```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/dice_utils"
)

func main() {
    // 掷 2d6
    roll, _ := dice_utils.RollDice(2, 6)
    fmt.Printf("2d6: %v = %d\n", roll.Dice, roll.Total)
    
    // 使用骰子表达式
    roll2, _ := dice_utils.RollNotation("1d20+5")
    fmt.Printf("1d20+5: %d\n", roll2.Total)
    
    // 快速函数
    d20 := dice_utils.RollD20()
    fmt.Printf("D20: %d\n", d20)
}
```

### 概率计算
```go
// 计算 2d6 掷出 7 的概率
prob := dice_utils.Probability(2, 6, 7)
fmt.Printf("Probability of 7: %.4f (%.2f%%)\n", prob, prob*100)

// 详细概率信息
pr := dice_utils.ProbabilityRange(2, 6, 7)
fmt.Printf("Ways: %d, Total: %d\n", pr.Ways, pr.Total)
fmt.Printf("At least 7: %.2f%%\n", pr.AtLeast*100)
fmt.Printf("At most 7: %.2f%%\n", pr.AtMost*100)

// 获取最可能的值
mostProb := dice_utils.MostProbableResult(2, 6)
fmt.Printf("Most probable: %v\n", mostProb) // [7]
```

### D&D 场景
```go
// 优势掷骰
adv, _ := dice_utils.Advantage(20)
fmt.Printf("Advantage: %d\n", adv.Total)

// 暴击检测
d20 := dice_utils.RollD20()
if dice_utils.CriticalHit(d20) {
    fmt.Println("🎉 CRITICAL HIT!")
}

// 爆炸骰 (如 Savage Worlds 系统)
total, results := dice_utils.ExplodingDie(6, 5)
fmt.Printf("Exploding d6: %v = %d\n", results, total)
```

### Yahtzee 检测
```go
dice := []int{6, 6, 6, 6, 6}

fmt.Printf("Is Yahtzee: %v\n", dice_utils.IsYahtzee(dice)) // true

dice2 := []int{1, 1, 1, 2, 2}
fmt.Printf("Is Full House: %v\n", dice_utils.IsFullHouse(dice2)) // true

dice3 := []int{1, 2, 3, 4, 5}
fmt.Printf("Is Large Straight: %v\n", dice_utils.IsLargeStraight(dice3)) // true
```

### 角色属性生成 (D&D 5e)
```go
// 掷 4d6，保留最高的 3 个（用于生成角色属性）
kept, total, _ := dice_utils.KeepHighest(4, 6, 3)
fmt.Printf("4d6 drop lowest: %v = %d\n", kept, total)
```

### 统计分析
```go
// 2d6 统计
ev := dice_utils.ExpectedValue(2, 6)       // 7.0
var := dice_utils.Variance(2, 6)           // ~5.83
sd := dice_utils.StandardDeviation(2, 6)   // ~2.42

fmt.Printf("EV: %.2f, Variance: %.4f, SD: %.4f\n", ev, var, sd)
```

### 频率分布
```go
// 掷 1000 次 2d6，生成频率分布
hist, _ := dice_utils.Histogram(1000, 2, 6)
for value, count := range hist {
    fmt.Printf("%d: %d times (%.2f%%)\n", value, count, float64(count)/10)
}
```

## API 参考

### 类型

```go
type Die struct {
    Sides int
}

type DiceRoll struct {
    Dice   []int      // 各骰子的值
    Total  int        // 总和
    Count  int        // 骰子数量
    Sides  int        // 每个骰子的面数
}

type DiceConfig struct {
    NumDice  int
    Sides    int
    Modifier int
}

type ProbResult struct {
    Ways    int     // 达成该值的方式数
    Total   int     // 总可能结果数
    Exact   float64 // 精确概率
    AtLeast float64 // 至少达到该值的概率
    AtMost  float64 // 至多达到该值的概率
}
```

### 主要函数

| 函数 | 描述 |
|------|------|
| `NewDie(sides)` | 创建新骰子 |
| `RollDice(numDice, sides)` | 掷多个骰子 |
| `RollNotation(notation)` | 按表达式掷骰 ("2d6+5") |
| `Probability(numDice, sides, target)` | 计算精确概率 |
| `CountWays(numDice, sides, target)` | 计算方式数 |
| `ExpectedValue(numDice, sides)` | 期望值 |
| `Variance(numDice, sides)` | 方差 |
| `IsYahtzee(dice)` | 五同检测 |
| `IsFullHouse(dice)` | Full House 检测 |
| `Advantage(sides)` | 优势掷骰 |
| `KeepHighest(numDice, sides, keep)` | 保留最高 N 个 |

## 测试覆盖

模块包含 **92+ 单元测试**，覆盖：
- 基础掷骰功能
- 概率计算验证
- 统计函数验证
- Yahtzee/D&D 模式检测
- 特殊掷骰模式
- 边界条件处理
- 错误处理

运行测试：
```bash
go test -v
```

## 数学原理

### 概率计算
使用动态规划计算组合数，避免递归效率问题。

对于 `n` 个 `s` 面骰子掷出总和 `t`：
- 方式数 = DP[i][j] 表示用 i 个骰子达到总和 j 的方式数
- 时间复杂度: O(n × n×s)

### 期望值和方差
- 单骰期望值: E[X] = (s+1)/2
- 单骰方差: Var[X] = (s²-1)/12
- n 个骰: E[nX] = n×E[X], Var[nX] = n×Var[X]

## 适用场景

- 🎲 桌面游戏 (D&D, Yahtzee, Monopoly)
- 🎮 RPG 游戏开发
- 📊 概率教学演示
- 🧮 统计模拟实验
- 🎰 游戏平衡分析

## 许可证

MIT License