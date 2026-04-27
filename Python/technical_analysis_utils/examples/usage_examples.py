"""
技术分析工具使用示例

演示各种技术指标的计算和使用方法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from technical_analysis_utils.mod import (
    sma, ema, wma, rsi, macd, bollinger_bands,
    kdj, stochastic, atr, obv, vwap,
    williams_r, cci, momentum, roc, adx,
    detect_trend, find_support_resistance,
    golden_cross_death_cross, analyze,
    is_oversold, is_overbought,
    calculate_returns, calculate_volatility,
    max_drawdown, sharpe_ratio,
    Trend
)


def print_section(title: str):
    """打印分隔线"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


# 示例数据 - 50天的股票数据
CLOSE = [
    44.12, 44.23, 44.52, 43.91, 44.22,
    44.57, 44.24, 44.33, 44.56, 44.12,
    44.78, 44.89, 45.12, 45.23, 45.11,
    45.34, 45.67, 45.89, 46.12, 46.34,
    46.12, 45.89, 45.67, 45.45, 45.23,
    45.12, 45.34, 45.56, 45.78, 46.01,
    46.23, 46.45, 46.67, 46.89, 47.12,
    47.34, 47.56, 47.23, 46.89, 46.56,
    46.23, 45.89, 45.56, 45.23, 44.89,
    44.56, 44.23, 44.01, 43.78, 43.56
]

HIGH = [
    44.50, 44.60, 44.80, 44.30, 44.50,
    44.90, 44.60, 44.70, 44.90, 44.50,
    45.10, 45.30, 45.40, 45.50, 45.40,
    45.60, 45.90, 46.20, 46.40, 46.60,
    46.40, 46.10, 45.90, 45.70, 45.50,
    45.40, 45.60, 45.80, 46.00, 46.30,
    46.50, 46.70, 46.90, 47.10, 47.40,
    47.60, 47.80, 47.50, 47.10, 46.80,
    46.50, 46.10, 45.80, 45.50, 45.10,
    44.80, 44.50, 44.30, 44.00, 43.80
]

LOW = [
    43.90, 44.00, 44.20, 43.60, 43.90,
    44.30, 44.00, 44.10, 44.30, 43.90,
    44.60, 44.70, 44.90, 45.00, 44.90,
    45.10, 45.40, 45.60, 45.90, 46.10,
    45.90, 45.70, 45.40, 45.20, 45.00,
    44.90, 45.10, 45.30, 45.50, 45.80,
    46.00, 46.20, 46.40, 46.70, 46.90,
    47.10, 47.30, 46.70, 46.40, 46.10,
    45.80, 45.50, 45.20, 44.90, 44.60,
    44.30, 44.00, 43.80, 43.60, 43.40
]

VOLUME = [
    1000, 1200, 1500, 800, 1100,
    1300, 900, 1000, 1400, 1200,
    1600, 1800, 2000, 1500, 1700,
    1900, 2100, 2300, 2000, 1800,
    1600, 1400, 1200, 1000, 900,
    1100, 1300, 1500, 1700, 1900,
    2100, 2300, 2500, 2700, 2900,
    3100, 3300, 2800, 2400, 2000,
    1600, 1400, 1200, 1000, 900,
    800, 700, 600, 500, 400
]


def example_sma():
    """SMA 示例"""
    print_section("简单移动平均线 (SMA)")
    
    # 计算 5 日、10 日、20 日 SMA
    sma_5 = sma(CLOSE, 5)
    sma_10 = sma(CLOSE, 10)
    sma_20 = sma(CLOSE, 20)
    
    print(f"SMA(5):  {sma_5[-1]}")
    print(f"SMA(10): {sma_10[-1]}")
    print(f"SMA(20): {sma_20[-1]}")
    
    # SMA 交叉判断
    if sma_5[-1] > sma_20[-1]:
        print("短期均线在长期均线之上 → 短期趋势向上")
    else:
        print("短期均线在长期均线之下 → 短期趋势向下")


def example_ema():
    """EMA 示例"""
    print_section("指数移动平均线 (EMA)")
    
    # 计算 12 日、26 日 EMA (MACD 常用参数)
    ema_12 = ema(CLOSE, 12)
    ema_26 = ema(CLOSE, 26)
    
    print(f"EMA(12): {ema_12[-1]}")
    print(f"EMA(26): {ema_26[-1]}")
    
    # EMA 比 SMA 更敏感
    sma_12 = sma(CLOSE, 12)
    print(f"\n对比 SMA(12): {sma_12[-1]}")
    print("EMA 对近期价格变化更敏感")


