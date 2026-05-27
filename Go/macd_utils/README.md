# MACD Utils - Go MACD 技术指标工具库

完整的 MACD (Moving Average Convergence Divergence) 技术分析工具库，零外部依赖。

## 功能特性

### 核心 MACD 计算
- **EMA 计算**: 指数移动平均线，支持任意周期
- **SMA 计算**: 简单移动平均线
- **MACD 线**: 快速EMA - 慢速EMA
- **信号线**: MACD线的EMA
- **柱状图**: MACD线 - 信号线

### 信号检测
- **交叉信号**: MACD与信号线的金叉/死叉
- **零轴穿越**: MACD穿越零轴的买入/卖出信号
- **信号强度**: 0-1范围内的强度评分
- **置信度**: strong/moderate/weak三级评估

### 趋势分析
- **趋势判断**: 牛市/熊市/中性
- **趋势强度**: 0-1范围内的强度评分
- **动量状态**: 加速/减速/稳定
- **趋势持续时间**: 当前趋势持续周期数

### 背离检测
- **看涨背离**: 价格新低，MACD走高
- **看跌背离**: 价格新高，MACD走低
- **背离强度**: 0-1范围内的强度评分

### 状态检测
- **超买检测**: MACD高于阈值
- **超卖检测**: MACD低于阈值
- **状态描述**: 强势看涨/弱势看涨/强势看跌/弱势看跌/中性

### 实时计算
- **增量计算**: 单点价格更新MACD值
- **滚动更新**: 适用于实时数据流

## 安装

```go
import "github.com/ayukyo/alltoolkit/Go/macd_utils"
```

## 使用示例

### 基础 MACD 计算

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/macd_utils"
)

func main() {
    // 股票收盘价数据
    prices := []float64{
        44.12, 44.23, 44.52, 43.95, 44.45,
        44.65, 44.87, 45.12, 45.35, 45.20,
        45.50, 45.80, 46.10, 46.25, 46.50,
        // ... 更多数据
    }

    // 使用默认参数(12, 26, 9)计算MACD
    result, err := macd_utils.CalculateMACDDefault(prices)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    // 输出最新MACD值
    lastIdx := len(prices) - 1
    fmt.Printf("MACD Line: %.4f\n", result.MACDLine[lastIdx])
    fmt.Printf("Signal Line: %.4f\n", result.SignalLine[lastIdx])
    fmt.Printf("Histogram: %.4f\n", result.Histogram[lastIdx])
}
```

### 自定义参数计算

```go
// 使用自定义参数(快线周期, 慢线周期, 信号线周期)
result, err := macd_utils.CalculateMACD(prices, 8, 17, 9)
if err != nil {
    fmt.Println("Error:", err)
    return
}
```

### 检测交易信号

```go
// 查找交叉信号(金叉/死叉)
signals := macd_utils.FindCrossovers(result)
for _, sig := range signals {
    fmt.Printf("[%d] %s 信号, 强度: %.2f, 置信度: %s\n",
        sig.Index, sig.Type, sig.Strength, sig.Confidence)
}

// 查找零轴穿越信号
zeroSignals := macd_utils.FindZeroLineCrossovers(result)
for _, sig := range zeroSignals {
    fmt.Printf("[%d] %s 信号, MACD值: %.4f\n",
        sig.Index, sig.Type, sig.Value)
}
```

### 趋势分析

```go
trend := macd_utils.AnalyzeTrend(result)
fmt.Printf("趋势: %s\n", trend.Trend)           // bullish/bearish/neutral
fmt.Printf("强度: %.2f\n", trend.Strength)      // 0-1
fmt.Printf("动量: %s\n", trend.Momentum)         // accelerating/decelerating/stable
fmt.Printf("持续: %d 周期\n", trend.Duration)   // 趋势持续周期数
```

### 背离检测

```go
// 检测价格与MACD之间的背离
divergences := macd_utils.FindDivergences(prices, result, 5)
for _, div := range divergences {
    fmt.Printf("[%d-%d] %s 背离, 强度: %.2f\n",
        div.StartIndex, div.EndIndex, div.Type, div.Strength)
}
```

### 超买超卖检测

```go
// 检测超买(MACD > threshold)
overbought, value := macd_utils.IsOverbought(result, 0.5)
if overbought {
    fmt.Printf("超买! MACD值: %.4f\n", value)
}

