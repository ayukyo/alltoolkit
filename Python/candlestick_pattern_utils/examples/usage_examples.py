"""
Candlestick Pattern Recognition Utilities - 使用示例

本示例演示如何使用蜡烛图形态识别工具:
- 基本蜡烛创建和分析
- 单根形态识别
- 双根/三根形态识别
- 综合形态扫描
- 反转信号检测
- 实战应用场景
"""

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Candle, PatternType, SignalType,
    is_doji, is_hammer, is_shooting_star,
    is_bullish_engulfing, is_bearish_engulfing,
    is_morning_star, is_evening_star,
    is_three_white_soldiers, is_three_black_crows,
    identify_patterns, scan_all_patterns,
    get_reversal_signals, pattern_summary,
    candles_from_data, create_candle,
    analyze_trend_context, identify_single_candle_pattern,
)


def example_1_basic_candle():
    """示例1: 基本蜡烛创建和属性"""
    print("=" * 60)
    print("示例1: 基本蜡烛创建和属性")
    print("=" * 60)
    
    # 创建蜡烛
    candle = create_candle(open=100, high=105, low=95, close=103)
    
    print(f"\n蜡烛数据:")
    print(f"  开盘: {candle.open}")
    print(f"  最高: {candle.high}")
    print(f"  最低: {candle.low}")
    print(f"  收盘: {candle.close}")
    
    print(f"\n蜡烛属性:")
    print(f"  类型: {'阳线' if candle.is_bullish else '阴线'}")
    print(f"  实体大小: {candle.body}")
    print(f"  上影线: {candle.upper_shadow}")
    print(f"  下影线: {candle.lower_shadow}")
    print(f"  总范围: {candle.range}")
    print(f"  实体占比: {candle.body_ratio():.2%}")
    print(f"  是否十字星形态: {candle.is_doji_like}")


def example_2_single_patterns():
    """示例2: 单根蜡烛形态识别"""
    print("\n" + "=" * 60)
    print("示例2: 单根蜡烛形态识别")
    print("=" * 60)
    
    # 十字星
    doji = create_candle(100, 105, 95, 100.1)
    print(f"\n十字星示例:")
    print(f"  是否十字星: {is_doji(doji)}")
    patterns = identify_single_candle_pattern(doji)
    for p in patterns:
        print(f"  检测到: {p.pattern_type.value} - {p.description}")
    
    # 锤子线
    hammer = create_candle(100, 102, 85, 101)
    print(f"\n锤子线示例:")
    print(f"  是否锤子线: {is_hammer(hammer)}")
    patterns = identify_single_candle_pattern(hammer)
    for p in patterns:
        print(f"  检测到: {p.pattern_type.value} - {p.description}")
    
    # 流星线
    shooting_star = create_candle(100, 115, 99, 101)
    print(f"\n流星线示例:")
    print(f"  是否流星线: {is_shooting_star(shooting_star)}")
    patterns = identify_single_candle_pattern(shooting_star)
    for p in patterns:
        print(f"  检测到: {p.pattern_type.value} - {p.description}")
    
    # 光头光脚蜡烛
    marubozu = create_candle(100, 110, 100, 110)
    print(f"\n光头光脚蜡烛示例:")
    patterns = identify_single_candle_pattern(marubozu)
    for p in patterns:
        print(f"  检测到: {p.pattern_type.value} - {p.description}")


