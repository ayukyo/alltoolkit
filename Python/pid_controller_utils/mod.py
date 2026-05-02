"""
PID Controller Utilities - PID控制器工具集

提供多种PID控制器实现，用于自动控制系统。

功能：
- 标准PID控制器
- 带抗积分饱和的PID控制器
- 带死区的PID控制器
- 串级PID控制器
- PID参数自动整定（Ziegler-Nichols方法）
"""

from typing import Optional, Callable, Tuple, List
from dataclasses import dataclass, field
from enum import Enum
import math


class PIDMode(Enum):
    """PID控制器模式"""
    MANUAL = "manual"  # 手动模式
    AUTOMATIC = "automatic"  # 自动模式


class DerivativeMode(Enum):
    """微分项模式"""
    ON_MEASUREMENT = "on_measurement"  # 基于测量值的微分（避免设定值变化引起的微分冲击）
    ON_ERROR = "on_error"  # 基于误差的微分


class ProportionalMode(Enum):
    """比例项模式"""
    ON_MEASUREMENT = "on_measurement"  # 基于测量值的比例（减少设定值变化冲击）
    ON_ERROR = "on_error"  # 基于误差的比例


@dataclass
class PIDGains:
    """PID增益参数"""
    kp: float  # 比例增益
    ki: float  # 积分增益
    kd: float  # 微分增益
    
    def to_array(self) -> Tuple[float, float, float]:
        """转换为元组"""
        return (self.kp, self.ki, self.kd)
    
    @classmethod
    def from_array(cls, arr: Tuple[float, float, float]) -> 'PIDGains':
        """从元组创建"""
        return cls(kp=arr[0], ki=arr[1], kd=arr[2])


@dataclass
class PIDLimits:
    """PID输出限制"""
    output_min: float = -float('inf')
    output_max: float = float('inf')
    integral_min: Optional[float] = None  # 积分项下限
    integral_max: Optional[float] = None  # 积分项上限
    
    def clamp_output(self, value: float) -> float:
        """限制输出值"""
        return max(self.output_min, min(self.output_max, value))
    
    def clamp_integral(self, value: float) -> float:
        """限制积分项"""
        if self.integral_min is None or self.integral_max is None:
            return value
        return max(self.integral_min, min(self.integral_max, value))


