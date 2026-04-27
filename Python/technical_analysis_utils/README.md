# 技术分析工具 (technical_analysis_utils)

股票/金融数据技术分析指标计算模块，零依赖纯 Python 实现。

## 功能列表

### 移动平均线
- **SMA** - 简单移动平均线
- **EMA** - 指数移动平均线
- **WMA** - 加权移动平均线

### 动量指标
- **RSI** - 相对强弱指数 (超买 > 70，超卖 < 30)
- **MACD** - 移动平均线收敛/发散指标
- **Momentum** - 动量指标
- **ROC** - 变动率指标
- **Stochastic** - 随机指标 (%K, %D)
- **Williams %R** - 威廉指标

### 波动性指标
- **Bollinger Bands** - 布林带
- **ATR** - 平均真实波幅
- **CCI** - 顺势指标

### 成交量指标
- **OBV** - 能量潮指标
- **VWAP** - 成交量加权平均价

### 趋势指标
- **KDJ** - KDJ 指标
- **ADX** - 平均趋向指数
- **趋势检测** - UP/DOWN/SIDEWAYS
- **金叉死叉** - 移动平均线交叉信号

### 支撑阻力
- **支撑位识别** - 局部低点聚类
- **阻力位识别** - 局部高点聚类

### 分析工具
- **综合分析** - 一键生成所有指标
- **波动率计算** - 年化波动率
- **最大回撤** - Max Drawdown
- **夏普比率** - Sharpe Ratio
- **收益率序列** - Returns Calculation

## 使用示例

### 基本使用

```python
from technical_analysis_utils.mod import *

# 收盘价数据
close = [44.12, 44.23, 44.52, 43.91, 44.22, 44.57, ...]

# SMA 计算
sma_20 = sma(close, 20)
print(f"SMA(20): {sma_20[-1]}")

# EMA 计算
ema_12 = ema(close, 12)
print(f"EMA(12): {ema_12[-1]}")

# RSI 计算
rsi_14 = rsi(close, 14)
print(f"RSI(14): {rsi_14[-1]}")
```

### MACD 分析

```python
# MACD 默认参数: fast=12, slow=26, signal=9
macd_result = macd(close)

last = macd_result[-1]
if last is not None:
    print(f"MACD: {last.macd}")
    print(f"Signal: {last.signal}")
    print(f"Histogram: {last.histogram}")
    
    # 判断信号
    if last.histogram > 0:
        print("多头信号")
    else:
        print("空头信号")
```

### 布林带

```python
# 默认参数: period=20, std_dev=2
bb = bollinger_bands(close)

last = bb[-1]
if last is not None:
    print(f"上轨: {last.upper}")
    print(f"中轨: {last.middle}")
    print(f"下轨: {last.lower}")
    print(f"带宽: {last.bandwidth}%")
    print(f"%B: {last.percent_b}")
    
    # 判断位置
    if last.percent_b > 1:
        print("突破上轨")
    elif last.percent_b < 0:
        print("跌破下轨")
```

### KDJ 指标

```python
high = [44.50, 44.60, 44.80, ...]
low = [43.90, 44.00, 44.20, ...]
close = [44.12, 44.23, 44.52, ...]

kdj_result = kdj(high, low, close, n=9, m1=3, m2=3)

last = kdj_result[-1]
if last is not None:
    print(f"K: {last['k']}")
    print(f"D: {last['d']}")
    print(f"J: {last['j']}")
    
    # 判断信号
    if last['k'] > 80 and last['d'] > 80:
        print("超买区")
    elif last['k'] < 20 and last['d'] < 20:
        print("超卖区")
```

### 趋势检测

```python
trend = detect_trend(close, period=20)
print(f"趋势: {trend.value}")

if trend == Trend.UP:
    print("上升趋势")
elif trend == Trend.DOWN:
    print("下降趋势")
else:
    print("横盘整理")
```

### 支撑阻力位

