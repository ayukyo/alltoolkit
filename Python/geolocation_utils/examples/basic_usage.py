#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geolocation Utils 基本使用示例
=============================

展示地理定位工具库的基本功能。

作者: AllToolkit 自动化生成
日期: 2026-05-26
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Coordinate, DistanceUnit, Geofence,
    haversine_distance, initial_bearing, destination_point,
    bounding_box, midpoint, encode_geohash, decode_geohash,
    distance_between, bearing_to_compass, format_coordinates
)


def main():
    print("=" * 50)
    print("Geolocation Utils 基本使用示例")
    print("=" * 50)
    
    # 1. 创建坐标
    print("\n【1. 创建坐标】")
    beijing = Coordinate(39.9042, 116.4074)
    shanghai = Coordinate(31.2304, 121.4737)
    print(f"北京: {beijing}")
    print(f"上海: {shanghai}")
    
    # 2. 计算距离
    print("\n【2. 计算距离】")
    dist_km = haversine_distance(beijing, shanghai)
    dist_mi = haversine_distance(beijing, shanghai, DistanceUnit.MILES)
    print(f"北京-上海距离: {dist_km:.2f} km")
    print(f"北京-上海距离: {dist_mi:.2f} miles")
    
    # 3. 计算方位角
    print("\n【3. 计算方位角】")
    bearing = initial_bearing(beijing, shanghai)
    compass = bearing_to_compass(bearing)
    print(f"北京到上海方位角: {bearing:.1f}° ({compass})")
    
    # 4. 目的地计算
    print("\n【4. 目的地计算】")
    dest = destination_point(beijing, bearing, 500)
    print(f"从北京向上海方向走 500km: {dest}")
    
    # 5. 中点计算
    print("\n【5. 中点计算】")
    mid = midpoint(beijing, shanghai)
    print(f"北京-上海中点: {mid}")
    
    # 6. 边界框
    print("\n【6. 边界框】")
    sw, ne = bounding_box(beijing, 10)
    print(f"北京周边 10km 边界框:")
    print(f"  西南角: {sw}")
    print(f"  东北角: {ne}")
    
    # 7. Geohash
    print("\n【7. Geohash】")
    geohash = encode_geohash(beijing, 8)
    print(f"北京 Geohash (精度8): {geohash}")
    decoded, error = decode_geohash(geohash)
    print(f"解码坐标: {decoded}")
    print(f"误差范围: 纬度±{error.latitude:.4f}°, 经度±{error.longitude:.4f}°")
    
    # 8. 坐标格式化
    print("\n【8. 坐标格式化】")
    print(f"十进制度: {format_coordinates(beijing, 'decimal')}")
    print(f"度分秒:   {format_coordinates(beijing, 'dms')}")
    print(f"度分:     {format_coordinates(beijing, 'dm')}")
    
    # 9. 快捷函数
    print("\n【9. 快捷函数】")
    dist = distance_between(39.9042, 116.4074, 31.2304, 121.4737)
    print(f"快捷距离: {dist:.2f} km")
    
    # 10. 地理围栏
    print("\n【10. 地理围栏】")
    fence = Geofence.circle(beijing, 100)
    test_point = Coordinate(39.5, 116.5)
    print(f"北京 100km 围栏包含 {test_point}: {fence.contains(test_point)}")
    
    # 到边界距离
    dist_to_boundary = fence.distance_to_boundary(test_point)
    print(f"到边界距离: {dist_to_boundary:.2f} km")
    
    print("\n" + "=" * 50)
    print("示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()