# PID Controller Utils - PID控制器工具集

一个纯Python实现的PID控制器工具库，零外部依赖，适用于各种自动控制场景。

## 功能特性

- ✅ **标准PID控制器** - 基本的PID控制算法
- ✅ **抗积分饱和PID** - 防止积分饱和问题
- ✅ **增量式PID** - 适用于步进电机等增量控制场景
- ✅ **串级PID控制器** - 主从控制系统
- ✅ **自动整定** - Ziegler-Nichols参数整定方法
- ✅ **多种微分模式** - 基于误差或基于测量值
- ✅ **输出限制** - 支持输出和积分项限制
- ✅ **死区设置** - 避免频繁控制

## 安装

```python
# 直接导入使用，无需安装
from pid_controller_utils.mod import PIDController
```

## 快速开始

### 基本使用

```python
from pid_controller_utils.mod import PIDController

# 创建PID控制器
pid = PIDController(kp=1.0, ki=0.1, kd=0.01)
pid.setpoint = 100.0  # 目标值

# 设置输出限制
pid.set_output_limits(0, 100)

# 在控制循环中使用
while True:
    measurement = get_current_value()  # 获取当前测量值
    output = pid.compute(measurement, dt=0.1)  # 计算输出
    apply_control(output)  # 应用控制输出
```

### 抗积分饱和PID

```python
from pid_controller_utils.mod import AntiWindupPIDController

pid = AntiWindupPIDController(
    kp=2.0,
    ki=0.5,
    kd=0.1,
    anti_windup_method="back_calculation"
)
pid.set_output_limits(-100, 100)
```

### 串级控制

```python
from pid_controller_utils.mod import CascadePIDController, PIDController

# 主控制器（外环）和副控制器（内环）
primary = PIDController(kp=2.0, ki=0.5)
secondary = PIDController(kp=1.0, ki=0.2)

cascade = CascadePIDController(primary, secondary)
cascade.primary_setpoint = 100.0

# 主回路测量值 -> 副回路测量值 -> 输出
output = cascade.compute(primary_meas, secondary_meas, dt=0.1)
```

### 参数自动整定

```python
from pid_controller_utils.mod import PIDController

pid = PIDController()

# 已知临界增益和临界周期
gains = pid.auto_tune_ziegler_nichols(
    ultimate_gain=4.0,    # Ku
    ultimate_period=10.0,  # Tu
    method="classic"       # 整定方法
)
# gains.kp, gains.ki, gains.kd 已自动设置
```

### 增量式PID

```python
from pid_controller_utils.mod import IncrementalPIDController

pid = IncrementalPIDController(kp=1.0, ki=0.1, kd=0.01)
pid.setpoint = 1000.0

# 返回的是控制增量
increment = pid.compute(measurement, dt=0.1)
total_output = pid.get_total_output()  # 累计输出
```

## API参考

### PIDController

主PID控制器类。

**初始化参数：**
- `kp` (float): 比例增益
- `ki` (float): 积分增益
- `kd` (float): 微分增益
- `setpoint` (float): 设定值
- `sample_time` (float, optional): 采样时间
- `mode` (PIDMode): 控制模式（MANUAL/AUTOMATIC）

**方法：**
- `compute(measurement, dt)`: 计算PID输出
- `reset()`: 重置控制器状态
- `set_output_limits(min, max)`: 设置输出限制
- `set_integral_limits(min, max)`: 设置积分项限制
- `auto_tune_ziegler_nichols(ku, tu, method)`: 自动整定参数

**属性：**
- `kp`, `ki`, `kd`: PID增益
- `gains`: PIDGains对象
- `integral_term`: 当前积分项值
- `components`: 各分量字典

### PIDGains

PID增益参数容器。

```python
gains = PIDGains(kp=1.0, ki=0.1, kd=0.01)
arr = gains.to_array()  # (1.0, 0.1, 0.01)
```

### 工厂函数

```python
from pid_controller_utils.mod import create_pid_controller

pid = create_pid_controller(
    kp=1.0,
    ki=0.1,
    kd=0.01,
    controller_type="standard"  # "standard", "anti_windup", "incremental"
)
```

## 控制理论

### PID公式

```
u(t) = Kp * e(t) + Ki * ∫e(t)dt + Kd * de(t)/dt
```

其中：
- `Kp`: 比例增益，控制响应速度
- `Ki`: 积分增益，消除稳态误差
- `Kd`: 微分增益，抑制超调和振荡

### Ziegler-Nichols整定

| 方法 | Kp | Ki | Kd |
|------|-----|-----|-----|
| 经典 | 0.6Ku | 1.2Ku/Tu | 0.075Ku*Tu |
| Pessen | 0.7Ku | 1.75Ku/Tu | 0.105Ku*Tu |
| 无超调 | 0.2Ku | 0.4Ku/Tu | 0.0667Ku*Tu |

## 应用场景

1. **温度控制** - 恒温器、加热器
2. **电机速度控制** - 变频器、伺服
3. **液位控制** - 水箱、反应釜
4. **位置控制** - 机械臂、数控机床
5. **pH控制** - 化工过程
6. **压力控制** - 气动系统

## 测试

```bash
cd Python/pid_controller_utils
python pid_controller_utils_test.py
```

## 许可证

MIT License