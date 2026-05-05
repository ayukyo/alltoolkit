"""
Physics Utils 测试文件
"""

import math
import sys
sys.path.insert(0, '.')

from mod import (
    # 常数
    SPEED_OF_LIGHT, GRAVITATIONAL_CONSTANT, STANDARD_GRAVITY,
    # 数据类
    Vector2D, Vector3D,
    # 运动学
    velocity, acceleration, displacement_kinematic, final_velocity_kinematic,
    free_fall_distance, free_fall_time, projectile_range, projectile_max_height,
    projectile_flight_time, projectile_position,
    # 动力学
    force, weight, friction_force, momentum, impulse,
    gravitational_force, centripetal_force,
    # 能量与功
    kinetic_energy, potential_energy_gravity, potential_energy_spring,
    work, power, power_force_velocity, escape_velocity,
    # 圆周运动
    angular_velocity, angular_velocity_from_frequency, linear_velocity_from_angular,
    centripetal_acceleration, period_from_frequency, frequency_from_period,
    # 波动
    wave_speed, wavelength_from_speed, frequency_from_wavelength,
    doppler_effect_observer_moving, sound_speed_in_air,
    # 热力学
    celsius_to_fahrenheit, fahrenheit_to_celsius, celsius_to_kelvin, kelvin_to_celsius,
    heat_energy, ideal_gas_pressure, ideal_gas_volume, ideal_gas_temperature,
    # 流体力学
    pressure_force, hydrostatic_pressure, buoyant_force, flow_rate, reynolds_number,
    # 电磁学
    coulomb_force, electric_field_force, electric_potential_energy,
    ohms_law_voltage, ohms_law_current, electric_power_voltage_current,
    electric_power_resistance, magnetic_force_on_charge,
    # 振动
    simple_harmonic_position, simple_harmonic_velocity, simple_harmonic_acceleration,
    pendulum_period, spring_period,
    # 相对论
    lorentz_factor, time_dilation, length_contraction, relativistic_mass, relativistic_energy,
    # 单位换算
    mph_to_mps, mps_to_mph, kmh_to_mps, mps_to_kmh,
    knot_to_mps, mps_to_knot, joule_to_calorie, calorie_to_joule,
    joule_to_ev, ev_to_joule, pascal_to_atm, atm_to_pascal,
    pascal_to_bar, bar_to_pascal
)


def test_constants():
    """测试物理常数"""
    print("测试物理常数...")
    assert SPEED_OF_LIGHT == 299792458
    assert abs(GRAVITATIONAL_CONSTANT - 6.67430e-11) < 1e-20
    assert STANDARD_GRAVITY == 9.80665
    print("  ✓ 物理常数测试通过")


def test_vector_2d():
    """测试二维向量"""
    print("测试二维向量...")
    v1 = Vector2D(3, 4)
    assert v1.magnitude() == 5.0
    assert abs(v1.angle_degrees() - 53.13010235415598) < 1e-10
    
    v2 = Vector2D(1, 0)
    v3 = Vector2D(0, 1)
    assert abs(v2.angle_degrees() - 0) < 1e-10
    assert abs(v3.angle_degrees() - 90) < 1e-10
    
    # 向量运算
    v4 = v1 + Vector2D(1, 1)
    assert v4.x == 4 and v4.y == 5
    
    v5 = v1 - Vector2D(1, 1)
    assert v5.x == 2 and v5.y == 3
    
    v6 = v1 * 2
    assert v6.x == 6 and v6.y == 8
    
    assert v2.dot(v3) == 0  # 正交向量点积为0
    assert v1.normalize().magnitude() == 1.0
    print("  ✓ 二维向量测试通过")


def test_vector_3d():
    """测试三维向量"""
    print("测试三维向量...")
    v1 = Vector3D(1, 2, 2)
    assert abs(v1.magnitude() - 3.0) < 1e-10
    
    v2 = Vector3D(1, 0, 0)
    v3 = Vector3D(0, 1, 0)
    
    # 叉积
    cross = v2.cross(v3)
    assert cross.x == 0 and cross.y == 0 and cross.z == 1
    
    # 点积
    assert v2.dot(v3) == 0
    print("  ✓ 三维向量测试通过")


