package main

import (
	"fmt"
	"math"

	macd_utils "github.com/ayukyo/alltoolkit/Go/macd_utils"
)

func main() {
	fmt.Println("=== MACD Utils 示例 ===")
	fmt.Println()

	// 示例1: 基础MACD计算
	fmt.Println("1. 基础 MACD 计算")
	fmt.Println("------------------")

	// 模拟股票价格数据 (100天)
	prices := generateStockPrices(100)

	result, err := macd_utils.CalculateMACDDefault(prices)
	if err != nil {
		fmt.Println("错误:", err)
		return
	}

	// 输出最新值
	lastIdx := len(prices) - 1
	fmt.Printf("价格数据: %d 天\n", len(prices))
	fmt.Printf("最新价格: %.2f\n", prices[lastIdx])
	fmt.Printf("MACD线:   %.4f\n", result.MACDLine[lastIdx])
	fmt.Printf("信号线:   %.4f\n", result.SignalLine[lastIdx])
	fmt.Printf("柱状图:   %.4f\n", result.Histogram[lastIdx])
	fmt.Println()

	// 示例2: 自定义参数
	fmt.Println("2. 自定义参数计算")
	fmt.Println("------------------")

	// 使用更快的参数(5, 13, 4)适合短线交易
	result2, err := macd_utils.CalculateMACD(prices, 5, 13, 4)
	if err != nil {
		fmt.Println("错误:", err)
		return
	}
	fmt.Printf("参数(5, 13, 4): MACD=%.4f, 信号=%.4f, 柱=%.4f\n",
		result2.MACDLine[lastIdx], result2.SignalLine[lastIdx], result2.Histogram[lastIdx])
	fmt.Println()

	// 示例3: 信号检测
	fmt.Println("3. 交易信号检测")
	fmt.Println("------------------")

	// 交叉信号
	signals := macd_utils.FindCrossovers(result)
	fmt.Printf("检测到 %d 个交叉信号\n", len(signals))
	for i, sig := range signals {
		if i < 5 { // 只显示前5个
			fmt.Printf("[%d] 类型=%s, 强度=%.2f, 置信度=%s\n",
				sig.Index, sig.Type, sig.Strength, sig.Confidence)
		}
	}

	// 零轴穿越
	zeroSignals := macd_utils.FindZeroLineCrossovers(result)
	fmt.Printf("检测到 %d 个零轴穿越信号\n", len(zeroSignals))
	for i, sig := range zeroSignals {
		if i < 3 { // 只显示前3个
			fmt.Printf("[%d] 类型=%s, MACD值=%.4f\n",
				sig.Index, sig.Type, sig.Value)
		}
	}
	fmt.Println()

	// 示例4: 趋势分析
	fmt.Println("4. 趋势分析")
	fmt.Println("-----------")

	trend := macd_utils.AnalyzeTrend(result)
	fmt.Printf("当前趋势: %s\n", trend.Trend)
	fmt.Printf("趋势强度: %.2f (0-1)\n", trend.Strength)
	fmt.Printf("动量状态: %s\n", trend.Momentum)
	fmt.Printf("持续周期: %d 天\n", trend.Duration)
	fmt.Println()

	// 示例5: 背离检测
	fmt.Println("5. 背离检测")
	fmt.Println("-----------")

	divergences := macd_utils.FindDivergences(prices, result, 10)
	fmt.Printf("检测到 %d 个背离信号\n", len(divergences))
	for i, div := range divergences {
		if i < 3 { // 只显示前3个
			fmt.Printf("[%d-%d] %s背离, 强度=%.2f\n",
				div.StartIndex, div.EndIndex, div.Type, div.Strength)
		}
	}
	fmt.Println()

	// 示例6: 超买超卖
	fmt.Println("6. 超买超卖检测")
	fmt.Println("---------------")

	overbought, obValue := macd_utils.IsOverbought(result, 0.5)
	oversold, osValue := macd_utils.IsOversold(result, -0.5)
	fmt.Printf("超买阈值: 0.5, 当前MACD: %.4f, 是否超买: %v\n", obValue, overbought)
	fmt.Printf("超卖阈值: -0.5, 当前MACD: %.4f, 是否超卖: %v\n", osValue, oversold)
	fmt.Println()

	// 示例7: 状态判断
	fmt.Println("7. MACD状态")
	fmt.Println("-----------")

	state := macd_utils.GetMACDState(result)
	fmt.Printf("当前MACD状态: %s\n", state)
	switch state {
	case "strong_bullish":
		fmt.Println("解读: 强势看涨，MACD在零轴上方且柱状图为正")
	case "weakening_bullish":
		fmt.Println("解读: 弱势看涨，MACD在零轴上方但柱状图为负")
	case "strong_bearish":
		fmt.Println("解读: 强势看跌，MACD在零轴下方且柱状图为负")
	case "weakening_bearish":
		fmt.Println("解读: 弱势看跌，MACD在零轴下方但柱状图为正")
	case "neutral":
		fmt.Println("解读: 中性状态")
	}
	fmt.Println()

	// 示例8: 柱状图强度
	fmt.Println("8. 柱状图强度分析")
	fmt.Println("-----------------")

	strength := macd_utils.CalculateHistogramStrength(result, 5)
	fmt.Printf("最近5期柱状图平均强度: %.4f\n", strength)
	fmt.Println()

	// 示例9: 实时增量计算
	fmt.Println("9. 实时增量计算")
	fmt.Println("---------------")

	// 获取上一期EMA值作为起点
	validIdx := findLastValidIndex(result)
	prevFast := result.MACDLine[validIdx] + result.SignalLine[validIdx] // 近似
	prevSlow := result.SignalLine[validIdx]                            // 近似
	prevSignal := result.SignalLine[validIdx]

	newPrice := prices[lastIdx] + 2.0 // 假设新价格
	newFast, newSlow, newMACD, newSignal, newHist := 
		macd_utils.CalculateMACDForPrice(prevFast, prevSlow, prevSignal, newPrice, 12, 26, 9)

	fmt.Printf("新价格: %.2f\n", newPrice)
	fmt.Printf("新MACD线: %.4f\n", newMACD)
	fmt.Printf("新信号线: %.4f\n", newSignal)
	fmt.Printf("新柱状图: %.4f\n", newHist)
	fmt.Println()

	// 示例10: 默认参数
	fmt.Println("10. 默认参数")
	fmt.Println("------------")

	fast, slow, signal := macd_utils.DefaultMACDParams()
	fmt.Printf("默认参数: 快线=%d, 慢线=%d, 信号线=%d\n", fast, slow, signal)
	fmt.Println()

	// 示例11: EMA单独使用
	fmt.Println("11. EMA单独计算")
	fmt.Println("---------------")

	ema12, err := macd_utils.CalculateEMA(prices, 12)
	if err == nil {
		fmt.Printf("12日EMA最新值: %.2f\n", ema12[findLastValidIndexSimple(ema12)])
	}

	ema26, err := macd_utils.CalculateEMA(prices, 26)
	if err == nil {
		fmt.Printf("26日EMA最新值: %.2f\n", ema26[findLastValidIndexSimple(ema26)])
	}
	fmt.Println()

	// 示例12: SMA单独使用
	fmt.Println("12. SMA单独计算")
	fmt.Println("---------------")

	sma20, err := macd_utils.CalculateSMA(prices, 20)
	if err == nil {
		fmt.Printf("20日SMA最新值: %.2f\n", sma20[findLastValidIndexSimple(sma20)])
	}

	fmt.Println()
	fmt.Println("=== 示例完成 ===")
}

// 生成模拟股票价格数据
func generateStockPrices(count int) []float64 {
	prices := make([]float64, count)
	startPrice := 100.0

	for i := 0; i < count; i++ {
		// 添加趋势、周期波动和噪声
		trend := float64(i) * 0.3         // 上涨趋势
		cycle := 10.0 * math.Sin(float64(i) / 15.0) // 周期波动
		noise := 2.0 * math.Sin(float64(i) * 0.5)   // 小波动

		prices[i] = startPrice + trend + cycle + noise
	}

	return prices
}

// 找到最后一个有效索引
func findLastValidIndex(result *macd_utils.MACDResult) int {
	for i := len(result.MACDLine) - 1; i >= 0; i-- {
		if !math.IsNaN(result.MACDLine[i]) && !math.IsNaN(result.SignalLine[i]) {
			return i
		}
	}
	return -1
}

// 找到最后一个有效索引(简单版)
func findLastValidIndexSimple(data []float64) int {
	for i := len(data) - 1; i >= 0; i-- {
		if !math.IsNaN(data[i]) {
			return i
		}
	}
	return -1
}