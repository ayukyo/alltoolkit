"""
Physics Utils 使用示例
展示物理计算工具库的各种用法
"""

from mod import (
    # 常数
    SPEED_OF_LIGHT, GRAVITATIONAL_CONSTANT, STANDARD_GRAVITY,
    PLANCK_CONSTANT, BOLTZMANN_CONSTANT, AVOGADRO_NUMBER,
    ELECTRON_MASS, PROTON_MASS, EARTH_MASS, EARTH_RADIUS,
    # 数据类
    Vector2D, Vector3D,
    # 运动学
    velocity, acceleration, displacement_kinematic,
    free_fall_distance, free_fall_time,
    projectile_range, projectile_max_height, projectile_flight_time, projectile_position,
    # 动力学
    force, weight, friction_force, momentum, gravitational_force, centripetal_force,
    # 能量
    kinetic_energy, potential_energy_gravity, potential_energy_spring, work, power,
    escape_velocity,
    # 圆周运动
    angular_velocity_from_frequency, period_from_frequency,
    # 波动
    wave_speed, sound_speed_in_air,
    # 热力学
    celsius_to_fahrenheit, celsius_to_kelvin, heat_energy, ideal_gas_pressure,
    # 流体力学
    hydrostatic_pressure, buoyant_force,
    # 电磁学
    coulomb_force, ohms_law_voltage, ohms_law_current, electric_power_voltage_current,
    # 振动
    simple_harmonic_position, pendulum_period, spring_period,
    # 相对论
    lorentz_factor, time_dilation, relativistic_energy,
    # 单位换算
    kmh_to_mps, mps_to_kmh, joule_to_calorie
)


def example_kinematics():
    """运动学示例"""
    print("\n" + "=" * 50)
    print("运动学示例")
    print("=" * 50)
    
    # 匀加速运动
    print("\n【匀加速运动】")
    v0 = 0  # 初速度 0
    a = 9.8  # 加速度 9.8 m/s²
    t = 5  # 时间 5秒
    
    s = displacement_kinematic(v0, a, t)
    v = v0 + a * t
    
    print(f"初速度: {v0} m/s, 加速度: {a} m/s², 时间: {t} s")
    print(f"位移: {s:.2f} m")
    print(f"末速度: {v:.2f} m/s")
    
    # 抛射体运动
    print("\n【抛射体运动】")
    v0 = 50  # 初速度 50 m/s
    angle = 45  # 发射角度 45度
    
    R = projectile_range(v0, angle)
    H = projectile_max_height(v0, angle)
    T = projectile_flight_time(v0, angle)
    
    print(f"初速度: {v0} m/s, 发射角度: {angle}°")
    print(f"水平射程: {R:.2f} m")
    print(f"最大高度: {H:.2f} m")
    print(f"飞行时间: {T:.2f} s")
    
    # 显示轨迹
    print("\n轨迹点:")
    for t in [0, 1, 2, 3, 4, 5]:
        x, y = projectile_position(v0, angle, t)
        print(f"  t={t}s: x={x:.1f}m, y={y:.1f}m")


def example_dynamics():
    """动力学示例"""
    print("\n" + "=" * 50)
    print("动力学示例")
    print("=" * 50)
    
    # 牛顿第二定律
    print("\n【牛顿第二定律】")
    m = 10  # 质量 10 kg
    a = 5   # 加速度 5 m/s²
    F = force(m, a)
    print(f"质量: {m} kg, 加速度: {a} m/s²")
    print(f"力: F = ma = {F} N")
    
    # 重力
    print("\n【重力计算】")
    m = 70  # 质量 70 kg
    W = weight(m)
    print(f"质量: {m} kg")
    print(f"重力: W = mg = {W:.2f} N")
    
    # 摩擦力
    print("\n【摩擦力】")
    N = 100  # 正压力 100 N
    mu = 0.3  # 摩擦系数
    f = friction_force(N, mu)
    print(f"正压力: {N} N, 摩擦系数: {mu}")
    print(f"摩擦力: f = μN = {f} N")
    
    # 万有引力
    print("\n【万有引力 - 地球表面】")
    m1 = 70  # 人质量
    m2 = EARTH_MASS
    r = EARTH_RADIUS
    F = gravitational_force(m1, m2, r)
    print(f"人质量: {m1} kg")
    print(f"地球质量: {m2:.3e} kg")
    print(f"地球半径: {r/1000:.1f} km")
    print(f"引力: {F:.2f} N (应等于重力)")


