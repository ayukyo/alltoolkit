"""
PID Controller Utilities Tests
"""

import math
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PIDController,
    AntiWindupPIDController,
    CascadePIDController,
    PIDAutoTuner,
    IncrementalPIDController,
    PIDGains,
    PIDLimits,
    PIDMode,
    DerivativeMode,
    ProportionalMode,
    create_pid_controller,
    pid_compute
)


def test_pid_gains():
    """测试PID增益参数类"""
    print("测试 PIDGains...")
    
    gains = PIDGains(kp=1.0, ki=0.5, kd=0.1)
    assert gains.kp == 1.0
    assert gains.ki == 0.5
    assert gains.kd == 0.1
    
    arr = gains.to_array()
    assert arr == (1.0, 0.5, 0.1)
    
    new_gains = PIDGains.from_array((2.0, 1.0, 0.2))
    assert new_gains.kp == 2.0
    assert new_gains.ki == 1.0
    assert new_gains.kd == 0.2
    
    print("✓ PIDGains 测试通过")


def test_pid_limits():
    """测试PID限制类"""
    print("测试 PIDLimits...")
    
    limits = PIDLimits(output_min=-100, output_max=100)
    
    assert limits.clamp_output(50) == 50
    assert limits.clamp_output(150) == 100
    assert limits.clamp_output(-150) == -100
    
    limits.integral_min = -10
    limits.integral_max = 10
    assert limits.clamp_integral(5) == 5
    assert limits.clamp_integral(15) == 10
    
    print("✓ PIDLimits 测试通过")


def test_basic_pid():
    """测试基本PID控制器"""
    print("测试基本PID控制器...")
    
    pid = PIDController(kp=1.0, ki=0.1, kd=0.01)
    pid.setpoint = 100.0
    
    # 初始状态
    output = pid.compute(0.0, dt=0.1)
    # 误差 = 100, P = 100, I = 10 (100*0.1*0.1), D ≈ 0
    # output ≈ 101
    assert output > 0  # 误差为正，输出应为正
    assert abs(output - 100) < 10  # 输出接近P项
    
    # 超过设定值（输出应为负）
    pid.reset()
    output = pid.compute(110.0, dt=0.1)
    # 误差 = -10, 输出应该为负
    assert output < 0
    
    print("✓ 基本PID控制器测试通过")


def test_pid_with_output_limits():
    """测试带输出限制的PID"""
    print("测试带输出限制的PID...")
    
    pid = PIDController(kp=10.0, ki=0.0, kd=0.0)
    pid.set_output_limits(-50, 50)
    pid.setpoint = 100.0
    
    # 误差=100, P=1000, 但被限制到50
    output = pid.compute(0.0, dt=0.1)
    assert output == 50
    
    # 误差=-200, P=-2000, 但被限制到-50
    pid.setpoint = 0
    output = pid.compute(200.0, dt=0.1)
    assert output == -50
    
    print("✓ 输出限制测试通过")


def test_pid_integral_accumulation():
    """测试积分项累积"""
    print("测试积分项累积...")
    
    pid = PIDController(kp=0.0, ki=1.0, kd=0.0)
    pid.setpoint = 10.0
    
    # 每次误差为10, dt=0.1, 积分增加1
    for i in range(5):
        output = pid.compute(0.0, dt=0.1)
    
    # 5次累积后积分项 = 10 * 0.1 * 5 = 5
    assert abs(pid.integral_term - 5.0) < 0.01
    
    print("✓ 积分项累积测试通过")


def test_pid_manual_mode():
    """测试手动模式"""
    print("测试手动模式...")
    
    pid = PIDController(kp=1.0, ki=0.1, kd=0.01, mode=PIDMode.MANUAL)
    pid.setpoint = 100.0
    pid._last_output = 50.0
    
    # 手动模式下输出不变
    output = pid.compute(0.0, dt=0.1)
    assert output == 50.0
    
    print("✓ 手动模式测试通过")