class PIDController:
    """
    标准PID控制器
    
    实现基本的PID控制算法：
    output = Kp * e(t) + Ki * ∫e(t)dt + Kd * de(t)/dt
    
    使用示例：
        pid = PIDController(kp=1.0, ki=0.1, kd=0.01)
        pid.setpoint = 100
        
        # 在控制循环中
        output = pid.compute(measured_value, dt)
    """
    
    def __init__(
        self,
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        setpoint: float = 0.0,
        sample_time: Optional[float] = None,
        mode: PIDMode = PIDMode.AUTOMATIC,
        proportional_mode: ProportionalMode = ProportionalMode.ON_ERROR,
        derivative_mode: DerivativeMode = DerivativeMode.ON_MEASUREMENT
    ):
        """
        初始化PID控制器
        
        Args:
            kp: 比例增益
            ki: 积分增益
            kd: 微分增益
            setpoint: 设定值
            sample_time: 采样时间（秒），None表示手动提供dt
            mode: 控制模式
            proportional_mode: 比例项模式
            derivative_mode: 微分项模式
        """
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self.setpoint = setpoint
        self.sample_time = sample_time
        self.mode = mode
        self.proportional_mode = proportional_mode
        self.derivative_mode = derivative_mode
        
        # 内部状态
        self._integral = 0.0
        self._last_error = 0.0
        self._last_measurement = 0.0
        self._last_output = 0.0
        self._last_time: Optional[float] = None
        self._initialized = False
        
        # 输出限制
        self.limits = PIDLimits()
        
        # 死区设置
        self.deadband = 0.0
    
    @property
    def kp(self) -> float:
        """比例增益"""
        return self._kp
    
    @kp.setter
    def kp(self, value: float):
        self._kp = value
    
    @property
    def ki(self) -> float:
        """积分增益"""
        return self._ki
    
    @ki.setter
    def ki(self, value: float):
        self._ki = value
    
    @property
    def kd(self) -> float:
        """微分增益"""
        return self._kd
    
    @kd.setter
    def kd(self, value: float):
        self._kd = value
    
    @property
    def gains(self) -> PIDGains:
        """获取增益参数"""
        return PIDGains(self._kp, self._ki, self._kd)
    
    @gains.setter
    def gains(self, gains: PIDGains):
        """设置增益参数"""
        self._kp = gains.kp
        self._ki = gains.ki
        self._kd = gains.kd
    
    @property
    def integral_term(self) -> float:
        """当前积分项值"""
        return self._integral
    
    @property
    def components(self) -> dict:
        """获取PID各分量"""
        return {
            'proportional': self._last_p,
            'integral': self._last_i,
            'derivative': self._last_d
        }
    
    def set_output_limits(self, min_val: float, max_val: float):
        """设置输出限制"""
        self.limits.output_min = min_val
        self.limits.output_max = max_val
    
    def set_integral_limits(self, min_val: float, max_val: float):
        """设置积分项限制"""
        self.limits.integral_min = min_val
        self.limits.integral_max = max_val
    
    def compute(self, measurement: float, dt: Optional[float] = None) -> float:
        """
        计算PID输出
        
        Args:
            measurement: 测量值
            dt: 时间步长（秒），如果未设置sample_time则必须提供
            
        Returns:
            PID控制器输出
        """
        if self.mode == PIDMode.MANUAL:
            return self._last_output
        
        # 确定时间步长
        if dt is None:
            dt = self.sample_time
            if dt is None:
                raise ValueError("必须提供dt或设置sample_time")
        
        # 计算误差
        error = self.setpoint - measurement
        
        # 应用死区
        if abs(error) < self.deadband:
            error = 0.0
        
        # 比例项
        if self.proportional_mode == ProportionalMode.ON_ERROR:
            p_term = self._kp * error
        else:
            p_term = -self._kp * (measurement - self._last_measurement)
        
        # 积分项（带抗饱和）
        self._integral += error * dt
        self._integral = self.limits.clamp_integral(self._integral)
        i_term = self._ki * self._integral
        
        # 微分项
        if self.derivative_mode == DerivativeMode.ON_ERROR:
            d_term = self._kd * (error - self._last_error) / dt if dt > 0 else 0.0
        else:
            d_term = -self._kd * (measurement - self._last_measurement) / dt if dt > 0 else 0.0
        
        # 计算输出
        output = p_term + i_term + d_term
        output = self.limits.clamp_output(output)
        
        # 保存状态
        self._last_error = error
        self._last_measurement = measurement
        self._last_output = output
        self._last_p = p_term
        self._last_i = i_term
        self._last_d = d_term
        self._initialized = True
        
        return output
    
    def reset(self):
        """重置控制器状态"""
        self._integral = 0.0
        self._last_error = 0.0
        self._last_measurement = 0.0
        self._last_output = 0.0
        self._last_time = None
        self._initialized = False
    
    def auto_tune_ziegler_nichols(
        self,
        ultimate_gain: float,
        ultimate_period: float,
        method: str = "classic"
    ) -> PIDGains:
        """
        Ziegler-Nichols参数整定
        
        Args:
            ultimate_gain: 临界增益（Ku）- 使系统产生持续振荡的增益
            ultimate_period: 临界周期（Tu）- 振荡周期
            method: 整定方法
                - "classic": 经典Ziegler-Nichols
                - "pessen": Pessen积分规则
                - "no_overshoot": 无超调规则
                
        Returns:
            整定后的PID增益参数
        """
        ku = ultimate_gain
        tu = ultimate_period
        
        if method == "classic":
            kp = 0.6 * ku
            ki = 1.2 * ku / tu
            kd = 0.075 * ku * tu
        elif method == "pessen":
            kp = 0.7 * ku
            ki = 1.75 * ku / tu
            kd = 0.105 * ku * tu
        elif method == "no_overshoot":
            kp = 0.2 * ku
            ki = 0.4 * ku / tu
            kd = 0.0667 * ku * tu
        else:
            raise ValueError(f"未知的整定方法: {method}")
        
        gains = PIDGains(kp=kp, ki=ki, kd=kd)
        self.gains = gains
        return gains
    
    def simulate_step_response(
        self,
        process_fn: Callable[[float], float],
        steps: int = 100,
        dt: float = 0.1
    ) -> Tuple[List[float], List[float], List[float]]:
        """
        模拟阶跃响应
        
        Args:
            process_fn: 过程函数，接收控制输出，返回测量值
            steps: 模拟步数
            dt: 时间步长
            
        Returns:
            (时间序列, 输出序列, 测量值序列)
        """
        times = []
        outputs = []
        measurements = []
        
        self.reset()
        
        for i in range(steps):
            t = i * dt
            measurement = process_fn(self._last_output)
            output = self.compute(measurement, dt)
            
            times.append(t)
            outputs.append(output)
            measurements.append(measurement)
        
        return times, outputs, measurements


