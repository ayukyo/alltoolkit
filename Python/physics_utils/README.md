# Physics Utils - 物理计算工具库

一个零外部依赖的 Python 物理计算工具库，提供运动学、动力学、能量、波动、热力学、流体力学、电磁学、振动、相对论等领域的计算功能。

## 功能特点

- 🚀 **零外部依赖** - 纯 Python 标准库实现
- 📐 **向量运算** - 支持 2D/3D 向量运算
- 🔬 **全面覆盖** - 涵盖经典力学到相对论
- 📏 **单位换算** - 常用物理单位互转
- ⚡ **高性能** - 轻量级，无额外开销

## 安装使用

```python
from physics_utils.mod import *

# 或者导入特定模块
from physics_utils.mod import kinetic_energy, projectile_range
```

## 核心功能

### 物理常数

```python
from physics_utils.mod import SPEED_OF_LIGHT, GRAVITATIONAL_CONSTANT, STANDARD_GRAVITY

print(f"光速: {SPEED_OF_LIGHT:,} m/s")  # 299,792,458 m/s
print(f"万有引力常数: {GRAVITATIONAL_CONSTANT}")  # 6.67430e-11 m³/(kg·s²)
print(f"标准重力加速度: {STANDARD_GRAVITY} m/s²")  # 9.80665 m/s²
```

### 运动学

```python
from physics_utils.mod import (
    velocity, acceleration, displacement_kinematic,
    free_fall_distance, projectile_range, projectile_position
)

# 匀加速运动
s = displacement_kinematic(v0=0, a=9.8, t=5)  # 122.5 m

# 抛射体运动
range_ = projectile_range(v0=50, angle_degrees=45)  # 约 255 m
x, y = projectile_position(v0=50, angle_degrees=45, time=2)  # 轨迹点
```

### 动力学

```python
from physics_utils.mod import force, weight, momentum, gravitational_force

# 牛顿第二定律
F = force(mass=10, acceleration=5)  # 50 N

# 重力
W = weight(mass=70)  # 约 686 N

# 万有引力
F = gravitational_force(m1=70, m2=EARTH_MASS, distance=EARTH_RADIUS)
```

### 能量与功

```python
from physics_utils.mod import (
    kinetic_energy, potential_energy_gravity, potential_energy_spring,
    work, power, escape_velocity
)

# 动能
KE = kinetic_energy(mass=1000, velocity=20)  # 200,000 J

# 重力势能
PE = potential_energy_gravity(mass=50, height=100)  # 约 49,000 J

# 弹性势能
PE = potential_energy_spring(spring_constant=1000, displacement=0.1)  # 5 J

# 逃逸速度
v = escape_velocity(mass=EARTH_MASS, radius=EARTH_RADIUS)  # 约 11.2 km/s
```

### 圆周运动与振动

```python
from physics_utils.mod import (
    angular_velocity_from_frequency, centripetal_acceleration,
    pendulum_period, spring_period, simple_harmonic_position
)

# 单摆周期
T = pendulum_period(length=1.0)  # 约 2 秒

# 弹簧振子周期
T = spring_period(mass=0.5, spring_constant=50)  # 约 0.63 秒

# 简谐运动
x = simple_harmonic_position(amplitude=0.1, angular_frequency=omega, time=0.5)
```

### 波动

```python
from physics_utils.mod import wave_speed, sound_speed_in_air, doppler_effect_observer_moving

# 波速
v = wave_speed(frequency=440, wavelength=0.78)  # 约 343 m/s

# 空气中声速（温度相关）
v = sound_speed_in_air(temperature_celsius=20)  # 约 343 m/s
```

### 热力学

```python
from physics_utils.mod import (
    celsius_to_fahrenheit, celsius_to_kelvin,
    heat_energy, ideal_gas_pressure
)

# 温度转换
f = celsius_to_fahrenheit(25)  # 77°F
k = celsius_to_kelvin(25)  # 298.15 K

# 热量计算
Q = heat_energy(mass=1, specific_heat=4184, temperature_change=80)  # 加热水

# 理想气体状态方程
P = ideal_gas_pressure(n_moles=1, volume=0.0224, temperature_kelvin=273.15)
```

### 流体力学

```python
from physics_utils.mod import hydrostatic_pressure, buoyant_force, reynolds_number

# 静水压强
P = hydrostatic_pressure(density=1000, height=10)  # 约 98 kPa

# 浮力
F = buoyant_force(density=1000, volume=0.5)  # 约 4900 N

# 雷诺数
Re = reynolds_number(density=1000, velocity=1, length=0.1, viscosity=0.001)
```

