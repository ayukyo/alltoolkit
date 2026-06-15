# Time Series Utils 📈

时间序列分析工具，提供滚动统计、平滑、趋势检测、异常检测等功能。

## 特性

- ✅ **滚动统计** - 移动平均/标准差/极值
- ✅ **指数平滑** - 一次/二次/三次指数平滑
- ✅ **趋势检测** - 线性趋势识别
- ✅ **季节性检测** - 周期性分析
- ✅ **异常检测** - 基于统计的异常识别
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from time_series_utils import rolling_mean, exponential_smoothing, detect_trend

# 滚动平均
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ma = rolling_mean(data, window=3)
print(ma)  # [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# 指数平滑
smoothed = exponential_smoothing(data, alpha=0.3)

# 趋势检测
trend = detect_trend(data)
print(trend)  # 'increasing'/'decreasing'/'stable'
```

## API 参考

| 函数 | 说明 |
|------|------|
| `rolling_mean(data, window)` | 滚动平均 |
| `rolling_std(data, window)` | 滚动标准差 |
| `exponential_smoothing(data, alpha)` | 指数平滑 |
| `double_exponential_smoothing(data, alpha, beta)` | 二次平滑 |
| `detect_trend(data)` | 趋势检测 |
| `detect_seasonality(data)` | 季节性检测 |
| `detect_anomalies(data, threshold)` | 异常检测 |
