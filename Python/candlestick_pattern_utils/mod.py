"""
Candlestick Pattern Recognition Utilities - 蜡烛图形态识别工具

功能:
- 单根蜡烛形态识别 (Doji, Hammer, Shooting Star 等)
- 双根蜡烛形态识别 (Engulfing, Harami, Tweezer 等)
- 三根蜡烛形态识别 (Morning Star, Evening Star, Three White Soldiers 等)
- 多根蜡烛形态识别 (Head and Shoulders, Double Top/Bottom 等)
- 形态强度评估
- 反转/延续信号判断

零外部依赖，纯 Python 实现。

作者: AllToolkit
日期: 2026-05-13
"""

from typing import List, Tuple, Optional, Dict, Any, NamedTuple
from enum import Enum
from dataclasses import dataclass
import math


# ============================================================================
# 基础数据结构
# ============================================================================

@dataclass
class Candle:
    """单根蜡烛数据"""
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    
    @property
    def body(self) -> float:
        """实体大小"""
        return abs(self.close - self.open)
    
    @property
    def body_top(self) -> float:
        """实体顶部"""
        return max(self.open, self.close)
    
    @property
    def body_bottom(self) -> float:
        """实体底部"""
        return min(self.open, self.close)
    
    @property
    def upper_shadow(self) -> float:
        """上影线"""
        return self.high - self.body_top
    
    @property
    def lower_shadow(self) -> float:
        """下影线"""
        return self.body_bottom - self.low
    
    @property
    def range(self) -> float:
        """总范围"""
        return self.high - self.low
    
    @property
    def is_bullish(self) -> bool:
        """是否为阳线"""
        return self.close > self.open
    
    @property
    def is_bearish(self) -> bool:
        """是否为阴线"""
        return self.close < self.open
    
    @property
    def is_doji_like(self) -> bool:
        """是否类似十字星"""
        if self.range == 0:
            return True
        return self.body / self.range < 0.1
    
    def body_ratio(self) -> float:
        """实体占比"""
        if self.range == 0:
            return 0.0
        return self.body / self.range
    
    def shadow_ratio(self) -> Tuple[float, float]:
        """影线占比 (上影线, 下影线)"""
        if self.range == 0:
            return (0.0, 0.0)
        return (self.upper_shadow / self.range, self.lower_shadow / self.range)


class PatternType(Enum):
    """形态类型"""
    # 单根形态
    DOJI = "doji"
    LONG_LEGGED_DOJI = "long_legged_doji"
    DRAGONFLY_DOJI = "dragonfly_doji"
    GRAVESTONE_DOJI = "gravestone_doji"
    HAMMER = "hammer"
    INVERTED_HAMMER = "inverted_hammer"
    HANGING_MAN = "hanging_man"
    SHOOTING_STAR = "shooting_star"
    MARUBOZU = "marubozu"
    SPINNING_TOP = "spinning_top"
    
    # 双根形态
    BULLISH_ENGULFING = "bullish_engulfing"
    BEARISH_ENGULFING = "bearish_engulfing"
    BULLISH_HARAMI = "bullish_harami"
    BEARISH_HARAMI = "bearish_harami"
    TWEEZER_TOP = "tweezer_top"
    TWEEZER_BOTTOM = "tweezer_bottom"
    PIERCING_LINE = "piercing_line"
    DARK_CLOUD_COVER = "dark_cloud_cover"
    
    # 三根形态
    MORNING_STAR = "morning_star"
    EVENING_STAR = "evening_star"
    THREE_WHITE_SOLDIERS = "three_white_soldiers"
    THREE_BLACK_CROWS = "three_black_crows"
    THREE_OUTSIDE_UP = "three_outside_up"
    THREE_OUTSIDE_DOWN = "three_outside_down"
    THREE_INSIDE_UP = "three_inside_up"
    THREE_INSIDE_DOWN = "three_inside_down"
    ABANDONED_BABY = "abandoned_baby"
    
    # 多根形态
    HEAD_AND_SHOULDERS = "head_and_shoulders"
    INVERSE_HEAD_AND_SHOULDERS = "inverse_head_and_shoulders"
    DOUBLE_TOP = "double_top"
    DOUBLE_BOTTOM = "double_bottom"
    TRIPLE_TOP = "triple_top"
    TRIPLE_BOTTOM = "triple_bottom"


class SignalType(Enum):
    """信号类型"""
    BULLISH_REVERSAL = "bullish_reversal"
    BEARISH_REVERSAL = "bearish_reversal"
    BULLISH_CONTINUATION = "bullish_continuation"
    BEARISH_CONTINUATION = "bearish_continuation"
    NEUTRAL = "neutral"


@dataclass
class PatternResult:
    """形态识别结果"""
    pattern_type: PatternType
    signal_type: SignalType
    strength: float  # 0.0 - 1.0
    candles: List[int]  # 涉及的蜡烛索引
    description: str
    confidence: float  # 识别置信度


# ============================================================================
# 单根蜡烛形态识别
# ============================================================================

def is_doji(candle: Candle, threshold: float = 0.05) -> bool:
    """
    十字星判断
    
    特征: 开盘价和收盘价几乎相同
    """
    if candle.range == 0:
        return True
    return candle.body_ratio() < threshold


def is_long_legged_doji(candle: Candle, threshold: float = 0.05, 
                        min_shadow_ratio: float = 0.3) -> bool:
    """
    长腿十字星判断
    
    特征: 实体很小，上下影线都很长且大致相等
    """
    if not is_doji(candle, threshold):
        return False
    
    upper_ratio, lower_ratio = candle.shadow_ratio()
    return upper_ratio >= min_shadow_ratio and lower_ratio >= min_shadow_ratio


