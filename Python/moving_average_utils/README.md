# Moving Average Utils - 移动平均工具模块

提供多种移动平均算法实现，用于时间序列分析、信号处理、趋势预测等场景。

## 支持的移动平均类型

| 类型 | 名称 | 描述 |
|------|------|------|
| SMA | Simple Moving Average | 简单移动平均，最基础的移动平均方法 |
| EMA | Exponential Moving Average | 指数移动平均，对近期数据赋予更大权重 |
| WMA | Weighted Moving Average | 加权移动平均，线性加权 |
| CMA | Cumulative Moving Average | 累积移动平均，从开始到当前的平均 |
| TMA | Triangular Moving Average | 三角移动平均，双重平滑 |
| HMA | Hull Moving Average | Hull移动平均，减少滞后同时保持平滑 |
| KAMA | Kaufman's Adaptive MA | 自适应移动平均，根据波动性调整 |
| VWMA | Volume Weighted MA | 成交量加权移动平均 |

## 技术指标

- **MACD** - 移动平均收敛发散指标
- **Bollinger Bands** - 布林带
- **ATR** - 平均真实波幅

## 安装使用

```python
from moving_average_utils.mod import (
    simple_moving_average,
    exponential_moving_average,
    bollinger_bands,
    MovingAverage,
)
```

## 快速开始

### 基础移动平均

```python
data = [10, 12, 14, 13, 15, 17, 16, 18, 20, 19]

# 简单移动平均
sma = simple_moving_average(data, window=3)
# [None, None, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0]

# 指数移动平均
ema = exponential_moving_average(data, window=3)
# [None, None, 12.0, 12.67, 13.56, 14.87, 15.58, 16.72, 17.91, 18.62]

# 加权移动平均
wma = weighted_moving_average(data, window=3)
```

### 布林带

```python
upper, middle, lower = bollinger_bands(data, window=20, num_std=2.0)
```

### MACD

```python
macd_line, signal_line, histogram = moving_average_convergence_divergence(
    data, fast_period=12, slow_period=26, signal_period=9
)
```

### 流式数据处理

```python
ma = MovingAverage(window=5, method='ema')

for value in data_stream:
    current_ma = ma.update(value)
    print(f"值: {value}, EMA: {current_ma}")

# 获取当前值
print(f"当前EMA: {ma.current}")
```

### 滚动统计量

```python
stats = rolling_statistics(data, window=5, stats=['mean', 'std', 'min', 'max'])
# {'mean': [...], 'std': [...], 'min': [...], 'max': [...]}
```

## 零外部依赖

纯 Python 实现，无需安装任何外部包。

## 运行测试

```bash
python -m pytest moving_average_utils_test.py -v
```

## 应用场景

- 📈 股票/期货技术分析
- 🌡️ 传感器数据平滑
- 📊 时间序列预测
- 🔄 信号处理滤波
- 📉 波动率分析