def example_energy():
    """能量示例"""
    print("\n" + "=" * 50)
    print("能量与功示例")
    print("=" * 50)
    
    # 动能
    print("\n【动能】")
    m = 1000  # 质量 1000 kg (汽车)
    v = 20    # 速度 20 m/s (72 km/h)
    KE = kinetic_energy(m, v)
    print(f"汽车质量: {m} kg, 速度: {v} m/s ({v*3.6:.0f} km/h)")
    print(f"动能: KE = ½mv² = {KE:.0f} J = {KE/1000:.0f} kJ")
    
    # 势能
    print("\n【重力势能】")
    m = 50    # 质量 50 kg
    h = 100   # 高度 100 m
    PE = potential_energy_gravity(m, h)
    print(f"质量: {m} kg, 高度: {h} m")
    print(f"重力势能: PE = mgh = {PE:.2f} J")
    
    # 弹性势能
    print("\n【弹性势能】")
    k = 1000  # 弹簧常数 1000 N/m
    x = 0.1   # 形变量 0.1 m
    PE = potential_energy_spring(k, x)
    print(f"弹簧常数: {k} N/m, 形变量: {x} m")
    print(f"弹性势能: PE = ½kx² = {PE:.2f} J")
    
    # 功和功率
    print("\n【功和功率】")
    F = 500   # 力 500 N
    s = 10    # 位移 10 m
    t = 5     # 时间 5 s
    W = work(F, s)
    P = power(W, t)
    print(f"力: {F} N, 位移: {s} m, 时间: {t} s")
    print(f"功: W = Fs = {W} J")
    print(f"功率: P = W/t = {P} W")


def example_oscillations():
    """振动示例"""
    print("\n" + "=" * 50)
    print("振动示例")
    print("=" * 50)
    
    # 单摆
    print("\n【单摆】")
    L = 1.0  # 摆长 1 m
    T = pendulum_period(L)
    print(f"摆长: {L} m")
    print(f"周期: T = 2π√(L/g) = {T:.3f} s")
    print(f"频率: f = 1/T = {1/T:.3f} Hz")
    
    # 弹簧振子
    print("\n【弹簧振子】")
    m = 0.5   # 质量 0.5 kg
    k = 50    # 弹簧常数 50 N/m
    T = spring_period(m, k)
    print(f"质量: {m} kg, 弹簧常数: {k} N/m")
    print(f"周期: T = 2π√(m/k) = {T:.3f} s")
    
    # 简谐运动
    print("\n【简谐运动】")
    A = 0.1   # 振幅 0.1 m
    omega = angular_velocity_from_frequency(1)  # 频率 1 Hz
    print(f"振幅: {A} m, 频率: 1 Hz")
    print("位移随时间变化:")
    for t in [0, 0.25, 0.5, 0.75, 1.0]:
        x = simple_harmonic_position(A, omega, t)
        print(f"  t={t:.2f}s: x={x*100:.1f} cm")


def example_fluid():
    """流体力学示例"""
    print("\n" + "=" * 50)
    print("流体力学示例")
    print("=" * 50)
    
    # 静水压强
    print("\n【静水压强】")
    rho = 1000  # 水密度 1000 kg/m³
    h = 10      # 深度 10 m
    P = hydrostatic_pressure(rho, h)
    print(f"水深: {h} m")
    print(f"压强: P = ρgh = {P:.0f} Pa = {P/1000:.2f} kPa")
    
    # 浮力
    print("\n【浮力】")
    V = 0.5  # 排开体积 0.5 m³
    F = buoyant_force(rho, V)
    print(f"排开水体积: {V} m³")
    print(f"浮力: F = ρVg = {F:.2f} N")


def example_thermodynamics():
    """热力学示例"""
    print("\n" + "=" * 50)
    print("热力学示例")
    print("=" * 50)
    
    # 温度转换
    print("\n【温度转换】")
    c = 25
    f = celsius_to_fahrenheit(c)
    k = celsius_to_kelvin(c)
    print(f"{c}°C = {f:.1f}°F = {k:.2f} K")
    
    # 热量计算
    print("\n【热量计算】")
    m = 1           # 1 kg 水
    c_water = 4184  # 水的比热容 J/(kg·K)
    delta_T = 80    # 温度升高 80 K
    Q = heat_energy(m, c_water, delta_T)
    print(f"加热 {m} kg 水从 20°C 到 100°C")
    print(f"热量: Q = mcΔT = {Q:.0f} J = {Q/1000:.0f} kJ")