def is_dragonfly_doji(candle: Candle, threshold: float = 0.05,
                      max_upper_shadow_ratio: float = 0.1) -> bool:
    """
    蜻蜓十字星判断
    
    特征: 实体很小，上影线极短或没有，下影线很长
    """
    if not is_doji(candle, threshold):
        return False
    
    upper_ratio, lower_ratio = candle.shadow_ratio()
    return upper_ratio <= max_upper_shadow_ratio and lower_ratio > 0.3


def is_gravestone_doji(candle: Candle, threshold: float = 0.05,
                       max_lower_shadow_ratio: float = 0.1) -> bool:
    """
    墓碑十字星判断
    
    特征: 实体很小，下影线极短或没有，上影线很长
    """
    if not is_doji(candle, threshold):
        return False
    
    upper_ratio, lower_ratio = candle.shadow_ratio()
    return lower_ratio <= max_lower_shadow_ratio and upper_ratio > 0.3


def is_hammer(candle: Candle, min_lower_shadow_ratio: float = 0.6,
              max_upper_shadow_ratio: float = 0.1,
              max_body_ratio: float = 0.35) -> bool:
    """
    锤子线判断
    
    特征: 下影线很长(至少是实体的2倍)，上影线很短或没有，实体在顶部
    
    出现下跌趋势中为看涨反转信号
    """
    if candle.range == 0:
        return False
    
    upper_ratio, lower_ratio = candle.shadow_ratio()
    body_ratio = candle.body_ratio()
    
    return (
        lower_ratio >= min_lower_shadow_ratio and
        upper_ratio <= max_upper_shadow_ratio and
        body_ratio <= max_body_ratio and
        candle.body_bottom > candle.low + candle.range * 0.3  # 实体在顶部
    )


def is_inverted_hammer(candle: Candle, min_upper_shadow_ratio: float = 0.6,
                       max_lower_shadow_ratio: float = 0.1,
                       max_body_ratio: float = 0.35) -> bool:
    """
    倒锤子线判断
    
    特征: 上影线很长，下影线很短或没有，实体在底部
    
    出现下跌趋势中为看涨反转信号
    """
    if candle.range == 0:
        return False
    
    upper_ratio, lower_ratio = candle.shadow_ratio()
    body_ratio = candle.body_ratio()
    
    return (
        upper_ratio >= min_upper_shadow_ratio and
        lower_ratio <= max_lower_shadow_ratio and
        body_ratio <= max_body_ratio and
        candle.body_top < candle.high - candle.range * 0.3  # 实体在底部
    )


def is_hanging_man(candle: Candle, min_lower_shadow_ratio: float = 0.6,
                   max_upper_shadow_ratio: float = 0.1,
                   max_body_ratio: float = 0.35) -> bool:
    """
    上吊线判断
    
    特征: 与锤子线形态相同，但出现在上升趋势中为看跌反转信号
    """
    return is_hammer(candle, min_lower_shadow_ratio, max_upper_shadow_ratio, max_body_ratio)


def is_shooting_star(candle: Candle, min_upper_shadow_ratio: float = 0.6,
                     max_lower_shadow_ratio: float = 0.1,
                     max_body_ratio: float = 0.35) -> bool:
    """
    流星线判断
    
    特征: 与倒锤子线形态相同，但出现在上升趋势中为看跌反转信号
    """
    return is_inverted_hammer(candle, min_upper_shadow_ratio, max_lower_shadow_ratio, max_body_ratio)


def is_marubozu(candle: Candle, max_shadow_ratio: float = 0.05) -> bool:
    """
    光头光脚蜡烛判断
    
    特征: 没有影线或影线极短，开盘价即最低价，收盘价即最高价(或反过来)
    """
    if candle.range == 0:
        return False
    
    upper_ratio, lower_ratio = candle.shadow_ratio()
    return upper_ratio <= max_shadow_ratio and lower_ratio <= max_shadow_ratio


def is_spinning_top(candle: Candle, max_body_ratio: float = 0.35,
                    min_shadow_ratio: float = 0.3) -> bool:
    """
    纺锤线判断
    
    特征: 实体很小，上下影线较长且大致相等
    """
    if candle.range == 0:
        return False
    
    upper_ratio, lower_ratio = candle.shadow_ratio()
    body_ratio = candle.body_ratio()
    
    return (
        body_ratio <= max_body_ratio and
        upper_ratio >= min_shadow_ratio and
        lower_ratio >= min_shadow_ratio
    )


# ============================================================================
# 双根蜡烛形态识别
# ============================================================================

def is_bullish_engulfing(candles: List[Candle], idx: int,
                         min_body_ratio: float = 0.1) -> Optional[PatternResult]:
    """
    看涨吞没形态
    
    特征: 第一根阴线，第二根阳线完全吞没第一根实体
    """
    if idx < 1:
        return None
    
    c1 = candles[idx - 1]
    c2 = candles[idx]
    
    # 第一根必须是阴线
    if not c1.is_bearish:
        return None
    
    # 第二根必须是阳线
    if not c2.is_bullish:
        return None
    
    # 第二根完全吞没第一根实体
    if c2.body_bottom <= c1.body_bottom and c2.body_top >= c1.body_top:
        # 计算强度
        engulf_strength = c2.body / c1.body if c1.body > 0 else 1.0
        strength = min(1.0, engulf_strength / 2)
        
        return PatternResult(
            pattern_type=PatternType.BULLISH_ENGULFING,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=strength,
            candles=[idx - 1, idx],
            description="看涨吞没: 阳线完全吞没前一根阴线",
            confidence=0.8 + strength * 0.2
        )
    
    return None


