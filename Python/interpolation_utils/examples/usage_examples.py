"""
Interpolation Utils - 使用示例

展示各种插值方法的使用场景和实际应用。
"""

import sys
import os
import math

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    linear_interpolate,
    lagrange_interpolate,
    newton_interpolate,
    piecewise_linear_interpolate,
    idw_interpolate,
    bilinear_interpolate,
    trilinear_interpolate,
    nearest_neighbor_interpolate,
    akima_interpolate,
    cubic_spline_interpolate,
    polynomial_fit,
    evaluate_polynomial,
    Interpolator,
    BilinearInterpolator,
    interpolate_2d_grid,
)


def example_1_basic_linear():
    """示例 1: 基本线性插值"""
    print("=" * 60)
    print("示例 1: 基本线性插值")
    print("=" * 60)
    
    # 温度测量数据
    temps = [(0, 15), (6, 18), (12, 25), (18, 22), (24, 16)]
    print(f"\n24小时温度数据 (小时, 温度℃):")
    for hour, temp in temps:
        print(f"  {hour}时: {temp}℃")
    
    # 查询上午9点的温度
    result = linear_interpolate(temps, 9)
    print(f"\n上午9点的插值温度: {result:.1f}℃")
    
    # 查询多个时间点
    print("\n多个时间点的插值温度:")
    for hour in [3, 9, 15, 21]:
        temp = linear_interpolate(temps, hour)
        print(f"  {hour}时: {temp:.1f}℃")
    
    print()


def example_2_stock_price():
    """示例 2: 股票价格插值"""
    print("=" * 60)
    print("示例 2: 股票价格插值")
    print("=" * 60)
    
    # 每日收盘价
    prices = [
        (1, 100),   # 第1天
        (2, 105),
        (3, 103),
        (5, 108),   # 第4天数据缺失
        (7, 110),   # 第6天数据缺失
    ]
    
    print("\n已知收盘价 (天, 价格):")
    for day, price in prices:
        print(f"  第{day}天: ${price}")
    
    # 使用分段线性插值填充缺失数据
    print("\n缺失数据的插值估计:")
    interp = Interpolator(prices, method='linear')
    
    missing_days = [4, 6]
    for day in missing_days:
        price = interp.interpolate(day)
        print(f"  第{day}天: ${price:.2f}")
    
    # 使用 IDW 方法（考虑更多点的权重）
    print("\n使用反距离加权插值:")
    for day in missing_days:
        price = idw_interpolate(prices, day, power=2)
        print(f"  第{day}天: ${price:.2f}")
    
    print()


def example_3_temperature_grid():
    """示例 3: 2D 温度网格"""
    print("=" * 60)
    print("示例 3: 2D 温度网格插值")
    print("=" * 60)
    
    # 房间温度测量网格
    # 假设 4x4 米的房间，在四个角测量温度
    corner_temps = [
        (0, 0, 20),  # (x米, y米, 温度℃)
        (4, 0, 22),
        (0, 4, 24),
        (4, 4, 26),
    ]
    
    print("\n房间角落温度测量:")
    print("  左下(0,0): 20℃ | 右下(4,0): 22℃")
    print("  左上(0,4): 24℃ | 右上(4,4): 26℃")
    
    # 查询房间中心温度
    center_temp = bilinear_interpolate(corner_temps, 2, 2)
    print(f"\n房间中心(2, 2)温度: {center_temp:.1f}℃")
    
    # 查询其他位置
    positions = [(1, 1), (3, 1), (1, 3), (3, 3)]
    print("\n其他位置温度:")
    for x, y in positions:
        temp = bilinear_interpolate(corner_temps, x, y)
        print(f"  ({x}, {y}): {temp:.1f}℃")
    
    print()


def example_4_3d_volume():
    """示例 4: 3D 体积数据"""
    print("=" * 60)
    print("示例 4: 3D 体积数据插值")
    print("=" * 60)
    
    # MRI 体积数据（立方体角点）
    # 假设一个 2x2x2 的立方体区域的密度值
    density_data = [
        (0, 0, 0, 100),   # 左下后
        (2, 0, 0, 110),   # 右下后
        (0, 2, 0, 120),   # 左上后
        (2, 2, 0, 130),   # 右上后
        (0, 0, 2, 140),   # 左下前
        (2, 0, 2, 150),   # 右下前
        (0, 2, 2, 160),   # 左上前
        (2, 2, 2, 170),   # 右上前
    ]
    
    print("\n立方体角点密度值:")
    for x, y, z, d in density_data:
        print(f"  ({x}, {y}, {z}): {d}")
    
    # 查询中心点密度
    center = trilinear_interpolate(density_data, 1, 1, 1)
    print(f"\n中心点(1, 1, 1)密度: {center:.1f}")
    
    print()


