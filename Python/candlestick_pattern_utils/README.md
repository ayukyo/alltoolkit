# Candlestick Pattern Recognition Utilities

蜡烛图形态识别工具 - 零外部依赖的日本蜡烛图形态识别库

## 功能特性

### 单根蜡烛形态
- 十字星 (Doji)
- 长腿十字星 (Long Legged Doji)
- 蜻蜓十字星 (Dragonfly Doji)
- 墓碑十字星 (Gravestone Doji)
- 锤子线 (Hammer)
- 倒锤子线 (Inverted Hammer)
- 上吊线 (Hanging Man)
- 流星线 (Shooting Star)
- 光头光脚蜡烛 (Marubozu)
- 纡锤线 (Spinning Top)

### 双根蜡烛形态
- 看涨吞没 (Bullish Engulfing)
- 看跌吞没 (Bearish Engulfing)
- 看涨孕育线 (Bullish Harami)
- 看跌孕育线 (Bearish Harami)
- 镊子顶 (Tweezer Top)
- 镊子底 (Tweezer Bottom)
- 刺透线 (Piercing Line)
- 乌云盖顶 (Dark Cloud Cover)

### 三根蜡烛形态
- 启明星 (Morning Star)
- 黄昏星 (Evening Star)
- 三白兵 (Three White Soldiers)
- 三黑鸦 (Three Black Crows)
- 三外升/降 (Three Outside Up/Down)
- 三内升/降 (Three Inside Up/Down)
- 弃婴形态 (Abandoned Baby)

### 多根趋势形态
- 头肩顶/底 (Head and Shoulders)
- 双顶/底 (Double Top/Bottom)

## 安装使用

```python
from candlestick_pattern_utils import (
    create_candle,
    candles_from_data,
    identify_patterns,
    is_hammer,
    is_bullish_engulfing,
    is_morning_star,
)
```

## 快速示例

### 创建蜡烛数据

```python
# 单根蜡烛
candle = create_candle(open=100, high=105, low=95, close=103)

# 从数据列表创建
data = [
    {'open': 100, 'high': 105, 'low': 95, 'close': 103},
    {'open': 103, 'high': 108, 'low': 102, 'close': 107},
]
candles = candles_from_data(data)
```

### 单根形态识别

```python
candle = create_candle(100, 102, 85, 101)  # 锤子线
if is_hammer(candle):
    print("检测到锤子线 - 潜在底部反转信号!")
```

### 双根形态识别

```python
# 看涨吞没
candles = candles_from_data([
    {'open': 105, 'high': 106, 'low': 95, 'close': 96},  # 阴线
    {'open': 94, 'high': 105, 'low': 93, 'close': 104},  # 大阳线
])

result = is_bullish_engulfing(candles, 1)
if result:
    print(f"检测到看涨吞没! 强度: {result.strength}")
```

### 综合形态扫描

```python
# 识别所有形态
patterns = identify_patterns(candles, idx=-1)

for p in patterns:
    print(f"形态: {p.pattern_type.value}")
    print(f"信号: {p.signal_type.value}")
    print(f"强度: {p.strength}")
    print(f"描述: {p.description}")
```

## API 参考

### Candle 类

| 属性 | 描述 |
|------|------|
| `open`, `high`, `low`, `close` | OHLC 价格 |
| `body` | 实体大小 |
| `upper_shadow` | 上影线长度 |
| `lower_shadow` | 下影线长度 |
| `range` | 总范围 |
| `is_bullish` | 是否阳线 |
| `is_bearish` | 是否阴线 |
| `is_doji_like` | 是否十字星形态 |

### PatternResult 类

| 属性 | 描述 |
|------|------|
| `pattern_type` | 形态类型枚举 |
| `signal_type` | 信号类型 (看涨/看跌反转/延续) |
| `strength` | 形态强度 (0.0-1.0) |
| `candles` | 涉及的蜡烛索引列表 |
| `description` | 中文描述 |
| `confidence` | 识别置信度 |

### 主要函数

| 函数 | 描述 |
|------|------|
| `identify_patterns(candles, idx)` | 综合形态识别 |
| `scan_all_patterns(candles)` | 扫描所有蜡烛 |
| `get_reversal_signals(candles, idx)` | 获取反转信号 |
| `pattern_summary(patterns)` | 生成摘要报告 |
| `analyze_trend_context(candles, idx)` | 分析趋势背景 |

## 实战建议

1. **结合趋势背景**: 形态的有效性取决于出现位置
   - 锤子线在下跌趋势中有效
   - 流星线在上升趋势中有效

2. **关注强度指标**: `strength >= 0.7` 的形态更可靠

3. **等待确认**: 形态出现后，等待下一根蜡烛确认

4. **多形态组合**: 多个形态同时出现时信号更强

## 测试运行

```bash
cd Python/candlestick_pattern_utils
python candlestick_pattern_utils_test.py
```

## 示例运行

```bash
cd Python/candlestick_pattern_utils
python examples/usage_examples.py
```

## 零依赖

本模块使用纯 Python 实现，无需安装任何外部包。

---

作者: AllToolkit
日期: 2026-05-13