// 检测超卖(MACD < threshold)
oversold, value := macd_utils.IsOversold(result, -0.5)
if oversold {
    fmt.Printf("超卖! MACD值: %.4f\n", value)
}
```

### 状态判断

```go
state := macd_utils.GetMACDState(result)
fmt.Println("MACD状态:", state)
// 可能的值: strong_bullish, weakening_bullish,
//          strong_bearish, weakening_bearish, neutral
```

### 实时增量计算

```go
// 已知的上一期EMA值
prevFastEMA := 45.2
prevSlowEMA := 44.8
prevSignalEMA := 0.3

// 新价格
newPrice := 46.0

// 计算新的MACD值
newFast, newSlow, newMACD, newSignal, newHist := 
    macd_utils.CalculateMACDForPrice(
        prevFastEMA, prevSlowEMA, prevSignalEMA, newPrice,
        12, 26, 9,
    )

fmt.Printf("新MACD: %.4f, 新信号线: %.4f, 新柱状图: %.4f\n",
    newMACD, newSignal, newHist)
```

### EMA/SMA 单独使用

```go
// 计算EMA
ema, err := macd_utils.CalculateEMA(prices, 12)
if err != nil {
    fmt.Println("Error:", err)
    return
}
fmt.Printf("12日EMA: %.4f\n", ema[len(ema)-1])

// 计算SMA
sma, err := macd_utils.CalculateSMA(prices, 20)
if err != nil {
    fmt.Println("Error:", err)
    return
}
fmt.Printf("20日SMA: %.4f\n", sma[len(sma)-1])
```

## 数据结构

### MACDResult
```go
type MACDResult struct {
    MACDLine   []float64 // MACD线
    SignalLine []float64 // 信号线
    Histogram  []float64 // 柱状图
}
```

### MACDSignal
```go
type MACDSignal struct {
    Index      int     // 信号索引位置
    Type       string  // 信号类型
    Value      float64 // MACD值
    Strength   float64 // 信号强度(0-1)
    Price      float64 // 价格(可选)
    Confidence string  // 置信度(strong/moderate/weak)
}
```

### Divergence
```go
type Divergence struct {
    StartIndex int     // 背离开始索引
    EndIndex   int     // 背离结束索引
    Type       string  // 背离类型(bullish/bearish)
    Strength   float64 // 背离强度(0-1)
}
```

### TrendAnalysis
```go
type TrendAnalysis struct {
    Trend         string  // 趋势(bullish/bearish/neutral)
    Strength      float64 // 趋势强度(0-1)
    Momentum      string  // 动量(accelerating/decelerating/stable)
    MomentumValue float64 // 动量值
    Duration      int     // 趋势持续周期数
}
```

## 技术说明

### MACD 计算公式
```
MACD Line = EMA(fast) - EMA(slow)
Signal Line = EMA(MACD Line, signal_period)
Histogram = MACD Line - Signal Line
```

### EMA 计算公式
```
EMA_today = (Price_today - EMA_yesterday) * multiplier + EMA_yesterday
multiplier = 2 / (period + 1)
```

### 默认参数
- 快线周期: 12
- 慢线周期: 26
- 信号线周期: 9

### 时间复杂度
- EMA计算: O(n)
- MACD计算: O(n)
- 信号检测: O(n)
- 背离检测: O(n²) (在最坏情况下)

## 应用场景

- 股票技术分析
- 期货交易系统
- 加密货币量化
- 外汇交易策略
- 算法交易系统
- 金融数据分析
- 量化投资研究

## 测试覆盖

50+ 单元测试，覆盖：
- EMA/SMA 计算
- MACD 计算
- 交叉信号检测
- 零轴穿越检测
- 背离检测
- 趋势分析
- 超买超卖检测
- 边界条件处理
- 错误处理

## License

MIT License