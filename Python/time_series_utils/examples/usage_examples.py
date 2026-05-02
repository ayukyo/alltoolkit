"""
时间序列分析工具使用示例
Time Series Analysis Utilities Examples
"""

import sys
sys.path.insert(0, '..')

from time_series_utils.mod import (
    # 滚动窗口
    RollingWindow, rolling_mean, rolling_std, rolling_min, rolling_max,
    # 移动平均
    simple_moving_average, weighted_moving_average, exponential_moving_average,
    ema_from_period,
    # 指数平滑
    single_exponential_smoothing, double_exponential_smoothing,
    triple_exponential_smoothing,
    # 趋势检测
    detect_trend, calculate_trend_slope, linear_regression, TrendDirection,
    # 季节性检测
    detect_seasonality, autocorrelation,
    # 异常检测
    zscore_anomaly_detection, iqr_anomaly_detection, moving_average_anomaly_detection,
    # 分解
    decompose_time_series,
    # 预测
    forecast_ses, forecast_holt, forecast_holt_winters,
    # 差分与平稳性
    difference, is_stationary,
    # 其他
    find_peaks, find_valleys, calculate_volatility, percentage_change,
    cumulative_return, resample, fill_missing
)


def example_rolling_statistics():
    """示例：滚动统计计算"""
    print("=" * 50)
    print("示例 1: 滚动统计")
    print("=" * 50)
    
    # 股票价格数据
    prices = [100, 102, 98, 105, 103, 107, 104, 110, 108, 112,
              109, 115, 113, 118, 116, 120, 118, 122, 120, 125]
    
    # 计算滚动平均值（5日均线）
    ma5 = simple_moving_average(prices, 5)
    print(f"5日移动平均线: {ma5[-5:]}")
    
    # 计算滚动标准差（波动率）
    volatility = rolling_std(prices, 5)
    print(f"5日波动率: {volatility[-5:]}")
    
    # 使用 RollingWindow 类进行增量计算
    print("\n增量计算滚动统计:")
    rw = RollingWindow(5)
    for price in prices[-3:]:
        stats = rw.add(price)
        print(f"  价格: {price}, 均值: {stats.mean:.2f}, 标准差: {stats.std:.2f}, "
              f"最小: {stats.min}, 最大: {stats.max}")


def example_moving_averages():
    """示例：各种移动平均"""
    print("\n" + "=" * 50)
    print("示例 2: 移动平均类型比较")
    print("=" * 50)
    
    data = [10, 12, 14, 11, 13, 15, 12, 14, 16, 13, 15, 17, 14, 16, 18]
    
    # 简单移动平均
    sma = simple_moving_average(data, 5)
    print(f"SMA(5): {sma[-5:]}")
    
    # 加权移动平均
    wma = weighted_moving_average(data, 5)
    print(f"WMA(5): {wma[-5:]}")
    
    # 指数移动平均
    ema = exponential_moving_average(data, alpha=0.2)
    print(f"EMA(α=0.2): {ema[-5:]}")
    
    # 从周期计算 EMA
    ema5 = ema_from_period(data, 5)
    print(f"EMA(5): {ema5[-5:]}")


def example_exponential_smoothing():
    """示例：指数平滑"""
    print("\n" + "=" * 50)
    print("示例 3: 指数平滑")
    print("=" * 50)
    
    # 有趋势的数据
    trending_data = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]
    
    # 单次指数平滑（适用于无趋势数据）
    ses = single_exponential_smoothing(trending_data, alpha=0.3)
    print(f"单次指数平滑: {ses[-5:]}")
    
    # 双重指数平滑（适用于有趋势数据）
    des = double_exponential_smoothing(trending_data, alpha=0.3, beta=0.1)
    print(f"双重指数平滑: {des[-5:]}")
    
    # 有季节性的数据
    seasonal_data = [100, 150, 120, 80, 100, 150, 120, 80, 100, 150, 120, 80]
    
    # 三次指数平滑（适用于有趋势和季节性的数据）
    tes = triple_exponential_smoothing(seasonal_data, period=4, 
                                        alpha=0.3, beta=0.1, gamma=0.1)
    print(f"三次指数平滑: {tes[-5:]}")


