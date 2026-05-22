# RSI Utils - 相对强弱指标工具

RSI (Relative Strength Index) 相对强弱指标是金融技术分析中广泛使用的动量振荡器，用于衡量价格变动的速度和幅度，帮助识别超买/超卖条件。

## 功能特性

- ✅ **标准 RSI 计算** - 支持多种周期和平滑方法
- ✅ **多种平滑方法** - SMA、EMA、Wilder's Smoothing（标准方法）
- ✅ **背离检测** - 检测看涨/看跌背离信号
- ✅ **超买超卖信号** - 自动生成交易信号
- ✅ **Stochastic RSI** - 随机 RSI 计算（K/D 值）
- ✅ **增量式计算** - 实时数据流场景支持
- ✅ **零外部依赖** - 仅使用 Python 标准库

## 安装

```python
# 直接复制 mod.py 到项目中使用
from rsi_utils import calculate_rsi, RSICalculator
```

## 快速开始

### 基本用法

```python
from mod import calculate_rsi, calculate_rsi_single

# 价格序列
prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5,
          47, 47.5, 48, 48.5, 47.5, 48, 49, 48.5, 49, 50]

# 计算 14 周期 RSI 序列
rsi_values = calculate_rsi(prices, period=14)
# 输出: [None, None, ..., None, 70.5, 72.3, ...]  # 前 period+1 个为 None

# 计算最新 RSI 值
current_rsi = calculate_rsi_single(prices, period=14)
# 输出: 72.5
```

### 使用增量式计算器

```python
from mod import RSICalculator

# 创建计算器（适用于实时数据）
calc = RSICalculator(period=14, method='wilder')

# 逐个添加价格
for price in price_stream:
    rsi = calc.update(price)
    if rsi is not None:
        print(f"当前 RSI: {rsi:.2f}")

# 获取当前 RSI
current = calc.current_rsi

# 重置计算器
calc.reset()
```

### 背离检测

```python
from mod import calculate_rsi, detect_divergence

prices = [...]
rsi_values = calculate_rsi(prices, period=14)

# 检测背离（看涨/看跌）
divergences = detect_divergence(prices, rsi_values, lookback=5)

for div in divergences:
    print(f"{div['type']}: {div['message']}")
    # 输出如: "bullish: 看涨背离：价格新低但RSI未新低，可能上涨"
```

### 生成交易信号

```python
from mod import calculate_rsi, generate_signals

rsi_values = calculate_rsi(prices, period=14)

# 生成超买超卖信号
signals = generate_signals(rsi_values, oversold=30, overbought=70)

for sig in signals:
    print(f"索引 {sig['index']}: {sig['message']}")
```

### Stochastic RSI

```python
from mod import calculate_stoch_rsi

prices = [...]

# 计算 Stoch RSI（K/D 值）
k_values, d_values = calculate_stoch_rsi(prices, rsi_period=14, stoch_period=14)

# K 值超过 80 超买，低于 20 超卖
```

## API 参考

### `calculate_rsi(prices, period=14, method='wilder')`

计算 RSI 序列。

**参数：**
- `prices` (List[float]): 价格序列
- `period` (int): RSI 周期，默认 14
- `method` (str): 平滑方法 ('sma', 'ema', 'wilder')

**返回：**
- List[Optional[float]]: RSI 值序列（前 period+1 个为 None）

### `calculate_rsi_single(prices, period=14, method='wilder')`

计算最新 RSI 值。

**返回：**
- Optional[float]: 最新 RSI 值，数据不足返回 None

### `RSICalculator(period=14, method='wilder')`

增量式 RSI 计算器类。

**方法：**
- `update(price)`: 添加新价格，返回当前 RSI
- `reset()`: 重置计算器
- `current_rsi`: 当前 RSI 值属性

### `detect_divergence(prices, rsi_values, lookback=5)`

检测 RSI 背离。

**返回：**
- List[dict]: 背离信号列表，每项包含 type、index、message

### `generate_signals(rsi_values, oversold=30.0, overbought=70.0)`

根据 RSI 生成交易信号。

**返回：**
- List[dict]: 信号列表

### `calculate_stoch_rsi(prices, rsi_period=14, stoch_period=14)`

计算 Stochastic RSI。

**返回：**
- Tuple[List[Optional[float]], List[Optional[float]]]: (K值列表, D值列表)

### 工具函数

```python
# 格式化 RSI 显示
rsi_to_string(72.5, precision=1)  # "RSI: 72.5 (超买)"

# 验证 RSI 值
validate_rsi(50.0)  # True

# 获取 RSI 区域
get_rsi_zone(25.0)  # "oversold"
```

## RSI 区域说明

| 区域 | RSI 值 | 说明 |
|------|--------|------|
| deep_oversold | 0-20 | 深度超卖 |
| oversold | 20-30 | 超卖区 |
| bearish | 30-40 | 偏空 |
| neutral | 40-60 | 中性 |
| bullish | 60-70 | 偏多 |
| overbought | 70-80 | 超买区 |
| deep_overbought | 80-100 | 深度超买 |

## 测试

```bash
python rsi_utils_test.py
```

**测试覆盖：**
- 43 个测试用例
- 100% 通过率 ✅

## 许可证

MIT License

---

**最后更新**: 2026-05-23