def example_wma():
    """WMA 示例"""
    print_section("加权移动平均线 (WMA)")
    
    wma_5 = wma(CLOSE, 5)
    sma_5 = sma(CLOSE, 5)
    
    print(f"WMA(5): {wma_5[-1]}")
    print(f"SMA(5): {sma_5[-1]}")
    
    print("\nWMA 给近期数据更大权重，更能反映最新趋势")


def example_rsi():
    """RSI 示例"""
    print_section("相对强弱指数 (RSI)")
    
    rsi_14 = rsi(CLOSE, 14)
    rsi_value = rsi_14[-1]
    
    print(f"RSI(14): {rsi_value}")
    
    # 超买超卖判断
    if is_overbought(rsi_value):
        print("⚠️ 超买区 (>70)，可能回调")
    elif is_oversold(rsi_value):
        print("⚠️ 超卖区 (<30)，可能反弹")
    else:
        print("✅ 正常区间 (30-70)")
    
    # 中线判断
    if rsi_value > 50:
        print("RSI > 50 → 偏多头")
    else:
        print("RSI < 50 → 偏空头")


def example_macd():
    """MACD 示例"""
    print_section("MACD 指标")
    
    macd_result = macd(CLOSE)
    last = macd_result[-1]
    
    if last is not None:
        print(f"MACD (DIF):    {last.macd}")
        print(f"Signal (DEA):  {last.signal}")
        print(f"Histogram:     {last.histogram}")
        
        # 信号判断
        if last.histogram > 0:
            print("✅ 柱状图为正 → 多头趋势")
            if last.macd > last.signal:
                print("   MACD 上穿 Signal → 多头确认")
        else:
            print("❌ 柱状图为负 → 空头趋势")
            if last.macd < last.signal:
                print("   MACD 下穿 Signal → 空头确认")


def example_bollinger():
    """布林带示例"""
    print_section("布林带 (Bollinger Bands)")
    
    bb = bollinger_bands(CLOSE)
    last = bb[-1]
    
    if last is not None:
        print(f"上轨: {last.upper}")
        print(f"中轨: {last.middle}")
        print(f"下轨: {last.lower}")
        print(f"带宽: {last.bandwidth}%")
        print(f"%B:   {last.percent_b}")
        
        current_price = CLOSE[-1]
        
        # 价格位置判断
        if last.percent_b > 1:
            print(f"当前价格 {current_price} 突破上轨 → 可能回调")
        elif last.percent_b < 0:
            print(f"当前价格 {current_price} 跌破下轨 → 可能反弹")
        elif last.percent_b > 0.5:
            print(f"当前价格在中轨上方 → 偏多头")
        else:
            print(f"当前价格在中轨下方 → 偏空头")


def example_kdj():
    """KDJ 示例"""
    print_section("KDJ 指标")
    
    kdj_result = kdj(HIGH, LOW, CLOSE)
    last = kdj_result[-1]
    
    if last is not None:
        print(f"K: {last['k']}")
        print(f"D: {last['d']}")
        print(f"J: {last['j']}")
        
        # KDJ 超买超卖判断
        if last['k'] > 80 and last['d'] > 80:
            print("⚠️ KDJ 超买区 (>80)")
        elif last['k'] < 20 and last['d'] < 20:
            print("⚠️ KDJ 超卖区 (<20)")
        
        # K-D 交叉判断
        if last['k'] > last['d']:
            print("K > D → 金叉信号")
        else:
            print("K < D → 死叉信号")


def example_stochastic():
    """随机指标示例"""
    print_section("随机指标 (Stochastic)")
    
    stoch = stochastic(HIGH, LOW, CLOSE)
    last = stoch[-1]
    
    if last is not None:
        print(f"%K: {last.k}")
        print(f"%D: {last.d}")
        
        # 超买超卖判断
        if last.k > 80:
            print("⚠️ %K 超买区 (>80)")
        elif last.k < 20:
            print("⚠️ %K 超卖区 (<20)")


def example_atr():
    """ATR 示例"""
    print_section("平均真实波幅 (ATR)")
    
    atr_14 = atr(HIGH, LOW, CLOSE)
    atr_value = atr_14[-1]
    
    if atr_value is not None:
        print(f"ATR(14): {atr_value}")
        
        # 波动性判断
        avg_price = sum(CLOSE[-14:]) / 14
        atr_pct = atr_value / avg_price * 100
        
        print(f"ATR 占均价比例: {atr_pct:.2f}%")
        
        if atr_pct > 3:
            print("高波动性")
        elif atr_pct < 1:
            print("低波动性")
        else:
            print("正常波动性")