def example_trend_detection():
    """示例：趋势检测"""
    print("\n" + "=" * 50)
    print("示例 4: 趋势检测")
    print("=" * 50)
    
    # 上升趋势数据
    upward = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
    trend = detect_trend(upward)
    print(f"数据 {upward[:5]}... 的趋势: {trend.value}")
    
    # 下降趋势数据
    downward = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    trend = detect_trend(downward)
    print(f"数据 {downward[:5]}... 的趋势: {trend.value}")
    
    # 平稳数据
    flat = [50, 51, 49, 50, 51, 49, 50, 51, 49, 50]
    trend = detect_trend(flat)
    print(f"数据 {flat[:5]}... 的趋势: {trend.value}")
    
    # 计算趋势斜率
    slope = calculate_trend_slope(upward)
    print(f"上升趋势斜率: {slope:.2f}")
    
    # 线性回归
    slope, intercept, r_squared = linear_regression(upward)
    print(f"线性回归: 斜率={slope:.2f}, 截距={intercept:.2f}, R²={r_squared:.4f}")


def example_seasonality_detection():
    """示例：季节性检测"""
    print("\n" + "=" * 50)
    print("示例 5: 季节性检测")
    print("=" * 50)
    
    # 有季节性的销售数据（季度周期）
    sales = [100, 150, 200, 150, 100, 150, 200, 150, 100, 150, 200, 150]
    
    period = detect_seasonality(sales, max_period=6)
    print(f"检测到的季节周期: {period}")
    
    # 自相关分析
    print("\n自相关系数:")
    for lag in range(1, 6):
        autocorr = autocorrelation(sales, lag)
        print(f"  滞后 {lag}: {autocorr:.4f}")


def example_anomaly_detection():
    """示例：异常检测"""
    print("\n" + "=" * 50)
    print("示例 6: 异常检测")
    print("=" * 50)
    
    # 传感器数据（包含异常值）
    sensor_data = [20.1, 20.3, 20.2, 20.4, 20.3, 35.0, 20.2, 20.1, 
                   20.3, 20.2, 20.4, 20.1, 5.0, 20.3, 20.2]
    
    print("原始数据:", sensor_data)
    
    # Z-Score 异常检测
    print("\nZ-Score 异常检测:")
    zscore_results = zscore_anomaly_detection(sensor_data, threshold=2.0)
    for r in zscore_results:
        if r.is_anomaly:
            print(f"  索引 {r.index}: 值={r.value}, Z-Score={r.score:.2f} ⚠️ 异常")
    
    # IQR 异常检测
    print("\nIQR 异常检测:")
    iqr_results = iqr_anomaly_detection(sensor_data, k=1.5)
    for r in iqr_results:
        if r.is_anomaly:
            print(f"  索引 {r.index}: 值={r.value} ⚠️ 异常")
    
    # 移动平均异常检测
    print("\n移动平均异常检测:")
    ma_results = moving_average_anomaly_detection(sensor_data, window_size=3, threshold=2.0)
    for r in ma_results:
        if r.is_anomaly:
            print(f"  索引 {r.index}: 值={r.value}, 偏离={r.score:.2f}σ ⚠️ 异常")


def example_decomposition():
    """示例：时间序列分解"""
    print("\n" + "=" * 50)
    print("示例 7: 时间序列分解")
    print("=" * 50)
    
    # 有趋势和季节性的数据
    data = [100, 120, 140, 120, 110, 130, 150, 130, 120, 140, 160, 140]
    
    result = decompose_time_series(data, period=4)
    
    print("原始数据:")
    print(f"  {data}")
    print("\n趋势成分:")
    print(f"  {[round(x, 1) for x in result.trend]}")
    print("\n季节性成分:")
    print(f"  {[round(x, 1) for x in result.seasonal]}")
    print("\n残差成分:")
    print(f"  {[round(x, 1) for x in result.residual]}")