def example_5_polynomial_regression():
    """示例 5: 多项式拟合"""
    print("=" * 60)
    print("示例 5: 多项式拟合")
    print("=" * 60)
    
    # 销售数据
    sales = [
        (1, 100),   # 第1月
        (2, 120),
        (3, 150),
        (4, 180),
        (5, 230),
        (6, 300),
    ]
    
    print("\n销售数据 (月, 销量):")
    for month, sale in sales:
        print(f"  第{month}月: {sale}")
    
    # 二次多项式拟合
    coeffs = polynomial_fit(sales, 2)
    print(f"\n二次拟合系数: {[round(c, 2) for c in coeffs]}")
    print("拟合公式: y = {:.2f} + {:.2f}x + {:.2f}x²".format(*coeffs))
    
    # 预测未来销量
    print("\n预测销量:")
    for month in [7, 8, 9]:
        predicted = evaluate_polynomial(coeffs, month)
        print(f"  第{month}月: {int(predicted)}")
    
    print()


def example_6_interpolator_class():
    """示例 6: Interpolator 类使用"""
    print("=" * 60)
    print("示例 6: Interpolator 类使用")
    print("=" * 60)
    
    # 物体运动轨迹数据
    trajectory = [
        (0, 0),     # t=0, 位置=0
        (1, 5),     # t=1, 位置=5
        (2, 10),    # t=2, 位置=10
        (3, 12),    # t=3, 位置=12 (减速)
        (4, 13),    # t=4, 位置=13
    ]
    
    print("\n运动轨迹数据 (时间秒, 位置米):")
    for t, pos in trajectory:
        print(f"  t={t}s: pos={pos}m")
    
    # 使用不同插值方法
    methods = ['linear', 'cubic_spline', 'akima']
    query_time = 2.5
    
    print(f"\n在 t={query_time}s 时不同方法的插值结果:")
    for method in methods:
        interp = Interpolator(trajectory, method=method)
        pos = interp.interpolate(query_time)
        print(f"  {method}: {pos:.2f}m")
    
    # 批量查询
    interp = Interpolator(trajectory, method='cubic_spline')
    times = [0.5, 1.5, 2.5, 3.5]
    positions = interp.interpolate_batch(times)
    
    print("\n批量查询 (三次样条):")
    for t, pos in zip(times, positions):
        print(f"  t={t}s: pos={pos:.2f}m")
    
    print()


def example_7_image_scaling():
    """示例 7: 图像缩放概念"""
    print("=" * 60)
    print("示例 7: 图像缩放概念演示")
    print("=" * 60)
    
    # 简化的图像像素网格 (3x3)
    # 假设这是一个灰度图像
    x_coords = [0, 1, 2]
    y_coords = [0, 1, 2]
    pixels = [
        [0, 50, 100],     # 第一行
        [25, 75, 125],    # 第二行
        [50, 100, 150],   # 第三行
    ]
    
    print("\n原始图像像素值 (3x3):")
    for row in pixels:
        print("  " + " ".join(f"{p:3d}" for p in row))
    
    # 创建插值器
    interp = interpolate_2d_grid(x_coords, y_coords, pixels, method='bilinear')
    
    # 缩放到 5x5（在原始像素之间插值）
    print("\n缩放后图像像素值 (5x5，使用双线性插值):")
    scaled = []
    for i in range(5):
        y = i * 0.5
        row = []
        for j in range(5):
            x = j * 0.5
            pixel = interp(x, y)
            row.append(int(pixel))
        scaled.append(row)
        print("  " + " ".join(f"{p:3d}" for p in row))
    
    # 最近邻插值对比
    interp_nn = interpolate_2d_grid(x_coords, y_coords, pixels, method='nearest')
    
    print("\n缩放后图像像素值 (5x5，使用最近邻插值):")
    for i in range(5):
        y = i * 0.5
        row = []
        for j in range(5):
            x = j * 0.5
            pixel = interp_nn(x, y)
            row.append(int(pixel))
        print("  " + " .".join(f"{p:3d}" for p in row))
    
    print()