def example_3_double_patterns():
    """示例3: 双根蜡烛形态识别"""
    print("\n" + "=" * 60)
    print("示例3: 双根蜡烛形态识别")
    print("=" * 60)
    
    # 看涨吞没
    bullish_engulfing_data = [
        {'open': 105, 'high': 106, 'low': 95, 'close': 96},  # 阴线
        {'open': 94, 'high': 105, 'low': 93, 'close': 104},  # 大阳线吞没
    ]
    candles = candles_from_data(bullish_engulfing_data)
    
    print(f"\n看涨吞没示例:")
    for i, c in enumerate(candles):
        print(f"  蜡烛{i}: O:{c.open} H:{c.high} L:{c.low} C:{c.close}")
    
    result = is_bullish_engulfing(candles, 1)
    if result:
        print(f"  检测到: {result.pattern_type.value}")
        print(f"  信号类型: {result.signal_type.value}")
        print(f"  强度: {result.strength:.2f}")
        print(f"  描述: {result.description}")
    
    # 看跌吞没
    bearish_engulfing_data = [
        {'open': 96, 'high': 105, 'low': 95, 'close': 104},  # 阳线
        {'open': 105, 'high': 106, 'low': 93, 'close': 94},  # 大阴线吞没
    ]
    candles = candles_from_data(bearish_engulfing_data)
    
    print(f"\n看跌吞没示例:")
    result = is_bearish_engulfing(candles, 1)
    if result:
        print(f"  检测到: {result.pattern_type.value}")
        print(f"  信号类型: {result.signal_type.value}")
        print(f"  描述: {result.description}")


def example_4_triple_patterns():
    """示例4: 三根蜡烛形态识别"""
    print("\n" + "=" * 60)
    print("示例4: 三根蜡烛形态识别")
    print("=" * 60)
    
    # 启明星
    morning_star_data = [
        {'open': 105, 'high': 106, 'low': 94, 'close': 95},   # 大阴线
        {'open': 94, 'high': 95, 'low': 93.5, 'close': 94.2}, # 小实体(星)
        {'open': 94, 'high': 103, 'low': 93, 'close': 102},   # 大阳线
    ]
    candles = candles_from_data(morning_star_data)
    
    print(f"\n启明星示例:")
    for i, c in enumerate(candles):
        print(f"  蜡烛{i}: O:{c.open} H:{c.high} L:{c.low} C:{c.close} "
              f"{'阳' if c.is_bullish else '阴'}线")
    
    result = is_morning_star(candles, 2)
    if result:
        print(f"  检测到: {result.pattern_type.value}")
        print(f"  信号: {result.signal_type.value}")
        print(f"  强度: {result.strength:.2f}")
    
    # 黄昏星
    evening_star_data = [
        {'open': 95, 'high': 105, 'low': 94, 'close': 104},   # 大阳线
        {'open': 104, 'high': 105, 'low': 103, 'close': 104.1}, # 小实体(星)
        {'open': 104, 'high': 105, 'low': 93, 'close': 94},   # 大阴线
    ]
    candles = candles_from_data(evening_star_data)
    
    print(f"\n黄昏星示例:")
    result = is_evening_star(candles, 2)
    if result:
        print(f"  检测到: {result.pattern_type.value}")
        print(f"  信号: {result.signal_type.value}")
    
    # 三白兵
    three_white_soldiers_data = [
        {'open': 95, 'high': 102, 'low': 94, 'close': 101},
        {'open': 100, 'high': 108, 'low': 99, 'close': 107},
        {'open': 106, 'high': 112, 'low': 105, 'close': 111},
    ]
    candles = candles_from_data(three_white_soldiers_data)
    
    print(f"\n三白兵示例:")
    result = is_three_white_soldiers(candles, 2)
    if result:
        print(f"  检测到: {result.pattern_type.value}")
        print(f"  强度: {result.strength:.2f}")
        print(f"  置信度: {result.confidence:.2f}")
    
    # 三黑鸦
    three_black_crows_data = [
        {'open': 111, 'high': 112, 'low': 105, 'close': 106},
        {'open': 107, 'high': 108, 'low': 99, 'close': 100},
        {'open': 101, 'high': 102, 'low': 94, 'close': 95},
    ]
    candles = candles_from_data(three_black_crows_data)
    
    print(f"\n三黑鸦示例:")
    result = is_three_black_crows(candles, 2)
    if result:
        print(f"  检测到: {result.pattern_type.value}")