def example_forecasting():
    """示例：预测"""
    print("\n" + "=" * 50)
    print("示例 8: 预测")
    print("=" * 50)
    
    # 销售数据
    sales = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
    
    # 单次指数平滑预测
    ses_forecast = forecast_ses(sales, alpha=0.3, horizon=3)
    print(f"SES 预测未来3期: {[round(x, 2) for x in ses_forecast]}")
    
    # Holt 方法预测（有趋势）
    holt_forecast = forecast_holt(sales, alpha=0.3, beta=0.1, horizon=3)
    print(f"Holt 预测未来3期: {[round(x, 2) for x in holt_forecast]}")
    
    # 有季节性的数据
    seasonal_sales = [100, 150, 200, 150, 100, 150, 200, 150, 100, 150, 200, 150]
    
    # Holt-Winters 预测
    hw_forecast = forecast_holt_winters(seasonal_sales, period=4, 
                                         alpha=0.3, beta=0.1, gamma=0.1, 
                                         horizon=4)
    print(f"Holt-Winters 预测未来4期: {[round(x, 2) for x in hw_forecast]}")


def example_difference_stationarity():
    """示例：差分与平稳性"""
    print("\n" + "=" * 50)
    print("示例 9: 差分与平稳性检验")
    print("=" * 50)
    
    # 非平稳数据（有趋势）
    non_stationary = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
    
    print(f"原始数据: {non_stationary[:5]}...")
    print(f"是否平稳: {is_stationary(non_stationary)}")
    
    # 一阶差分
    diff1 = difference(non_stationary, order=1)
    print(f"\n一阶差分: {diff1}")
    print(f"是否平稳: {is_stationary(diff1)}")
    
    # 二阶差分
    diff2 = difference(non_stationary, order=2)
    print(f"\n二阶差分: {diff2}")


def example_peaks_valleys():
    """示例：峰值谷值检测"""
    print("\n" + "=" * 50)
    print("示例 10: 峰值与谷值检测")
    print("=" * 50)
    
    # 股价数据
    prices = [100, 105, 110, 108, 103, 98, 95, 100, 108, 115, 
              112, 108, 105, 110, 118, 125, 120, 115, 118, 122]
    
    print(f"股价数据: {prices}")
    
    # 找峰值
    peaks = find_peaks(prices, min_distance=2)
    print(f"\n峰值位置: {peaks}")
    print(f"峰值价格: {[prices[i] for i in peaks]}")
    
    # 找谷值
    valleys = find_valleys(prices, min_distance=2)
    print(f"\n谷值位置: {valleys}")
    print(f"谷值价格: {[prices[i] for i in valleys]}")


def example_financial_analysis():
    """示例：金融分析"""
    print("\n" + "=" * 50)
    print("示例 11: 金融分析应用")
    print("=" * 50)
    
    # 每日股价
    prices = [100, 102, 99, 103, 101, 105, 108, 106, 110, 107,
              112, 115, 113, 118, 116, 120, 118, 122, 120, 125]
    
    print("股价数据分析:")
    print(f"  最终价格: {prices[-1]}")
    print(f"  最高价: {max(prices)}")
    print(f"  最低价: {min(prices)}")
    
    # 计算收益率
    returns = percentage_change(prices)
    print(f"\n每日收益率 (%): {[round(r, 2) for r in returns[-5:]]}")
    
    # 累计收益
    total_return = cumulative_return(prices)
    print(f"累计收益率: {total_return:.2f}%")
    
    # 波动率（滚动标准差）
    volatility = calculate_volatility(prices, window_size=5)
    print(f"5日波动率: {[round(v, 2) for v in volatility[-5:]]}")
    
    # 技术指标：短期和长期均线
    ma5 = simple_moving_average(prices, 5)
    ma10 = simple_moving_average(prices, 10)
    
    print(f"\n5日均线: {ma5[-1]:.2f}")
    print(f"10日均线: {ma10[-1]:.2f}")
    
    # 均线交叉信号
    if ma5[-1] > ma10[-1] and ma5[-2] <= ma10[-2]:
        print("📈 金叉信号 - 看涨")
    elif ma5[-1] < ma10[-1] and ma5[-2] >= ma10[-2]:
        print("📉 死叉信号 - 看跌")