def is_bearish_engulfing(candles: List[Candle], idx: int,
                         min_body_ratio: float = 0.1) -> Optional[PatternResult]:
    """
    看跌吞没形态
    
    特征: 第一根阳线，第二根阴线完全吞没第一根实体
    """
    if idx < 1:
        return None
    
    c1 = candles[idx - 1]
    c2 = candles[idx]
    
    # 第一根必须是阳线
    if not c1.is_bullish:
        return None
    
    # 第二根必须是阴线
    if not c2.is_bearish:
        return None
    
    # 第二根完全吞没第一根实体
    if c2.body_bottom <= c1.body_bottom and c2.body_top >= c1.body_top:
        engulf_strength = c2.body / c1.body if c1.body > 0 else 1.0
        strength = min(1.0, engulf_strength / 2)
        
        return PatternResult(
            pattern_type=PatternType.BEARISH_ENGULFING,
            signal_type=SignalType.BEARISH_REVERSAL,
            strength=strength,
            candles=[idx - 1, idx],
            description="看跌吞没: 阴线完全吞没前一根阳线",
            confidence=0.8 + strength * 0.2
        )
    
    return None


def is_bullish_harami(candles: List[Candle], idx: int) -> Optional[PatternResult]:
    """
    看涨孕育线
    
    特征: 第一根大阴线，第二根小阳线被第一根实体包含
    """
    if idx < 1:
        return None
    
    c1 = candles[idx - 1]
    c2 = candles[idx]
    
    # 第一根必须是阴线且实体较大
    if not c1.is_bearish:
        return None
    
    # 第二根必须是小实体且被包含
    if c2.body_bottom >= c1.body_bottom and c2.body_top <= c1.body_top:
        containment_ratio = c2.body / c1.body if c1.body > 0 else 0
        
        return PatternResult(
            pattern_type=PatternType.BULLISH_HARAMI,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=0.5 + (1 - containment_ratio) * 0.3,
            candles=[idx - 1, idx],
            description="看涨孕育线: 小阳线被大阴线包含",
            confidence=0.7
        )
    
    return None


def is_bearish_harami(candles: List[Candle], idx: int) -> Optional[PatternResult]:
    """
    看跌孕育线
    
    特征: 第一根大阳线，第二根小阴线被第一根实体包含
    """
    if idx < 1:
        return None
    
    c1 = candles[idx - 1]
    c2 = candles[idx]
    
    if not c1.is_bullish:
        return None
    
    if c2.body_bottom >= c1.body_bottom and c2.body_top <= c1.body_top:
        containment_ratio = c2.body / c1.body if c1.body > 0 else 0
        
        return PatternResult(
            pattern_type=PatternType.BEARISH_HARAMI,
            signal_type=SignalType.BEARISH_REVERSAL,
            strength=0.5 + (1 - containment_ratio) * 0.3,
            candles=[idx - 1, idx],
            description="看跌孕育线: 小阴线被大阳线包含",
            confidence=0.7
        )
    
    return None


def is_tweezer_top(candles: List[Candle], idx: int, tolerance: float = 0.02) -> Optional[PatternResult]:
    """
    镊子顶
    
    特征: 两根蜡烛的高点几乎相同
    """
    if idx < 1:
        return None
    
    c1 = candles[idx - 1]
    c2 = candles[idx]
    
    # 检查高点是否相近
    avg_high = (c1.high + c2.high) / 2
    if avg_high == 0:
        return None
    
    high_diff = abs(c1.high - c2.high) / avg_high
    if high_diff <= tolerance:
        return PatternResult(
            pattern_type=PatternType.TWEEZER_TOP,
            signal_type=SignalType.BEARISH_REVERSAL,
            strength=0.6 + (1 - high_diff / tolerance) * 0.2,
            candles=[idx - 1, idx],
            description="镊子顶: 两根蜡烛高点相近",
            confidence=0.75
        )
    
    return None


def is_tweezer_bottom(candles: List[Candle], idx: int, tolerance: float = 0.02) -> Optional[PatternResult]:
    """
    镊子底
    
    特征: 两根蜡烛的低点几乎相同
    """
    if idx < 1:
        return None
    
    c1 = candles[idx - 1]
    c2 = candles[idx]
    
    avg_low = (c1.low + c2.low) / 2
    if avg_low == 0:
        return None
    
    low_diff = abs(c1.low - c2.low) / avg_low
    if low_diff <= tolerance:
        return PatternResult(
            pattern_type=PatternType.TWEEZER_BOTTOM,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=0.6 + (1 - low_diff / tolerance) * 0.2,
            candles=[idx - 1, idx],
            description="镊子底: 两根蜡烛低点相近",
            confidence=0.75
        )
    
    return None


def is_piercing_line(candles: List[Candle], idx: int,
                     min_penetration: float = 0.5) -> Optional[PatternResult]:
    """
    刺透线
    
    特征: 第一根阴线，第二根阳线开盘低于前一根实体底部附近，收盘超过前一根实体中点
    """
    if idx < 1:
        return None
    
    c1 = candles[idx - 1]
    c2 = candles[idx]
    
    if not c1.is_bearish or not c2.is_bullish:
        return None
    
    # 第二根开盘低于第一根实体底部附近 (开盘在低位)
    # 不需要严格低于low，只要开盘低于前一根收盘即可
    if c2.open >= c1.close:
        return None
    
    # 第二根收盘超过第一根实体中点
    midpoint = (c1.open + c1.close) / 2
    penetration = (c2.close - midpoint) / c1.body if c1.body > 0 else 0
    
    if penetration >= min_penetration:
        return PatternResult(
            pattern_type=PatternType.PIERCING_LINE,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=0.5 + penetration * 0.3,
            candles=[idx - 1, idx],
            description="刺透线: 阳线刺透阴线实体中点",
            confidence=0.75
        )
    
    return None


