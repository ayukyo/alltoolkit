"""
PID控制器使用示例

演示如何使用pid_controller_utils进行自动控制。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PIDController,
    AntiWindupPIDController,
    CascadePIDController,
    IncrementalPIDController,
    PIDAutoTuner,
    PIDGains,
    PIDMode,
    create_pid_controller
)


def example_basic_pid():
    """示例1: 基本PID控制"""
    print("\n" + "=" * 50)
    print("示例1: 基本PID控制")
    print("=" * 50)
    
    # 创建PID控制器
    # Kp: 比例增益 - 控制响应速度
    # Ki: 积分增益 - 消除稳态误差
    # Kd: 微分增益 - 抑制超调
    pid = PIDController(kp=2.0, ki=0.5, kd=0.1)
    pid.setpoint = 25.0  # 目标温度25度
    
    # 设置输出限制（例如加热器功率0-100%）
    pid.set_output_limits(0, 100)
    
    print(f"目标温度: {pid.setpoint}°C")
    print("-" * 50)
    
    # 模拟温度控制过程
    temperature = 20.0  # 初始温度
    
    for i in range(20):
        # 计算控制输出
        output = pid.compute(temperature, dt=0.1)
        
        # 模拟温度变化（简单的一阶滞后模型）
        ambient = 20.0
        tau = 2.0  # 时间常数
        dt = 0.1
        temperature += (output * 0.1 - (temperature - ambient)) * dt / tau
        
        print(f"步 {i+1:2d}: 温度={temperature:.2f}°C, 输出={output:.1f}%")
    
    print(f"\n最终温度: {temperature:.2f}°C (目标: {pid.setpoint}°C)")


def example_temperature_control():
    """示例2: 温度控制系统"""
    print("\n" + "=" * 50)
    print("示例2: 温度控制系统（带抗积分饱和）")
    print("=" * 50)
    
    # 使用抗积分饱和PID控制器
    pid = AntiWindupPIDController(
        kp=5.0,
        ki=1.0,
        kd=0.2,
        anti_windup_method="back_calculation",
        back_calculation_coefficient=1.0
    )
    pid.setpoint = 100.0  # 目标温度100度
    pid.set_output_limits(0, 100)  # 加热器功率限制
    
    print(f"目标温度: {pid.setpoint}°C")
    print("-" * 50)
    
    # 模拟加热过程
    temperature = 25.0  # 室温
    ambient = 25.0
    
    for i in range(30):
        output = pid.compute(temperature, dt=0.5)
        
        # 加热模型
        heat_rate = output * 0.5  # 加热速率
        cool_rate = (temperature - ambient) * 0.1  # 散热速率
        temperature += (heat_rate - cool_rate) * 0.5
        
        if i % 3 == 0:
            print(f"时间 {i*0.5:4.1f}s: 温度={temperature:.1f}°C, 功率={output:.1f}%")
    
    print(f"\n最终温度: {temperature:.2f}°C")


def example_motor_speed_control():
    """示例3: 电机速度控制"""
    print("\n" + "=" * 50)
    print("示例3: 电机速度控制（增量式PID）")
    print("=" * 50)
    
    # 增量式PID适合电机控制
    pid = IncrementalPIDController(kp=0.5, ki=0.1, kd=0.05)
    pid.setpoint = 1000.0  # 目标RPM
    pid.output_min = -50  # 最小调整量
    pid.output_max = 50   # 最大调整量
    
    print(f"目标转速: {pid.setpoint} RPM")
    print("-" * 50)
    
    speed = 0.0
    pwm = 50.0  # 初始PWM占空比
    
    for i in range(25):
        increment = pid.compute(speed, dt=0.02)
        pwm += increment
        pwm = max(0, min(100, pwm))  # PWM限制
        
        # 模拟电机响应
        load = 20.0  # 负载
        speed += (pwm * 15 - speed - load) * 0.1
        
        if i % 5 == 0:
            print(f"步 {i+1:2d}: 转速={speed:.0f} RPM, PWM={pwm:.1f}%, 增量={increment:.2f}")
    
    print(f"\n最终转速: {speed:.0f} RPM")


def example_cascade_control():
    """示例4: 串级控制（液位控制）"""
    print("\n" + "=" * 50)
    print("示例4: 串级控制（液位-流量控制）")
    print("=" * 50)
    
    # 主控制器：液位控制
    primary = PIDController(kp=2.0, ki=0.5, kd=0.0)
    primary.set_output_limits(0, 100)  # 流量设定值限制
    
    # 副控制器：流量控制
    secondary = PIDController(kp=1.0, ki=0.2, kd=0.0)
    secondary.set_output_limits(0, 100)  # 阀门开度限制
    
    # 串级控制器
    cascade = CascadePIDController(primary, secondary)
    cascade.primary_setpoint = 50.0  # 目标液位
    
    print(f"目标液位: {cascade.primary_setpoint}%")
    print("-" * 50)
    
    level = 30.0  # 初始液位
    flow = 20.0   # 初始流量
    tank_area = 10.0  # 水箱截面积
    
    for i in range(20):
        # 主回路：液位 -> 流量设定值
        # 副回路：流量 -> 阀门开度
        valve = cascade.compute(level, flow, dt=0.5)
        
        # 模拟流量变化
        flow += (valve * 0.5 - flow) * 0.3
        
        # 模拟液位变化
        outflow = 10.0  # 出水流量
        level += (flow - outflow) * 0.5 / tank_area
        level = max(0, min(100, level))
        
        if i % 4 == 0:
            print(f"步 {i+1:2d}: 液位={level:.1f}%, 流量={flow:.1f}L/min, 阀门={valve:.1f}%")
    
    print(f"\n最终液位: {level:.1f}%")


def example_auto_tuning():
    """示例5: PID参数自动整定"""
    print("\n" + "=" * 50)
    print("示例5: PID参数自动整定")
    print("=" * 50)
    
    # 创建整定器
    tuner = PIDAutoTuner(relay_amplitude=10.0, setpoint=50.0)
    
    print("开始继电器反馈整定...")
    print("-" * 50)
    
    # 模拟系统响应
    process_value = 50.0
    time = 0.0
    
    for i in range(60):
        relay_out = tuner.relay_output(process_value, 0.1)
        time += 0.1
        
        # 简单的一阶加滞后模型
        tau = 2.0
        delay = 0.3
        process_value += (relay_out * 0.2 - (process_value - 50.0) * 0.1) * 0.1 / tau
        
        if i % 10 == 0:
            print(f"时间 {time:.1f}s: 输出={relay_out:.1f}, 测量={process_value:.1f}")
    
    if tuner.is_tuning_complete(min_oscillations=2):
        gains = tuner.compute_pid_params(method="classic")
        print(f"\n整定结果:")
        print(f"  Kp = {gains.kp:.4f}")
        print(f"  Ki = {gains.ki:.4f}")
        print(f"  Kd = {gains.kd:.4f}")
        
        # 使用整定参数创建控制器
        pid = PIDController()
        pid.gains = gains
        pid.setpoint = 50.0
        print(f"\n已应用整定参数到控制器")
    else:
        print("整定未完成")


def example_position_control():
    """示例6: 位置控制"""
    print("\n" + "=" * 50)
    print("示例6: 机械臂位置控制")
    print("=" * 50)
    
    # 位置控制器
    pid = PIDController(
        kp=10.0,
        ki=0.5,
        kd=2.0,
        proportional_mode=PIDMode.ON_ERROR,  # 基于误差的比例
        derivative_mode=PIDMode.AUTOMATIC  # 自动模式
    )
    
    # 使用死区避免抖动
    pid.deadband = 0.5  # 0.5mm死区
    pid.set_output_limits(-100, 100)  # 电机速度限制
    pid.setpoint = 100.0  # 目标位置100mm
    
    print(f"目标位置: {pid.setpoint}mm")
    print("-" * 50)
    
    position = 0.0
    velocity = 0.0
    
    for i in range(30):
        output = pid.compute(position, dt=0.01)
        
        # 模拟电机和机械臂动力学
        mass = 1.0
        friction = 0.5
        acceleration = (output - friction * velocity) / mass
        velocity += acceleration * 0.01
        position += velocity * 0.01
        
        if i % 5 == 0:
            print(f"时间 {i*0.01:.2f}s: 位置={position:.2f}mm, 速度={velocity:.1f}mm/s")
    
    print(f"\n最终位置: {position:.2f}mm (目标: {pid.setpoint}mm)")


def example_ph_control():
    """示例7: pH值控制"""
    print("\n" + "=" * 50)
    print("示例7: pH值控制（慢速过程）")
    print("=" * 50)
    
    # pH控制通常是慢速过程，需要较大的积分作用
    pid = PIDController(kp=0.5, ki=0.1, kd=0.0)
    pid.setpoint = 7.0  # 目标pH值
    pid.set_output_limits(-10, 10)  # 酸/碱添加速率
    pid.set_integral_limits(-5, 5)  # 积分限制
    
    print(f"目标pH值: {pid.setpoint}")
    print("-" * 50)
    
    ph = 5.0  # 初始酸性
    buffer_capacity = 0.01  # 缓冲容量
    
    for i in range(40):
        # 添加碱（正值）或酸（负值）
        addition_rate = pid.compute(ph, dt=1.0)
        
        # pH变化模型（简化）
        ph += addition_rate * buffer_capacity
        ph = max(0, min(14, ph))
        
        if i % 8 == 0:
            acid_base = "碱" if addition_rate > 0 else "酸" if addition_rate < 0 else "无"
            print(f"步 {i+1:2d}: pH={ph:.2f}, 添加={abs(addition_rate):.2f}mL/s ({acid_base})")
    
    print(f"\n最终pH值: {ph:.2f}")


def example_multi_setpoint():
    """示例8: 多设定值切换"""
    print("\n" + "=" * 50)
    print("示例8: 多设定值切换控制")
    print("=" * 50)
    
    pid = PIDController(kp=1.0, ki=0.3, kd=0.1)
    pid.set_output_limits(0, 100)
    
    # 设定值序列
    setpoints = [20.0, 50.0, 30.0, 80.0]
    current_value = 25.0
    
    print("设定值切换测试:")
    print("-" * 50)
    
    for target in setpoints:
        pid.setpoint = target
        pid.reset()  # 切换设定值时重置积分
        
        print(f"\n新目标: {target}")
        
        for step in range(15):
            output = pid.compute(current_value, dt=0.1)
            
            # 简单响应模型
            current_value += (output * 0.5 - (current_value - 20) * 0.1) * 0.1
            
            if step % 5 == 0:
                print(f"  步 {step:2d}: 值={current_value:.1f}, 输出={output:.1f}")
        
        print(f"  → 达到: {current_value:.1f}")


def example_factory_function():
    """示例9: 使用工厂函数创建控制器"""
    print("\n" + "=" * 50)
    print("示例9: 工厂函数创建控制器")
    print("=" * 50)
    
    # 创建不同类型的控制器
    controllers = {
        "标准PID": create_pid_controller(kp=1.0, ki=0.1, kd=0.01, controller_type="standard"),
        "抗饱和PID": create_pid_controller(kp=1.0, ki=0.1, kd=0.01, controller_type="anti_windup"),
        "增量式PID": create_pid_controller(kp=1.0, ki=0.1, kd=0.01, controller_type="incremental"),
    }
    
    setpoint = 50.0
    measurement = 30.0
    
    print(f"设定值: {setpoint}, 测量值: {measurement}")
    print("-" * 50)
    
    for name, ctrl in controllers.items():
        ctrl.setpoint = setpoint
        if hasattr(ctrl, 'set_output_limits'):
            ctrl.set_output_limits(-100, 100)
        
        output = ctrl.compute(measurement, dt=0.1)
        print(f"{name}: 输出 = {output:.2f}")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("PID控制器工具集 - 使用示例")
    print("=" * 50)
    
    examples = [
        example_basic_pid,
        example_temperature_control,
        example_motor_speed_control,
        example_cascade_control,
        example_auto_tuning,
        example_position_control,
        example_ph_control,
        example_multi_setpoint,
        example_factory_function,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例 {example.__name__} 执行错误: {e}")
    
    print("\n" + "=" * 50)
    print("所有示例执行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()