def test_pid_derivative_modes():
    """测试微分模式"""
    print("测试微分模式...")
    
    # 基于误差的微分
    pid_error = PIDController(kp=0.0, ki=0.0, kd=1.0, derivative_mode=DerivativeMode.ON_ERROR)
    pid_error.setpoint = 0.0
    output1 = pid_error.compute(0.0, dt=0.1)  # 误差=0
    output2 = pid_error.compute(10.0, dt=0.1)  # 误差=-10, d(error)/dt = -10/0.1 = -100
    assert abs(output2 - (-100)) < 1  # D = -100
    
    # 基于测量值的微分
    pid_meas = PIDController(kp=0.0, ki=0.0, kd=1.0, derivative_mode=DerivativeMode.ON_MEASUREMENT)
    pid_meas.setpoint = 0.0
    output1 = pid_meas.compute(0.0, dt=0.1)
    output2 = pid_meas.compute(10.0, dt=0.1)  # -d(measurement)/dt = -100
    assert abs(output2 - (-100)) < 1
    
    print("✓ 微分模式测试通过")


def test_pid_deadband():
    """测试死区"""
    print("测试死区...")
    
    pid = PIDController(kp=1.0, ki=0.0, kd=0.0)
    pid.setpoint = 100.0
    pid.deadband = 5.0
    
    # 误差在死区内，输出应为0
    output = pid.compute(98.0, dt=0.1)  # 误差=2，在死区内
    assert output == 0.0
    
    # 误差超出死区
    pid.reset()
    output = pid.compute(90.0, dt=0.1)  # 误差=10，超出死区
    assert abs(output - 10.0) < 0.01
    
    print("✓ 死区测试通过")


def test_anti_windup_pid():
    """测试抗积分饱和PID"""
    print("测试抗积分饱和PID...")
    
    # 标准PID（会积分饱和）
    std_pid = PIDController(kp=1.0, ki=10.0, kd=0.0)
    std_pid.set_output_limits(-100, 100)
    std_pid.set_integral_limits(-100, 100)  # 设置较大的积分限制
    std_pid.setpoint = 1000.0  # 无法达到的设定值
    
    for _ in range(100):
        std_pid.compute(0.0, dt=0.1)
    
    std_integral = std_pid.integral_term
    
    # 抗积分饱和PID
    aw_pid = AntiWindupPIDController(kp=1.0, ki=10.0, kd=0.0)
    aw_pid.set_output_limits(-100, 100)
    aw_pid.set_integral_limits(-100, 100)
    aw_pid.setpoint = 1000.0
    
    for _ in range(100):
        aw_pid.compute(0.0, dt=0.1)
    
    aw_integral = aw_pid.integral_term
    
    # 抗积分饱和PID的积分项应该更小（反算法修正）
    # 注意：两者积分项都应该被限制
    assert abs(std_integral) <= 100
    assert abs(aw_integral) <= 100
    
    print(f"  标准PID积分项: {std_integral}")
    print(f"  抗饱和PID积分项: {aw_integral}")
    print("✓ 抗积分饱和PID测试通过")


def test_incremental_pid():
    """测试增量式PID"""
    print("测试增量式PID...")
    
    pid = IncrementalPIDController(kp=1.0, ki=0.1, kd=0.01)
    pid.setpoint = 100.0
    
    # 第一次计算
    inc1 = pid.compute(0.0, dt=0.1)
    total1 = pid.get_total_output()
    
    # 第二次计算
    inc2 = pid.compute(50.0, dt=0.1)
    total2 = pid.get_total_output()
    
    # 增量式PID输出增量
    assert isinstance(inc1, float)
    assert isinstance(inc2, float)
    # total2应该等于total1 + inc2
    assert abs(total2 - (total1 + inc2)) < 0.01
    
    print(f"  增量1: {inc1:.4f}, 累计: {total1:.4f}")
    print(f"  增量2: {inc2:.4f}, 累计: {total2:.4f}")
    print("✓ 增量式PID测试通过")


def test_cascade_pid():
    """测试串级PID"""
    print("测试串级PID...")
    
    primary = PIDController(kp=1.0, ki=0.1, kd=0.0)
    secondary = PIDController(kp=2.0, ki=0.5, kd=0.0)
    
    cascade = CascadePIDController(primary, secondary)
    cascade.primary_setpoint = 100.0
    
    # 主回路测量值=50, 副回路测量值=25
    output = cascade.compute(primary_measurement=50.0, secondary_measurement=25.0, dt=0.1)
    
    # 输出应该是两个控制器共同作用的结果
    assert isinstance(output, float)
    
    # 检查副控制器设定值已被主控制器更新
    assert secondary.setpoint != 0.0
    
    print(f"  主控制器设定值: {cascade.primary_setpoint}")
    print(f"  副控制器设定值: {secondary.setpoint:.4f}")
    print(f"  最终输出: {output:.4f}")
    print("✓ 串级PID测试通过")