def is_dark_cloud_cover(candles: List[Candle], idx: int,
                        min_penetration: float = 0.5) -> Optional[PatternResult]:
    """
    乌云盖顶
    
    特征: 第一根阳线，第二根阴线开盘高于前一根实体顶部附近，收盘跌破前一根实体中点
    """
    if idx < 1:
        return None
    
    c1 = candles[idx - 1]
    c2 = candles[idx]
    
    if not c1.is_bullish or not c2.is_bearish:
        return None
    
    # 第二根开盘高于第一根实体顶部附近
    # 不需要严格高于high，只要开盘高于前一根收盘即可
    if c2.open <= c1.close:
        return None
    
    # 第二根收盘跌破第一根实体中点
    midpoint = (c1.open + c1.close) / 2
    penetration = (midpoint - c2.close) / c1.body if c1.body > 0 else 0
    
    if penetration >= min_penetration:
        return PatternResult(
            pattern_type=PatternType.DARK_CLOUD_COVER,
            signal_type=SignalType.BEARISH_REVERSAL,
            strength=0.5 + penetration * 0.3,
            candles=[idx - 1, idx],
            description="乌云盖顶: 阴线覆盖阳线实体中点",
            confidence=0.75
        )
    
    return None


# ============================================================================
# 三根蜡烛形态识别
# ============================================================================

def is_morning_star(candles: List[Candle], idx: int) -> Optional[PatternResult]:
    """
    启明星
    
    特征: 第一根大阴线，第二根小实体(十字星类)，第三根大阳线收盘超过第一根实体中点
    """
    if idx < 2:
        return None
    
    c1 = candles[idx - 2]
    c2 = candles[idx - 1]
    c3 = candles[idx]
    
    # 第一根大阴线
    if not c1.is_bearish or c1.body_ratio() < 0.5:
        return None
    
    # 第二根小实体
    if c2.body_ratio() > 0.35:
        return None
    
    # 第三根大阳线
    if not c3.is_bullish or c3.body_ratio() < 0.4:
        return None
    
    # 第三根收盘超过第一根实体中点
    midpoint = (c1.open + c1.close) / 2
    if c3.close < midpoint:
        return None
    
    return PatternResult(
        pattern_type=PatternType.MORNING_STAR,
        signal_type=SignalType.BULLISH_REVERSAL,
        strength=0.7,
        candles=[idx - 2, idx - 1, idx],
        description="启明星: 大阴线+小实体+大阳线",
        confidence=0.85
    )


def is_evening_star(candles: List[Candle], idx: int) -> Optional[PatternResult]:
    """
    黄昏星
    
    特征: 第一根大阳线，第二根小实体(十字星类)，第三根大阴线收盘跌破第一根实体中点
    """
    if idx < 2:
        return None
    
    c1 = candles[idx - 2]
    c2 = candles[idx - 1]
    c3 = candles[idx]
    
    if not c1.is_bullish or c1.body_ratio() < 0.5:
        return None
    
    if c2.body_ratio() > 0.35:
        return None
    
    if not c3.is_bearish or c3.body_ratio() < 0.4:
        return None
    
    midpoint = (c1.open + c1.close) / 2
    if c3.close > midpoint:
        return None
    
    return PatternResult(
        pattern_type=PatternType.EVENING_STAR,
        signal_type=SignalType.BEARISH_REVERSAL,
        strength=0.7,
        candles=[idx - 2, idx - 1, idx],
        description="黄昏星: 大阳线+小实体+大阴线",
        confidence=0.85
    )


def is_three_white_soldiers(candles: List[Candle], idx: int,
                            min_body_ratio: float = 0.5) -> Optional[PatternResult]:
    """
    三白兵
    
    特征: 连续三根上涨阳线，每根开盘在前一根实体内，收盘更高
    """
    if idx < 2:
        return None
    
    c1 = candles[idx - 2]
    c2 = candles[idx - 1]
    c3 = candles[idx]
    
    # 三根都是阳线
    if not (c1.is_bullish and c2.is_bullish and c3.is_bullish):
        return None
    
    # 实体较大
    if not (c1.body_ratio() >= min_body_ratio and 
            c2.body_ratio() >= min_body_ratio and
            c3.body_ratio() >= min_body_ratio):
        return None
    
    # 每根收盘更高
    if not (c3.close > c2.close > c1.close):
        return None
    
    # 每根开盘在前一根实体内
    if not (c2.open > c1.body_bottom and c2.open < c1.body_top):
        return None
    
    if not (c3.open > c2.body_bottom and c3.open < c2.body_top):
        return None
    
    return PatternResult(
        pattern_type=PatternType.THREE_WHITE_SOLDIERS,
        signal_type=SignalType.BULLISH_REVERSAL,
        strength=0.8,
        candles=[idx - 2, idx - 1, idx],
        description="三白兵: 连续三根上涨阳线",
        confidence=0.9
    )


