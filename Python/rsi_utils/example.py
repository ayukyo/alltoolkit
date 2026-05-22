"""
RSI Utils 使用示例

展示 RSI (Relative Strength Index) 指标的各种用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rsi_utils.mod import (
    calculate_rsi,
    calculate_rsi_single,
    RSICalculator,
    detect_divergence,
    generate_signals,
    calculate_stoch_rsi,
    rsi_to_string,
    validate_rsi,
    get_rsi_zone
)


def example_basic_rsi():
    """基础 RSI 计算示例"""
    print("\n" + "=" * 50)
    print("示例 1: 基础 RSI 计算")
    print("=" * 50)
    
    # 模拟价格数据
    prices = [
        44.0, 44.5, 43.5, 44.5, 45.0, 46.0, 45.5, 46.0, 47.0, 46.5,
        47.0, 47.5, 48.0, 48.5, 47.5, 48.0, 49.0, 48.5, 49.0, 50.0,
        49.5, 50.5, 51.0, 50.5, 51.5, 52.0, 51.5, 52.5, 53.0, 52.5
    ]
    
    # 计算 14 周期 RSI
    rsi_values = calculate_rsi(prices, period=14)
    
    print(f"\n价格数量: {len(prices)}")
    print(f"RSI 周期: 14")
    print(f"\n最近 5 天价格和 RSI:")
    
    for i in range(-5, 0):
        price = prices[i]
        rsi = rsi_values[i]
        zone = get_rsi_zone(rsi)
        rsi_str = f"{rsi:.1f}" if rsi else "N/A"
        print(f"  价格: {price:6.2f}  RSI: {rsi_str:>5}  区域: {zone}")
    
    # 获取最新 RSI
    latest_rsi = calculate_rsi_single(prices, period=14)
    print(f"\n最新 RSI: {rsi_to_string(latest_rsi)}")


def example_different_methods():
    """不同平滑方法对比"""
    print("\n" + "=" * 50)
    print("示例 2: 不同平滑方法对比")
    print("=" * 50)
    
    prices = [100 + (i % 10 - 5) * 2 for i in range(30)]
    
    rsi_sma = calculate_rsi(prices, period=14, method='sma')
    rsi_ema = calculate_rsi(prices, period=14, method='ema')
    rsi_wilder = calculate_rsi(prices, period=14, method='wilder')
    
    print(f"\n价格序列最后 5 个: {prices[-5:]}")
    print(f"\n三种方法的 RSI 值:")
    print(f"  SMA 方法:    {rsi_sma[-1]:.2f}")
    print(f"  EMA 方法:    {rsi_ema[-1]:.2f}")
    print(f"  Wilder 方法: {rsi_wilder[-1]:.2f}")
    print(f"\n注: Wilder 方法是标准 RSI 计算方法")


def example_realtime_calculator():
    """实时 RSI 计算器示例"""
    print("\n" + "=" * 50)
    print("示例 3: 实时 RSI 计算器")
    print("=" * 50)
    
    # 创建计算器
    calc = RSICalculator(period=14, method='wilder')
    
    # 模拟实时价格更新
    prices = [100.0]
    print("\n模拟实时价格更新 (14 周期 RSI):")
    print("-" * 40)
    
    import random
    random.seed(42)
    
    for i in range(20):
        # 随机价格变动
        change = random.uniform(-2, 2)
        new_price = round(prices[-1] + change, 2)
        prices.append(new_price)
        
        # 更新 RSI
        rsi = calc.update(new_price)
        
        if rsi is not None:
            zone = get_rsi_zone(rsi)
            print(f"  价格: {new_price:7.2f}  →  RSI: {rsi:5.1f}  ({zone})")
        else:
            print(f"  价格: {new_price:7.2f}  →  RSI: 计算中... (需要更多数据)")
    
    print(f"\n最终 RSI: {rsi_to_string(calc.current_rsi)}")


def example_signals():
    """交易信号示例"""
    print("\n" + "=" * 50)
    print("示例 4: RSI 交易信号")
    print("=" * 50)
    
    # 模拟价格序列（包含超买超卖）
    prices = []
    base = 100
    
    # 先下跌进入超卖
    for i in range(10):
        prices.append(base - i * 3)
    
    # 反弹
    for i in range(10):
        prices.append(prices[-1] + 4)
    
    # 继续上涨进入超买
    for i in range(10):
        prices.append(prices[-1] + 3)
    
    # 回落
    for i in range(10):
        prices.append(prices[-1] - 3)
    
    rsi_values = calculate_rsi(prices, period=14)
    signals = generate_signals(rsi_values, oversold=30, overbought=70)
    
    print(f"\n价格范围: {min(prices):.2f} - {max(prices):.2f}")
    print(f"\n检测到的信号 ({len(signals)} 个):")
    
    for signal in signals:
        idx = signal['index']
        price = prices[idx] if idx < len(prices) else 'N/A'
        print(f"  [{signal['type']}] 价格: {price}, RSI: {signal['rsi']:.1f}")
        print(f"    → {signal['message']}")


def example_divergence():
    """背离检测示例"""
    print("\n" + "=" * 50)
    print("示例 5: RSI 背离检测")
    print("=" * 50)
    
    # 构造看涨背离场景
    prices = [
        100, 95, 90, 85, 80,  # 下跌
        82, 85, 88,  # 小反弹
        78, 75, 72,  # 再次下跌（价格新低）
        76, 80, 85, 90,  # 反转上涨
    ]
    
    rsi_values = calculate_rsi(prices, period=5)
    divergences = detect_divergence(prices, rsi_values, lookback=5)
    
    print(f"\n价格序列: {prices}")
    print(f"\n检测到的背离 ({len(divergences)} 个):")
    
    for div in divergences:
        print(f"  类型: {div['type']}")
        print(f"  位置: 价格={div['price']}, RSI={div['rsi']:.1f}")
        print(f"  说明: {div['message']}")


def example_stoch_rsi():
    """Stochastic RSI 示例"""
    print("\n" + "=" * 50)
    print("示例 6: Stochastic RSI")
    print("=" * 50)
    
    prices = [100 + (i % 7 - 3) * 2 + (i // 10) for i in range(50)]
    
    k_values, d_values = calculate_stoch_rsi(prices, rsi_period=14, stoch_period=14)
    
    print(f"\n价格数量: {len(prices)}")
    print(f"\n最近的 K 和 D 值:")
    
    for i in range(-5, 0):
        k = k_values[i]
        d = d_values[i]
        if k is not None and d is not None:
            print(f"  K: {k:5.1f}  D: {d:5.1f}")
        else:
            print(f"  K: N/A    D: N/A")


def example_zones():
    """RSI 区域判断示例"""
    print("\n" + "=" * 50)
    print("示例 7: RSI 区域判断")
    print("=" * 50)
    
    test_values = [10, 25, 35, 50, 65, 75, 90]
    
    print("\nRSI 值对应的区域:")
    print("-" * 40)
    
    for rsi in test_values:
        zone = get_rsi_zone(rsi)
        description = {
            'deep_oversold': '深度超卖 - 强买入信号',
            'oversold': '超卖区 - 可能买入机会',
            'bearish': '偏弱区 - 下跌趋势',
            'neutral': '中性区 - 无明显趋势',
            'bullish': '偏强区 - 上涨趋势',
            'overbought': '超买区 - 可能卖出机会',
            'deep_overbought': '深度超买 - 强卖出信号',
        }
        print(f"  RSI {rsi:3d} → {zone:15s} ({description[zone]})")


def example_validation():
    """RSI 验证示例"""
    print("\n" + "=" * 50)
    print("示例 8: RSI 值验证")
    print("=" * 50)
    
    test_cases = [
        (50, "正常值"),
        (0, "边界值(下限)"),
        (100, "边界值(上限)"),
        (-5, "无效值(负数)"),
        (105, "无效值(超上限)"),
        ("50", "无效值(字符串)"),
    ]
    
    print("\n验证结果:")
    for value, desc in test_cases:
        is_valid = validate_rsi(value)
        status = "✓ 有效" if is_valid else "✗ 无效"
        print(f"  {str(value):6s} ({desc:15s}) → {status}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("        RSI Utils 使用示例")
    print("        (Relative Strength Index 工具)")
    print("=" * 60)
    
    example_basic_rsi()
    example_different_methods()
    example_realtime_calculator()
    example_signals()
    example_divergence()
    example_stoch_rsi()
    example_zones()
    example_validation()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()