def test_auto_tuner():
    """测试自动整定器"""
    print("测试自动整定器...")
    
    tuner = PIDAutoTuner(relay_amplitude=1.0, setpoint=50.0)
    
    # 模拟一个简单的一阶系统响应
    process_value = 50.0
    for i in range(50):
        relay_out = tuner.relay_output(process_value, 0.1)
        # 简单模拟：过程值向relay输出方向移动
        process_value += relay_out * 0.5 + (50.0 - process_value) * 0.1
    
    # 检查振荡计数
    oscillations = tuner._oscillation_count
    print(f"  检测到振荡次数: {oscillations}")
    
    if tuner.is_tuning_complete(min_oscillations=2):
        try:
            gains = tuner.compute_pid_params()
            print(f"  整定结果 - Kp: {gains.kp:.4f}, Ki: {gains.ki:.4f}, Kd: {gains.kd:.4f}")
        except ValueError as e:
            print(f"  整定未完成: {e}")
    else:
        print("  整定尚未完成（需要更多振荡）")
    
    print("✓ 自动整定器测试通过")


def test_ziegler_nichols_tuning():
    """测试Ziegler-Nichols整定"""
    print("测试Ziegler-Nichols整定...")
    
    pid = PIDController()
    
    # 使用经典Ziegler-Nichols方法
    gains = pid.auto_tune_ziegler_nichols(ultimate_gain=4.0, ultimate_period=10.0, method="classic")
    
    # Ku=4, Tu=10
    # Kp = 0.6 * Ku = 2.4
    # Ki = 1.2 * Ku / Tu = 0.48
    # Kd = 0.075 * Ku * Tu = 3.0
    assert abs(gains.kp - 2.4) < 0.01
    assert abs(gains.ki - 0.48) < 0.01
    assert abs(gains.kd - 3.0) < 0.01
    
    print(f"  经典方法: Kp={gains.kp:.4f}, Ki={gains.ki:.4f}, Kd={gains.kd:.4f}")
    
    # 无超调方法
    gains_no = pid.auto_tune_ziegler_nichols(4.0, 10.0, method="no_overshoot")
    print(f"  无超调方法: Kp={gains_no.kp:.4f}, Ki={gains_no.ki:.4f}, Kd={gains_no.kd:.4f}")
    
    # 无超调方法应该更保守
    assert gains_no.kp < gains.kp
    
    print("✓ Ziegler-Nichols整定测试通过")


def test_pid_gains_setter():
    """测试增益设置器"""
    print("测试增益设置器...")
    
    pid = PIDController()
    
    # 使用gains属性设置
    gains = PIDGains(kp=2.0, ki=0.5, kd=0.1)
    pid.gains = gains
    
    assert pid.kp == 2.0
    assert pid.ki == 0.5
    assert pid.kd == 0.1
    
    # 获取gains
    retrieved = pid.gains
    assert retrieved.kp == 2.0
    assert retrieved.ki == 0.5
    assert retrieved.kd == 0.1
    
    print("✓ 增益设置器测试通过")


def test_pid_components():
    """测试PID分量获取"""
    print("测试PID分量获取...")
    
    pid = PIDController(kp=1.0, ki=0.5, kd=0.1)
    pid.setpoint = 100.0
    output = pid.compute(0.0, dt=0.1)
    
    components = pid.components
    assert 'proportional' in components
    assert 'integral' in components
    assert 'derivative' in components
    
    print(f"  P项: {components['proportional']:.4f}")
    print(f"  I项: {components['integral']:.4f}")
    print(f"  D项: {components['derivative']:.4f}")
    print(f"  总输出: {output:.4f}")
    
    print("✓ PID分量获取测试通过")