class AntiWindupPIDController(PIDController):
    """
    带抗积分饱和的PID控制器
    
    当输出达到限制时，停止积分项累加，防止积分饱和。
    """
    
    def __init__(
        self,
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        setpoint: float = 0.0,
        anti_windup_method: str = "back_calculation",
        back_calculation_coefficient: float = 1.0,
        **kwargs
    ):
        """
        Args:
            kp, ki, kd, setpoint: 同PIDController
            anti_windup_method: 抗饱和方法
                - "back_calculation": 反算法
                - "clamping": 钳位法
            back_calculation_coefficient: 反算法系数（Kb）
        """
        super().__init__(kp, ki, kd, setpoint, **kwargs)
        self.anti_windup_method = anti_windup_method
        self.back_calculation_coefficient = back_calculation_coefficient
    
    def compute(self, measurement: float, dt: Optional[float] = None) -> float:
        """计算PID输出（带抗积分饱和）"""
        if self.mode == PIDMode.MANUAL:
            return self._last_output
        
        if dt is None:
            dt = self.sample_time
            if dt is None:
                raise ValueError("必须提供dt或设置sample_time")
        
        error = self.setpoint - measurement
        
        if abs(error) < self.deadband:
            error = 0.0
        
        # 比例项
        if self.proportional_mode == ProportionalMode.ON_ERROR:
            p_term = self._kp * error
        else:
            p_term = -self._kp * (measurement - self._last_measurement)
        
        # 积分项（带抗饱和）
        if self.anti_windup_method == "back_calculation":
            # 计算预限制输出
            pre_output = p_term + self._ki * self._integral + self._kd * (error - self._last_error) / dt if dt > 0 else p_term + self._ki * self._integral
            output = self.limits.clamp_output(pre_output)
            
            # 反算积分修正
            windup_error = (output - pre_output) * self.back_calculation_coefficient
            self._integral += (error - windup_error) * dt
        else:  # clamping
            # 只有当输出未饱和且误差与积分同向时才积分
            should_integrate = True
            
            # 检查是否饱和
            pre_integral = self._integral + error * dt
            pre_output = p_term + self._ki * pre_integral
            
            if pre_output > self.limits.output_max and error > 0:
                should_integrate = False
            elif pre_output < self.limits.output_min and error < 0:
                should_integrate = False
            
            if should_integrate:
                self._integral = pre_integral
        
        self._integral = self.limits.clamp_integral(self._integral)
        i_term = self._ki * self._integral
        
        # 微分项
        if self.derivative_mode == DerivativeMode.ON_ERROR:
            d_term = self._kd * (error - self._last_error) / dt if dt > 0 else 0.0
        else:
            d_term = -self._kd * (measurement - self._last_measurement) / dt if dt > 0 else 0.0
        
        output = p_term + i_term + d_term
        output = self.limits.clamp_output(output)
        
        self._last_error = error
        self._last_measurement = measurement
        self._last_output = output
        self._last_p = p_term
        self._last_i = i_term
        self._last_d = d_term
        
        return output