def is_three_black_crows(candles: List[Candle], idx: int,
                         min_body_ratio: float = 0.5) -> Optional[PatternResult]:
    """
    三黑鸦
    
    特征: 连续三根下跌阴线，每根开盘在前一根实体内，收盘更低
    """
    if idx < 2:
        return None
    
    c1 = candles[idx - 2]
    c2 = candles[idx - 1]
    c3 = candles[idx]
    
    if not (c1.is_bearish and c2.is_bearish and c3.is_bearish):
        return None
    
    if not (c1.body_ratio() >= min_body_ratio and 
            c2.body_ratio() >= min_body_ratio and
            c3.body_ratio() >= min_body_ratio):
        return None
    
    if not (c3.close < c2.close < c1.close):
        return None
    
    if not (c2.open > c1.body_bottom and c2.open < c1.body_top):
        return None
    
    if not (c3.open > c2.body_bottom and c3.open < c2.body_top):
        return None
    
    return PatternResult(
        pattern_type=PatternType.THREE_BLACK_CROWS,
        signal_type=SignalType.BEARISH_REVERSAL,
        strength=0.8,
        candles=[idx - 2, idx - 1, idx],
        description="三黑鸦: 连续三根下跌阴线",
        confidence=0.9
    )


def is_abandoned_baby(candles: List[Candle], idx: int,
                      doji_threshold: float = 0.05) -> Optional[PatternResult]:
    """
    弃婴形态
    
    特征: 第一根大阴线，第二根十字星(有缺口)，第三根大阳线(有缺口)
    """
    if idx < 2:
        return None
    
    c1 = candles[idx - 2]
    c2 = candles[idx - 1]
    c3 = candles[idx]
    
    # 第一根大阴线
    if not c1.is_bearish or c1.body_ratio() < 0.5:
        return None
    
    # 第二根十字星
    if not is_doji(c2, doji_threshold):
        return None
    
    # 第三根大阳线
    if not c3.is_bullish or c3.body_ratio() < 0.5:
        return None
    
    # 缺口: 十字星低点高于第一根高点，十字星高点低于第三根低点
    if c2.low > c1.high and c2.high < c3.low:
        return PatternResult(
            pattern_type=PatternType.ABANDONED_BABY,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=0.85,
            candles=[idx - 2, idx - 1, idx],
            description="弃婴: 大阴线+缺口十字星+缺口大阳线",
            confidence=0.95
        )
    
    return None


def is_three_outside_up(candles: List[Candle], idx: int) -> Optional[PatternResult]:
    """
    三外升
    
    特征: 看涨吞没+第三根阳线收盘更高
    """
    engulfing = is_bullish_engulfing(candles, idx - 1)
    if engulfing is None:
        return None
    
    c3 = candles[idx]
    c2 = candles[idx - 1]
    
    if not c3.is_bullish or c3.close <= c2.close:
        return None
    
    return PatternResult(
        pattern_type=PatternType.THREE_OUTSIDE_UP,
        signal_type=SignalType.BULLISH_REVERSAL,
        strength=0.75,
        candles=[idx - 2, idx - 1, idx],
        description="三外升: 看涨吞没+阳线确认",
        confidence=0.85
    )


def is_three_outside_down(candles: List[Candle], idx: int) -> Optional[PatternResult]:
    """
    三外降
    
    特征: 看跌吞没+第三根阴线收盘更低
    """
    engulfing = is_bearish_engulfing(candles, idx - 1)
    if engulfing is None:
        return None
    
    c3 = candles[idx]
    c2 = candles[idx - 1]
    
    if not c3.is_bearish or c3.close >= c2.close:
        return None
    
    return PatternResult(
        pattern_type=PatternType.THREE_OUTSIDE_DOWN,
        signal_type=SignalType.BEARISH_REVERSAL,
        strength=0.75,
        candles=[idx - 2, idx - 1, idx],
        description="三外降: 看跌吞没+阴线确认",
        confidence=0.85
    )


def is_three_inside_up(candles: List[Candle], idx: int) -> Optional[PatternResult]:
    """
    三内升
    
    特征: 看涨孕育线+第三根阳线收盘更高
    """
    harami = is_bullish_harami(candles, idx - 1)
    if harami is None:
        return None
    
    c3 = candles[idx]
    c2 = candles[idx - 1]
    
    if not c3.is_bullish or c3.close <= c2.close:
        return None
    
    return PatternResult(
        pattern_type=PatternType.THREE_INSIDE_UP,
        signal_type=SignalType.BULLISH_REVERSAL,
        strength=0.65,
        candles=[idx - 2, idx - 1, idx],
        description="三内升: 看涨孕育线+阳线确认",
        confidence=0.8
    )


def is_three_inside_down(candles: List[Candle], idx: int) -> Optional[PatternResult]:
    """
    三内降
    
    特征: 看跌孕育线+第三根阴线收盘更低
    """
    harami = is_bearish_harami(candles, idx - 1)
    if harami is None:
        return None
    
    c3 = candles[idx]
    c2 = candles[idx - 1]
    
    if not c3.is_bearish or c3.close >= c2.close:
        return None
    
    return PatternResult(
        pattern_type=PatternType.THREE_INSIDE_DOWN,
        signal_type=SignalType.BEARISH_REVERSAL,
        strength=0.65,
        candles=[idx - 2, idx - 1, idx],
        description="三内降: 看跌孕育线+阴线确认",
        confidence=0.8
    )


# ============================================================================
# 多根蜡烛形态识别 (趋势形态)
# ============================================================================

