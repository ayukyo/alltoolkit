"""
四元数工具模块 (Quaternion Utilities)

四元数是一种用于表示 3D 旋转的数学工具，广泛应用于：
- 游戏开发（角色旋转、相机控制）
- 机器人学（姿态估计）
- 计算机图形学（动画插值）
- 航空航天（飞行器姿态控制）

相比欧拉角，四元数避免了万向节锁问题，插值更平滑。
"""

import math
from typing import Tuple, List, Optional, Union
from dataclasses import dataclass
from functools import total_ordering


@dataclass
@total_ordering
class Quaternion:
    """
    四元数类：q = w + xi + yj + zk
    
    属性:
        w: 标量部分（实部）
        x, y, z: 向量部分（虚部）
    """
    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __repr__(self) -> str:
        return f"Quaternion(w={self.w:.6f}, x={self.x:.6f}, y={self.y:.6f}, z={self.z:.6f})"
    
    def __str__(self) -> str:
        parts = []
        if self.w != 0:
            parts.append(f"{self.w:.4f}")
        if self.x != 0:
            parts.append(f"{'+' if self.x > 0 and parts else ''}{self.x:.4f}i")
        if self.y != 0:
            parts.append(f"{'+' if self.y > 0 and parts else ''}{self.y:.4f}j")
        if self.z != 0:
            parts.append(f"{'+' if self.z > 0 and parts else ''}{self.z:.4f}k")
        return ' '.join(parts) if parts else "0"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quaternion):
            return NotImplemented
        return (abs(self.w - other.w) < 1e-10 and
                abs(self.x - other.x) < 1e-10 and
                abs(self.y - other.y) < 1e-10 and
                abs(self.z - other.z) < 1e-10)
    
    def __lt__(self, other: 'Quaternion') -> bool:
        if not isinstance(other, Quaternion):
            return NotImplemented
        return self.magnitude() < other.magnitude()
    
    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        if not isinstance(other, Quaternion):
            raise TypeError(f"Cannot add Quaternion and {type(other)}")
        return Quaternion(
            self.w + other.w,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def __sub__(self, other: 'Quaternion') -> 'Quaternion':
        if not isinstance(other, Quaternion):
            raise TypeError(f"Cannot subtract Quaternion and {type(other)}")
        return Quaternion(
            self.w - other.w,
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
    
    def __mul__(self, other: Union['Quaternion', float, int]) -> 'Quaternion':
        """四元数乘法或标量乘法"""
        if isinstance(other, (int, float)):
            return Quaternion(
                self.w * other,
                self.x * other,
                self.y * other,
                self.z * other
            )
        elif isinstance(other, Quaternion):
            # Hamilton 乘积
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        else:
            raise TypeError(f"Cannot multiply Quaternion and {type(other)}")
    
    def __rmul__(self, other: Union[float, int]) -> 'Quaternion':
        """右乘标量"""
        return self.__mul__(other)
    
    def __truediv__(self, other: Union[float, int]) -> 'Quaternion':
        """标量除法"""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide quaternion by zero")
            return Quaternion(
                self.w / other,
                self.x / other,
                self.y / other,
                self.z / other
            )
        else:
            raise TypeError(f"Cannot divide Quaternion by {type(other)}")
    
    def __neg__(self) -> 'Quaternion':
        return Quaternion(-self.w, -self.x, -self.y, -self.z)
    
    def __abs__(self) -> float:
        """返回模长"""
        return self.magnitude()
    
    def magnitude(self) -> float:
        """计算四元数的模（长度）"""
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    
    def norm(self) -> float:
        """模的别名"""
        return self.magnitude()
    
    def conjugate(self) -> 'Quaternion':
        """返回共轭四元数"""
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    def inverse(self) -> 'Quaternion':
        """返回逆四元数（对于单位四元数，逆等于共轭）"""
        mag_sq = self.w**2 + self.x**2 + self.y**2 + self.z**2
        if mag_sq < 1e-10:
            raise ValueError("Cannot invert zero quaternion")
        conj = self.conjugate()
        return Quaternion(
            conj.w / mag_sq,
            conj.x / mag_sq,
            conj.y / mag_sq,
            conj.z / mag_sq
        )
    
    def normalize(self) -> 'Quaternion':
        """返回单位四元数"""
        mag = self.magnitude()
        if mag < 1e-10:
            raise ValueError("Cannot normalize zero quaternion")
        return Quaternion(
            self.w / mag,
            self.x / mag,
            self.y / mag,
            self.z / mag
        )
    
    def is_unit(self, tolerance: float = 1e-6) -> bool:
        """检查是否为单位四元数"""
        return abs(self.magnitude() - 1.0) < tolerance
    
    def dot(self, other: 'Quaternion') -> float:
        """计算两个四元数的点积"""
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z
    
    def to_tuple(self) -> Tuple[float, float, float, float]:
        """转换为元组 (w, x, y, z)"""
        return (self.w, self.x, self.y, self.z)
    
    def to_list(self) -> List[float]:
        """转换为列表 [w, x, y, z]"""
        return [self.w, self.x, self.y, self.z]
    
    def to_array(self):
        """转换为 numpy 数组（如果 numpy 可用）"""
        try:
            import numpy as np
            return np.array([self.w, self.x, self.y, self.z])
        except ImportError:
            raise ImportError("NumPy is required for to_array()")
    
    # ==================== 旋转相关方法 ====================
    
    def rotate_vector(self, v: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        使用四元数旋转向量
        
        公式: v' = q * v * q^(-1)
        
        参数:
            v: 三维向量 (x, y, z)
            
        返回:
            旋转后的向量 (x', y', z')
        """
        # 将向量表示为纯四元数
        p = Quaternion(0, v[0], v[1], v[2])
        # q * p * q^(-1)
        result = self * p * self.conjugate()
        return (result.x, result.y, result.z)
    
    def rotate_point(self, point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """rotate_vector 的别名"""
        return self.rotate_vector(point)
    
    def to_axis_angle(self) -> Tuple[Tuple[float, float, float], float]:
        """
        转换为轴角表示
        
        返回:
            (axis, angle): 轴向量和旋转角度（弧度）
        """
        q = self.normalize()
        
        # 处理特殊情况
        angle = 2 * math.acos(max(-1, min(1, q.w)))
        
        s = math.sqrt(1 - q.w * q.w)
        if s < 1e-10:
            # 角度接近0，任意轴都可以
            return ((1.0, 0.0, 0.0), 0.0)
        
        axis = (q.x / s, q.y / s, q.z / s)
        return (axis, angle)
    
    def to_euler_angles(self, order: str = 'XYZ') -> Tuple[float, float, float]:
        """
        转换为欧拉角（弧度）
        
        使用 intrinsic (body-frame) 旋转约定：
        - 'XYZ': roll→pitch→yaw (先 roll 后 pitch 后 yaw)
        - 'ZYX': yaw→pitch→roll (先 yaw 后 pitch 后 roll, 航空标准)
        
        参数:
            order: 旋转顺序
            
        返回:
            三个欧拉角（弧度）: (roll, pitch, yaw)
        """
        q = self.normalize()
        w, x, y, z = q.w, q.x, q.y, q.z
        
        if order.upper() == 'XYZ':
            # Intrinsic XYZ: q = qz_yaw * qy_pitch * qx_roll
            # 提取公式从旋转矩阵 R = Rz * Ry * Rx
            
            # R[0][2] = sin(pitch)
            sinp = 2 * (x * z + w * y)
            sinp = max(-1, min(1, sinp))
            pitch = math.asin(sinp)
            
            # yaw = atan2(-R[0][1], R[0][0])
            # R[0][1] = 2*(x*y - w*z)
            # R[0][0] = 1 - 2*(y*y + z*z)
            yaw = math.atan2(-2 * (x * y - w * z), 1 - 2 * (y * y + z * z))
            
            # roll = atan2(-R[1][2], R[2][2])
            # R[1][2] = 2*(y*z - w*x)
            # R[2][2] = 1 - 2*(x*x + y*y)
            roll = math.atan2(-2 * (y * z - w * x), 1 - 2 * (x * x + y * y))
            
            return (roll, pitch, yaw)
        
        elif order.upper() == 'ZYX':
            # Intrinsic ZYX: q = qx_roll * qy_pitch * qz_yaw
            # 航空标准：先 yaw (Z), 后 pitch (Y), 后 roll (X)
            
            # pitch = asin(2*(w*y - z*x))
            sinp = 2 * (w * y - z * x)
            sinp = max(-1, min(1, sinp))
            pitch = math.asin(sinp)
            
            # yaw = atan2(2*(w*z + x*y), 1 - 2*(y*y + z*z))
            yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
            
            # roll = atan2(2*(w*x + y*z), 1 - 2*(x*x + y*y))
            roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
            
            return (roll, pitch, yaw)
        
        else:
            raise ValueError(f"Unsupported rotation order: {order}")
    
    def to_rotation_matrix(self) -> Tuple[Tuple[float, float, float], 
                                          Tuple[float, float, float], 
                                          Tuple[float, float, float]]:
        """
        转换为 3x3 旋转矩阵
        
        返回:
            3x3 旋转矩阵，以三个行向量表示
        """
        q = self.normalize()
        w, x, y, z = q.w, q.x, q.y, q.z
        
        row1 = (
            1 - 2*(y*y + z*z),
            2*(x*y - w*z),
            2*(x*z + w*y)
        )
        row2 = (
            2*(x*y + w*z),
            1 - 2*(x*x + z*z),
            2*(y*z - w*x)
        )
        row3 = (
            2*(x*z - w*y),
            2*(y*z + w*x),
            1 - 2*(x*x + y*y)
        )
        
        return (row1, row2, row3)
    
    @classmethod
    def from_axis_angle(cls, axis: Tuple[float, float, float], 
                        angle: float) -> 'Quaternion':
        """
        从轴角表示创建四元数
        
        参数:
            axis: 旋转轴向量（会被归一化）
            angle: 旋转角度（弧度）
            
        返回:
            表示该旋转的四元数
        """
        # 归一化轴
        mag = math.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)
        if mag < 1e-10:
            raise ValueError("Axis cannot be zero vector")
        
        ax, ay, az = axis[0]/mag, axis[1]/mag, axis[2]/mag
        
        half_angle = angle / 2
        s = math.sin(half_angle)
        
        return cls(
            w=math.cos(half_angle),
            x=ax * s,
            y=ay * s,
            z=az * s
        )
    
    @classmethod
    def from_euler_angles(cls, roll: float, pitch: float, yaw: float,
                          order: str = 'XYZ') -> 'Quaternion':
        """
        从欧拉角创建四元数
        
        使用 intrinsic (body-frame) 旋转约定：
        - 'XYZ': roll→pitch→yaw (先 roll 后 pitch 后 yaw)
        - 'ZYX': yaw→pitch→roll (先 yaw 后 pitch 后 roll, 航空标准)
        
        参数:
            roll: X 轴旋转角度（弧度）
            pitch: Y 轴旋转角度（弧度）
            yaw: Z 轴旋转角度（弧度）
            order: 旋转顺序
            
        返回:
            表示该旋转的四元数
        """
        cr, cp, cy = math.cos(roll/2), math.cos(pitch/2), math.cos(yaw/2)
        sr, sp, sy = math.sin(roll/2), math.sin(pitch/2), math.sin(yaw/2)
        
        if order.upper() == 'XYZ':
            # Intrinsic XYZ: q = qz_yaw * qy_pitch * qx_roll
            # 即先 roll (X), 后 pitch (Y), 后 yaw (Z) 在 body frame
            w = cr * cp * cy - sr * sp * sy
            x = sr * cp * cy + cr * sp * sy
            y = cr * sp * cy - sr * cp * sy
            z = cr * cp * sy + sr * sp * cy
            
            return cls(w, x, y, z)
        
        elif order.upper() == 'ZYX':
            # Intrinsic ZYX: q = qx_roll * qy_pitch * qz_yaw
            # 即先 yaw (Z), 后 pitch (Y), 后 roll (X) 在 body frame
            w = cr * cp * cy + sr * sp * sy
            x = sr * cp * cy - cr * sp * sy
            y = cr * sp * cy + sr * cp * sy
            z = cr * cp * sy - sr * sp * cy
            
            return cls(w, x, y, z)
        
        else:
            raise ValueError(f"Unsupported rotation order: {order}")
    
    @classmethod
    def from_rotation_matrix(cls, m11: float, m12: float, m13: float,
                            m21: float, m22: float, m23: float,
                            m31: float, m32: float, m33: float) -> 'Quaternion':
        """
        从 3x3 旋转矩阵创建四元数
        
        参数:
            m11-m33: 旋转矩阵的 9 个元素（行优先）
            
        返回:
            对应的四元数
        """
        trace = m11 + m22 + m33
        
        if trace > 0:
            s = 0.5 / math.sqrt(trace + 1.0)
            w = 0.25 / s
            x = (m32 - m23) * s
            y = (m13 - m31) * s
            z = (m21 - m12) * s
        elif m11 > m22 and m11 > m33:
            s = 2.0 * math.sqrt(1.0 + m11 - m22 - m33)
            w = (m32 - m23) / s
            x = 0.25 * s
            y = (m12 + m21) / s
            z = (m13 + m31) / s
        elif m22 > m33:
            s = 2.0 * math.sqrt(1.0 + m22 - m11 - m33)
            w = (m13 - m31) / s
            x = (m12 + m21) / s
            y = 0.25 * s
            z = (m23 + m32) / s
        else:
            s = 2.0 * math.sqrt(1.0 + m33 - m11 - m22)
            w = (m21 - m12) / s
            x = (m13 + m31) / s
            y = (m23 + m32) / s
            z = 0.25 * s
        
        return cls(w, x, y, z).normalize()
    
    @classmethod
    def from_two_vectors(cls, v1: Tuple[float, float, float],
                        v2: Tuple[float, float, float]) -> 'Quaternion':
        """
        创建将向量 v1 旋转到向量 v2 的四元数
        
        参数:
            v1: 起始向量
            v2: 目标向量
            
        返回:
            表示该旋转的四元数
        """
        # 归一化
        mag1 = math.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
        mag2 = math.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
        
        if mag1 < 1e-10 or mag2 < 1e-10:
            raise ValueError("Vectors cannot be zero")
        
        u1 = (v1[0]/mag1, v1[1]/mag1, v1[2]/mag1)
        u2 = (v2[0]/mag2, v2[1]/mag2, v2[2]/mag2)
        
        # 点积
        dot = u1[0]*u2[0] + u1[1]*u2[1] + u1[2]*u2[2]
        
        # 向量相同
        if dot > 0.999999:
            return cls(1, 0, 0, 0)  # 单位四元数
        
        # 向量相反
        if dot < -0.999999:
            # 找一个垂直轴旋转180度
            if abs(u1[0]) > 0.5:
                axis = (-u1[2], 0, u1[0])
            else:
                axis = (0, u1[2], -u1[1])
            mag = math.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)
            axis = (axis[0]/mag, axis[1]/mag, axis[2]/mag)
            return cls(0, axis[0], axis[1], axis[2])
        
        # 叉积
        cross = (
            u1[1]*u2[2] - u1[2]*u2[1],
            u1[2]*u2[0] - u1[0]*u2[2],
            u1[0]*u2[1] - u1[1]*u2[0]
        )
        
        s = math.sqrt((1 + dot) * 2)
        inv_s = 1.0 / s
        
        return cls(
            s * 0.5,
            cross[0] * inv_s,
            cross[1] * inv_s,
            cross[2] * inv_s
        ).normalize()


# ==================== 工厂函数 ====================

def identity() -> 'Quaternion':
    """返回单位四元数（无旋转）"""
    return Quaternion(1, 0, 0, 0)


def from_axis_angle(axis: Tuple[float, float, float], angle: float) -> 'Quaternion':
    """从轴角创建四元数"""
    return Quaternion.from_axis_angle(axis, angle)


def from_euler(roll: float, pitch: float, yaw: float, order: str = 'XYZ') -> 'Quaternion':
    """从欧拉角创建四元数"""
    return Quaternion.from_euler_angles(roll, pitch, yaw, order)


def from_rotation_matrix(matrix: Tuple[Tuple[float, float, float], 
                                       Tuple[float, float, float], 
                                       Tuple[float, float, float]]) -> 'Quaternion':
    """从旋转矩阵创建四元数"""
    m = matrix
    return Quaternion.from_rotation_matrix(
        m[0][0], m[0][1], m[0][2],
        m[1][0], m[1][1], m[1][2],
        m[2][0], m[2][1], m[2][2]
    )


def from_two_vectors(v1: Tuple[float, float, float], 
                     v2: Tuple[float, float, float]) -> 'Quaternion':
    """创建将 v1 旋转到 v2 的四元数"""
    return Quaternion.from_two_vectors(v1, v2)


# ==================== 插值函数 ====================

def lerp(q1: 'Quaternion', q2: 'Quaternion', t: float) -> 'Quaternion':
    """
    线性插值两个四元数
    
    参数:
        q1: 起始四元数
        q2: 结束四元数
        t: 插值参数 [0, 1]
        
    返回:
        插值后的四元数（需要手动归一化）
    """
    if t < 0 or t > 1:
        raise ValueError(f"t must be in [0, 1], got {t}")
    
    return Quaternion(
        q1.w + t * (q2.w - q1.w),
        q1.x + t * (q2.x - q1.x),
        q1.y + t * (q2.y - q1.y),
        q1.z + t * (q2.z - q1.z)
    ).normalize()


def slerp(q1: 'Quaternion', q2: 'Quaternion', t: float, 
          shortest_path: bool = True) -> 'Quaternion':
    """
    球面线性插值（Spherical Linear Interpolation）
    
    这是四元数插值的标准方法，产生恒定角速度的旋转。
    
    参数:
        q1: 起始四元数
        q2: 结束四元数
        t: 插值参数 [0, 1]
        shortest_path: 是否选择最短路径
        
    返回:
        插值后的四元数
    """
    if t < 0 or t > 1:
        raise ValueError(f"t must be in [0, 1], got {t}")
    
    # 归一化输入
    q1 = q1.normalize()
    q2 = q2.normalize()
    
    # 计算点积
    dot = q1.dot(q2)
    
    # 选择最短路径
    if shortest_path and dot < 0:
        dot = -dot
        q2 = -q2
    
    # 四元数非常接近时，使用线性插值避免数值问题
    if dot > 0.9995:
        return lerp(q1, q2, t)
    
    # 限制在 [-1, 1] 范围内避免数值问题
    dot = max(-1, min(1, dot))
    
    theta_0 = math.acos(dot)
    theta = theta_0 * t
    
    # 计算正交分量
    sin_theta_0 = math.sin(theta_0)
    if abs(sin_theta_0) < 1e-10:
        return q1
    
    sin_theta = math.sin(theta)
    
    s1 = math.cos(theta) - dot * sin_theta / sin_theta_0
    s2 = sin_theta / sin_theta_0
    
    return Quaternion(
        s1 * q1.w + s2 * q2.w,
        s1 * q1.x + s2 * q2.x,
        s1 * q1.y + s2 * q2.y,
        s1 * q1.z + s2 * q2.z
    )


def squad(q1: 'Quaternion', a1: 'Quaternion', a2: 'Quaternion', q2: 'Quaternion',
          t: float) -> 'Quaternion':
    """
    SQUAD (Spherical and Quadrangle) 插值
    
    用于平滑插值多个四元数，C1 连续。
    
    参数:
        q1: 起始四元数
        a1: 第一个控制点
        a2: 第二个控制点
        q2: 结束四元数
        t: 插值参数 [0, 1]
        
    返回:
        插值后的四元数
    """
    slerp_t = slerp(q1, q2, t)
    slerp_a = slerp(a1, a2, t)
    return slerp(slerp_t, slerp_a, 2 * t * (1 - t))


# ==================== 工具函数 ====================

def angle_between(q1: 'Quaternion', q2: 'Quaternion') -> float:
    """
    计算两个四元数之间的角度（弧度）
    
    这是旋转 q1^(-1) * q2 的角度。
    """
    q1 = q1.normalize()
    q2 = q2.normalize()
    dot = abs(q1.dot(q2))
    dot = max(-1, min(1, dot))  # Clamp to avoid numerical issues
    return 2 * math.acos(dot)


def angular_velocity(q1: 'Quaternion', q2: 'Quaternion', dt: float) -> Tuple[float, float, float]:
    """
    计算从 q1 到 q2 的角速度向量
    
    参数:
        q1: 起始四元数
        q2: 结束四元数
        dt: 时间间隔（秒）
        
    返回:
        角速度向量 (wx, wy, wz)，单位：弧度/秒
    """
    if dt <= 0:
        raise ValueError("dt must be positive")
    
    # q_diff = q2 * q1^(-1)
    q_diff = q2 * q1.conjugate()
    q_diff = q_diff.normalize()
    
    # 从轴角表示获取角速度
    axis, angle = q_diff.to_axis_angle()
    
    return (axis[0] * angle / dt, axis[1] * angle / dt, axis[2] * angle / dt)


def look_rotation(forward: Tuple[float, float, float],
                  upwards: Tuple[float, float, float] = (0, 1, 0)) -> 'Quaternion':
    """
    创建一个使对象朝向指定方向的四元数
    
    类似 Unity 的 Quaternion.LookRotation
    
    参数:
        forward: 前方向（目标朝向）
        upwards: 上方向（用于确定朝向）
        
    返回:
        表示该朝向的四元数
    """
    # 归一化 forward
    mag = math.sqrt(forward[0]**2 + forward[1]**2 + forward[2]**2)
    if mag < 1e-10:
        raise ValueError("Forward vector cannot be zero")
    f = (forward[0]/mag, forward[1]/mag, forward[2]/mag)
    
    # 归一化 upwards
    mag = math.sqrt(upwards[0]**2 + upwards[1]**2 + upwards[2]**2)
    if mag < 1e-10:
        upwards = (0, 1, 0)
    else:
        upwards = (upwards[0]/mag, upwards[1]/mag, upwards[2]/mag)
    
    # 右向量 = forward × upwards
    right = (
        f[1] * upwards[2] - f[2] * upwards[1],
        f[2] * upwards[0] - f[0] * upwards[2],
        f[0] * upwards[1] - f[1] * upwards[0]
    )
    mag = math.sqrt(right[0]**2 + right[1]**2 + right[2]**2)
    if mag < 1e-10:
        # forward 与 upwards 平行
        return identity()
    right = (right[0]/mag, right[1]/mag, right[2]/mag)
    
    # 重新计算 up = right × forward
    up = (
        right[1] * f[2] - right[2] * f[1],
        right[2] * f[0] - right[0] * f[2],
        right[0] * f[1] - right[1] * f[0]
    )
    
    # 构建旋转矩阵
    m = (
        (right[0], right[1], right[2]),
        (up[0], up[1], up[2]),
        (f[0], f[1], f[2])
    )
    
    return from_rotation_matrix(m)


def random_rotation() -> 'Quaternion':
    """
    生成随机单位四元数（均匀分布在旋转空间）
    
    使用 Marsaglia 方法确保均匀分布。
    """
    import random
    
    u1 = random.random()
    u2 = random.random()
    u3 = random.random()
    
    s1 = math.sqrt(1 - u1)
    s2 = math.sqrt(u1)
    
    theta1 = 2 * math.pi * u2
    theta2 = 2 * math.pi * u3
    
    return Quaternion(
        w=s1 * math.sin(theta1),
        x=s1 * math.cos(theta1),
        y=s2 * math.sin(theta2),
        z=s2 * math.cos(theta2)
    )


def rotation_x(angle: float) -> 'Quaternion':
    """绕 X 轴旋转 angle 弧度"""
    half = angle / 2
    return Quaternion(math.cos(half), math.sin(half), 0, 0)


def rotation_y(angle: float) -> 'Quaternion':
    """绕 Y 轴旋转 angle 弧度"""
    half = angle / 2
    return Quaternion(math.cos(half), 0, math.sin(half), 0)


def rotation_z(angle: float) -> 'Quaternion':
    """绕 Z 轴旋转 angle 弧度"""
    half = angle / 2
    return Quaternion(math.cos(half), 0, 0, math.sin(half))


# 导出公共 API
__all__ = [
    'Quaternion',
    'identity',
    'from_axis_angle',
    'from_euler',
    'from_rotation_matrix',
    'from_two_vectors',
    'lerp',
    'slerp',
    'squad',
    'angle_between',
    'angular_velocity',
    'look_rotation',
    'random_rotation',
    'rotation_x',
    'rotation_y',
    'rotation_z',
]