class CascadePIDController:
    """
    串级PID控制器
    
    由主控制器（外环）和副控制器（内环）组成。
    主控制器的输出作为副控制器的设定值。
    
    使用示例：
        primary = PIDController(kp=1.0, ki=0.1)
        secondary = PIDController(kp=2.0, ki=0.5)
        cascade = CascadePIDController(primary, secondary)
        
        cascade.primary_setpoint = 100
        output = cascade.compute(primary_measurement, secondary_measurement, dt)
    """
    
    def __init__(
        self,
        primary_controller: PIDController,
        secondary_controller: PIDController,
        primary_to_secondary_scale: float = 1.0
    ):
        """
        Args:
            primary_controller: 主控制器
            secondary_controller: 副控制器
            primary_to_secondary_scale: 主控制器输出到副控制器设定值的比例系数
        """
        self.primary = primary_controller
        self.secondary = secondary_controller
        self.scale = primary_to_secondary_scale
    
    @property
    def primary_setpoint(self) -> float:
        """主控制器设定值"""
        return self.primary.setpoint
    
    @primary_setpoint.setter
    def primary_setpoint(self, value: float):
        self.primary.setpoint = value
    
    def compute(
        self,
        primary_measurement: float,
        secondary_measurement: float,
        dt: Optional[float] = None
    ) -> float:
        """
        计算串级控制输出
        
        Args:
            primary_measurement: 主回路测量值
            secondary_measurement: 副回路测量值
            dt: 时间步长
            
        Returns:
            控制输出
        """
        # 主控制器输出作为副控制器设定值
        primary_output = self.primary.compute(primary_measurement, dt)
        self.secondary.setpoint = primary_output * self.scale
        
        # 副控制器输出
        secondary_output = self.secondary.compute(secondary_measurement, dt)
        
        return secondary_output
    
    def reset(self):
        """重置两个控制器"""
        self.primary.reset()
        self.secondary.reset()


class PIDAutoTuner:
    """
    PID参数自动整定器
    
    使用继电器反馈法自动确定临界增益和临界周期，
    然后使用Ziegler-Nichols方法计算PID参数。
    """
    
    def __init__(
        self,
        relay_amplitude: float = 1.0,
        setpoint: float = 0.0,
        hysteresis: float = 0.0
    ):
        """
        Args:
            relay_amplitude: 继电器振幅
            setpoint: 设定值
            hysteresis: 滞后值（防止噪声）
        """
        self.relay_amplitude = relay_amplitude
        self.setpoint = setpoint
        self.hysteresis = hysteresis
        
        self._peaks: List[Tuple[float, float]] = []  # (time, value)
        self._last_time: Optional[float] = None
        self._last_output: float = 0.0
        self._time: float = 0.0
        self._oscillation_count: int = 0
        self._last_crossing_time: Optional[float] = None
        self._crossings: List[float] = []
    
    def relay_output(self, measurement: float, dt: float) -> float:
        """
        生成继电器输出用于激励系统振荡
        
        Args:
            measurement: 测量值
            dt: 时间步长
            
        Returns:
            继电器输出
        """
        self._time += dt
        error = measurement - self.setpoint
        
        # 带滞后的继电器
        if error > self.hysteresis:
            output = -self.relay_amplitude
        elif error < -self.hysteresis:
            output = self.relay_amplitude
        else:
            output = self._last_output
        
        # 检测过零点
        prev_error = getattr(self, '_prev_error', 0)
        if prev_error * error < 0:  # 过零
            if self._last_crossing_time is not None:
                self._crossings.append(self._time - self._last_crossing_time)
            self._last_crossing_time = self._time
            self._oscillation_count += 1
        
        self._prev_error = error
        self._last_output = output
        return output
    
    def is_tuning_complete(self, min_oscillations: int = 4) -> bool:
        """检查整定是否完成"""
        return self._oscillation_count >= min_oscillations
    
    def get_tuning_results(self) -> Tuple[float, float]:
        """
        获取整定结果
        
        Returns:
            (ultimate_gain, ultimate_period)
            
        Raises:
            ValueError: 如果振荡次数不足
        """
        if len(self._crossings) < 2:
            raise ValueError("振荡次数不足，无法计算整定参数")
        
        # 计算平均周期
        avg_period = sum(self._crossings) / len(self._crossings) * 2
        
        # 计算临界增益 (使用描述函数法)
        # Ku = 4 * d / (π * a), 其中d是继电器振幅，a是振荡振幅
        # 这里简化处理
        ultimate_gain = 4 * self.relay_amplitude / (math.pi * self.relay_amplitude * 0.5)
        ultimate_period = avg_period
        
        return ultimate_gain, ultimate_period
    
    def compute_pid_params(
        self,
        method: str = "classic"
    ) -> PIDGains:
        """
        计算PID参数
        
        Args:
            method: 整定方法
            
        Returns:
            PID增益参数
        """
        ku, tu = self.get_tuning_results()
        
        pid = PIDController()
        return pid.auto_tune_ziegler_nichols(ku, tu, method)
    
    def reset(self):
        """重置整定器"""
        self._peaks = []
        self._last_time = None
        self._last_output = 0.0
        self._time = 0.0
        self._oscillation_count = 0
        self._last_crossing_time = None
        self._crossings = []