def example_obv():
    """OBV 示例"""
    print_section("能量潮指标 (OBV)")
    
    obv_result = obv(CLOSE, VOLUME)
    
    print(f"OBV 最新值: {obv_result[-1]}")
    
    # OBV 趋势判断
    if obv_result[-1] > obv_result[-5]:
        print("OBV 上升 → 资金流入")
    else:
        print("OBV 下降 → 资金流出")


def example_vwap():
    """VWAP 示例"""
    print_section("成交量加权平均价 (VWAP)")
    
    vwap_result = vwap(HIGH, LOW, CLOSE, VOLUME)
    
    print(f"VWAP: {vwap_result[-1]}")
    print(f"当前价格: {CLOSE[-1]}")
    
    if CLOSE[-1] > vwap_result[-1]:
        print("价格高于 VWAP → 偏多头")
    else:
        print("价格低于 VWAP → 偏空头")


def example_williams_r():
    """Williams %R 示例"""
    print_section("威廉指标 (Williams %R)")
    
    wr = williams_r(HIGH, LOW, CLOSE)
    wr_value = wr[-1]
    
    if wr_value is not None:
        print(f"Williams %R: {wr_value}")
        
        # Williams %R 范围 -100 到 0
        if wr_value > -20:
            print("⚠️ 超买区 (> -20)")
        elif wr_value < -80:
            print("⚠️ 超卖区 (< -80)")
        else:
            print("✅ 正常区间 (-80 到 -20)")


def example_cci():
    """CCI 示例"""
    print_section("顺势指标 (CCI)")
    
    cci_20 = cci(HIGH, LOW, CLOSE)
    cci_value = cci_20[-1]
    
    if cci_value is not None:
        print(f"CCI(20): {cci_value}")
        
        if cci_value > 100:
            print("⚠️ 超买区 (>100)")
        elif cci_value < -100:
            print("⚠️ 超卖区 (<-100)")
        else:
            print("✅ 正常区间 (-100 到 100)")


def example_momentum():
    """动量指标示例"""
    print_section("动量指标 (Momentum)")
    
    mom_10 = momentum(CLOSE)
    mom_value = mom_10[-1]
    
    if mom_value is not None:
        print(f"Momentum(10): {mom_value}")
        
        if mom_value > 0:
            print(f"上涨动量: {mom_value}")
        else:
            print(f"下跌动量: {mom_value}")


def example_roc():
    """ROC 示例"""
    print_section("变动率指标 (ROC)")
    
    roc_10 = roc(CLOSE)
    roc_value = roc_10[-1]
    
    if roc_value is not None:
        print(f"ROC(10): {roc_value}%")
        
        if roc_value > 5:
            print("强势上涨")
        elif roc_value < -5:
            print("强势下跌")
        else:
            print("小幅波动")


def example_adx():
    """ADX 示例"""
    print_section("平均趋向指数 (ADX)")
    
    adx_result = adx(HIGH, LOW, CLOSE)
    last = adx_result[-1]
    
    if last is not None:
        print(f"ADX:     {last['adx']}")
        print(f"+DI:     {last['plus_di']}")
        print(f"-DI:     {last['minus_di']}")
        
        # ADX 趋势强度
        if last['adx'] > 25:
            print("趋势强劲")
        elif last['adx'] > 20:
            print("趋势温和")
        else:
            print("无明显趋势")
        
        # +DI vs -DI
        if last['plus_di'] > last['minus_di']:
            print("+DI > -DI → 偏多头")
        else:
            print("-DI > +DI → 偏空头")


def example_trend_detection():
    """趋势检测示例"""
    print_section("趋势检测")
    
    trend = detect_trend(CLOSE, period=20)
    
    print(f"检测到趋势: {trend.value}")
    
    if trend == Trend.UP:
        print("📈 上升趋势")
        print("建议: 考虑逢低买入")
    elif trend == Trend.DOWN:
        print("📉 下降趋势")
        print("建议: 考虑逢高卖出或观望")
    else:
        print("➡️ 横盘整理")
        print("建议: 等待突破信号")


def example_support_resistance():
    """支撑阻力位示例"""
    print_section("支撑阻力位")
    
    sr = find_support_resistance(HIGH, LOW, CLOSE)
    
    print("支撑位:", sr.support_levels)
    print("阻力位:", sr.resistance_levels)
    
    current_price = CLOSE[-1]
    
    if sr.support_levels:
        nearest_support = sr.support_levels[-1]
        print(f"\n最近支撑位: {nearest_support}")
        print(f"距离支撑: {(current_price - nearest_support) / current_price * 100:.2f}%")
    
    if sr.resistance_levels:
        nearest_resistance = sr.resistance_levels[-1]
        print(f"最近阻力位: {nearest_resistance}")
        print(f"距离阻力: {(nearest_resistance - current_price) / current_price * 100:.2f}%")