def detect_head_and_shoulders(candles: List[Candle], idx: int,
                               min_candles: int = 5) -> Optional[PatternResult]:
    """
    头肩顶形态
    
    特征: 三个峰值，中间最高(头)，两侧较低(肩)
    """
    if idx < min_candles + 2:
        return None
    
    # 简化检测: 检查最近5-10根蜡烛
    lookback = min(10, idx)
    highs = [c.high for c in candles[idx - lookback:idx + 1]]
    
    # 寻找峰值
    peaks = []
    for i in range(1, len(highs) - 1):
        if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:
            peaks.append((i + idx - lookback, highs[i]))
    
    if len(peaks) < 3:
        return None
    
    # 检查是否符合头肩形态
    if len(peaks) >= 3:
        # 取最近的三个峰值
        recent_peaks = peaks[-3:]
        left, head, right = recent_peaks
        
        # 头应该高于两侧肩膀
        if head[1] > left[1] and head[1] > right[1]:
            # 两肩应该大致相等
            shoulder_diff = abs(left[1] - right[1]) / head[1]
            if shoulder_diff < 0.1:  # 允许10%差异
                return PatternResult(
                    pattern_type=PatternType.HEAD_AND_SHOULDERS,
                    signal_type=SignalType.BEARISH_REVERSAL,
                    strength=0.75,
                    candles=[left[0], head[0], right[0]],
                    description="头肩顶: 三峰形态，中间最高",
                    confidence=0.7
                )
    
    return None


def detect_inverse_head_and_shoulders(candles: List[Candle], idx: int,
                                       min_candles: int = 5) -> Optional[PatternResult]:
    """
    头肩底形态 (倒头肩顶)
    
    特征: 三个谷值，中间最低(头)，两侧较高(肩)
    """
    if idx < min_candles + 2:
        return None
    
    lookback = min(10, idx)
    lows = [c.low for c in candles[idx - lookback:idx + 1]]
    
    # 寻找谷值
    troughs = []
    for i in range(1, len(lows) - 1):
        if lows[i] < lows[i - 1] and lows[i] < lows[i + 1]:
            troughs.append((i + idx - lookback, lows[i]))
    
    if len(troughs) < 3:
        return None
    
    if len(troughs) >= 3:
        recent_troughs = troughs[-3:]
        left, head, right = recent_troughs
        
        if head[1] < left[1] and head[1] < right[1]:
            shoulder_diff = abs(left[1] - right[1]) / head[1]
            if shoulder_diff < 0.1:
                return PatternResult(
                    pattern_type=PatternType.INVERSE_HEAD_AND_SHOULDERS,
                    signal_type=SignalType.BULLISH_REVERSAL,
                    strength=0.75,
                    candles=[left[0], head[0], right[0]],
                    description="头肩底: 三谷形态，中间最低",
                    confidence=0.7
                )
    
    return None


def detect_double_top(candles: List[Candle], idx: int,
                      tolerance: float = 0.02) -> Optional[PatternResult]:
    """
    双顶形态 (M头)
    
    特征: 两个相近的高点，中间有一个谷值
    """
    if idx < 5:
        return None
    
    lookback = min(20, idx)
    
    # 寻找峰值
    peaks = []
    for i in range(idx - lookback, idx + 1):
        if i > 0 and i < len(candles) - 1:
            if candles[i].high > candles[i - 1].high and candles[i].high > candles[i + 1].high:
                peaks.append((i, candles[i].high))
    
    if len(peaks) < 2:
        return None
    
    # 检查最近的两个峰值
    recent = peaks[-2:]
    p1, p2 = recent
    
    avg_high = (p1[1] + p2[1]) / 2
    high_diff = abs(p1[1] - p2[1]) / avg_high
    
    if high_diff <= tolerance:
        return PatternResult(
            pattern_type=PatternType.DOUBLE_TOP,
            signal_type=SignalType.BEARISH_REVERSAL,
            strength=0.65 + (1 - high_diff / tolerance) * 0.2,
            candles=[p1[0], p2[0]],
            description="双顶: 两个相近高点形成M头",
            confidence=0.75
        )
    
    return None


def detect_double_bottom(candles: List[Candle], idx: int,
                         tolerance: float = 0.02) -> Optional[PatternResult]:
    """
    双底形态 (W底)
    
    特征: 两个相近的低点，中间有一个峰值
    """
    if idx < 5:
        return None
    
    lookback = min(20, idx)
    
    troughs = []
    for i in range(idx - lookback, idx + 1):
        if i > 0 and i < len(candles) - 1:
            if candles[i].low < candles[i - 1].low and candles[i].low < candles[i + 1].low:
                troughs.append((i, candles[i].low))
    
    if len(troughs) < 2:
        return None
    
    recent = troughs[-2:]
    t1, t2 = recent
    
    avg_low = (t1[1] + t2[1]) / 2
    low_diff = abs(t1[1] - t2[1]) / avg_low
    
    if low_diff <= tolerance:
        return PatternResult(
            pattern_type=PatternType.DOUBLE_BOTTOM,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=0.65 + (1 - low_diff / tolerance) * 0.2,
            candles=[t1[0], t2[0]],
            description="双底: 两个相近低点形成W底",
            confidence=0.75
        )
    
    return None


# ============================================================================
# 综合形态识别
# ============================================================================