def example_8_scientific_data():
    """示例 8: 科学数据处理"""
    print("=" * 60)
    print("示例 8: 科学数据处理")
    print("=" * 60)
    
    # 实验测量数据 (某种化学反应的温度-产率关系)
    experiment_data = [
        (25, 10),    # 25℃ -> 10%产率
        (30, 15),
        (35, 25),
        (40, 45),
        (45, 70),
        (50, 85),
        (55, 95),
    ]
    
    print("\n实验数据 (温度℃, 产率%):")
    for temp, yield_rate in experiment_data:
        print(f"  {temp}℃: {yield_rate}%")
    
    # 查询中间温度的产率
    print("\n使用不同插值方法估计产率:")
    
    temps_to_query = [32, 38, 42, 48, 53]
    
    for method in ['linear', 'cubic_spline', 'akima', 'lagrange']:
        interp = Interpolator(experiment_data, method=method)
        results = interp.interpolate_batch(temps_to_query)
        print(f"\n{method} 方法:")
        for temp, yield_rate in zip(temps_to_query, results):
            print(f"  {temp}℃: {yield_rate:.1f}%")
    
    print()


def example_9_comparing_methods():
    """示例 9: 比较不同插值方法"""
    print("=" * 60)
    print("示例 9: 不同插值方法比较")
    print("=" * 60)
    
    # 创建一些数据点（包含噪声）
    points = [(0, 0), (1, 1.1), (2, 3.8), (3, 8.9), (4, 16)]
    
    print("原始数据点:")
    for x, y in points:
        print(f"  ({x}, {y:.1f})")
    
    # 在每个点之间查询 5 个值
    query_points = []
    for i in range(len(points) - 1):
        for j in range(1, 6):
            query_points.append(points[i][0] + j * 0.2)
    
    print("\n插值结果比较:")
    
    methods = ['linear', 'lagrange', 'cubic_spline', 'akima', 'idw']
    
    # 计算所有方法的值
    results = {}
    for method in methods:
        interp = Interpolator(points, method=method)
        results[method] = interp.interpolate_batch(query_points[:10])
    
    # 打印前 10 个查询点
    print("\nx值 | linear | lagrange | spline | akima | idw")
    print("-" * 60)
    for i, x in enumerate(query_points[:10]):
        vals = [results[m][i] for m in methods]
        print(f"{x:.1f} | {vals[0]:.2f} | {vals[1]:.2f} | {vals[2]:.2f} | {vals[3]:.2f} | {vals[4]:.2f}")
    
    print()


def example_10_real_world_scenario():
    """示例 10: 实际场景 - 路线规划"""
    print("=" * 60)
    print("示例 10: 实际场景 - GPS轨迹平滑")
    print("=" * 60)
    
    # GPS 轨迹点（有些噪声）
    gps_points = [
        (0, 0),      # 起点
        (5, 4.8),    # 第一段（略有偏差）
        (10, 9.5),   # 第二段
        (15, 14.2),  # 第三段（偏差更大）
        (20, 20),    # 终点
    ]
    
    print("原始 GPS 轨迹点 (时间秒, 位置米):")
    for t, pos in gps_points:
        print(f"  t={t}s: pos={pos:.1f}m")
    
    # 使用 Akima 插值平滑轨迹
    interp = Interpolator(gps_points, method='akima')
    
    # 生成平滑轨迹
    smooth_times = [i for i in range(21)]
    smooth_positions = interp.interpolate_batch(smooth_times)
    
    print("\n平滑后的轨迹:")
    for t, pos in zip(smooth_times, smooth_positions):
        if t % 5 == 0:
            print(f"  t={t}s: pos={pos:.2f}m")
    
    # 计算速度（位置的导数）
    print("\n估计的速度:")
    for i in range(1, len(smooth_times)):
        v = (smooth_positions[i] - smooth_positions[i-1])
        if smooth_times[i] % 5 == 0:
            print(f"  t={smooth_times[i]}s: v={v:.2f}m/s")
    
    print()


def run_all_examples():
    """运行所有示例"""
    print("\n")
    print("*" * 60)
    print(" Interpolation Utils 使用示例")
    print("*" * 60)
    print()
    
    example_1_basic_linear()
    example_2_stock_price()
    example_3_temperature_grid()
    example_4_3d_volume()
    example_5_polynomial_regression()
    example_6_interpolator_class()
    example_7_image_scaling()
    example_8_scientific_data()
    example_9_comparing_methods()
    example_10_real_world_scenario()
    
    print("*" * 60)
    print(" 示例演示完成！")
    print("*" * 60)


if __name__ == "__main__":
    run_all_examples()