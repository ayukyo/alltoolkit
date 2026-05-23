# Orbital Mechanics Utilities

轨道力学计算工具模块 - 提供完整的轨道计算功能，零外部依赖。

## 功能特性

### 核心功能

1. **开普勒定律计算**
   - 开普勒第三定律：轨道周期与半长轴关系
   - 维维瓦方程：轨道速度计算
   - 角动量计算

2. **基础轨道参数**
   - 圆形轨道速度和周期
   - 逃逸速度计算
   - 表面重力计算

3. **椭圆轨道参数**
   - 近地点/远地点高度转换
   - 偏心率计算
   - 半长轴/半短轴计算
   - 近地点和远地点速度

4. **轨道能量**
   - 特定轨道能量
   - 动能和势能分析
   - 总机械能计算

5. **霍曼转移轨道**
   - 转移时间计算
   - ΔV需求计算
   - 转移轨道速度分析

6. **地球静止轨道**
   - GEO高度计算
   - GEO速度计算

7. **发射计算**
   - 发射速度需求
   - 重力损失估算
   - 发射方位角计算
   - 最小倾角计算

8. **多体计算**
   - 影球半径计算
   - 希尔球半径
   - 会合周期
   - 轨道相位角

9. **预设天体数据**
   - 地球轨道信息
   - 月球轨道信息
   - 火星轨道信息

## 物理常数

模块内置以下物理常数：

- 引力常数 G = 6.67430×10⁻¹¹ m³/(kg·s²)
- 地球 GM = 3.986×10¹⁴ m³/s²
- 月球 GM = 4.904×10¹² m³/s²
- 太阳 GM = 1.327×10²⁰ m³/s²
- 火星 GM = 4.283×10¹³ m³/s²
- 地球半径 = 6,371 km
- 月球半径 = 1,737 km
- 天文单位 AU = 149.6百万 km

## 使用示例

### ISS轨道分析

```python
from orbital_mechanics_utils.mod import earth_orbit_info

# ISS轨道（400km高度）
info = earth_orbit_info(400)
print(f"速度: {info['velocity_kmps']:.2f} km/s")  # ~7.67 km/s
print(f"周期: {info['period_minutes']:.2f} 分钟") # ~92.5 分钟
```

### 地球静止轨道

```python
from orbital_mechanics_utils.mod import geostationary_altitude, geostationary_velocity

alt = geostationary_altitude() / 1000  # ~35786 km
v = geostationary_velocity()           # ~3075 m/s
```

### 霍曼转移

```python
from orbital_mechanics_utils.mod import hohmann_delta_v, R_EARTH

# LEO到GEO转移
r_leo = R_EARTH + 400000    # 400km LEO
r_geo = R_EARTH + 35786000  # GEO

dv1, dv2, total = hohmann_delta_v(r_leo, r_geo)
print(f"总ΔV: {total:.0f} m/s")  # ~3893 m/s
```

### 逃逸速度

```python
from orbital_mechanics_utils.mod import escape_velocity

v_esc_earth = escape_velocity()           # ~11.2 km/s (地表)
v_esc_400km = escape_velocity(400000)     # ~10.9 km/s
```

### 发射窗口计算

```python
from orbital_mechanics_utils.mod import launch_window_azimuth

# 从肯尼迪航天中心(28.5°N)发射到ISS轨道(51.6°倾角)
azimuth = launch_window_azimuth(51.6, 28.5)  # ~45°
```

## 测试

运行测试：

```bash
python orbital_mechanics_utils_test.py
```

运行示例：

```bash
cd examples
python usage_examples.py
```

## API参考

### 开普勒定律

| 函数 | 说明 |
|------|------|
| `kepler_third_law_period(a, gm)` | 从半长轴计算周期 |
| `kepler_third_lax_axis(t, gm)` | 从周期计算半长轴 |
| `kepler_first_law_velocity(r, a, gm)` | 维维瓦方程计算速度 |
| `kepler_second_law_area_velocity(a, gm)` | 计算角动量 |

### 基础轨道

| 函数 | 说明 |
|------|------|
| `orbital_velocity_circular(alt, r_body, gm)` | 圆形轨道速度 |
| `orbital_period_circular(alt, r_body, gm)` | 圆形轨道周期 |
| `escape_velocity(alt, r_body, gm)` | 逃逸速度 |
| `surface_gravity(r_body, gm)` | 表面重力 |

### 椭圆轨道

| 函数 | 说明 |
|------|------|
| `calculate_eccentricity(apogee, perigee, r_body)` | 计算偏心率 |
| `calculate_semi_major_axis(apogee, perigee, r_body)` | 计算半长轴 |
| `velocity_at_apogee(apogee, perigee, r_body, gm)` | 远地点速度 |
| `velocity_at_perigee(apogee, perigee, r_body, gm)` | 近地点速度 |

### 霍曼转移

| 函数 | 说明 |
|------|------|
| `hohmann_transfer_time(r1, r2, gm)` | 转移时间 |
| `hohmann_transfer_velocity(r1, r2, gm)` | 转移轨道速度 |
| `hohmann_delta_v(r1, r2, gm)` | ΔV需求 |

### 预设天体

| 函数 | 说明 |
|------|------|
| `earth_orbit_info(alt_km)` | 地球轨道综合信息 |
| `moon_orbit_info(alt_km)` | 月球轨道综合信息 |
| `mars_orbit_info(alt_km)` | 火星轨道综合信息 |

## 许可证

MIT License

## 作者

AllToolkit Contributors