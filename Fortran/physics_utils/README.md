# Physics Utilities Module

Fortran 90/95/2003+ 物理公式计算工具集，零外部依赖，纯标准库实现。

## 功能概述

- **运动学**：位移、速度、加速度计算
- **动力学**：力、动量、冲量、摩擦力
- **能量**：动能、势能、功、功率
- **圆周运动**：向心力、角速度、周期
- **抛体运动**：水平射程、最大高度、飞行时间
- **万有引力**：引力、逃逸速度、轨道速度
- **波动**：波长、频率、光子能量
- **热力学**：热量传递、理想气体
- **流体力学**：压力、浮力、伯努利方程
- **简谐运动**：弹簧、摆周期
- **转动**：转动动能、角动量、扭矩
- **单位转换**：温度、角度、速度、能量、SI 前缀

## 物理常数

模块内置以下常用物理常数（SI 单位）：

```fortran
GRAVITY             = 9.80665 m/s²      (重力加速度)
SPEED_OF_LIGHT      = 2.998e8 m/s       (光速)
PLANCK_CONSTANT     = 6.626e-34 J·s     (普朗克常数)
BOLTZMANN           = 1.381e-23 J/K     (玻尔兹曼常数)
AVOGADRO            = 6.022e23 1/mol    (阿伏伽德罗常数)
ELECTRON_CHARGE     = 1.602e-19 C       (基本电荷)
GAS_CONSTANT        = 8.314 J/(mol·K)   (气体常数)
```

## 使用方法

### 基本用法

```fortran
program example
    use physics_utils
    implicit none
    
    real(8) :: v, h, t, e
    
    ! 抛体运动计算
    v = 100.0d0  ! 初速度 100 m/s
    h = projectile_max_height(v, 45.0d0)  ! 45°发射角
    t = projectile_time_of_flight(v, 45.0d0)
    
    print *, "最大高度:", h, "米"
    print *, "飞行时间:", t, "秒"
    
    ! 能量计算
    e = kinetic_energy(10.0d0, 5.0d0)  ! 10kg物体以5m/s运动
    print *, "动能:", e, "焦耳"
    
end program example
```

### 编译

```bash
# 编译主模块
gfortran -c mod.f90

# 编译并运行测试
gfortran mod.f90 physics_utils_test.f90 -o test
./test
```

## API 参考

### 运动学

| 函数 | 公式 | 说明 |
|------|------|------|
| `kinematic_displacement(v0, t, a)` | s = v₀t + ½at² | 位移 |
| `kinematic_velocity(v0, a, t)` | v = v₀ + at | 末速度 |
| `kinematic_velocity_squared(v0, a, s)` | v² = v₀² + 2as | 速度平方方程 |
| `average_velocity(s, t)` | v = s/t | 平均速度 |
| `average_speed(distance, t)` | v = d/t | 平均速率 |

### 能量

| 函数 | 公式 | 说明 |
|------|------|------|
| `kinetic_energy(m, v)` | KE = ½mv² | 动能 |
| `potential_energy(m, h)` | PE = mgh | 重力势能 |
| `elastic_potential_energy(k, x)` | PE = ½kx² | 弹性势能 |
| `work(force, displacement, angle)` | W = Fd·cosθ | 功 |
| `power_work(w, t)` | P = W/t | 功率（从功） |
| `power_force_velocity(f, v)` | P = Fv | 功率（从力速度） |

### 圆周运动

| 函数 | 公式 | 说明 |
|------|------|------|
| `centripetal_acceleration(v, r)` | a = v²/r | 向心加速度 |
| `centripetal_force(m, v, r)` | F = mv²/r | 向心力 |
| `angular_velocity_from_linear(v, r)` | ω = v/r | 角速度 |
| `period_from_frequency(f)` | T = 1/f | 周期 |

### 抛体运动

| 函数 | 公式 | 说明 |
|------|------|------|
| `projectile_range(v0, angle)` | R = v₀²sin(2θ)/g | 水平射程 |
| `projectile_max_height(v0, angle)` | H = v₀²sin²θ/(2g) | 最大高度 |
| `projectile_time_of_flight(v0, angle)` | T = 2v₀sinθ/g | 飞行时间 |
| `projectile_horizontal_velocity(v0, angle)` | vx = v₀cosθ | 水平速度分量 |
| `projectile_vertical_velocity(v0, angle)` | vy = v₀sinθ | 垂直速度分量 |

### 单位转换

| 函数 | 说明 |
|------|------|
| `celsius_to_kelvin(c)` | 摄氏度 → 开尔文 |
| `kelvin_to_celsius(k)` | 开尔文 → 摄氏度 |
| `fahrenheit_to_celsius(f)` | 华氏度 → 摄氏度 |
| `degrees_to_radians(d)` | 度 → 弧度 |
| `ms_to_kmh(ms)` | m/s → km/h |
| `joules_to_ev(j)` | 焦耳 → 电子伏特 |
| `apply_si_prefix(value, prefix)` | 应用 SI 前缀 |

## 测试

运行完整测试套件：

```bash
cd Fortran/physics_utils
gfortran mod.f90 physics_utils_test.f90 -o physics_test
./physics_test
```

测试覆盖所有主要功能，使用相对容差验证浮点数精度。

## 示例

查看 `examples/` 目录获取更多使用示例：

- `kinematics_demo.f90` - 运动学计算示例
- `energy_demo.f90` - 能量转换示例
- `projectile_demo.f90` - 抛体运动分析

## 许可证

MIT License - 自由使用、修改和分发。

## 贡献

欢迎提交改进和新功能请求！