def test_kinematics():
    """测试运动学"""
    print("测试运动学...")
    
    # 速度
    assert velocity(100, 10) == 10.0
    
    # 加速度
    assert acceleration(20, 10, 5) == 2.0
    
    # 位移
    assert displacement_kinematic(10, 2, 5) == 75.0  # 10*5 + 0.5*2*25
    
    # 末速度
    assert final_velocity_kinematic(10, 2, 5) == 20.0
    
    # 自由落体
    assert abs(free_fall_distance(2) - 0.5 * 9.80665 * 4) < 1e-10
    assert abs(free_fall_time(19.6133) - 2.0) < 0.01
    
    # 抛射体
    # 45度发射，初速度 10 m/s
    r = projectile_range(10, 45)
    expected_range = (10**2 * math.sin(math.radians(90))) / 9.80665
    assert abs(r - expected_range) < 1e-10
    
    # 抛射体位置
    x, y = projectile_position(10, 45, 1)
    assert x > 0
    assert y >= 0
    print("  ✓ 运动学测试通过")


def test_dynamics():
    """测试动力学"""
    print("测试动力学...")
    
    # 牛顿第二定律
    assert force(10, 5) == 50.0
    
    # 重力
    assert abs(weight(10) - 98.0665) < 1e-10
    
    # 摩擦力
    assert friction_force(100, 0.5) == 50.0
    
    # 动量
    assert momentum(10, 5) == 50.0
    
    # 冲量
    assert impulse(100, 2) == 200.0
    
    # 万有引力
    F = gravitational_force(1, 1, 1)
    expected = 6.67430e-11
    assert abs(F - expected) < 1e-15
    
    # 向心力
    assert centripetal_force(10, 5, 2) == 125.0
    print("  ✓ 动力学测试通过")


def test_energy():
    """测试能量与功"""
    print("测试能量与功...")
    
    # 动能
    assert kinetic_energy(10, 5) == 125.0  # 0.5 * 10 * 25
    
    # 重力势能
    assert abs(potential_energy_gravity(10, 5) - 490.3325) < 1e-10
    
    # 弹性势能
    assert abs(potential_energy_spring(100, 0.1) - 0.5) < 1e-10  # 0.5 * 100 * 0.01
    
    # 功
    assert work(100, 10) == 1000.0
    assert abs(work(100, 10, 60) - 500.0) < 1e-10  # 100 * 10 * cos(60) = 500
    
    # 功率
    assert power(1000, 10) == 100.0
    
    # 逃逸速度
    v = escape_velocity(5.972e24, 6371000)  # 地球
    assert abs(v - 11186) < 100  # 约 11.2 km/s
    print("  ✓ 能量与功测试通过")


def test_circular_motion():
    """测试圆周运动"""
    print("测试圆周运动...")
    
    # 角速度
    assert angular_velocity(2 * math.pi, 1) == 2 * math.pi
    
    # 频率转角速度
    assert angular_velocity_from_frequency(1) == 2 * math.pi
    
    # 线速度
    assert linear_velocity_from_angular(2 * math.pi, 1) == 2 * math.pi
    
    # 向心加速度
    assert centripetal_acceleration(10, 2) == 50.0
    
    # 周期与频率
    assert period_from_frequency(2) == 0.5
    assert frequency_from_period(0.5) == 2.0
    print("  ✓ 圆周运动测试通过")


def test_waves():
    """测试波动"""
    print("测试波动...")
    
    # 波速
    assert wave_speed(2, 3) == 6.0
    
    # 波长
    assert wavelength_from_speed(6, 2) == 3.0
    
    # 频率
    assert frequency_from_wavelength(6, 3) == 2.0
    
    # 声速
    v = sound_speed_in_air(20)  # 20°C
    assert abs(v - 343.42) < 0.1  # 约 343 m/s
    print("  ✓ 波动测试通过")


def test_thermodynamics():
    """测试热力学"""
    print("测试热力学...")
    
    # 温度转换
    assert abs(celsius_to_fahrenheit(0) - 32) < 1e-10
    assert abs(celsius_to_fahrenheit(100) - 212) < 1e-10
    assert abs(fahrenheit_to_celsius(32) - 0) < 1e-10
    assert abs(fahrenheit_to_celsius(212) - 100) < 1e-10
    assert abs(celsius_to_kelvin(0) - 273.15) < 1e-10
    assert abs(kelvin_to_celsius(273.15) - 0) < 1e-10
    
    # 热量
    Q = heat_energy(1, 4184, 10)  # 1kg 水，升温 10K
    assert Q == 41840
    
    # 理想气体
    P = ideal_gas_pressure(1, 0.0224, 273.15)  # 1mol 在 STP
    assert abs(P - 101325) < 100  # 约 1 atm
    print("  ✓ 热力学测试通过")


