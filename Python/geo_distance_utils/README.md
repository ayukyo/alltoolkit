# Geographic Distance Utilities

地理位置距离计算工具模块，零外部依赖，纯 Python 标准库实现。

## 功能特性

### 📍 距离计算
- **Haversine 公式** - 球面地球距离（快速、近似）
- **Vincenty 公式** - 椭球地球距离（精确、WGS-84）
- 支持 km、m、miles、nautical miles 多种单位

### 🧭 方向与方位
- 初始方位角计算
- 终点方位角计算
- 目标点推算（从起点+方位+距离）

### 📐 坐标操作
- 中点坐标计算
- 大圆路径插值
- 边界框生成（半径搜索）
- 坐标验证与规范化

### 🔷 多边形操作
- 点在多边形内检测（射线投射算法）
- 多边形面积计算（球面）

### 📝 格式转换
- 十进制度 ↔ 度分秒 (DMS) 转换
- 人性化坐标字符串输出

### 🔄 单位转换
- km ↔ miles ↔ nautical ↔ m
- 统一转换函数

### 📊 批量操作
- 查找最近点
- 计算到所有目标的距离
- 半径范围内搜索

## 快速开始

```python
from geo_distance_utils import (
    haversine_distance,
    vincenty_distance,
    initial_bearing,
    destination_point,
    coordinate_to_string
)

# 北京到上海的距离
beijing = (39.9042, 116.4074)
shanghai = (31.2304, 121.4737)

print(f"Haversine: {haversine_distance(beijing, shanghai):.2f} km")
print(f"Vincenty: {vincenty_distance(beijing, shanghai):.2f} km")
print(f"方位角: {initial_bearing(beijing, shanghai):.2f}°")

# 从北京向东100km的地点
dest = destination_point(beijing, 90, 100)
print(f"目标点: {coordinate_to_string(dest)}")
```

## API 参考

### 距离计算

```python
# Haversine 距离（默认单位 km）
distance = haversine_distance((lat1, lng1), (lat2, lng2))
distance_miles = haversine_distance(coord1, coord2, unit='miles')

# Vincenty 距离（更精确）
distance = vincenty_distance(coord1, coord2)

# 统一接口
distance = distance(coord1, coord2, unit='km', method='haversine')
distance = distance(coord1, coord2, unit='m', method='vincenty')
```

### 方位角

```python
# 初始方位角（起点到终点）
bearing = initial_bearing((0, 0), (1, 0))  # 0° (北)
bearing = initial_bearing((0, 0), (0, 1))  # 90° (东)

# 终点方位角
final = final_bearing(coord1, coord2)
```

### 坐标操作

```python
# 中点
mid = midpoint_coordinate((0, 0), (10, 10))

# 目标点（起点 + 方位 + 距离）
dest = destination_point((0, 0), 90, 111.19)  # 东行约1度

# 边界框（半径搜索）
bbox = bounding_box((39.9, 116.4), 50)  # 50km范围
min_coord, max_coord = bbox

# 坐标验证
is_valid = is_valid_coordinate(39.9, 116.4)
normalized = normalize_coordinate(39.9, 200)  # lng规范化到[-180,180]
```

### 多边形

```python
# 点在多边形内
polygon = [(0, 0), (0, 10), (10, 10), (10, 0)]
inside = point_in_polygon((5, 5), polygon)  # True
inside = point_in_polygon((15, 5), polygon)  # False

# 多边形面积
area = polygon_area_km2(polygon)  # km²
```

### 路径

```python
# 路径插值
points = interpolate_path((0, 0), (0, 10), 5)  # 生成5个中间点

# 路径总距离
total = total_path_distance([(0, 0), (0, 1), (0, 2)])

# 最近点（路径上）
nearest, dist, idx = nearest_point_on_path(point, path)
```

### 格式转换

```python
# 十进制 → DMS
dms = decimal_to_dms((39.9042, 116.4074))
# {'lat': {'degrees': 39, 'minutes': 54, 'seconds': 15.12, 'direction': 'N'},
#  'lng': {'degrees': 116, 'minutes': 24, 'seconds': 26.64, 'direction': 'E'}}

# DMS → 十进制
coord = dms_to_decimal(
    {'degrees': 39, 'minutes': 54, 'seconds': 15.12, 'direction': 'N'},
    {'degrees': 116, 'minutes': 24, 'seconds': 26.64, 'direction': 'E'}
)

# 人性化字符串
s1 = coordinate_to_string((39.9042, 116.4074))  # '39.9042°N, 116.4074°E'
s2 = coordinate_to_string((39.9042, 116.4074), format='dms')  # '39°54'15"N, 116°24'26"E'
s3 = coordinate_to_string((39.9042, 116.4074), format='dm')   # '39°54.25'N, 116°24.44'E'
```

### 单位转换

```python
# 单独转换函数
miles = km_to_miles(100)       # 62.137
nautical = km_to_nautical(100) # 53.996
m = km_to_m(1)                 # 1000

# 统一转换
dist = convert_distance(100, 'km', 'miles')
dist = convert_distance(100, 'miles', 'nautical')
```

### 批量操作

```python
candidates = [(40, 116), (35, 117), (30, 120)]

# 查找最近
idx, dist, coord = find_nearest((39, 116), candidates)

# 计算所有距离
distances = distances_to_all((0, 0), candidates)

# 半径范围内
results = within_radius((0, 0), candidates, 200)  # 200km内
# 返回 [(index, distance, coordinate), ...]
```

## 常数

```python
EARTH_RADIUS_KM = 6371.0          # 平均地球半径 (km)
EARTH_RADIUS_M = 6371000.0        # 平均地球半径 (m)
EARTH_RADIUS_MILES = 3958.8       # 平均地球半径 (miles)
EARTH_RADIUS_NAUTICAL = 3440.065  # 平均地球半径 (nautical)

WGS84_SEMI_MAJOR = 6378137.0      # WGS-84 长半轴 (m)
WGS84_SEMI_MINOR = 6356752.314245 # WGS-84 短半轴 (m)
WGS84_FLATTENING = 1/298.257223563 # WGS-84 扁率
```

## 精度说明

| 方法 | 精度 | 适用场景 |
|------|------|----------|
| Haversine | ~0.5% | 快速计算、短距离 |
| Vincenty | ~0.5mm | 精确测量、长距离 |

**注意**: Vincenty 算法在某些接近对跖点的情况可能无法收敛，此时返回 0。

## 测试

```bash
python test.py
```

共 60+ 测试用例，覆盖所有主要功能。

## 零依赖

纯 Python 标准库实现，无需安装任何第三方包。

## 许可证

MIT License