```python
sr = find_support_resistance(high, low, close)

print("支撑位:", sr.support_levels)
print("阻力位:", sr.resistance_levels)
```

### 金叉死叉

```python
short_ma = sma(close, 5)
long_ma = sma(close, 20)

crosses = golden_cross_death_cross(short_ma, long_ma)

# 查找最近的信号
for i, signal in enumerate(crosses):
    if signal == 'golden':
        print(f"第 {i} 天出现金叉")
    elif signal == 'death':
        print(f"第 {i} 天出现死叉")
```

### 综合分析

```python
# 一键生成所有指标
analysis = analyze(
    close,
    high=high,
    low=low,
    volume=volume
)

print(f"当前价格: {analysis['current_price']}")
print(f"趋势: {analysis['trend']}")
print(f"SMA(20): {analysis['sma']['sma_20']}")
print(f"RSI(14): {analysis['rsi_14']}")
print(f"MACD: {analysis['macd']}")
print(f"布林带: {analysis['bollinger']}")
print(f"KDJ: {analysis['kdj']}")
print(f"支撑位: {analysis['support_resistance']['supports']}")
print(f"阻力位: {analysis['support_resistance']['resistances']}")
```

### 风险指标

```python
# 波动率
volatility = calculate_volatility(close)
print(f"年化波动率: {volatility}%")

# 最大回撤
max_dd = max_drawdown(close)
print(f"最大回撤: {max_dd}%")

# 夏普比率
sharpe = sharpe_ratio(close, risk_free_rate=0.02)
print(f"夏普比率: {sharpe}")
```

### RSI 超买超卖判断

```python
rsi_value = rsi(close, 14)[-1]

if is_overbought(rsi_value):
    print("超买信号，可能回调")
elif is_oversold(rsi_value):
    print("超卖信号，可能反弹")
```

## 数据结构

### MACDResult
```python
@dataclass
class MACDResult:
    macd: float      # DIF 线
    signal: float    # DEA 线
    histogram: float # 柱状图 (MACD - Signal)
```

### BollingerBands
```python
@dataclass
class BollingerBands:
    upper: float      # 上轨
    middle: float     # 中轨
    lower: float      # 下轨
    bandwidth: float  # 带宽 (%)
    percent_b: float  # %B (价格位置)
```

### StochasticResult
```python
@dataclass
class StochasticResult:
    k: float  # %K
    d: float  # %D
```

### SupportResistance
```python
@dataclass
class SupportResistance:
    support_levels: List[float]     # 支撑位列表
    resistance_levels: List[float]  # 阻力位列表
```

## 参数说明

| 函数 | 默认参数 | 说明 |
|------|----------|------|
| sma | period | 常用: 5, 10, 20, 50, 200 |
| ema | period | 常用: 12, 26 |
| rsi | period=14 | 超买 > 70, 超卖 < 30 |
| macd | fast=12, slow=26, signal=9 | 经典参数 |
| bollinger_bands | period=20, std_dev=2.0 | 经典参数 |
| kdj | n=9, m1=3, m2=3 | 经典参数 |
| stochastic | k_period=14, d_period=3 | 经典参数 |
| atr | period=14 | 波动性指标 |
| williams_r | period=14 | 超买 > -20, 超卖 < -80 |

## 测试

```bash
python technical_analysis_utils_test.py
```

测试覆盖:
- 所有指标计算函数
- 边界值测试
- 异常输入处理
- 大数据集性能

## 注意事项

1. **数据长度**: 确保数据长度足够计算周期
2. **None 值**: 结果列表中前几个值可能为 None（数据不足）
3. **高低价**: KDJ/ATR/Williams %R 等需要提供 high/low
4. **成交量**: OBV/VWAP 需要提供 volume

## 零依赖

本模块仅使用 Python 标准库:
- `math` - 数学计算
- `typing` - 类型注解
- `dataclasses` - 数据结构
- `enum` - 枚举类型

## 版本

- 1.0.0 - 2026-04-27 - 初始版本