### 电磁学

```python
from physics_utils.mod import (
    coulomb_force, ohms_law_voltage, ohms_law_current,
    electric_power_voltage_current, magnetic_force_on_charge
)

# 欧姆定律
I = ohms_law_current(voltage=5, resistance=100)  # 0.05 A = 50 mA

# 电功率
P = electric_power_voltage_current(voltage=5, current=0.05)  # 0.25 W

# 库仑力
F = coulomb_force(q1=1e-6, q2=1e-6, distance=0.1)  # 约 0.9 N
```

### 相对论

```python
from physics_utils.mod import lorentz_factor, time_dilation, relativistic_energy

# 洛伦兹因子
gamma = lorentz_factor(velocity=0.5 * SPEED_OF_LIGHT)  # 约 1.15

# 时间膨胀
t = time_dilation(proper_time=1.0, velocity=0.866 * SPEED_OF_LIGHT)  # 2 秒

# 静止能量
E = relativistic_energy(rest_mass=1.0)  # 约 9e16 J
```

### 向量运算

```python
from physics_utils.mod import Vector2D, Vector3D

# 二维向量
v1 = Vector2D(3, 4)
print(v1.magnitude())  # 5.0
print(v1.angle_degrees())  # 53.13°

# 三维向量
v3d = Vector3D(1, 2, 3)
print(v3d.magnitude())  # 3.74
cross = Vector3D(1, 0, 0).cross(Vector3D(0, 1, 0))  # (0, 0, 1)
```

### 单位换算

```python
from physics_utils.mod import (
    kmh_to_mps, mps_to_kmh, joule_to_calorie, calorie_to_joule,
    pascal_to_atm, atm_to_pascal
)

v_mps = kmh_to_mps(72)  # 20 m/s
E_cal = joule_to_calorie(4184)  # 1 kcal
P_atm = pascal_to_atm(101325)  # 1 atm
```

## 文件结构

```
physics_utils/
├── mod.py        # 主模块文件
├── test.py       # 测试文件
├── examples.py   # 使用示例
└── README.md     # 说明文档
```

## 运行测试

```bash
cd physics_utils
python test.py
```

## 运行示例

```bash
cd physics_utils
python examples.py
```

## API 概览

| 类别 | 函数 | 说明 |
|------|------|------|
| **运动学** | `velocity`, `acceleration`, `displacement_kinematic` | 基本运动学计算 |
| | `free_fall_distance`, `free_fall_time` | 自由落体 |
| | `projectile_range`, `projectile_max_height`, `projectile_position` | 抛射体运动 |
| **动力学** | `force`, `weight`, `friction_force` | 力的计算 |
| | `momentum`, `impulse` | 动量与冲量 |
| | `gravitational_force`, `centripetal_force` | 万有引力与向心力 |
| **能量** | `kinetic_energy`, `potential_energy_gravity` | 动能与重力势能 |
| | `potential_energy_spring`, `work`, `power` | 弹性势能、功、功率 |
| | `escape_velocity` | 逃逸速度 |
| **圆周运动** | `angular_velocity`, `centripetal_acceleration` | 角速度与向心加速度 |
| | `period_from_frequency`, `frequency_from_period` | 周期与频率转换 |
| **波动** | `wave_speed`, `wavelength_from_speed` | 波动基本计算 |
| | `sound_speed_in_air`, `doppler_effect_observer_moving` | 声速与多普勒效应 |
| **热力学** | `celsius_to_fahrenheit`, `celsius_to_kelvin` | 温度转换 |
| | `heat_energy`, `ideal_gas_pressure` | 热量与理想气体 |
| **流体力学** | `hydrostatic_pressure`, `buoyant_force` | 静水压强与浮力 |
| | `flow_rate`, `reynolds_number` | 流量与雷诺数 |
| **电磁学** | `coulomb_force`, `electric_field_force` | 库仑力与电场力 |
| | `ohms_law_voltage`, `ohms_law_current` | 欧姆定律 |
| | `electric_power_voltage_current` | 电功率 |
| | `magnetic_force_on_charge` | 洛伦兹力 |
| **振动** | `simple_harmonic_position`, `pendulum_period` | 简谐运动与单摆 |
| | `spring_period` | 弹簧振子周期 |
| **相对论** | `lorentz_factor`, `time_dilation` | 洛伦兹因子与时间膨胀 |
| | `length_contraction`, `relativistic_energy` | 长度收缩与静止能量 |

## 许可证

MIT License