def identify_single_candle_pattern(candle: Candle) -> List[PatternResult]:
    """
    识别单根蜡烛形态
    
    Returns:
        识别到的形态列表
    """
    patterns = []
    
    if is_doji(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.DOJI,
            signal_type=SignalType.NEUTRAL,
            strength=0.5,
            candles=[],
            description="十字星: 开盘收盘几乎相同",
            confidence=0.9
        ))
    
    if is_long_legged_doji(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.LONG_LEGGED_DOJI,
            signal_type=SignalType.NEUTRAL,
            strength=0.6,
            candles=[],
            description="长腿十字星: 市场犹豫不决",
            confidence=0.85
        ))
    
    if is_dragonfly_doji(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.DRAGONFLY_DOJI,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=0.65,
            candles=[],
            description="蜻蜓十字星: 买方力量增强",
            confidence=0.85
        ))
    
    if is_gravestone_doji(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.GRAVESTONE_DOJI,
            signal_type=SignalType.BEARISH_REVERSAL,
            strength=0.65,
            candles=[],
            description="墓碑十字星: 卖方力量增强",
            confidence=0.85
        ))
    
    if is_hammer(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.HAMMER,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=0.7,
            candles=[],
            description="锤子线: 潜在底部反转",
            confidence=0.8
        ))
    
    if is_inverted_hammer(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.INVERTED_HAMMER,
            signal_type=SignalType.BULLISH_REVERSAL,
            strength=0.65,
            candles=[],
            description="倒锤子线: 潜在底部反转",
            confidence=0.75
        ))
    
    if is_hanging_man(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.HANGING_MAN,
            signal_type=SignalType.BEARISH_REVERSAL,
            strength=0.6,
            candles=[],
            description="上吊线: 潜在顶部反转",
            confidence=0.7
        ))
    
    if is_shooting_star(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.SHOOTING_STAR,
            signal_type=SignalType.BEARISH_REVERSAL,
            strength=0.7,
            candles=[],
            description="流星线: 潜在顶部反转",
            confidence=0.8
        ))
    
    if is_marubozu(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.MARUBOZU,
            signal_type=SignalType.BULLISH_CONTINUATION if candle.is_bullish else SignalType.BEARISH_CONTINUATION,
            strength=0.8,
            candles=[],
            description=f"光头光脚{('阳' if candle.is_bullish else '阴')}线: 强势信号",
            confidence=0.95
        ))
    
    if is_spinning_top(candle):
        patterns.append(PatternResult(
            pattern_type=PatternType.SPINNING_TOP,
            signal_type=SignalType.NEUTRAL,
            strength=0.4,
            candles=[],
            description="纺锤线: 市场犹豫不决",
            confidence=0.85
        ))
    
    return patterns


def identify_patterns(candles: List[Candle], idx: int = -1) -> List[PatternResult]:
    """
    综合形态识别
    
    Args:
        candles: 蜡烛列表
        idx: 要分析的蜡烛索引，-1表示最后一根
    
    Returns:
        识别到的所有形态列表
    """
    if not candles:
        return []
    
    if idx == -1:
        idx = len(candles) - 1
    
    patterns = []
    
    # 单根形态
    single_patterns = identify_single_candle_pattern(candles[idx])
    for p in single_patterns:
        p.candles = [idx]
        patterns.append(p)
    
    # 双根形态
    double_pattern_funcs = [
        is_bullish_engulfing,
        is_bearish_engulfing,
        is_bullish_harami,
        is_bearish_harami,
        is_tweezer_top,
        is_tweezer_bottom,
        is_piercing_line,
        is_dark_cloud_cover,
    ]
    
    for func in double_pattern_funcs:
        result = func(candles, idx)
        if result:
            patterns.append(result)
    
    # 三根形态
    triple_pattern_funcs = [
        is_morning_star,
        is_evening_star,
        is_three_white_soldiers,
        is_three_black_crows,
        is_three_outside_up,
        is_three_outside_down,
        is_three_inside_up,
        is_three_inside_down,
        is_abandoned_baby,
    ]
    
    for func in triple_pattern_funcs:
        result = func(candles, idx)
        if result:
            patterns.append(result)
    
    # 多根形态 (趋势形态)
    multi_pattern_funcs = [
        detect_head_and_shoulders,
        detect_inverse_head_and_shoulders,
        detect_double_top,
        detect_double_bottom,
    ]
    
    for func in multi_pattern_funcs:
        result = func(candles, idx)
        if result:
            patterns.append(result)
    
    # 按强度排序
    patterns.sort(key=lambda p: p.strength, reverse=True)
    
    return patterns


def scan_all_patterns(candles: List[Candle]) -> Dict[int, List[PatternResult]]:
    """
    扫描所有蜡烛的形态
    
    Args:
        candles: 蜡烛列表
    
    Returns:
        每根蜡烛索引对应的形态列表
    """
    results = {}
    
    for i in range(len(candles)):
        patterns = identify_patterns(candles, i)
        if patterns:
            results[i] = patterns
    
    return results


def get_reversal_signals(candles: List[Candle], idx: int = -1) -> Dict[str, List[PatternResult]]:
    """
    获取反转信号
    
    Returns:
        bullish: 看涨反转形态列表
        bearish: 看跌反转形态列表
    """
    patterns = identify_patterns(candles, idx)
    
    bullish = [p for p in patterns if p.signal_type == SignalType.BULLISH_REVERSAL]
    bearish = [p for p in patterns if p.signal_type == SignalType.BEARISH_REVERSAL]
    
    return {
        "bullish": bullish,
        "bearish": bearish
    }


def analyze_trend_context(candles: List[Candle], idx: int, 
                          lookback: int = 10) -> str:
    """
    分析趋势背景
    
    Args:
        candles: 蜡烛列表
        idx: 当前索引
        lookback: 回看周期
    
    Returns:
        "uptrend", "downtrend", "sideways"
    """
    if idx < lookback:
        return "unknown"
    
    recent = candles[idx - lookback:idx + 1]
    first_close = recent[0].close
    last_close = recent[-1].close
    
    change = (last_close - first_close) / first_close if first_close > 0 else 0
    
    if change > 0.05:
        return "uptrend"
    elif change < -0.05:
        return "downtrend"
    else:
        return "sideways"


