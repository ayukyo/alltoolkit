"""
Physics Utils - 物理计算工具库
提供运动学、动力学、能量、波动、热力学等基础物理计算功能
零外部依赖，纯 Python 标准库实现
"""

from dataclasses import dataclass
from typing import Tuple, Optional, Union
import math

# ==================== 物理常数 ====================

SPEED_OF_LIGHT = 299792458  # 光速 m/s
GRAVITATIONAL_CONSTANT = 6.67430e-11  # 万有引力常数 m³/(kg·s²)
PLANCK_CONSTANT = 6.62607015e-34  # 普朗克常数 J·s
BOLTZMANN_CONSTANT = 1.380649e-23  # 玻尔兹曼常数 J/K
AVOGADRO_NUMBER = 6.02214076e23  # 阿伏伽德罗常数
ELECTRON_CHARGE = 1.602176634e-19  # 电子电荷 C
ELECTRON_MASS = 9.1093837015e-31  # 电子质量 kg
PROTON_MASS = 1.67262192369e-27  # 质子质量 kg
NEUTRON_MASS = 1.67492749804e-27  # 中子质量 kg
EARTH_MASS = 5.972e24  # 地球质量 kg
EARTH_RADIUS = 6371000  # 地球平均半径 m
SOLAR_MASS = 1.989e30  # 太阳质量 kg
STANDARD_GRAVITY = 9.80665  # 标准重力加速度 m/s²
VACUUM_PERMITTIVITY = 8.8541878128e-12  # 真空介电常数 F/m
VACUUM_PERMEABILITY = 1.25663706212e-6  # 真空磁导率 H/m


# ==================== 数据类 ====================

