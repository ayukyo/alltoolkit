"""
Moving Average Utils 使用示例

展示各种移动平均算法的实际应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    simple_moving_average,
    exponential_moving_average,
    weighted_moving_average,
    cumulative_moving_average,
    triangular_moving_average,
    hull_moving_average,
    kaufman_adaptive_moving_average,
    volume_weighted_moving_average,
    moving_average_convergence_divergence,
    average_true_range,
    bollinger_bands,
    rolling_statistics,
    MovingAverage,
)


def example_stock_analysis():
    """股票分析示例"""
    print("=" * 60)
    print("股票技术分析示例")
    print("=" * 60)
    
    # 模拟股价数据（收盘价）
    prices = [
        100.0, 102.5, 101.8, 104.2, 103.5,
        105.0, 106.8, 105.5, 107.2, 108.5,
        109.0, 107.8, 110.2, 111.5, 112.0,
        110.5, 111.8, 113.2, 112.5, 115.0,
        114.5, 116.2, 115.8, 117.5, 118.0
    ]
    
    print(f"\n股价数据（最近{len(prices)}天）:")
    print(f"  开盘: ¥{prices[0]:.2f}")
    print(f"  最新: ¥{prices[-1]:.2f}")
    print(f"  涨幅: {((prices[-1] - prices[0]) / prices[0] * 100):.2f}%")
    
    # 计算各种移动平均
    print("\n📊 移动平均分析:")
    
    sma_5 = simple_moving_average(prices, 5)
    sma_10 = simple_moving_average(prices, 10)
    sma_20 = simple_moving_average(prices, 20)
    
    print(f"  SMA(5):  ¥{sma_5[-1]:.2f}")
    print(f"  SMA(10): ¥{sma_10[-1]:.2f}")
    print(f"  SMA(20): ¥{sma_20[-1]:.2f}")
    
    ema_12 = exponential_moving_average(prices, 12)
    ema_26 = exponential_moving_average(prices, 26)
    
    print(f"  EMA(12): ¥{ema_12[-1]:.2f}" if ema_12[-1] else "  EMA(12): 数据不足")
    print(f"  EMA(26): ¥{ema_26[-1]:.2f}" if ema_26[-1] else "  EMA(26): 数据不足")
    
    # 布林带
    print("\n📈 布林带分析:")
    upper, middle, lower = bollinger_bands(prices, 20, 2.0)
    if upper[-1]:
        print(f"  上轨: ¥{upper[-1]:.2f}")
        print(f"  中轨: ¥{middle[-1]:.2f}")
        print(f"  下轨: ¥{lower[-1]:.2f}")
        print(f"  带宽: ¥{upper[-1] - lower[-1]:.2f}")
        print(f"  当前价格位置: {((prices[-1] - lower[-1]) / (upper[-1] - lower[-1]) * 100):.1f}%")
    
    # MACD
    print("\n📉 MACD分析:")
    macd_line, signal_line, histogram = moving_average_convergence_divergence(
        prices, fast_period=12, slow_period=26, signal_period=9
    )
    
    if macd_line[-1] and signal_line[-1]:
        print(f"  MACD线: {macd_line[-1]:.4f}")
        print(f"  信号线: {signal_line[-1]:.4f}")
        print(f"  柱状图: {histogram[-1]:.4f}")
        
        if histogram[-1] > 0:
            print("  信号: 多头趋势 📈")
        else:
            print("  信号: 空头趋势 📉")


def example_temperature_monitoring():
    """温度监控示例"""
    print("\n" + "=" * 60)
    print("温度监控分析示例")
    print("=" * 60)
    
    # 24小时温度数据（每小时一个数据点）
    temperatures = [
        22.0, 21.5, 21.0, 20.5, 20.2, 20.0,
        20.5, 21.5, 23.0, 24.5, 26.0, 27.5,
        28.5, 29.0, 29.5, 29.2, 28.5, 27.0,
        25.5, 24.0, 23.5, 23.0, 22.5, 22.0
    ]
    
    print(f"\n24小时温度数据:")
    print(f"  最低: {min(temperatures):.1f}°C (凌晨)")
    print(f"  最高: {max(temperatures):.1f}°C (下午)")
    print(f"  平均: {sum(temperatures) / len(temperatures):.1f}°C")
    
    # 使用不同移动平均平滑数据
    print("\n🌡️ 平滑处理:")
    
    # 3小时移动平均
    sma_3 = simple_moving_average(temperatures, 3)
    print(f"  3小时SMA最新: {sma_3[-1]:.1f}°C")
    
    # 6小时移动平均
    sma_6 = simple_moving_average(temperatures, 6)
    print(f"  6小时SMA最新: {sma_6[-1]:.1f}°C")
    
    # EMA更快响应温度变化
    ema = exponential_moving_average(temperatures, 6)
    print(f"  6小时EMA最新: {ema[-1]:.1f}°C")
    
    # 滚动统计
    print("\n📊 滚动统计（6小时窗口）:")
    stats = rolling_statistics(temperatures, 6, ['mean', 'std', 'min', 'max'])
    
    if stats['mean'][-1]:
        print(f"  均值: {stats['mean'][-1]:.1f}°C")
        print(f"  标准差: {stats['std'][-1]:.2f}°C")
        print(f"  最小: {stats['min'][-1]:.1f}°C")
        print(f"  最大: {stats['max'][-1]:.1f}°C")


def example_signal_processing():
    """信号处理示例"""
    print("\n" + "=" * 60)
    print("信号处理示例")
    print("=" * 60)
    
    # 生成带噪声的正弦波信号
    import math
    import random
    
    signal_length = 100
    frequency = 0.1
    noise_level = 0.5
    
    # 原始信号 + 噪声
    noisy_signal = [
        math.sin(2 * math.pi * frequency * i) + noise_level * (random.random() - 0.5) * 2
        for i in range(signal_length)
    ]
    
    print(f"\n信号参数:")
    print(f"  采样点数: {signal_length}")
    print(f"  频率: {frequency}")
    print(f"  噪声级别: ±{noise_level}")
    
    # 使用不同的滤波方法
    print("\n🔧 滤波结果:")
    
    # SMA滤波
    sma = simple_moving_average(noisy_signal, 5)
    sma_valid = [x for x in sma if x is not None]
    print(f"  SMA(5)滤波后标准差: {(sum((x**2 for x in sma_valid)) / len(sma_valid)) ** 0.5:.4f}")
    
    # EMA滤波（更快响应）
    ema = exponential_moving_average(noisy_signal, 5)
    ema_valid = [x for x in ema if x is not None]
    print(f"  EMA(5)滤波后标准差: {(sum((x**2 for x in ema_valid)) / len(ema_valid)) ** 0.5:.4f}")
    
    # TMA滤波（更平滑）
    tma = triangular_moving_average(noisy_signal, 5)
    tma_valid = [x for x in tma if x is not None]
    print(f"  TMA(5)滤波后标准差: {(sum((x**2 for x in tma_valid)) / len(tma_valid)) ** 0.5:.4f}")


def example_streaming_data():
    """流式数据处理示例"""
    print("\n" + "=" * 60)
    print("流式数据处理示例")
    print("=" * 60)
    
    print("\n📊 实时数据流模拟:")
    
    # 创建移动平均计算器
    sma_calculator = MovingAverage(window=5, method='sma')
    ema_calculator = MovingAverage(window=5, method='ema')
    
    # 模拟数据流
    data_stream = [10, 12, 11, 13, 15, 14, 16, 18, 17, 19]
    
    print("\n数据点 |  SMA(5)  |  EMA(5)")
    print("-" * 35)
    
    for i, value in enumerate(data_stream):
        sma_val = sma_calculator.update(value)
        ema_val = ema_calculator.update(value)
        
        sma_str = f"{sma_val:.2f}" if sma_val else "--"
        ema_str = f"{ema_val:.2f}" if ema_val else "--"
        
        print(f"  {value:4d}   | {sma_str:>8} | {ema_str:>8}")
    
    print(f"\n当前状态:")
    print(f"  SMA: {sma_calculator.current:.2f}")
    print(f"  EMA: {ema_calculator.current:.2f}")


def example_vwap():
    """VWAP（成交量加权平均价格）示例"""
    print("\n" + "=" * 60)
    print("VWAP分析示例")
    print("=" * 60)
    
    # 模拟交易数据
    prices = [100.0, 100.5, 101.0, 100.8, 101.5, 102.0, 101.8, 102.5, 103.0, 102.8]
    volumes = [1000, 1500, 2000, 1200, 2500, 1800, 2200, 3000, 2500, 2000]
    
    print(f"\n交易数据:")
    print(f"  价格范围: ¥{min(prices):.2f} - ¥{max(prices):.2f}")
    print(f"  总成交量: {sum(volumes):,}")
    
    # 计算VWAP
    vwap = volume_weighted_moving_average(prices, volumes, 5)
    
    print(f"\n📊 5期VWAP:")
    print(f"  当前VWAP: ¥{vwap[-1]:.2f}" if vwap[-1] else "  数据不足")
    
    # 累积VWAP
    total_value = sum(p * v for p, v in zip(prices, volumes))
    total_volume = sum(volumes)
    cumulative_vwap = total_value / total_volume
    
    print(f"  累积VWAP: ¥{cumulative_vwap:.2f}")
    print(f"  当前价格 vs VWAP: {((prices[-1] - cumulative_vwap) / cumulative_vwap * 100):+.2f}%")


def example_volatility_analysis():
    """波动率分析示例"""
    print("\n" + "=" * 60)
    print("波动率分析示例")
    print("=" * 60)
    
    # 模拟OHLC数据
    highs = [105, 108, 107, 110, 112, 111, 114, 116, 115, 118]
    lows = [100, 103, 102, 105, 108, 106, 109, 111, 110, 113]
    closes = [103, 106, 105, 108, 110, 109, 112, 114, 113, 116]
    
    print(f"\nK线数据（10根）:")
    for i in range(len(closes)):
        print(f"  第{i+1}根: 高{highs[i]} 低{lows[i]} 收{closes[i]}")
    
    # 计算ATR
    atr = average_true_range(highs, lows, closes, 14)
    
    print(f"\n📈 ATR(14)分析:")
    if atr[-1]:
        print(f"  当前ATR: {atr[-1]:.2f}")
        print(f"  相对波动率: {(atr[-1] / closes[-1] * 100):.2f}%")
    
    # 使用KAMA检测趋势强度
    print(f"\n📊 KAMA趋势检测:")
    kama = kaufman_adaptive_moving_average(closes, 5)
    if kama[-1]:
        print(f"  当前KAMA: {kama[-1]:.2f}")
        print(f"  价格偏离: {((closes[-1] - kama[-1]) / kama[-1] * 100):+.2f}%")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Moving Average Utils 使用示例集")
    print("=" * 60)
    
    example_stock_analysis()
    example_temperature_monitoring()
    example_signal_processing()
    example_streaming_data()
    example_vwap()
    example_volatility_analysis()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()