def pattern_summary(patterns: List[PatternResult]) -> str:
    """
    生成形态摘要报告
    """
    if not patterns:
        return "未检测到明显形态"
    
    lines = ["蜡烛图形态识别结果:"]
    lines.append("=" * 40)
    
    for p in patterns:
        signal_icon = {
            SignalType.BULLISH_REVERSAL: "📈",
            SignalType.BEARISH_REVERSAL: "📉",
            SignalType.BULLISH_CONTINUATION: "➡️📈",
            SignalType.BEARISH_CONTINUATION: "➡️📉",
            SignalType.NEUTRAL: "⚖️",
        }.get(p.signal_type, "?")
        
        lines.append(f"{signal_icon} {p.description}")
        lines.append(f"   强度: {p.strength:.2f}, 置信度: {p.confidence:.2f}")
        lines.append(f"   涉及蜡烛: {p.candles}")
    
    return "\n".join(lines)


# ============================================================================
# 便捷函数
# ============================================================================

def create_candle(open: float, high: float, low: float, close: float,
                  volume: Optional[float] = None) -> Candle:
    """创建蜡烛对象"""
    return Candle(open, high, low, close, volume)


def candles_from_data(data: List[Dict[str, float]]) -> List[Candle]:
    """
    从字典数据创建蜡烛列表
    
    Args:
        data: 包含 open, high, low, close 的字典列表
    
    Returns:
        蜡烛列表
    """
    return [
        Candle(
            open=d.get('open', 0),
            high=d.get('high', 0),
            low=d.get('low', 0),
            close=d.get('close', 0),
            volume=d.get('volume')
        )
        for d in data
    ]


def calculate_body_size_rank(candles: List[Candle]) -> List[int]:
    """
    计算实体大小排名 (用于识别大小实体)
    """
    bodies = [(i, c.body) for i, c in enumerate(candles)]
    bodies.sort(key=lambda x: x[1])
    
    ranks = [0] * len(candles)
    for rank, (i, _) in enumerate(bodies):
        ranks[i] = rank
    
    return ranks


# 导出公共接口
__all__ = [
    # 数据结构
    'Candle',
    'PatternType',
    'SignalType',
    'PatternResult',
    
    # 单根形态识别
    'is_doji',
    'is_long_legged_doji',
    'is_dragonfly_doji',
    'is_gravestone_doji',
    'is_hammer',
    'is_inverted_hammer',
    'is_hanging_man',
    'is_shooting_star',
    'is_marubozu',
    'is_spinning_top',
    'identify_single_candle_pattern',
    
    # 双根形态识别
    'is_bullish_engulfing',
    'is_bearish_engulfing',
    'is_bullish_harami',
    'is_bearish_harami',
    'is_tweezer_top',
    'is_tweezer_bottom',
    'is_piercing_line',
    'is_dark_cloud_cover',
    
    # 三根形态识别
    'is_morning_star',
    'is_evening_star',
    'is_three_white_soldiers',
    'is_three_black_crows',
    'is_three_outside_up',
    'is_three_outside_down',
    'is_three_inside_up',
    'is_three_inside_down',
    'is_abandoned_baby',
    
    # 多根形态识别
    'detect_head_and_shoulders',
    'detect_inverse_head_and_shoulders',
    'detect_double_top',
    'detect_double_bottom',
    
    # 综合识别
    'identify_patterns',
    'scan_all_patterns',
    'get_reversal_signals',
    'analyze_trend_context',
    'pattern_summary',
    
    # 便捷函数
    'create_candle',
    'candles_from_data',
    'calculate_body_size_rank',
]


# 主程序演示
if __name__ == "__main__":
    print("=" * 60)
    print("蜡烛图形态识别工具演示")
    print("=" * 60)
    
    # 创建示例蜡烛数据
    sample_data = [
        {'open': 100, 'high': 105, 'low': 99, 'close': 102},  # 小阳线
        {'open': 102, 'high': 103, 'low': 95, 'close': 96},   # 大阴线
        {'open': 96, 'high': 97, 'low': 95.5, 'close': 96.2}, # 小实体(孕育线)
        {'open': 96, 'high': 103, 'low': 95, 'close': 102},   # 大阳线(看涨吞没)
        {'open': 102, 'high': 108, 'low': 101, 'close': 107}, # 阳线确认
    ]
    
    candles = candles_from_data(sample_data)
    
    print("\n蜡烛数据:")
    for i, c in enumerate(candles):
        print(f"  [{i}] O:{c.open} H:{c.high} L:{c.low} C:{c.close} "
              f"{'阳' if c.is_bullish else '阴'}线 实体:{c.body:.1f}")
    
    print("\n形态识别:")
    patterns = identify_patterns(candles)
    print(pattern_summary(patterns))
    
    # 单根形态演示
    print("\n单根蜡烛形态分析:")
    doji_candle = create_candle(100, 105, 95, 100.1)  # 十字星
    hammer_candle = create_candle(100, 102, 90, 101)  # 锤子线
    shooting_star_candle = create_candle(100, 110, 99, 101)  # 流星线
    
    for name, candle in [("十字星", doji_candle), ("锤子线", hammer_candle), ("流星线", shooting_star_candle)]:
        print(f"\n{name}:")
        single_patterns = identify_single_candle_pattern(candle)
        for p in single_patterns:
            print(f"  - {p.pattern_type.value}: {p.description}")