def example_electromagnetism():
    """电磁学示例"""
    print("\n" + "=" * 50)
    print("电磁学示例")
    print("=" * 50)
    
    # 欧姆定律
    print("\n【欧姆定律】")
    R = 100  # 电阻 100 Ω
    V = 5    # 电压 5 V
    I = ohms_law_current(V, R)
    print(f"电压: {V} V, 电阻: {R} Ω")
    print(f"电流: I = V/R = {I*1000:.1f} mA")
    
    # 电功率
    P = electric_power_voltage_current(V, I)
    print(f"功率: P = VI = {P*1000:.1f} mW")
    
    # 库仑力
    print("\n【库仑力】")
    q1 = q2 = 1e-6  # 1 μC
    r = 0.1         # 10 cm
    F = coulomb_force(q1, q2, r)
    print(f"电荷: {q1*1e6} μC, 距离: {r*100} cm")
    print(f"库仑力: F = {F:.2f} N")


def example_relativity():
    """相对论示例"""
    print("\n" + "=" * 50)
    print("相对论示例")
    print("=" * 50)
    
    # 洛伦兹因子
    print("\n【洛伦兹因子】")
    for v_percent in [10, 50, 90, 99]:
        v = v_percent / 100 * SPEED_OF_LIGHT
        gamma = lorentz_factor(v)
        print(f"v = {v_percent}% c: γ = {gamma:.4f}")
    
    # 时间膨胀
    print("\n【时间膨胀】")
    t0 = 1.0  # 固有时间 1 秒
    v = 0.866 * SPEED_OF_LIGHT  # 86.6% 光速
    t = time_dilation(t0, v)
    print(f"固有时间: {t0} s")
    print(f"速度: {0.866:.1%} 光速")
    print(f"膨胀后时间: {t:.2f} s (是原来的 {t/t0:.1f} 倍)")
    
    # 静止能量
    print("\n【静止能量】")
    m = 1e-6  # 1 mg
    E = relativistic_energy(m)
    print(f"质量: {m*1e6} mg")
    print(f"静止能量: E = mc² = {E:.2e} J")
    print(f"         相当于 {E/4.184e6:.0f} kcal (千卡)")


def example_vectors():
    """向量示例"""
    print("\n" + "=" * 50)
    print("向量示例")
    print("=" * 50)
    
    # 二维向量
    print("\n【二维向量】")
    v1 = Vector2D(3, 4)
    v2 = Vector2D(1, 2)
    
    print(f"v1 = ({v1.x}, {v1.y})")
    print(f"v1 模长 = {v1.magnitude()}")
    print(f"v1 角度 = {v1.angle_degrees():.2f}°")
    print(f"v1 单位向量 = ({v1.normalize().x:.3f}, {v1.normalize().y:.3f})")
    print(f"v1 + v2 = ({(v1+v2).x}, {(v1+v2).y})")
    print(f"v1 · v2 = {v1.dot(v2)}")
    
    # 三维向量
    print("\n【三维向量】")
    v3d = Vector3D(1, 2, 3)
    print(f"v3d = ({v3d.x}, {v3d.y}, {v3d.z})")
    print(f"v3d 模长 = {v3d.magnitude():.4f}")
    
    a = Vector3D(1, 0, 0)
    b = Vector3D(0, 1, 0)
    cross = a.cross(b)
    print(f"a × b = ({cross.x}, {cross.y}, {cross.z})")


def main():
    """主函数"""
    print("=" * 60)
    print("Physics Utils - 物理计算工具库使用示例")
    print("=" * 60)
    
    print("\n物理常数:")
    print(f"  光速: c = {SPEED_OF_LIGHT:,} m/s")
    print(f"  万有引力常数: G = {GRAVITATIONAL_CONSTANT:.5e} m³/(kg·s²)")
    print(f"  标准重力加速度: g = {STANDARD_GRAVITY} m/s²")
    print(f"  普朗克常数: h = {PLANCK_CONSTANT:.5e} J·s")
    print(f"  阿伏伽德罗常数: NA = {AVOGADRO_NUMBER:.5e}")
    print(f"  电子质量: me = {ELECTRON_MASS:.5e} kg")
    print(f"  地球质量: ME = {EARTH_MASS:.3e} kg")
    
    example_kinematics()
    example_dynamics()
    example_energy()
    example_oscillations()
    example_fluid()
    example_thermodynamics()
    example_electromagnetism()
    example_relativity()
    example_vectors()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()