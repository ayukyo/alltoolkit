# Geohash Utilities - 地理编码工具

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

零依赖、生产就绪的 Geohash 编码工具模块，用于地理坐标与 Geohash 字符串之间的转换。

## 功能特性

- **编码**：经纬度 → Geohash 字符串
- **解码**：Geohash → 经纬度边界框和中心点
- **邻居计算**：获取相邻的 8 个 Geohash（用于邻近搜索）
- **距离计算**：Haversine 公式计算两点距离
- **精度信息**：查询不同精度的 Geohash 尺寸
- **边界框计算**：获取 Geohash 覆盖的地理范围

## 安装

```bash
# 直接使用
from geohash_utils import encode, decode, neighbors, distance

# 或安装为包
pip install alltoolkit-geohash-utils
```

## 快速开始

### 基本编码解码

```python
from geohash_utils import encode, decode

# 经纬度编码为 Geohash
geohash = encode(39.9042, 116.4074, precision=6)
print(geohash)  # 'wx4g0b'

# Geohash 解码为中心点和边界框
lat, lng, bbox = decode('wx4g0b')
print(f"中心点: ({lat}, {lng})")
print(f"边界框: {bbox}")  # (min_lat, max_lat, min_lng, max_lng)
```

### 邻近搜索

```python
from geohash_utils import encode, neighbors

# 获取相邻的 8 个 Geohash
geohash = encode(39.9042, 116.4074, precision=6)
adjacent = neighbors(geohash)
print(adjacent)  # {'n': 'wx4g0c', 's': 'wx4g09', ...}

# 用于邻近搜索：查询当前位置及周围 9 个格子
search_hashes = [geohash] + list(adjacent.values())
```

### 距离计算

```python
from geohash_utils import distance

# 计算两点间距离（Haversine 公式）
dist = distance(39.9042, 116.4074, 31.2304, 121.4737)
print(f"北京到上海: {dist:.2f} km")
```

### 精度信息

```python
from geohash_utils import get_precision_info

# 查询精度 6 的 Geohash 尺寸
info = get_precision_info(6)
print(info)
# {
#     'precision': 6,
#     'width_km': 1.2,
#     'height_km': 0.61,
#     'description': '街道级别'
# }
```

## API 参考

### encode(lat, lng, precision=10)

将经纬度编码为 Geohash 字符串。

**参数**:
- `lat` (float): 纬度 (-90, 90)
- `lng` (float): 经度 (-180, 180)
- `precision` (int): 精度 (1-12)，默认 10

**返回**: Geohash 字符串

**示例**:
```python
>>> encode(39.9042, 116.4074, 6)
'wx4g0b'
```

### decode(geohash)

将 Geohash 解码为经纬度。

**参数**:
- `geohash` (str): Geohash 字符串

**返回**: `(lat, lng, bbox)` 元组
- `lat`: 中心点纬度
- `lng`: 中心点经度
- `bbox`: 边界框 (min_lat, max_lat, min_lng, max_lng)

### neighbors(geohash)

获取相邻的 8 个 Geohash。

**参数**:
- `geohash` (str): Geohash 字符串

**返回**: 字典 `{'n': ..., 's': ..., 'e': ..., 'w': ..., 'ne': ..., 'nw': ..., 'se': ..., 'sw': ...}`

### distance(lat1, lng1, lat2, lng2)

计算两点间的球面距离（Haversine 公式）。

**参数**:
- `lat1, lng1`: 第一个点的坐标
- `lat2, lng2`: 第二个点的坐标

**返回**: 距离（千米）

### get_precision_info(precision)

获取指定精度的 Geohash 尺寸信息。

**返回**: 包含 `precision`, `width_km`, `height_km`, `description` 的字典

## 精度参考表

| 精度 | 宽度 | 高度 | 描述 |
|------|----------|----------|------|
| 1 | 5000 | 5000 | 世界级别 |
| 2 | 1250 | 625 | 国家级别 |
| 3 | 156 | 156 | 省份级别 |
| 4 | 39 | 19.5 | 城市级别 |
| 5 | 4.9 | 4.9 | 区县级别 |
| 6 | 1.2 | 0.61 | 街道级别 |
| 7 | 153 | 153 | 建筑级别 |
| 8 | 38 | 19 | 房屋级别 |
| 9 | 4.8 | 4.8 | 房间级别 |
| 10 | 1.2 | 0.6 | 桌子级别 |
| 11 | 0.149 | 0.149 | 人体级别 |
| 12 | 0.037 | 0.019 | 手掌级别 |

## 使用场景

- **位置搜索**：快速过滤邻近位置
- **地理索引**：数据库地理索引优化
- **地图应用**：网格化地图显示
- **签到系统**：附近地点推荐
- **物流配送**：配送区域划分

## 测试

```bash
python geohash_utils_test.py
```

## 许可证

MIT License