def example_golden_death_cross():
    """金叉死叉示例"""
    print_section("金叉死叉检测")
    
    short_ma = sma(CLOSE, 5)
    long_ma = sma(CLOSE, 20)
    
    crosses = golden_cross_death_cross(short_ma, long_ma)
    
    # 找最近的交叉
    recent_crosses = [(i, c) for i, c in enumerate(crosses[-10:]) if c]
    
    if recent_crosses:
        for i, cross in recent_crosses:
            day = len(CLOSE) - 10 + i
            if cross == 'golden':
                print(f"🟢 第 {day} 天出现金叉 (买入信号)")
            elif cross == 'death':
                print(f"🔴 第 {day} 天出现死叉 (卖出信号)")
    else:
        print("最近 10 天无交叉信号")
    
    # 当前状态
    if short_ma[-1] > long_ma[-1]:
        print("\n当前状态: 短期均线在上 → 多头排列")
    else:
        print("\n当前状态: 短期均线在下 → 空头排列")


def example_risk_metrics():
    """风险指标示例"""
    print_section("风险指标")
    
    # 波动率
    volatility = calculate_volatility(CLOSE)
    print(f"年化波动率: {volatility}%")
    
    # 最大回撤
    max_dd = max_drawdown(CLOSE)
    print(f"最大回撤: {max_dd}%")
    
    # 夏普比率
    sharpe = sharpe_ratio(CLOSE, risk_free_rate=0.02)
    print(f"夏普比率: {sharpe}")
    
    # 风险评估
    if volatility and volatility > 30:
        print("⚠️ 高波动性，风险较大")
    elif volatility and volatility < 15:
        print("✅ 低波动性，相对稳定")
    
    if max_dd > 20:
        print("⚠️ 最大回撤超过 20%，需关注风险控制")


def example_comprehensive_analysis():
    """综合分析示例"""
    print_section("综合分析")
    
    analysis = analyze(
        CLOSE,
        high=HIGH,
        low=LOW,
        volume=VOLUME
    )
    
    print(f"当前价格: {analysis['current_price']}")
    print(f"趋势方向: {analysis['trend']}")
    
    print("\n--- 移动平均线 ---")
    print(f"SMA(5):  {analysis['sma']['sma_5']}")
    print(f"SMA(10): {analysis['sma']['sma_10']}")
    print(f"SMA(20): {analysis['sma']['sma_20']}")
    
    print("\n--- EMA ---")
    print(f"EMA(12): {analysis['ema']['ema_12']}")
    print(f"EMA(26): {analysis['ema']['ema_26']}")
    
    print("\n--- RSI ---")
    print(f"RSI(14): {analysis['rsi_14']}")
    
    if analysis['macd']:
        print("\n--- MACD ---")
        print(f"MACD:    {analysis['macd']['macd']}")
        print(f"Signal:  {analysis['macd']['signal']}")
        print(f"柱状图:  {analysis['macd']['histogram']}")
    
    if analysis['bollinger']:
        print("\n--- 布林带 ---")
        print(f"上轨: {analysis['bollinger']['upper']}")
        print(f"中轨: {analysis['bollinger']['middle']}")
        print(f"下轨: {analysis['bollinger']['lower']}")
    
    if analysis['kdj']:
        print("\n--- KDJ ---")
        print(f"K: {analysis['kdj']['k']}")
        print(f"D: {analysis['kdj']['d']}")
        print(f"J: {analysis['kdj']['j']}")
    
    print("\n--- 动量指标 ---")
    print(f"Momentum: {analysis['momentum']}")
    print(f"ROC:      {analysis['roc']}%")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("  技术分析工具使用示例")
    print("=" * 50)
    
    example_sma()
    example_ema()
    example_wma()
    example_rsi()
    example_macd()
    example_bollinger()
    example_kdj()
    example_stochastic()
    example_atr()
    example_obv()
    example_vwap()
    example_williams_r()
    example_cci()
    example_momentum()
    example_roc()
    example_adx()
    example_trend_detection()
    example_support_resistance()
    example_golden_death_cross()
    example_risk_metrics()
    example_comprehensive_analysis()
    
    print("\n" + "=" * 50)
    print("  示例演示完成")
    print("=" * 50)


if __name__ == "__main__":
    main()