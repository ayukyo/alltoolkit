# GPS Utilities - GPS 坐标工具集

全面的 GPS/地理位置处理工具，零外部依赖，纯 Python 实现。

## 功能特性

- ✅ **坐标格式转换** - DD/DMS/DDM/UTM 多格式互转
- ✅ **距离计算** - Haversine 公式，支持多种单位
- ✅ **方位角计算** - 初始方位、终点方位
- ✅ **边界框计算** - 根据中心点和半径计算边界
- ✅ **坐标解析** - 智能解析多种格式字符串
- ✅ **坐标验证** - 范围验证、区域检测
- ✅ **轨迹处理** - 总距离、平均速度计算
- ✅ **地图 URL** - Google Maps、OSM、百度地图链接生成

## 安装

```bash
# 直接使用（无需安装依赖）
from gps_utils import distance_between, format_gps
```

## 快速开始

### 基础距离计算

```python
from gps_utils import distance_between, bearing_to

# 北京到上海的距离
beijing = (39.9042, 116.4074)
shanghai = (31.2304, 121.4737)

dist = distance_between(beijing[0], beijing[1], shanghai[0], shanghai[1])
print(f"距离: {dist:.1f} km")  # 约 1068 km

# 方位角
bearing = bearing_to(beijing[0], beijing[1], shanghai[0], shanghai[1])
print(f"方位角: {bearing:.1f}°")  # 约 124°（南偏东）
```

### 坐标格式转换

```python
from gps_utils import dd_to_dms, dms_to_dd, format_gps

# 十进制度转度分秒
lat = 39.9042
dms = dd_to_dms(lat)
print(f"度分秒: {dms[0]}°{dms[1]}'{dms[2]}\"")  # 39°54'15.12"

# 度分秒转十进制度
dd = dms_to_dd(39, 54, 15.12, 'N')
print(f"十进制度: {dd:.4f}°")  # 39.9042°

# 格式化显示
formatted = format_gps(39.9042, 116.4074, 'dms')
print(formatted)  # 39°54'15.12"N, 116°24'26.64"E
```

### 坐标对象

```python
from gps_utils import Coordinate, create_coordinate

# 创建坐标对象
coord = create_coordinate(39.9042, 116.4074, altitude=50.0)

# 查看属性
print(f"纬度: {coord.latitude}")
print(f"半球: {coord.hemisphere}")  # {'lat': 'N', 'lon': 'E'}
print(f"北半球: {coord.is_north}")

# 转换为其他格式
dms = coord.to_dms()
ddm = coord.to_ddm()
```

### 边界框

```python
from gps_utils import create_bbox

# 创建 10km 边界框
bbox = create_bbox(39.9042, 116.4074, 10, 'km')

print(f"范围: {bbox.min_lat} - {bbox.max_lat}")
print(f"宽度: {bbox.width_km():.1f} km")

# 检查坐标是否在范围内
inside = create_coordinate(39.95, 116.45)
print(f"是否包含: {bbox.contains(inside)}")
```

### 坐标解析

```python
from gps_utils import parse_gps, GPSParser

# 解析多种格式
formats = [
    "39°54'15\"N",       # 度分秒
    "39°54.25'N",        # 度分
    "39.9042°N",         # 十进制度
    "3954.2500,N",       # NMEA 格式
]

for f in formats:
    value, direction = parse_gps(f)
    print(f"{f} -> {value:.4f}°")

# 解析坐标对
coord = GPSParser.parse_coordinate_pair("39.9042, 116.4074")
```

### 地图 URL 生成

```python
from gps_utils import maps_url, GPSFormatter

# Google Maps
url = maps_url(39.9042, 116.4074, 'google')
print(url)  # https://www.google.com/maps?q=39.9042,116.4074

# OpenStreetMap
url = maps_url(39.9042, 116.4074, 'osm')

# 百度地图
url = maps_url(39.9042, 116.4074, 'baidu')

# GeoJSON 输出
geojson = GPSFormatter.format_geojson_point(39.9042, 116.4074)
print(geojson)
```

### 轨迹处理

```python
from gps_utils import total_track_distance

# 计算轨迹总距离
track = [
    (39.9042, 116.4074),  # 北京
    (35.0, 117.0),        # 济南附近
    (31.2304, 121.4737),  # 上海
]

total = total_track_distance(track)
print(f"总距离: {total:.1f} km")
```

### 区域检测

```python
from gps_utils import is_in_region, get_region

# 检查坐标所在区域
region = get_region(39.9042, 116.4074)
print(region)  # 'china' 或 'asia'

# 检查是否在特定区域
print(is_in_region(39.9042, 116.4074, 'china'))  # True
print(is_in_region(40.7128, -74.0060, 'usa'))    # True (纽约)
```

## API 参考

### 数据类

#### `Coordinate`
- `latitude`: 纬度
- `longitude`: 经度
- `altitude`: 高度（可选）
- `is_north`: 是否北半球
- `is_east`: 是否东半球
- `hemisphere`: 半球信息
- `to_dms()`: 转度分秒
- `to_ddm()`: 转度分
- `to_dict()`: 转字典

#### `BoundingBox`
- `min_lat`, `max_lat`: 纬度范围
- `min_lon`, `max_lon`: 经度范围
- `contains(coord)`: 检查包含
- `center()`: 获取中心
- `width_km()`, `height_km()`: 尺寸

### 主要函数

| 函数 | 说明 |
|------|------|
| `distance_between(lat1, lon1, lat2, lon2, unit)` | 计算两点距离 |
| `bearing_to(lat1, lon1, lat2, lon2)` | 计算方位角 |
| `midpoint_of(lat1, lon1, lat2, lon2)` | 计算中间点 |
| `destination_from(lat, lon, bearing, distance)` | 计算终点 |
| `create_bbox(lat, lon, distance)` | 创建边界框 |
| `dd_to_dms(dd)` | 十进制度转度分秒 |
| `dms_to_dd(d, m, s, dir)` | 度分秒转十进制度 |
| `parse_gps(str)` | 解析坐标字符串 |
| `format_gps(lat, lon, format)` | 格式化坐标 |
| `validate_gps(lat, lon)` | 验证坐标 |
| `total_track_distance(coords)` | 计算轨迹距离 |
| `maps_url(lat, lon, provider)` | 生成地图 URL |

### 支持单位

- `km` - 公里（默认）
- `m` - 米
- `mi` - 英里
- `nm` - 海里

### 预定义区域

- `china` - 中国
- `usa` - 美国
- `europe` - 欧洲
- `asia` - 亚洲
- `africa` - 非洲
- `australia` - 澳大利亚
- `antarctica` - 南极洲

## 性能优化

- 相同坐标距离计算直接返回 0
- 空轨迹直接返回 0
- 使用预计算常量减少重复计算
- 边界检查快速路径

## 测试

```bash
# 运行测试
python gps_utils_test.py

# 或使用 pytest
pytest gps_utils_test.py -v
```

## 许可证

MIT License - 详见项目根目录 LICENSE 文件