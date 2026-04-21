# 四元数工具模块 (Quaternion Utils)

纯 Python 实现的四元数库，用于 3D 旋转计算。零外部依赖。

## 功能特性

- ✅ **基本运算**：加、减、乘、除、共轭、逆、模长
- ✅ **旋转操作**：向量旋转、轴角转换、欧拉角转换、旋转矩阵转换
- ✅ **插值算法**：线性插值 (LERP)、球面线性插值 (SLERP)、SQUAD
- ✅ **工具函数**：LookRotation、随机旋转、角度计算、角速度计算
- ✅ **零依赖**：仅使用 Python 标准库

## 安装

```python
# 直接导入使用
from quaternion_utils import Quaternion, from_euler, slerp
```

## 快速开始

### 创建四元数

```python
import math
from quaternion_utils import Quaternion, from_euler, from_axis_angle

# 单位四元数（无旋转）
q = Quaternion(1, 0, 0, 0)

# 从轴角创建（绕 Z 轴旋转 90 度）
q = from_axis_angle((0, 0, 1), math.pi / 2)

# 从欧拉角创建 (roll, pitch, yaw)
q = from_euler(0.5, 0.3, 0.8, 'XYZ')

# 快捷函数
from quaternion_utils import rotation_x, rotation_y, rotation_z
q = rotation_z(math.pi / 4)  # 绕 Z 轴旋转 45 度
```

### 旋转向量

```python
# 创建绕 Y 轴旋转 90 度的四元数
q = rotation_y(math.pi / 2)

# 旋转向量
v = (1, 0, 0)  # X 轴方向
rotated = q.rotate_vector(v)
# 结果: (0, 0, -1)  即 Z 轴负方向
```

### 转换到其他表示

```python
# 转换为轴角
axis, angle = q.to_axis_angle()

# 转换为欧拉角
roll, pitch, yaw = q.to_euler_angles('XYZ')

# 转换为旋转矩阵
matrix = q.to_rotation_matrix()
# 返回 3x3 矩阵，以三个行向量表示
```

### 四元数运算

```python
from quaternion_utils import identity

q1 = rotation_x(0.5)
q2 = rotation_y(0.3)

# 乘法（组合旋转）
q_combined = q2 * q1  # 先 q1 后 q2

# 加法（通常用于插值）
q_sum = q1 + q2

# 共轭
q_conj = q1.conjugate()

# 逆
q_inv = q1.inverse()

# 模长
mag = q1.magnitude()

# 归一化
q_normalized = q1.normalize()

# 点积
dot = q1.dot(q2)
```

### 插值

```python
from quaternion_utils import lerp, slerp

q1 = identity()
q2 = rotation_z(math.pi / 2)

# 线性插值（快速但非恒定角速度）
q_lerp = lerp(q1, q2, 0.5)

# 球面线性插值（恒定角速度，推荐）
q_slerp = slerp(q1, q2, 0.5)
```

### LookRotation

```python
from quaternion_utils import look_rotation

# 创建一个使对象朝向指定方向的四元数
forward = (1, 0, 0)  # 目标朝向
upwards = (0, 1, 0)  # 上方向
q = look_rotation(forward, upwards)

# 现在向量 forward 会被旋转到 X 轴正方向
```

### 其他工具函数

```python
from quaternion_utils import (
    angle_between,      # 两四元数间角度
    angular_velocity,    # 计算角速度
    random_rotation,     # 生成随机旋转
    from_two_vectors,    # 创建将 v1 旋转到 v2 的四元数
)

# 两四元数间的角度
angle = angle_between(q1, q2)

# 角速度计算
wx, wy, wz = angular_velocity(q1, q2, dt=1.0)

# 随机旋转（均匀分布）
q_random = random_rotation()

# 从两向量创建旋转
q = from_two_vectors((1, 0, 0), (0, 1, 0))  # X 轴转到 Y 轴
```

## API 参考

### Quaternion 类

| 方法 | 说明 |
|------|------|
| `magnitude()` | 返回模长 |
| `normalize()` | 返回单位四元数 |
| `conjugate()` | 返回共轭 |
| `inverse()` | 返回逆四元数 |
| `is_unit()` | 检查是否为单位四元数 |
| `dot(q)` | 计算点积 |
| `rotate_vector(v)` | 旋转向量 |
| `to_axis_angle()` | 转换为轴角 |
| `to_euler_angles(order)` | 转换为欧拉角 |
| `to_rotation_matrix()` | 转换为旋转矩阵 |

### 工厂函数

| 函数 | 说明 |
|------|------|
| `identity()` | 单位四元数 |
| `from_axis_angle(axis, angle)` | 从轴角创建 |
| `from_euler(roll, pitch, yaw, order)` | 从欧拉角创建 |
| `from_rotation_matrix(m)` | 从旋转矩阵创建 |
| `from_two_vectors(v1, v2)` | 创建 v1→v2 的旋转 |
| `rotation_x/y/z(angle)` | 绕轴旋转 |
| `look_rotation(forward, up)` | 朝向指定方向 |
| `random_rotation()` | 随机旋转 |

### 插值函数

| 函数 | 说明 |
|------|------|
| `lerp(q1, q2, t)` | 线性插值 |
| `slerp(q1, q2, t)` | 球面线性插值 |
| `squad(q1, a1, a2, q2, t)` | SQUAD 插值 |

## 数学背景

四元数是形如 `q = w + xi + yj + zk` 的数，其中 `i² = j² = k² = ijk = -1`。

### 为什么使用四元数？

相比欧拉角：
- 避免万向节锁 (Gimbal Lock)
- 插值更平滑
- 组合更简单

相比旋转矩阵：
- 存储更紧凑（4 个数 vs 9 个数）
- 计算更快
- 数值更稳定

### 运算规则

**乘法**（Hamilton 乘积）：
```
q1 * q2 = (w1w2 - x1x2 - y1y2 - z1z2) +
          (w1x2 + x1w2 + y1z2 - z1y2)i +
          (w1y2 - x1z2 + y1w2 + z1x2)j +
          (w1z2 + x1y2 - y1x2 + z1w2)k
```

**向量旋转**：
```
v' = q * v * q^(-1)
```
其中 v 是纯四元数 `(0, vx, vy, vz)`。

## 测试

```bash
python -m quaternion_utils.quaternion_test
```

## 应用场景

- 🎮 **游戏开发**：角色旋转、相机控制、动画插值
- 🤖 **机器人学**：姿态估计、运动学计算
- 🖼️ **计算机图形学**：3D 变换、骨骼动画
- ✈️ **航空航天**：飞行器姿态控制
- 📱 **移动应用**：AR/VR 方向追踪

## 许可证

MIT License