def example_5_comprehensive_scan():
    """示例5: 综合形态扫描"""
    print("\n" + "=" * 60)
    print("示例5: 综合形态扫描")
    print("=" * 60)
    
    # 创建一段完整的蜡烛数据
    price_data = [
        {'open': 100, 'high': 105, 'low': 99, 'close': 103},   # 0
        {'open': 103, 'high': 108, 'low': 102, 'close': 107},  # 1
        {'open': 107, 'high': 112, 'low': 106, 'close': 110},  # 2 上升趋势
        {'open': 110, 'high': 111, 'low': 108, 'close': 109},  # 3
        {'open': 109, 'high': 110, 'low': 100, 'close': 101},  # 4 大阴线
        {'open': 101, 'high': 102, 'low': 100.5, 'close': 101.2}, # 5 小实体
        {'open': 100, 'high': 108, 'low': 99, 'close': 107},   # 6 大阳线(启明星完成)
        {'open': 107, 'high': 110, 'low': 106, 'close': 109},  # 7
        {'open': 109, 'high': 112, 'low': 108, 'close': 111},  # 8
        {'open': 111, 'high': 113, 'low': 110, 'close': 112},  # 9
    ]
    
    candles = candles_from_data(price_data)
    
    print(f"\n扫描所有蜡烛形态:")
    all_patterns = scan_all_patterns(candles)
    
    for idx, patterns in all_patterns.items():
        print(f"\n蜡烛[{idx}]:")
        for p in patterns[:2]:  # 只显示前两个最强的
            signal_icon = "📈" if p.signal_type.value.startswith("bullish") else "📉"
            print(f"  {signal_icon} {p.pattern_type.value}: {p.description}")
    
    # 分析最后一根蜡烛
    print(f"\n最后一根蜡烛形态分析:")
    patterns = identify_patterns(candles, -1)
    print(pattern_summary(patterns))


def example_6_reversal_signals():
    """示例6: 反转信号检测"""
    print("\n" + "=" * 60)
    print("示例6: 反转信号检测")
    print("=" * 60)
    
    # 模拟一段下跌后反转的数据
    downtrend_data = [
        {'open': 120, 'high': 122, 'low': 108, 'close': 110},
        {'open': 110, 'high': 112, 'low': 98, 'close': 100},
        {'open': 100, 'high': 102, 'low': 88, 'close': 90},
        {'open': 90, 'high': 92, 'low': 85, 'close': 86},   # 下跌结束
        {'open': 86, 'high': 87, 'low': 85.5, 'close': 86.2}, # 小实体(十字星)
        {'open': 85, 'high': 95, 'low': 84, 'close': 93},   # 反转阳线
        {'open': 93, 'high': 100, 'low': 92, 'close': 98},  # 确认阳线
    ]
    
    candles = candles_from_data(downtrend_data)
    
    print(f"\n检测反转信号:")
    signals = get_reversal_signals(candles, -1)
    
    print(f"\n看涨反转信号 ({len(signals['bullish'])} 个):")
    for p in signals['bullish']:
        print(f"  📈 {p.pattern_type.value}: 强度={p.strength:.2f}")
    
    print(f"\n看跌反转信号 ({len(signals['bearish'])} 个):")
    for p in signals['bearish']:
        print(f"  📉 {p.pattern_type.value}: 强度={p.strength:.2f}")
    
    # 趋势背景分析
    trend = analyze_trend_context(candles, 4, 5)
    print(f"\n趋势背景: {trend}")
    
    trend = analyze_trend_context(candles, -1, 5)
    print(f"最新趋势: {trend}")


