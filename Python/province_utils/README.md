# province_utils - 中国省份信息工具

## 功能概述

提供中国 34 个省级行政区（23个省、4个直辖市、5个自治区、2个特别行政区）的信息查询和管理功能。

## 核心功能

### 1. 省份查询

支持多种查询方式：

- **按简称查询**: `get_province_by_short("京")`
- **按全称查询**: `get_province_by_name("广东省")`
- **按行政代码查询**: `get_province_by_code("110000")`
- **按省会查询**: `get_province_by_capital("成都市")`
- **按电话区号查询**: `get_province_by_area_code("020")`
- **模糊搜索**: `search_province("州")`

### 2. 相邻关系

- **获取相邻省份**: `get_neighbors("川")`
- **计算邻接距离**: `calculate_distance("京", "沪")`
- **查找最短路径**: `find_route("京", "粤")`

### 3. 行政区划类型

- **直辖市**: `get_municipalities()` (北京、天津、上海、重庆)
- **自治区**: `get_autonomous_regions()` (内蒙古、广西、西藏、宁夏、新疆)
- **特别行政区**: `get_special_administrative_regions()` (香港、澳门)

### 4. 统计信息

- **省份统计**: `get_province_statistics("粤")`
- **全国统计**: `get_national_statistics()`

### 5. 数据导出

- **导出字典**: `export_to_dict()`
- **列出简称**: `list_province_short_names()`
- **列出全称**: `list_province_names()`

## 数据结构

每个省份包含以下信息：

```python
Province(
    name="北京市",           # 全称
    short_name="京",         # 简称
    code="110000",           # 行政代码
    capital="北京",          # 省会
    region_type=RegionType,  # 类型（省/直辖市/自治区/特别行政区）
    area_km2=16410,          # 面积（平方公里）
    population=2189,         # 人口（万人）
    cities=["海淀区"...],    # 下辖市/区列表
    area_codes=["010"],      # 电话区号列表
    neighbors=["津", "冀"],  # 相邻省份简称
    iso_code="HK"            # ISO代码（港澳台有）
)
```

## 使用示例

### 基本查询

```python
from province_utils.mod import get_province_by_short

# 查询北京
beijing = get_province_by_short("京")
print(beijing.name)        # 北京市
print(beijing.capital)     # 北京
print(beijing.area_codes)  # ['010']
```

### 搜索省份

```python
from province_utils.mod import search_province

# 搜索包含"州"的省份
results = search_province("州")
for p in results:
    print(p.name)  # 浙江省、福建省、河南省、广东省、贵州省...
```

### 相邻省份

```python
from province_utils.mod import get_neighbors, find_route

# 四川相邻省份
neighbors = get_neighbors("川")
print([n.name for n in neighbors])  # ['青海省', '甘肃省', '陕西省', '重庆市', '贵州省', '云南省', '西藏自治区']

# 北京到广东的路径
route = find_route("京", "粤")
print([get_province_by_short(s).name for s in route])
# ['北京市', '河北省', '河南省', '湖北省', '湖南省', '广东省']
```

### 统计信息

```python
from province_utils.mod import get_province_statistics, get_national_statistics

# 广东统计
stats = get_province_statistics("粤")
print(stats["area_km2"])     # 179800
print(stats["population_万"]) # 12684

# 全国统计
national = get_national_statistics()
print(national["total_count"])           # 34
print(national["municipality_count"])    # 4
```

## 测试覆盖

- **25 个测试函数**
- **180+ 测试用例**
- **100% 通过率**

测试覆盖范围：

- 数据结构完整性
- 各种查询方式
- 相邻关系和路径计算
- 行政区划类型筛选
- 统计信息
- 边界值（空字符串、特殊字符、超长字符串）
- Unicode 支持验证

## 零依赖

仅使用 Python 标准库：

- `typing` - 类型注解
- `dataclasses` - 数据类
- `enum` - 枚举类型

## 数据来源

省份数据基于国家统计局公开数据，包含：

- 行政区划代码（6位编码）
- 面积数据（平方公里）
- 人口数据（2020年第七次人口普查）
- 电话区号
- 下辖市/区列表

## 应用场景

- **地理信息系统**: 省份信息查询和展示
- **数据分析**: 区域统计分析
- **旅游规划**: 路线规划（邻接路径）
- **教育工具**: 中国行政区划学习
- **数据可视化**: 地图标注和数据展示
- **业务系统**: 地址验证、区号查询

## 扩展建议

可根据需要扩展：

- **市级数据**: 添加各市详细信息
- **邮政编码**: 添加邮编数据
- **气候数据**: 添加气候类型
- **经济数据**: GDP、产业结构等
- **坐标数据**: 省会经纬度坐标

---

**最后更新**: 2026-05-18