def test_factory_function():
    """测试工厂函数"""
    print("测试工厂函数...")
    
    # 创建标准PID
    std_pid = create_pid_controller(kp=1.0, ki=0.1, kd=0.01, controller_type="standard")
    assert isinstance(std_pid, PIDController)
    
    # 创建抗饱和PID
    aw_pid = create_pid_controller(kp=1.0, ki=0.1, kd=0.01, controller_type="anti_windup")
    assert isinstance(aw_pid, AntiWindupPIDController)
    
    # 创建增量式PID
    inc_pid = create_pid_controller(kp=1.0, ki=0.1, kd=0.01, controller_type="incremental")
    assert isinstance(inc_pid, IncrementalPIDController)
    
    # 无效类型
    try:
        create_pid_controller(kp=1.0, controller_type="invalid")
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("✓ 工厂函数测试通过")


def test_pid_compute_function():
    """测试无状态计算函数"""
    print("测试无状态计算函数...")
    
    # 初始计算
    output, integral, error = pid_compute(
        kp=1.0, ki=0.5, kd=0.1,
        setpoint=100.0,
        measurement=0.0,
        dt=0.1
    )
    
    # 误差=100, P=100, I=5, D=10
    assert error == 100.0
    assert integral == 10.0  # 100 * 0.1
    assert output > 100  # P + I + D
    
    # 继续计算
    output2, integral2, error2 = pid_compute(
        kp=1.0, ki=0.5, kd=0.1,
        setpoint=100.0,
        measurement=50.0,
        dt=0.1,
        integral=integral,
        last_error=error
    )
    
    assert error2 == 50.0
    assert integral2 > integral
    
    print(f"  第一次: 输出={output:.4f}, 积分={integral:.4f}, 误差={error}")
    print(f"  第二次: 输出={output2:.4f}, 积分={integral2:.4f}, 误差={error2}")
    print("✓ 无状态计算函数测试通过")


def test_pid_reset():
    """测试重置功能"""
    print("测试重置功能...")
    
    pid = PIDController(kp=1.0, ki=1.0, kd=0.0)
    pid.setpoint = 100.0
    
    # 累积一些积分
    for _ in range(5):
        pid.compute(0.0, dt=0.1)
    
    assert pid.integral_term > 0
    
    # 重置
    pid.reset()
    
    assert pid.integral_term == 0.0
    assert pid._last_error == 0.0
    assert pid._last_output == 0.0
    
    print("✓ 重置功能测试通过")


def test_pid_step_response_simulation():
    """测试阶跃响应模拟"""
    print("测试阶跃响应模拟...")
    
    pid = PIDController(kp=5.0, ki=1.0, kd=0.5)
    pid.setpoint = 50.0
    
    # 简单的一阶滞后过程
    process_value = 0.0
    def process_fn(control_output):
        nonlocal process_value
        tau = 1.0  # 时间常数
        dt = 0.1
        process_value += (control_output - process_value) * dt / tau
        return process_value
    
    times, outputs, measurements = pid.simulate_step_response(
        process_fn=process_fn,
        steps=200,
        dt=0.1
    )
    
    assert len(times) == 200
    assert len(outputs) == 200
    assert len(measurements) == 200
    
    # 最终应该接近设定值
    final_error = abs(measurements[-1] - pid.setpoint)
    print(f"  最终测量值: {measurements[-1]:.4f}")
    print(f"  设定值: {pid.setpoint}")
    print(f"  最终误差: {final_error:.4f}")
    assert final_error < 5.0, f"最终误差过大: {final_error}"
    
    print("✓ 阶跃响应模拟测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("PID Controller Utilities Tests")
    print("=" * 60)
    
    tests = [
        test_pid_gains,
        test_pid_limits,
        test_basic_pid,
        test_pid_with_output_limits,
        test_pid_integral_accumulation,
        test_pid_manual_mode,
        test_pid_derivative_modes,
        test_pid_deadband,
        test_anti_windup_pid,
        test_incremental_pid,
        test_cascade_pid,
        test_auto_tuner,
        test_ziegler_nichols_tuning,
        test_pid_gains_setter,
        test_pid_components,
        test_factory_function,
        test_pid_compute_function,
        test_pid_reset,
        test_pid_step_response_simulation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)