def example_data_resampling():
    """示例：数据重采样"""
    print("\n" + "=" * 50)
    print("示例 12: 数据重采样")
    print("=" * 50)
    
    # 每小时温度数据
    hourly_temp = [20, 21, 22, 23, 24, 25, 26, 27, 28, 27, 26, 25, 
                   24, 23, 22, 21, 20, 19, 18, 18, 17, 17, 18, 19]
    
    print(f"每小时温度数据 (24h): {hourly_temp}")
    
    # 重采样为每6小时
    temp_6h = resample(hourly_temp, factor=6, method='mean')
    print(f"\n每6小时平均温度: {[round(t, 1) for t in temp_6h]}")
    
    # 最高温度
    temp_max = resample(hourly_temp, factor=6, method='max')
    print(f"每6小时最高温度: {temp_max}")
    
    # 最低温度
    temp_min = resample(hourly_temp, factor=6, method='min')
    print(f"每6小时最低温度: {temp_min}")


def example_fill_missing():
    """示例：填充缺失值"""
    print("\n" + "=" * 50)
    print("示例 13: 填充缺失值")
    print("=" * 50)
    
    # 有缺失值的数据
    data = [10.0, None, 12.0, None, None, 15.0, 16.0, None, 18.0]
    
    print(f"原始数据: {data}")
    
    # 前向填充
    forward_filled = fill_missing(data, method='forward')
    print(f"前向填充: {forward_filled}")
    
    # 后向填充
    backward_filled = fill_missing(data, method='backward')
    print(f"后向填充: {backward_filled}")
    
    # 线性插值
    linear_filled = fill_missing(data, method='linear')
    print(f"线性插值: {[round(x, 2) for x in linear_filled]}")
    
    # 均值填充
    mean_filled = fill_missing(data, method='mean')
    print(f"均值填充: {[round(x, 2) for x in mean_filled]}")


def example_real_world_scenario():
    """示例：真实世界场景"""
    print("\n" + "=" * 50)
    print("示例 14: 真实世界场景 - 网站流量分析")
    print("=" * 50)
    
    # 24小时的网站访问量
    traffic = [120, 80, 50, 30, 20, 15, 25, 80, 200, 350, 400, 380,
               350, 320, 300, 280, 320, 400, 500, 450, 380, 300, 220, 180]
    
    print("网站24小时访问量分析:")
    
    # 1. 趋势分析
    trend = detect_trend(traffic)
    print(f"整体趋势: {trend.value}")
    
    # 2. 访问高峰
    peaks = find_peaks(traffic)
    peak_hours = [p for p in peaks]
    print(f"访问高峰时段: {peak_hours} 点")
    print(f"高峰访问量: {[traffic[i] for i in peak_hours]}")
    
    # 3. 访问低谷
    valleys = find_valleys(traffic)
    print(f"访问低谷时段: {valleys} 点")
    
    # 4. 异常检测
    anomalies = zscore_anomaly_detection(traffic, threshold=2.5)
    print(f"异常访问:")
    for a in anomalies:
        if a.is_anomaly:
            print(f"  {a.index}点: {a.value} 次访问 (Z-Score: {a.score:.2f})")
    
    # 5. 平滑处理
    smoothed = exponential_moving_average(traffic, alpha=0.2)
    print(f"\n平滑后的流量: {[round(s) for s in smoothed[:6]]}...")


if __name__ == "__main__":
    example_rolling_statistics()
    example_moving_averages()
    example_exponential_smoothing()
    example_trend_detection()
    example_seasonality_detection()
    example_anomaly_detection()
    example_decomposition()
    example_forecasting()
    example_difference_stationarity()
    example_peaks_valleys()
    example_financial_analysis()
    example_data_resampling()
    example_fill_missing()
    example_real_world_scenario()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)