def test_fluid_mechanics():
    """测试流体力学"""
    print("测试流体力学...")
    
    # 压强
    assert pressure_force(100, 10) == 10.0
    
    # 静水压强
    P = hydrostatic_pressure(1000, 10)  # 水，深 10m
    assert abs(P - 98066.5) < 1e-10
    
    # 浮力
    F = buoyant_force(1000, 0.1)  # 0.1m³ 在水中
    assert abs(F - 980.665) < 1e-10
    
    # 流量
    Q = flow_rate(0.01, 10)
    assert Q == 0.1
    
    # 雷诺数
    Re = reynolds_number(1000, 1, 0.1, 0.001)
    assert Re == 100000
    print("  ✓ 流体力学测试通过")


def test_electromagnetism():
    """测试电磁学"""
    print("测试电磁学...")
    
    # 库仑力
    F = coulomb_force(1e-6, 1e-6, 1)  # 1μC 相距 1m
    assert abs(F - 0.008987551787) < 1e-6  # 约 8.99 mN
    
    # 电场力
    assert electric_field_force(1e-6, 1000) == 0.001
    
    # 电势能
    assert electric_potential_energy(1, 10) == 10.0
    
    # 欧姆定律
    assert ohms_law_voltage(2, 5) == 10.0
    assert ohms_law_current(10, 5) == 2.0
    
    # 电功率
    assert electric_power_voltage_current(10, 2) == 20.0
    assert electric_power_resistance(10, 5) == 20.0
    
    # 磁场力
    F = magnetic_force_on_charge(1e-6, 1000, 0.1)  # 90度
    assert abs(F - 1e-4) < 1e-10
    print("  ✓ 电磁学测试通过")


def test_oscillations():
    """测试振动"""
    print("测试振动...")
    
    # 简谐运动
    A = 1.0
    omega = 2 * math.pi
    t = 0
    
    # t=0时，相位=0
    assert simple_harmonic_position(A, omega, t) == A
    assert simple_harmonic_velocity(A, omega, t) == 0
    assert simple_harmonic_acceleration(A, omega, t) == -A * omega**2
    
    # 单摆周期
    T = pendulum_period(1)  # 1米摆长
    assert abs(T - 2.006) < 0.01  # 约 2 秒
    
    # 弹簧周期
    T = spring_period(1, 100)  # 1kg，k=100 N/m
    expected = 2 * math.pi * math.sqrt(1/100)
    assert abs(T - expected) < 1e-10
    print("  ✓ 振动测试通过")


def test_relativity():
    """测试相对论"""
    print("测试相对论...")
    
    # 洛伦兹因子
    v = 0.5 * SPEED_OF_LIGHT
    gamma = lorentz_factor(v)
    expected = 1 / math.sqrt(1 - 0.25)
    assert abs(gamma - expected) < 1e-10
    
    # 时间膨胀
    t0 = 1.0
    t = time_dilation(t0, v)
    assert t > t0
    
    # 长度收缩
    L0 = 1.0
    L = length_contraction(L0, v)
    assert L < L0
    
    # 相对论质量
    m = relativistic_mass(1.0, v)
    assert m > 1.0
    
    # 静止能量
    E = relativistic_energy(1.0)
    assert abs(E - 8.987551787e16) < 1e10  # 约 9e16 J
    print("  ✓ 相对论测试通过")


def test_unit_conversions():
    """测试单位换算"""
    print("测试单位换算...")
    
    # 速度
    assert abs(mph_to_mps(100) - 44.704) < 1e-10
    assert abs(mps_to_mph(44.704) - 100) < 1e-10
    assert abs(kmh_to_mps(36) - 10) < 1e-10
    assert abs(mps_to_kmh(10) - 36) < 1e-10
    
    # 能量
    assert abs(joule_to_calorie(4.184) - 1) < 1e-10
    assert abs(calorie_to_joule(1) - 4.184) < 1e-10
    
    # 压强
    assert abs(pascal_to_atm(101325) - 1) < 1e-10
    assert abs(atm_to_pascal(1) - 101325) < 1e-10
    assert abs(pascal_to_bar(100000) - 1) < 1e-10
    assert abs(bar_to_pascal(1) - 100000) < 1e-10
    print("  ✓ 单位换算测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Physics Utils 测试套件")
    print("=" * 50)
    
    test_constants()
    test_vector_2d()
    test_vector_3d()
    test_kinematics()
    test_dynamics()
    test_energy()
    test_circular_motion()
    test_waves()
    test_thermodynamics()
    test_fluid_mechanics()
    test_electromagnetism()
    test_oscillations()
    test_relativity()
    test_unit_conversions()
    
    print("=" * 50)
    print("✓ 所有测试通过！")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()