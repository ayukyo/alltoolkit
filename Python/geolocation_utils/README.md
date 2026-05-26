# Geolocation Utils - 地理定位工具库

零依赖的地理坐标计算工具库，提供距离计算、方位角、地理围栏、Geohash 等功能。

## 特性

- **距离计算**: Haversine 公式计算两点间大圆距离
- **方位角**: 初始方位角、最终方位角、罗盘方向转换
- **目的地计算**: 给定起点、方位角、距离计算目标点
- **边界框**: 根据中心点和半径计算边界框
- **坐标转换**: 度分秒格式转换、十进制度转换
- **Geohash**: 编码、解码、相邻格子计算
- **地理围栏**: 圆形、多边形、矩形围栏
- **多边形操作**: 点在多边形内判断、面积计算
- **零依赖**: 纯 Python 标准库实现
- **高精度**: 基于 WGS84 椭球体模型

## 安装

```python
from geolocation_utils.mod import Coordinate, haversine_distance
```

## 快速开始

### 基本用法

```python
from geolocation_utils.mod import Coordinate, haversine_distance, initial_bearing

# 创建坐标
beijing = Coordinate(39.9042, 116.4074)
shanghai = Coordinate(31.2304, 121.4737)

# 计算距离
dist = haversine_distance(beijing, shanghai)
print(f"北京-上海距离: {dist:.2f} km")  # 约 1068 km

# 计算方位角
bearing = initial_bearing(beijing, shanghai)
print(f"方位角: {bearing:.1f}°")  # 约 161° (东南方向)
```

### 目的地计算

```python
from geolocation_utils.mod import destination_point

# 从北京出发，向东南方向走 100km
dest = destination_point(beijing, 161, 100)
print(f"目的地: {dest}")  # Coordinate(39.04, 117.23)
```

### 边界框

```python
from geolocation_utils.mod import bounding_box

# 北京周边 10km 边界框
sw, ne = bounding_box(beijing, 10)
print(f"西南角: {sw}")
print(f"东北角: {ne}")
```

### Geohash 编解码

```python
from geolocation_utils.mod import encode_geohash, decode_geohash

# 编码
geohash = encode_geohash(beijing, precision=8)
print(f"Geohash: {geohash}")  # wx4g0b1q

# 解码
coord, error = decode_geohash(geohash)
print(f"坐标: {coord}")
print(f"误差: {error}")
```

### 地理围栏

```python
from geolocation_utils.mod import Geofence

# 创建圆形围栏 (北京中心，半径 5km)
fence = Geofence.circle(beijing, 5)

# 检查点是否在围栏内
point = Coordinate(39.91, 116.42)
if fence.contains(point):
    print("点在围栏内")

# 多边形围栏
polygon = [
    Coordinate(0, 0),
    Coordinate(0, 1),
    Coordinate(1, 1),
    Coordinate(1, 0)
]
fence = Geofence.polygon(polygon)
```

### 坐标格式转换

```python
from geolocation_utils.mod import Coordinate, format_coordinates

coord = Coordinate(39.9042, 116.4074)

# 十进制度
print(format_coordinates(coord, 'decimal'))  # 39.9042°N, 116.4074°E

# 度分秒
print(format_coordinates(coord, 'dms'))  # 39°54'15.12"N, 116°24'26.64"E

# 度分
print(format_coordinates(coord, 'dm'))  # 39°54.252'N, 116°24.444'E
```

### 便捷函数

```python
from geolocation_utils.mod import distance_between, bearing_to_compass

# 快捷距离计算
dist = distance_between(39.9042, 116.4074, 31.2304, 121.4737)
print(f"{dist:.2f} km")

# 方位角转罗盘方向
print(bearing_to_compass(161))  # SSE
print(bearing_to_compass(45))   # NE
```

## API 文档

### Coordinate 类

| 属性/方法 | 说明 |
|----------|------|
| `latitude` | 纬度 |
| `longitude` | 经度 |
| `altitude` | 海拔 (可选) |
| `lat`, `lng` | 简写属性 |
| `lat_rad`, `lng_rad` | 弧度值 |
| `to_dms()` | 转度分秒 |
| `from_dms()` | 从度分秒创建 |

### 距离函数

| 函数 | 说明 |
|------|------|
| `haversine_distance(coord1, coord2, unit)` | Haversine 距离 |
| `distance_between(lat1, lng1, lat2, lng2, unit)` | 快捷距离计算 |

### 方位角函数

| 函数 | 说明 |
|------|------|
| `initial_bearing(coord1, coord2)` | 初始方位角 |
| `final_bearing(coord1, coord2)` | 最终方位角 |
| `bearing_to_compass(bearing)` | 转罗盘方向 |

### 目的地函数

| 函数 | 说明 |
|------|------|
| `destination_point(start, bearing, distance, unit)` | 目的地坐标 |
| `midpoint(coord1, coord2)` | 两点中点 |
| `interpolate(coord1, coord2, fraction)` | 按比例插值 |

### 边界函数

| 函数 | 说明 |
|------|------|
| `bounding_box(center, radius, unit)` | 边界框 |
| `is_point_in_polygon(point, polygon)` | 点在多边形内 |
| `polygon_area(polygon, unit)` | 多边形面积 |

### Geohash 函数

| 函数 | 说明 |
|------|------|
| `encode_geohash(coord, precision)` | 编码 Geohash |
| `decode_geohash(geohash)` | 解码 Geohash |
| `geohash_neighbors(geohash)` | 相邻格子 |

### Geofence 类

| 方法 | 说明 |
|------|------|
| `Geofence.circle(center, radius)` | 创建圆形围栏 |
| `Geofence.polygon(vertices)` | 创建多边形围栏 |
| `Geofence.rectangle(sw, ne)` | 创建矩形围栏 |
| `contains(point)` | 判断点是否在围栏内 |
| `distance_to_boundary(point)` | 到边界距离 |

### DistanceUnit 枚举

| 单位 | 说明 |
|------|------|
| `METERS` | 米 |
| `KILOMETERS` | 公里 |
| `MILES` | 英里 |
| `NAUTICAL_MILES` | 海里 |
| `FEET` | 英尺 |
| `YARDS` | 码 |

## 使用场景

1. **地图应用**: 计算 POI 之间的距离和方位
2. **物流配送**: 规划路线、计算配送范围
3. **位置服务**: 地理围栏触发、位置监控
4. **数据分析**: 用户分布分析、商圈分析
5. **导航系统**: 方位角计算、目的地预测
6. **地理编码**: Geohash 存储、附近搜索

## 精度说明

- 基于 WGS84 椭球体模型
- Haversine 公式适用于球面距离计算
- 对于精确测量 (< 1m)，考虑使用 Vincenty 公式
- Geohash 精度对应距离误差:
  - 1 字符: ±2500 km
  - 2 字符: ±630 km
  - 3 字符: ±78 km
  - 4 字符: ±20 km
  - 5 字符: ±2.4 km
  - 6 字符: ±0.61 km
  - 7 字符: ±76 m
  - 8 字符: ±19 m

## 作者

AllToolkit 自动化生成

## 日期

2026-05-26