def example_7_trading_simulation():
    """示例7: 实战应用场景"""
    print("\n" + "=" * 60)
    print("示例7: 实战应用场景")
    print("=" * 60)
    
    # 模拟真实交易数据
    trading_data = [
        # Day 1-3: 上涨
        {'open': 50, 'high': 52, 'low': 49, 'close': 51},
        {'open': 51, 'high': 54, 'low': 50.5, 'close': 53},
        {'open': 53, 'high': 56, 'low': 52, 'close': 55},
        # Day 4: 顶部十字星
        {'open': 55, 'high': 56, 'low': 54, 'close': 55.1},
        # Day 5-6: 下跌
        {'open': 55, 'high': 55.5, 'low': 50, 'close': 51},
        {'open': 51, 'high': 52, 'low': 48, 'close': 49},
        # Day 7: 底部锤子线
        {'open': 49, 'high': 50, 'low': 45, 'close': 49.5},
        # Day 8: 看涨吞没
        {'open': 48, 'high': 53, 'low': 47, 'close': 52},
        # Day 9-10: 反弹确认
        {'open': 52, 'high': 55, 'low': 51, 'close': 54},
        {'open': 54, 'high': 57, 'low': 53, 'close': 56},
    ]
    
    candles = candles_from_data(trading_data)
    
    print("\n模拟交易分析:")
    
    # 逐日分析
    for i in range(len(candles)):
        patterns = identify_patterns(candles, i)
        if patterns:
            candle = candles[i]
            price_change = ((candle.close - candles[0].open) / candles[0].open) * 100
            
            for p in patterns[:1]:  # 只显示最强的
                if p.strength >= 0.5:  # 只显示有意义强度的形态
                    signal_icon = {
                        'bullish_reversal': '📈🔄',
                        'bearish_reversal': '📉🔄',
                        'bullish_continuation': '📈➡️',
                        'bearish_continuation': '📉➡️',
                        'neutral': '⚖️',
                    }.get(p.signal_type.value, '?')
                    
                    print(f"Day {i+1}: 价格={candle.close:.1f} (+{price_change:.1f}%)")
                    print(f"  {signal_icon} {p.description}")
                    print(f"  建议: {'注意' if p.strength < 0.7 else '关注'}")


def example_8_pattern_filtering():
    """示例8: 按信号类型过滤形态"""
    print("\n" + "=" * 60)
    print("示例8: 按信号类型过滤形态")
    print("=" * 60)
    
    price_data = [
        {'open': 100, 'high': 105, 'low': 99, 'close': 103},
        {'open': 103, 'high': 108, 'low': 102, 'close': 107},
        {'open': 107, 'high': 110, 'low': 105, 'close': 106},
        {'open': 106, 'high': 107, 'low': 98, 'close': 99},
        {'open': 98, 'high': 99, 'low': 97.5, 'close': 98.2},
        {'open': 97, 'high': 105, 'low': 96, 'close': 104},
    ]
    
    candles = candles_from_data(price_data)
    patterns = identify_patterns(candles, -1)
    
    # 按信号类型分类
    reversal_patterns = [p for p in patterns 
                         if 'reversal' in p.signal_type.value]
    continuation_patterns = [p for p in patterns 
                             if 'continuation' in p.signal_type.value]
    
    print(f"\n反转形态 ({len(reversal_patterns)} 个):")
    for p in reversal_patterns:
        print(f"  {p.pattern_type.value}: {p.strength:.2f}")
    
    print(f"\n延续形态 ({len(continuation_patterns)} 个):")
    for p in continuation_patterns:
        print(f"  {p.pattern_type.value}: {p.strength:.2f}")
    
    # 按强度过滤
    strong_patterns = [p for p in patterns if p.strength >= 0.7]
    print(f"\n高强度形态 ({len(strong_patterns)} 个):")
    for p in strong_patterns:
        print(f"  {p.pattern_type.value}: 强度={p.strength:.2f}, 置信度={p.confidence:.2f}")


if __name__ == "__main__":
    example_1_basic_candle()
    example_2_single_patterns()
    example_3_double_patterns()
    example_4_triple_patterns()
    example_5_comprehensive_scan()
    example_6_reversal_signals()
    example_7_trading_simulation()
    example_8_pattern_filtering()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60)