class IncrementalPIDController:
    """
    增量式PID控制器
    
    输出的是控制量的增量，而不是绝对值。
    适用于需要增量控制的场合，如步进电机控制。
    """
    
    def __init__(
        self,
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        setpoint: float = 0.0
    ):
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self.setpoint = setpoint
        
        self._prev_error = 0.0
        self._prev_prev_error = 0.0
        self._last_increment = 0.0
        self._total_output = 0.0
        
        self.output_min = -float('inf')
        self.output_max = float('inf')
    
    def compute(self, measurement: float, dt: float = 1.0) -> float:
        """
        计算增量输出
        
        Args:
            measurement: 测量值
            dt: 时间步长
            
        Returns:
            输出增量
        """
        error = self.setpoint - measurement
        
        # 增量式PID公式
        # Δu = Kp*(e(k) - e(k-1)) + Ki*e(k)*dt + Kd*(e(k) - 2*e(k-1) + e(k-2))/dt
        p_increment = self._kp * (error - self._prev_error)
        i_increment = self._ki * error * dt
        d_increment = self._kd * (error - 2 * self._prev_error + self._prev_prev_error) / dt if dt > 0 else 0
        
        increment = p_increment + i_increment + d_increment
        
        self._prev_prev_error = self._prev_error
        self._prev_error = error
        self._last_increment = increment
        self._total_output += increment
        self._total_output = max(self.output_min, min(self.output_max, self._total_output))
        
        return increment
    
    def get_total_output(self) -> float:
        """获取累计输出"""
        return self._total_output
    
    def reset(self):
        """重置控制器"""
        self._prev_error = 0.0
        self._prev_prev_error = 0.0
        self._last_increment = 0.0
        self._total_output = 0.0


def create_pid_controller(
    kp: float,
    ki: float = 0.0,
    kd: float = 0.0,
    controller_type: str = "standard",
    **kwargs
) -> PIDController:
    """
    创建PID控制器的工厂函数
    
    Args:
        kp: 比例增益
        ki: 积分增益
        kd: 微分增益
        controller_type: 控制器类型
            - "standard": 标准PID
            - "anti_windup": 抗积分饱和PID
            - "incremental": 增量式PID
        **kwargs: 其他参数
        
    Returns:
        PID控制器实例
    """
    if controller_type == "standard":
        return PIDController(kp, ki, kd, **kwargs)
    elif controller_type == "anti_windup":
        return AntiWindupPIDController(kp, ki, kd, **kwargs)
    elif controller_type == "incremental":
        return IncrementalPIDController(kp, ki, kd, **kwargs)
    else:
        raise ValueError(f"未知的控制器类型: {controller_type}")


# 便捷函数
def pid_compute(
    kp: float,
    ki: float,
    kd: float,
    setpoint: float,
    measurement: float,
    dt: float,
    integral: float = 0.0,
    last_error: float = 0.0
) -> Tuple[float, float, float]:
    """
    单次PID计算（无状态）
    
    Args:
        kp, ki, kd: PID增益
        setpoint: 设定值
        measurement: 测量值
        dt: 时间步长
        integral: 积分项累积值
        last_error: 上次误差
        
    Returns:
        (输出, 新积分值, 新误差)
    """
    error = setpoint - measurement
    integral += error * dt
    derivative = (error - last_error) / dt if dt > 0 else 0.0
    
    output = kp * error + ki * integral + kd * derivative
    
    return output, integral, error


# 导出
__all__ = [
    'PIDMode',
    'DerivativeMode', 
    'ProportionalMode',
    'PIDGains',
    'PIDLimits',
    'PIDController',
    'AntiWindupPIDController',
    'CascadePIDController',
    'PIDAutoTuner',
    'IncrementalPIDController',
    'create_pid_controller',
    'pid_compute'
]