@dataclass
class Vector2D:
    """二维向量"""
    x: float
    y: float
    
    def magnitude(self) -> float:
        """向量模长"""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def angle(self) -> float:
        """向量角度（弧度）"""
        return math.atan2(self.y, self.x)
    
    def angle_degrees(self) -> float:
        """向量角度（度）"""
        return math.degrees(self.angle())
    
    def normalize(self) -> 'Vector2D':
        """单位向量"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def dot(self, other: 'Vector2D') -> float:
        """点积"""
        return self.x * other.x + self.y * other.y


@dataclass
class Vector3D:
    """三维向量"""
    x: float
    y: float
    z: float
    
    def magnitude(self) -> float:
        """向量模长"""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self) -> 'Vector3D':
        """单位向量"""
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, other: 'Vector3D') -> float:
        """点积"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        """叉积"""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )


# ==================== 运动学 ====================

def velocity(displacement: float, time: float) -> float:
    """
    计算速度
    
    Args:
        displacement: 位移 (m)
        time: 时间 (s)
    
    Returns:
        速度 (m/s)
    """
    if time == 0:
        raise ValueError("时间不能为零")
    return displacement / time


def acceleration(final_velocity: float, initial_velocity: float, time: float) -> float:
    """
    计算加速度
    
    Args:
        final_velocity: 末速度 (m/s)
        initial_velocity: 初速度 (m/s)
        time: 时间 (s)
    
    Returns:
        加速度 (m/s²)
    """
    if time == 0:
        raise ValueError("时间不能为零")
    return (final_velocity - initial_velocity) / time


def displacement_kinematic(initial_velocity: float, acceleration: float, time: float) -> float:
    """
    匀加速运动位移公式: s = v₀t + ½at²
    
    Args:
        initial_velocity: 初速度 (m/s)
        acceleration: 加速度 (m/s²)
        time: 时间 (s)
    
    Returns:
        位移 (m)
    """
    return initial_velocity * time + 0.5 * acceleration * time ** 2


def final_velocity_kinematic(initial_velocity: float, acceleration: float, time: float) -> float:
    """
    匀加速运动末速度: v = v₀ + at
    
    Args:
        initial_velocity: 初速度 (m/s)
        acceleration: 加速度 (m/s²)
        time: 时间 (s)
    
    Returns:
        末速度 (m/s)
    """
    return initial_velocity + acceleration * time


def free_fall_distance(time: float, g: float = STANDARD_GRAVITY) -> float:
    """
    自由落体距离: h = ½gt²
    
    Args:
        time: 时间 (s)
        g: 重力加速度 (m/s²)，默认标准重力
    
    Returns:
        下落距离 (m)
    """
    return 0.5 * g * time ** 2


def free_fall_time(height: float, g: float = STANDARD_GRAVITY) -> float:
    """
    自由落体时间
    
    Args:
        height: 高度 (m)
        g: 重力加速度 (m/s²)
    
    Returns:
        落地时间 (s)
    """
    return math.sqrt(2 * height / g)


def projectile_range(initial_velocity: float, angle_degrees: float, g: float = STANDARD_GRAVITY) -> float:
    """
    抛射体水平射程
    
    Args:
        initial_velocity: 初速度 (m/s)
        angle_degrees: 发射角度 (度)
        g: 重力加速度 (m/s²)
    
    Returns:
        水平射程 (m)
    """
    angle_rad = math.radians(angle_degrees)
    return (initial_velocity ** 2 * math.sin(2 * angle_rad)) / g


def projectile_max_height(initial_velocity: float, angle_degrees: float, g: float = STANDARD_GRAVITY) -> float:
    """
    抛射体最大高度
    
    Args:
        initial_velocity: 初速度 (m/s)
        angle_degrees: 发射角度 (度)
        g: 重力加速度 (m/s²)
    
    Returns:
        最大高度 (m)
    """
    angle_rad = math.radians(angle_degrees)
    return (initial_velocity ** 2 * (math.sin(angle_rad) ** 2)) / (2 * g)


def projectile_flight_time(initial_velocity: float, angle_degrees: float, g: float = STANDARD_GRAVITY) -> float:
    """
    抛射体飞行时间
    
    Args:
        initial_velocity: 初速度 (m/s)
        angle_degrees: 发射角度 (度)
        g: 重力加速度 (m/s²)
    
    Returns:
        飞行时间 (s)
    """
    angle_rad = math.radians(angle_degrees)
    return (2 * initial_velocity * math.sin(angle_rad)) / g


def projectile_position(initial_velocity: float, angle_degrees: float, time: float, 
                         g: float = STANDARD_GRAVITY) -> Tuple[float, float]:
    """
    抛射体在某一时刻的位置
    
    Args:
        initial_velocity: 初速度 (m/s)
        angle_degrees: 发射角度 (度)
        time: 时间 (s)
        g: 重力加速度 (m/s²)
    
    Returns:
        (水平距离, 垂直高度) (m)
    """
    angle_rad = math.radians(angle_degrees)
    x = initial_velocity * math.cos(angle_rad) * time
    y = initial_velocity * math.sin(angle_rad) * time - 0.5 * g * time ** 2
    return (x, max(0, y))


# ==================== 动力学 ====================

def force(mass: float, acceleration: float) -> float:
    """
    牛顿第二定律: F = ma
    
    Args:
        mass: 质量 (kg)
        acceleration: 加速度 (m/s²)
    
    Returns:
        力 (N)
    """
    return mass * acceleration


def weight(mass: float, g: float = STANDARD_GRAVITY) -> float:
    """
    重力
    
    Args:
        mass: 质量 (kg)
        g: 重力加速度 (m/s²)
    
    Returns:
        重力 (N)
    """
    return mass * g


def friction_force(normal_force: float, coefficient: float) -> float:
    """
    摩擦力: f = μN
    
    Args:
        normal_force: 正压力 (N)
        coefficient: 摩擦系数
    
    Returns:
        摩擦力 (N)
    """
    return coefficient * normal_force


def momentum(mass: float, velocity: float) -> float:
    """
    动量: p = mv
    
    Args:
        mass: 质量 (kg)
        velocity: 速度 (m/s)
    
    Returns:
        动量 (kg·m/s)
    """
    return mass * velocity


def impulse(force: float, time: float) -> float:
    """
    冲量: J = F·t
    
    Args:
        force: 力 (N)
        time: 时间 (s)
    
    Returns:
        冲量 (N·s)
    """
    return force * time


def gravitational_force(m1: float, m2: float, distance: float) -> float:
    """
    万有引力: F = G·m₁·m₂/r²
    
    Args:
        m1: 物体1质量 (kg)
        m2: 物体2质量 (kg)
        distance: 距离 (m)
    
    Returns:
        引力 (N)
    """
    if distance == 0:
        raise ValueError("距离不能为零")
    return GRAVITATIONAL_CONSTANT * m1 * m2 / (distance ** 2)


def centripetal_force(mass: float, velocity: float, radius: float) -> float:
    """
    向心力: F = mv²/r
    
    Args:
        mass: 质量 (kg)
        velocity: 速度 (m/s)
        radius: 半径 (m)
    
    Returns:
        向心力 (N)
    """
    if radius == 0:
        raise ValueError("半径不能为零")
    return mass * velocity ** 2 / radius


# ==================== 能量与功 ====================

def kinetic_energy(mass: float, velocity: float) -> float:
    """
    动能: KE = ½mv²
    
    Args:
        mass: 质量 (kg)
        velocity: 速度 (m/s)
    
    Returns:
        动能 (J)
    """
    return 0.5 * mass * velocity ** 2


def potential_energy_gravity(mass: float, height: float, g: float = STANDARD_GRAVITY) -> float:
    """
    重力势能: PE = mgh
    
    Args:
        mass: 质量 (kg)
        height: 高度 (m)
        g: 重力加速度 (m/s²)
    
    Returns:
        重力势能 (J)
    """
    return mass * g * height


def potential_energy_spring(spring_constant: float, displacement: float) -> float:
    """
    弹性势能: PE = ½kx²
    
    Args:
        spring_constant: 弹簧常数 (N/m)
        displacement: 形变量 (m)
    
    Returns:
        弹性势能 (J)
    """
    return 0.5 * spring_constant * displacement ** 2


def work(force: float, displacement: float, angle_degrees: float = 0) -> float:
    """
    功: W = F·s·cos(θ)
    
    Args:
        force: 力 (N)
        displacement: 位移 (m)
        angle_degrees: 力与位移的夹角 (度)，默认为0
    
    Returns:
        功 (J)
    """
    angle_rad = math.radians(angle_degrees)
    return force * displacement * math.cos(angle_rad)


def power(work_done: float, time: float) -> float:
    """
    功率: P = W/t
    
    Args:
        work_done: 功 (J)
        time: 时间 (s)
    
    Returns:
        功率 (W)
    """
    if time == 0:
        raise ValueError("时间不能为零")
    return work_done / time


def power_force_velocity(force: float, velocity: float) -> float:
    """
    功率: P = F·v
    
    Args:
        force: 力 (N)
        velocity: 速度 (m/s)
    
    Returns:
        功率 (W)
    """
    return force * velocity


def escape_velocity(mass: float, radius: float) -> float:
    """
    逃逸速度: v = √(2GM/r)
    
    Args:
        mass: 天体质量 (kg)
        radius: 天体半径 (m)
    
    Returns:
        逃逸速度 (m/s)
    """
    if radius == 0:
        raise ValueError("半径不能为零")
    return math.sqrt(2 * GRAVITATIONAL_CONSTANT * mass / radius)


# ==================== 圆周运动 ====================

def angular_velocity(angle_radians: float, time: float) -> float:
    """
    角速度: ω = θ/t
    
    Args:
        angle_radians: 角度 (弧度)
        time: 时间 (s)
    
    Returns:
        角速度 (rad/s)
    """
    if time == 0:
        raise ValueError("时间不能为零")
    return angle_radians / time


def angular_velocity_from_frequency(frequency: float) -> float:
    """
    从频率计算角速度: ω = 2πf
    
    Args:
        frequency: 频率 (Hz)
    
    Returns:
        角速度 (rad/s)
    """
    return 2 * math.pi * frequency


def linear_velocity_from_angular(angular_velocity: float, radius: float) -> float:
    """
    从角速度计算线速度: v = ωr
    
    Args:
        angular_velocity: 角速度 (rad/s)
        radius: 半径 (m)
    
    Returns:
        线速度 (m/s)
    """
    return angular_velocity * radius


def centripetal_acceleration(velocity: float, radius: float) -> float:
    """
    向心加速度: a = v²/r
    
    Args:
        velocity: 速度 (m/s)
        radius: 半径 (m)
    
    Returns:
        向心加速度 (m/s²)
    """
    if radius == 0:
        raise ValueError("半径不能为零")
    return velocity ** 2 / radius


def period_from_frequency(frequency: float) -> float:
    """
    从频率计算周期: T = 1/f
    
    Args:
        frequency: 频率 (Hz)
    
    Returns:
        周期 (s)
    """
    if frequency == 0:
        raise ValueError("频率不能为零")
    return 1 / frequency


def frequency_from_period(period: float) -> float:
    """
    从周期计算频率: f = 1/T
    
    Args:
        period: 周期 (s)
    
    Returns:
        频率 (Hz)
    """
    if period == 0:
        raise ValueError("周期不能为零")
    return 1 / period


# ==================== 波动 ====================

def wave_speed(frequency: float, wavelength: float) -> float:
    """
    波速: v = fλ
    
    Args:
        frequency: 频率 (Hz)
        wavelength: 波长 (m)
    
    Returns:
        波速 (m/s)
    """
    return frequency * wavelength


def wavelength_from_speed(speed: float, frequency: float) -> float:
    """
    从波速和频率计算波长: λ = v/f
    
    Args:
        speed: 波速 (m/s)
        frequency: 频率 (Hz)
    
    Returns:
        波长 (m)
    """
    if frequency == 0:
        raise ValueError("频率不能为零")
    return speed / frequency


def frequency_from_wavelength(speed: float, wavelength: float) -> float:
    """
    从波速和波长计算频率: f = v/λ
    
    Args:
        speed: 波速 (m/s)
        wavelength: 波长 (m)
    
    Returns:
        频率 (Hz)
    """
    if wavelength == 0:
        raise ValueError("波长不能为零")
    return speed / wavelength


def doppler_effect_observer_moving(source_frequency: float, source_velocity: float,
                                    observer_velocity: float, wave_speed: float) -> float:
    """
    多普勒效应（观察者移动）
    
    Args:
        source_frequency: 声源频率 (Hz)
        source_velocity: 声源速度 (m/s)，朝向观察者为正
        observer_velocity: 观察者速度 (m/s)，朝向声源为正
        wave_speed: 波速 (m/s)
    
    Returns:
        观察者接收到的频率 (Hz)
    """
    return source_frequency * (wave_speed + observer_velocity) / (wave_speed - source_velocity)


def sound_speed_in_air(temperature_celsius: float) -> float:
    """
    空气中声速（近似公式）
    
    Args:
        temperature_celsius: 温度 (°C)
    
    Returns:
        声速 (m/s)
    """
    return 331.3 + 0.606 * temperature_celsius


# ==================== 热力学 ====================

def celsius_to_fahrenheit(celsius: float) -> float:
    """摄氏度转华氏度"""
    return celsius * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """华氏度转摄氏度"""
    return (fahrenheit - 32) * 5/9


def celsius_to_kelvin(celsius: float) -> float:
    """摄氏度转开尔文"""
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """开尔文转摄氏度"""
    return kelvin - 273.15


def heat_energy(mass: float, specific_heat: float, temperature_change: float) -> float:
    """
    热量: Q = mcΔT
    
    Args:
        mass: 质量 (kg)
        specific_heat: 比热容 (J/(kg·K))
        temperature_change: 温度变化 (K or °C)
    
    Returns:
        热量 (J)
    """
    return mass * specific_heat * temperature_change


def ideal_gas_pressure(n_moles: float, volume: float, temperature_kelvin: float) -> float:
    """
    理想气体状态方程求压强: PV = nRT
    
    Args:
        n_moles: 物质的量 (mol)
        volume: 体积 (m³)
        temperature_kelvin: 温度 (K)
    
    Returns:
        压强 (Pa)
    """
    if volume == 0:
        raise ValueError("体积不能为零")
    R = 8.314  # 气体常数 J/(mol·K)
    return n_moles * R * temperature_kelvin / volume


def ideal_gas_volume(n_moles: float, pressure: float, temperature_kelvin: float) -> float:
    """
    理想气体状态方程求体积: PV = nRT
    
    Args:
        n_moles: 物质的量 (mol)
        pressure: 压强 (Pa)
        temperature_kelvin: 温度 (K)
    
    Returns:
        体积 (m³)
    """
    if pressure == 0:
        raise ValueError("压强不能为零")
    R = 8.314  # 气体常数 J/(mol·K)
    return n_moles * R * temperature_kelvin / pressure


def ideal_gas_temperature(n_moles: float, pressure: float, volume: float) -> float:
    """
    理想气体状态方程求温度: PV = nRT
    
    Args:
        n_moles: 物质的量 (mol)
        pressure: 压强 (Pa)
        volume: 体积 (m³)
    
    Returns:
        温度 (K)
    """
    if n_moles == 0:
        raise ValueError("物质的量不能为零")
    R = 8.314  # 气体常数 J/(mol·K)
    return pressure * volume / (n_moles * R)


# ==================== 流体力学 ====================

def pressure_force(force: float, area: float) -> float:
    """
    压强: P = F/A
    
    Args:
        force: 力 (N)
        area: 面积 (m²)
    
    Returns:
        压强 (Pa)
    """
    if area == 0:
        raise ValueError("面积不能为零")
    return force / area


def hydrostatic_pressure(density: float, height: float, g: float = STANDARD_GRAVITY) -> float:
    """
    静水压强: P = ρgh
    
    Args:
        density: 液体密度 (kg/m³)
        height: 深度 (m)
        g: 重力加速度 (m/s²)
    
    Returns:
        压强 (Pa)
    """
    return density * g * height


def buoyant_force(density: float, volume: float, g: float = STANDARD_GRAVITY) -> float:
    """
    浮力: F = ρVg
    
    Args:
        density: 流体密度 (kg/m³)
        volume: 排开流体体积 (m³)
        g: 重力加速度 (m/s²)
    
    Returns:
        浮力 (N)
    """
    return density * volume * g


def flow_rate(area: float, velocity: float) -> float:
    """
    流量: Q = Av
    
    Args:
        area: 截面积 (m²)
        velocity: 流速 (m/s)
    
    Returns:
        流量 (m³/s)
    """
    return area * velocity


def reynolds_number(density: float, velocity: float, length: float, viscosity: float) -> float:
    """
    雷诺数: Re = ρvL/μ
    
    Args:
        density: 流体密度 (kg/m³)
        velocity: 特征速度 (m/s)
        length: 特征长度 (m)
        viscosity: 动力粘度 (Pa·s)
    
    Returns:
        雷诺数（无量纲）
    """
    if viscosity == 0:
        raise ValueError("粘度不能为零")
    return density * velocity * length / viscosity


# ==================== 电磁学 ====================

def coulomb_force(q1: float, q2: float, distance: float) -> float:
    """
    库仑力: F = k·q₁·q₂/r²
    
    Args:
        q1: 电荷1 (C)
        q2: 电荷2 (C)
        distance: 距离 (m)
    
    Returns:
        力 (N)
    """
    if distance == 0:
        raise ValueError("距离不能为零")
    k = 1 / (4 * math.pi * VACUUM_PERMITTIVITY)
    return k * abs(q1 * q2) / (distance ** 2)


def electric_field_force(charge: float, electric_field: float) -> float:
    """
    电场力: F = qE
    
    Args:
        charge: 电荷 (C)
        electric_field: 电场强度 (N/C or V/m)
    
    Returns:
        力 (N)
    """
    return charge * electric_field


def electric_potential_energy(charge: float, voltage: float) -> float:
    """
    电势能: U = qV
    
    Args:
        charge: 电荷 (C)
        voltage: 电势 (V)
    
    Returns:
        电势能 (J)
    """
    return charge * voltage


def ohms_law_voltage(current: float, resistance: float) -> float:
    """
    欧姆定律求电压: V = IR
    
    Args:
        current: 电流 (A)
        resistance: 电阻 (Ω)
    
    Returns:
        电压 (V)
    """
    return current * resistance


def ohms_law_current(voltage: float, resistance: float) -> float:
    """
    欧姆定律求电流: I = V/R
    
    Args:
        voltage: 电压 (V)
        resistance: 电阻 (Ω)
    
    Returns:
        电流 (A)
    """
    if resistance == 0:
        raise ValueError("电阻不能为零")
    return voltage / resistance


def electric_power_voltage_current(voltage: float, current: float) -> float:
    """
    电功率: P = VI
    
    Args:
        voltage: 电压 (V)
        current: 电流 (A)
    
    Returns:
        功率 (W)
    """
    return voltage * current


def electric_power_resistance(voltage: float, resistance: float) -> float:
    """
    电功率: P = V²/R
    
    Args:
        voltage: 电压 (V)
        resistance: 电阻 (Ω)
    
    Returns:
        功率 (W)
    """
    if resistance == 0:
        raise ValueError("电阻不能为零")
    return voltage ** 2 / resistance


def magnetic_force_on_charge(charge: float, velocity: float, magnetic_field: float,
                              angle_degrees: float = 90) -> float:
    """
    洛伦兹力: F = qvB·sin(θ)
    
    Args:
        charge: 电荷 (C)
        velocity: 速度 (m/s)
        magnetic_field: 磁感应强度 (T)
        angle_degrees: 速度与磁场夹角 (度)，默认90度
    
    Returns:
        力 (N)
    """
    angle_rad = math.radians(angle_degrees)
    return charge * velocity * magnetic_field * math.sin(angle_rad)


# ==================== 振动与简谐运动 ====================

def simple_harmonic_position(amplitude: float, angular_frequency: float, time: float,
                              phase: float = 0) -> float:
    """
    简谐运动位移: x = A·cos(ωt + φ)
    
    Args:
        amplitude: 振幅 (m)
        angular_frequency: 角频率 (rad/s)
        time: 时间 (s)
        phase: 初相位 (rad)
    
    Returns:
        位移 (m)
    """
    return amplitude * math.cos(angular_frequency * time + phase)


def simple_harmonic_velocity(amplitude: float, angular_frequency: float, time: float,
                              phase: float = 0) -> float:
    """
    简谐运动速度: v = -Aω·sin(ωt + φ)
    
    Args:
        amplitude: 振幅 (m)
        angular_frequency: 角频率 (rad/s)
        time: 时间 (s)
        phase: 初相位 (rad)
    
    Returns:
        速度 (m/s)
    """
    return -amplitude * angular_frequency * math.sin(angular_frequency * time + phase)


def simple_harmonic_acceleration(amplitude: float, angular_frequency: float, time: float,
                                   phase: float = 0) -> float:
    """
    简谐运动加速度: a = -Aω²·cos(ωt + φ)
    
    Args:
        amplitude: 振幅 (m)
        angular_frequency: 角频率 (rad/s)
        time: 时间 (s)
        phase: 初相位 (rad)
    
    Returns:
        加速度 (m/s²)
    """
    return -amplitude * angular_frequency ** 2 * math.cos(angular_frequency * time + phase)


def pendulum_period(length: float, g: float = STANDARD_GRAVITY) -> float:
    """
    单摆周期: T = 2π√(L/g)
    
    Args:
        length: 摆长 (m)
        g: 重力加速度 (m/s²)
    
    Returns:
        周期 (s)
    """
    if g == 0:
        raise ValueError("重力加速度不能为零")
    return 2 * math.pi * math.sqrt(length / g)


def spring_period(mass: float, spring_constant: float) -> float:
    """
    弹簧振子周期: T = 2π√(m/k)
    
    Args:
        mass: 质量 (kg)
        spring_constant: 弹簧常数 (N/m)
    
    Returns:
        周期 (s)
    """
    if spring_constant == 0:
        raise ValueError("弹簧常数不能为零")
    return 2 * math.pi * math.sqrt(mass / spring_constant)


# ==================== 相对论 ====================

def lorentz_factor(velocity: float) -> float:
    """
    洛伦兹因子: γ = 1/√(1 - v²/c²)
    
    Args:
        velocity: 速度 (m/s)
    
    Returns:
        洛伦兹因子（无量纲）
    """
    if velocity >= SPEED_OF_LIGHT:
        raise ValueError("速度不能达到或超过光速")
    return 1 / math.sqrt(1 - (velocity / SPEED_OF_LIGHT) ** 2)


def time_dilation(proper_time: float, velocity: float) -> float:
    """
    时间膨胀: Δt = γ·Δt₀
    
    Args:
        proper_time: 固有时间 (s)
        velocity: 速度 (m/s)
    
    Returns:
        膨胀后的时间 (s)
    """
    return proper_time * lorentz_factor(velocity)


def length_contraction(proper_length: float, velocity: float) -> float:
    """
    长度收缩: L = L₀/γ
    
    Args:
        proper_length: 固有长度 (m)
        velocity: 速度 (m/s)
    
    Returns:
        收缩后的长度 (m)
    """
    return proper_length / lorentz_factor(velocity)


def relativistic_mass(rest_mass: float, velocity: float) -> float:
    """
    相对论质量: m = γm₀
    
    Args:
        rest_mass: 静止质量 (kg)
        velocity: 速度 (m/s)
    
    Returns:
        相对论质量 (kg)
    """
    return rest_mass * lorentz_factor(velocity)


def relativistic_energy(rest_mass: float) -> float:
    """
    静止能量: E = mc²
    
    Args:
        rest_mass: 静止质量 (kg)
    
    Returns:
        能量 (J)
    """
    return rest_mass * SPEED_OF_LIGHT ** 2


# ==================== 单位换算 ====================

def mph_to_mps(mph: float) -> float:
    """英里每小时转米每秒"""
    return mph * 0.44704


def mps_to_mph(mps: float) -> float:
    """米每秒转英里每小时"""
    return mps / 0.44704


def kmh_to_mps(kmh: float) -> float:
    """千米每小时转米每秒"""
    return kmh / 3.6


def mps_to_kmh(mps: float) -> float:
    """米每秒转千米每小时"""
    return mps * 3.6


def knot_to_mps(knot: float) -> float:
    """节转米每秒"""
    return knot * 0.514444


def mps_to_knot(mps: float) -> float:
    """米每秒转节"""
    return mps / 0.514444


def joule_to_calorie(joule: float) -> float:
    """焦耳转卡路里"""
    return joule / 4.184


def calorie_to_joule(calorie: float) -> float:
    """卡路里转焦耳"""
    return calorie * 4.184


def joule_to_ev(joule: float) -> float:
    """焦耳转电子伏特"""
    return joule / ELECTRON_CHARGE


def ev_to_joule(ev: float) -> float:
    """电子伏特转焦耳"""
    return ev * ELECTRON_CHARGE


def pascal_to_atm(pascal: float) -> float:
    """帕斯卡转标准大气压"""
    return pascal / 101325


def atm_to_pascal(atm: float) -> float:
    """标准大气压转帕斯卡"""
    return atm * 101325


def pascal_to_bar(pascal: float) -> float:
    """帕斯卡转巴"""
    return pascal / 100000


def bar_to_pascal(bar: float) -> float:
    """巴转帕斯卡"""
    return bar * 100000